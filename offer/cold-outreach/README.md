# /offer/cold-outreach/ — historic outreach drafts

**Status: superseded as of 2026-05-16.** These three files were drafted under
the original "operator hits send" model (operator's voice, manual posting).
After 2026-05-16 the operator stepped fully back; the live cold-outreach
machine is the workflow.

**What replaced these:**

| Old file | What's live now |
|---|---|
| `checkatrade-cold-email.md` | `scripts/cold_email_batch.py` — generates personalised emails via Groq Llama-3.3-70B and sends via Resend on a daily cron. The `COLD_SYSTEM_PROMPT` constant in that file is the canonical voice and rules. |
| `facebook-group-post.md` | Dropped. Facebook group posting can't be automated within ToS; the operator stepped back so this channel is dormant for the 14-day autonomous period. |
| `reddit-show-ih.md` | One-shot Reddit post was published on Day 0 at https://www.reddit.com/r/indiehacking/comments/1ter9im/i_gave_an_ai_agent_10_and_14_days_to_build_a_real/ . No ongoing Reddit automation. |

If reactivating any of these channels manually post-2026-05-29: the templates
here are good starting points but the **voice has shifted** from operator-first
("I'm 18 building this") to brand-first with transparent AI authorship.
Reference the live workflow prompts before reusing.
