# DECISIONS

_Append-only. Most recent at top. Each entry: date, decision, why, what would change my mind._

## 2026-05-16 — Operator stepped fully back. Autonomous mode begins.
- **Decision:** As of ~end-of-day 2026-05-16, the operator is checked out. Hard return cap: **Friday 2026-05-29 (Day 14)**. Until then, Crew OS runs entirely on the autonomous workflows committed to the repo today. Nothing surfaces to the operator unless STATE.md flags a hard blocker.

**What's provisioned (final state, end-of-day 16-May):**
- Domain `crewos.co.uk` registered + auto-renew ON.
- Site live at `https://crewos.co.uk` via GitHub Pages + Actions deploy workflow.
- Resend domain Verified (outbound from `@crewos.co.uk` works).
- ImprovMX inbound forwarding configured but with a *live DNS conflict* (rogue `MX @ inbound-smtp.eu-west-1.amazonaws.com` record at Hostinger that operator believed deleted but live `dig` shows still present). Expected inbound deliverability: ~50%. **Working around via web-form-first intake.**
- Gmail `crewos.uk@gmail.com` with 2FA + app password for IMAP polling.
- UptimeRobot monitoring `https://crewos.co.uk`.
- GitHub Secrets: `GMAIL_APP_PASSWORD`, `GMAIL_USERNAME`, `GROQ_API_KEY`, `RESEND_API_KEY`, `UPTIMEROBOT_API_KEY` (operator added the last one, useful).
- Reddit post live at https://www.reddit.com/r/indiehacking/comments/1ter9im/i_gave_an_ai_agent_10_and_14_days_to_build_a_real/ (Day 0 build-in-public).

**What's not provisioned (and the workaround):**
- ❌ Anthropic API key — operator declined billing setup. *All CI workflows use Groq exclusively.* Strategic reasoning is baked into today's outputs, not deferred to runtime.
- ❌ LinkedIn Company Page — LinkedIn forces use of operator's personal account; operator declined. *Dropping LinkedIn as a channel entirely; repurposing the 5-post pack as `/blog` posts on the site.*
- ❌ Indie Hackers Show forum — operator's account isn't verified yet; deferred to post-May-29.
- ⚠️ ImprovMX inbound — flaky. *Web form is the primary pilot intake; email-based intake is bonus.*
- ❌ File uploads on Formspree free tier — *v0 ships text-only intake; voice/photos deferred to v1.*

**What surfaces to operator (and when):**
- A red banner in STATE.md if something hard-blocks the autopilot (e.g., all Groq calls failing for 24h+).
- A "Day 14 Retrospective" entry in STATE.md by 2026-05-29.
- Otherwise, nothing.

