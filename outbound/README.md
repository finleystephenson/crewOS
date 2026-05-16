# /outbound — Crew OS cold-acquisition state

This folder is the **shared brain** for cold-acquisition. Everything append-only.

## Files

| File | Written by | Purpose |
|---|---|---|
| `targets.csv` | manually populated; future scrape workflow | Cold-email target list. Each row = one UK trade business to email. |
| `sent.csv` | cold-email-batch workflow | Log of every cold email sent — when, to whom, with what variant. |
| `signups.csv` | inbound-triage workflow | Every pilot signup from the landing-page form. |
| `intakes.csv` | inbound-triage workflow | Every successful intake reply that went into the quote engine. |
| `cold_replies.csv` | inbound-triage workflow | Every reply to a cold email (auto-acked + logged). |
| `needs_human.csv` | inbound-triage workflow | Emails that didn't classify — for a human to read on May 29+. |

## `targets.csv` schema

```
email,first_name,business_name,trade,town,country,source_url,added_at,sent_at,reply_at,notes
```

- `email` (required, unique key)
- `first_name` (used for personalisation)
- `business_name` (used for personalisation)
- `trade` — one of: `electrical`, `plumbing_heating`, `building`, `groundworks`, `bricklaying`, `general`
- `town` — UK town/city, used for personalisation
- `country` — should always be `UK` (we don't email outside the UK)
- `source_url` — where we found this contact, for audit trail
- `added_at` — ISO date when added
- `sent_at` — ISO datetime, set by cold-email-batch on send. Empty = not yet sent.
- `reply_at` — ISO datetime, set by inbound-triage if a reply comes in.
- `notes` — anything

## Acceptable target sources

- Public UK trade directories that explicitly list business contact emails for inquiries (Checkatrade, MyBuilder, Bark, Rated People — all permit public listing of email-on-business-profile per their ToS).
- Tradesperson business websites with a public `info@` or `contact@` email visible without scraping past a CAPTCHA or login.
- LinkedIn business pages with a public contact email (rare).

## NOT acceptable

- Personal Gmail / Yahoo / Hotmail addresses unless explicitly listed as the trader's *business* contact.
- Email harvested from anywhere behind a login or CAPTCHA.
- Email patterns guessed from a name + business domain (e.g., trying `firstname@business.co.uk` without verification).
- Anyone who's previously replied with anything that suggests opt-out.

## Volume guidance

- v0 / first 14 days: **0-5 emails/day** while the new domain warms up. Resend free tier supports 100/day; we deliberately stay tiny early.
- Post-warmup (post-May-29): scale to 20-50/day if reply rates justify.

## Status

As of 2026-05-16 (Day 0 closeout): `targets.csv` is empty. Cold-acquisition is dormant until populated. Inbound from Reddit / SEO / direct discovery is the primary acquisition channel for the 14-day window. See `STATE.md` for the honest read.
