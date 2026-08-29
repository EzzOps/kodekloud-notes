# If needed in a fresh environment, uncomment:
import os
from typing import List, Literal
from typing_extensions import TypedDict, NotRequired

from openai import OpenAI
from tavily import TavilyClient
from langgraph.graph import StateGraph, START, END

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5")
TAVILY_MAX_RESULTS = int(os.environ.get("TAVILY_MAX_RESULTS", "3"))

# Ensure API keys are set in the environment (or set them here for testing)
os.environ.setdefault("OPENAI_API_KEY", "your-openai-api-key-here")
os.environ.setdefault("TAVILY_API_KEY", "your-tavily-api-key-here")

openai_client = OpenAI()  # reads OPENAI_API_KEY from env
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
```

<Callout icon="warning">
  Make sure `OPENAI_API_KEY` and `TAVILY_API_KEY` are available in your environment before running the examples. Leaving keys in source code is not recommended for production.
</Callout>

This example uses:

* OpenAI Responses API client for LLM calls.
* Tavily client for web search; the exact method name for searching may vary by SDK version—adapt as needed.

***

## Typed shared state

We define a typed `AgentState` that nodes will read from and write to. LangGraph's nodes interact through this shared state rather than direct node-to-node parameter passing.

```python theme={null}
class AgentState(TypedDict):
    question: str
    intent: NotRequired[Literal["search", "answer"]]
    search_results: NotRequired[list[dict]]  # Tavily results
    draft_answer: NotRequired[str]
    final_answer: NotRequired[str]
```

The state begins with `question` and accumulates `intent`, `search_results`, `draft_answer`, and `final_answer` as the graph runs.

***

## Node overview

We implement four nodes:

| Node              | Purpose                                                                                   | Example output                |
| ----------------- | ----------------------------------------------------------------------------------------- | ----------------------------- |
| `classify_intent` | Decide whether the question needs a web search or can be answered from general knowledge. | `{"intent": "search"}`        |
| `search_web`      | Call Tavily and normalize results into `title`, `url`, `content`.                         | `{"search_results": [{...}]}` |
| `answer_direct`   | Ask the LLM (Responses API) to produce a concise draft answer.                            | `{"draft_answer": "..."}`     |
| `format_output`   | Terminal node: format either the LLM draft or the Tavily results into `final_answer`.     | `{"final_answer": "..."}`     |

Use the table above to quickly see responsibilities and expected state writes.

***

## classify\_intent

This node returns a single label — `"search"` or `"answer"` — which controls conditional routing.

```python theme={null}
def classify_intent(state: AgentState) -> dict:
    """Classify whether the question needs a web search."""
    prompt = (
        "Classify the user question into exactly one label: 'search' or 'answer'.\n"
        "Use 'search' if the question likely requires up-to-date facts, sources, or web lookup.\n"
        "Use 'answer' if general knowledge is enough.\n\n"
        f"Question: {state['question']}\n"
        "Return ONLY the label.\n"
    )

    resp = openai_client.responses.create(
        model=OPENAI_MODEL,
        instructions="You are a strict classifier.",
        input=prompt,
    )

    # Many client wrappers expose text via `output_text`; fall back defensively.
    label = (getattr(resp, "output_text", None) or "").strip().lower()
    label = "search" if "search" in label else "answer"
    return {"intent": label}
```

<Callout icon="lightbulb">
  Use a terse classifier prompt to minimize hallucination and to make the decision deterministic. If you want higher fidelity, consider a small validation step after classification.
</Callout>

***

## search\_web

This node fetches results from Tavily and normalizes them into a simple list of dictionaries with `title`, `url`, and `content`.

```python theme={null}
def search_web(state: AgentState) -> dict:
    """Retrieve web results for the question using Tavily."""
    query = state["question"]

    # Adjust this call to match your tavily-python SDK if necessary.
    # Many clients provide a `.search()` method that returns a list/dict of results.
    resp = tavily_client.search(query, max_results=TAVILY_MAX_RESULTS)

    # Normalize results into a list of dicts with 'title', 'url', 'content'.
    raw_results = getattr(resp, "results", resp) or []
    normalized = []
    for r in raw_results:
        if isinstance(r, dict):
            title = r.get("title", "") or ""
            url = r.get("url", "") or ""
            content = r.get("content", "") or r.get("snippet", "") or ""
        else:
            # Fallback for object-like results
            title = getattr(r, "title", "") or ""
            url = getattr(r, "url", "") or ""
            content = getattr(r, "content", "") or getattr(r, "snippet", "") or ""
        normalized.append({"title": title, "url": url, "content": content})

    return {"search_results": normalized}
