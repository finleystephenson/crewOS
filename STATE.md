# STATE

_Updated end-of-session. Most recent at top._

## 2026-05-15 — Session 1
**Did:**
- Scaffolded project (folders, STATE.md, DECISIONS.md, README.md).
- Approved /goal for `research/playbook.md` with three operator-imposed amendments.
- **Phase 0 complete.** Shipped `research/playbook.md` — 4,691 words, 26 verified sources, all six required sections, passing every self-audit check.

**Self-audit results:**
- File exists, ≥3,500 words: 4,691 ✓
- Thesis ≥500 words: 712 ✓
- ≥5 falsifiable claims: 5 numbered ✓
- ≥12 frameworks (≥4 Priestley + ≥6 outside): 4 + 13 = 17 ✓
- Scoring rubric weights sum to 100, with worked example: 15+15+15+12+10+10+8+10+5 = 100 ✓
- ≥5 contradictions: 7 ✓
- 2026 edge section: alive/dead/asymmetric subsections ✓
- ≥25 distinct URLs, all fetched 2xx in-session: 26 ✓
- Every framework cites a fetched source ✓
- Turn budget: well under the 40-cap (~17 turns used)

**Decided:** See `DECISIONS.md` entries dated 2026-05-15.

**Next:** Phase 1. The first deliverable is `research/landscape.md` (where the £0-lifestyle-business gaps are in May 2026, evidence-cited, tombstone-tested). After that comes the one-shot questionnaire (`research/me-profile.md`) — this is the only point in the project where I'll surface questions to the operator.

**Blocked:** Nothing.

## 2026-05-15 — Session 1 (continued)
**Did:**
- Shipped `research/landscape.md`: 3,660 words, 20 verified URLs, 5 sections all ≥400 words, tombstone exercise on top 5 niches, passes self-audit (target ≥3,000 words, ≥400 per section, ≥3 sources per section, ≥20 distinct URLs).
- Shipped `research/me-profile.md`: 20-question one-shot questionnaire across 6 categories (skills, interests, irritations, network, prior attempts, constraints).

**Landscape highlights pulled forward into the decision-frame:**
- The pick will almost certainly be in **Pool A** (B2B for UK trades / 1–5 person field-service crews) or **Pool C** (reskilling/coaching for displaced or transitioning white-collar workers), with **Pool B** (services for AI-augmented freelancers) as fallback.
- Will be operator-led (face/name), vertical-deep (named region/regulator/customer type), and sequence service → productise → optional software.
- Niches that pass the tombstone test: trades back-office for 1–5 person crews; reskilling/coaching for white-collar transitioning workers; UK specialty food producer compliance; solo legal practitioner vertical-AI tooling; wedding/event vendor coordination.

**Next:** Operator fills `research/me-profile.md` and replies "filled" (or pastes contents). Then I summarise their profile, score 10 concepts privately, and ship `research/decision.md`. After decision lands, Phase 2 plan goes into `README.md`.

**Blocked:** Waiting on operator to fill questionnaire. This is the only blocked-on-operator step in the project.

## 2026-05-16 — Session 2 (Phase 1 closeout + Phase 2 kickoff)
**Did:**
- Operator filled `research/me-profile.md` end-to-end. Notable: 18yo UK, already runs Expanza (AI consultancy for UK SMEs), Claude Code-native, large UK trades network via grandfather + friends, A-levels in 2 weeks (near-term time constraint).
- Operator added an explicit reframe: "don't anchor on my profile; pick what works." Handled — see new entries in `DECISIONS.md`.
- Appended **"Operator-summary as Claude understood it"** (~480 words) to `research/me-profile.md`.
- Scored 10 concepts privately against playbook rubric. Winner: **Crew OS** at 79/100.
- Shipped `research/decision.md`: Crew OS chosen, two runners-up named (BidLift, CareCompliance), trust-the-pick rationale included.
- Rewrote `README.md` as the 30-day execution plan: named first-10 customers, weekly cadence May 16 → June 14, falsifiable end-of-month success criteria.

**Decided (full entries in `DECISIONS.md`):**
- The pick: Crew OS for UK 1–5 person trade businesses, £49/mo productised SaaS.
- Domain target: `crewos.co.uk` (fallback chain: `getcrewos.co.uk`, `joincrewos.co.uk`, `crewos.uk`).
- "Don't anchor on profile" interpreted as: pick driven by `landscape.md`, not by what's safest-adjacent; execution path *does* use operator's trades network because ignoring it would be theatre.
- Productised £49/mo, not bespoke consultancy — avoids cannibalising Expanza.

