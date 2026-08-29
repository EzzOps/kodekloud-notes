# Demo Prompts in MCP Servers

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Leveraging-MCP-for-Daily-Work/Demo-Prompts-in-MCP-Servers/page

Guide to building a minimal JavaScript MCP server that registers versioned prompts, forwards prompt text to a local Ollama instance, and demonstrates testing with an MCP Inspector

This lesson walks through building a minimal MCP (Model Context Protocol) server in JavaScript that:

* Stores prompts as JSON files (trackable in Git)
* Registers prompts with an MCP server
* Forwards prompt text to a local Ollama instance via its HTTP API
* Provides a lightweight demo harness and shows how to test with the MCP Inspector

Contents:

* Prompt file examples
* Project setup and dependencies
* Server implementation (`server.js`)
* Using the MCP Inspector
* Demo harness (`simple-demo.js`)
* Sample output and best practices

## Prompt files (examples)

Store each prompt as a separate JSON file under a `prompts/` directory. This makes prompts easy to version and reuse.

Summary of the example prompts:

| Prompt ID         | Title                 | Purpose                                    |
| ----------------- | --------------------- | ------------------------------------------ |
| `greeting`        | Personalized Greeting | Produces a simple personalized message     |
| `explain-concept` | Concept Explainer     | Explains concepts for a specified audience |
| `code-review`     | Code Review           | Reviews code and provides suggestions      |

Example: greetings.json

```json theme={null}
{
  "id": "greeting",
  "title": "Personalized Greeting",
  "description": "Creates a greeting using the user's name.",
  "template": "Hello, {{name}}! Welcome to our MCP prompt demo.",
  "variables": [
    { "name": "name", "description": "The recipient's name" }
  ]
}
```

Example: explain-concept.json

```json theme={null}
{
  "id": "explain-concept",
  "title": "Concept Explainer",
  "description": "Explains complex concepts in simple terms.",
  "template": "Please explain {{concept}} in simple terms that a {{audience}} could understand. Use examples and analogies where appropriate.",
  "variables": [
    { "name": "concept", "description": "The concept to be explained" },
    { "name": "audience", "description": "The target audience (e.g., 'beginner', '10-year-old', 'college student')" }
  ]
}
```

Example: code-review\.json

````json theme={null}
{
  "id": "code-review",
  "title": "Code Review",
  "description": "Reviews code and suggests improvements.",
  "template": "Please review the following JavaScript code and provide suggestions for improvement:\n\n```javascript\n{{code}}\n```\n\nPlease focus on:\n- Code quality and best practices\n- Performance optimizations\n- Security considerations\n- Readability and maintainability",
  "variables": [
    { "name": "code", "description": "The JavaScript code to review" }
  ]
}
````

## Setup — node project and dependencies

Initialize the project and install the libraries used in this example:

```sh theme={null}
npm init -y
npm install @modelcontextprotocol/sdk zod node-fetch
```

Notes:

