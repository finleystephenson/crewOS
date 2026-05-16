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