```

Notes:

* SDKs differ: if `tavily_client.search` returns a paged object or `resp.results`, adapt the extraction accordingly.
* Keep the normalized output small and consistent to simplify downstream formatting.

***

## answer\_direct

Ask the LLM to answer concisely without performing a web lookup. The draft is stored in `draft_answer`.

```python theme={null}
def answer_direct(state: AgentState) -> dict:
    """Answer directly without web search."""
    resp = openai_client.responses.create(
        model=OPENAI_MODEL,
        instructions="Answer concisely and accurately.",
        input=state["question"],
    )
    answer_text = (getattr(resp, "output_text", None) or "").strip()
    return {"draft_answer": answer_text}
```

***

## format\_output

The final node handles both branches:

* If `intent == "search"`, it formats Tavily results into a readable summary.
* If `intent == "answer"`, it returns the LLM's draft answer.

```python theme={null}
def format_output(state: AgentState) -> dict:
    """Final formatting node.
    - If intent == 'answer': return the LLM draft answer.
    - If intent == 'search': format Tavily results into a readable response.
    """
    intent = state.get("intent", "answer")

    if intent == "search":
        results = state.get("search_results", [])
        if not results:
            return {"final_answer": "I couldn't find relevant sources for this query."}

        lines = ["Here are the top results I found:"]
        for i, r in enumerate(results, start=1):
            title = (r.get("title") or "").strip()
            url = (r.get("url") or "").strip()
            snippet = (r.get("content") or "").strip()

            # Keep it demo-friendly: short list + short snippet
            if title and url:
                lines.append(f"- [{i}] {title} — {url}")
            elif url:
                lines.append(f"- [{i}] {url}")
            else:
                lines.append(f"- [{i}] (no title/url)")

            if snippet:
                short = snippet[:180] + ("... " if len(snippet) > 180 else "")
                lines.append(f"{short}")

        return {"final_answer": "\n".join(lines).strip()}

    # Default: direct answer path
    answer = (state.get("draft_answer") or "").strip()
    if not answer:
        return {"final_answer": "I couldn't generate an answer."}
    return {"final_answer": answer}
```

***

## Wiring the graph

We wire the graph to start at `classify_intent`, branch conditionally to `search_web` or `answer_direct`, and then converge at `format_output` before transitioning to `END`.

```python theme={null}
builder = StateGraph(AgentState)

# Register nodes
builder.add_node("classify_intent", classify_intent)
builder.add_node("search_web", search_web)
builder.add_node("answer_direct", answer_direct)
builder.add_node("format_output", format_output)

# Start -> classify
builder.add_edge(START, "classify_intent")

# Conditional routing: returns either "search" or "answer"
def route_by_intent(state: AgentState):
    return state.get("intent", "answer")

builder.add_conditional_edges(
    "classify_intent",
    route_by_intent,
    path_map={
        "search": "search_web",
        "answer": "answer_direct",
    },
)

# Both branches converge into the same formatter, then end
builder.add_edge("search_web", "format_output")
builder.add_edge("answer_direct", "format_output")
builder.add_edge("format_output", END)

app = builder.compile()
```

<Callout icon="lightbulb">
  Conditional edges let the graph decide the next node dynamically based on the current `state`. This makes branching explicit, easier to reason about, and straightforward to visualize.
</Callout>

***

## Run examples

Run two sample invocations to exercise both routes:

```python theme={null}
# Example 1: general knowledge -> direct answer path
out1 = app.invoke({"question": "Explain conditional edges in LangGraph in one sentence."})
print("Intent:", out1.get("intent"))
print(out1.get("final_answer"))

