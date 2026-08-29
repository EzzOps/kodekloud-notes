# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI(title="customer-db-mcp", version="0.1.0")


# Request schema: what the MCP client (the AI agent) will send
class GetCustomerRequest(BaseModel):
    customer_id: str


# Response schema: what the MCP server returns
class Customer(BaseModel):
    customer_id: str
    name: str
    email: Optional[str] = None
    status: str  # e.g., 'shipped', 'processing', 'closed' (use values appropriate for your domain)


# Fake in-memory database (replace with real DB in production)
customers: Dict[str, Customer] = {
    "1234": Customer(customer_id="1234", name="Alice Johnson", email="alice@example.com", status="shipped"),
    "2345": Customer(customer_id="2345", name="Bob Smith", email="bob@example.com", status="processing"),
}


@app.post("/mcp/get_customer", response_model=Customer)
async def get_customer(req: GetCustomerRequest):
    """
    MCP function: returns customer information by customer_id.
    The agent can call this endpoint to retrieve customer state.
    """
    cust = customers.get(req.customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="customer not found")
    return cust
```

Run the server with uvicorn:

```bash theme={null}
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

Example MCP client request (what an agent or other client would send):

```bash theme={null}
curl -X POST "http://localhost:8000/mcp/get_customer" \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "1234"}'
```

Example JSON response:

```json theme={null}
{
  "customer_id": "1234",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "status": "shipped"
}
```

## Key components and best practices

| Component                   | Purpose                                 | Example / Notes                      |
| --------------------------- | --------------------------------------- | ------------------------------------ |
| Endpoint (function surface) | Defines callable operations for agents  | POST /mcp/get\_customer              |
| Typed schemas               | Makes discovery and validation reliable | Pydantic models, OpenAPI schemas     |
| Persistence                 | Store and retrieve real-world state     | SQL, MongoDB, managed services       |
| Security                    | Protect data and control access         | API keys, OAuth, RBAC, rate limits   |
| Agent discovery             | How agents find and interpret functions | OpenAPI, function registry, metadata |

This structure—define endpoints and schemas once—lets any compatible agent call your MCP server to fetch or modify external state. Many ecosystems publish reusable MCP adapters for common services (e.g., source control, databases, productivity tools), letting you plug them into agents without custom integration work.

