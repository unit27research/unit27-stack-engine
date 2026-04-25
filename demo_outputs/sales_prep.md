# Sales Prep // Stack Engine Output

## Input
Our small sales team needs better prep before discovery calls. Notes are spread across HubSpot, Gmail, and old docs, and reps waste time assembling context instead of asking sharper questions.

## Diagnosis
The team is losing leverage before calls because account context is fragmented. The stack should produce a pre-call brief that is consistent enough to trust, narrow enough to scan, and tied directly to better discovery questions.

## Recommended Stack
- **Intelligence:** Gemini, ChatGPT
- **Memory:** Google Drive, Airtable
- **Orchestration:** Zapier
- **Execution:** HubSpot, Gmail, Google Calendar
- **Human Approval:** Slack approval message

## Workflows
### 1. Account Context Assembly
- **Trigger:** A discovery call appears on tomorrow's calendar.
- **Steps:** Pull the HubSpot record; Collect recent Gmail thread summaries; Search Drive for related notes; Create a one-page account brief.
- **Human Check:** Rep confirms the brief is attached to the right account.

### 2. Discovery Question Builder
- **Trigger:** An account brief is generated.
- **Steps:** Identify likely pains; Map pains to product value; Write five call questions; Rank questions by expected signal.
- **Human Check:** Rep approves the final question set before the call.

### 3. Post-Call Next Step
- **Trigger:** Call notes are added after the meeting.
- **Steps:** Summarize buying signals; Detect objections; Draft the follow-up email; Update next action in HubSpot.
- **Human Check:** Rep reviews the Gmail draft and HubSpot update.

## Implementation Plan
1. Define a standard pre-call brief format with account facts, context, risks, and questions.
2. Create an Airtable table that maps accounts to source links and prep status.
3. Connect Google Calendar events to a Zapier workflow that finds matching HubSpot records.
4. Use Gemini or ChatGPT to summarize account sources into the brief template.
5. Send the completed brief and question set to Slack for rep approval.
6. Track call outcomes for two weeks and adjust the prompt based on rep feedback.

## Scorecard
- **Impact:** 4/5
- **Reliability:** 4/5
- **Fit:** 5/5
- **Complexity:** 3/5
- **Cost:** 3/5
- **Weighted Score:** 3.2

## Score Rationale
- **Impact:** Meaningful impact because better prep can improve discovery quality and follow-up relevance.
- **Reliability:** Reliable when constrained to source-linked briefs and rep approval before customer-facing use.
- **Fit:** Strong fit because sales prep is repeatable, context-heavy, and benefits from structured synthesis.
- **Complexity:** Moderate complexity because account matching across CRM, email, calendar, and docs can be brittle.
- **Cost:** Moderate cost because CRM and automation dependencies may already exist but require setup time.

## Verdict
MANUAL FIRST

## Prompt Pack
1. Create a pre-call brief from this account data. Focus on current context, likely pain, open questions, and risks.
2. Generate five discovery questions that would produce useful buying-signal evidence for this account.
3. Summarize these call notes into buying signals, objections, next steps, and a draft follow-up email.
