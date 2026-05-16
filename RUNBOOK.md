# RUNBOOK — Crew OS

_Written 2026-05-16, end-of-day. The audience for this document is a stranger who picks up Crew OS without context. If you're that person: start here, then read `STATE.md`, then `DECISIONS.md`, then `research/playbook.md`._

---

## 1. What Crew OS is

A £49/month productised tool for UK trade businesses with 1–5 people that turns a site-visit description into a branded client quote (HTML email), sent to the trader for review, with optional follow-up sequence. Founded by Finley Stephenson (18, UK). Operated end-to-end by Claude (Anthropic's AI). Built £0, one ~£10 domain.

The pick reasoning, the landscape it lives in, the playbook it draws from, and the rubric used to select it are all in `/research/*.md`. Read them before making strategy changes.

## 2. What's deployed

| Surface | URL | Notes |
|---|---|---|
| Landing page | https://crewos.co.uk | GitHub Pages, deployed by `.github/workflows/deploy.yml` on every push to `main`. |
| Repo | https://github.com/finleystephenson/crewOS | Public. Single source of truth for state. |
| Outbound email | Resend, domain `crewos.co.uk` verified | Free tier, 100/day, 3000/month. |
| Inbound email | ImprovMX → `crewos.uk@gmail.com` | **Flaky** due to live DNS conflict; see §6. |
| Monitoring | UptimeRobot on `https://crewos.co.uk` | Alerts to `crewos.uk@gmail.com`. |
| Pilot signup form | Formspree, embedded on landing page | Free tier, 50 submissions/month. |

## 3. The autonomous workflows

Five files under `.github/workflows/`. All commit changes back to the repo using the auto-injected `GITHUB_TOKEN`.

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy.yml` | push to `main` | Builds the static site from `/site/` and deploys to GitHub Pages. |
| `inbound-triage.yml` | cron every 2h (UK day) + manual | Polls `crewos.uk@gmail.com` via IMAP, classifies messages (pilot signup, intake reply, cold reply, needs-human), routes each: sends onboarding emails, writes intake JSONs, auto-acks cold replies, logs everything to `/outbound/*.csv`. |
| `quote-engine-runner.yml` | push to `intake-queue/*.json` + manual | Processes each pending intake by calling `v0/quote_engine.py`. On success, moves to `intake-queue/_processed/` with a `.result.json` sidecar. On 3× failure, moves to `intake-queue/_failed/`. |
| `cold-email-batch.yml` | cron weekdays 11:00 UK + manual | Reads `outbound/targets.csv`, picks N (default 3) eligible rows, personalises each via Groq, sends via Resend, logs to `outbound/sent.csv`. Won't email the same target within 30 days. Honours `outbound/suppressions.csv`. |
| `trader-nudge.yml` | cron daily 10:00 UK + manual | Walks `intake-queue/_processed/*.result.json`. For any quote 3–14 days old that hasn't been nudged, sends ONE reminder email to the trader. Doesn't email the customer. Logs to `outbound/nudges.csv`. |
| `weekly-status.yml` | cron Fridays 17:00 UK + manual | Tallies metrics and inserts a "Week N status" block at the top of `STATE.md`. |
| `day-14-retrospective.yml` | cron May 29 17:00 UK + manual | Writes a comprehensive cumulative retrospective block at the top of `STATE.md` with headline numbers + decision-points (keep going / pivot / pause). Idempotent. |

## 4. The v0 quote engine

`/v0/quote_engine.py` — single-file Python, runs locally or in CI.

- **Input:** structured intake JSON (see `/v0/test_intake.json` for the schema).
- **LLM:** Groq, `llama-3.3-70b-versatile`. Structured-output mode (`response_format=json_object`).
- **Template:** Jinja2 → `/v0/templates/quote_email.html`.
- **Output:** branded HTML quote, sent via Resend to the trader's email (not the customer; v0 is review-mode).
- **Run locally:** `cd v0 && pip install -r requirements.txt && python quote_engine.py test_intake.json --no-send`.

## 5. Secrets

GitHub Secrets at https://github.com/finleystephenson/crewOS/settings/secrets/actions:

| Name | Used by | Source |
|---|---|---|
| `GMAIL_USERNAME` | `inbound-triage` | `crewos.uk@gmail.com` |
| `GMAIL_APP_PASSWORD` | `inbound-triage` | Gmail app password (rotatable) |
| `GROQ_API_KEY` | `inbound-triage`, `quote-engine-runner`, `cold-email-batch` | Groq Console |
| `RESEND_API_KEY` | all email-sending workflows | Resend Dashboard |
| `UPTIMEROBOT_API_KEY` | (not actively used by any workflow yet) | UptimeRobot Dashboard |

**No Anthropic API key.** All runtime AI is Groq. Strategic reasoning was baked into the repo on 2026-05-16 — there is no "ceo-pulse" daemon making Claude-grade decisions in CI.

## 6. Known issues (and where to look)

### 6.1 ImprovMX inbound has a DNS conflict
`dig crewos.co.uk MX` still shows `inbound-smtp.eu-west-1.amazonaws.com` at priority 10 alongside `mx1.improvmx.com` at priority 10. Expected: ~50% of inbound emails to `hello@`, `quote@`, `finley@` will bounce/lose.

**Fix:** at Hostinger DNS → Domains → `crewos.co.uk` → DNS → delete the row `MX @ 10 inbound-smtp.eu-west-1.amazonaws.com`. One click.

**Workaround currently in place:** primary pilot intake = Formspree web form (100% reliable). Email-based intake (`quote@crewos.co.uk`) is a bonus path that works ~half the time.

### 6.2 No file uploads in v0
Formspree free tier blocks file uploads. v0 intake is text-only via the email reply template. Voice notes + photos are a v1 feature.

**Fix paths (any one is enough):**
- Upgrade Formspree to a paid plan ($10/mo).
- Add Tally.so (free tier supports file uploads). Replace the landing-page form with a Tally embed; have Tally's webhook hit a Cloudflare Worker (or GitHub Issue) that writes to `intake-queue/`.
- Add a Cloudflare R2 bucket + a Worker for direct uploads.

### 6.3 No LinkedIn distribution channel
Operator declined personal-LinkedIn admin of a Crew OS Company Page (which LinkedIn requires). The 5 build-in-public posts originally calibrated for LinkedIn are in `/content/linkedin-posts-pack.md`. They will be repurposed as `/blog` posts on the site (next item on the Day-0 close-of-day list).

**Fix:** if a future operator is happy to admin a Company Page, create it, set the page URL in `site/index.html` footer, and switch the build-in-public output back to LinkedIn-scheduled posts.

### 6.4 Empty cold-email targets list
`outbound/targets.csv` ships empty on 2026-05-16. The `cold-email-batch` workflow runs without errors on an empty list (returns `no_targets`) but sends nothing. Populating the list is the highest-leverage manual task to unlock cold-acquisition volume.

**Fix:** see `outbound/README.md` for acceptable target sources. Add rows to `targets.csv` and the workflow will start emailing.

## 7. How to operate

### 7.1 Daily check (5 min)
1. Read `STATE.md` — most recent dated entry first.
2. Check Actions: https://github.com/finleystephenson/crewOS/actions — anything red in the last 24h?
3. Skim `outbound/needs_human.csv` for any non-classified inbound.

### 7.2 Pilot signup arrives (auto, watch the logs)
Inbound-triage will:
- Detect Formspree's notification email.
- Reply to the signup with the onboarding email + intake template.
- Log to `outbound/signups.csv`.

You do nothing unless `needs_human.csv` grows.

### 7.3 Pilot replies with filled intake template (auto)
- Inbound-triage parses the reply, writes `intake-queue/<ts>.json`, commits.
- Quote-engine-runner triggers on the push, generates the quote, sends to the trader.
- The trader gets a draft quote for review within ~10 minutes.

### 7.4 A pilot replies "this quote is wrong" or "send it again"
- Inbound-triage will classify this as `cold_reply` (treats it as a thread continuation). It will auto-ack and log.
- Read `outbound/cold_replies.csv` and decide whether to send a corrected quote manually or improve the prompt in `v0/quote_engine.py`.

### 7.5 A workflow fails red
- Click into the run on GitHub Actions, read the log.
- If it's a Groq 429: retry will fix itself.
- If it's a Resend 4xx: probably a domain-verification regression or an invalid `to`. Check Resend dashboard.
- If it's an IMAP authentication error: rotate the Gmail app password and update `GMAIL_APP_PASSWORD` secret.
- Document in `STATE.md` and `DECISIONS.md` if you change anything substantive.

### 7.6 You need to ship a v0.2
- Make changes locally.
- Push to `main`.
- Deploy is automatic for site changes.
- Workflow changes take effect on next scheduled trigger.
- Tag releases: `git tag v0.2.0 && git push --tags`.

## 8. When to escalate to a human
Per the original brief, the only things that need human (Finley) involvement are:
- Irreversible real-world actions (domain renewal payment, new account signups requiring identity, sending real money).
- Anything involving the legal entity (Finley owns Crew OS).
- Customer disputes that need a named human.
- A decision to wind the business down.

Everything else: keep iterating in the repo.

## 9. The 14-day cap (2026-05-29)
The original brief says the autopilot is real until Friday May 29, 2026. After that:
- If the autopilot is producing pilot signups and quotes: keep going indefinitely; nothing requires human intervention to continue.
- If it's silent: read `STATE.md`'s Day-14 retrospective. Decide whether to pivot, pause, or kill. Default-pause is acceptable per the brief.

## 10. Read order for a stranger picking this up cold
1. `README.md` (project overview)
2. `STATE.md` (most recent first)
3. `DECISIONS.md` (most recent first)
4. This file
5. `/research/decision.md` (why Crew OS specifically)
6. `/research/landscape.md` (the May 2026 market)
7. `/research/playbook.md` (the synthesis the decision rests on)
8. `/v0/README.md` (the product)
9. `/outbound/README.md` (the acquisition state)
10. `/research/me-profile.md` (founder context, useful only for vibe-setting)