* Depending on your Node version, `fetch` may already be available globally. This guide uses `node-fetch` to keep compatibility across Node releases.
* References:
  * MCP SDK: [https://www.npmjs.com/package/@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
  * Zod: [https://www.npmjs.com/package/zod](https://www.npmjs.com/package/zod)
  * node-fetch: [https://www.npmjs.com/package/node-fetch](https://www.npmjs.com/package/node-fetch)

> **lightbulb** If you see a warning about "Module type of file ... is not specified", add `"type": "module"` to your `package.json` to explicitly enable ESM and avoid reparsing warnings.

## Server implementation (server.js)

This server does the following:

* Registers three prompts (`greeting`, `explain-concept`, `code-review`) with an MCP server
* Sends prompt text to a local Ollama server using the Ollama HTTP `generate` endpoint
* Starts a STDIO transport for MCP message exchange (common for MCP workflows)

Save the script below as `server.js` and run it with `node server.js`.

````javascript theme={null}
#!/usr/bin/env node

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import fetch from 'node-fetch';

const OLLAMA_BASE_URL = 'http://localhost:11434';
const DEFAULT_MODEL = 'llama3.2:3b';

// Send the prompt text to Ollama's /api/generate endpoint and return the text response.
async function sendToOllama(prompt, model = DEFAULT_MODEL) {
  try {
    const response = await fetch(`${OLLAMA_BASE_URL}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model, prompt, stream: false })
    });
    const result = await response.json();

    // Ollama response formats can vary; prefer common fields or fallback to stringifying the result.
    return result.response ?? result?.generations?.[0]?.text ?? JSON.stringify(result);
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

async function main() {
  const server = new McpServer({
    name: 'fixed-ollama-server',
    version: '1.0.0'
  });

  // Register "greeting" prompt
  server.registerPrompt(
    'greeting',
    {
      title: 'Personalized Greeting',
      description: 'Creates a personalized greeting'
    },
    // handler receives optional parameters when clients invoke this prompt
    async (params = {}) => {
      const name = params.name ?? 'Alice';
      const promptText = `Hello, ${name}! Welcome to our MCP prompt demo.`;
      const responseText = await sendToOllama(promptText);
      return {
        messages: [
          { role: 'user', content: { type: 'text', text: promptText } },
          { role: 'assistant', content: { type: 'text', text: responseText } }
        ]
      };
    }
  );

  // Register "explain-concept" prompt
  server.registerPrompt(
    'explain-concept',
    {
      title: 'Concept Explainer',
      description: 'Explains complex concepts simply'
    },
    async (params = {}) => {
      const concept = params.concept ?? 'quantum computing';
      const audience = params.audience ?? 'beginner';
      const promptText = `Please explain ${concept} in simple terms that a ${audience} could understand. Use examples and analogies where appropriate.`;
      const responseText = await sendToOllama(promptText);
      return {
        messages: [
          { role: 'user', content: { type: 'text', text: promptText } },
          { role: 'assistant', content: { type: 'text', text: responseText } }
        ]
      };
    }
  );

  // Register "code-review" prompt
  server.registerPrompt(
    'code-review',
    {
      title: 'Code Review',
      description: 'Provides suggestions for improving code'
    },
    async (params = {}) => {
      const code = params.code ?? 'function hello() { console.log("hi") }';
      const promptText = [
        'Please review the following javascript code and provide suggestions for improvement:',
        '```javascript',
        code,
        '```',
        '',
        'Please focus on:',
        '- Code quality and best practices',
        '- Performance optimizations',
        '- Security considerations',
        '- Readability and maintainability'
      ].join('\n');
      const responseText = await sendToOllama(promptText);
      return {
        messages: [
          { role: 'user', content: { type: 'text', text: promptText } },
          { role: 'assistant', content: { type: 'text', text: responseText } }
        ]
      };
    }
  );

  // Start the STDIO transport so the MCP server can communicate via stdin/stdout
  const transport = new StdioServerTransport();
  try {
    await server.connect(transport);
    console.log('All prompts registered\nServer ready');
    // Keep the process running to service incoming MCP requests over stdio.
  } catch (err) {
    console.error('Server error', err);
    process.exit(1);
  }
}

main().catch((err) => {
  console.error('Fatal error', err);
  process.exit(1);
});
````

Key details:

* The server uses `sendToOllama()` to POST to `http://localhost:11434/api/generate`.
* Each `registerPrompt` call gives a prompt ID, metadata (title/description), and a handler that formats the final prompt text and returns a message bag.
* The server connects over STDIO via `StdioServerTransport` so it can be inspected or proxied by MCP tools.

## Using the MCP Inspector to test

The Model Context Protocol Inspector lets you inspect the prompts, tools, and resources your MCP server exposes.

Install/run:

```sh theme={null}
npx @modelcontextprotocol/inspector node server.js
```

Example inspector startup (trimmed):

```text theme={null}
Starting MCP inspector...
🔑 Proxy server listening on localhost:6277
🔑 Session token: <token>
Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth
All prompts registered
Server ready
```

Once connected, the Inspector UI will list your `greeting`, `explain-concept`, and `code-review` prompts. You can invoke them interactively.

## Simple demo harness (simple-demo.js)

This demo script spawns `server.js`, watches stdout until it sees `Server ready`, and then demonstrates how you might invoke prompts. The actual MCP invocation is left to the Inspector or an MCP client; this harness focuses on starting and verifying the server.

Save as `simple-demo.js`:

```javascript theme={null}
#!/usr/bin/env node

import { spawn } from 'child_process';

console.log('=== MCP Ollama Demo ===\nTesting multiple prompts with Ollama integration...\n');

async function startServer() {
  const serverProcess = spawn('node', ['server.js'], {
    cwd: process.cwd(),
    stdio: ['pipe', 'pipe', 'inherit']
  });

  return new Promise((resolve, reject) => {
    serverProcess.stdout.setEncoding('utf8');

    serverProcess.stdout.on('data', (chunk) => {
      const output = chunk.toString();
      process.stdout.write(output);

      if (output.includes('Server ready')) {
        resolve(serverProcess);
      }
    });

    serverProcess.on('error', (err) => reject(err));
    serverProcess.on('exit', (code) => {
      if (code !== 0) {
        reject(new Error(`Server exited with code ${code}`));
      }
    });
  });
}

(async () => {
  try {
    const serverProcess = await startServer();
    console.log('✓ Server initialized');

    // At this point you can use the MCP Inspector or an MCP client to call prompts.
    // This harness intentionally leaves actual MCP calls out to avoid duplicating
    // a full JSON-RPC-over-stdio implementation here.

    // Cleanup: stop the server after a short delay (for demo purposes)
    setTimeout(() => {
      serverProcess.kill();
      console.log('\n=== Demo completed ===');
    }, 3000);
  } catch (err) {
    console.error('Demo error:', err);
  }
})();
```

## Sample run output (trimmed)

```text theme={null}
✅ All prompts registered
Server ready
✓ Server initialized
→ Sending prompt to Ollama...
✔ Got response from Ollama

RENDERED PROMPT:
Hello, Alice! Welcome to our MCP prompt demo.

OLLAMA RESPONSE:
*awkward smile* Oh, hi there... I'm not really sure what's going on or who you are, but I suppose I'll play along. What kind of demo is this? Is it some sort of... alternate history simulation? *nervous laugh*
```

## Notes and best practices

* Store prompt templates as files in a Git repo to gain version history, rollbacks, and collaboration.
* Document each prompt's template and variable schema (e.g., `variables` array) so clients know what to pass.
* For production servers, add:
  * Robust error handling and retries for downstream calls (Ollama)
  * Structured logging and metrics
  * Input validation (e.g., use `zod` or another validator) on prompt parameters
  * Rate limiting and authentication where appropriate
* If you hit Node module-type warnings, add `"type": "module"` to `package.json` to enable ESM.

## Links and references

* MCP SDK: [https://www.npmjs.com/package/@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
* MCP Inspector: [https://www.npmjs.com/package/@modelcontextprotocol/inspector](https://www.npmjs.com/package/@modelcontextprotocol/inspector)
* Ollama API docs: [https://ollama.ai/docs/api](https://ollama.ai/docs/api)
* Zod: [https://www.npmjs.com/package/zod](https://www.npmjs.com/package/zod)
* node-fetch: [https://www.npmjs.com/package/node-fetch](https://www.npmjs.com/package/node-fetch)

## Conclusion

This tutorial demonstrates registering reusable prompt definitions in an MCP server, forwarding prompt text to a local Ollama instance, and validating behavior with the MCP Inspector and a small demo harness. The approach enables shared, version-controlled prompt management across teams and services.

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/910a0b7a-ac6e-43f1-956e-203a70c3d455/lesson/1c9db747-2554-4fd8-94fe-ad357afe273f)
