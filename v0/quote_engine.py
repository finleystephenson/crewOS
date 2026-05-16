"""
Crew OS — v0 quote engine.

Given a structured pilot intake (customer info + job description + trader profile),
produces a branded HTML quote and emails it to the trader for review.

Pure-Python, single file. No Anthropic — Groq Llama-3.3-70B only.
Runs locally or inside a GitHub Actions workflow with secrets.

Inputs (intake.json):
    {
      "customer":   {"name": str, "email": str, "address": str},
      "trader":     {"business_name", "owner_name", "email",
                     "phone", "address", "registration_numbers",
                     "vat_registered" (bool), "vat_number"|null,
                     "hourly_rate_gbp" (int), "callout_fee_gbp" (int)},
      "job":        {"trade": str, "description": str, "site_visit_notes": str}
    }

Outputs:
    - HTML email body
    - Sent to trader's email via Resend
    - Returns (success: bool, message_id_or_err: str)

Env required: GROQ_API_KEY, RESEND_API_KEY.
"""
from __future__ import annotations
import json
import os
import sys
import datetime as dt
from pathlib import Path
from typing import Any

import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
RESEND_URL = "https://api.resend.com/emails"

GROQ_MODEL = "llama-3.3-70b-versatile"

TEMPLATES_DIR = Path(__file__).parent / "templates"

SYSTEM_PROMPT = """\
You are a quote-writing assistant for UK trade businesses (1-5 person crews:
electrical, plumbing, heating, building, groundworks). You produce realistic,
defensible client quotes that read like a tradesperson wrote them.

Rules:
- Break the job into discrete line items. Each line has: description (UK trade
  language, plain), quantity, unit ("hours" or "fixed"), unit_price_gbp.
- Estimate labour time conservatively. A 1-5 person crew, not a 20-person shop.
- Materials line items reflect typical UK retail + 10-15% markup. Be specific
  ("4-gang chrome socket faceplate", not "sockets").
- Include the trader's callout fee as its own line if it applies.
- VAT: if vat_registered, add 20% VAT line. Otherwise no VAT.
- Round labour hours to the nearest half-hour. Round prices to the nearest £5.
- Payment terms: 50% on acceptance, 50% on completion, unless job < £500 where
  payment-on-completion is fine.
- Valid for 30 days from today.
- Do NOT include speculative work not mentioned in the description.
- Do NOT make up certifications, regulations, or registration numbers the trader
  didn't supply.

Return ONLY valid JSON matching this exact schema, no markdown fences, no prose:
{
  "summary": "<one short line summarising the job>",
  "line_items": [
    {"description": str, "quantity": number, "unit": "hours"|"fixed",
     "unit_price_gbp": number, "subtotal_gbp": number}
  ],
  "subtotal_gbp": number,
  "vat_gbp": number,
  "total_gbp": number,
  "payment_terms": str,
  "valid_until": "YYYY-MM-DD",
  "notes": "<optional short note from the trader to the customer; can be empty>"
}
"""


def _call_groq(messages: list[dict], temperature: float = 0.2) -> str:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY not set in env")
    resp = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": GROQ_MODEL,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def generate_quote(intake: dict[str, Any]) -> dict[str, Any]:
    """Call Groq, parse JSON, return structured quote."""
    today = dt.date.today().isoformat()
    valid_until = (dt.date.today() + dt.timedelta(days=30)).isoformat()
    user_prompt = (
        f"TODAY'S DATE: {today}\n"
        f"DEFAULT VALID_UNTIL: {valid_until}\n\n"
        f"TRADER PROFILE:\n{json.dumps(intake['trader'], indent=2)}\n\n"
        f"JOB:\n{json.dumps(intake['job'], indent=2)}\n\n"
        f"CUSTOMER:\n{json.dumps(intake['customer'], indent=2)}\n\n"
        f"Produce the JSON quote now."
    )
    raw = _call_groq(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )
    return json.loads(raw)


def render_quote_html(intake: dict[str, Any], quote: dict[str, Any]) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    tpl = env.get_template("quote_email.html")
    return tpl.render(
        intake=intake,
        quote=quote,
        generated_at=dt.datetime.now().strftime("%-d %B %Y at %H:%M"),
    )


def send_via_resend(
    *,
    to_email: str,
    subject: str,
    html: str,
    reply_to: str | None = None,
    cc: list[str] | None = None,
) -> tuple[bool, str]:
    key = os.environ.get("RESEND_API_KEY")
    if not key:
        return (False, "RESEND_API_KEY not set")
    payload: dict[str, Any] = {
        "from": "Crew OS <quotes@crewos.co.uk>",
        "to": [to_email],
        "subject": subject,
        "html": html,
    }
    if reply_to:
        payload["reply_to"] = reply_to
    if cc:
        payload["cc"] = cc
    resp = requests.post(
        RESEND_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    if resp.status_code >= 400:
        return (False, f"{resp.status_code}: {resp.text[:400]}")
    return (True, resp.json().get("id", "no-id"))


def process(intake: dict[str, Any], *, send: bool = True) -> dict[str, Any]:
    """Full pipeline. Returns a result dict suitable for logging."""
    started = dt.datetime.utcnow().isoformat()
    quote = generate_quote(intake)
    html = render_quote_html(intake, quote)

    result: dict[str, Any] = {
        "started_at": started,
        "trader_email": intake["trader"]["email"],
        "customer_email": intake["customer"]["email"],
        "summary": quote.get("summary"),
        "total_gbp": quote.get("total_gbp"),
        "quote": quote,
    }

    if not send:
        result["status"] = "rendered_only"
        result["html_preview_chars"] = len(html)
        return result

    subject = (
        f"Crew OS draft quote — {quote.get('summary', 'job')[:60]} — "
        f"£{quote.get('total_gbp', 0):,.0f}"
    )
    ok, info = send_via_resend(
        to_email=intake["trader"]["email"],
        subject=subject,
        html=html,
        reply_to="hello@crewos.co.uk",
    )
    result["sent"] = ok
    result["resend_id_or_err"] = info
    result["status"] = "sent" if ok else "send_failed"
    return result


def _main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python quote_engine.py <intake.json> [--no-send]", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    send = "--no-send" not in sys.argv
    intake = json.loads(path.read_text())
    result = process(intake, send=send)
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") in ("sent", "rendered_only") else 1


if __name__ == "__main__":
    raise SystemExit(_main())
