# Example model interface; replace with your model client
class Model:
    def invoke(self, messages: List[SystemMessage]):
        # returns an object with `.content`
        ...

model = Model()

def summarize_node(state: ChatState, keep_last_k: int = 0) -> ChatState:
    """
    Compress current state['messages'] into a summary, optionally keep last_k recent messages.
    """
    if not state.get("messages"):
        return state  # nothing to summarize

    prompt = [
        SystemMessage(content="You are a summarizer. Summarize the following conversation concisely, preserving facts and decisions:"),
        *state["messages"]
    ]

    result = model.invoke(prompt)

    # Merge new summary with any existing summary to preserve history
    combined_summary = (state.get("summary") or "") + "\n\n" + result.content if state.get("summary") else result.content

    # Optionally retain the last K messages to preserve immediate continuity
    kept_messages = state["messages"][-keep_last_k:] if keep_last_k > 0 else []

    return {
        "summary": combined_summary,
        "messages": kept_messages,
        "turn_count": 0  # reset the turn counter after compression
    }
```

Key points:

* The system instruction defines the summarization objective (preserve facts/decisions).
* Save the model’s output to `state["summary"]`.
* Trim `state["messages"]` (or keep the last N messages) to avoid unbounded token growth.
* Reset or adjust `turn_count` after compression.

This transforms memory by extracting meaning, not merely trimming tokens.

## Injecting compressed memory back into prompts

When generating replies, include the `summary` as part of the system-level context and then append the recent `messages`. This hybrid prompt keeps long-term facts available while maintaining immediacy.

```python theme={null}
from langchain_core.messages import SystemMessage

def build_prompt(state: ChatState):
    system_msg = SystemMessage(
        content=f"Conversation summary so far:\n{state.get('summary','')}"
    )
    return [system_msg] + state.get("messages", [])
```

Extend this to add role instructions, user metadata, domain constraints, or tone controls as needed.

## Counters: a control lever for routing and summarization

A simple integer in state can drive a lot of behavior. Use `turn_count` to:

* Trigger summarization after N turns.
* Limit retries or loop iterations.
* Influence router/evaluator branching.

Example helper functions:

```json theme={null}
{"turn_count": 0}
```

```python theme={null}
def increment_turn(state: dict) -> dict:
    state["turn_count"] = state.get("turn_count", 0) + 1
    return state

def should_summarize(state: dict, threshold: int = 4) -> bool:
    return state.get("turn_count", 0) >= threshold