# Example 2: web-query -> search path
out2 = app.invoke({"question": "What is the latest Tavily Search API update? Provide a short summary."})
print("Intent:", out2.get("intent"))
print(out2.get("final_answer"))
```

Expected behavior:

* The first question should choose `answer`, produce `draft_answer` via the LLM, and return it as `final_answer`.
* The second should choose `search`, fetch results with Tavily, and return a formatted list of top matches.

***

## Visualize the graph

To inspect control flow and conditional edges, export the graph as Mermaid source and render it in any Mermaid-compatible tool (for example, mermaid.live or the VS Code Mermaid preview). Many graph implementations expose a method such as `to_mermaid()` or `get_mermaid()`—check your graph object's API.

Recommended rendering steps:

1. Get the Mermaid source string from your graph object.
2. Paste the Mermaid code into an external renderer (e.g., [https://mermaid.live/](https://mermaid.live/)).
3. Inspect branching points and convergence to verify the routing.

***

## Extending this pattern

This pattern scales well:

* Add more classifier labels and map them to additional tool nodes via `add_conditional_edges`.
* Insert validation or hallucination-checking nodes before the formatter.
* Persist important facts into memory nodes that future queries can read.

References and further reading:

* [OpenAI Responses API](https://platform.openai.com/docs/guides/responses)
* [Mermaid Live Editor](https://mermaid.live/)
* [LangGraph (concepts)](https://example.com/langgraph-docs) &#x20;
* [Tavily (search API)](https://tavily.ai/) &#x20;

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langgraph/module/7a80b285-b366-4c4d-95d0-bce0c24aaf58/lesson/59a2609f-b3cc-4ec4-836c-342af3155b7e" />
</CardGroup>


# Developing Safe Termination Conditions and Loop Limits

Source: https://notes.kodekloud.com/docs/LangGraph/State-Management-and-Iterative-Loops/Developing-Safe-Termination-Conditions-and-Loop-Limits/page

Guidance on designing safe loop termination and limits in LangGraph, combining hard iteration counters with semantic goal checks, graceful exits, observability, and logging for reliable flows.

Why focus on termination conditions?

Termination conditions are the brakes for your LangGraph cycles — the guardrails that prevent loops from running forever, burning compute, confusing users, or breaking downstream flows. They are essential in agentic systems, retry logic, and any iterative reasoning pipeline where you must decide when “good enough” is good enough.

A termination condition is a function or rule that inspects the current graph state at the end of each cycle and decides whether the loop should continue. Typical checks include:

* Did we reach the goal?
* Have we exhausted retries?
* Has the user confirmed or intervened?

When the condition returns true, the loop breaks and the graph transitions to whatever final node you design: a response, a fallback, a handoff, or a cleanup sequence. This gives you fine-grained control over dynamic flows and predictable behavior.

<Frame>
  <img alt="The image highlights the importance of focusing on termination conditions, illustrating that not having them leads to wasted compute, confused users, and broken flows." />
</Frame>

Think of Ravi rechecking his route after every delivery: if there are no more packages or the customer is satisfied, he stops. The most common and reliable termination pattern is counting iterations.

Add a loop count to your graph state and increment it each pass. Once it reaches a predefined max, your router exits the loop. This guarantees an upper bound and prevents infinite execution — a practical safety net when semantic checks fail.

<Frame>
  <img alt="A person standing next to a bicycle is holding a clipboard, with check marks next to listed termination conditions, including &#x22;Did I hit the goal?&#x22;" />
</Frame>

Loop counters: a simple, robust pattern

Store the counter in state, increment on each iteration, and compare to a configured max value.

```python theme={null}
def increment_loop(state: dict) -> dict:
    """
    Increment the loop counter in the state and return the new state.
    """
    return {**state, "loop_count": state.get("loop_count", 0) + 1}

def limit_reached(state: dict) -> bool:
    """
    Return True if the loop_count has reached or exceeded max_loops.
    """
    return state.get("loop_count", 0) >= state.get("max_loops", 3)

