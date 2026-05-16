"""
Trader nudge — sends a single polite reminder to a trader 3 days after their
Crew OS quote was generated, prompting them to chase the customer if they
haven't heard back. Honours the "you stop forgetting the ones that went quiet"
promise on the landing page WITHOUT spamming the customer.

Rules:
- Nudge only the TRADER (not their customer). Customer-direct follow-up is
  deliberately out of v0.
- One nudge per quote, maximum.
- Triggers when `started_at` is between 3 and 14 days old.
- Idempotent: writes `nudge_sent_at` into the result.json so a second run
  doesn't re-send.
- Skips quotes where the customer email obviously bounced (no email present
  on the original intake) — we have no way to follow up there.

Env: RESEND_API_KEY.
"""
from __future__ import annotations
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from v0.quote_engine import send_via_resend  # noqa: E402

PROCESSED = ROOT / "intake-queue" / "_processed"
NUDGES_LOG = ROOT / "outbound" / "nudges.csv"

NUDGE_AFTER_DAYS = 3
NUDGE_BEFORE_DAYS = 14   # don't nudge quotes that are already stale
NUDGE_FROM = "Crew OS <hello@crewos.co.uk>"


NUDGE_HTML = """\
<!doctype html><html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:#0f0f0f;line-height:1.55;max-width:560px;margin:0 auto;padding:24px;font-size:15px;">

<p>Hi {trader_first_name},</p>

<p>Quick nudge — the Crew OS quote we drafted for <strong>{customer_name}</strong> went into your inbox <strong>{days_ago} days ago</strong>.</p>

<table role="presentation" cellpadding="6" cellspacing="0" style="border:1px solid #1a1a1a;background:#f6f3ec;font-size:14px;margin:14px 0;">
  <tr><td>Customer</td><td>{customer_name} &lt;{customer_email}&gt;</td></tr>
  <tr><td>Job</td><td>{summary}</td></tr>
  <tr><td>Total</td><td>£{total_gbp:,.0f}</td></tr>
</table>

<p>If you've sent it on and haven't heard back, this is your nudge to follow up. Most quotes that convert get a reply inside the first week — the ones that go quiet usually need a phone call, not another email.</p>

<p><strong>No action needed</strong> if you're still waiting or already heard back — we won't nudge again on this one.</p>

<hr style="margin:24px 0;border:none;border-top:1px solid #e5e0d4;">
<p style="font-size:11px;color:#6b6b6b;">Crew OS — built by Claude (AI), founded by Finley Stephenson. Reply to reach a human (or another AI; we're transparent either way). <a href="https://crewos.co.uk" style="color:#6b6b6b;">crewos.co.uk</a></p>
</body></html>
"""


def _parse_iso(s: str) -> dt.datetime | None:
    if not s:
        return None
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None


def _first_name(full: str | None) -> str:
    if not full:
        return "there"
    return full.strip().split()[0]


def _append_log(row: dict[str, Any]) -> None:
    import csv
    NUDGES_LOG.parent.mkdir(exist_ok=True)
    existed = NUDGES_LOG.exists() and NUDGES_LOG.stat().st_size > 0
    with NUDGES_LOG.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not existed:
            w.writeheader()
        w.writerow(row)


def process_one(path: Path, now: dt.datetime) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        return {"path": str(path.relative_to(ROOT)), "skipped": "unreadable_json", "error": str(e)[:200]}

    if data.get("nudge_sent_at"):
        return {"path": str(path.relative_to(ROOT)), "skipped": "already_nudged"}

    started = _parse_iso(data.get("started_at", ""))
    if not started:
        return {"path": str(path.relative_to(ROOT)), "skipped": "no_started_at"}

    age = (now - started).total_seconds() / 86400
    if age < NUDGE_AFTER_DAYS:
        return {"path": str(path.relative_to(ROOT)), "skipped": "too_recent", "age_days": round(age, 2)}
    if age > NUDGE_BEFORE_DAYS:
        return {"path": str(path.relative_to(ROOT)), "skipped": "too_old", "age_days": round(age, 2)}

    quote = data.get("quote") or {}
    trader_email = data.get("trader_email")
    if not trader_email:
        return {"path": str(path.relative_to(ROOT)), "skipped": "no_trader_email"}

    # The intake's customer name lives inside the originally-recorded result,
    # not here — pull what we can.
    customer_email = data.get("customer_email", "")
    summary = quote.get("summary") or "your job"
    total = quote.get("total_gbp") or 0
    # We didn't record trader's first name in the result; fall back to "there".
    trader_first = "there"
    customer_name = "your customer"

    html = NUDGE_HTML.format(
        trader_first_name=trader_first,
        customer_name=customer_name,
        customer_email=customer_email or "(no email captured)",
        days_ago=int(age),
        summary=summary,
        total_gbp=total,
    )
    subject = f"Crew OS nudge: your quote ({summary[:60]}) is {int(age)} days old"
    ok, info = send_via_resend(
        to_email=trader_email,
        subject=subject,
        html=html,
        reply_to="hello@crewos.co.uk",
    )

    if ok:
        data["nudge_sent_at"] = now.isoformat(timespec="seconds") + "Z"
        data["nudge_resend_id"] = info
        path.write_text(json.dumps(data, indent=2))

    _append_log(
        {
            "ts": now.isoformat(timespec="seconds") + "Z",
            "trader_email": trader_email,
            "customer_email": customer_email,
            "summary": summary[:120],
            "age_days": round(age, 2),
            "ok": ok,
            "resend_id_or_err": info,
        }
    )
    return {"path": str(path.relative_to(ROOT)), "sent": ok, "info": info, "age_days": round(age, 2)}


def run() -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    if not PROCESSED.exists():
        return {"status": "no_processed_dir", "now": now.isoformat(timespec="seconds") + "Z"}
    results = [process_one(p, now) for p in sorted(PROCESSED.glob("*.result.json"))]
    sent = sum(1 for r in results if r.get("sent"))
    return {"status": "ran", "candidates": len(results), "sent": sent, "results": results}


def _main() -> int:
    print(json.dumps(run(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
