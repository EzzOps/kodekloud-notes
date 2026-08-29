# Model Context Protocol

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-2/Model-Context-Protocol/page

Describes the Model-Context-Protocol for letting AI agents call registered service endpoints with typed schemas to integrate external systems without custom code

Model-Context-Protocol (MCP) rethinks how AI agents integrate with external systems. Instead of having developers write bespoke API integrations for every use case, MCP lets services register as callable tools that agents can invoke. This shifts the integration burden from application code to the agent, enabling more flexible, composable workflows.

In practice, an MCP server exposes one or more well-defined functions (endpoints) with explicit input and output schemas. When an agent runs, it discovers and calls these functions to query or mutate external state. That makes it straightforward to extend an assistant’s capabilities—plug in an MCP server for a system and the agent can use it without additional glue code.

For example, a TechDocs assistant could query customer, order, inventory, or ticketing systems via MCP endpoints. If a user asks, "What's the status of order 1234?", the agent can call an MCP that queries the order-management system, receive the structured response, and compose a natural-language reply that includes the order state.

<Frame>
  <img alt="A hand-drawn system diagram showing a user asking &#x22;What's the status of order #1234&#x22; to Tech Corp's AI chat assistant and agent. The agent connects to internal knowledge (a vector DB) and external systems (customer database, inventory/support) via an MCP/API to fetch the information." />
</Frame>

## Minimal FastAPI MCP server example

Below is a concise, practical example: a FastAPI-based MCP that exposes a simple customer lookup function. It demonstrates the typical pieces of an MCP server:

* A web app that exposes a function endpoint the agent can call.
* Typed request/response models so agents know how to call the function.
* A persistence layer (here, an in-memory dict) — replace with your production DB.

Use this as a template for a real integration (SQL, MongoDB, or any service).

```python theme={null}
