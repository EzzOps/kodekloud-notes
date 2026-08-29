# Application spawns service and sends a prompt over stdin
echo "Summarize this document" | ./mcp-service
```

## HTTP

HTTP exposes the MCP service over a network so clients send standard HTTP requests and receive HTTP responses. This follows the familiar client–server API model and supports remote access, load balancing, and multi-client usage.

How HTTP works:

* Client sends an HTTP request containing the prompt or payload.
* The MCP service processes the request and returns an HTTP response (JSON, text, etc.).
* Each logical request is independent, though underlying TCP connections may be reused (keep-alive).

When to use HTTP:

* Short, atomic tasks such as classification, function calling, or quick Q\&A.
* Cases that require remote access, authentication, and horizontal scaling.
* When you need a conventional REST/gRPC-style API surface.

Trade-offs:

* HTTP adds per-request overhead (headers, TLS handshake, request lifecycle).
* Connection reuse (keep-alive) and HTTP/2 can mitigate overhead for many small requests.

Reference: [HTTP overview — MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

<Frame>
  <img alt="A diagram titled &#x22;HTTPS&#x22; showing a local application sending a prompt to an MCP service on another local machine which connects to the Internet and backend resources, with responses returned to the application." />
</Frame>

## SSE (Server-Sent Events)

SSE (Server-Sent Events) is an HTTP-based, server→client streaming mechanism. The client makes an initial HTTP request to open a long-lived connection; the server then pushes events to the client when new data is available. SSE is ideal for sending incremental outputs (e.g., streaming model tokens) to improve perceived responsiveness.

How SSE works:

* Client initiates an HTTP request to open the event stream.
* The server keeps the connection open and sends `text/event-stream` messages incrementally.
* The client receives server-pushed events without repeatedly re-establishing HTTP handshakes.

Important details:

* SSE is unidirectional (server → client). For bidirectional streaming (client ↔ server), use WebSockets or another full-duplex protocol.
* SSE is text-based and works well in browsers via the EventSource API.

Reference: [Server-sent events — MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

<Frame>
  <img alt="A diagram titled &#x22;SSE — Server Sent Events&#x22; showing an Application on a local machine making an initial request to an MCP Service on another local machine. The MCP Service keeps a persistent connection to push events and interacts with the internet and backend resources." />
</Frame>

## Protocol differences and typical use cases

Below is a concise comparison of the three transports to help you decide which to use.

| Feature / Transport | STDIO                                              | HTTP                                                                        | SSE                                                               |
| ------------------- | -------------------------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Connection model    | Local IPC via `stdin`/`stdout` (no network)        | Request–response over HTTP(S)                                               | Single persistent HTTP connection (server → client)               |
| Data flow           | One-shot: write prompt → read full response        | Request → process → full response (can stream with chunked encoding)        | Client opens stream; server pushes events incrementally           |
| Best for            | Local dev, CLI tools, single-machine batch jobs    | Short, atomic tasks: classification, function calls, quick Q\&A             | Chat UIs, long-running generation, progressive token streaming    |
| Overhead            | Very low — minimal IPC overhead                    | Higher per-request overhead (headers, TLS); connection reuse mitigates cost | Low initial handshake; lightweight per-message overhead once open |
| Directionality      | Bi-directional only via process I/O; not networked | Request–response (client → server, then server → client)                    | Unidirectional (server → client)                                  |

<Frame>
  <img alt="A presentation slide titled &#x22;Protocol Differences and Use Cases&#x22; showing a three-column comparison table for STDIO, HTTPS, and SSE. It compares features like Connection, Data Flow, Best for, and Overhead (e.g., local inter-process vs individual TCP connection vs single persistent streaming)." />
</Frame>

## Summary — Which transport should you pick?

* STDIO: Use for fast, simple local integrations, developer tooling, CLI utilities, and environments where both processes run on the same host.
* HTTP: Use when you need a network-accessible API, multi-client access, load balancing, authentication, or short, atomic requests.
* SSE: Use when you want server-to-client streaming (for example, streaming model tokens for a chat UI). For full two-way streaming, prefer [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) or another bidirectional protocol.

> **lightbulb** SSE is a one-way stream (server → client). If your use case requires simultaneous client↔server streaming, use WebSockets or another full-duplex protocol.

Further reading and references:

* [Standard streams (stdin/stdout) — Wikipedia](https://en.wikipedia.org/wiki/Standard_streams)
* [HTTP overview — MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
* [Server-sent events — MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
* [WebSocket — MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

Now you should understand the differences between STDIO, HTTP, and SSE MCP service types and which transport to choose for common scenarios.

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/a27f1996-5412-4f48-a085-c87d68c51206/lesson/1c04f1d1-a2e5-4e6b-aa8e-9e2e8b3e9d35)


# Testing a Local MCP Server

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Core-Concepts/Testing-a-Local-MCP-Server/page

Guide to manually and automatically testing local MCP STDIO servers using Postman, MCP Inspector, shell piping, and Node-based CI-friendly test patterns

Hey — this lesson walks through practical ways to test a local MCP (Model Context Protocol) server. You'll find quick manual techniques for one-off checks, interactive UIs for exploring tools, and automated patterns for CI/CD-friendly tests that work well with STDIO MCP servers.

<Frame>
  <img alt="A presentation slide titled &#x22;Testing a Local MCP Server&#x22; with a large stylized &#x22;Demo&#x22; on a dark curved background to the right. The slide includes a small &#x22;© Copyright KodeKloud&#x22; note in the bottom-left." />
</Frame>

Callouts

> **lightbulb** Use interactive tools for quick debugging ([Postman](https://www.postman.com/), [MCP Inspector](https://www.npmjs.com/package/@modelcontextprotocol/inspector)), and automated tests for CI/CD (MCP Tester or language-specific test frameworks).

Why test locally?

* Validate tool discovery (`tools/list`) and invocation (`tools/call`) before deploying.
* Catch protocol/JSON-RPC issues early.
* Automate checks to prevent regressions in CI/CD.

Summary of approaches

| Method                            | Best for                                                     | Quick example                                                                |
| --------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| Manual STDIO via Postman          | Fast interactive spot checks of STDIO MCP servers            | Use Postman transport type `STDIO` and run `node /full/path/to/server.js`    |
| MCP Inspector (web UI)            | Interactive exploration and structured debugging             | `npx @modelcontextprotocol/inspector node server.js`                         |
| Automated Node tests (MCP Tester) | Repeatable CI checks that spawn processes and assert results | Create a test script that spawns `node server.js` and communicates via STDIO |
| Shell piping (echo)               | Very quick one-off checks or shell scripts                   | See section 4 for an echo example (echo a JSON-RPC request into node)        |

Important: For any table cells or inline examples containing curly braces or angle brackets we use code formatting so MDX doesn't try to parse them.

***

## 1) Quick manual testing with Postman (STDIO)

Postman supports launching a process and communicating over STDIO. This is ideal for ad-hoc verification of JSON-RPC requests/responses.

Steps:

1. Open Postman → New → MCP request.
2. Select transport type: STDIO.
3. Set command to `node` and arguments to the full path of your `server.js` (e.g., `/full/path/to/server.js`).
4. Postman will spawn `node /full/path/to/server.js` and communicate via STDIO.
5. Use `tools/list` to discover tools, and `tools/call` to invoke them.

Example JSON-RPC request to call the `add-integers` tool:

```json theme={null}
{
  "method": "tools/call",
  "params": {
    "name": "add-integers",
    "arguments": {
      "a": 0,
      "b": 0
    }
  }
}
```

Minimal `server.js` example that exposes a single tool (add-integers):

```javascript theme={null}
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/transport";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types";

