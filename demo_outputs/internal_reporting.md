# Internal Reporting // Stack Engine Output

## Input
Our internal reporting is slow and inconsistent. Each Friday people paste updates from Slack, spreadsheets, and meetings into a doc, then leadership still asks what changed and what needs attention.

## Diagnosis
The reporting process is slow because status collection and executive synthesis are treated as the same task. The stack should separate structured update capture from leadership-ready interpretation.

## Recommended Stack
- **Intelligence:** Claude
- **Memory:** Airtable, Google Drive
- **Orchestration:** n8n
- **Execution:** Slack, Google Calendar
- **Human Approval:** Slack approval message, Notion approval field

## Workflows
### 1. Structured Update Collection
- **Trigger:** Thursday afternoon reminder posts in Slack.
- **Steps:** Ask each owner for progress, blockers, metric changes, and decisions needed; Normalize responses into Airtable; Flag missing updates; Link supporting docs from Drive.
- **Human Check:** Team leads confirm their captured update before synthesis.

### 2. Leadership Brief Synthesis
- **Trigger:** All required updates are received or the deadline passes.
- **Steps:** Compare updates to last week; Identify changes that matter; Separate facts from interpretation; Draft a concise leadership brief.
- **Human Check:** Operations owner approves the brief in Slack.

### 3. Decision Follow-Through
- **Trigger:** Leadership marks an item as decision needed.
- **Steps:** Create a decision record; Assign owner and due date; Post the decision ask to Slack; Carry unresolved items into next week's report.
- **Human Check:** Decision owner confirms the action before it enters the next cycle.

## Implementation Plan
1. Define the reporting fields that every team must submit each week.
2. Create an Airtable base for weekly updates, source links, blockers, and decision requests.
3. Build an n8n workflow that posts Slack reminders and writes responses to Airtable.
4. Use Claude to turn structured records into a leadership brief with facts, changes, risks, and asks.
5. Add Slack approval before the final report is shared.
6. Run two manual reporting cycles before automating carryover decisions.

## Scorecard
- **Impact:** 4/5
- **Reliability:** 4/5
- **Fit:** 4/5
- **Complexity:** 3/5
- **Cost:** 2/5
- **Weighted Score:** 3.0

## Score Rationale
- **Impact:** Meaningful impact because faster reporting reduces leadership ambiguity and repeated status questions.
- **Reliability:** Reliable when updates are structured first and team leads approve before synthesis.
- **Fit:** Good fit because reporting needs normalization, comparison, and concise executive interpretation.
- **Complexity:** Moderate complexity because multiple teams, missing updates, and carryover decisions add process risk.
- **Cost:** Low cost because Slack, Airtable, Drive, and n8n can support the workflow without custom infrastructure.

## Verdict
MANUAL FIRST

## Prompt Pack
1. Normalize these weekly updates into progress, blockers, metric changes, decisions needed, and source links.
2. Compare this week's updates to last week's report and identify only the changes leadership should care about.
3. Draft a concise leadership report with facts, interpretation, risks, decisions needed, and unresolved carryovers.
