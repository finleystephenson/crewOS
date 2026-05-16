# Day-14 todo

Things I found during the pre-flight audit that are **not load-bearing for
the next 13 days** (the autonomous machine will run without them) but are
worth a look when the operator returns on or after 2026-05-29.

Ordered by what I'd do first if I were picking it up cold.

---

## A. Polish that would obviously improve the product

### A1. Trader-nudge uses hardcoded "Hi there" / "your customer"

`scripts/trader_nudge.py` currently sends:

> Hi there,
> Quick nudge — the Crew OS quote we drafted for **your customer** went into your inbox 3 days ago.

This is because `v0/quote_engine.py`'s `process()` saves `trader_email` and
`customer_email` into the result.json but not `trader_owner_name` /
`customer_name`. Two-line fix:

1. In `v0/quote_engine.py` `process()`, copy `intake["trader"]["owner_name"]`
   and `intake["customer"]["name"]` into the result dict.
2. In `scripts/trader_nudge.py` `process_one()`, read those fields instead
   of the hardcoded fallback strings.

Why it didn't ship in v0.1.3: cosmetic, not load-bearing. Nudge still
delivers the time-saved value (£total + summary + days_ago).

### A2. `dt.datetime.utcnow()` deprecation warning in `quote_engine.py`

`process()` line ~155 still uses `dt.datetime.utcnow().isoformat()`. Python
3.12 emits a DeprecationWarning. Doesn't break anything, but `weekly_status`
and `trader_nudge` were already migrated to
`dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)`. Same change in
`quote_engine.py` for consistency.

### A3. Sample-quote screenshot on the landing page

A sceptical UK plumber arrives at crewos.co.uk and gets a copy promise
("£49/mo, branded HTML quote in 10 minutes") but no visual of what the
quote actually looks like. The smoke-test `v0/_smoke_quote.html` rendered
fine — capture a screenshot, embed it in `site/index.html` between the
"How it works" and "Join the first 5 pilots" sections. Significantly raises
conversion confidence for first-time visitors.

### A4. Privacy/legal page

The footer + the data FAQ cover GDPR-101 but a `crewos.co.uk/privacy` page
with a real (paid-template-style) policy is worth ~£0 of operator effort
(open-source templates exist). UK B2B legitimate-interest rules favour us
but a clear policy reduces ICO complaint risk and helps deliverability.

---

## B. Plumbing gaps (no pun intended) that limit upside

### B1. No Stripe / billing wiring

A pilot who loves Crew OS at the end of their 14 days has no way to pay
£49/mo. Today they'd have to email us asking how to convert. v1 needs:
- Stripe account (free signup, fee per transaction)
- Stripe Checkout link
- A workflow that marks a customer as "paid" when their checkout completes
- Auto-disable for cancelled subscriptions

Realistic scope: a half-day's work.

### B2. No bounce tracking on cold email

Resend doesn't notify us when an email bounces. Today we record "ok: True,
resend_id: xyz" in `outbound/sent.csv` and never check whether it actually
delivered. If 50% of our cold-email volume bounces, we'd never know.

Fix paths (in order of effort):
1. Manual: weekly check the Resend dashboard for bounce metrics.
2. Webhook: Resend → Cloudflare Worker → GitHub issue (new infra).
3. Polling: weekly workflow that queries Resend's `/emails` API for recent
   send statuses and updates `outbound/sent.csv` with the delivered/bounced
   verdict.

Recommend option 3 (cleanest, no new infra). ~1 day.

### B3. No structured workflow-failure notifications

If a workflow fails, the only signal is a red dot on the Actions tab.
Nobody reads it during the autonomous window. Two options:
- Add a "workflow-monitor" workflow that hourly checks the latest run of
  each workflow and writes a 🟡 banner to STATE.md if any failed in the
  last 24h. Cheap.
- Wire UptimeRobot to ping a GitHub Action that returns 500 if any
  workflow failed recently. Uses existing UptimeRobot API key. Cheaper.

### B4. ImprovMX DNS conflict (still present)

The rogue `MX @ inbound-smtp.eu-west-1.amazonaws.com` at Hostinger still
exists. Half of inbound to `hello@crewos.co.uk` / `quote@crewos.co.uk`
bounces. One Hostinger click fixes it. Operator: go to Hostinger → Domains
→ `crewos.co.uk` → DNS Zone → delete that single row.

---

## C. Product gaps the original `decision.md` promised but v0 doesn't ship

These are in `v0/README.md`'s "doesn't do yet" list — repeating here so the
return-to-work read includes them.

