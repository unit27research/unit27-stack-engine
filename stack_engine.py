"""CLI engine for U27-S02 Stack Engine."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from schemas import StackEngineOutput
from scoring import score_payload


ROOT = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "data" / "tool_catalog.yaml"
DEMO_DIR = ROOT / "demo_outputs"
CATEGORY_LABELS = {
    "intelligence": "Intelligence",
    "memory": "Memory",
    "orchestration": "Orchestration",
    "execution": "Execution",
    "human_approval": "Human Approval",
}

EXAMPLE_ALIASES = {
    "musician": "musician_growth",
    "musician_growth": "musician_growth",
    "founder": "solo_founder_ops",
    "solo_founder": "solo_founder_ops",
    "solo_founder_ops": "solo_founder_ops",
    "sales": "sales_prep",
    "sales_prep": "sales_prep",
    "reporting": "internal_reporting",
    "internal_reporting": "internal_reporting",
}

DEFAULT_CATALOG = {
    "intelligence": ["ChatGPT", "Claude", "Gemini"],
    "memory": ["Notion", "Airtable", "Google Drive", "Obsidian"],
    "orchestration": ["Zapier", "Make", "n8n"],
    "execution": ["Gmail", "Slack", "Buffer", "Metricool", "Google Calendar", "HubSpot"],
    "human_approval": ["Notion approval field", "Gmail draft review", "Slack approval message"],
}

DEMO_EXAMPLES_PATH = ROOT / "data" / "demo_examples.json"


def load_demo_examples() -> dict[str, dict[str, Any]]:
    with DEMO_EXAMPLES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


SAVED_EXAMPLES = load_demo_examples()
EXAMPLE_INPUTS = {key: value["input_summary"] for key, value in SAVED_EXAMPLES.items()}


def model_validate(payload: dict[str, Any]) -> StackEngineOutput:
    if hasattr(StackEngineOutput, "model_validate"):
        return StackEngineOutput.model_validate(payload)
    return StackEngineOutput.parse_obj(payload)


def model_dump(model: StackEngineOutput) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def load_catalog() -> dict[str, list[str]]:
    try:
        import yaml
    except ModuleNotFoundError:
        return DEFAULT_CATALOG
    with CATALOG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def validate_stack_against_catalog(stack: dict[str, list[str]], catalog: dict[str, list[str]]) -> None:
    """Reject recommendations that use tools outside the catalog."""
    unknown: list[str] = []
    for category, tools in stack.items():
        allowed = set(catalog.get(category, []))
        for tool in tools:
            if tool not in allowed:
                unknown.append(f"{category}: {tool}")
    if unknown:
        formatted = ", ".join(unknown)
        raise ValueError(f"Recommended stack includes tools outside the catalog: {formatted}")


def example_key(value: str) -> str:
    key = value.strip().lower().replace("-", "_")
    if key not in EXAMPLE_ALIASES:
        choices = ", ".join(sorted(EXAMPLE_ALIASES))
        raise SystemExit(f"Unknown example '{value}'. Choose one of: {choices}")
    return EXAMPLE_ALIASES[key]


def prepare_payload(payload: dict[str, Any]) -> StackEngineOutput:
    scored = dict(payload)
    scored["scorecard"] = score_payload(scored["scorecard"])
    scored["verdict"] = scored["scorecard"]["verdict"]
    validate_stack_against_catalog(scored["stack"], load_catalog())
    return model_validate(scored)


def saved_example(name: str) -> StackEngineOutput:
    return prepare_payload(SAVED_EXAMPLES[example_key(name)])


def saved_markdown(name: str) -> str:
    return render_markdown(saved_example(name))


def write_demo_outputs() -> None:
    DEMO_DIR.mkdir(exist_ok=True)
    for key in sorted(SAVED_EXAMPLES):
        path = DEMO_DIR / f"{key}.md"
        path.write_text(render_markdown(saved_example(key)), encoding="utf-8")


def build_prompt(user_input: str, catalog: dict[str, list[str]]) -> str:
    return f"""
You are Stack Engine, a deterministic AI workflow architecture engine.

Convert the user's messy operational goal into a structured AI stack recommendation.
This is not a chatbot answer. Return a decision artifact.

Available tool catalog:
{json.dumps(catalog, indent=2)}

Rules:
- Return only valid JSON.
- Use exactly 3 workflows.
- Use exactly 6 implementation_steps.
- Use exactly 3 prompts.
- scorecard values must be integers from 1 to 5.
- score_rationales must explain every scorecard dimension in concrete terms.
- Do not include overall score or verdict. They are calculated deterministically.
- Every stack tool must come from the available tool catalog.
- Every stack category must include at least one tool.
- Prefer simple, auditable workflows with human approval.

JSON shape:
{{
  "scenario": "Short scenario name",
  "input_summary": "One sentence summary of the user input",
  "diagnosis": "Decision-engine diagnosis",
  "stack": {{
    "intelligence": [],
    "memory": [],
    "orchestration": [],
    "execution": [],
    "human_approval": []
  }},
  "workflows": [
    {{"name": "", "trigger": "", "steps": [], "human_check": ""}}
  ],
  "implementation_steps": [],
  "scorecard": {{"impact": 1, "reliability": 1, "fit": 1, "complexity": 1, "cost": 1}},
  "score_rationales": {{"impact": "", "reliability": "", "fit": "", "complexity": "", "cost": ""}},
  "verdict": "",
  "prompts": []
}}

