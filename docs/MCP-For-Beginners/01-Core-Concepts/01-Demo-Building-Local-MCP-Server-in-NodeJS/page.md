# Demo Building Local MCP Server in NodeJS

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Core-Concepts/Demo-Building-Local-MCP-Server-in-NodeJS/page

Guide to building a minimal Node.js MCP stdio server exposing an add-integers tool, including project setup, server implementation, testing via command line and Postman

This lesson shows how to build a minimal stdio MCP (Model Context Protocol) server in Node.js. The goal is a tiny tool catalog exposing a single tool, `add-integers`, which adds two integers. You'll walk through project initialization, a complete `server.js` implementation, and quick ways to test the server from the command line and Postman.

Prerequisites:

* Node.js installed (LTS recommended)

## Quick overview

* Initialize a Node project and install the MCP SDK.
* Implement an MCP `Server` that:
  * exposes a `tools/list` catalog describing input schemas,
  * implements `tools/call` to run the `add-integers` tool,
  * communicates over stdio using `StdioServerTransport`.
* Test via piping JSON into the script or using Postman.

## Initialize the project

Create a new directory and initialize an npm project:

```bash theme={null}
npm init -y
```

Install the MCP SDK:

```bash theme={null}
npm install @modelcontextprotocol/sdk
```

A typical `package.json` for this example enables ES modules and provides a `bin` entry so you can run the server directly:

```json theme={null}
{
  "name": "basic-mcp-server",
  "version": "1.0.0",
  "main": "index.js",
  "type": "module",
  "bin": {
    "basic-mcp-server": "./server.js"
  },
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "description": "",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.15.0"
  }
}
```

<Callout icon="lightbulb">
  Make sure `"type": "module"` is present so Node.js accepts ES module `import` syntax in `server.js`.
</Callout>

## Files and commands at a glance

| Item         | Purpose                   | Example / Command                                       |
| ------------ | ------------------------- | ------------------------------------------------------- |
| Project init | Create package files      | `npm init -y`                                           |
| Install SDK  | Add MCP SDK dependency    | `npm install @modelcontextprotocol/sdk`                 |
| Run server   | Execute script directly   | `node server.js` or `chmod +x server.js && ./server.js` |
| Main file    | MCP server implementation | `server.js`                                             |

## Implement server.js

Create `server.js` in the project root. The file starts with a shebang so you can run it directly from the shell. Import the Server and transport classes and the request schemas from the SDK:

```javascript theme={null}
#!/usr/bin/env node

import { Server, StdioServerTransport } from "@modelcontextprotocol/sdk";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
```

Next, create a Server instance with basic metadata and an initial empty capabilities object:

```javascript theme={null}
const server = new Server(
  {
    name: "basic-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);
```

### Implement the tools catalog (`tools/list`)

When a client requests the tool catalog (`tools/list`), return an array of tools with a clear `inputSchema`. This helps clients know the expected types and required fields. Here we expose a single tool, `add-integers`, which expects two integer properties: `a` and `b`.

```javascript theme={null}
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "add-integers",
        description: "Add two integers and return the result",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "integer",
              description: "First integer to add",
            },
            b: {
              type: "integer",
              description: "Second integer to add",
            },
          },
          required: ["a", "b"],
        },
      },
    ],
  };
});
```

This schema gives clients machine-readable validation rules and clear human-readable descriptions.

### Implement the tool execution (`tools/call`)

Handle `tools/call` requests by extracting the tool name and arguments, validating types, performing the operation, and returning a result in MCP content format. This example requires both arguments to be integers:

```javascript theme={null}
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params || {};
  const a = args?.a;
  const b = args?.b;

  if (name === "add-integers") {
    if (typeof a !== "number" || typeof b !== "number") {
      throw new Error("Both arguments must be numbers");
    }

    if (!Number.isInteger(a) || !Number.isInteger(b)) {
      throw new Error("Both arguments must be integers");
    }

    const result = a + b;

    // Return result as text so clients can parse/convert as needed
    return {
      content: [
        {
          type: "text",
          text: `${result}`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});
```

Tip: returning content as `text` is broadly interoperable; callers that need numbers can parse or convert the text result.

### Start the server using stdio transport

Use `StdioServerTransport` so the server communicates over standard input/output. Wrap startup in an async `main` and log to stderr to avoid polluting MCP JSON responses on stdout:

```javascript theme={null}
async function main() {
  try {
    const transport = new StdioServerTransport();
    await server.listen(transport);
    // Log to stderr so MCP JSON on stdout is not polluted by startup logs
    console.error("Basic MCP Server running on stdio");
  } catch (err) {
    console.error("Server error:", err);
    process.exit(1);
  }
}

main();
```

Make `server.js` executable if you want to run it directly:

```bash theme={null}
chmod +x server.js
./server.js
```

## Test the server from the command line

You can simulate MCP JSON-RPC requests by piping JSON messages into the running script. Because the server writes status messages to stderr, the stdout will contain only the JSON response (useful for automated tests).

1. Test `tools/list`:

```bash theme={null}
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | node server.js
```

Expected stdout (example):

```JSON theme={null}
{"result":{"tools":[{"name":"add-integers","description":"Add two integers and return the result","inputSchema":{"type":"object","properties":{"a":{"type":"integer","description":"First integer to add"},"b":{"type":"integer","description":"Second integer to add"}},"required":["a","b"]}}],"jsonrpc":"2.0","id":1}
```

2. Call the `add-integers` tool:

```bash theme={null}
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"add-integers","arguments":{"a":5,"b":3}}}' | node server.js
```

Expected stdout (example):

```JSON theme={null}
{"result":{"content":[{"type":"text","text":"8"}],"jsonrpc":"2.0","id":1}
```

## Test with Postman

Postman supports MCP-style workflows and can invoke stdio transports or HTTP transports depending on how the client and server are configured.

* Create a new request in Postman.
* Choose the stdio transport and point it to the `node server.js` command (or the path to the executable).
* Send a `tools/list` request to inspect the catalog and input schema.
* Send a `tools/call` request with:
  * `name: "add-integers"`
  * `arguments: { "a": 3, "b": 3 }`
* Postman will display the JSON-RPC responses similar to the command-line examples above.

<Callout icon="lightbulb">
  If you prefer HTTP transport for testing or integration, you can adapt the server to an HTTP transport or use a proxy that translates HTTP requests to stdio MCP messages.
</Callout>

## Recap and next steps

You now have a minimal, functioning MCP server in Node.js that:

* Exposes a tools catalog with structured input schemas.
* Implements tool execution with explicit input validation and clear error handling.
* Communicates over stdio in standard MCP JSON-RPC format.

Next ideas to extend this project:

* Add more tools (file operations, DB queries, external API calls).
* Return richer `content` types (JSON objects, structured results, or binary data via attachments).
* Add logging, metrics, and unit tests around the request handlers.

## Links and references

* Node.js — [https://nodejs.org/](https://nodejs.org/)
* Model Context Protocol SDK (npm) — [https://www.npmjs.com/package/@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
* JSON-RPC 2.0 spec — [https://www.jsonrpc.org/specification](https://www.jsonrpc.org/specification)

Thank you for following this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/a27f1996-5412-4f48-a085-c87d68c51206/lesson/d30edec1-a055-437f-82bc-18aadbcf3985" />
</CardGroup>
