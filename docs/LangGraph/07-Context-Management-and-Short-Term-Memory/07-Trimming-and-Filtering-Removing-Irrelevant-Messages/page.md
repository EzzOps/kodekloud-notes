# Instantiate the streaming stdout handler
stream_handler = StreamingStdOutCallbackHandler()

# Streaming-enabled model with handler
llm = ChatOpenAI(
    streaming=True,                  # emit tokens incrementally
    callbacks=[stream_handler],      # handle streaming events
    model="gpt-3.5-turbo",
    temperature=0.7,
)
```

Why streaming matters

* Perceived speed and engagement improve even if total latency is the same.
* Users can interrupt or redirect generation mid-response.
* Streaming supports long outputs (code generation, multi-part summaries) with progressive rendering.

Streaming is orthogonal to your graph topology: the same nodes and orchestration patterns work with either sync or streaming outputs. The difference is how tokens are emitted and consumed during node execution.

Streaming relies on callbacks (the observer pattern)
Libraries like [LangChain](https://langchain.readthedocs.io/) use an observer/callback model: each newly generated token triggers an event that your handler receives. The handler can print tokens (development mode), send them via WebSocket, append to a buffer, or apply moderation checks.

Minimal custom callback example

```python theme={null}
from langchain.callbacks.base import BaseCallbackHandler

class CustomStreamHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # Prints tokens as they arrive to create a typing effect.
        # In production, replace this with WebSocket sends, buffering, or storage.
        print(token, end="", flush=True)
