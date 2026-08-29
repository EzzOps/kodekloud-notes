# Demo The Conditional Edge

Source: https://notes.kodekloud.com/docs/LangGraph/The-Core-Workflow-Nodes-Edges-and-Routing/Demo-The-Conditional-Edge/page

Demonstrates using LangGraph conditional edges to route between web search and direct LLM answers, showing node implementations, state wiring, example runs, and Mermaid visualization

In this short lesson we demonstrate how to use LangGraph conditional edges to route between multiple execution paths in an agentic workflow. The example is intentionally simple: based on the user's question, the graph either performs a web search using Tavily or answers directly with an LLM. Both paths converge into a final formatting step.

This tutorial covers:

* environment setup and imports,
* the shared typed state for the graph,
* node implementations (intent classification, web search, direct answer, formatting),
* wiring the StateGraph with conditional edges,
* running two example invocations to observe routing,
* and printing the Mermaid source for visualization.

<Callout icon="lightbulb">
  Before running the code, set your `OPENAI_API_KEY` and `TAVILY_API_KEY` environment variables. For local testing you can also set them in the script using `os.environ.setdefault(...)`.
</Callout>

<Callout icon="warning">
  Never commit your API keys to version control. Use environment variables or a secrets manager in production.
</Callout>

```python theme={null}