```

Best practices:

* Initialize the counter when a conversation starts.
* Increment after each user+assistant exchange.
* Use `should_summarize` in routing logic to decide when to call the summarization node.
* Reset or archive the counter as part of the summary operation.

<Frame>
  <img alt="The image describes the Counter Pattern in LangGraph, highlighting tracking iterations with fields like turn_count, storing counters in state for node access, and using them in routers or evaluators to trigger actions like summarization or retries." />
</Frame>

## When to summarize

Summarization has a cost. Choose triggers that balance currency and efficiency.

Two common strategies:

* Time-based: after a fixed number of turns (e.g., 4–6).
* Event-based: when a significant event occurs (topic shift, long message, new decision, etc.).

Comparison table

| Strategy    | Trigger example                       | Pros                      | Cons                          |
| ----------- | ------------------------------------- | ------------------------- | ----------------------------- |
| Time-based  | Every N turns (`turn_count >= 4`)     | Simple, predictable       | Might summarize mid-topic     |
| Event-based | Topic change or long message detected | Preserves topic coherence | Requires detection heuristics |

Typical pattern:

1. Increment `turn_count` after each exchange.
2. If `should_summarize` is true, route to the summarization node.
3. Persist the updated summary, reset the counter, and continue.

This hybrid approach (summary + recent messages) keeps continuity while remaining within token limits.

## Conversation flow

After several exchanges, trigger summarization. Older messages are compressed into `summary`; recent messages are kept in `messages`. The next LLM prompt uses this cleaned-up state, so the model sees a compact, focused context instead of the entire conversation history.

<Frame>
  <img alt="The image illustrates an example conversation flow, starting from the user interacting with a system that asks three questions, followed by summarization, processing by a language model (LLM), and concluding with a bot reply." />
</Frame>

## Production considerations and extensions

* Keep the last 1–3 messages verbatim for conversational continuity when appropriate.
* Persist summaries in an external store (document DB, vector DB) for retrieval and audit trails.
* Generate structured summaries (bullet points, actions, deadlines, named entities) to make downstream reasoning easier.
* Combine time-based and event-based triggers for robust behavior.
* Tune the summarization prompt to preserve facts, decisions, and action items.
* Use observability tools (LangGraph Studio / [LangSmith](https://learn.kodekloud.com/user/courses/langsmith)) to inspect state evolution and verify critical facts are retained.

<Callout icon="lightbulb">
  Always test by printing or inspecting the state after each node to ensure summaries preserve key facts and that retained recent messages provide the necessary context for correct responses.
</Callout>

## Why this pattern matters

Treat summarization as a first-class architectural component. By modeling memory explicitly in the graph state and using counter-driven routing, you can move from a simple prompt-based bot to a structured, long-running conversational system that scales gracefully and maintains high-quality responses.

<Frame>
  <img alt="The image lists four takeaways focused on smart state management, performance in long conversations, lightweight graph design, and improving model accuracy and user engagement." />
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-b58a-4c3e-9e5e-851e67d45b06/lesson/e69446b9-3d1f-444b-bb90-d153546aa669" />
</CardGroup>


# Strategies for Context Overflow

Source: https://notes.kodekloud.com/docs/LangGraph/Context-Management-and-Short-Term-Memory/Strategies-for-Context-Overflow/page

Techniques to manage LLM context overflow by prioritizing recent turns, summarizing history, filtering roles, chunking, and using memory snapshots to preserve crucial information and prevent degraded responses

Context overflow occurs when the combined size of your prompt and chat history exceeds a model’s token window. Common model windows are 8K, 16K, or 100K tokens, but every model has a finite context length. When the input exceeds that window, earlier parts of the conversation are typically truncated, which can lead to degraded responses, broken references, or hallucinations. Models and APIs rarely warn you; many implementations drop tokens from the start or middle until the input fits, so crucial system instructions or user preferences can vanish silently unless you design for it.

<Frame>
  <img alt="The image titled &#x22;Understanding Context Overflow&#x22; shows an illustration of a person holding blocks and a smartphone with gears, alongside icons for Apple, Android, and Windows." />
</Frame>

Understanding where a model drifts and what context matters most is the first step to preventing failures. A useful mental model is a delivery cart: if you cram too many packages, some will fall off the back. In chat flows the oldest messages are the most likely to be dropped while the newest remain.

Below are practical, tested strategies you can apply singly or in combination depending on the application type (chatbot, document agent, long-form assistant, multi-turn planner, etc.).

## Strategy summaries

| Strategy                                        | When to use                                                                 | Benefit                                                         |
| ----------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Prioritize recent turns (truncate from the top) | Transactional flows — summarization, single-question answering, short chats | Keeps prompt focused on the most relevant messages              |
| Summarize or compress older exchanges           | Long-running sessions where user preferences and state matter               | Retains essential info while saving tokens                      |
| Role-based filtering                            | Agent systems with tool outputs, logs, or verbose system messages           | Removes noisy, low-value messages first                         |
| Chunking with recency bias                      | Multi-topic or multi-step workflows                                         | Preserves coherent chunks of context instead of scattered turns |
| Memory snapshots + external storage             | Sessions with logical milestones or persistent memory needs                 | Enables retrieval of relevant history without pulling full logs |
| Combine techniques                              | All complex applications                                                    | Balances freshness, relevance, and token budgets                |

## 1) Prioritize recent turns (truncate from the top)

Many conversations are driven by the most recent user and assistant exchanges. For transactional tasks — summarization, translation, or answering a single question — trimming older turns from the start of the history often preserves the necessary context and keeps the prompt focused.

* When to use: short sessions or tasks where the latest messages determine intent.
* Trade-offs: simple and effective, but may discard important earlier setup or constraints.

<Frame>
  <img alt="The image shows a mobile phone displaying a chat interface, accompanied by a strategy for prioritizing recent turns by truncating older history to focus on the current goal, with tasks like summarizing, translating, and responding to a prompt." />
</Frame>

<Callout icon="warning">
  When truncating, never discard persistent system instructions, user preferences, or critical configuration the assistant relies on. Losing these can break correctness even if recent turns remain intact.
</Callout>

## 2) Summarize or compress older exchanges

Instead of preserving every earlier message verbatim, collapse groups of past messages into a concise summary, e.g., “User asked for trip advice; prefers warm climates; avoids crowds.” This preserves the essentials while saving tokens.

* How to produce summaries:
  * Use another LLM node to create a compact summary.
  * Implement reducer functions with deterministic rules.
  * Store structured key-value facts (e.g., user preferences) rather than full dialogue text.

* Best practice: save structured summaries (preferences, constraints, important facts) so they can be reinserted into prompts only when needed.

<Frame>
  <img alt="The image shows a smartphone displaying a chat interface with a prompt summarizing user preferences for trip advice, emphasizing a warm climate and avoiding crowds." />
</Frame>

<Callout icon="lightbulb">
  Store concise user preferences and persistent facts as structured summaries so they can be re-inserted into the prompt when needed without exhausting the token budget.
</Callout>

## 3) Role-based filtering

Drop or downweight messages by role. Tool outputs, debug traces, or verbose system logs are often lower value than user inputs and assistant replies—preserve the latter first.

* Strategy: assign priorities by role (e.g., user > assistant > tool > system logs) and prune lower-priority content when nearing the token limit.
* Result: retains the conversational thread while removing noisy content.

<Frame>
  <img alt="The image shows a list interface illustrating role-based filtering with categories like &#x22;User,&#x22; &#x22;Tool,&#x22; and &#x22;System,&#x22; alongside a circular icon and flag for each entry." />
</Frame>

## 4) Chunking with recency bias

Group messages into semantic or task-based chunks (by session, topic, or milestone). When overflow occurs, evict whole older chunks while keeping recent ones intact—this mirrors human short-term memory and preserves coherence within retained chunks.

* Example approach:
  * Partition conversation into chunks per topic or step.
  * When trimming, drop older chunks rather than scattered lines.

<Frame>
  <img alt="The image illustrates the concept of &#x22;Chunking With Recency Bias,&#x22; featuring overlapping text segments in shades of black, gray, and blue, resembling layers of information." />
</Frame>

## 5) Memory snapshots and external storage

At logical milestones (e.g., task completion, end of a step), store compressed snapshots of the dialogue or session state. When the active prompt must remain small, retrieve the most relevant snapshot instead of loading the whole history.

* Storage options:
  * Vector databases for semantic search and retrieval.
  * Document stores or key-value systems for structured facts.

* Example: store a snapshot like `Session 2026-05-01: planning Paris trip — prefers museums, budget $2000` and use semantic search to pull relevant snapshots.

<Frame>
  <img alt="The image illustrates a strategy for &#x22;Memory Snapshots,&#x22; showing a woman pointing at a document with a highlighted text box explaining the concept of storing compressed dialogue snapshots at milestones." />
</Frame>

Reference: see resources on vector DBs for GenAI workflows such as `https://learn.kodekloud.com/user/courses/vector-database-for-genai`.

