"""Streamlit UI for Stack Engine."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from stack_engine import EXAMPLE_INPUTS, generate_with_openai, render_markdown, saved_example


SCENARIOS = {
    "Musician Growth": "musician_growth",
    "Solo Founder Ops": "solo_founder_ops",
    "Sales Prep": "sales_prep",
    "Internal Reporting": "internal_reporting",
}


def render_output(output):
    st.subheader("Diagnosis")
    st.write(output.diagnosis)

    st.subheader("Stack")
    stack = output.stack
    st.write(f"**Intelligence:** {', '.join(stack.intelligence)}")
    st.write(f"**Memory:** {', '.join(stack.memory)}")
    st.write(f"**Orchestration:** {', '.join(stack.orchestration)}")
    st.write(f"**Execution:** {', '.join(stack.execution)}")
    st.write(f"**Human approval:** {', '.join(stack.human_approval)}")

    st.subheader("Workflows")
    for index, workflow in enumerate(output.workflows, start=1):
        with st.expander(f"{index}. {workflow.name}", expanded=True):
            st.write(f"**Trigger:** {workflow.trigger}")
            for step in workflow.steps:
                st.write(f"- {step}")
            st.write(f"**Human check:** {workflow.human_check}")

    st.subheader("Implementation")
    for index, step in enumerate(output.implementation_steps, start=1):
        st.write(f"{index}. {step}")

    st.subheader("Scorecard")
    cols = st.columns(6)
    values = [
        ("Impact", output.scorecard.impact),
        ("Reliability", output.scorecard.reliability),
        ("Fit", output.scorecard.fit),
        ("Complexity", output.scorecard.complexity),
        ("Cost", output.scorecard.cost),
        ("Score", output.scorecard.overall),
    ]
    for col, (label, value) in zip(cols, values):
        col.metric(label, value)

    st.subheader("Score Rationale")
    rationales = output.score_rationales
    st.write(f"**Impact:** {rationales.impact}")
    st.write(f"**Reliability:** {rationales.reliability}")
    st.write(f"**Fit:** {rationales.fit}")
    st.write(f"**Complexity:** {rationales.complexity}")
    st.write(f"**Cost:** {rationales.cost}")

    st.subheader("Verdict")
    st.success(output.verdict)

    st.subheader("Prompts")
    for index, prompt in enumerate(output.prompts, start=1):
        st.write(f"{index}. {prompt}")

    markdown = render_markdown(output)
    st.download_button(
        "Download markdown",
        data=markdown,
        file_name=f"{output.scenario.lower().replace(' ', '_')}_stack_engine.md",
        mime="text/markdown",
    )


st.set_page_config(page_title="U27-S02 Stack Engine", layout="wide")
st.title("U27-S02 // Stack Engine")

scenario_label = st.selectbox("Demo scenario", list(SCENARIOS.keys()))
selected_key = SCENARIOS[scenario_label]
custom_input = st.text_area(
    "Messy paragraph",
    value=EXAMPLE_INPUTS[selected_key],
    height=160,
)

use_saved = st.checkbox(
    "Use saved demo output",
    value=not bool(os.getenv("OPENAI_API_KEY")),
    help="Saved output works without an OpenAI API key.",
)

if st.button("Generate", type="primary"):
    if use_saved:
        output = saved_example(selected_key)
    else:
        if not os.getenv("OPENAI_API_KEY"):
            st.error("OPENAI_API_KEY is not set. Use saved demo output or set an API key.")
            st.stop()
        output = generate_with_openai(custom_input)
    render_output(output)