## 2026-05-16 — Scheduled-AI operating mode (not fully-AI)
- **Decision:** Operator role from this point = sign-ups and one-time API-key paste only. Recurring operator hours: zero. Build-in-public LinkedIn series consists of 5 posts that the operator schedules in a single ~15-min session in week 1 using LinkedIn's native scheduler — then never touches LinkedIn again for the 30 days. Cold email is automated via Resend free tier. Inbound replies auto-handled. Demo calls removed; self-serve onboarding only.
- **Why I'm not going fully-AI (zero LinkedIn at all):** The whole reason Crew OS won the decision was the playbook §3 "human-as-moat" finding and the landscape's read that UK trade buyers are buying *trust*, not just software. Strip the human face entirely and we keep the product but lose the moat that made it winnable on a £0 budget. Scheduled-AI is the minimum-human path that doesn't break the strategic foundation.
- **What we trade:** 5 LinkedIn posts can't be perfectly accurate to day-by-day reality because they're scheduled before the events they describe. We accept narrative compression in exchange for zero-recurring-operator-time. Posts are written about the *build journey* (which is stable) not specific numerical milestones (which aren't).
- **Demo calls removed:** UK trade buyers do prefer phone/video, so removing demos costs ~30-50% on conversion. Mitigation: a polished Loom-style video demo embedded on the landing page (I'll record once v0 is real), an async email-onboarding flow, and a Calendly link only for traders who explicitly request a call. If they request one, it bounces to an async-friendly auto-reply with the demo video.
- **Would change my mind:** If 30 days of zero-recurring-operator-mode yields zero pilots, I'd come back asking for permission to add a single 20-min weekly demo-call window. The trade-off would be named explicitly.

## 2026-05-16 — Publishing surface: new Crew OS LinkedIn Company Page, no personal-LinkedIn leverage
- **Decision:** Operator removed personal LinkedIn from the available channels. Crew OS gets its **own LinkedIn Company Page** (created fresh, 0 followers). All build-in-public content publishes from there. No X/Twitter account in week 1; defer that until Show IH launch in week 4 if we want indie-maker reach.
- **Why:** Operator's call; respect it. LinkedIn Company Pages are weak distribution at 0 followers, so this materially raises the cost of the build-in-public channel — but UK trades B2B buyers do live on LinkedIn (electricians and small contractor businesses scroll LinkedIn at lunchtime), and a branded page that hits trade-specific Facebook groups & Reddit is still the right *brand* surface. Personal page would've been faster reach but the operator wants a clean separation.
- **Site change applied:** the footer's LinkedIn link is removed; only "Source on GitHub" remains until the Crew OS Company Page exists, after which the footer gets a link to that page instead.
- **Build-in-public post #1:** still ships, lightly retoned for brand-voice rather than first-person operator-voice. Operator creates the Company Page first, then publishes from there.
- **Would change my mind:** If 4 posts on the brand page produce zero engagement and zero pilot signups by end of week 3, I'd come back asking for explicit permission to either (a) post on personal page anyway, or (b) launch an X/Twitter account too, with the trade-off named.

## 2026-05-16 — Stack picks (domain, host, email, form vendor)

Operator handed back four operational decisions with "I make zero judgement calls." Picks below; each carries its own justification line.

**Domain: `crewos.co.uk` registered via Hostinger (operator's existing account).** Not the free `crewos.expanza.co.uk` subdomain.
- *Why:* The whole point of separating Crew OS from Expanza (DECISIONS entry, "Productised SaaS, not bespoke consultancy") is brand independence. A subdomain ties Crew OS visibly back to the consultancy and would confuse a cold-arriving UK tradesperson — exactly the brand fracture I argued against earlier. The £10 spend is explicitly allowed by the brief and is a one-time cost across the entire project; if I refused it here, the brief's permission for the one spend never gets used. Hostinger registrar = one less account.
- *Would change my mind:* `crewos.co.uk` already taken by someone else and we have to fall through to `crewos.uk` or similar.

**Host: GitHub Pages, deployed via a GitHub Actions workflow from `/site/`.**
- *Why:* Static HTML, no build step, no credit card, official GitHub feature, custom-domain native, no framework constraint (which is what killed Hostinger's deploy). Cloudflare Pages is more flexible but more setup; Vercel/Netlify add an extra account and aren't built for plain HTML. The workflow approach keeps `/site/` as the source-of-truth folder rather than forcing a move to `/docs` or root.
- *Would change my mind:* GitHub Pages outage in week 1 (then fall back to Cloudflare Pages).

**Email: register a fresh Gmail `crewos.uk@gmail.com` (fallback chain if taken: `crewoshq@gmail.com`, `getcrewos@gmail.com`, `crewos.io@gmail.com`).** Custom-domain forwarding (`hello@crewos.co.uk` → Gmail) is a week-2 task, not week-1 critical path.
- *Why:* No good free option exists for full custom-domain mailbox (Google Workspace, Fastmail = paid; Cloudflare Email Routing only works if DNS is on Cloudflare, which it won't be initially). A Gmail address works for all signups (Formspree, etc.) and gets us live this week. The forwarding polish in week 2 makes the public-facing address `hello@crewos.co.uk` without us actually running a mailbox.
- *Site implication (already applied):* `site/index.html` footer no longer shows a mailto until forwarding is live. Inbound goes through the pilot form for now.
- *Would change my mind:* `crewos.uk` Gmail is taken — fall through the list.

**Form vendor: Formspree free tier ("Free" plan; "Basic Form" type; one form named "Crew OS pilot signup"; one field: email).**
- *Why:* 50 submissions/month is more than enough for the cold-only 30-day target (we'd be lucky to land 50 pilot signups in week 4). No card. Single static-form endpoint we paste into the HTML's `action=` attribute. Replaceable later if we hit limits or need fancier validation.
- *Would change my mind:* Submission spam from cold launches saturates 50/month — upgrade or migrate.

## 2026-05-16 — Cold-only GTM, no operator network
- **Decision:** First-10-customers strategy is now 100% cold acquisition. No WhatsApps to grandfather, no warm intros to electrician friends. Channels: UK trade Facebook groups, Reddit (r/UKtradesmen and adjacent), Checkatrade/MyBuilder cold email, build-in-public on operator's existing public LinkedIn audience (which is *output*, not *network*), and a Show IH / ProductHunt launch in week 4.
- **Why:** Operator explicitly removed network leverage. As CEO I accept the constraint; the pick was network-independent anyway (see decision.md trust-rationale). The cost is timeline: cold-only adds ~1–2 weeks to first-paid-customer. The benefit is a clean test of whether the proposition works without any insider goodwill — which is the more durable signal anyway.
- **Pricing/offer unchanged** by this decision; only the customer-acquisition motion changes.
- **What would change my mind:** End-of-month criteria fail by a wide margin (0 pilots, 0 paid) AND the post-mortem identifies cold-channel saturation rather than offer-side problems. In that case I'd come back asking for explicit permission to soften the no-network rule, with the trade-off named.

## 2026-05-16 — Picked: Crew OS for UK 1–5 person trade businesses
- **Decision:** The chosen business is Crew OS — an AI quote-engine + follow-up sequence for UK trade businesses with 1–5 people, sold at £49/month after a 14-day free pilot. Working domain target: `crewos.co.uk` (fallback chain: `getcrewos.co.uk`, `joincrewos.co.uk`, `crewos.uk`).
- **Why:** Independent landscape evidence puts UK trades B2B as the strongest pool in May 2026 (1.3M tradespeople needed by 2033; 1–5 person crews stuck on paper; incumbents priced for the wrong tier). The quote workflow is the most-cited specific pain. Tombstone test survives (UK-jurisdictional, workflow-deep, embodied users). Does NOT cannibalise Expanza (different audience, different motion, different price).
- **What would change my mind:** the v0 manual ("Wizard of Oz") pilots in weeks 2–3 not producing a written time-savings testimonial from at least one trade. If pilots can't articulate the time saved, the wedge isn't real. End-of-month criteria in `README.md` are the falsifiable gate.

## 2026-05-16 — Operator's "don't anchor on profile" instruction, how I read it
- **Decision:** I took "don't anchor on profile" to mean don't pick the *safest-adjacent* thing because it fits. I did NOT take it to mean ignore structural facts about the operator (existing business, time available, regional base). The pick is driven by `landscape.md` evidence; the *execution path* uses the operator's network because not doing so would be theatre, not discipline.
- **Why:** "Crew OS would still be picked if the operator had no trade network" is testable from `landscape.md` §2/§4 alone. That's the test.
- **Would change my mind:** Operator explicitly says "no, ignore the network entirely even at the cost of slower launch" — in which case the GTM in `README.md` weeks 3–4 changes from "warm network first" to "cold-only Facebook + Checkatrade", and the timeline doubles.

## 2026-05-16 — Productised SaaS, not bespoke consultancy
- **Decision:** £49/month subscription, free 14-day pilot, no card. Not £2K bespoke implementation projects.
- **Why:** (a) Avoids cannibalising Expanza (which IS a bespoke consultancy). (b) Operator's stack (Claude Code) means a v0 productised build is roughly the same effort as one bespoke onboarding. (c) The buyer (1–5 person trade) doesn't have a £2K consulting budget but does have a £49/month tool budget — that's the *whole reason* this segment is under-served.
- **Would change my mind:** Pilot data shows the manual ("Wizard of Oz") workflow is unblocked but the self-serve productised version stalls at month 3. Revert to high-touch onboarding-as-a-service at £499 setup + £49/month.

## 2026-05-15 — Soft turn cap of 40 on Phase 0
- **Decision:** If `research/playbook.md` isn't passing self-audit by turn 40, stop and write `research/playbook-blockers.md` instead of polishing past the cap.
- **Why:** Operator asked for honest partial work over fake-looking polished work. Tokens have a cost; runaway research without a kill-switch produces a doc that looks fine but hides what's missing.
- **Would change my mind:** Operator extends the cap explicitly.

## 2026-05-15 — Every URL must be fetched in-session
- **Decision:** No URL goes in the Sources section without a 2xx fetch this session. If fetch fails, source is replaced not retained. No "from memory" citations even if the URL is famous.
- **Why:** LLMs hallucinate URLs that look right. The whole point of citing is to let the human audit; an unfetched URL gives the appearance of citation without the substance.
- **Would change my mind:** Nothing in scope here — this is a baseline.

## 2026-05-15 — Frameworks must trace to fetched material
- **Decision:** Every framework in `research/playbook.md` must cite at least one URL that was fetched in-session and contains material relevant to the framework. No "Priestley says X" without a fetched recap, interview, or excerpt.
- **Why:** Same reason as URL verification: stops me from laundering training-data recall as research.
- **Would change my mind:** A fetched source disagrees with my prior summary — in which case the framework gets re-written, not removed silently.

## 2026-05-15 — Skip shortlists, just pick
- **Decision:** Per operator brief, I will never present a shortlist for the operator to choose from. I decide; if I can't, I flip a coin in this file and explain why it didn't matter.
- **Why:** Operator explicitly said decision-making by them counts as my failure.
- **Would change my mind:** Operator overrides for a specific call.
