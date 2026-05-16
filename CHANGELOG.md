# CHANGELOG

All meaningful releases of Crew OS. Append-only.

## v0.1.2 — Honesty pass + trader-nudge (2026-05-16)

Audit of the public surface as a sceptical UK tradesperson — caught several
active false promises on the landing page and one broken cold-email CTA. This
release closes those and ships the smallest version of the "we chase the
customer for you" claim that we can actually deliver.

**Site (false-promise fixes)**
- Removed the "Pilots 0/5 · Paid 0" header ticker — calibrated for an
  indie-hacker audience, trust-destroying for the actual buyer (a UK
  tradesperson). Replaced with "UK trades · open source · built in public".
- Rewrote "How it works" step 1 ("Talk it out") to match reality — v0 takes
  text intake by email reply; voice doesn't exist.
- Rewrote step 3 ("Polite email follow-ups until they book the job") to the
  honest version — we nudge the *trader* (not the customer) 3 days later,
  one reminder, never customer-direct spam.
- Replaced "We'll book a 10-minute call" with "intake template within an
  hour" — no one is available to take calls during the autonomous window.
- Dropped the "£99 template migration" line item from the pricebar — that
  language is SaaS jargon a plumber wouldn't parse.
- Replaced "UK-hosted infrastructure" with the actual stack disclosure
  (GitHub Pages CDN, Resend EU, Groq US).
- "Finley reads escalations" now correctly notes the 14-day autonomous
  window; AI handles support replies until 29 May 2026.
- Added an explicit "What v0 does and doesn't do (honest list)" FAQ entry.
- Added a small operator email + version tag to the footer; explicit "no
  tracking" note.
- Updated `<meta description>` and Open Graph tags to match shipped reality.

**Cold-email CTA fix**
- The "reply 'send it' to join the pilot" CTA in every cold email was
  classifying as a generic cold reply and getting auto-acked — not
  triggering the onboarding template. Now `inbound_triage` detects
  "send it" / "yes" / "I'm in" / "count me in" / "sign me up" and routes
  to the full pilot-signup flow.

**Trader-nudge workflow** (the smallest defensible version of "we chase")
- `scripts/trader_nudge.py` — walks `intake-queue/_processed/*.result.json`,
  finds quotes 3–14 days old without a `nudge_sent_at` field, sends a
  single reminder email to the trader summarising the quote + customer.
  Updates the result.json with `nudge_sent_at` for idempotency. Logs every
  send to `outbound/nudges.csv`.
- `.github/workflows/trader-nudge.yml` — daily cron at 09:00 UTC (10:00 UK
  BST). Uses the same pull-rebase-retry pattern as the other workflows.

**Docs**
- `v0/README.md` now ships a full and honest "what v0 doesn't do yet" list,
  including: voice, photos, direct-to-customer send, customer-side chase
  (trader-nudge is the boundary), PDF output, pricing memory, partial-VAT
  scenarios, Stripe wiring, quote-state transitions.
- `RUNBOOK.md` updated to reflect 6 workflows (was 5) — added the
  `trader-nudge` and `day-14-retrospective` entries.

**Verified by lint**
- All Python compiles. Suppression detector: 12/12 cases pass. "Send it"
  detector: 12/12 cases pass. Site visited byte-by-byte for the removed
  false-promise strings; all 5 confirmed absent.

---

## v0.1.1 — Final-session hardening (2026-05-16)

Improvements after Day-0 build and before operator went dark:

**Reliability**
- Fixed push-race condition in all 5 push-emitting workflows (`inbound-triage`,
  `quote-engine-runner`, `cold-email-batch`, `weekly-status`,
  `day-14-retrospective`). Each now does pull–rebase–retry up to 5× with
  exponential backoff, so concurrent workflow runs no longer drop commits.
  Root cause: the first real `inbound-triage` CI run failed because
  `weekly-status` pushed first — the triage's local commit was lost.

**Honoured promises**
- **Suppression list** (`outbound/suppressions.csv`) now lives. Every cold
  email asks recipients to reply "stop" to opt out. `inbound_triage` now
  detects "stop" / "unsubscribe" / "remove me" / "please stop emailing" /
  similar phrases in cold replies, adds the sender to the suppression list,
  and sends a single confirmation. `cold_email_batch` filters the
  suppression list before every send. The promise we made on every cold
  email is now actually wired up.
- **Day 14 retrospective workflow** (`day-14-retrospective.yml` +
  `scripts/day_14_retrospective.py`). Cron set to fire May 29 at 16:00 UTC
  (17:00 UK BST) — the hard cap. Writes a comprehensive cumulative
  "DAY 14 RETROSPECTIVE" block at the top of `STATE.md` with headline
  numbers, decision-points (keep going / pivot / pause), and known-issues
  rollover. Idempotent (re-runs replace, don't duplicate).

**Hygiene**
- Deleted smoke-test artefacts (`outbound/_smoke_cold_email.html`,
  `v0/_smoke_quote.html`) that had no purpose in production.
- Added deprecation READMEs to `/content/` and `/offer/cold-outreach/`
  explaining what's stale (LinkedIn-pack drafts pre-pivot) and what's live
  (the workflow prompts).
- This CHANGELOG.

**Verified in CI on Day 0:**
- ✅ `cold-email-batch` — empty targets → exits cleanly.
- ✅ `weekly-status` — wrote a real weekly block to STATE.md, pushed.
- ✅ `quote-engine-runner` — ran on empty queue, exited cleanly.
- ✅ `deploy` — site live at https://crewos.co.uk.
- 🟡 `inbound-triage` — first run failed at push step (race condition,
  now fixed); the triage logic itself ran successfully (Gmail polled,
  one email classified into `needs_human.csv` — that data was lost when
  the push was rejected).

**Operator return-date metrics target (unchanged):** ≥1 pilot signup from
cold sources, ≥1 real intake → quote sent end-to-end, by 2026-05-29.

---

## v0.1.0-handoff — Day 0 build complete (2026-05-16)

The autonomous-mode armed release. See the git tag `v0.1.0-handoff`.

**Ships:**
- v0 quote engine (Python, Groq Llama-3.3-70B → Jinja2 HTML → Resend).
- 5 GitHub Actions workflows: `deploy`, `inbound-triage` (2h cron),
  `quote-engine-runner` (push trigger), `cold-email-batch` (daily cron),
  `weekly-status` (Friday cron).
- 5 scripts under `/scripts/` powering the workflows.
- `RUNBOOK.md` (stranger-takes-over operator manual, 10 sections).
- `README.md` (rewritten for autonomous mode).
- `outbound/README.md` (cold-acquisition state convention).
- Landing page at https://crewos.co.uk retoned for text-first intake
  ("talk it out, type it up, or paste your site notes") while preserving
  the "8 minutes" promise.
- AI-transparency FAQ on the landing page.
- Final commit `e9e39b9`, tag `v0.1.0-handoff`.

**Known issues at handoff (carried forward to v0.1.1):**
- 🟡 ImprovMX DNS conflict (rogue `MX @ inbound-smtp.eu-west-1.amazonaws.com`)
  causing ~50% inbound email loss. Fix: one Hostinger DNS deletion.
- 🟡 `outbound/targets.csv` ships empty. Cold-email volume is 0 until
  populated.
- 🟡 No file uploads in v0 intake (Formspree free tier).
- 🟡 Anthropic API key declined by operator — Groq is the runtime LLM in
  every workflow.
- 🟡 LinkedIn dropped (operator declined personal-account admin); no
  Company Page for the autonomous period.
