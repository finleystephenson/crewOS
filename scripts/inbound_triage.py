"""
Inbound triage orchestrator.

Pulls classified messages from gmail_poll, takes the right action for each:
- pilot_signup     → send onboarding email with intake template, log to outbound/signups.csv
- intake_reply     → write intake-queue/<ts>.json for the quote-engine to pick up
- cold_reply       → log to outbound/replies.csv; auto-acknowledge; classify sentiment
- needs_human      → log to outbound/needs_human.csv; STATE.md gets a 🟡 if pile grows

Env required: GMAIL_USERNAME, GMAIL_APP_PASSWORD, GROQ_API_KEY, RESEND_API_KEY.

Idempotency: gmail_poll labels every processed message with crew-os/seen,
so re-runs only handle new mail.
"""
from __future__ import annotations
import csv
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any

# Allow running from repo root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts import gmail_poll, suppressions  # noqa: E402
from v0.quote_engine import send_via_resend  # noqa: E402

INTAKE_QUEUE = ROOT / "intake-queue"
OUTBOUND = ROOT / "outbound"
INTAKE_QUEUE.mkdir(exist_ok=True)
OUTBOUND.mkdir(exist_ok=True)


ONBOARDING_HTML_TEMPLATE = """\
<!doctype html>
<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:#0f0f0f;line-height:1.55;max-width:600px;margin:0 auto;padding:24px;">
<p style="font-family:Georgia,serif;font-size:22px;font-weight:700;margin:0 0 6px;">Welcome to the Crew OS pilot.</p>
<p style="color:#6b6b6b;margin:0 0 18px;">Day 1 of 14, no card, no obligation.</p>

<p>You're in. Here's how the 14-day pilot works for you:</p>
<ol style="padding-left:18px;">
  <li>Reply to this email with the template below filled in (just plain text — your reply parses automatically).</li>
  <li>Within ~10 minutes you get a draft quote back, written in your pricing voice.</li>
  <li>Review it. If it's good, forward to your customer. If not, hit reply and tell me what's off — we'll improve before the next one.</li>
  <li>Do this for as many real jobs as you like in the next 14 days. After, £49/mo if it's earning its keep. £0 if not. No card needed either way.</li>
</ol>

<p style="margin-top:22px;"><strong>Reply to this email with the lines below filled in:</strong></p>

<pre style="background:#f6f3ec;border:1px solid #1a1a1a;padding:14px;font-size:13px;line-height:1.45;white-space:pre-wrap;">CREW-OS-INTAKE-V1

Customer name:
Customer email:
Customer address:

Business name:
Your name:
Your email:
Your phone:
Your address:
Registration numbers:
VAT registered: no
VAT number:
Hourly rate: 45
Callout fee: 50

Trade: electrical
Job description:
Site visit notes: </pre>

<p style="margin-top:22px;font-size:13px;color:#6b6b6b;">Leave the <code>CREW-OS-INTAKE-V1</code> marker line — that's how we route your reply to the engine.</p>

<hr style="margin:24px 0;border:none;border-top:1px solid #e5e0d4;">

<p style="font-size:11px;color:#6b6b6b;">Built by Claude (AI), founded by Finley Stephenson. This email was written by an AI agent. Reply to reach a human (or another AI; we're transparent either way). <a href="https://crewos.co.uk" style="color:#6b6b6b;">crewos.co.uk</a></p>
</body></html>
"""


def _csv_append(path: Path, row: dict[str, Any]) -> None:
    existed = path.exists()
    with path.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not existed:
            w.writeheader()
        w.writerow(row)


def _now_iso() -> str:
    return dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"


def handle_pilot_signup(item: dict[str, Any]) -> dict[str, Any]:
    email_addr = item.get("applicant_email") or _extract_addr(item.get("from", ""))
    if not email_addr:
        return {"action": "skipped_no_email", "item": item}
    ok, info = send_via_resend(
        to_email=email_addr,
        subject="Welcome to the Crew OS pilot — your intake template",
        html=ONBOARDING_HTML_TEMPLATE,
        reply_to="hello@crewos.co.uk",
    )
    _csv_append(
        OUTBOUND / "signups.csv",
        {
            "ts": _now_iso(),
            "email": email_addr,
            "source": "formspree",
            "onboarding_sent": ok,
            "resend_id_or_err": info,
        },
    )
    return {"action": "onboarding_sent" if ok else "onboarding_failed", "email": email_addr, "info": info}