**Next (Phase 2, week 1):**
1. **Operator action (irreversible):** register `crewos.co.uk` (~£10) and confirm; create GitHub repo `crewos` and Cloudflare Pages project pointing at it.
2. Once that lands, I draft the three WhatsApp messages to grandfather + electrician friend + plumber friend, operator hits send.
3. I begin the Claude Code v0 build (voice-note → quote-PDF + follow-up sequence) and stand up the landing page on Cloudflare Pages.

**Blocked:** Domain registration. Nothing else can ship cleanly until the domain + repo are live.

## 2026-05-16 — Session 2 (cont.) — Cold-only constraint + first build
**Did:**
- Operator registered the domain and created the GitHub repo (https://github.com/finleystephenson/crewOS). Operator also explicitly removed warm-network leverage: **cold-only GTM** from here.
- Logged the no-network rule in `DECISIONS.md` with the cost (timeline +1–2 weeks, operator hours +6–7) made explicit.
- Rewrote the GTM section of `README.md`: first-10-customers table is now 100% cold channels (UK trades Facebook groups, Reddit, Checkatrade/MyBuilder cold email, build-in-public on operator's existing public LinkedIn output, Show IH/PH launch).
- Adjusted end-of-month success criteria for the cold-only reality: 2+ pilots (down from 3), 200+ cold contacts logged (up from 10 conversations).
- Built **`/site/index.html`** — brutalist-typographic single-file landing page (UK-trade voice, 5-pilot ask, FAQ, pricing bar, formspree-ready email capture). Mobile-first, no JS, no dependencies, no build step. Ready to deploy to GitHub Pages.
- Initialised git in the project dir, added the GitHub remote, wrote `.gitignore`, staged all 9 files. **Not committed** — operator's git identity isn't set globally; per the brief, I won't modify git config without explicit instruction. Operator commits + pushes.
- Drafted **LinkedIn build-in-public post #1** at `/content/linkedin-buildinpublic-01.md` ready to publish today.

**Open operator clicks (in order):**
1. Confirm which exact domain you got (assuming `crewos.co.uk`; tell me if different).
2. Confirm which hosting platform — GitHub Pages? Cloudflare Pages? Vercel? Netlify? — so I can give you the right DNS target.
3. Set local git identity (one-time, ~30 sec): `git config user.name "Finley Stephenson"` then `git config user.email "your@email"`.
4. Commit + push: `git commit -m "Crew OS — phase 0+1 docs, landing page v1"` then `git push -u origin main`.
5. Sign up for Formspree free tier, create a form, replace `REPLACE_FORM_ID` in `site/index.html` line 137-ish with the form ID. (~5 min.)
6. Once hosting is confirmed, point the domain DNS at the hosting platform per the values I'll provide. Add a `site/CNAME` file containing just `crewos.co.uk` if GitHub Pages.
7. Optionally publish `/content/linkedin-buildinpublic-01.md` today as the Day-1 build-in-public post.

**Next (my side, after operator answers Q1+Q2):**
- Provide exact DNS values for whichever hosting platform.
- Write the cold-outreach pack: 3 Facebook-group post variants, 1 Reddit Show-IH post, 1 Checkatrade cold-email template. Ship to `/offer/cold-outreach/`.
- Begin v0 quote-engine build in `/v0/` (Python + Anthropic API + Whisper, runs locally end-to-end first).

**Blocked:** Operator clicks 1–4 above. Everything I can do without operator's hands is queued up to start the moment the repo is live.

## 2026-05-16 — Session 2 (cont.) — Stack picks made, click-by-click handoff
**Did:**
- Operator handed back the four operational picks. Made them all in `DECISIONS.md` and prepped supporting files:
  - **Domain:** `crewos.co.uk` registered via Hostinger (~£10, the brief's one allowed spend).
  - **Host:** GitHub Pages via Actions workflow (`/site/` is the source of truth).
  - **Email:** `crewos.uk@gmail.com` (fallback chain documented).
  - **Form:** Formspree free tier; one form, email-only field.
- Added `.github/workflows/deploy.yml` (standard GitHub-Pages-via-Actions).
- Added `site/CNAME` containing `crewos.co.uk`.
- Edited `site/index.html` footer to drop the broken mailto until ImprovMX forwarding is live in week 2; added a LinkedIn link (assumed `linkedin.com/in/finleystephenson/` — operator can correct).
- Staged 12 files. **Still not committed** — operator's git identity isn't set (per brief, I don't modify config). Commit + push are operator steps in the handoff.
- Wrote the full click-by-click handoff in the chat reply.

**Next (my side, after operator finishes click checklist):**
- Verify the site is live at `https://crewos.co.uk` and the Formspree form posts a real test signup.
- Ship the cold-outreach pack (`/offer/cold-outreach/`): 3 FB-group variants, 1 Reddit Show-IH, 1 Checkatrade cold email.
- Begin v0 quote engine in `/v0/`.
- Set up ImprovMX forwarding `hello@crewos.co.uk → crewos.uk@gmail.com` once Gmail is registered (week 2 task; deferred to keep the critical path clean).

**Blocked:** Operator click-by-click checklist (~10 steps, est. 25 min).

## 2026-05-16 — Session 2 (cont.) — Status post-first-push
**Operator-side progress:**
- ✅ Gmail registered: `crewos.uk@gmail.com`. (Password leaked into chat; operator instructed to rotate.)
- ✅ Domain registered: `crewos.co.uk` via Hostinger.
- ✅ First push to GitHub: 12 files, root commit `0008c75`. Repo is now public at https://github.com/finleystephenson/crewOS.
- ✅ Formspree form created. Form ID: `maqvrvve`. Plan: free.
- ❌ GitHub Pages: not enabled yet ("it didn't work" — operator did not complete the Settings → Pages → Source = "GitHub Actions" step).
- ❌ DNS at Hostinger: "I think I broke it" — incomplete; needs nuke-and-pave below.
- ⛔ Personal LinkedIn ruled out by operator. Replaced with: create a fresh Crew OS LinkedIn Company Page; rebrand build-in-public to post from there.

**My-side changes this turn:**
- Patched `site/index.html`: real Formspree ID wired in; personal LinkedIn link removed from footer.
- Lightly retoned `content/linkedin-buildinpublic-01.md` from operator-voice → brand-voice (Company Page).
- `DECISIONS.md`: new entry "Publishing surface: new Crew OS LinkedIn Company Page, no personal-LinkedIn leverage" added at top.

**Next operator clicks (in chat):**
1. Rotate Gmail password (security).
2. Enable Pages with the *exact* clicks I've spelt out for the Settings page.
3. DNS nuke-and-pave at Hostinger using the explicit table I've given.
4. Create Crew OS LinkedIn Company Page (~3 min).
5. `git commit -m "Wire Formspree + drop personal LinkedIn + Company Page brand voice"` + `git push`.

**Once those land:** site is live at https://crewos.co.uk with working form; build-in-public post #1 publishes from the Crew OS Company Page; I move to cold-outreach pack + v0 quote engine.

## 2026-05-16 — Session 2 (cont.) — SITE IS LIVE
- ✅ **`https://crewos.co.uk` returns HTTP 200.** DNS resolves to four GitHub Pages IPs as expected. `www.crewos.co.uk` CNAMEs correctly to `finleystephenson.github.io`. HTTPS works.
- ✅ Pages workflow deployed (green tick on GitHub Actions).
- ✅ Formspree wired with form ID `maqvrvve`. Footer cleaned of personal LinkedIn.
- ✅ DECISIONS.md updated with **scheduled-AI operating mode** as the official stance.

**Content + outreach pack shipped this turn (in repo, ready for use):**
- `content/linkedin-posts-pack.md` — 5 LinkedIn build-in-public posts written, calibrated for one-session scheduling.
- `offer/cold-outreach/facebook-group-post.md` — UK trades Facebook group template + 5 target groups.
- `offer/cold-outreach/reddit-show-ih.md` — Reddit + Indie Hackers Show post template + 5 target subs.
- `offer/cold-outreach/checkatrade-cold-email.md` — cold email template, sending rules, deliverability requirements, volume targets, expected funnel maths.

**Still operator-pending (one batched session, ~30 min):**
1. Create Crew OS LinkedIn Company Page (step set previously, 17–26).
2. Schedule 5 LinkedIn posts using LinkedIn native scheduler.
3. Sign up for Resend (free tier, no card) → paste API key into GitHub repository secrets.
4. Sign up for ImprovMX (free tier) → set up hello@crewos.co.uk → crewos.uk@gmail.com forwarding.
5. Join 5 UK trades Facebook groups (admin-approval, async wait).
6. Push the pending 4 modified files + the new pack files.

**Next (my side, no operator click needed):**
- Begin v0 quote engine in `/v0/` (Python + Anthropic API + Whisper). Goal: voice-note + 3 photos → branded PDF quote, runnable end-to-end on my machine before next operator handoff.
- Set up the GitHub Actions secrets schema (placeholder names so operator pastes API keys into the right place).
- Draft the auto-reply email template for Formspree submissions.

---

## 2026-05-16 — DAY 0 CLOSEOUT — Operator stepped back. Autonomous mode begins.

### Snapshot at handoff

| Domain | `https://crewos.co.uk` — live, HTTPS, HTTP 200 |
| Repo | `https://github.com/finleystephenson/crewOS` — 3 commits, clean |
| Operator return cap | **Friday 2026-05-29 (Day 14)** |

### What landed in the operator's final session

- 4 of 5 GitHub Secrets in place: `RESEND_API_KEY`, `GROQ_API_KEY`, `GMAIL_APP_PASSWORD`, `GMAIL_USERNAME` (+ a bonus `UPTIMEROBOT_API_KEY`). **Anthropic SKIPPED** at operator's choice — no Claude API in CI.
- Resend domain `crewos.co.uk` Verified (outbound works).
- DNS SPF merged correctly (`v=spf1 include:spf.improvmx.com include:amazonses.com ~all`).
- UptimeRobot monitor on the site.
- Reddit post Day-0 live at https://www.reddit.com/r/indiehacking/comments/1ter9im/i_gave_an_ai_agent_10_and_14_days_to_build_a_real/
- All three rotated credentials are in repo Secrets (post-rotation; the leaked chat-log versions are revoked).

### KNOWN ISSUES at handoff (workarounds in place)

🟡 **ImprovMX MX conflict (DNS).** Live `dig` shows `inbound-smtp.eu-west-1.amazonaws.com` still on apex with priority 10, tied with `mx1.improvmx.com`. Operator believed this was deleted but it wasn't. Expected: ~50% of inbound to `hello@crewos.co.uk` will fail / bounce. **Workaround:** v0 pilot intake = Formspree web form (100% reliable); email-based intake on `quote@crewos.co.uk` becomes a bonus path that works ~half the time. Fix is one Hostinger click whenever operator returns.

🟡 **No Anthropic API in CI.** All AI in workflows uses Groq (Llama 3.3 70B + Whisper-large-v3). Step down in quality from Claude for nuanced tasks; deterministic prompt engineering compensates.

🟡 **LinkedIn dropped.** Operator declined to admin a Company Page from personal account. The 5 LinkedIn posts I drafted are being repurposed as `/blog` posts.

🟡 **Formspree free tier blocks file uploads.** v0 ships text-only intake. Voice notes + photos deferred to v1 (post-May-29).

🟡 **No demo calls + no real-time engagement.** No human present means we can't reply to comments on Reddit, pick up phone calls, run live demos. Conversion will be lower; tracked.

### What I'm building tonight (no operator clicks needed)

1. v0 quote engine in `/v0/` (Python; Groq Llama 3.3 70B + Resend; text-input → HTML email quote in <30 sec).
2. Five GitHub Actions workflows: `cold-email-batch`, `inbound-triage`, `quote-engine-runner`, `weekly-status`, `ceo-pulse`.
3. Seed list of ~100 UK trade businesses for cold email (from public sources, today's session).
4. Rewritten cold-outreach pack in brand voice with AI transparency footer.
5. `/site/blog/` scaffolding + 5 repurposed posts from the LinkedIn pack.
6. `RUNBOOK.md` — written for "a stranger picks this up on Day 14 and has to operate it from cold."
7. Landing page tweak: web form becomes primary intake; voice/photos messaging becomes "v1 feature".
8. README rewrite for autonomous operating mode.
9. Final commit + push + tag `v0.1.0-handoff`.

By 2026-05-29 (Day 14), STATE.md will contain a retrospective: what shipped, what worked, what didn't, what to do next. Until then, Crew OS runs on the workflows.
