# If needed in a fresh environment, uncomment:
# !pip -q install --upgrade openai langgraph tavily-python
```

Setup and imports. We create separate clients to avoid name collisions and read model/limit config from environment variables.

```python theme={null}
import os
from typing import List, Literal
from typing_extensions import TypedDict, NotRequired

from openai import OpenAI
from tavily import TavilyClient
from langgraph.graph import StateGraph, START, END

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5")
TAVILY_MAX_RESULTS = int(os.environ.get("TAVILY_MAX_RESULTS", "3"))

# Set your API keys here if not in environment (for local testing only)
os.environ.setdefault("OPENAI_API_KEY", "your-openai-api-key-here")
os.environ.setdefault("TAVILY_API_KEY", "your-tavily-api-key-here")

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
```

Typed shared state
The graph always starts with a `question`. Nodes may add other optional fields as they execute.

```python theme={null}
class AgentState(TypedDict):
    question: str
    intent: NotRequired[Literal["search", "answer"]]
    search_results: NotRequired[List[dict]]  # Tavily results
    draft_answer: NotRequired[str]
    final_answer: NotRequired[str]
```

Node implementations
Below are the four node functions used in the graph. Each returns a dictionary of fields to merge into the shared state.

1. classify\_intent — decide whether the question requires a web search or can be answered directly. It returns `{"intent": "search"}` or `{"intent": "answer"}`.

```python theme={null}
def classify_intent(state: AgentState) -> dict:
    """Classify whether the question needs web search."""
    prompt = (
        "Classify the user question into exactly one label: 'search' or 'answer'.\n"
        "Use 'search' if the question likely requires up-to-date facts, sources, or web lookup.\n"
        "Use 'answer' if general knowledge is enough.\n\n"
        f"Question: {state['question']}\n"
        "Return ONLY the label."
    )
    resp = openai_client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    # Robustly extract textual output from the Responses object
    label = (getattr(resp, "output_text", "") or "").strip().lower()
    # Defensive normalization
    label = "search" if "search" in label else "answer"
    return {"intent": label}
```

2. search\_web — call the Tavily client to retrieve search results for the question and return them under `search_results`.

```python theme={null}
def search_web(state: AgentState) -> dict:
    """Run a web search using Tavily and return top results."""
    query = state["question"]
    # Assume tavily_client.search returns a list of dicts with keys: title, url, content
    results = tavily_client.search(query=query, max_results=TAVILY_MAX_RESULTS)
    # Defensive: ensure list format
    results = results or []
    return {"search_results": results}
```

3. answer\_direct — call the OpenAI Responses API to produce a direct draft answer (no web lookup).

```python theme={null}
def answer_direct(state: AgentState) -> dict:
    """Answer directly without web search."""
    resp = openai_client.responses.create(
        model=OPENAI_MODEL,
        input=state["question"],
    )
    draft = (getattr(resp, "output_text", "") or "").strip()
    return {"draft_answer": draft}
```

4. format\_output — shared terminal node that formats the output based on the `intent`. If `intent == "search"`, it summarizes Tavily results; otherwise it returns the LLM draft.

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
                short = snippet[:180] + ("..." if len(snippet) > 180 else "")
                lines.append(f"{short}")

        return {"final_answer": "\n".join(lines).strip()}

    # Default: direct answer path
    answer = (state.get("draft_answer") or "").strip()
    return {"final_answer": answer or "No answer generated."}
```

Node summary

| Node name         | Purpose                                                    | Returns                                          |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------------ |
| `classify_intent` | Decide whether to perform a web search or answer directly  | `{"intent": "search"}` or `{"intent": "answer"}` |
| `search_web`      | Query Tavily and return top results                        | `{"search_results": [...]}`                      |
| `answer_direct`   | Ask OpenAI for a direct draft answer                       | `{"draft_answer": "..."}`                        |
| `format_output`   | Final formatting; merges search or draft into final answer | `{"final_answer": "..."}`                        |

Wiring the StateGraph