const server = new Server(
  {
    name: "basic-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
    transport: new StdioServerTransport(),
  }
);

// List tools handler
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "add-integers",
        description: "Add two integers and return the result",
        inputSchema: {
          type: "object",
          properties: {
            a: { type: "integer", description: "First integer to add" },
            b: { type: "integer", description: "Second integer to add" }
          },
          required: ["a", "b"]
        }
      }
    ]
  };
});

// Call tool handler (example)
server.setRequestHandler(CallToolRequestSchema, async ({ params }) => {
  if (params.name === "add-integers") {
    const { a, b } = params.arguments;
    return {
      content: [
        {
          type: "text",
          text: String(a + b)
        }
      ]
    };
  }
  throw new Error("Tool not found");
});

server.listen();
```

Once connected in Postman, call the tool with `a=3` and `b=4` and verify the output (`"7"`).

***

## 2) Using MCP Inspector (interactive web UI)

[MCP Inspector](https://www.npmjs.com/package/@modelcontextprotocol/inspector) gives a web UI tailored to MCP servers. It’s excellent for exploring tool metadata, trying inputs, and seeing raw JSON-RPC traffic.

Quick start:

```bash theme={null}
npx @modelcontextprotocol/inspector node server.js
```

What to expect:

* The inspector prints a local URL and a session token — open that in your browser.
* Configure transport: STDIO, command: `node`, arguments: `server.js`.
* You can call `tools/list`, `tools/call`, fill input fields, and view a history of JSON-RPC messages and raw stdin/stdout.

Inspector highlights:

* Transport configuration (STDIO)
* Tool discovery and input fields (e.g., `add-integers`)
* JSON-RPC request/response history
* Convenient manual testing similar to Postman but MCP-focused

***

## 3) Automated tests with a Node "MCP Tester"

Automated tests are essential for CI. The pattern below spawns your server, writes JSON-RPC messages to STDIN, captures STDOUT, and asserts correct behavior.

Example test helper (compact):

```javascript theme={null}
#!/usr/bin/env node

