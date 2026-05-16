"""
Suppression list helpers.

`outbound/suppressions.csv` is the authoritative list of email addresses
Crew OS will NEVER cold-email. Adding to it is a one-way door — the cold
email workflow filters this list out before every send.

Triggers for auto-adding:
- A reply that reads exactly "stop", "unsubscribe", "remove me", or "no thanks"
  (case-insensitive, ignoring quoted text from the original email)
- A reply that contains: "unsubscribe", "opt-out", "stop emailing", "please stop",
  "do not email", "do not contact", "take me off"

Hand-edits to the CSV are also valid — just add a row.
"""
from __future__ import annotations
import csv
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUPP = ROOT / "outbound" / "suppressions.csv"

# Conservative patterns. Better to occasionally miss an unsubscribe than to
# wrongly suppress someone who wrote "stop by anytime."
_PHRASE_RE = re.compile(
    r"\b(unsubscribe|opt[- ]?out|stop emailing|please stop|"
    r"do not (?:email|contact|message)|take me off|"
    r"remove (?:me|us)|no longer (?:wish|want)|"
    r"stop sending|leave me alone)\b",
    re.I,
)

# Standalone short replies — body == one of these (after stripping quotes).
_SHORT_TOKENS = {"stop", "unsubscribe", "remove me", "no thanks", "no.", "no", "remove"}


def _strip_quoted(body: str) -> str:
    """Remove the quoted-original-email portion of a reply."""
    out_lines = []
    for ln in body.splitlines():
        s = ln.strip()
        if s.startswith(">"):
            continue
        if "wrote:" in s.lower() and len(s) < 200:
            # likely a "On Thu, X wrote:" boundary
            break
        out_lines.append(ln)
    return "\n".join(out_lines).strip()


def should_suppress(body_preview: str) -> bool:
    body = _strip_quoted(body_preview or "")
    # Short, standalone replies
    norm = re.sub(r"\s+", " ", body).strip().lower().rstrip(".!?")
    if norm in _SHORT_TOKENS:
        return True
    # Phrase-in-longer-body
    return bool(_PHRASE_RE.search(body))


def load() -> set[str]:
    if not SUPP.exists():
        return set()
    out: set[str] = set()
    with SUPP.open() as f:
        for row in csv.DictReader(f):
            e = (row.get("email") or "").strip().lower()
            if e:
                out.add(e)
    return out


def add(email: str, reason: str, source: str = "auto") -> bool:
    """Append a row if not already suppressed. Returns True if added."""
    email = email.strip().lower()
    if not email or "@" not in email:
        return False
    if email in load():
        return False
    SUPP.parent.mkdir(exist_ok=True)
    existed = SUPP.exists() and SUPP.stat().st_size > 0
    with SUPP.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["email", "reason", "added_at", "source"])
        if not existed:
            w.writeheader()
        w.writerow(
            {
                "email": email,
                "reason": reason[:300],
                "added_at": dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds") + "Z",
                "source": source,
            }
        )
    return True
