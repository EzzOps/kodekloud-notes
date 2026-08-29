# Streaming for Responsive UX

Source: https://notes.kodekloud.com/docs/LangGraph/Context-Management-and-Short-Term-Memory/Streaming-for-Responsive-UX/page

How streaming LLM outputs token-by-token improves perceived responsiveness, UX, and architecture while detailing handlers, frontend integration, patterns, and production trade-offs.

In user experience design, perceived speed is a superpower. Even when a language model needs time to produce a full answer, streaming partial output token-by-token creates a sense of immediacy. Users stay engaged, worry less about latency, and can interact mid-generation — much like how humans speak and build meaning incrementally.

<Frame>
  <img alt="The image describes why streaming matters for user experience (UX), highlighting benefits like perceived speed boosting satisfaction, reducing wait anxiety, and feeling natural and conversational." />
</Frame>

What is streaming in LLMs? Streaming means the model emits output incrementally (often token-by-token) instead of returning a single completed message. Implementing streaming requires both the model backend and your orchestration or application infrastructure to support incremental events and callbacks. Streaming is a core pattern for real-time, responsive UIs and interactive agents.

<Frame>
  <img alt="The image illustrates &#x22;Streaming in LLMs,&#x22; showing a flow from the &#x22;AI Model Backend&#x22; through tokens with &#x22;Stream = True&#x22; to a phone with a chat interface, emphasizing real-time interaction and incremental token delivery." />
</Frame>

Key benefits of streaming include immediate user feedback, reduced anxiety about stalled requests, and the ability to interrupt, steer, or augment generation mid-flight. This pattern unlocks UX features such as partial rendering, progressive summarization, and real-time tool invocation — giving users control rather than a blocking, opaque process.

<Frame>
  <img alt="The image outlines the benefits of streaming, which include immediate feedback to keep users engaged, demonstrating that the system isn't stuck, and enabling interruption or real-time feedback." />
</Frame>

How to enable streaming (overview)

* At the model/node level: flip a streaming flag (for example, `streaming=True`) when you construct the model or node.
* Attach a callback or stream handler to consume emitted tokens as they arrive.
* The orchestrator emits streaming events during node execution; your handler decides whether to push tokens to the UI, buffer them, or apply policies (moderation, logging, metrics).

Minimal example (enabling streaming on a Chat model)

```python theme={null}
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