import { spawn } from "child_process";
import { strict as assert } from "assert";

class MCPTester {
  constructor(entry = "server.js") {
    this.entry = entry;
    this.server = null;
    this._buffer = "";
  }

  spawnServer() {
    this.server = spawn("node", [this.entry], { stdio: ["pipe", "pipe", "inherit"] });

    // Capture stdout chunks and buffer them for JSON parsing
    this.server.stdout.on("data", (chunk) => {
      this._buffer += chunk.toString();
    });

    // Wait a short time to allow server startup logs; in real tests use a readiness probe
    return new Promise((resolve) => setTimeout(resolve, 200));
  }

  async sendMessage(message) {
    if (!this.server) throw new Error("Server not started");
    const payload = JSON.stringify(message) + "\n";

    // Clear buffer before sending
    this._buffer = "";

    this.server.stdin.write(payload);

    // Wait for a matching response by ID
    return new Promise((resolve, reject) => {
      const cleanup = () => clearInterval(interval);

      const wrappedResolve = (value) => {
        clearTimeout(timeout);
        cleanup();
        resolve(value);
      };
      const wrappedReject = (err) => {
        clearTimeout(timeout);
        cleanup();
        reject(err);
      };

      const timeout = setTimeout(() => wrappedReject(new Error("Response timeout")), 2000);

      const onData = () => {
        // Try to find first JSON object in buffer
        try {
          // Attempt multiple parses in case startup logs precede JSON
          const start = this._buffer.indexOf("{");
          const end = this._buffer.lastIndexOf("}");
          if (start !== -1 && end !== -1 && end > start) {
            const candidate = this._buffer.slice(start, end + 1);
            const parsed = JSON.parse(candidate);
            if (parsed && parsed.id === message.id) {
              wrappedResolve(parsed);
            }
          }
        } catch (err) {
          // ignore parse errors until buffer contains full JSON
        }
      };

      // Poll buffer periodically for responses (simple approach)
      const interval = setInterval(() => {
        try {
          onData();
        } catch (e) {
          // Ignore
        }
      }, 50);
    });
  }

  killServer() {
    if (this.server) {
      this.server.kill();
      this.server = null;
    }
  }

  async testListTools() {
    await this.spawnServer();
    try {
      const message = {
        jsonrpc: "2.0",
        id: 1,
        method: "tools/list",
        params: {}
      };
      const response = await this.sendMessage(message);

      assert(response.jsonrpc === "2.0", "Response should have jsonrpc 2.0");
      assert(response.id === 1, "Response should have matching id");
      assert(response.result, "Response should have result");
      assert(Array.isArray(response.result.tools), "Result should have tools array");
      // This test expects exactly one tool (change as appropriate)
      assert(response.result.tools.length === 1, "Should have exactly one tool");

      const tool = response.result.tools[0];
      assert(tool.name === "add-integers", "Tool name should be add-integers");
      assert(tool.description, "Tool should have description");
      assert(tool.inputSchema, "Tool should have inputSchema");
      assert(tool.inputSchema.properties.a, "Tool should require parameter 'a'");
      assert(tool.inputSchema.properties.b, "Tool should require parameter 'b'");
    } finally {
      this.killServer();
    }
  }

