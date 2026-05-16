# Crew OS

**The AI operating system for UK trade businesses with 1–5 people.** Turns a tradesperson's site-visit description into a sent, branded client quote in under 10 minutes, then chases the customer via email until the job's booked. £49/month after a 14-day free pilot, no card.

Live at https://crewos.co.uk · Repo at https://github.com/finleystephenson/crewOS

---

## What this repo is

Crew OS was built as a £0 lifestyle-business experiment by an AI agent (Claude, Anthropic) with one human collaborator (Finley Stephenson, 18, UK) clicking real-world buttons. The full premise is in the original brief; the working artefacts are:

- [`research/playbook.md`](research/playbook.md) — 26-source synthesis on £0 lifestyle businesses in May 2026.
- [`research/landscape.md`](research/landscape.md) — where the gaps actually are, evidence-cited.
- [`research/me-profile.md`](research/me-profile.md) — founder context, lightly used.
- [`research/decision.md`](research/decision.md) — why Crew OS specifically.

The decision rested on a tombstone test: which niches still exist in 12 months once AI eats the easy categories. Crew OS won because the moat is UK-specific compliance + workflow depth + human trust between trader and customer — none of which a frontier-model release in 2026 eliminates.

## Operating mode

As of 2026-05-16 (Day 0 close-of-day), Crew OS runs in **autonomous mode** until **Friday 2026-05-29 (Day 14)**:

- The founder stepped fully back on Day 0. No human is on-call until May 29.
- Five GitHub Actions workflows handle inbound, outbound, and processing.
- All runtime AI uses Groq (Llama 3.3 70B); no Anthropic API in CI.
- LinkedIn dropped (founder declined personal-account admin); replaced with `/blog` + Reddit + cold email + SEO.

If you've just landed in this repo for the first time, read in this order:
1. This file.
2. [`STATE.md`](STATE.md) — chronological log, most recent at top.
3. [`DECISIONS.md`](DECISIONS.md) — append-only choice log, most recent at top.
4. [`RUNBOOK.md`](RUNBOOK.md) — how to operate Crew OS without context.
5. [`v0/README.md`](v0/README.md) — the actual product.

## What's deployed

| Surface | Notes |
|---|---|
| `https://crewos.co.uk` | Landing page (static HTML via GitHub Pages) with pilot signup form. |
| `crewos.uk@gmail.com` | Inbound mail address. Receives Formspree notifications + ImprovMX-forwarded mail. |
| Resend, domain Verified | Outbound from `*@crewos.co.uk`. Used by every email-sending workflow. |
| UptimeRobot | Watches the landing page; alerts to Gmail on downtime. |

GitHub Secrets in place: `GMAIL_USERNAME`, `GMAIL_APP_PASSWORD`, `GROQ_API_KEY`, `RESEND_API_KEY`, `UPTIMEROBOT_API_KEY`. **No Anthropic key** — operator declined paid API tokens.

## Active workflows (all under `.github/workflows/`)

| Workflow | Trigger | Purpose |
|---|---|---|
| `deploy.yml` | push to `main` | Deploys the static site from `/site/` to GitHub Pages. |
| `inbound-triage.yml` | every 2h (UK day) | Polls Gmail, classifies inbound, sends onboarding to new signups, writes intakes to the queue, auto-acks cold replies. |
| `quote-engine-runner.yml` | new files in `intake-queue/` | Runs `v0/quote_engine.py` on each pending intake. Moves processed/failed to `_processed/` or `_failed/`. |
| `cold-email-batch.yml` | weekdays 11:00 UK | Sends up to N (default 3) personalised cold emails from `outbound/targets.csv`. |

## Folder layout

```
/research/          immutable research outputs from Phases 0–1
/v0/                the product itself (Python quote engine + templates)
/scripts/           the autonomous CLI scripts the workflows invoke
/.github/workflows/ the five Actions workflows
/site/              the static landing page (deployed to crewos.co.uk)
/site/blog/         build-in-public posts (auto-published)
/intake-queue/      pilot intake JSONs awaiting processing; _processed/ + _failed/ subfolders for state
/outbound/          cold-acquisition state: targets, sent log, signups log, replies log
/content/           drafted content (some files deprecated; see headers)
/offer/             offer + cold-outreach docs (some files deprecated; see headers)
/runs/              per-run JSON snapshots from workflows (audit trail)
STATE.md            running log
DECISIONS.md        append-only choice log
RUNBOOK.md          operator manual for a stranger picking this up cold
README.md           you are here
```

## End-of-month criteria (May 29, Day 14)

Honest reads on what I'm trying to ship by Day 14:

- ✅ Site live at `crewos.co.uk` with working pilot form — **DONE Day 0**.
- ✅ v0 quote engine functional end-to-end (smoke-tested locally) — **DONE Day 0**.
- ✅ All five workflows shipped + valid — **DONE Day 0**.
- ✅ RUNBOOK.md so a stranger can pick up — **DONE Day 0**.
- ⏳ At least 1 pilot signup from cold sources by Day 14.
- ⏳ At least 1 real intake successfully processed → quote sent.
- ⏳ 1 written testimonial or one paying customer (stretch).

Stretch beyond Day 14 is acceptable per the brief. If the autopilot produces nothing in 14 days, `STATE.md` will have a Day-14 retrospective explaining why, and the operator can decide whether to pivot, pause, or kill.

## License

The repo is open and public on purpose — this is also a build-in-public experiment. Code is unlicensed (default: all rights reserved); take inspiration freely but don't fork-and-rebrand without contact.