## 6) Combine techniques and iterate

No single method is optimal for every application. Combine summarization, role-based filtering, chunking, and snapshots to create a predictable policy for your workflow.

* Test different mixes against real usage patterns.
* Tailor the balance of freshness vs. historical coverage depending on app type:
  * Chatbots benefit from recency prioritization + role-based filtering.
  * Long-form assistants benefit from summarization + snapshots.
  * Multi-step planners benefit from chunking + memory snapshots.

<Frame>
  <img alt="The image illustrates &#x22;Combining Strategies,&#x22; showing a toolbox labeled &#x22;Context Strategies&#x22; alongside a list of strategies: &#x22;Summarize older turns,&#x22; &#x22;Prioritize recent ones,&#x22; and &#x22;Filter system noise.&#x22;" />
</Frame>

## Key operational points (checklist)

* Identify what must never be dropped (system prompts, safety constraints, user preferences) and mark these as highest priority.

* Define deterministic policies for:
  * Automatic summarization frequency and format.
  * Chunk eviction rules and sizes.
  * External snapshot cadence and retrieval logic.

* Monitor model outputs for drift or hallucinations as policies evolve and iterate on thresholds.

* Quick checklist:
  * [ ] Protect system prompts and safety instructions.
  * [ ] Persist user preferences as structured data.
  * [ ] Implement semantic search on snapshots for retrieval.
  * [ ] Log and review examples where truncation caused errors.

Context overflow is inevitable in real-world LLM apps. The goal is to design policies that preserve the most useful information for your app’s behavior and user intent. Test, observe, and iterate on your strategy to maintain reliability.

<Frame>
  <img alt="The image displays three takeaways: planning for inevitable overflow, choosing strategies based on app behavior, and testing and evolving handling logic." />
</Frame>

Like someone deciding which packages to keep on a crowded cart, choose the context you can't live without and discard or compress the rest.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-b58a-4c3e-9e5e-851e67d45b06/lesson/ba89c994-703e-4cf1-b8fb-adbb6560a2a9" />
</CardGroup>