* Start at `classify_intent`.
* Add a conditional edge from `classify_intent` that routes to either `search_web` or `answer_direct`.
* Both of those nodes then converge into `format_output`, which is the terminal node.

```python theme={null}
builder = StateGraph(AgentState)

builder.add_node("classify_intent", classify_intent)
builder.add_node("search_web", search_web)
builder.add_node("answer_direct", answer_direct)
builder.add_node("format_output", format_output)

# Graph entry
builder.add_edge(START, "classify_intent")

def route_by_intent(state: AgentState):
    return state.get("intent", "answer")

# Conditional routing based on the intent field
builder.add_conditional_edges(
    "classify_intent",
    route_by_intent,
    path_map={
        "search": "search_web",
        "answer": "answer_direct",
    },
)

# Converge both paths into the final formatter and then to END
builder.add_edge("search_web", "format_output")
builder.add_edge("answer_direct", "format_output")
builder.add_edge("format_output", END)

# Build the executable app
app = builder.build()
```

Run the graph with two example questions to observe the routing behavior.

```python theme={null}
out1 = app.invoke({"question": "Explain conditional edges in LangGraph in one sentence."})
print("Intent:", out1.get("intent"))
print(out1.get("final_answer"))

out2 = app.invoke({"question": "What is the latest Tavily Search API update? Provide a short summary."})
print("Intent:", out2.get("intent"))
print(out2.get("final_answer"))
```

Inspecting the graph visualization
If you want to inspect the control flow produced by the graph without rendering an image, you can print the Mermaid source for the diagram and paste it into any Mermaid renderer or editor.

```python theme={null}
# Print the Mermaid diagram source so it can be reviewed or pasted into a renderer
mermaid_source = app.get_graph().draw_mermaid()
print(mermaid_source)
```

Conclusion
This pattern scales naturally to more complex agentic systems. You can add more routes, tool calls, validation steps, or memory writes while keeping the same state-driven routing model. Conditional edges keep control flow explicit and make branching logic easy to reason about during orchestration.

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/2e37c751-0429-43c9-8ecf-2df222ce0663/lesson/e59ee1a7-b8ca-447f-aa47-1ada8a61726d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/langgraph/module/2e37c751-0429-43c9-8ecf-2df222ce0663/lesson/f2a854da-14d2-4b37-9457-bfaa786c3d20)


# Practical Application Building a Basic Conversational Agent

Source: https://notes.kodekloud.com/docs/LangGraph/The-Core-Workflow-Nodes-Edges-and-Routing/Practical-Application-Building-a-Basic-Conversational-Agent/page

Guide to designing a minimal modular conversational agent in LangGraph using intent classification, conditional routing, optional retrieval, LLM generation, and centralized response formatting.

This lesson assumes familiarity with nodes, edges, and conditional routing — the core mechanics of LangGraph. We'll translate those fundamentals into a concrete, minimal conversational agent design and walk through a demo implementation in LangGraph.

A conversational agent is an ideal example because it is:

* Easy to visualize,
* Highly modular, and
* A practical, real-world use case you can adapt for your organization.

<Frame>
  <img alt="The image is a slide titled &#x22;Why Build a Conversational Agent Now?&#x22; with three points: &#x22;Easy to visualize,&#x22; &#x22;Highly modular,&#x22; and &#x22;Practical real-world use case.&#x22;" />
</Frame>

## High-level objective

* Build a chatbot that:
  * Understands user intent,
  * Decides whether to answer directly or perform a document search, and
  * Returns a formatted response.
* Adhere to LangGraph principles: modular nodes, explicit state, and declarative routing.

## High-level flow

1. Receive user input — an entry node persists the user's message into the graph state.
2. Classify intent — a lightweight LLM or classifier marks whether the user expects a direct answer or a search.
3. Conditional routing — route to search or answer branches based on intent.
4. External search (optional) — perform retrieval when external knowledge is required.
5. Answer generation — use an LLM to produce the response (with or without retrieved context).
6. Merge and respond — format a final response in a shared node so output formatting or streaming can be centralized.

