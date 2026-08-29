# Demo The Token Crisis

Source: https://notes.kodekloud.com/docs/LangGraph/Context-Management-and-Short-Term-Memory/Demo-The-Token-Crisis/page

Demonstrates periodic summarization to manage conversational token growth, compress older context into summaries, and preserve recent turns to reduce tokens, cost, and latency.

In this lesson we simulate a common production problem for conversational AI: the token crisis. When you naively append every user and assistant turn to the prompt, the conversation history grows without bound. Over time this increases token counts, latency, and cost, and eventually exceeds the model’s context window — making the system slow, expensive, or unusable.

This demo demonstrates how periodic memory summarization controls token growth. It uses plain Python (no external APIs), so you can focus on architecture and behavior rather than infrastructure.

Overview

* Problem: Unbounded prompt growth (the "token crisis")
* Solution: Periodic summarization to compress older context into long-term memory while keeping recent turns verbatim
* Demo: Two simulations (naive vs managed) and a visual comparison

Step 1 — Setup

Install the optional plotting package (matplotlib is used below):

```bash theme={null}
