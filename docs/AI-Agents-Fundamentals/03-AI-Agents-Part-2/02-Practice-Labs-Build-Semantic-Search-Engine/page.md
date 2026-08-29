# Initialize the MCP server
mcp = FastMCP("Calculator")

# Create calculator tools using FastMCP decorators
@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together"""
    result = a + b
    print(f"🔧 Tool 'add' called with a={a}, b={b}")
    print(f"➕ Result: {result}")
    return result

# Create the multiply tool
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    result = a * b
    print(f"🔧 Tool 'multiply' called with a={a}, b={b}")
    print(f"✖ Result: {result}")
    return result
```

Tips for tool implementations:

* Use Python type hints for parameters and return types; they generate structured schemas consumed by clients.
* Keep logs inside tools for easier debugging (print statements or structured logging).
* Choose the appropriate transport: stdin/stdout is easiest for local tests; SSE/HTTP is suitable for distributed clients.

Expected console output when the server starts (illustrative):

```text theme={null}
✅ Task 1 complete! MCP tools tested successfully.
------------------------------------------------------------
🚀 STARTING MCP SERVER
------------------------------------------------------------
The calculator MCP server is now starting...
Keep this terminal open - the server will run continuously.
Use Ctrl-C to stop the server when you're done.

Server ready! Waiting for client connections...
```

> **lightbulb** Keep the server terminal open while clients connect. If you stop the server, the agent will no longer be able to reach the tools.

***

## Task 2 — Integrate MCP tools with a LangGraph agent

Connect the Calculator server to a LangGraph (or LangChain-style) agent. The client obtains tools via client.get\_tools(), and the agent is created with those tools so it can choose when to call them (for example, using a ReAct-style agent).

Example async integration (completed):

```python theme={null}
async def run_agent_with_mcp():
    """Create and run agent with MCP tools"""

    # Get tools from MCP client
    tools = await client.get_tools()

    # Create react agent with model and tools
    agent = create_react_agent(model, tools)

    print("✅ Agent created with MCP tools!\n")
    print("=" * 60)
    print("TESTING MCP-INTEGRATED AGENT:")
    print("=" * 60)

    # Test 1: Math query (should use MCP tools)
    print("\nTest 1: Math Query")
    math_response = await agent.ainvoke({
        "messages": "What is 25 plus 17?"
    })
    print(f"Response: {math_response['messages'][-1].content}")
```

Representative debug output:

```text theme={null}
Processing request of type ListToolsRequest
Processing request of type CallToolRequest

Response: 25 plus 17 is 42.

Test 2: Non-math Query
Response: The capital of France is Paris.
```

Notes:

* The agent uses tool schemas to decide whether invoking a tool is appropriate.
* Non-math queries that require general knowledge should be handled by the model directly without tool calls.

***

## Task 3 — Multi-server orchestration (Calculator + Weather)

Scale the system by connecting multiple MCP servers (for example, Calculator and Weather). A MultiServerMCPClient or equivalent gathers tools from all servers; the agent is then built with the aggregated toolset so it can route requests to the right service.

Example multi-server orchestration (cleaned and completed):

```python theme={null}
async def run_multi_server_agent():
    """Create and run agent with tools from multiple MCP servers"""

    print("📦 Loading tools from multiple servers...")

    # Get all tools from both servers
    tools = await client.get_tools()

    print(f"✅ Loaded {len(tools) if hasattr(tools, '__len__') else 'multiple'} tools from servers")

    # Create react agent with model and tools
    agent = create_react_agent(model, tools)

    print("\n" + "-" * 60)
    print("TESTING MULTI-SERVER ORCHESTRATION:")
    print("=" * 60)

    # Example queries
    print("\nTest 1: Calculator query")
    calc_response = await agent.ainvoke({"messages": "What is 8 times 9?"})
    print(f"Response: {calc_response['messages'][-1].content}")

    print("\nTest 2: Weather comparison query")
    weather_response = await agent.ainvoke({
        "messages": "Compare current weather in New York and Tokyo."
    })
    print(f"Response: {weather_response['messages'][-1].content}")
```

Representative outputs when multiple servers are used:

```text theme={null}
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Response: 8 times 9 is 72.

Processing request of type CallToolRequest
Processing request of type ListToolsRequest
Response: The current weather comparison between New York and Tokyo is as follows:

New York:
- Temperature: 17°C
- Condition: Clear
- Humidity: 58%
- Wind: 14 km/h

Tokyo:
- Temperature: 18°C
- Condition: Clear
- Humidity: 51%
- Wind: 16 km/h

Both cities have clear weather with similar temperatures, but New York has slightly higher humidity while Tokyo has a bit stronger wind.
```

Best practices for multi-server setups:

* Use a consistent naming convention (for example, prefix tools with the server name) so tools from different servers do not collide.
* Monitor ListToolsRequest and CallToolRequest logs to trace cross-server calls.
* Start with read-only tools when exposing external systems (APIs, DBs) and gradually add write capabilities with proper access control.

<Frame>
  <img alt="A screenshot of a developer tutorial UI showing completed MCP integration with LangGraph: four task cards (MCP Basics, Integration, Multi-Server, Ready For) and a &#x22;Key Takeaways&#x22; panel listing points about MCP, naming, routing, and extensibility. A file explorer with Python files is visible in a dark sidebar on the right." />
</Frame>

***

## Deeper explorations and next steps

Once you are comfortable with MCP basics and multi-server orchestration, extend MCP to expose:

* Databases (query/update operations)
* External REST APIs (wrapped as typed tools)
* File systems (search, read, write)
* Human-in-the-loop endpoints (approval workflows)

The pattern stays the same:

1. Expose structured tools on an MCP server.
2. Fetch tools from the client (client.get\_tools()).
3. Build an agent (create\_react\_agent or similar) that orchestrates tool calls as needed.

Key reminders:

| Topic         | Recommendation                                                         |
| ------------- | ---------------------------------------------------------------------- |
| Tool schemas  | Use type hints for strong, machine-readable schemas                    |
| Transports    | Start with stdin/stdout for local tests; use HTTP/SSE for production   |
| Security      | Protect write operations and external integrations with authentication |
| Observability | Log ListToolsRequest and CallToolRequest for troubleshooting           |

This concludes the lesson. Experiment with exposing new resources and creating safe, auditable human-in-the-loop flows.

***

## Links and references

* [LangChain course (overview)](https://learn.kodekloud.com/user/courses/langchain)
* LangGraph documentation (refer to your project docs or README for LangGraph usage)
* MCP adapters (installed via pip as part of this lab)

Happy experimenting — extend your agents with real-world services using MCP and LangGraph.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/ff68d510-a374-46e6-ac61-0ac106069c3b/lesson/75f70469-4662-4439-b7c3-bb356785e38b)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/ff68d510-a374-46e6-ac61-0ac106069c3b/lesson/817f248b-aee4-483d-ad03-79b134bb8c50)


# Practice Labs Build Semantic Search Engine

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-2/Practice-Labs-Build-Semantic-Search-Engine/page

Guide to building a production-ready semantic search engine using embeddings, document chunking, ChromaDB and LangChain, with examples for embedding creation, indexing, and similarity search.

We're going to build a semantic search engine step-by-step.

The story begins with TechDocs, Inc., where users search through documentation 10,000 times a day. More than half of those searches fail because traditional keyword search can't connect related phrases like "reset password" and "password recovery."

Our mission is to fix that by building a search system that understands meaning, not just words.

<Frame>
  <img alt="A screenshot of a presentation or tutorial page titled &#x22;Mission: Build TechDocs Semantic Search Engine&#x22; that explains a documentation search problem (high failure rate due to keyword mismatches) and outlines a mission to build a semantic search engine to improve results. The page shows Before/After examples and a note about using embeddings rather than AI generation." />
</Frame>

## Approach overview

We’ll build a production-grade semantic search pipeline by following these core steps:

* Convert text (documents and queries) into vector embeddings using an embedding model (sentence-transformers / Hugging Face).
* Store embeddings in a fast vector database (ChromaDB) for nearest-neighbor search.
* For each query, find nearby document embeddings (semantic similarity) and retrieve the top-K chunks.
* Rank and return the most relevant document chunks to the user.

This approach enables queries like "forgot my password" to match documents titled "Password recovery" or "Login help" even when keywords differ.

## Environment setup

Install the packages used for embeddings, orchestration, and vector storage:

* sentence-transformers — embedding models (e.g. all-MiniLM-L6-v2)
* LangChain — orchestration utilities & text splitters
* langchain-community & langchain-huggingface — community integrations for LangChain
* ChromaDB — vector database
* numpy, tempfile, and other utilities

<Frame>
  <img alt="A screenshot of an &#x22;Environment Setup&#x22; panel showing &#x22;Installing Vector Search Libraries&#x22; with a checklist of packages (sentence-transformers, langchain, langchain-community, langchain-huggingface, chromadb, numpy) and model names to auto-download. On the right is a code file list including README.md and several task_*.py files." />
</Frame>

Example environment setup (bash):

```bash theme={null}
