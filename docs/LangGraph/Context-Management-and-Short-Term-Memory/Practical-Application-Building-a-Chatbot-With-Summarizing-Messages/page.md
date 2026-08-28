# Setup model (adjust model_name/parameters for your SDK)
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)

# Define graph state schema
class GraphState(TypedDict):
    messages: List[HumanMessage | AIMessage]
    summary: str

# Summarization node
def summarize_messages(state: GraphState) -> GraphState:
    """
    Build a system prompt asking the model to summarize the conversation,
    then call the chat model with the combined messages.
    """
    prompt = [SystemMessage(content="Summarize the following conversation:")] + state["messages"]

    # Many chat clients return a single AIMessage or a list; adapt the call to your SDK.
    # Here we use predict_messages which returns a list of messages; take the first AIMessage.
    response = model.predict_messages(prompt)
    ai_message = None
    for msg in response:
        if isinstance(msg, AIMessage):
            ai_message = msg
            break
    summary_text = ai_message.content if ai_message else ""

    return {
        "summary": summary_text,
        "messages": [],  # Optionally clear or trim messages after summarization
    }
```

The prompt begins with a clear system instruction such as "Summarize the following conversation:" followed by the message history. The model returns a summary you store in the graph state and then optionally reset or trim the `messages` list. This compresses the conversation so it stops growing unbounded while preserving context.

## When to Trigger Summarization

Use summarization intentionally at transition points that meaningfully reduce context size or before expensive downstream steps.

| Trigger Point                                 | Why it helps                                                 |
| --------------------------------------------- | ------------------------------------------------------------ |
| End of a task cycle                           | Consolidates final decisions and outcomes for the next cycle |
| Before calling a memory- or compute-heavy LLM | Keeps the prompt within token limits                         |
| After N conversational turns                  | Prevents accumulation of low-value chit-chat                 |
| Prior to persisting to long-term storage      | Stores compressed, relevant history                          |

## State Management Patterns

After creating a summary, you can choose how to store or apply it:

| Storage Strategy                      | When to use                                | Example                                           |
| ------------------------------------- | ------------------------------------------ | ------------------------------------------------- |
| Overwrite messages with summary       | When raw history is unneeded or costly     | `{"summary": "...", "messages": []}`              |
| Keep both summary and raw messages    | For auditing or debugging                  | `{"summary": "...", "messages": [...]} `          |
| Maintain summary + truncated messages | Preserve recent turns + compressed history | `{"summary": "...", "messages": recent_messages}` |

<Frame>
  <img alt="The image is a flowchart titled &#x22;Adding Summary to Graph State,&#x22; depicting a process that starts with an initial state, followed by summarization/processing logic leading to different state options like &#x22;summary,&#x22; &#x22;messages,&#x22; and &#x22;history.&#x22;" />
</Frame>

## Advanced Summarization Strategies

To improve fidelity and downstream utility, consider:

* Incremental summaries: update an existing summary after each turn rather than re-summarizing the whole history.
* Role-based summaries: generate separate summaries for user, assistant, and tool messages to preserve perspective.
* Structured summaries: produce JSON or key-value summaries to simplify downstream parsing and filtering.
* Combine summarization with trimming: summarize the portion you plan to remove, then trim it from the message list.
* Persist summaries in a vector store or other long-term storage to reload compact history for new sessions.

For working with persistent storage and vector databases, see resources on vector DBs and persistent storage strategies, such as [vector databases for GenAI](https://learn.kodekloud.com/user/courses/vector-database-for-genai).

<Frame>
  <img alt="The image illustrates the concept of combining summarization and trimming, with icons representing vector store and persistent storage." />
</Frame>

## Monitoring and Improving Summaries

Summarization is not infallible. Implement monitoring and feedback to detect and correct information loss:

* Log summary outputs and compare them periodically to raw history.
* Add explicit prompt instructions to preserve critical facts, goals, and action items (e.g., "Preserve any user goals and action items").
* Use structured formats (JSON) to make validation and downstream processing deterministic.
* Consider human-in-the-loop review for mission-critical flows.

<Frame>
  <img alt="The image outlines steps for monitoring and improving summaries: reviewing and refining them regularly, comparing with full context, and tuning prompts for detail." />
</Frame>

Over time, iterate on prompts and summarization cadence so summaries become both smaller and more informative — saving tokens while preserving critical context.

<Frame>
  <img alt="The image presents two key takeaways: summarization nodes compress history without losing context, and they improve token efficiency and focus." />
</Frame>

<Callout icon="lightbulb">
  Trigger summarization at meaningful transition points (end of task cycles, before expensive reasoning, or when history size exceeds thresholds) to balance compute cost and context fidelity.
</Callout>

<Callout icon="warning">
  Always validate summaries periodically. Important facts can be lost in aggressive compression — monitor, log, and tune prompts accordingly.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-b58a-4c3e-9e5e-851e67d45b06/lesson/8c234f88-7163-4865-9489-a31a37eae7bc" />
</CardGroup>


# Practical Application Building a Chatbot With Summarizing Messages

Source: https://notes.kodekloud.com/docs/LangGraph/Context-Management-and-Short-Term-Memory/Practical-Application-Building-a-Chatbot-With-Summarizing-Messages/page

Building a stateful chatbot that summarizes older conversation turns to manage context, reduce tokens, and preserve important facts using hybrid short-term messages and compressed summary

In this lesson we apply message-summarization techniques to build a stateful chatbot that handles long conversations without exhausting the model's context window. Instead of sending the entire message history on every turn, the chatbot periodically compresses older turns into a concise summary and continues the conversation using only the essential context.

This pattern keeps the model focused, reduces token and latency costs, and preserves important facts and decisions across long-running sessions.

<Frame>
  <img alt="The image illustrates a process flow from &#x22;Past Messages&#x22; through a &#x22;Summarization Process&#x22; to produce &#x22;Recent Context,&#x22; which then feeds into a &#x22;Model.&#x22;" />
</Frame>

Use case example: customer-support agents often summarize a ticket's history rather than repeating every past exchange. Our chatbot follows the same approach—summarize older turns and retain the immediacy of recent messages.

<Frame>
  <img alt="The image illustrates a concept for a customer support summary system, showing past interactions transforming into a support ticket summary." />
</Frame>

## Architecture overview

High-level flow:

* User input → short-term messages (working memory) → LLM node produces a reply.
* A summarization node compresses older messages after a threshold and stores that compressed text in the graph state.
* For generation, the LLM prompt is built from the stored summary plus recent messages (not the entire history).

This hybrid memory strategy combines long-term compressed context with a short-term working window.

## State design

In LangGraph the graph state is the single shared memory object passed between nodes. The state defines what every node reads, writes, and routes on, so its shape is a primary architectural decision.

A compact ChatState schema (using TypedDict) looks like:

```python theme={null}
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage

