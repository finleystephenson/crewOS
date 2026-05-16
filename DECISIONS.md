# DECISIONS

_Append-only. Most recent at top. Each entry: date, decision, why, what would change my mind._

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