### C1. Voice intake
The original decision.md headline mentioned voice notes. v0 is text-only.
v1 needs file upload (Formspree free blocks this — use Tally.so free, or
add a Cloudflare Worker for direct uploads). Once a file is in, Groq's
`whisper-large-v3-turbo` is free and ready to go via `GROQ_API_KEY`.

### C2. Photo intake
Same upload-path problem. Photos would let the model understand the work
visually (e.g., "OK so that's a 30-year-old combi, your replacement will
need..."). Groq has vision-capable models on the free tier — worth piloting.

### C3. Customer-side chase
v0.1.2 added trader-nudge (we nudge the trader at 3 days). Original promise
was "we chase the customer for you." Building this responsibly needs:
- Customer email validation
- Visible unsubscribe link in the customer's view
- Multi-touch sequence (3, 7, 14 days; configurable)
- Reply detection on the customer side
- Trader override controls

~3 days of careful work to ship without spamming.

### C4. PDF output
v0 sends HTML email. Some traders will want a PDF attachment to forward.
WeasyPrint (Python) handles HTML → PDF nicely but adds system deps to the
CI runner (cairo, pango). Or use a hosted service (DocRaptor free tier).

### C5. Per-trader pricing memory
Each new intake re-asks for hourly rate + callout fee. Once a trader has
been through one round, those should be remembered. Schema:
`outbound/traders.json` keyed by email, with last-seen-pricing.

### C6. Quote-state transitions
Today a quote is sent and either gets nudged at 3 days or doesn't. There's
no "BOOKED" / "LOST" / "CHASE" state from the trader's side. If a trader
replies to a nudge with "booked", we just classify it as a cold_reply.
Real product behavior:
- "BOOKED" → close the quote, no further nudges, log to a wins ledger
- "LOST" → close the quote, log to a losses ledger, optionally ask why
- "CHASE" → escalate to customer-side chase (depends on C3)

---

## D. Repo / dev experience

### D1. No tests beyond unit cases for suppressions + send-it trigger

The quote engine is smoke-tested locally but has no automated tests.
`quote_engine.generate_quote()` could be golden-tested with a fixed Groq
response (mocked), confirming the Jinja render produces stable HTML.
Useful before any v1 refactor.

### D2. No CI lint / type-check step

`python -m py_compile` runs as part of every workflow's `pip install` — but
no `ruff` / `mypy` step catches things like unused imports or wrong types.
Add a `.github/workflows/ci-lint.yml` that runs `ruff check .` on PRs.

### D3. Structured logging

Workflows currently print JSON to stdout. Decent. But there's no structured
event log that compounds — each workflow's output is independent. A
`runs/events.jsonl` append-only log would let a future weekly-status read
"all events from week N" rather than per-workflow CSVs.

---

## E. Strategy / business

### E1. `outbound/targets.csv` is still empty

Cold-email channel is dormant. To unlock:
- Manually source 20–50 UK trade business emails from public listings
  (Checkatrade public profiles, MyBuilder, Bark, Rated People, GasSafe
  Register, NICEIC member directory).
- Or: build a respectful scraper workflow that adds 5/week.
- Or: switch primary acquisition to SEO blog (slower but autonomous).

### E2. Decision.md headline mismatch

`research/decision.md`'s opening sentence still says "voice note + photos →
sent-in-minutes branded client quote AND an automated follow-up sequence."
v0 ships none of those exactly. Log entry in `DECISIONS.md` (2026-05-16
audit) names the gap honestly. Either update decision.md to match shipped
reality OR build the missing pieces to match the headline. I'd update
decision.md unless you're going to ship voice+photos+customer-chase
in week 1 of return.

### E3. The brief said "If we built customer acquisition systems running, that's a win"

After 13 days the operator should see: any pilot signups, any quotes
generated, any nudges sent, any cold-email replies. The metrics workflows
(weekly-status + day-14-retrospective) surface this. If those are all
zeros, the next strategy question is "wedge problem or distribution
problem?" — `outbound/cold_replies.csv` + the Reddit thread comments are
the qualitative data to read.

---

## F. Out of scope for me, in scope for a returning operator

### F1. Talk to a real plumber

Three names from `research/me-profile.md` are tradespeople in the operator's
network (electrician friend, plumber friend, grandfather-with-agri-business).
The operator declined to use them for the autonomous experiment, but
post-cap is fair game. **One 20-minute call** with a real tradesperson
testing v0 would teach you more than the next 7 days of building.

### F2. Decide: continue, pivot, or pause

The Day-14 retrospective will surface a recommendation. The operator's
call on which path.

---

_File written 2026-05-16 at the end of the v0.1.3-preflight audit. Each
item is independent — pick freely. Order in this file is roughly by my
own priority sense, not commitment. The operator's free to ignore it._
