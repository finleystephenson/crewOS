# Crew OS — v0 quote engine

Single-file Python pipeline that turns a structured pilot intake into a branded HTML quote, sent via Resend to the trader for review.

## Architecture (v0, May 2026)

```
[pilot fills web form on crewos.co.uk]
            ↓ (Formspree → email to crewos.uk@gmail.com)
[inbound-triage workflow polls Gmail every 2h]
            ↓ (parses fields → writes intake.json)
[quote-engine-runner workflow]
            ↓ (python quote_engine.py intake.json)
[Groq Llama-3.3-70B → JSON quote]
            ↓ (jinja2 renders quote_email.html)
[Resend → trader's inbox]
            ↓ (trader reviews + forwards to their customer)
```

v0 sends the quote to the **trader** to review, not directly to the customer.
This is deliberate — lower risk while we validate the model is producing
defensible quotes. v1 (post-May-29) will send direct-to-customer once we trust
the output.

## Why no voice / photos in v0

- Formspree free tier doesn't accept file uploads. Operator's £0 brief blocks
  the paid tier.
- ImprovMX inbound is partially broken (DNS conflict on apex MX), so
  email-based intake at `quote@crewos.co.uk` is flaky.
- Text-only intake works 100% via the web form. Voice + photos becomes v1.

Decision logged in `DECISIONS.md` (2026-05-16, "Operator stepped fully back").

## Why no Anthropic / Claude

Operator declined billing setup on the Anthropic API. All runtime LLM work
uses Groq's free tier:

- **Quote generation:** `llama-3.3-70b-versatile`
- **Whisper transcription:** `whisper-large-v3-turbo` (reserved for v1)

Logged in DECISIONS.md.

## Local run

```
cd v0
pip install -r requirements.txt
export GROQ_API_KEY=...   # only needed for actual generation
export RESEND_API_KEY=... # only needed when --no-send is omitted

python quote_engine.py test_intake.json --no-send   # generates + prints JSON
python quote_engine.py test_intake.json             # generates + emails trader
```

## CI run

`.github/workflows/quote-engine-runner.yml` picks up new intake files committed
to `intake-queue/` and runs the same pipeline using repo secrets
`GROQ_API_KEY` and `RESEND_API_KEY`.

## Trade-template starter data

For pilots without their own pricing on file, `templates/trade_starter.json`
provides sensible defaults per trade (electrical / plumbing / building /
groundworks). The model will be told to use these only when the pilot doesn't
provide their own. (v1 will add per-trader pricing storage.)

## Failure modes & what to do

| Failure | Cause | Recovery |
|---|---|---|
| Groq 429 / 5xx | Rate limit or transient | The CI workflow retries with backoff. After 3 fails, intake is moved to `intake-queue/_failed/` with the error in JSON. |
| Resend 4xx | Bad email / unverified domain | Same: moved to `_failed/`. STATE.md gets a 🟡 note on next weekly-status run. |
| Malformed model JSON | Llama drift | We use Groq's `response_format=json_object`. If it still drifts, parser fails loudly; CI logs the raw response. |
| Empty / missing fields in intake | Web form had blanks | `inbound-triage` rejects pre-engine; pilot gets an auto-reply asking for the missing field. |

## What v0 does NOT do (yet)

- ❌ Voice transcription (Groq Whisper is wired, just no upload path)
- ❌ Photo OCR / scene understanding
- ❌ Direct-to-customer send (v0 sends to trader only)
- ❌ Follow-up sequence (separate workflow, ships next)
- ❌ PDF output (HTML email only)
- ❌ Multi-trader pricing storage (uses intake's `trader` block each call)
- ❌ VAT calculation for partial-VAT scenarios

All marked for v1 in `RUNBOOK.md`.
