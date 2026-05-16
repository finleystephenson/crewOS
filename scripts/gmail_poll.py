"""
Gmail IMAP poller for Crew OS inbound triage.

Reads crewos.uk@gmail.com via IMAP, finds unprocessed messages, classifies them,
and emits actions as JSON on stdout. The calling workflow applies the actions
(write intake.json, send onboarding email, etc.).

Stateful via Gmail labels:
    - "crew-os/seen"           : we've processed this message
    - "crew-os/pilot-signup"   : new pilot signup (from Formspree)
    - "crew-os/intake-reply"   : pilot replied with filled intake template
    - "crew-os/cold-reply"     : reply to one of our outbound cold emails
    - "crew-os/needs-human"    : unclassified, leave for human review

Env required: GMAIL_USERNAME, GMAIL_APP_PASSWORD.
"""
from __future__ import annotations
import email
import email.policy
import imaplib
import json
import os
import re
import sys
from email.message import EmailMessage
from typing import Any

IMAP_HOST = "imap.gmail.com"

# Subjects we recognise from Formspree
FORMSPREE_SUBJECT_RE = re.compile(r"crew os pilot signup", re.I)

# Marker the onboarding email asks the pilot to leave in their reply
INTAKE_REPLY_MARKER = "CREW-OS-INTAKE-V1"


def _connect() -> imaplib.IMAP4_SSL:
    user = os.environ["GMAIL_USERNAME"]
    pw = os.environ["GMAIL_APP_PASSWORD"]
    m = imaplib.IMAP4_SSL(IMAP_HOST)
    m.login(user, pw)
    return m


def _ensure_label(m: imaplib.IMAP4_SSL, label: str) -> None:
    # Gmail labels live in the "[Gmail]" hierarchy; create if missing.
    typ, _ = m.create(f'"{label}"')  # idempotent; succeeds if missing, errors silently if exists
    if typ != "OK":
        pass  # almost always "already exists"


def _label(m: imaplib.IMAP4_SSL, uid: bytes, label: str) -> None:
    _ensure_label(m, label)
    m.uid("COPY", uid, label)
    m.uid("STORE", uid, "+FLAGS", "(\\Seen)")


def _fetch_full(m: imaplib.IMAP4_SSL, uid: bytes) -> EmailMessage:
    typ, data = m.uid("FETCH", uid, "(RFC822)")
    if typ != "OK" or not data or not data[0]:
        raise RuntimeError(f"Failed to fetch UID {uid!r}")
    raw = data[0][1]
    return email.message_from_bytes(raw, policy=email.policy.default)  # type: ignore


def _body_text(msg: EmailMessage) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                try:
                    return part.get_content()
                except Exception:
                    pass
        # fallback: any text
        for part in msg.walk():
            if part.get_content_type().startswith("text/"):
                try:
                    return part.get_content()
                except Exception:
                    pass
        return ""
    return msg.get_content() if msg.get_content_type().startswith("text/") else ""


def _parse_intake_reply(body: str) -> dict[str, Any] | None:
    """Pull structured fields out of a reply containing the intake template."""
    if INTAKE_REPLY_MARKER not in body:
        return None
    # Template uses `> field: value` style lines. Tolerant parser.
    fields: dict[str, str] = {}
    for raw in body.splitlines():
        line = raw.strip().lstrip(">").strip()
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip().lower().replace(" ", "_")
        v = v.strip()
        if k and v:
            fields[k] = v

    def need(*keys: str) -> str | None:
        for k in keys:
            if k in fields:
                return fields[k]
        return None

    intake = {
        "customer": {
            "name": need("customer_name") or "",
            "email": need("customer_email") or "",
            "address": need("customer_address") or "",
        },
        "trader": {
            "business_name": need("business_name", "trader_business") or "",
            "owner_name": need("your_name", "trader_name") or "",
            "email": need("your_email", "trader_email") or "",
            "phone": need("your_phone", "trader_phone") or "",
            "address": need("your_address", "trader_address") or "",
            "registration_numbers": need("registration_numbers", "registrations") or "",
            "vat_registered": (need("vat_registered") or "no").lower().startswith("y"),
            "vat_number": need("vat_number") or None,
            "hourly_rate_gbp": int(re.sub(r"\D", "", need("hourly_rate") or "0") or 0),
            "callout_fee_gbp": int(re.sub(r"\D", "", need("callout_fee") or "0") or 0),
        },
        "job": {
            "trade": need("trade") or "general",
            "description": need("job_description", "description") or "",
            "site_visit_notes": need("site_visit_notes", "notes") or "",
        },
    }
    return intake


def classify(msg: EmailMessage) -> dict[str, Any]:
    subject = (msg.get("Subject") or "").strip()
    from_addr = (msg.get("From") or "").strip()
    body = _body_text(msg)

    if FORMSPREE_SUBJECT_RE.search(subject):
        m = re.search(r"[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}", body)
        return {
            "kind": "pilot_signup",
            "from": from_addr,
            "subject": subject,
            "applicant_email": m.group(0) if m else "",
        }

    intake = _parse_intake_reply(body)
    if intake is not None:
        return {
            "kind": "intake_reply",
            "from": from_addr,
            "subject": subject,
            "intake": intake,
        }

    # Looks like a reply to one of our outbound cold emails?
    if "re:" in subject.lower() or "crew os" in subject.lower():
        return {
            "kind": "cold_reply",
            "from": from_addr,
            "subject": subject,
            "body_preview": body[:1200],
        }

    return {
        "kind": "needs_human",
        "from": from_addr,
        "subject": subject,
        "body_preview": body[:500],
    }


def poll(max_messages: int = 50) -> list[dict[str, Any]]:
    """Return classified, not-yet-seen messages. Marks them seen via label."""
    m = _connect()
    try:
        m.select("INBOX")
        # Find messages that have NOT been labelled crew-os/seen
        typ, data = m.uid("SEARCH", None, "X-GM-RAW", '"-label:crew-os/seen"')
        if typ != "OK":
            return []
        uids = (data[0] or b"").split()
        out: list[dict[str, Any]] = []
        for uid in uids[:max_messages]:
            msg = _fetch_full(m, uid)
            classified = classify(msg)
            classified["uid"] = uid.decode()
            classified["message_id"] = (msg.get("Message-Id") or "").strip()
            # Tag in Gmail for routing visibility + state
            _label(m, uid, "crew-os/seen")
            _label(m, uid, f"crew-os/{classified['kind'].replace('_', '-')}")
            out.append(classified)
        return out
    finally:
        try:
            m.close()
        except Exception:
            pass
        m.logout()


def _main() -> int:
    results = poll()
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
