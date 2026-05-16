# Cold-outreach: Checkatrade / MyBuilder cold email

## Strategy

Checkatrade and MyBuilder publicly list small UK trade businesses with contact details. We scrape (manually, via me) name + business + town + listed email/phone, then send a personalised cold email referencing their own listed details.

Automated via Resend free tier (3K emails/month free, no card). Operator setup: one Resend signup + paste API key into the repo as a GitHub Actions secret. After that, I run sends.

## Personalisation requirements (so it doesn't read as spam)

Every email must include:
- The trader's first name (from listing).
- Their business name.
- Their primary trade (electrician / plumber / builder / etc.).
- One specific detail from their listing — e.g., "I saw your 14 reviews mention turnaround time" or "noticed you're focused on commercial in [town]". If we can't find a specific detail, skip that listing — don't send a generic email.

## Email template (UK-flavoured, plain text, no images)

**Subject:** Quoting take an hour for [Business Name]?

**Body:**

> Hi [First name],
>
> I came across [Business Name] on Checkatrade — saw [specific detail, e.g. "the 23 five-star reviews from [town]" or "you focus on [specific work type]"].
>
> Quick question: how long does it usually take you to write up a quote after a site visit? Most of the traders I'm talking to say 30–60 min, mostly at the kitchen table after hours.
>
> I've spent the last week building **Crew OS** — a tool that turns a voice note + a few photos from the site into a branded, accurate quote in under 10 minutes, plus auto-follow-up the customer.
>
> Built specifically for 1–5 person crews. £49/mo, free 14-day pilot, no card. Looking for 5 UK tradespeople to try it this week and tell me where it breaks.
>
> If that's a yes, reply with the words "send it" and I'll send a 5-minute onboarding link.
>
> If not, no follow-up — promise.
>
> Cheers,
> Finley
> crewos.co.uk

## Sending rules (deliverability)

- **From address:** `finley@crewos.co.uk` (once ImprovMX forwarding is live). Until then, fall back to `crewos.uk@gmail.com`.
- **Reply-to:** same as From.
- **Volume:** 20 emails/day max for the first 7 days (warm-up). Then 50/day max. Never burst-send 100+ in a sitting from a new domain — go straight to spam.
- **DKIM/SPF/DMARC:** must be configured on `crewos.co.uk` before any send via Resend. I'll handle the DNS records once operator authorises (no operator action beyond pasting four DNS records into Hostinger).
- **Targets:** UK only. NW England, Yorkshire, Midlands, NE, SW in that priority order — start where competition for tradesperson attention is lower.
- **Don't email anyone twice** within 30 days unless they replied.
- **Unsubscribe link** at the bottom is mandatory by UK law (CAN-SPAM equivalent). Resend handles this automatically.

## Volume targets

- Week 2: 60 emails (20/day × 3 days, warm-up week).
- Week 3: 150 emails (50/day × 3 days).
- Week 4: 150 emails to a new geography.
- Total: ~360 cold emails across the 30 days.

## Expected funnel

Honest cold-email maths:
- 360 sent → 100 opens (28% open) → 12 replies (3.4% reply, on the high end for cold) → 5 demos requested → 2–3 free pilots → 1 paid.

Anything materially below these conversion rates and we revisit the wedge in week 4.

## Operator role

- One-time: sign up for Resend free tier. Sign up for ImprovMX free tier. Paste API keys into GitHub repository secrets. (~10 min total, all in one session per click-by-click in chat.)
- Recurring: zero. I send.
- If a tradesperson replies with "send it" or "interested": Formspree-style auto-reply sends the onboarding link with the pilot signup form. No operator action.
- If a reply requires judgement: I draft the reply text and the operator pastes-and-sends from the Gmail. Estimated <5 such cases across 30 days.
