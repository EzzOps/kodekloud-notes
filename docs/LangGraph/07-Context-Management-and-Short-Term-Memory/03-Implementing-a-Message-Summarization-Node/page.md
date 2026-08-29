# If needed in a fresh environment, uncomment:
!pip -q install matplotlib
```

Import required modules:

```python theme={null}
from typing import TypedDict, List, Dict
import math
import matplotlib.pyplot as plt
```

Step 2 — Shared state and token estimation

We simulate a small conversational memory container similar to what agent frameworks use. The state contains:

* `messages`: list of recent message dictionaries (`role` and `content`)
* `summary`: compressed long-term memory (string)
* `turn_count`: counter to decide when to summarize

For visualization we use a simple token estimator: roughly one token per four characters. This is an approximation for illustrative purposes only.

```python theme={null}
class ChatState(TypedDict):
    messages: List[Dict[str, str]]
    summary: str
    turn_count: int

def new_state() -> ChatState:
    return {
        'messages': [],
        'summary': '',
        'turn_count': 0,
    }

def estimate_tokens_from_text(text: str) -> int:
    # Rough approximation: ~1 token per 4 characters
    return math.ceil(len(text) / 4)

def estimate_state_tokens(state: ChatState) -> int:
    message_text = '\n'.join([f"{m['role']}: {m['content']}" for m in state['messages']])
    total_text = f"SUMMARY:\n{state['summary']}\n\nMESSAGES:\n{message_text}"
    return estimate_tokens_from_text(total_text)
```

Step 3 — Naive chatbot: append every turn forever

This naive implementation appends both the user message and the assistant response to `messages` and increments `turn_count`. Nothing is removed or compressed.

```python theme={null}
def append_turn(state: ChatState, user_text: str, ai_text: str) -> ChatState:
    state['messages'].append({'role': 'human', 'content': user_text})
    state['messages'].append({'role': 'ai', 'content': ai_text})
    state['turn_count'] += 1
    return state
```

Step 4 — Simulate a long conversation (naive)

We simulate a series of turns across several topics with intentionally verbose messages to make token growth visible.

```python theme={null}
topics = [
    'cloud architecture',
    'vector search',
    'retrieval augmented generation',
    'LLM evaluation',
    'cost optimization',
    'agent memory',
    'tool calling',
    'multi-agent routing',
    'guardrails',
    'prompt engineering',
    'streaming UX',
    'summarization strategies',
]

def make_user_message(i: int, topic: str) -> str:
    return (
        f"Turn {i}: Explain {topic} in detail, compare it with earlier concepts, "
        f"and keep the explanation practical for an enterprise chatbot that must scale."
    )

def make_ai_message(i: int, topic: str) -> str:
    return (
        f"On turn {i}, the assistant explains {topic}, relates it to previous topics, "
        f"adds trade-offs, risks, and examples, and provides a fairly long answer meant to simulate real token growth."
    )
```

Run the naive simulation and record estimated tokens after each turn:

```python theme={null}
naive_state = new_state()
naive_token_growth = []

for i in range(1, 13):
    topic = topics[(i - 1) % len(topics)]
    naive_state = append_turn(
        naive_state,
        make_user_message(i, topic),
        make_ai_message(i, topic),
    )
    naive_token_growth.append(estimate_state_tokens(naive_state))

print(naive_token_growth)  # estimated token counts after each turn
```

You should observe a steady upward curve: every turn increases the prompt size and estimated token count. This is the token crisis.

Step 5 — Introduce a summarization node

A practical solution is to periodically summarize older parts of the conversation into a compact summary, keeping only the most recent turns in full. The pattern is:

* Compress older history into a `summary` string
* Keep recent messages verbatim (short-term context)
* Reset `turn_count`
* Trigger summarization when `turn_count` reaches a threshold

Below is a deterministic demo summarizer that extracts topic-like fragments and builds a compact summary. In production, you would typically call a language model for higher-quality, semantic summarization.

```python theme={null}
def should_summarize(state: ChatState, threshold: int = 4) -> bool:
    # Summarize when the number of turns since the last summary reaches the threshold
    return state['turn_count'] >= threshold