class ChatState(TypedDict):
    messages: List[BaseMessage]  # Recent message history (short-term working memory)
    summary: str                  # Compressed summary of older history (long-term memory)
    turn_count: int               # Integer counter to trigger summarization or other actions
```

Table: ChatState fields and purpose

| Field        | Purpose                                                                        | Example                                                                     |
| ------------ | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| `messages`   | Short-term working memory containing the most recent `BaseMessage` objects     | `["HumanMessage(...)", "AIMessage(...)"]`                                   |
| `summary`    | Compressed long-term context; contains facts, decisions, and important details | `"Customer prefers email; issue: login failure; tried resetting password."` |
| `turn_count` | Control counter to trigger summarization, retries, or routing                  | `0`                                                                         |

This schema gives a balanced memory architecture: short-term context for immediacy, compressed long-term memory for historical facts, and control logic (the counter) to determine when to compress.

## Summarization node

The summarization node compresses the `messages` into a concise `summary` and updates the state. Typical responsibilities:

* Build a summarization prompt that preserves facts, decisions, deadlines, and requested actions.
* Invoke a model to produce a summary.
* Merge the new summary with the existing summary (optionally), trim `messages`, and reset or adjust counters.

Example summarization node (concise):

```python theme={null}
from langchain_core.messages import SystemMessage
from typing import List
