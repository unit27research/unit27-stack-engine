from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from stack_engine import SAVED_EXAMPLES, render_markdown, saved_example, saved_markdown


class FakeMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class FakeChoice:
    def __init__(self, content: str) -> None:
        self.message = FakeMessage(content)


class FakeResponse:
    def __init__(self, content: str) -> None:
        self.choices = [FakeChoice(content)]


class FakeCompletions:
    def __init__(self, responses: list[str]) -> None:
        self.responses = responses
        self.calls = 0
        self.messages = []

    def create(self, **kwargs):
        self.messages.append(kwargs["messages"])
        content = self.responses[self.calls]
        self.calls += 1
        return FakeResponse(content)


class FakeChat:
    def __init__(self, responses: list[str]) -> None:
        self.completions = FakeCompletions(responses)


class FakeClient:
    def __init__(self, responses: list[str]) -> None:
        self.chat = FakeChat(responses)


class StackEngineTests(unittest.TestCase):
    def test_saved_markdown_is_rendered_from_validated_output(self) -> None:
        output = saved_example("musician")
        self.assertEqual(saved_markdown("musician"), render_markdown(output))
        self.assertIn("## Scorecard", saved_markdown("musician"))

    def test_saved_examples_enforce_required_counts(self) -> None:
        for key in SAVED_EXAMPLES:
            with self.subTest(example=key):
                output = saved_example(key)
                self.assertEqual(len(output.workflows), 3)
                self.assertEqual(len(output.implementation_steps), 6)
                self.assertEqual(len(output.prompts), 3)
                self.assertTrue(output.score_rationales.impact)
                self.assertTrue(output.score_rationales.reliability)
                self.assertTrue(output.score_rationales.fit)
                self.assertTrue(output.score_rationales.complexity)
                self.assertTrue(output.score_rationales.cost)

    def test_catalog_rejects_unknown_tools(self) -> None:
        from stack_engine import prepare_payload

        payload = copy.deepcopy(SAVED_EXAMPLES["musician_growth"])
        payload["stack"]["intelligence"] = ["Imaginary AI Tool"]

        with self.assertRaisesRegex(ValueError, "outside the catalog"):
            prepare_payload(payload)

    def test_openai_generation_repairs_invalid_first_response(self) -> None:
        from stack_engine import generate_with_openai

        invalid_payload = copy.deepcopy(SAVED_EXAMPLES["musician_growth"])
        invalid_payload["stack"]["intelligence"] = ["Imaginary AI Tool"]
        valid_payload = copy.deepcopy(SAVED_EXAMPLES["musician_growth"])
        client = FakeClient([json.dumps(invalid_payload), json.dumps(valid_payload)])

        output = generate_with_openai("messy musician growth problem", client=client)

        self.assertEqual(output.verdict, "BUILD NOW")
        self.assertEqual(client.chat.completions.calls, 2)
        self.assertIn("failed Stack Engine validation", client.chat.completions.messages[1][-1]["content"])


if __name__ == "__main__":
    unittest.main()