def summarize_messages(state: ChatState) -> ChatState:
    if not state['messages']:
        return state

    recent_topics = []
    # Look back across recent messages for phrasing like "Explain <topic> in detail"
    for msg in state['messages'][-8:]:
        text = msg['content']
        part = None
        if 'Explain' in text and 'in detail' in text:
            # Extract the substring between 'Explain' and 'in detail'
            part = text.split('Explain', 1)[1].split('in detail', 1)[0].strip(' :')
        elif 'Explain' in text:
            # Extract the substring after 'Explain' if 'in detail' is not present
            part = text.split('Explain', 1)[1].strip(' :')
        else:
            # Fallback: take the first few words as a short descriptor
            part = ' '.join(text.split()[:6])

        recent_topics.append(part)

    # Remove duplicates while preserving order and form a compact summary
    compressed = ' . '.join(dict.fromkeys(recent_topics)) or 'previous discussion topics'
    state['summary'] = f'Conversation so far covered: {compressed}.'
    # Keep only the last 2 messages as the immediate short-term context
    state['messages'] = state['messages'][-2:]
    state['turn_count'] = 0
    return state
```

> **lightbulb** Periodic summarization is a common pattern in production chat architectures: compress older context into a summary while keeping recent turns verbatim to preserve immediate context.

> **warning** This demo's token estimator and summarizer are simplified for illustration. In production, use a model-based summarizer and an accurate tokenizer for your target LLM (e.g., tiktoken for OpenAI models).

Step 6 — Run the memory-aware (managed) version

Run a second simulation that summarizes every 4 turns (threshold is tunable). We record token estimates and the summaries created.

```python theme={null}
smart_state = new_state()
smart_token_growth = []
summaries_created = []

for i in range(1, 13):
    topic = topics[(i - 1) % len(topics)]
    smart_state = append_turn(
        smart_state,
        make_user_message(i, topic),
        make_ai_message(i, topic),
    )

    if should_summarize(smart_state, threshold=4):
        smart_state = summarize_messages(smart_state)
        summaries_created.append((i, smart_state['summary']))

    smart_token_growth.append(estimate_state_tokens(smart_state))

print("Managed token growth:", smart_token_growth)
print("\nSummaries created:")
for turn, summary in summaries_created:
    print(f"After turn {turn}: {summary}")
```

With summarization, token growth becomes controlled: older parts of the conversation are compressed while recent turns remain detailed. This prevents the unbounded upward curve seen in the naive approach.

Step 7 — Visual comparison (plot)

Plot naive vs managed token growth to see the difference.

```python theme={null}
plt.figure(figsize=(9, 5))
plt.plot(range(1, len(naive_token_growth) + 1), naive_token_growth, marker='o', label='Naive: keep everything')
plt.plot(range(1, len(smart_token_growth) + 1), smart_token_growth, marker='s', label='Managed: summarize every 4 turns')
plt.xlabel('Turn')
plt.ylabel('Estimated Tokens in State')
plt.title('The Token Crisis vs Context Management')
plt.grid(True)
plt.legend()
plt.show()
```

Step 8 — Constructing the prompt: inject the summary + recent messages

A production-ready prompt pattern combines:

* A system instruction
* A compressed `summary` (older context)
* The most recent messages (short-term context) verbatim

This pattern preserves long-term context efficiently while keeping the active context small.

```python theme={null}
def build_prompt(state: ChatState) -> str:
    recent_messages = '\n'.join([f"{m['role']}: {m['content']}" for m in state['messages']])
    return (
        "SYSTEM: You are a helpful assistant.\n"
        f"SYSTEM: Conversation summary so far: {state['summary']}\n\n"
        f"RECENT TURNS:\n{recent_messages}\n\n"
    )

print(build_prompt(smart_state))
```

Example output (approximate):

```text theme={null}
SYSTEM: You are a helpful assistant.
SYSTEM: Conversation summary so far: Conversation so far covered: guardrails . prompt engineering . streaming UX . summarization strategies.

