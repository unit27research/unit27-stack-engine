# Solo Founder Ops // Stack Engine Output

## Input
I am a solo founder juggling sales calls, customer follow-ups, product notes, and investor updates. Everything lives in my inbox and memory, so opportunities slip through the cracks when the week gets busy.

## Diagnosis
The founder needs a lightweight operating system, not a full CRM overhaul. The highest-value move is to centralize commitments, next actions, and weekly narrative updates so follow-through becomes visible and repeatable.

## Recommended Stack
- **Intelligence:** Claude, ChatGPT
- **Memory:** Notion, Google Drive
- **Orchestration:** Make
- **Execution:** Gmail, Google Calendar, Slack
- **Human Approval:** Notion approval field, Gmail draft review

## Workflows
### 1. Commitment Capture
- **Trigger:** A meeting ends or an important email thread changes.
- **Steps:** Extract promised follow-ups; Assign owner and due date; Link the source note or email; Place the action in a weekly operating board.
- **Human Check:** Founder approves extracted commitments before reminders are activated.

### 2. Follow-Up Drafting
- **Trigger:** A commitment is due within 24 hours.
- **Steps:** Collect relevant notes; Draft a concise update or ask; Reference the last interaction; Save the draft in Gmail.
- **Human Check:** Founder edits and sends the Gmail draft.

### 3. Weekly Investor Narrative
- **Trigger:** Friday morning calendar block begins.
- **Steps:** Summarize shipped work; Identify risks and asks; Pull customer and sales highlights; Draft a short update for stakeholders.
- **Human Check:** Founder reviews and trims the narrative before sending.

## Implementation Plan
1. Create a Notion operating board with people, commitments, status, due date, and source links.
2. Define the minimum fields that must be captured after every call or email.
3. Use Claude or ChatGPT to extract follow-ups from pasted notes and email snippets.
4. Build a Make scenario that turns approved commitments into calendar reminders and Gmail drafts.
5. Create a Friday investor-update template that pulls from the operating board.
6. Review the board every Monday and remove automations that create noise.

## Scorecard
- **Impact:** 5/5
- **Reliability:** 4/5
- **Fit:** 5/5
- **Complexity:** 3/5
- **Cost:** 2/5
- **Weighted Score:** 3.6

## Score Rationale
- **Impact:** High impact because missed follow-ups and unclear commitments directly affect revenue and momentum.
- **Reliability:** Reliable enough because the founder approves extracted commitments before reminders or drafts activate.
- **Fit:** Strong fit because the problem is information routing, summarization, and repeatable operating cadence.
- **Complexity:** Moderate complexity because email, calendar, notes, and stakeholder updates must stay synchronized.
- **Cost:** Low cost because the system can run on existing productivity tools and simple automation.

## Verdict
BUILD NOW

## Prompt Pack
1. Extract commitments, owners, dates, and open questions from these founder notes. Return only actionable items.
2. Draft a concise follow-up email based on this last interaction. Keep it specific, warm, and low-friction.
3. Turn this week's operating board into a short investor update with wins, risks, asks, and next milestones.
