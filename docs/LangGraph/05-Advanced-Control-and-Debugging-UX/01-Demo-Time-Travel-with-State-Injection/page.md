# Example (pseudocode) showing builder usage
builder = StateGraph(TextState)

builder.add_node("load_data", load_data_node)
builder.add_node("summarize", summarize_node)
builder.add_node("format", format_node)

builder.add_edge("load_data", "summarize")
builder.add_edge("summarize", "format")

builder.set_entry("load_data")
builder.set_exit("format")
```

This yields a clean, testable flow — an excellent starting point for learning how nodes receive and update state.

A concrete real-world example: AI text preprocessing pipeline

* Clean input — remove irrelevant tokens and normalize formatting.
* Summarize — use an LLM chain to condense the cleaned text.
* Rewrite — adjust tone, grammar, or structure.
* Output — save or return the final text.

Each step is an independent transformation and can be tested or replaced without changing the rest of the graph.

<Frame>
  <img alt="The image illustrates an AI text preprocessing pipeline with steps: Clean Input, Summarize, Rewrite, and Output. Each step is explained with concise descriptions." />
</Frame>

Node functions and typed shared state

At the top level, define a typed state model that represents the shared data object flowing through the graph. Each node receives the entire current state and returns a dictionary with the fields it produces. LangGraph merges those results back into the global state.

Example typed state and node functions

```python theme={null}
from typing import TypedDict, NotRequired

class TextState(TypedDict):
    raw_text: str
    cleaned_text: NotRequired[str]
    summary: NotRequired[str]
    final_text: NotRequired[str]

def clean_text(state: TextState) -> dict:
    cleaned = normalize_and_strip(state["raw_text"])
    return {"cleaned_text": cleaned}

def summarize_text(state: TextState) -> dict:
    summary = summarizer.invoke(state["cleaned_text"])
    return {"summary": summary}

def rewrite_text(state: TextState) -> dict:
    final = rewriter.invoke({"text": state["summary"], "tone": "professional"})
    return {"final_text": final}
```

Key points:

* Optional fields start as absent and are produced by downstream nodes.
* Node functions return only the new or updated fields.
* The framework merges partial updates into the global state so subsequent nodes always receive the complete current state.

<Callout icon="lightbulb">
  If you're using Python versions prior to 3.11, import `NotRequired` from `typing_extensions` instead of `typing`.
</Callout>

This full-state-in, partial-state-out pattern keeps nodes decoupled. Nodes never pass values directly to one another; they communicate exclusively through the shared state object. That separation simplifies extensions like validation, external tool calls, and alternative routing without changing node signatures.

Visualizing execution

Running a linear graph yields a straightforward execution trace: input → cleaning → summarization → rewriting → output. Because there are no cycles, intermediate states and logs are easy to inspect. Use LangGraph Studio or standard logging/print statements to trace the state at each node.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Visualizing Execution: Flow from Start to Finish,&#x22; showing a process from user input to a summary, with stages including cleaning and summarizing." />
</Frame>

Benefits for debugging and cost control

Because each step updates state in one direction:

* Debugging is simpler — you can inspect the state after any node.
* Token usage for LLM calls is easier to measure per node.
* Replacing or stubbing nodes for tests is straightforward.

When to use non-cyclical graphs

Non-cyclical graphs are not just for demos — they are production-ready for many deterministic workloads. Use linear graphs when the overall task structure is fixed and predictable.

Examples of good fits:

| Use Case                            | Why it fits                                                             |
| ----------------------------------- | ----------------------------------------------------------------------- |
| PDF data extraction + summarization | Fixed extraction and transform steps                                    |
| Static reporting pipelines          | Deterministic processing stages with clear outputs                      |
| Chatbots with a fixed flow          | Predictable conversational stages (e.g., intent → slot-fill → response) |
| Lightweight ETL tasks               | Sequential extract → transform → load steps                             |

<Frame>
  <img alt="The image explains when to use non-cyclical sequences, highlighting scenarios like PDF data extraction and summarization, static reporting pipelines, and chatbots with known flows. A colorful gear represents these applications." />
</Frame>

Next steps — hands-on lab

Try this exercise to internalize the pattern:

1. Build a small linear graph with 3–4 nodes.
2. Define a typed state model for your pipeline.
3. Implement node functions that return only partial updates.
4. Wire nodes with explicit edges, set entry and exit nodes.
5. Run with a mock state and inspect intermediate state snapshots.

This practical work will cement your understanding of state flow and node chaining.

<Frame>
  <img alt="The image is an infographic titled &#x22;Build Your First Linear Graph,&#x22; showing a four-step process with each step represented by a gear: creating a graph builder, adding nodes, connecting them in order, and testing with mock state." />
</Frame>

Practical tips and best practices

* Reuse existing LLM/chain components (for example, LangChain) instead of reimplementing common logic.
* Keep node functions focused; place LLM chains inside nodes and tools outside when possible.
* Move routing and conditional logic out of core node implementations to retain node simplicity.
* For testing, stub LLM/tool calls and validate partial state outputs at each node.

<Frame>
  <img alt="The image features a silhouette of a head divided into three colored segments, each containing a tech tip: &#x22;Reuse LLM Chains inside nodes,&#x22; &#x22;Use tools to preprocess,&#x22; and &#x22;Keep routing outside the logic.&#x22;" />
</Frame>

Wrap-up

Sequential LangGraphs are an essential foundation: they teach node creation, state design, and wiring. They work well for prototypes, pipelines, and stable production workloads. As systems grow, these linear patterns often remain as subflows inside larger branched or cyclical graphs — so investing time to practice them pays dividends later.

Complete the hands-on exercise to practice building and testing a simple linear graph — it will solidify these fundamental concepts and make later extensions much easier.

Links and references

* [LangChain — official site](https://langchain.com)
* LangGraph concepts: builder, nodes, edges, typed state (search for “LangGraph builder nodes edges” for more examples)
* For typing help: `typing_extensions` documentation (if on Python \<3.11)

<Callout icon="warning">
  When evolving a linear graph into a branching or looping graph, keep node interfaces unchanged where possible — break changes across many nodes make maintenance harder.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langgraph/module/2e37c751-0429-43c9-8ecf-2df222ce0663/lesson/dc7a3746-fc97-46fd-b06e-0a82d5760404" />
</CardGroup>


# Demo Time Travel with State Injection

Source: https://notes.kodekloud.com/docs/LangGraph/Advanced-Control-and-Debugging-UX/Demo-Time-Travel-with-State-Injection/page

Demonstrating workflow checkpointing and state injection to rewind execution, modify checkpoints, and resume for faster debugging, testing, and exploring alternate outcomes

In this lesson we show a practical debugging pattern for LangGraph-style workflows: time travel via state injection. Using simple checkpointing, you can rewind a workflow to an earlier step, modify the saved state, and resume execution from that point. This enables fast experimentation, targeted debugging, and verification of alternate decision paths without re-running the entire pipeline.

Why this is useful

* Debug agent reasoning and decision logic by exploring alternate histories.
* Reproduce and test edge cases by changing specific values at a chosen checkpoint.
* Save time when only a later-stage decision needs to be inspected or changed.

Keywords: time travel, state injection, checkpointing, LangGraph, workflow state, debugging

## Overview

We’ll build a minimal example in Python that demonstrates:

1. Creating and storing checkpoints as deep copies of workflow state.
2. Rewinding to a specific checkpoint.
3. Injecting a modified value into that checkpointed state.
4. Resuming execution from the rewound checkpoint to observe a different outcome.

Code for the demo is organized into discrete blocks so you can run each section independently.

```python theme={null}
