"""Small deterministic eval harness for Stack Engine saved examples."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from stack_engine import model_dump, saved_example


CASES_PATH = Path(__file__).resolve().parent / "eval_cases.json"


def flatten_stack(output: dict) -> set[str]:
    tools: set[str] = set()
    for values in output["stack"].values():
        tools.update(values)
    return tools


def has_required_sections(output: dict, sections: list[str]) -> bool:
    section_map = {
        "diagnosis": bool(output["diagnosis"]),
        "stack": all(output["stack"].values()),
        "workflows": len(output["workflows"]) == 3,
        "implementation": len(output["implementation_steps"]) == 6,
        "score_rationales": all(output["score_rationales"].values()),
        "prompts": len(output["prompts"]) == 3,
    }
    return all(section_map[section] for section in sections)


def evaluate_case(case: dict) -> list[str]:
    output = model_dump(saved_example(case["example"]))
    failures: list[str] = []
    tools = flatten_stack(output)
    score = output["scorecard"]["overall"]

    if output["verdict"] not in case["expected_verdicts"]:
        failures.append(f"verdict {output['verdict']} not in {case['expected_verdicts']}")
    missing_tools = sorted(set(case["required_tools"]) - tools)
    if missing_tools:
        failures.append(f"missing tools: {', '.join(missing_tools)}")
    if not case["expected_score_min"] <= score <= case["expected_score_max"]:
        failures.append(
            f"score {score} outside range {case['expected_score_min']}..{case['expected_score_max']}"
        )
    if not has_required_sections(output, case["required_sections"]):
        failures.append("missing required structured sections")
    return failures


def main() -> int:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    failed = 0
    for case in cases:
        failures = evaluate_case(case)
        if failures:
            failed += 1
            print(f"FAIL {case['id']}: {'; '.join(failures)}")
        else:
            print(f"PASS {case['id']}")
    print(f"\n{len(cases) - failed}/{len(cases)} evals passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
