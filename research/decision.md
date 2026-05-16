# Decision

## The chosen business — in one sentence

**Crew OS — the AI operating system for UK trade businesses with 1–5 people, turning a site visit (voice note + photos) into a sent-in-minutes branded client quote and an automated follow-up sequence, sold at £49/month after a 14-day free pilot.**

---

## Why it won (one page)

The pick is **Pool A** from `landscape.md` — UK trades B2B for the under-served 1–5 person crew segment — operationalised around the single most expensive workflow in a trade business: **the quote**.

Three independent lines of evidence point here, and they don't share root causes:

1. **The macro tide.** UK demand for tradespeople runs structurally hot through 2033 — 1.3M new tradespeople needed, immediate shortfall of 250,000+ workers, self-employed electricians earning £55K+, electrician business owners ~£65K ([landscape §2](./landscape.md)). Net-zero electrification + EV charging + heat-pump rollout drive durable demand. These buyers are *cash-flush and software-light*.
2. **The product gap.** ServiceTitan, Housecall Pro and Commusoft are priced and architected for 20+ employee operations (£200–500/month). The 1–5 person crew is stuck on paper invoices, generic spreadsheets, and phone-based scheduling. ServiceTitan's own marketing copy admits the current state is *"customer info scribbled on paper, typed into Excel, or scattered across multiple systems"* — they're describing the buyer they can't profitably serve. The most specific quoted pain across multiple landscape sources is **the quote workflow itself**: *"spending half their day creating estimates that may never convert."*
3. **The tombstone test.** Write the 2027 obituary for this business. Most likely cause of death: *"out-competed by a better-funded specialist with the same wedge"* — i.e., operator-side, not structural. Not killed by next-gen frontier models, because the moat lives in (a) UK-specific compliance (CIS, VAT for subbies, gas-safe certification, NICEIC, FENSA, trade-specific paperwork), (b) workflow depth that survives a single prompt, and (c) human-to-human trust between the trade business and their client which the tool serves rather than replaces. Survives.

**Why this specific wedge, not "AI for trades" generally.** Trade businesses lose more money to *quotes that never convert* than to almost any other workflow inefficiency. A quote-to-win cycle that takes a tradesperson an hour at the kitchen table (or worse, gets forgotten for three days while they're on-site) is a known, named, recurring pain. The AI lift is real and verifiable in v1: take a voice note from the site visit + three photos + the client's address, generate a line-itemised, branded PDF quote in the trade's own pricing voice, send it, and run a polite SMS/email follow-up sequence until booked or formally lost. This is a discrete, ship-in-weeks v0. Everything else (job scheduling, invoicing, parts ordering, accountancy integration) is *next*; the quote is *now*.

**Why £49/month, not bespoke services.** Service-first sounds like the safe ladder, but for this segment the operator (Claude Code-native) can ship a working productised v0 in the same time it would take to onboard a single bespoke client. The ladder we'll actually run: free 14-day pilot (no card) → £49/month or £490/year per crew, with a £99 onboarding session for crews that want me to migrate their existing quote templates. Margin is fine; CAC at £20–80 per indie-hacker benchmark from `playbook.md` is fine; the maths only requires ~500 paying crews for £24K MRR.

**Why it doesn't cannibalise Expanza.** Expanza is bespoke AI consultancy for UK SMEs — high-ticket, custom, founder-led delivery. Crew OS is productised SaaS for a named vertical at a fixed price point with self-serve onboarding. Different buyers (Expanza buyer = office-based SME owner who wants AI-assisted client acquisition; Crew OS buyer = field-based tradesperson who wants paperwork to disappear), different motion (consult vs. subscription), different price (5-figure projects vs. £49/month). If anything, Crew OS *de-risks* Expanza by making the operator's "AI Operating System" thesis visible in a vertical where it can be ruthlessly productised.

**Why an 18-year-old with no trade experience can credibly ship this.** Because the product is the product, not the operator. The buyer doesn't need to know my age; they need to know that the quote went out in 8 minutes and the customer paid. The first ten pilots come from the operator's existing trade-adjacent network (grandfather, electrician friends, builder friends), all of whom can be approached as "let me run this on your last three quotes for free, you keep the data either way." Credibility compounds from named pilot results, not from operator biography.

**Why now and not in 2024.** The voice-to-quote workflow only became reliably good enough for production use in late 2025 with the current generation of speech recognition + structured-output LLMs. Before that, you couldn't ship a v0 in weeks; now you can. This is the playbook's "live in the future" criterion (Source: Paul Graham essay, fetched in playbook session) applied literally — *the timing window opened recently and most of the field-service incumbents haven't moved into it yet*.

---

## The two runners-up

1. **"BidLift" — an AI bid-engine for UK construction subcontractors (groundworks, brickwork, joinery, MEP)**, taking architect's plans + scope + take-off and producing a priced bid within hours. **Lost because:** longer sales cycles, bigger contract values but each customer takes more relationship work to close; v0 build is materially harder (CAD parsing, BoQ generation); first-£100 timeline is 12+ weeks not 4–6.

2. **"CareCompliance" — a vertical-AI tool for UK independent care home operators**, handling CQC documentation, shift-log narratives, family-comms templates, and incident reporting. **Lost because:** heavily regulated buyer with long procurement cycles, no operator network in the care sector, and the regulatory complexity is real enough that getting it wrong has consequences I'm not equipped to absorb at v0.

---

## Why you should trust this pick despite me only knowing you from one questionnaire

Three reasons, none of which rely on you taking my word for it:

1. **The pick is independent of your profile in the part that matters.** The landscape analysis put UK trades B2B as Pool A *before* I read your answers. If you'd handed me a profile with zero trade adjacency, I'd still pick this — the launch path would just be slower and more outreach-heavy. You can audit that claim by reading `landscape.md` §2 and §4 without reference to anything about you, then asking whether the conclusion holds.
2. **Where your profile *did* affect things, I'm being explicit.** Your existing network into UK trades makes the first-10-customers problem materially cheaper, so the *go-to-market plan* leans on it. Your existing business (Expanza) is the reason I picked a productised SaaS at £49/month rather than another consultancy — that's *avoiding* a profile-anchored mistake, not making one. Your Claude Code fluency is why I'm comfortable with a build-in-public timeline measured in weeks not months. Each of these is called out in the plan; you can disagree and tell me to revise.
3. **The tombstone test is honest.** I've named the most likely death (out-competed by a better-funded specialist) rather than the most flattering one. If the business dies, it'll be operator-execution-side, not because the underlying landscape was wrong. That's the failure mode I'd rather have than "I picked a category that the next OpenAI release just absorbed."

---

## What happens next

Per the brief, I now move directly to Phase 2 — the 30-day plan goes in `README.md`. Two real-world actions I'll need from you in the first 7 days, both irreversible:

1. **Register a domain.** Target: `crewos.co.uk`. Fallbacks in priority order: `getcrewos.co.uk`, `joincrewos.co.uk`, `crewos.uk`. Budget: the ~£10 allowed by the brief.
2. **Talk to your grandfather and at least two trade friends** about being unpaid pilot customers in weeks 2–3. I'll provide the exact message to send — you're the one who hits send.

Everything else — the build, the offer, the onboarding flow, the content, the cold outreach scripts — I'll handle.

I'm not asking for sign-off on the pick. Per the brief, I move on.
