# Crew OS

**The AI operating system for UK trade businesses with 1–5 people.** Takes a site visit (voice note + photos) and produces a sent-in-minutes branded client quote, then runs the follow-up sequence until the job is booked or formally lost.

Working domain target: `crewos.co.uk` (fallbacks: `getcrewos.co.uk`, `joincrewos.co.uk`, `crewos.uk`).

Decision rationale: see [`research/decision.md`](research/decision.md). Landscape evidence: [`research/landscape.md`](research/landscape.md). Frameworks the plan applies: [`research/playbook.md`](research/playbook.md).

---

## The offer (clean version)

> *"Crew OS turns the worst hour of your week — writing a quote at the kitchen table after a long day — into eight minutes on the road home. Voice-note the job and the price, photo the site, send the quote before you're back to base. We chase it for you. £49/month. 14-day free pilot, no card."*

- **Price:** £49/month per crew, or £490/year (2 months free), or £99 one-time onboarding for migrating existing quote templates.
- **Free pilot:** 14 days, no card, full functionality. Pilot cohort #1 is a hand-curated 5 from the operator's network — those pilots get the £49/month locked in for life as a thank-you.
- **What's in v0:** voice note + photos → branded PDF quote in operator's pricing voice → SMS/email send → 4-touch follow-up sequence → win/loss logged → repeat-customer reminder.
- **What's NOT in v0 (Phase 3+):** scheduling, invoicing, accountancy sync, parts ordering, team management. Quote-only on purpose.

---

## The first 10 customers and how we reach them — cold-only

Per operator instruction (2026-05-16, logged in `DECISIONS.md`): no warm network. Every customer comes from a cold channel. Slower, but a cleaner test of the proposition.