RECENT TURNS:
human: Turn 12: Explain summarization strategies in detail, compare it with earlier concepts, and keep the explanation practical for an enterprise chatbot that must scale.
ai: On turn 12, the assistant explains summarization strategies, relates it to previous topics, adds trade-offs, risks, and examples, and provides a fairly long answer meant to simulate this situation.
```

Step 9 — Takeaways

* The token crisis: without context management, conversation history grows until it exhausts the model’s context window, increasing cost and latency.
* Summarization-based memory: periodically compress older interactions into a compact summary and keep recent turns verbatim — this reduces tokens while preserving relevant context.
* Production pattern: build prompts combining a system instruction, a compressed long-term summary, and a short-term verbatim buffer. This scales well across many turns.

Comparison: naive vs managed

| Approach                         | Behavior                                                        | Pros                                                                  | Cons                                                             |
| -------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Naive (keep everything)          | Append every turn verbatim                                      | Simple to implement; full context available                           | Unbounded token growth, higher latency/cost, hits context window |
| Managed (periodic summarization) | Compress older turns into `summary`, keep recent turns verbatim | Controls token growth; reduces cost and latency; scales to many turns | Requires summarization logic and careful tuning of thresholds    |

Links and References

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (example reference)
* Use tokenizer libraries such as `tiktoken` for accurate token counts with OpenAI models
* Consider model-based summarizers or fine-tuned summarization prompts for production-quality memory

Memory design is one of the most important architectural choices for production conversational systems: it directly impacts cost, latency, and session lifetime. Use periodic summarization (or other memory management strategies) to avoid the token crisis and keep conversations scalable.

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/372c4db3-b58a-4c3e-9e5e-851e67d45b06/lesson/5a5fa6eb-9e6a-4515-8e62-ad114796993b)


# Implementing a Message Summarization Node

Source: https://notes.kodekloud.com/docs/LangGraph/Context-Management-and-Short-Term-Memory/Implementing-a-Message-Summarization-Node/page

Explains building a message summarization node that compresses conversation history to save tokens, manage graph state, trigger summarization, store summaries, and monitor for information loss.

Summarization is a critical technique for managing token limits in long-running conversations with large language models (LLMs). Rather than discarding prior messages, a summarization node compresses them into a compact, high-value representation that preserves essential context while trimming verbosity. This reduces token usage, lowers cost, and improves model reliability.

A message summarization node in LangGraph is a modular function that ingests a list of messages and returns a condensed representation. You can inject that summary back into the graph state to replace or augment the full chat history, keeping downstream nodes efficient and focused.

<Frame>
  <img alt="The image illustrates a &#x22;Message Summarization Node&#x22; flowchart showing messages being condensed into a summary, leading to a &#x22;Graph State,&#x22; ensuring a compact, high-value input flow." />
</Frame>

Imagine Robbie, who maintains pages of delivery logs. Before passing his notes to the next person, he rewrites the important parts onto a single sticky note. That sticky note is the summary: compact, actionable, and easy to carry forward.

<Frame>
  <img alt="The image titled &#x22;Message Summarization Node&#x22; illustrates a process involving delivery logs being summarized into a sticky note, featuring a person holding a package." />
</Frame>

You don't need to summarize after every turn. Trigger summarization strategically — for example, at the end of a task cycle, before calling an LLM with tight token constraints, or after multiple turns of accumulated history. This targeted approach preserves compute and avoids unnecessary overhead.

<Frame>
  <img alt="The image outlines when to use summarization: at key transition points, before calling LLM nodes with tight limits, and when accumulating too many messages." />
</Frame>

## Why a Summarization Node?

When conversations expand, simple trimming or filtering can lose context. A summarization node compresses the conversation into a smaller, information-dense representation so the graph continues to operate with sufficient context without exceeding token budgets.

Key benefits:

* Keeps long-running workflows efficient.
* Reduces token consumption and cost.
* Preserves essential facts, objectives, and action items.
* Enables historical context to be reloaded compactly (e.g., from a vector DB).

## Typical Implementation Flow

1. Instantiate a chat model to generate summaries.
2. Define the graph state schema (e.g., `messages` + `summary`).
3. Implement a node that builds a prompt (system instruction + conversation) and asks the model to produce a concise summary.
4. Store the summary in state and optionally reset or trim `messages`.

Example implementation (Python). Adjust imports, types, and the model invocation to match your SDK or runtime.

```python theme={null}
from typing import List, TypedDict
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