This flow remains intentionally simple and mostly acyclic. It emphasizes routing, node design, and state transitions so you can observe, test, and extend behavior with minimal friction.

## About the entry node and state

* The entry node's responsibility is to persist the raw user message into graph state (for example: `state.user_message`).
* Every subsequent node reads from and writes to `state`; this keeps each node small, composable, and independently testable.

> **lightbulb** Design the entry node to only persist input (avoid embedding logic here). Separating intent classification, retrieval, and generation makes each piece replaceable and easier to maintain or extend.

## Routing and branching

* After intent classification, treat the graph like a decision tree: if `intent == "search"`, route to the retrieval branch; if `intent == "answer"`, route to the direct answer branch.
* Converge both branches into a common response node. Centralizing response formatting makes it trivial to add streaming, templating, or channel-specific outputs without changing upstream logic.
* Because nodes are independent and routing is declarative, you can swap or instrument nodes without refactoring unrelated components.

## Extensibility and observability

* Replace the intent classifier with a fine-tuned model when higher accuracy is required.
* Add a fallback node to handle empty search results or low-confidence classifications.
* Swap the final response generator for a streaming responder to enable real-time outputs.
* Use LangGraph observability tools (logs, metrics, traces) to debug node behavior and routing decisions.

This diagram illustrates a modular design that cleanly separates classification, search, generation, and response formatting. It highlights how feedback, clarification, and retry mechanisms can be added as separate nodes without changing the core structure.

<Frame>
  <img alt="The image depicts a flowchart illustrating a modular design process for handling input and generating responses, highlighting components like classification, feedback, and retry mechanisms. It emphasizes the design's extendability with points such as node independence, declarative routing, and zero refactoring needed for updates." />
</Frame>

## Quick reference: Node responsibilities and example state

| Component          | Responsibility                                           | Example state key(s)       |
| ------------------ | -------------------------------------------------------- | -------------------------- |
| Entry node         | Persist raw user input                                   | `state.user_message`       |
| Intent classifier  | Classify intent (search vs answer)                       | `state.intent`             |
| Retriever          | Fetch relevant documents or passages                     | `state.search_results`     |
| Generator          | Produce final answer using LLM (with or without context) | `state.answer`             |
| Response formatter | Merge pieces and format final output                     | `state.formatted_response` |

## Minimal node pseudocode

Below is an illustrative pseudocode sketch of node behaviors and state transitions:

```javascript theme={null}
// Entry node
function entryNode(input, state) {
  state.user_message = input;
  return state;
}

// Intent classifier
function classifyIntent(state) {
  // simple LLM/classifier call returns "search" or "answer"
  state.intent = callClassifier(state.user_message);
  return state;
}

// Conditional routing handled by LangGraph's declarative edges
// Retrieval node (runs only if state.intent === "search")
function retrieve(state) {
  state.search_results = callRetriever(state.user_message);
  return state;
}

// Generator (uses search_results if present)
function generateAnswer(state) {
  const context = state.search_results || null;
  state.answer = callLLM(state.user_message, context);
  return state;
}

// Final formatter
function respond(state) {
  state.formatted_response = formatTemplate(state.answer, state.search_results);
  return state.formatted_response;
}
```

## Recap

* Nodes are chainable functions: LLM calls, retrievers, classifiers, and formatters.
* State captures user input and intermediate results, enabling small, testable nodes.
* Conditional routing makes flow explicit and predictable.
* The pattern is readable, testable, reusable, and ready to extend with cycles, memory, or streaming.

This minimal but powerful conversational agent pattern is a solid foundation. From here, add memory, clarification loops, or streaming outputs as your product requirements evolve.

## Links and references

* [LangGraph documentation](https://langgraph.example/docs)
* [Retrieval-Augmented Generation patterns](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
* [Best practices for prompt design and LLM safety](https://platform.openai.com/docs/guides/prompting)

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/2e37c751-0429-43c9-8ecf-2df222ce0663/lesson/a87d8e60-a7cd-4290-9a07-9fbe3ce00d05)
