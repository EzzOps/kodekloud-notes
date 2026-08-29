# Demo Breakpoint and Continue

Source: https://notes.kodekloud.com/docs/LangGraph/Human-in-the-Loop-HILT-Architectures/Demo-Breakpoint-and-Continue/page

Demonstrates pausing a workflow for human review then resuming execution with preserved workflow state using interrupt and resume primitives

This lesson demonstrates a common human-in-the-loop interruption pattern for workflows: instead of running end-to-end automatically, a workflow pauses at a breakpoint, waits for a human decision (review/approval), and then continues from the same logical point. The example below simulates this behavior with plain Python to keep it simple and portable. It mirrors how breakpoints and interrupts behave in workflow runtimes while remaining runtime-agnostic.

> **lightbulb** This example demonstrates the pattern and data flow used for breakpoints. In a real deployment the interrupt/continue primitives would be provided by the platform runtime.

## Overview

The demo implements a lightweight pattern that:

1. Generates content.
2. Interrupts execution and returns an interrupt payload for human review.
3. Resumes execution using the reviewer’s decision and updates the workflow state.

Key concepts used:

* Breakpoint / Interrupt: the point where the workflow pauses and returns a payload for review.
* Resume: receiving an external decision and continuing execution from the same logical point.
* Workflow State: an object carrying the data that travels between nodes.

## Setup and types

Begin with the necessary imports and the type that represents the workflow state. This `ReviewState` carries the generated content, the approval decision, and a status flag.

```python theme={null}