def handle_intake_reply(item: dict[str, Any]) -> dict[str, Any]:
    intake = item["intake"]
    # Basic validation: trader email and job description must be present.
    missing = []
    if not intake["trader"]["email"]:
        missing.append("trader.email")
    if not intake["job"]["description"]:
        missing.append("job.description")
    if missing:
        # Bounce back asking for the missing piece.
        msg = (
            "<p>Thanks for the reply — we couldn't queue this job because the following are missing:</p>"
            f"<ul>{''.join(f'<li>{m}</li>' for m in missing)}</ul>"
            "<p>Hit reply with the filled lines and we'll run it.</p>"
        )
        send_via_resend(
            to_email=_extract_addr(item.get("from", "")),
            subject="Re: Crew OS pilot — quick missing field",
            html=msg,
            reply_to="hello@crewos.co.uk",
        )
        return {"action": "intake_bounced_missing_fields", "missing": missing}

    ts = _now_iso().replace(":", "").replace("-", "")
    out_path = INTAKE_QUEUE / f"{ts}.json"
    out_path.write_text(json.dumps(intake, indent=2))
    _csv_append(
        OUTBOUND / "intakes.csv",
        {"ts": _now_iso(), "trader": intake["trader"]["email"], "queued_path": str(out_path.relative_to(ROOT))},
    )
    return {"action": "intake_queued", "path": str(out_path.relative_to(ROOT))}


def handle_cold_reply(item: dict[str, Any]) -> dict[str, Any]:
    body_preview = item.get("body_preview") or ""
    sender_email = _extract_addr(item.get("from", ""))

    _csv_append(
        OUTBOUND / "cold_replies.csv",
        {
            "ts": _now_iso(),
            "from": item.get("from", ""),
            "subject": item.get("subject", ""),
            "preview": body_preview[:400],
        },
    )

    # Did they reply with "send it"? That's our cold-email CTA — promote to
    # full pilot-signup flow (onboarding template, not just an ack).
    import re as _re
    body_lower = (body_preview or "").lower()
    body_stripped = _re.sub(r"^\s*>.*$", "", body_lower, flags=_re.M).strip()
    if sender_email and (
        body_stripped.startswith("send it")
        or _re.search(r"\bsend it\b", body_lower[:300])
        or _re.search(r"\b(yes|im in|i'm in|i am in|count me in|sign me up)\b", body_stripped[:120])
    ):
        return handle_pilot_signup({"applicant_email": sender_email, "from": item.get("from", "")})

    # Suppression check — honour the unsubscribe promise made in every cold email.
    if sender_email and suppressions.should_suppress(body_preview):
        added = suppressions.add(
            sender_email,
            reason=f"cold reply requested removal — subject: {item.get('subject','')[:120]}",
            source="cold_reply_auto",
        )
        # Send a one-line confirmation (no further follow-up).
        send_via_resend(
            to_email=sender_email,
            subject="You're off the list",
            html=(
                "<p>Done. We've added you to our suppression list and you won't "
                "receive any further emails from Crew OS.</p>"
                "<p>If this was a mistake, reply once and a human will see it on or after May 29.</p>"
            ),
            reply_to="hello@crewos.co.uk",
        )
        return {
            "action": "suppressed_via_reply",
            "from": sender_email,
            "newly_added": added,
        }

    # Otherwise auto-acknowledge.
    send_via_resend(
        to_email=sender_email,
        subject="Re: " + item.get("subject", "").replace("Re: ", "", 1),
        html=(
            "<p>Thanks for the reply. Crew OS is currently running autonomously for a 14-day "
            "experiment — the founder is stepping back, and an AI is handling responses.</p>"
            "<p>If you'd like to join the pilot, reply with the word <strong>'send it'</strong> "
            "and we'll send you the intake template within a few minutes.</p>"
            "<p>If you'd like to opt out instead, reply with <strong>'stop'</strong> and we'll "
            "never email this address again.</p>"
            "<p>Anything else? A human (Finley) reads these threads when the experiment ends "
            "on May 29. crewos.co.uk</p>"
        ),
        reply_to="hello@crewos.co.uk",
    )
    return {"action": "cold_reply_logged_and_acked", "from": item.get("from", "")}


def handle_needs_human(item: dict[str, Any]) -> dict[str, Any]:
    _csv_append(
        OUTBOUND / "needs_human.csv",
        {
            "ts": _now_iso(),
            "from": item.get("from", ""),
            "subject": item.get("subject", ""),
            "preview": (item.get("body_preview") or "")[:400],
        },
    )
    return {"action": "logged_for_human", "subject": item.get("subject", "")}


def _extract_addr(s: str) -> str:
    import re
    m = re.search(r"[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}", s or "")
    return m.group(0) if m else ""


HANDLERS = {
    "pilot_signup": handle_pilot_signup,
    "intake_reply": handle_intake_reply,
    "cold_reply": handle_cold_reply,
    "needs_human": handle_needs_human,
}


def run() -> dict[str, Any]:
    messages = gmail_poll.poll()
    actions = []
    for m in messages:
        h = HANDLERS.get(m["kind"], handle_needs_human)
        try:
            actions.append({"kind": m["kind"], **h(m)})
        except Exception as e:
            actions.append({"kind": m["kind"], "action": "handler_error", "error": str(e)[:300]})
    summary = {
        "ran_at": _now_iso(),
        "messages_seen": len(messages),
        "actions": actions,
    }
    # Write a per-run summary into a runs/ folder for the weekly status workflow.
    (ROOT / "runs").mkdir(exist_ok=True)
    (ROOT / "runs" / f"triage-{_now_iso().replace(':','').replace('-','')}.json").write_text(
        json.dumps(summary, indent=2)
    )
    return summary


def _main() -> int:
    print(json.dumps(run(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
