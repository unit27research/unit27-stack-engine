# U27-S02 // Stack Engine

Stack Engine converts ambiguous operational goals into scored AI workflow architectures.

Read [DESIGN_NOTES.md](DESIGN_NOTES.md) for the system philosophy, tradeoffs, failure modes, and eval rationale.

## Why Use It

Use Stack Engine before building an AI workflow when the goal is still fuzzy and the real decision is what to build, what to keep manual, and which stack fits the work.

It is useful when a project idea sounds promising but needs a scored architecture, concrete implementation plan, and decision artifact before code or automation work starts.

Example:

```text
Problem: "We should automate this" is too vague to build from.
Result: Stack Engine returns a scored workflow architecture and a build/manual/later verdict.
```

## What It Does

Stack Engine takes one messy paragraph and returns a decision artifact:

1. Diagnosis
2. Recommended AI stack
3. Three workflows
4. Six-step implementation plan
5. Deterministic scorecard
6. Score rationale
7. Verdict
8. Prompt pack

It is designed to feel like a decision engine, not a chatbot.

## Install

```bash
pip install -r requirements.txt
```

## Demo Commands

```bash
python stack_engine.py --example musician --saved
python stack_engine.py --example musician
streamlit run ui/streamlit_app.py
```

If `OPENAI_API_KEY` is not set, use the `--saved` flag to load a saved demo artifact.
On macOS, use `python3` in place of `python` if your shell does not provide a `python` executable.

Saved examples are stored as canonical structured data in `data/demo_examples.json`, then validated, scored, and rendered into markdown by the same engine path used by generated outputs. Regenerate exported demo files with:

```bash
python stack_engine.py --write-demo-outputs
```

## Examples

```bash
python stack_engine.py --example founder --saved
python stack_engine.py --example sales --saved
python stack_engine.py --example reporting --saved
python stack_engine.py --input "I run a small agency and client follow-up is scattered across email, Slack, and notes."
```

## Scoring

Stack Engine calculates the weighted score deterministically:

```text
impact * 0.35
+ reliability * 0.25
+ fit * 0.25
- complexity * 0.10
- cost * 0.05
```

Verdicts:

- `BUILD NOW`
- `MANUAL FIRST`
- `BUILD LATER`
- `DO NOT BUILD`

## What It Shows

- AI workflow design
- Structured generation
- Schema validation
- Deterministic scoring
- Score rationale and tradeoff explanation
- System thinking
- Validation repair for malformed model output

## Verify

```bash
python -m unittest discover -s tests
python evals/run_evals.py
```

## Reliability

Stack Engine is maintained as part of the Unit27 research toolchain. The local verification contract is the unit test suite plus deterministic eval runner.

## Project Structure

```text
unit27-stack-engine/
├── README.md
├── DESIGN_NOTES.md
├── stack_engine.py
├── schemas.py
├── scoring.py
├── requirements.txt
├── data/
│   ├── demo_examples.json
│   └── tool_catalog.yaml
├── demo_outputs/
│   ├── musician_growth.md
│   ├── solo_founder_ops.md
│   ├── sales_prep.md
│   └── internal_reporting.md
├── evals/
│   ├── eval_cases.json
│   └── run_evals.py
├── tests/
│   └── test_stack_engine.py
└── ui/
    └── streamlit_app.py
```