| # | Channel | Reach mechanism | Volume target (Wk1–4) |
|---|---------|-----------------|----------------------|
| 1–3 | **UK trades Facebook groups** (On the Tools UK; UK Plumbers, Heating & Gas Engineers; Electricians UK; UK Builders & Tradespeople) | One value-first post per group offering 5 free pilots in exchange for feedback. Operator posts under own name. | 5 group posts |
| 4–5 | **Reddit** (r/UKtradesmen, r/PlumbingUK, r/DIYUK with trade crossover) | Soft Show-IH-style post: "I'm building this, here's what it does, who wants in?" | 3 posts |
| 6–8 | **Checkatrade & MyBuilder profile cold-email** | Scrape (via my agent or operator's stack) listed contact emails of 1–5 person crews in NW England, NE England, Midlands. Personalised cold email referencing their own listed jobs. | 100 emails sent |
| 9 | **Build-in-public on operator's existing public LinkedIn audience** | 4 short-form posts over 30 days. *Output of public work*, not network outreach — explicitly distinct from network leverage. | 4 posts |
| 10 | **Show IH (Indie Hackers) + ProductHunt + Uneed launch** | Week 4 coordinated launch with a 60-day cohort of pilots framed as the unit of progress. | 1 launch event |

Customers 1–3 are free 14-day pilots whose feedback shapes v1. Customers 4–10 are the first paid-conversion attempts after v1 ships. **Realistic conversion expectation:** ~200 cold contacts → 5 replies → 3 booked demos → 1–2 free pilots → 1 paid by Day 30. Cold maths is honest about the funnel.

---

## What I removed from the plan (because of the no-network rule)

- Direct asks to operator's grandfather / electrician / plumber / builder friends. They are no longer pilot #1–5.
- LinkedIn DMs to operator's warm 1st-degree connections for trade referrals.
- Any Cumbria/Preston-specific WhatsApp / personal-network move.
- Tier-0 lifetime-free deals to friends-of-friends.

What remains: cold channels, operator's existing public LinkedIn *output* (not contacts), Show IH / PH / Uneed launches, and direct cold email/DM to strangers.

---

## 30-day plan — May 16 → June 14, 2026

The plan accommodates **operator A-levels through ~early June**. Operator-time is light for weeks 1–2 and ramps from week 3.

### Week 1 — May 16–22 — Foundations + landing page live (operator: ~45 min total)

**Operator (irreversible clicks):**
- [x] Day 1: Domain registered. Repo at https://github.com/finleystephenson/crewOS created.
- [ ] Day 1: Confirm which domain you actually got (`crewos.co.uk` is the assumed default). Reply with the exact string.
- [ ] Day 1–2: Push the initial project to the repo. I'll provide the exact commands in the message after this README ships.
- [ ] Day 2: Point the domain at your existing GitHub-based hosting (DNS records: I'll provide CNAME / A-record values once you confirm which hosting platform you use — sounds like GitHub Pages or similar).

**Me (no operator time required):**
- [x] Landing page v1 at `/site/index.html` — single-file, brutalist-typographic, mobile-first, with email-capture form. Ready to be wired to the domain.
- [ ] Build the v0 Claude Code workflow scaffold (voice-note → Whisper API → structured-output prompt → quote-JSON → branded PDF). No UI yet; runs locally and produces a working artefact.
- [ ] Three trade-specific quote templates as starter JSON (electrical install / boiler swap / general builder), assembled from public price-norm research.
- [ ] First three cold-outreach drafts in `/offer/cold-outreach/`: one Facebook-group post template, one Reddit Show-IH post, one Checkatrade cold-email template.

### Week 2 — May 23–29 — Cold outreach v1 (A-levels peak; operator: ~3 hours)

**Operator:**
- [ ] Post in **5 UK trades Facebook groups** (I'll provide the exact list + post text). Spread across the week, one per evening, ~10 min each.
- [ ] Post **1 Reddit Show-IH-style post** to r/UKtradesmen and one to r/IndieHacking. I'll draft.
- [ ] Send **30 personalised cold emails** to Checkatrade/MyBuilder-listed crews. I'll draft each one with the trader's own listed details quoted back to them. Operator hits send via own email so deliverability is real.
- [ ] **Post #1 of the build-in-public LinkedIn series.** Drafted by me; operator hits publish. ~5 min.

**Me:**
- [ ] Finish v0 Claude Code workflow. Goal: I can run a sample voice-note + 3 photos and produce a usable PDF quote end-to-end on my own machine within 5 minutes.
- [ ] Build a simple lead-capture / pilot-intake form on the landing page that pipes responses to a Google Sheet (via Sheets API or a Formspree free-tier endpoint, no auth fuss).
- [ ] Stand up a basic CRM-as-Google-Sheet for outbound: name, channel, message sent, replied (Y/N), demo booked (Y/N), pilot (Y/N), notes.
- [ ] Draft the second batch of cold outreach (volume target for week 3: 50 more cold emails + 5 more Facebook group posts).

### Week 3 — May 30 – June 5 — First demos + first pilots

**Goal:** 3 pilots signed up from week-2 outreach.

**Operator (~5 hours over the week, A-levels mostly finished by mid-week):**
- [ ] Respond to inbound replies from week 2 outreach. I'll draft the reply scripts; operator answers in own voice within them.
- [ ] Take **2–4 short demo calls** (15 min each) with interested traders. I'll provide a tight call script and a 1-page "what you'll get" PDF beforehand.
- [ ] Continue cold outreach: another **50 cold emails**, **5 Facebook group posts** in different communities. Drafted by me.
- [ ] **Post #2 and #3 of the build-in-public series.** Drafted by me.

**Me:**
- [ ] Run the **Wizard-of-Oz workflow** for each new pilot's first quote — operator forwards me their voice note + photos via the intake form, I run the (still partially manual) v0, send the PDF back within 30 minutes. Quote turnaround time measured.
- [ ] Tighten the v0 into something that can be self-served by a trader who isn't technical. Lovable or vanilla Tailwind on top of the existing GitHub Pages site.
- [ ] Wire up **Stripe Checkout** with the £49/month + £490/year + £99 onboarding products configured. No live charges until a pilot converts.
- [ ] Draft the 4-touch SMS/email follow-up sequence for the trader's *own customers* (the value loop the product runs for them, not for us).

### Week 4 — June 6–14 — Paid conversions + Show IH launch

**Goal:** ≥1 paying customer, public launch.

**Operator (~10 hours):**
- [ ] Ask the active pilots for written feedback and offer to convert at £49/month. I'll provide the conversion message and the testimonial-collection template.
- [ ] **Show IH / ProductHunt / Uneed coordinated launch on Day 25.** I'll prep all assets; operator hits the submit buttons.
- [ ] Continue cold outreach: 50 more cold emails to a new geography (e.g., Yorkshire / West Midlands crews).
- [ ] **Post #4 of build-in-public**: results-of-month-1 numbers, real screenshots, what's next.

**Me:**
- [ ] Productise the manual workflow into self-serve onboarding. Stripe live for conversions.
- [ ] Write the public-facing case study (1,500 words, real screenshots, time-saved numbers from actual pilots).
- [ ] Publish accumulated build-in-public posts as `/notes` on the destination site.
- [ ] Set up basic analytics (Plausible free or PostHog free) so the funnel is readable from week 5 onward.

---

## End-of-month success criteria (the falsifiable bit)

If by June 14 we do not have **all** of:

- Domain registered, site live, repo public. *(Domain + repo done at start of Phase 2; "site live on domain" is the open piece.)*
- 2+ pilots actively using v0 on real quotes (not synthetic ones). *Cold-acquired only.*
- ≥1 written pilot testimonial with a specific time-savings number.
- ≥1 paying customer at £49/month or a card-on-file pilot converting.
- ≥200 outbound cold contacts logged (emails, group posts, DMs combined).
- ≥4 build-in-public LinkedIn posts published by the operator.

— then I write a post-mortem in `STATE.md`, name what specifically blocked it, and either pivot the offer or kill the project rather than entering Month 2 on momentum. Same rule as Phase 0's turn cap: honest partial work beats pretending things are on track.

---

## Tools (all free tier or one-time spend within the £10 brief)

| Layer | Tool | Cost |
|-------|------|------|
| Domain | `crewos.co.uk` via standard registrar | ~£10 one-time (allowed by brief) |
| Hosting | Cloudflare Pages | Free |
| Repo | GitHub (operator's account) | Free |
| Email | Resend | Free tier (3K/mo) |
| Billing | Stripe Checkout + Subscriptions | Pay-per-txn only |
| Analytics | Plausible community / PostHog free tier | Free |
| Transcription | Operator's existing AI stack / Whisper local | Operator already covered |
| LLM | Anthropic API (operator's existing usage) | Operator already covered |
| DB | Supabase free tier (or SQLite in repo for v0) | Free |
| Form / UI v0 | Lovable + Tailwind / vanilla HTML | Free |
| CRM | Google Sheet → Airtable free tier if needed | Free |
| SMS (later) | Twilio sandbox (free) → trial credit | Free initially |

**Total operator spend through June 14: £10.** This stays inside the brief.

---

## What's NOT in this plan on purpose

- **No paid ads.** Zero spend, period.
- **No team hire.** Operator + me. Per `playbook.md`'s lifestyle filter.
- **No "AI for everything" pivot.** Quote workflow only. We earn the right to expand by shipping one thing that works.
- **No raising money.** Permanent constraint; not just for now.
- **No competitor with Expanza.** Productised SaaS is a different shape — not a different version of the consultancy.

---

## File structure (updated)

```
/research/
  playbook.md       — Phase 0, shipped
  landscape.md      — Phase 1, shipped
  me-profile.md     — Phase 1, shipped (with operator-summary appended)
  decision.md       — Phase 1, shipped
/idea/              — to be deleted; chosen idea is the project root now
/brand/             — week 1: name decision log + logo (text-only first)
/content/           — LinkedIn drafts + atomic essays
/site/              — Cloudflare Pages source (mirrors crewos.co.uk)
/offer/             — pricing page copy, onboarding scripts, follow-up sequences
STATE.md            — updated end of every session
DECISIONS.md        — append-only
README.md           — this file (the running plan)
```

Updates to this README will track week-by-week status checks. STATE.md gets the deep notes; DECISIONS.md gets the choice log.

---

## What I need from you, in the order I need it (cold-only edit)

1. **Now (Day 1):** confirm the exact domain you registered, and tell me which hosting platform you're using (GitHub Pages? Cloudflare Pages? Vercel? Netlify?). I need to know the DNS target.
2. **Day 1–2:** push the initial project to the repo. Exact commands provided in the chat message after this README.
3. **Day 2–3:** point the domain DNS at your hosting per the values I'll give you.
4. **Week 2 (A-levels peak):** ~3 hours of cold outreach button-pressing (5 Facebook group posts, 30 cold emails, 2 Reddit posts, 1 LinkedIn build-in-public post). All drafted by me; you hit publish/send.
5. **Week 3 (A-levels ending):** ~5 hours including 2–4 short demo calls with interested traders.
6. **Week 4 (post-A-levels):** ~10 hours including Show IH/PH launch, conversion conversations, more cold outreach.

Total ~18–22 operator hours across the month under the cold-only rule (up from the ~12–15 hours that the network-leveraged version would've cost). The trade-off is logged in `DECISIONS.md`.

That's it. Now I start building.
