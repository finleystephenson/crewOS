"""
Cold email batch — sends a small daily batch from outbound/targets.csv via Resend.

Conservative-by-default:
- Daily cap (DAILY_CAP env, default 3 during warmup).
- 30-day re-contact lockout (won't email a target twice within 30 days).
- Skips any row where reply_at is non-empty.
- Uses Groq Llama-3.3-70B to personalise the message body using the row's profile.

Env: GROQ_API_KEY, RESEND_API_KEY.
"""
from __future__ import annotations
import csv
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from v0.quote_engine import _call_groq, send_via_resend  # noqa: E402
from scripts import suppressions  # noqa: E402

TARGETS_CSV = ROOT / "outbound" / "targets.csv"
SENT_CSV = ROOT / "outbound" / "sent.csv"

DAILY_CAP = int(os.environ.get("DAILY_CAP", "3"))


COLD_SYSTEM_PROMPT = """\
You are writing a cold email FROM Crew OS, an AI-built tool for UK trade
businesses (1-5 person crews) that turns a site-visit description into a sent
client quote in under 10 minutes. £49/month after a 14-day free pilot, no card.

The email must:
- Be addressed to a real UK tradesperson by first name.
- Open with a specific, on-the-record detail from their business profile
  (their trade, their town, or something equivalent in the profile dict).
- Be plain text — no HTML, no signatures with images.
- Be under 130 words.
- Have a single ask: reply with "send it" if they want the pilot intake.
- Be honest about being from an AI and built on a transparent experiment.
- NEVER fabricate a fact about the trader.

Return ONLY the email body — no subject, no JSON, no markdown fence.
"""


def _personalise(row: dict[str, str]) -> str:
    user = (
        "TARGET PROFILE:\n"
        f"- first_name: {row.get('first_name', '')}\n"
        f"- business: {row.get('business_name', '')}\n"
        f"- trade: {row.get('trade', '')}\n"
        f"- town: {row.get('town', '')}\n"
        f"- source: {row.get('source_url', '')}\n"
        "Write the cold email now."
    )
    return _call_groq(
        [
            {"role": "system", "content": COLD_SYSTEM_PROMPT},
            {"role": "user", "content": user},
        ],
        temperature=0.4,
    ).strip()


def _subject(row: dict[str, str]) -> str:
    return f"Quoting take an hour for {row.get('business_name','your crew')}?"


def _read_targets() -> list[dict[str, str]]:
    if not TARGETS_CSV.exists():
        return []
    with TARGETS_CSV.open() as f:
        return list(csv.DictReader(f))


def _write_targets(rows: list[dict[str, str]], headers: list[str]) -> None:
    with TARGETS_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _append_sent(row: dict[str, Any]) -> None:
    SENT_CSV.parent.mkdir(exist_ok=True)
    existed = SENT_CSV.exists()
    with SENT_CSV.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not existed:
            w.writeheader()
        w.writerow(row)


def _is_eligible(row: dict[str, str], now: dt.datetime, suppressed: set[str]) -> bool:
    email = (row.get("email") or "").strip().lower()
    if not email or "@" not in email:
        return False
    if email in suppressed:
        return False
    if row.get("country", "UK").upper() != "UK":
        return False
    if row.get("reply_at"):
        return False
    sent_at = row.get("sent_at")
    if sent_at:
        try:
            t = dt.datetime.fromisoformat(sent_at.replace("Z", "+00:00"))
            if (now - t.replace(tzinfo=None)).days < 30:
                return False
        except Exception:
            pass  # malformed → treat as never sent
    return True


def _send_html_wrap(plain_body: str) -> str:
    paras = [p.strip() for p in plain_body.split("\n\n") if p.strip()]
    body_html = "".join(f"<p>{p}</p>" for p in paras)
    return f"""<!doctype html><html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:#0f0f0f;line-height:1.55;max-width:560px;margin:0 auto;padding:24px;font-size:15px;">
{body_html}
<hr style="margin:24px 0;border:none;border-top:1px solid #e5e0d4;">
<p style="font-size:11px;color:#6b6b6b;">Crew OS — built by Claude (AI), founded by Finley Stephenson. This email was written by an AI agent. Reply to reach a human (or another AI; we're transparent either way). <a href="https://crewos.co.uk" style="color:#6b6b6b;">crewos.co.uk</a></p>
<p style="font-size:11px;color:#6b6b6b;">Unsubscribe: reply with the word "stop" and we'll never email this address again. We are a UK business contacting business addresses under PECR; if this address is personal, tell us and we'll remove it immediately.</p>
</body></html>"""


def run() -> dict[str, Any]:
    rows = _read_targets()
    if not rows:
        return {"status": "no_targets", "sent": 0}

    headers = list(rows[0].keys())
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    suppressed = suppressions.load()
    eligible = [r for r in rows if _is_eligible(r, now, suppressed)]
    batch = eligible[:DAILY_CAP]
    results: list[dict[str, Any]] = []

    for row in batch:
        try:
            body_text = _personalise(row)
            html = _send_html_wrap(body_text)
            ok, info = send_via_resend(
                to_email=row["email"],
                subject=_subject(row),
                html=html,
                reply_to="hello@crewos.co.uk",
            )
            row["sent_at"] = now.isoformat(timespec="seconds") + "Z"
            _append_sent(
                {
                    "ts": row["sent_at"],
                    "email": row["email"],
                    "business_name": row.get("business_name", ""),
                    "trade": row.get("trade", ""),
                    "subject": _subject(row),
                    "body_preview": body_text[:240].replace("\n", " "),
                    "ok": ok,
                    "resend_id_or_err": info,
                }
            )
            results.append({"email": row["email"], "ok": ok, "info": info})
        except Exception as e:
            results.append({"email": row["email"], "ok": False, "info": f"exception: {e}"[:300]})

    _write_targets(rows, headers)
    return {"status": "ran", "eligible": len(eligible), "sent": len(batch), "results": results}


def _main() -> int:
    print(json.dumps(run(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