```

Architectural insight: decoupling concerns
Streaming decouples:

* generation logic (the model),
* orchestration (graph execution, branching, tools),
* presentation logic (UI, sockets, buffering).

You can route tokens to multiple sinks (live UI, logs, metrics, storage) without changing model code.

Production streaming patterns

| Pattern                   | Purpose                                                | Example                                                                                                      |
| ------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| WebSocket live stream     | Low-latency, two-way updates between client and server | Send each token over a persistent connection to render as it arrives                                         |
| Buffering + finalization  | Stream UX while preserving a final complete response   | Stream tokens to the UI and accumulate a buffer; on completion, persist `final_buffer` to conversation state |
| Hybrid (stream + storage) | Real-time UX plus auditing/analytics                   | Stream tokens to the client and simultaneously write final transcript to storage for later inspection        |

Practical considerations for production

* Typical handlers: a WebSocket handler for live UIs, a buffering handler that assembles the final response, or a hybrid handler that streams while persisting the finished output.
* Useful flow: stream tokens to the user, accumulate a final response in-memory, and commit the final response to conversation history once generation completes.
* Monitoring: instrument token rates, partial/complete response sizes, and error rates to track health and UX regressions.

Frontend integration
To show streaming to users, use WebSocket, Server-Sent Events (SSE), or chunked HTTP responses to relay tokens. On the client, buffer incoming text and animate it (typing effect, cursor, incremental highlights). Small UX elements — animated dots, a blinking cursor, or a real-time progress bar — significantly improve perceived responsiveness.

Challenges and trade-offs
Streaming adds complexity: buffering, partial output handling, interleaving token streams, finalization hooks, retries, and consistency guarantees all require careful engineering and testing.

<Frame>
  <img alt="The image presents three challenges in streaming: it's more complex than sync output, requires managing token buffers and interleaving, and is harder to test and debug." />
</Frame>

Takeaways for product and engineering teams

* Streaming transforms an LLM from a blocking black box into an event-driven system that feels alive to users.
* It’s typically a small configuration change (enable streaming + attach handlers) with an outsized UX payoff.
* Plan for partial outputs: buffering, finalization hooks, consistency checks, and robust error handling.
* Invest in tracing, testing, and monitoring to catch subtle failures or degraded experiences.

<Frame>
  <img alt="The image lists four takeaways related to user experience and chatbots, highlighting the benefits of streaming, human-like interactions, engineering effort, and UX improvements." />
</Frame>

References and links

* LangChain callbacks and streaming: [https://langchain.readthedocs.io/](https://langchain.readthedocs.io/)
* WebSockets for real-time UIs: [https://developer.mozilla.org/docs/Web/API/WebSockets\_API](https://developer.mozilla.org/docs/Web/API/WebSockets_API)
* Server-Sent Events (SSE): [https://developer.mozilla.org/docs/Web/API/Server-sent\_events](https://developer.mozilla.org/docs/Web/API/Server-sent_events)

> **lightbulb** Streaming is a small configuration change with a large UX impact: enable streaming on the model, attach a handler, and stream tokens to the client (WebSocket/SSE/HTTP-chunked) for real-time, responsive interactions.

> **warning** Remember to design for partial outputs: implement buffering, finalization hooks, and robust error handling to avoid inconsistent or truncated user-visible responses.

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/372c4db3-b58a-4c3e-9e5e-851e67d45b06/lesson/ae40e239-a2a4-459d-afe4-91a46fd9e673)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/langgraph/module/372c4db3-b58a-4c3e-9e5e-851e67d45b06/lesson/5c0a78aa-ee9f-4204-8e63-9f3c04e1c746)


# Trimming and Filtering Removing Irrelevant Messages

Source: https://notes.kodekloud.com/docs/LangGraph/Context-Management-and-Short-Term-Memory/Trimming-and-Filtering-Removing-Irrelevant-Messages/page

Techniques for trimming and filtering conversational context in LLM pipelines to reduce token usage, lower cost, improve latency, and preserve relevant information while avoiding loss of critical context.

Large language models have finite context windows and every token matters. Sending outdated, redundant, or low-value content wastes tokens, increases cost, and weakens model focus. Trimming and filtering are not just micro-optimizations — they are core design patterns for robust LLM workflows.

> **lightbulb** Trim and filter early in your pipeline. Doing so reduces cost, improves latency, and helps the model concentrate on the most relevant signals.

<Frame>
  <img alt="The image discusses the importance of trimming and filtering, highlighting them as core design principles and not just optimizations. It features a block of text and a highlighter icon." />
</Frame>

Think of trimming and filtering like editing a conversation before you hand it to the model: keep what's helpful and cut the clutter.

<Frame>
  <img alt="The image depicts a person sitting at a desk using a computer, with a large email interface on the screen and the text &#x22;Why Trimming and Filtering Matter&#x22; above." />
</Frame>

What’s the difference?

* Trimming typically means removing messages by position (for example, dropping the oldest entries).
* Filtering uses metadata or content rules to decide which messages remain (e.g., exclude system prompts or tool traces).

<Frame>
  <img alt="The image provides an overview of &#x22;Trimming and Filtering,&#x22; highlighting that filtering uses message metadata or logic to decide what stays and what goes." />
</Frame>

Together they give you fine-grained control over what the LLM sees. Imagine Ravi sorting delivery notes: he discards duplicates and old logs but retains the directions that help him finish the route — that’s trimming and filtering in practice.

Recency-based trimming is the simplest rule: keep the most recent N turns and discard the rest. It’s especially effective for chat-oriented or support scenarios where only recent exchanges are relevant.

<Frame>
  <img alt="The image illustrates a process of &#x22;Trimming by Recency,&#x22; where less recent data (Turns 1-3) is trimmed, and the most recent and current data (Turns 4-7) is kept for relevance and used by a large language model (LLM)." />
</Frame>

Be mindful: important context can hide in older turns. Combine recency trimming with other heuristics or summarization to avoid losing crucial information.

<Frame>
  <img alt="The image illustrates a concept of &#x22;Trimming by Recency&#x22; with a smartphone displaying a chat interface, highlighting that it works best for casual or support chats and notes the importance of watching for hidden context in earlier turns." />
</Frame>

Filtering by role or type often removes noise: tool outputs, system prompts, diagnostic traces, or verbose metadata frequently add little value to generation and should be filtered out so the model can focus on user and assistant content.

<Frame>
  <img alt="The image illustrates a &#x22;Filtering by Role or Type&#x22; process, where various inputs such as user, assistant, and metadata are processed through a filtering mechanism before reaching a large language model (LLM)." />
</Frame>

Content-based filtering further refines what remains. Remove repeated statements, overly vague turns, or messages that add no new information. Heuristic scoring or simple NLP checks (e.g., token overlap, similarity, or length thresholds) are effective and cheap.

<Frame>
  <img alt="The image is a flowchart illustrating content-based filtering, showing how content (specific, repetitive, new info, vague) is filtered to be either kept or trimmed." />
</Frame>

Even lightweight NLP can detect repetition and discard low-signal phrases, freeing tokens for higher-value context.

Practical pattern: filter relevant messages before the LLM call. In production, token limits are a hard constraint — if you keep appending messages without pruning, the context window fills up and your pipeline suffers (higher cost, slower responses, worse outputs).

Here’s a concise, deterministic Python example that filters out non-conversational messages and keeps only user and assistant turns:

```python theme={null}
from typing import Dict, Any, List

