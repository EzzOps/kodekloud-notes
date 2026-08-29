# Install locally in your project
npm i mcp-remote

# Or install globally
npm i -g mcp-remote
```

Common mcp-remote CLI usages (port binding, host override, allow non-TLS):

```bash theme={null}
# Basic: proxy a remote SSE endpoint to a local port (default behavior)
npx mcp-remote https://remote.mcp.server/sse

# Bind to a specific local port (e.g., 9696)
npx mcp-remote https://remote.mcp.server/sse 9696

# Bind to a specific local host address
npx mcp-remote https://remote.mcp.server/sse --host 127.0.0.1

# Allow non-TLS (HTTP) remote endpoints (use with caution)
npx mcp-remote http://internal-service.vpc/sse --allow-http
```

Many desktop clients (Claude Desktop, Cursor, Windsurf, etc.) can be configured to launch such a proxy so a remote MCP server appears local to the client.

## Anthropic and Remote MCP Servers

Anthropic’s developer docs include examples and references for remote MCP servers and how production providers typically expose MCP endpoints. A common format for remote MCP endpoints is `https://mcp.<provider>.com/sse`, indicating an SSE-over-HTTPS endpoint for production integrations.

<Frame>
  <img alt="A screenshot of an Anthropic developer documentation page titled &#x22;Remote MCP servers,&#x22; showing a left navigation menu and main content with instructions for connecting to remote MCP servers. The page includes a blue informational notice and example server listings further down." />
</Frame>

<Frame>
  <img alt="A browser screenshot of the Anthropic developer documentation page titled &#x22;Remote MCP server examples.&#x22; It shows a table listing companies (Asana, Atlassian, Cloudflare, etc.) with descriptions and server URLs alongside a left-hand navigation menu." />
</Frame>

## Local vs Remote Trends

* Local MCP servers (Node, Python, Go) remain the most common environment for experimenting and developing MCP integrations. They’re easy to run, test, and hook up to local LLM clients like Claude or Cline.
* Production usage is trending toward remote MCP servers hosted by cloud and platform vendors (Cloudflare, Atlassian, Anthropic, etc.). Remote MCP endpoints typically use SSE over HTTPS to support production-grade integrations with authentication, monitoring, and scaling.

## Wrapping up — How to Explore Further

* Try these resources: Postman Explore, OpenTools registry, PulseMCP, Smithery, and the GitHub awesome list.
* Use `mcp-remote` to connect remote MCP endpoints to local STDIO-only clients when needed.
* Experiment by composing multiple APIs into a single MCP server to simplify complex workflows via natural language orchestration.

Thanks for taking this lesson. If you have questions, join the course community, work through the hands-on exercises, and keep exploring MCP servers and integrations — you’ll build confidence quickly.

## Links and references

