"""
Quote-engine runner. Picks up any new intake JSON in intake-queue/ that
hasn't been processed yet, runs v0/quote_engine.py, archives results.

State convention:
    intake-queue/<ts>.json          → pending
    intake-queue/_processed/<ts>.json → done (with .result.json sibling)
    intake-queue/_failed/<ts>.json    → failed after retries (with .error.txt)

Env: GROQ_API_KEY, RESEND_API_KEY (passed through to quote_engine).
"""
from __future__ import annotations
import json
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from v0.quote_engine import process  # noqa: E402

QUEUE = ROOT / "intake-queue"
PROCESSED = QUEUE / "_processed"
FAILED = QUEUE / "_failed"
PROCESSED.mkdir(parents=True, exist_ok=True)
FAILED.mkdir(parents=True, exist_ok=True)


def _pending() -> list[Path]:
    return sorted(p for p in QUEUE.glob("*.json") if p.is_file())


def run_one(path: Path) -> dict:
    intake = json.loads(path.read_text())
    last_err = None
    for attempt in (1, 2, 3):
        try:
            result = process(intake, send=True)
            # Move file to _processed/ and write result sidecar.
            dest = PROCESSED / path.name
            path.rename(dest)
            dest.with_suffix(".result.json").write_text(json.dumps(result, indent=2))
            return {"path": str(dest.relative_to(ROOT)), "status": result.get("status"), "attempt": attempt}
        except Exception as e:
            last_err = e
            time.sleep(2 ** attempt)
    # 3 failures → _failed/
    dest = FAILED / path.name
    path.rename(dest)
    dest.with_suffix(".error.txt").write_text(
        f"{type(last_err).__name__}: {last_err}\n\n{traceback.format_exc()}"
    )
    return {"path": str(dest.relative_to(ROOT)), "status": "failed", "error": str(last_err)[:300]}


def run() -> dict:
    pending = _pending()
    results = [run_one(p) for p in pending]
    return {"processed": len(results), "results": results}


def _main() -> int:
    print(json.dumps(run(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
