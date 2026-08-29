# Using State to Drive Conversations

Source: https://notes.kodekloud.com/docs/Google-ADK/ADK-Fundamentals/Using-State-to-Drive-Conversations/page

Guide on using ADK session state to manage multi-turn conversational agents, tracking minimal curated values, scoping keys, dynamic prompt injection, and deterministic state updates for troubleshooting flows.

In this lesson we cover how to use state in Google ADK to build smarter multi-turn conversational agents. Previously we built an agent that can answer questions and call tools; now we go one level deeper to show how agents maintain context across turns so they can perform structured troubleshooting and other multi-step tasks.

State management makes agents intelligent: ADK gives agents a way to remember curated values, track progress through workflows, and keep essential details across turns. This enables structured troubleshooting flows rather than single-shot responses.

## Session, state, history — how they fit

* Session: the top-level container that tracks the conversation, user identity, and event history.
* State: a curated key/value store used to remember values the agent needs to continue a flow (progress markers, flags, decisions, preferences).
* History: the full transcript of messages and tool calls.

History is the complete log of the conversation (every message and tool call). State is selective — a small set of intentionally remembered values that help the agent move a workflow forward (for example, issue type or current troubleshooting step). Think of state as the agent’s working memory: small, curated, and purposeful.

Here’s a simple example showing how you might use `session.state` to track a VPN troubleshooting flow:

```python theme={null}