  async testAddIntegersValid() {
    await this.spawnServer();
    try {
      const message = {
        jsonrpc: "2.0",
        id: 2,
        method: "tools/call",
        params: {
          name: "add-integers",
          arguments: {
            a: 5,
            b: 3
          }
        }
      };

      const response = await this.sendMessage(message);

      assert(response.jsonrpc === "2.0", "Response should have jsonrpc 2.0");
      assert(response.id === 2, "Response should have matching id");
      assert(response.result, "Response should have result");
      assert(Array.isArray(response.result.content), "Result should have content array");
      assert(response.result.content.length === 1, "Should have one content item");
      assert(response.result.content[0].type === "text", "Content should be text type");
      assert(response.result.content[0].text === "8", "5 + 3 should equal 8");
    } finally {
      this.killServer();
    }
  }
}

// Example runner
(async () => {
  const tester = new MCPTester("server.js");
  try {
    await tester.testListTools();
    console.log("testListTools PASSED");
    await tester.testAddIntegersValid();
    console.log("testAddIntegersValid PASSED");
  } catch (err) {
    console.error("Test failed:", err);
    process.exit(1);
  }
})();
```

Notes on the example:

* `sendMessage` uses a simple polling approach to extract JSON from a mixed stdout buffer. For production, implement a robust framing strategy (newline-delimited JSON, explicit frames, or length-prefix).
* Add a proper readiness probe (e.g., wait for a specific log line or implement a `ready` JSON-RPC method) rather than fixed sleep timers.
* Integrate these tests as part of `npm test` or your CI job so failures block merges.

***

## 4) Crude but fast: echoing JSON into the server (shell)

For one-off checks you can pipe a JSON-RPC request into the server process:

```bash theme={null}
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | node server.js
```

Example console output (startup logs followed by the JSON-RPC response):

```text theme={null}
Basic MCP Server running on stdio
{"result":{"tools":[{"name":"add-integers","description":"Add two integers and return the result","inputSchema":{"type":"object","properties":{"a":{"type":"integer","description":"First integer to add"},"b":{"type":"integer","description":"Second integer to add"}},"required":["a","b"]}}]},"jsonrpc":"2.0","id":1}
```

Use this approach for quick smoke tests or to write simple shell-based checks and automation.

***

## Recommendations and next steps

* Use Postman or MCP Inspector for interactive debugging and rapid exploration.
* Add automated tests (like the MCP Tester example) to CI so regressions are caught early.
* If your server is implemented in other languages (Python, Java, etc.), implement equivalent tests using that language’s test frameworks:
  * Python: `pytest`, `unittest`
  * Java: `JUnit`
  * Node: `mocha`, `jest`
* For reliable automation:
  * Use a clear STDIO framing protocol (e.g., newline-delimited JSON).
  * Add explicit readiness checks before sending requests.
  * Capture and assert on both structured JSON-RPC responses and important logs.

> **lightbulb** Automated tests are essential. Manual checks are helpful for debugging, but CI/CD tests prevent regressions and give confidence when deploying changes.

## Links and references

* [MCP Inspector (npm)](https://www.npmjs.com/package/@modelcontextprotocol/inspector)
* [Postman](https://www.postman.com/)
* JSON-RPC 2.0 specification: [https://www.jsonrpc.org/specification](https://www.jsonrpc.org/specification)
* Node child\_process.spawn: [https://nodejs.org/api/child\_process.html#child\_process\_child\_process\_spawn\_command\_args\_options](https://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options)

If you want, I can adapt the automated test to use a line-delimited JSON framing strategy or convert the tester into a Jest/Mocha test suite ready for CI.

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/a27f1996-5412-4f48-a085-c87d68c51206/lesson/83d1f673-c1c9-4b33-93dc-198bd818a56b)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/a27f1996-5412-4f48-a085-c87d68c51206/lesson/9693b203-2dbe-43a7-8554-471b9d76a834)