def filter_messages(state: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Keep only conversational messages (human and ai) from the state.

    Expected input shape:
    {
        "messages": [
            {"type": "human", "text": "...", ...},
            {"type": "tool", "text": "...", ...},
            ...
        ]
    }
    """
    messages = state.get("messages", [])
    filtered = [
        msg for msg in messages
        if msg.get("type") in ("human", "ai")
    ]
    return {"messages": filtered}
```

This approach is cheap, testable, and deterministic. Typical extensions:

* Trim by length or keep only the last N conversational turns.
* Deduplicate repeated messages.
* Score and prune low-value turns.
* Summarize older context instead of dropping it.

Filtering is one of the highest-impact optimizations for long-running dialogs: it reduces cost, improves latency, and keeps the model’s reasoning focused. Small preprocessing steps produce outsized improvements in system robustness.

However, trimming can be dangerous if applied too aggressively. If you drop a task setup, constraint, or an earlier user question, the model may lose essential context.

<Frame>
  <img alt="The image is a diagram titled &#x22;Common Mistakes to Avoid,&#x22; featuring four points: trimming away essential context, removing key task details, not testing filters across scenarios, and assuming the model can infer missing info." />
</Frame>

> **warning** Be cautious: overly aggressive trimming or filtering can remove crucial context. Validate filters on diverse conversations and add safeties that preserve critical messages.

Best practice is a hybrid strategy: combine recency trimming, role/type filtering, content-based pruning, and summarization. Make your graph or pipeline configurable — expose parameters (e.g., `max_turns`, `min_token_value`, summarization thresholds) so trimming adapts to the task. Use observability to measure token usage, latency, and model quality to ensure filters help rather than harm.

<Frame>
  <img alt="The image is a diagram of &#x22;Best Practices&#x22; with four interconnected strategies: combining trimming, filtering, and summarization; keeping context handling flexible; adapting trimming to the task; and measuring impact with observability tools." />
</Frame>

Quick reference — Trimming & Filtering patterns

| Strategy                     |                                             When to use | Example / Notes                                          |
| ---------------------------- | ------------------------------------------------------: | -------------------------------------------------------- |
| Recency trimming             | Chats where only recent turns matter (support/chatbots) | Keep last N turns: `N = 6`                               |
| Role/type filtering          |   Remove noise like tool outputs, logs, system messages | Keep only `human` and `ai` messages                      |
| Content-based filtering      |        Remove duplicates, low-signal, or vague messages | Remove if similarity > 0.95 or length \< 5 tokens        |
| Summarization of old context |    Long conversations with important historical context | Replace older turns with a short summary (50–200 tokens) |

In LLM workflows, context is currency. Every token counts. Thoughtful trimming and filtering improve relevance, reduce cost, and increase user satisfaction. When done well, these techniques ensure the model sees what truly matters — like Ravi keeping only the delivery notes that get him to the doorstep.

<Frame>
  <img alt="The image lists four key takeaways about managing context in LLM workflows, emphasizing its critical importance, token management, relevance focus, and performance improvement." />
</Frame>

Links and references

* [OpenAI: Context management & long prompts](https://platform.openai.com/docs/guides/longer-contexts)
* [Best practices for prompt engineering and cost optimization](https://platform.openai.com/docs/guides/cost-and-latency)

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/372c4db3-b58a-4c3e-9e5e-851e67d45b06/lesson/11578f67-d4df-41d9-9e5d-f9ba745d553b)
