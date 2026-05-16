# CHANGELOG

All meaningful releases of Crew OS. Append-only.

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
