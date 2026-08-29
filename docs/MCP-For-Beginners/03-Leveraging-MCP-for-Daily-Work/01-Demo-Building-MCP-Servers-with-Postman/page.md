# Example project directory contents
cd code/
ls
# main.py
```

## Core concepts and connection methods

After the basics you'll dive deeper into running MCP servers locally and the connection options available:

| Connection Method | When to use                               | Pros                                                      | Cons                                                 |
| ----------------- | ----------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------- |
| `stdio`           | Local development, single-process testing | Simple, no HTTP server required; good for quick iteration | Limited visibility, not ideal for remote deployment  |
| `HTTP`            | Production or multi-process deployments   | Standard web tooling, easier to test with Postman and CI  | Requires server setup and more robust error handling |

Hands-on labs will guide you through both methods and best practices for testing and debugging.

## Leveraging MCP in daily workflows

This course shows concrete examples of integrating MCP with tools and platforms developers use every day:

* Claude (Anthropic) for advanced LLMs: [Claude](https://www.anthropic.com/product/claude)
* Google Calendar for scheduling and event lookups: [Google Calendar](https://calendar.google.com/)
* Postman for testing HTTP-connected MCP servers: [Postman](https://www.postman.com/)
* CI/CD and GitHub Actions for automated tests and deployments: [GitHub Actions](https://docs.github.com/en/actions)
* Terraform for provisioning cloud resources as triggers or data sources: [Terraform](https://www.terraform.io/)

Example: local JSON configuration showing how you might reference a Google Calendar MCP adapter and a GitHub Action trigger:

```json theme={null}
{
  "args": ["@cocal/google-calendar-mcp"],
  "env": {
    "GOOGLE_OAUTH_CREDENTIALS": "/Users/jeremy/demos/mcpstuff/google-calendar-mcp/credentials.json"
  },
  "github-action-trigger-mcp": {
    "command": "npx",
    "args": ["-y", "@nextdrive/github-action-trigger-mcp"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": ""
    }
  }
}
```

> **warning** Never commit credentials or OAuth files to source control. Store sensitive values in secure stores or CI secrets and reference them via environment variables.

## Example lab flow (high level)

1. Run the Weather tool locally and observe the model calling the tool.
2. Build a minimal MCP server that accepts tool requests and returns structured responses.
3. Switch connection modes (stdio → HTTP) and validate behavior with Postman or curl.
4. Add authentication and secure credentials using environment variables or secret managers.
5. Integrate a third-party adapter (e.g., Google Calendar) and test end-to-end.

## Community and support

At KodeKloud we encourage collaboration—ask questions, share discoveries, and learn with others in the forums and resource hubs. These channels are ideal for getting help, exchanging MCP patterns, and finding real-world examples you can adapt.

<Frame>
  <img alt="A screenshot of the KodeKloud community/forum page showing categories in a left sidebar and discussion threads on the right. A small circular video overlay of a person appears in the lower-right corner." />
</Frame>

## Links and references

* MCP best practices and protocol patterns (covered in course labs)
* [Claude (Anthropic)](https://www.anthropic.com/product/claude)
* [Google Calendar](https://calendar.google.com/)
* [Postman](https://www.postman.com/)
* [Terraform](https://www.terraform.io/)
* [GitHub Actions](https://docs.github.com/en/actions)

Let's dive in and unlock the full potential of the Model Context Protocol.

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/aec3d24f-fc96-42cb-802f-f6d39e4923f1/lesson/f28709cc-c5b1-4492-b8ae-f164647b7d4c)


# Demo Building MCP Servers with Postman

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Leveraging-MCP-for-Daily-Work/Demo-Building-MCP-Servers-with-Postman/page

How to generate, inspect, run, and integrate a local MCP server from a Postman collection to expose APIs like Hacker News to LLMs and tool hosts.

Use the Postman MCP Server Generator to turn a Postman collection into a small local MCP server that exposes the APIs and tools you select. This lets a local LLM or tool host call those endpoints via the MCP protocol. In this demo we use the Hacker News API as an example because it requires no API key and is easy to test.

What you'll learn:

* How to generate a local MCP server from a Postman collection
* How to inspect the generated Node.js project and its files
* How to install dependencies, provide environment variables, and run the server
* How to point an LLM/tool host at the local MCP server so it discovers tools

<Frame>
  <img alt="A dark-themed screenshot of the Postman web interface showing search results for &#x22;HackerNews&#x22; with multiple API/collection entries (e.g., Hacker News API, Brewing Postman Flows, Slack Integration Flows). A mouse cursor is visible hovering over one of the results." />
</Frame>

## 1 — Pick a Postman collection and generate the project

Open the Postman MCP generator at postman.com/explore/mcp-generator, choose the Hacker News API collection (or any collection you control), and select the requests you want exposed via the MCP server. Typical Hacker News endpoints you might include are:

```http theme={null}
GET {{url}}/v0/beststories.json?print=pretty
GET {{url}}/v0/newstories.json?print=pretty
GET {{url}}/v0/topstories.json?print=pretty
GET https://hacker-news.firebaseio.com/v0/item/{{item-id}}.json?print=pretty
```

Click Generate. Postman will produce a ZIP containing a small Node.js project that implements an MCP server. The generator supports including tools from multiple APIs in one process — for example, you could include both Hacker News and Discord tools together.

## 2 — Inspect the generated project

Unzip the download and open the folder in your editor (Visual Studio Code is shown below). The generator produces a focused project you can review and modify before running.

<Frame>
  <img alt="A screenshot of Visual Studio Code with the Explorer sidebar open for a project named &#x22;postman-mcp-server,&#x22; showing files like index.js, mcpServer.js, package.json and a Dockerfile. The main editor area is empty with a large VS Code logo and quick‑command hints on a dark blue background." />
</Frame>

Typical files in a generated project:

| File           | Purpose                                                           |
| -------------- | ----------------------------------------------------------------- |
| `index.js`     | Small CLI helper — e.g., list tools or run a single tool          |
| `mcpServer.js` | MCP server entrypoint — the process that listens for MCP requests |
| `package.json` | Project metadata and dependency list                              |
| `Dockerfile`   | Optional containerization and runtime instructions                |
| `README.md`    | Setup, environment variable examples, and usage notes             |

Example Dockerfile included with the generator:

```dockerfile theme={null}
FROM node:22.12-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

COPY . .

ENTRYPOINT ["node", "mcpServer.js"]
```

A cleaned and typical `package.json` (the generator may include additional fields):

```json theme={null}
{
  "name": "postman-mcp-generator-mcp",
  "version": "1.0.0",
  "description": "A simple MCP server with packaged tools",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "list-tools": "node index.js tools"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.9.0",
    "commander": "^13.1.0",
    "dotenv": "^16.4.7",
    "express": "^5.1.0"
  },
  "engines": {
    "node": ">=16.0.0"
  },
  "author": "Postman, Inc.",
  "license": "MIT"
}
```

## 3 — Install dependencies and configure secrets

Read the included README for exact setup details. In short, from the project root:

```bash theme={null}
npm install
```

The generator typically provides a sample `.env` or documents the environment variables required by each workspace/tool. Example `.env` entries:

```env theme={null}