def check_termination(state: dict) -> str:
    """
    Router decision: return "exit" if limit reached, otherwise "loop".
    """
    return "exit" if limit_reached(state) else "loop"
```

Goal-oriented termination

Sometimes you want to stop because the task is complete — for example, when a confidence score exceeds a threshold, a summarizer detects no new content, or a parser successfully extracted the needed value. Goal-oriented conditions rely on semantic flags in state (for example, `answer_valid` or `confidence >= 0.9`) and can lead to earlier, more efficient exits.

Goal-based stopping is powerful but needs careful definition of “done.” Because LLM outputs can appear confidently incorrect, always combine semantic checks with a hard limit in production.

<Frame>
  <img alt="The image shows a grid of colored circles labeled &#x22;Graph state&#x22; under the title &#x22;Loop Counters and Max Iterations.&#x22; It is part of a visual explanation related to programming concepts." />
</Frame>

<Frame>
  <img alt="The image illustrates &#x22;Goal-Oriented Termination&#x22; with the text &#x22;Loops stop when a goal is reached&#x22; alongside a target and a wheel graphic." />
</Frame>

Combining conditions

In practice, combine termination checks to balance safety and adaptability. Examples:

* Stop if we hit max loops OR if the answer is good enough.
* Require BOTH success flag and a minimum number of iterations (e.g., run at least 3 rounds then accept success).
* Escalate to a human or fallback after the limit is reached but semantic success is unclear.

<Frame>
  <img alt="The image is a flowchart illustrating a process that involves starting a loop, checking conditions for maximum loops or success, and then deciding to either stop or perform another iteration." />
</Frame>

Even with safeguards, loops can fail to meet their conditions. Include fallback nodes that gracefully exit with a helpful message or alert, and log full state and loop history for debugging.

<Frame>
  <img alt="The image depicts a person sitting with a phone alongside a large screen displaying &#x22;Report Issue.&#x22; It includes tips on handling process failures such as implementing fallback nodes, logging state and history, and preventing infinite loops." />
</Frame>

Ravi doesn't keep driving forever if something blocks him — he reports back to dispatch. Your graph should behave the same way.

<Callout icon="lightbulb">
  Use combined patterns for production: a semantic completion flag for efficiency plus a loop counter for safety. Log which condition triggered the exit so you can analyze and improve flows later.
</Callout>

Observability

Use LangGraph observability to verify loop behavior: track loop count, log conditional evaluations, and inspect state changes before the break. These traces let you tune thresholds, adjust retry strategies, and detect pathological cases early.

<Frame>
  <img alt="The image illustrates a &#x22;LangGraph Trace Timeline&#x22; with a path marked as &#x22;TERMINATED&#x22; alongside a list of observability tools from LangGraph for verifying loop exits, tracking metrics, and analyzing performance." />
</Frame>

Design for graceful exit

A termination should not look like a failure. When the loop ends:

* Transition state to a meaningful final state (generate a response, update memory, or hand off).
* Clean up temporary fields and leave a normalized state for downstream systems.
* Emit structured logs that explain why the graph ended (safety limit vs. semantic success).
* Optionally trigger alerts, retries, or human escalation.

<Frame>
  <img alt="The image illustrates the concept of &#x22;Designing for Graceful Exit,&#x22; featuring a person sitting with a checklist and a list of steps to ensure a clean and functional conclusion, such as generating a final response and updating system memory." />
</Frame>

Standard safety pattern: max iteration limit

Store `loop_count` in the state and increment each iteration. Set `max_loops` in the initial state and route to a graceful exit when reached. LangGraph won’t enforce this for you — design it into your routers and nodes.

Goal-based termination

Use a semantic flag such as `answer_valid` to indicate completion. This mirrors human decision-making: Ravi stops when deliveries are complete, not after a fixed number of turns. Because of model fallibility, pair this with a hard iteration limit.

Combined pattern (goal OR limit)

The safest production pattern combines semantic checks and hard limits. First check the safety condition, then the semantic condition; otherwise, continue looping.

```python theme={null}
def goal_or_limit(state: dict) -> str:
    """
    Router decision combining a hard loop limit with a semantic completion flag.
    Returns "exit" if either safety or goal condition is met, otherwise "loop".
    """
    if state.get("loop_count", 0) >= state.get("max_loops", 3):
        return "exit"
    if state.get("answer_valid", False):
        return "exit"
    return "loop"