User input:
{user_input}
""".strip()


def repair_prompt(error: Exception, invalid_content: str) -> str:
    return f"""
The previous response failed Stack Engine validation.

Validation error:
{error}

Previous response:
{invalid_content}

Return corrected JSON only. Keep the same schema, use exactly 3 workflows,
exactly 6 implementation_steps, exactly 3 prompts, integer scorecard values
from 1 to 5, and only tools from the catalog.
""".strip()


def generate_with_openai(user_input: str, client: Any | None = None) -> StackEngineOutput:
    if client is None:
        from openai import OpenAI

        client = OpenAI()
    model = os.getenv("STACK_ENGINE_MODEL", "gpt-4o-mini")
    messages = [
        {"role": "system", "content": "You return valid JSON for a structured AI workflow architecture engine."},
        {"role": "user", "content": build_prompt(user_input, load_catalog())},
    ]
    last_error: Exception | None = None
    for attempt in range(2):
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=messages,
            temperature=0.2,
        )
        content = response.choices[0].message.content or "{}"
        try:
            return prepare_payload(json.loads(content))
        except (json.JSONDecodeError, ValueError) as error:
            last_error = error
            if attempt == 1:
                break
            messages.extend(
                [
                    {"role": "assistant", "content": content},
                    {"role": "user", "content": repair_prompt(error, content)},
                ]
            )
    raise RuntimeError(f"OpenAI response failed Stack Engine validation after repair: {last_error}")


def render_markdown(output: StackEngineOutput) -> str:
    data = model_dump(output)
    scorecard = data["scorecard"]
    score_rationales = data["score_rationales"]
    stack = data["stack"]
    lines = [
        f"# {data['scenario']} // Stack Engine Output",
        "",
        "## Input",
        data["input_summary"],
        "",
        "## Diagnosis",
        data["diagnosis"],
        "",
        "## Recommended Stack",
    ]
    for category, label in CATEGORY_LABELS.items():
        lines.append(f"- **{label}:** {', '.join(stack[category])}")
    lines.extend(["", "## Workflows"])
    for index, workflow in enumerate(data["workflows"], start=1):
        workflow_steps = "; ".join(step.rstrip(".") for step in workflow["steps"])
        lines.extend(
            [
                f"### {index}. {workflow['name']}",
                f"- **Trigger:** {workflow['trigger']}",
                f"- **Steps:** {workflow_steps}.",
                f"- **Human Check:** {workflow['human_check']}",
                "",
            ]
        )
    lines.extend(["## Implementation Plan"])
    for index, step in enumerate(data["implementation_steps"], start=1):
        lines.append(f"{index}. {step}")
    lines.extend(
        [
            "",
            "## Scorecard",
            f"- **Impact:** {scorecard['impact']}/5",
            f"- **Reliability:** {scorecard['reliability']}/5",
            f"- **Fit:** {scorecard['fit']}/5",
            f"- **Complexity:** {scorecard['complexity']}/5",
            f"- **Cost:** {scorecard['cost']}/5",
            f"- **Weighted Score:** {scorecard['overall']}",
            "",
            "## Score Rationale",
            f"- **Impact:** {score_rationales['impact']}",
            f"- **Reliability:** {score_rationales['reliability']}",
            f"- **Fit:** {score_rationales['fit']}",
            f"- **Complexity:** {score_rationales['complexity']}",
            f"- **Cost:** {score_rationales['cost']}",
            "",
            "## Verdict",
            data["verdict"],
            "",
            "## Prompt Pack",
        ]
    )
    for index, prompt in enumerate(data["prompts"], start=1):
        lines.append(f"{index}. {prompt}")
    lines.append("")
    return "\n".join(lines)


def resolve_input(args: argparse.Namespace) -> tuple[str, str | None]:
    if args.input:
        return args.input, None
    if args.example:
        key = example_key(args.example)
        return EXAMPLE_INPUTS[key], key
    raise SystemExit("Provide --example musician or --input \"custom text\".")


def run(args: argparse.Namespace) -> str:
    if args.write_demo_outputs:
        write_demo_outputs()
        return f"Wrote {len(SAVED_EXAMPLES)} demo outputs to {DEMO_DIR}"
    user_input, example = resolve_input(args)
    if args.saved:
        if not example:
            raise SystemExit("--saved requires --example.")
        return saved_markdown(example)
    if not os.getenv("OPENAI_API_KEY"):
        if example:
            return saved_markdown(example)
        raise SystemExit("OPENAI_API_KEY is not set. Use --example musician --saved or set an API key.")
    return render_markdown(generate_with_openai(user_input))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stack Engine decision artifact generator.")
    parser.add_argument("--example", help="Demo example: musician, founder, sales, reporting")
    parser.add_argument("--input", help="Custom messy operational goal")
    parser.add_argument("--saved", action="store_true", help="Load saved markdown demo output")
    parser.add_argument(
        "--write-demo-outputs",
        action="store_true",
        help="Regenerate demo_outputs/*.md from canonical structured examples",
    )
    return parser.parse_args()


if __name__ == "__main__":
    print(run(parse_args()))