* [Postman Explore — MCP Generator](https://postman.com/explore/MCP-generator)
* [OpenTools registry](https://opentools.com/registry)
* [PulseMCP Server Directory](https://pulsemcp.com/servers)
* [Smithery.ai](https://smithery.ai)
* [Awesome MCP Servers (GitHub)](https://github.com/punkpeye/awesome-mcp-servers)
* [Anthropic Developer Docs](https://www.anthropic.com/docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/910a0b7a-ac6e-43f1-956e-203a70c3d455/lesson/8a950c99-347b-4020-baff-3caa7336f2c7)


# Course Introduction What is MCP and Why It Matters

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Pre-requisites/Course-Introduction-What-is-MCP-and-Why-It-Matters/page

Introduction to the Model Context Protocol explaining how a standardized client server framework connects LLMs to external data and tools, enabling live data access, actions, and reusable integrations

What is MCP?

MCP stands for Model Context Protocol. It’s a lightweight, open framework that standardizes how large language models (LLMs) request data and perform actions with external systems. Think of MCP as a common interface — like a universal connector — that lets models interact predictably with databases, file systems, web APIs, and other tools.

<Frame>
  <img alt="A slide titled &#x22;MCP — Introduction&#x22; showing a Model Context Protocol diagram with bidirectional arrows between an AI Model (robot and atom icon) and an External Data Source (globe and database icons). The caption describes it as a framework for enhancing interactions between AI models and external data sources or tools." />
</Frame>

MCP was initiated by [Anthropic](https://www.anthropic.com) (the creators of [Claude](https://www.anthropic.com/claude)), but it’s designed to be an open, vendor-neutral protocol usable with any LLM. A helpful analogy: MCP is like USB for AI — a predictable, standardized way to connect models to external services.

> **lightbulb** MCP enables LLMs to access fresh, private, and actionable information without hardwiring bespoke integrations into every application.

Why MCP matters

Out of the box, LLMs face practical limits that matter for real applications:

* Training cutoff: Models only “know” information up to their training cutoff date.
* No live data access: They cannot query the web or enterprise systems without an external bridge.
* No direct access to private sources: Internal documents and databases require a secure interface to expose data.
* Limited actionability: Models alone don’t perform external actions (send emails, update systems, or run scripts).

Without a protocol like MCP, teams build many custom adapters, which multiplies engineering effort and increases maintenance overhead. MCP reduces duplication by offering a consistent contract between LLMs (via a host) and external services.

What we’ll cover in this lesson/article

* Key components of MCP architecture
* How MCP enables the flow between LLMs, host applications, and external services
* MCP primitives: resources, tools, and prompts
* Real-world examples and practical benefits

Below is a high-level architecture and flow overview.

<Frame>
  <img alt="A dark-slide diagram titled &#x22;How MCP Works&#x22; showing two sections: &#x22;01 Key Components&#x22; listing MCP Client/Host, MCP Protocol, MCP Server, and External Services, and &#x22;02 The Flow&#x22; listing Language Model and Client Application." />
</Frame>

Client–server model (the core idea)

At its heart, MCP uses a familiar client–server pattern to mediate access to tools and data. A restaurant analogy often makes this easy to remember:

* Customer (Host application + LLM): The user-facing app that needs data or an action performed.
* Waiter (MCP client): The messenger that formats and forwards requests using MCP.
* Kitchen (MCP server): The system with access to ingredients (external data and tools) that fulfills requests.
* Ingredients / tools (External services): Databases, file stores, web APIs, and other services.

The MCP client (waiter) sends standardized requests to one or more MCP servers (kitchens). Each server interfaces with the external services (ingredients) to fetch data or execute actions and returns results to the client, which then passes them back to the host and the LLM.

<Frame>
  <img alt="A diagram titled &#x22;How Does MCP Work?&#x22; using a restaurant analogy: the left panel shows &#x22;The Restaurant&#x22; with the client and waiter, and the right panel shows &#x22;The Kitchen (The Server)&#x22; with the chef and ingredients labeled as external data/tools." />
</Frame>

A simplified MCP flow

Typical request sequence:

Host application (with the LLM) → MCP client → MCP server → External data/tool

1. The host and LLM determine additional data or an action is required.
2. The LLM issues an MCP-formatted request to the MCP client.
3. The MCP client routes the request to the correct MCP server.
4. The server communicates with the external resource, retrieves data or performs the action, and returns the result.
5. The client relays the result back to the host application and the LLM.

This separation keeps responsibilities clear and makes it easy to add new capabilities without changing the LLM or host logic.

<Frame>
  <img alt="A diagram titled &#x22;How MCP Works&#x22; showing a vertical flow: Host Application with LLM → MCP Client → MCP Server → External Data/Tool. To the right is a resources column with items like Database, File System, and Third‑Party Web App." />
</Frame>

MCP primitives: resources, tools, and prompts

MCP servers expose three fundamental primitives that LLMs use through the client. These primitives make interactions structured, auditable, and reusable.

| Primitive | Purpose                                           | Common examples                                          |
| --------- | ------------------------------------------------- | -------------------------------------------------------- |
| Resources | Readable context data the LLM can query           | File contents, database rows, API responses              |
| Tools     | Actions the LLM can request the server to perform | Send email, create task, run a script, post to a service |
| Prompts   | Standardized templates or interaction patterns    | Predefined request templates, structured input forms     |

These primitives let the LLM request information or trigger actions in a consistent way across many backends.

<Frame>
  <img alt="A diagram titled &#x22;MCP Primitives&#x22; showing an MCP Server that connects to three categories: Resources (data), Tools (actions) and Prompts (templates). The Tools column lists example actions like sending an email, creating a task, adding an event, and running a script." />
</Frame>

Extending the analogy

In the restaurant metaphor, the host doesn’t need to understand how the kitchen prepares a dish or where every ingredient is sourced. Similarly, MCP abstracts away the internal details of external systems: the LLM “orders” data or an action, and the MCP server returns a consistent, usable response.

Real-world examples

MCP supports practical workflows across many domains. Typical use cases include:

1. File system access — securely read and write files on behalf of the model, with audit logs.
2. GitHub integration — summarize commits, create pull requests, or comment on issues programmatically.
3. Web search augmentation — incorporate recent web results that are outside the model’s training data.
4. Database queries — fetch private customer data to provide contextually accurate answers.

A host application can connect to multiple MCP servers (e.g., one server for files, another for databases, a third for web search), enabling a single LLM-driven interface to orchestrate many backend systems.

<Frame>
  <img alt="A presentation slide titled &#x22;MCP in Action: Real-World Examples&#x22; showing four numbered cards: 01 File System Access, 02 GitHub Integration, 03 Web Search, and 04 Database Access, each with a small icon. The cards are arranged horizontally under a dark header on a light background." />
</Frame>

Benefits of MCP

MCP delivers concrete advantages when building LLM-powered applications:

| Benefit                | What it enables                                                       |
| ---------------------- | --------------------------------------------------------------------- |
| Standardization        | Reusable integrations, less duplicated effort                         |
| Separation of concerns | Host and LLM focus on intent; servers handle integrations             |
| Extensibility          | Add new servers for more services without changing the client         |
| Reduced hallucinations | Verify facts by pulling authoritative data before response generation |
| Enhanced capabilities  | Combine LLM reasoning with real-world actions and live data           |

<Frame>
  <img alt="A presentation slide titled &#x22;MCP – Benefits&#x22; showing five numbered dark cards across the page. The cards list: 01 Standardization, 02 Separation of concerns, 03 Extensibility, 04 Reduced hallucinations, and 05 Enhanced capabilities." />
</Frame>

Final thoughts

MCP shifts how we apply LLMs: from isolated models with static knowledge to connected agents that can securely access live data and perform actions. By standardizing the interface between models and external systems, MCP reduces engineering friction, improves reliability, and unlocks new capabilities.

> **lightbulb** MCP is an open, standard approach for connecting models to external tools and data. In this lesson/article we’ll explore how to design and implement MCP clients and servers and how to use these primitives effectively.

Links and references

* [Anthropic — MCP origin and resources](https://www.anthropic.com)
* [Claude by Anthropic](https://www.anthropic.com/claude)
* Example specs and community projects: search for “Model Context Protocol” or check relevant GitHub repositories for MCP implementations and examples.

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/ef6da233-05e8-4813-b17a-52f829e130f1/lesson/afd3474e-04d7-41d7-beda-5385ab1c261e)
