# Workspace API Keys
HACKER_NEWS_API_API_KEY=
DISCORD_API_API_KEY=
```

Inside each tool file the code will reference environment variables, for example:

```javascript theme={null}
// environment variables are used inside of each tool file
const apiKey = process.env.ACME_API_KEY;
```

Make sure to populate `.env` with any API keys or secrets before starting the server.

## 4 — Run the MCP server locally

From the project directory you can run the server directly:

```bash theme={null}
node mcpServer.js
```

When integrating the server with a tool host you may need absolute paths and the full Node executable path. Useful commands:

```bash theme={null}
which node
node --version
realpath mcpServer.js
```

Example output you might see after `npm install`:

```text theme={null}
added 90 packages, and audited 91 packages in 2s
18 packages are looking for funding
run `npm fund` for details

found 0 vulnerabilities
```

## 5 — MCP request and tool discovery

With the MCP server running, it will expose the configured tools. A typical MCP request to fetch a single Hacker News story looks like this:

```json theme={null}
{
  "method": "tools/call",
  "params": {
    "name": "get_story",
    "arguments": {
      "itemId": "44628930"
    }
  }
}
```

To integrate with an LLM host or tool manager, configure a tool entry that runs the Node executable and passes the `mcpServer.js` path as an argument. Use the `which node` and `realpath mcpServer.js` outputs to fill in the command and arguments in your host configuration.

Example host configuration (conceptual):

* Command: `/usr/local/bin/node`
* Arguments: `/full/path/to/postman-mcp-server/mcpServer.js`

After restarting your host, the new MCP tools (for example, Hacker News — Fetch Top Stories and Get Story) should appear in the host’s tool list. You can then call tools via MCP — for instance, request Top Stories to get story IDs, then call Get Story with a chosen `itemId`.

> **lightbulb** You can run the generated MCP server locally (or in Docker). The Postman MCP generator currently produces local servers — it does not publish a remotely reachable server for you. If you need a remote endpoint, deploy the generated project to your preferred hosting environment or container platform.

## 6 — End-to-end checklist

1. Use Postman’s MCP generator to select APIs and generate a project.
2. Download and unzip the generated project.
3. Inspect and optionally edit `mcpServer.js`, `index.js`, and individual tool files.
4. Create or populate `.env` with required API keys and secrets.
5. Run `npm install`, then start the server with `node mcpServer.js` (or build and run via Docker).
6. Point your LLM/tool host to the Node command and the `mcpServer.js` path; restart the host to discover tools.
7. Call tools via MCP (e.g., fetch top stories, then fetch individual stories by `itemId`).

## Links and references

* Postman MCP Generator: [https://www.postman.com/explore/MCP-generator](https://www.postman.com/explore/MCP-generator)
* Hacker News API: [https://github.com/HackerNews/API](https://github.com/HackerNews/API)

This workflow makes it simple to expose curated Postman endpoints as MCP tools so local LLMs and tool hosts can call them directly.

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/910a0b7a-ac6e-43f1-956e-203a70c3d455/lesson/6e2f5927-e7a6-43b8-829c-9b2483fc6394)


# Demo Claude Integration with MCP

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Leveraging-MCP-for-Daily-Work/Demo-Claude-Integration-with-MCP/page

Guide to connecting Claude to MCP servers and desktop extensions, adding custom connectors, running MarkItDown to convert files to Markdown, and deployment and debugging tips

We already built MCP servers and a local server integrated with Claude successfully. This guide shows additional ways to connect Claude to MCP (Model Context Protocol) servers so you can automate day-to-day workflows — for example, converting documents to Markdown with a local connector.

Claude advertises that it "works with your favorite tools." From the Claude UI you can add connectors (Gmail, Google Drive, Linear, Square, Stripe, Zapier, and more) and grant the assistant access to reference or act on context from those apps.

<Frame>
  <img alt="A dark-mode desktop screenshot showing a &#x22;Connectors&#x22; dialog listing web integrations (Asana, Atlassian, Canva, Gmail, Google Drive, etc.) inside an app window. A large white mouse cursor is visible and the dialog is over a blue-themed code editor/IDE background." />
</Frame>

Claude also supports Desktop Extensions (local processes) that behave similarly to web connectors. The key distinction is:

* Web connectors → hosted HTTP MCP servers (accessible via URL).
* Desktop extensions → local processes running on your machine.

<Frame>
  <img alt="A computer screenshot showing a &#x22;Connectors&#x22; settings window (Desktop extensions tab) listing connector plugins like PDF Filler, Spotify (AppleScript), Stripe, and various MCP servers. The dialog is over a dark-blue desktop background with a partially visible Spotify app on the right." />
</Frame>

If a connector you need isn't listed, you can add a custom connector and point Claude to any MCP-compatible HTTP endpoint (local, on your network, or public).

Example: MarkItDown — a lightweight MCP server that converts documents to Markdown. You can install and run it locally (recommended inside a Python virtual environment) or run it in Docker.

Quick local install and run (recommended inside a venv)

```bash theme={null}
