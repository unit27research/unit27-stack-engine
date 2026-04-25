# Design Notes

Stack Engine is intentionally small. The point is not to build another chatbot UI or a generic automation marketplace. The point is to show how an ambiguous operational goal can be converted into a constrained, inspectable AI workflow architecture.

The core design claim is:

> AI systems become more useful when generation is wrapped in structure, constraints, scoring, and human approval.

## Why This Is Not A Chatbot

Most chatbot answers stop at advice. Stack Engine turns the same input into a decision artifact:

1. Diagnose the operational pattern.
2. Recommend a bounded tool stack.
3. Define concrete workflows.
4. Produce an implementation plan.
5. Score the opportunity.
6. Explain the score.
7. Return a build verdict.
8. Provide prompts that can actually operate the system.

The UI and CLI are thin on purpose. The product surface is the artifact, not the conversation.

## System Shape

The engine has three layers:

- **Generative layer:** Converts messy input into structured JSON.
- **Constraint layer:** Enforces schema shape, catalog-approved tools, count requirements, score ranges, and meaningful text.
- **Decision layer:** Computes deterministic score and verdict, then renders the output as markdown.

Saved examples and live model outputs travel through the same validation, scoring, and rendering path. The markdown demo files are generated exports, not a second source of truth.

## Why Deterministic Scoring Exists

The model recommends raw scorecard values, but Stack Engine owns the final weighted score and verdict.

That split is deliberate:

- The model can judge messy context.
- The engine applies a stable rubric.
- Reviewers can inspect the weights.
- Saved demos and live generations remain comparable.

The current score formula is not meant to be universal. It is a simple MVP rubric:

```text
impact * 0.35
+ reliability * 0.25
+ fit * 0.25
- complexity * 0.10
- cost * 0.05
```

This favors high-impact, reliable, well-fit automations while penalizing complexity and cost. The verdict is intentionally conservative: systems with meaningful uncertainty tend to land in `MANUAL FIRST`, not `BUILD NOW`.

## Why Human Approval Is Required

AI workflow architecture is risky when it turns uncertain context directly into external action. Every recommended stack must include a human approval mechanism.

That requirement keeps the system grounded:

- Drafts can be useful before they are trusted.
- Structured summaries can support decisions without replacing ownership.
- Automation should remove repeated assembly work, not remove judgment.

## Validation And Repair

Live generation is expected to make occasional mistakes. The engine handles this with a single repair attempt:

1. Ask the model for structured JSON.
2. Validate JSON, schema, catalog tools, counts, and score fields.
3. If invalid, send the validation error and prior response back once.
4. If still invalid, fail clearly.

This is small but important. The engine does not silently accept invalid output, and it does not hide model failure behind a polished UI.

## Evals

The `evals/` folder is not a benchmark suite. It is a compact regression harness that checks whether the examples preserve the project thesis:

- Expected verdict range
- Expected score band
- Required tools
- Required sections
- Score rationales

These evals make the repo more than a static demo. They give future changes a small but concrete way to prove that the decision shape still holds.

## Failure Modes

Stack Engine should downgrade or fail when:

- The proposed stack uses tools outside the catalog.
- A workflow lacks human approval.
- The model returns too few workflows, implementation steps, or prompts.
- A score has no rationale.
- The input suggests high-risk automation with unclear source data.
- The answer is generic advice rather than an executable workflow architecture.

Some of these are enforced in code now. Others are documented design targets for the next iteration.

## What I Would Improve Next

The next strongest improvements would be:

1. Add live-generation evals using recorded model responses.
2. Expand the catalog with tool capabilities, not just names.
3. Add score calibration examples for each verdict.
4. Add a comparison fixture: raw LLM answer vs Stack Engine artifact.
5. Emit machine-readable JSON alongside markdown.

Those would deepen the system without turning it into a platform.

## What This Demonstrates

This project is designed to show:

- System thinking over prompt-only thinking
- Structured generation over freeform chat
- Deterministic judgment over vague recommendation
- Human approval over blind automation
- Small evals over vibes
- Practical architecture over product theater

The intended reviewer reaction is not "this is a huge app." It is:

> This person can take messy real-world work and impose enough structure to make AI useful, inspectable, and executable.