```

This combination guarantees safety (no infinite loops) and intelligence (early exit when the objective is achieved).

Advanced options

* Require both conditions for a stricter stop.
* Adjust `max_loops` dynamically based on task complexity.
* Log which condition triggered exit (`"exit_reason": "limit"` or `"exit_reason": "goal"`).
* Escalate to a fallback workflow when limits are reached.

Handle exits explicitly

Even with good termination logic, not every flow will complete successfully. The important part is how you exit and what context you preserve.

```python theme={null}
def handle_exit(state: dict) -> dict:
    """
    Populate an error field when the answer is not valid so downstream
    systems know why the graph terminated.
    """
    if not state.get("answer_valid"):
        state["error"] = "Failed to reach valid answer"
    return state
```

In production, extend this to log structured failure metadata, trigger alerts, offer a retry option, or escalate to a human operator. Proper exit handling turns surprises into controlled outcomes.

<Frame>
  <img alt="The image is titled &#x22;Observing Termination in Action&#x22; and features three points on observing termination: tracing logic via observability, visualizing loop flow and breakpoints, and using it to improve flow design." />
</Frame>

Cleanup and finalization

Stopping a loop is not the same as finishing cleanly. Remove temporary keys, add a terminal marker, and return a normalized state for downstream systems and observability.

```python theme={null}
def cleanup_and_finish(state: dict) -> dict:
    """
    Clean up transient fields and mark the state as complete.
    """
    state.pop("temporary_data", None)
    state.pop("debug_info", None)
    state["status"] = "complete"
    return state
```

A graceful exit node can also persist results, trigger analytics, send webhooks, or escalate unresolved failures. It’s the final checkpoint where the loop lands safely.

Key patterns at a glance

| Pattern                          | When to use                                     | Example / Notes                                   |
| -------------------------------- | ----------------------------------------------- | ------------------------------------------------- |
| Loop counter (hard limit)        | Always include for safety                       | `loop_count` + `max_loops`                        |
| Goal-oriented (semantic)         | When you can define a reliable `done` condition | `answer_valid`, `confidence >= 0.9`               |
| Combined (goal OR limit)         | Production-ready: balanced and safe             | Check safety first, then semantic flag            |
| Strict (goal AND min iterations) | When you need verification before exit          | Require both `answer_valid` and `loop_count >= 3` |

<Frame>
  <img alt="The image displays two takeaways regarding loops: ensuring termination for safety and usefulness, and using counters, goals, and guards." />
</Frame>

<Callout icon="warning">
  Never rely solely on semantic confidence for termination in production. Always include a hard iteration limit and structured logging so you can understand why a flow ended.
</Callout>

Key takeaways

* Intelligent loops require thoughtful termination logic — counters, semantic flags, and guards.
* Combine safety (hard limits) and intelligence (goal checks) to get the best of both worlds.
* Design graceful exits that preserve context, emit observability data, and support downstream handling.
* Log exit reasons and loop history to iterate on thresholds and improve reliability.

Links and references

* [LangGraph observability and traces](https://www.langgraph.com/docs) (example reference)
* [Termination problem — background theory](https://en.wikipedia.org/wiki/Termination_problem)
* Best practices for retry and backoff strategies (search for "retry patterns" in your internal docs)

Implement these patterns in your routers and state management to keep LangGraph flows responsive, predictable, and safe.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langgraph/module/7a80b285-b366-4c4d-95d0-bce0c24aaf58/lesson/b125b0f3-0de9-467e-a15d-d41957c4cb81" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/langgraph/module/7a80b285-b366-4c4d-95d0-bce0c24aaf58/lesson/2e2dc1e6-ba1c-4dba-8390-ad105ce7cedd" />
</CardGroup>