> **lightbulb** MCP servers should clearly define input and output schemas (e.g., via [OpenAPI](https://www.openapis.org) / [Pydantic](https://docs.pydantic.dev)). This makes it easy for agents to discover and call them reliably. In production, secure these endpoints (authentication, authorization, rate-limiting) before exposing them to agents.

## Links and references

* FastAPI: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
* uvicorn: [https://www.uvicorn.org](https://www.uvicorn.org)
* Pydantic: [https://docs.pydantic.dev](https://docs.pydantic.dev)
* OpenAPI: [https://www.openapis.org](https://www.openapis.org)
* SQL: [https://en.wikipedia.org/wiki/SQL](https://en.wikipedia.org/wiki/SQL)
* MongoDB: [https://www.mongodb.com](https://www.mongodb.com)
* Example repositories and community MCP adapters: search GitHub for "MCP" and "agent tooling" for community-provided integrations

Use this pattern to make your AI assistants actionable: define function surfaces, provide strict schemas, and secure endpoints—then let the agent do the integration work.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/ff68d510-a374-46e6-ac61-0ac106069c3b/lesson/d88f28a2-ea10-4b4a-abfb-a427c54fcf5e)


# Practice Labs Advanced MCP Concepts

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-2/Practice-Labs-Advanced-MCP-Concepts/page

Guide to using MCP with LangGraph to expose and integrate external tools and multi-server orchestration for agents, including setup, calculator server, tool schemas, and examples.

We go deeper into MCP (Model Context Protocol) and demonstrate how to extend LangGraph agents with external tools. MCP acts like a universal port (think USB) that standardizes how AI systems connect to tools, databases, and APIs. With MCP, LangGraph agents can call out to external services and receive structured responses.

This lesson covers:

* Environment setup for the lab
* Conceptual MCP architecture and how it maps to agents
* Task 1: Run a simple MCP server (Calculator)
* Task 2: Connect an agent to MCP tools
* Task 3: Orchestrate multiple MCP servers and aggregate tools
* Next steps and references

***

## Environment — create the virtual environment and install dependencies

Create or activate your virtual environment, then install the required packages: LangGraph (workflow framework), LangChain (core model abstractions), and the MCP adapters for model integration and servers.

Environment setup (bash)

```bash theme={null}
cd /root && source /root/venv/bin/activate

pip install langgraph langchain langchain-openai langchain-mcp-adapters
```

You may see dependency messages during installation similar to:

```text theme={null}
Requirement already satisfied: sse-starlette>=1.6.1 in ./venv/lib/python3.12/site-packages (from mcp>=1.9.2->langchain-mcp-adapters) (3.0.2)
Requirement already satisfied: starlette>=0.27 in ./venv/lib/python3.12/site-packages (from mcp>=1.9.2->langchain-mcp-adapters) (0.48.0)
Requirement already satisfied: uvicorn>=0.31.1 in ./venv/lib/python3.12/site-packages (from mcp>=1.9.2->langchain-mcp-adapters) (0.37.0)
Requirement already satisfied: attrs>=22.2.0 in ./venv/lib/python3.12/site-packages (from jsonschema>=4.20.0->mcp>=1.9.2->langchain-mcp-adapters) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in ./venv/lib/python3.12/site-packages (from jsonschema>=4.20.0->mcp>=1.9.2->langchain-mcp-adapters) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in ./venv/lib/python3.12/site-packages (from jsonschema>=4.20.0->mcp>=1.9.2->langchain-mcp-adapters) (0.36.2)
Requirement already satisfied: rpds-py>=0.7.1 in ./venv/lib/python3.12/site-packages (from jsonschema>=4.20.0->mcp>=1.9.2->langchain-mcp-adapters) (0.27.1)
Requirement already satisfied: python-dotenv>=0.21.0 in ./venv/lib/python3.12/site-packages (from pydantic-settings>=2.5.2->mcp>=1.9.2->langchain-mcp-adapters) (1.1.1)
```

Run the verification script:

```bash theme={null}
python3 /root/code/task_1_mcp_basics.py
```

***

## MCP architecture — conceptual overview

MCP bridges an AI assistant built with LangGraph to external tools and services. The high-level flow:

* The MCP server registers tools and publishes their schemas.
* A client connects to the server and fetches tool definitions.
* A LangGraph (or LangChain-style) agent receives those tools and decides when to call them.
* When invoked, the MCP client routes the tool call to the server and returns a structured response.

<Frame>
  <img alt="A presentation slide titled &#x22;Understanding MCP Architecture&#x22; showing a diagram of an AI Assistant linked to an MCP Server via the MCP protocol. Below the diagram are four panels outlining MCP Server, Tools, Integration, and Naming with brief bullet points." />
</Frame>

Analogy: MCP is the USB port — the protocol is the port, the server is a device, and tools are the device's functions. LangGraph is the host computer using those functions.

<Frame>
  <img alt="A dark-themed screenshot of a slide or app UI showing a &#x22;SIMPLE EXAMPLE&#x22; box that compares MCP to USB devices with a numbered list (USB Port, Device, Functions, Computer). A colorful mouse cursor points at the list and nearby panels show headings like Integration and Naming." />
</Frame>

Key MCP concepts at a glance:

| Concept      | Purpose                               | Notes                                                      |
| ------------ | ------------------------------------- | ---------------------------------------------------------- |
| MCP Server   | Hosts tools and exposes their schemas | Tools annotated with type hints produce structured schemas |
| MCP Client   | Discovers and calls tools             | client.get\_tools() returns tools for the agent            |
| Agent        | Uses tools to extend capabilities     | create\_react\_agent(model, tools) builds the agent        |
| Transports   | How server and client communicate     | stdin/stdout, SSE, HTTP supported                          |
| Multi-server | Aggregate tools across servers        | Use multi-server clients to merge toolsets                 |

***

## Task 1 — MCP basics: build a Calculator server

Create a simple MCP server named "Calculator" that exposes calculator tools (add, multiply). Servers can be run using stdin/stdout transport for local testing or via SSE/HTTP for networked deployments.

Example server script (completed):

```python theme={null}
