# Global install (may require sudo)
sudo npm install -g @nextdrive/github-action-trigger-mcp

# Or run it via npx (no global install required)
npx -y @nextdrive/github-action-trigger-mcp
```

Package: [https://www.npmjs.com/package/@nextdrive/github-action-trigger-mcp](https://www.npmjs.com/package/@nextdrive/github-action-trigger-mcp)

## 4) Configure authentication (GitHub Personal Access Token)

The MCP server needs a GitHub Personal Access Token (PAT) with the correct permissions to trigger workflows. Export the token into your environment before starting the MCP server or include it in your host configuration:

```bash theme={null}
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

Recommended scopes/permissions:

| Token type       | Required scopes / permissions                                     |
| ---------------- | ----------------------------------------------------------------- |
| Classic PAT      | `repo` (private repos) or `public_repo` (public) and `workflow`   |
| Fine‑grained PAT | Actions (Read & Write) or equivalent for workflows                |
| Alternative      | Use GitHub Apps or OIDC where possible to avoid long‑lived tokens |

> **warning** Store and manage PATs securely. Do not commit tokens to source control. Use secrets managers or environment variables with least privilege and proper access controls.

For more on PATs and security: [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## 5) Add the MCP server to your Claude/host configuration

Add an MCP server entry so your host can start and connect to it. Example `mcpServers` JSON snippet for the host configuration:

```json theme={null}
{
  "mcpServers": {
    "google-calendar": {
      "command": "npx",
      "args": ["@cocal/google-calendar-mcp"],
      "env": {
        "GOOGLE_OAUTH_CREDENTIALS": "/Users/jeremy/demos/mcpstuff/google-calendar-mcp/credentials.json"
      }
    },
    "github-action-trigger-mcp": {
      "command": "npx",
      "args": ["-y", "@nextdrive/github-action-trigger-mcp"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": ""
      }
    }
  }
}
```

Fill `GITHUB_PERSONAL_ACCESS_TOKEN` with your token or ensure the environment variable is set for the running process. See your host/Claude docs for exact config file location and syntax.

## 6) Start the MCP server and authorize the client

* Start the host/Claude application (or the MCP directly via npx) and ensure `github-action-trigger-mcp` appears in the tools/services list.
* When the LLM client requests the tool, grant access (for example, “Allow always”) so the client can call the MCP.
* When asked for repository context, provide the owner and repo (for example: `jeremymorgan/turbo-broccoli`).

The MCP will query GitHub for available workflows and present them to the client.

## 7) Trigger a workflow via the MCP server

To trigger a workflow manually, provide the payload that includes the repository, workflow identifier, and the ref (branch or SHA). Example request payload:

```json theme={null}
{
  "owner": "jeremymorgan",
  "repo": "turbo-broccoli",
  "workflow_id": "azure-static-web-apps-black-rock-02284341e.yml",
  "ref": "main"
}
```

Notes:

* `workflow_id` may be the workflow file name, the numeric workflow id, or the workflow name depending on the API/MCP implementation.
* Many implementations accept optional `inputs` for `workflow_dispatch` inputs.

Example success response:

```json theme={null}
{
  "success": true,
  "message": "Workflow triggered successfully",
  "run_id": 123456789,
  "triggered_by": "jeremymorgan"
}
```

After triggering, open the GitHub Actions UI to view the run, logs, and deployment progress. In this demo the run redeploys the site to Azure Static Web Apps.

## 8) Next steps and possibilities

* Extend this pattern to trigger different workflows, pass inputs, or orchestrate multiple workflows across repositories.
* Use other MCP servers that expose Git commands, cloud provider APIs, or infra actions to build more sophisticated LLM-driven automation.
* Always evaluate security: prefer short‑lived credentials (OIDC, GitHub Apps) and minimize granted scopes.

This lesson demonstrated wiring an MCP server to GitHub Actions, configuring authentication with a PAT, adding the MCP to your host/Claude setup, and triggering a workflow. The pattern generalizes to other CI/CD platforms and MCP implementations.

## Links and references

* [GitHub Actions docs](https://docs.github.com/en/actions)
* [Vite docs](https://vitejs.dev/)
* [Azure Static Web Apps documentation](https://learn.microsoft.com/azure/static-web-apps/)
* [@nextdrive/github-action-trigger-mcp on npm](https://www.npmjs.com/package/@nextdrive/github-action-trigger-mcp)

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/910a0b7a-ac6e-43f1-956e-203a70c3d455/lesson/9a8d29b5-a1e1-4ae4-8628-8dd95e68f2a8)


# Where to Find MCP Servers

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Leveraging-MCP-for-Daily-Work/Where-to-Find-MCP-Servers/page

Guide to discovering, using, and bridging production and community MCP servers, catalogs, integrations, and tools for local and remote orchestration with clients

Now that you’ve learned how to run and compose MCP servers locally and remotely, connect them to Claude or CLI clients, and use them to orchestrate APIs and services, here’s a curated set of places to discover production-ready and community MCP servers you can use, extend, or remix.

Use this guide to find:

* ready-made MCP integrations for common platforms (Asana, GitHub, Supabase, etc.),
* community examples and tutorials,
* curated catalogs and registries,
* and tools to bridge remote MCP endpoints to local STDIO clients.

## Popular MCP Server Sources

1. Postman Explore — MCP Generator

* My top recommendation is the Postman Explore collection at [https://postman.com/explore/MCP-generator](https://postman.com/explore/MCP-generator). It hosts hundreds of published MCP server collections you can inspect, remix, and generate locally.
* These collections are ideal for experimentation: combine parts of a public API collection (e.g., PayPal) with other services (Amadeus, Discord) to generate a single MCP server that runs on your machine. That makes it possible to orchestrate workflows (initiate a payment, post to a channel, and save a record) using natural language.

2. OpenTools Registry — Official Integrations

* The OpenTools registry at [https://opentools.com/registry](https://opentools.com/registry) lists production-grade MCP integrations maintained by platform vendors and companies. You’ll find integrations for services such as Asana with endpoints like `get_attachments`, `get_goals`, `create_goal`, and more.
* Remember: MCP provides a standardized protocol to describe and interact with APIs, object stores (S3), monitoring dashboards (Grafana), and other systems via a consistent interface.

<Frame>
  <img alt="A screenshot of a browser window open to the OpenTools registry, showing a table of Asana API endpoints and their parameter descriptions (e.g., asana_get_goals, asana_get_goal, asana_create_goal). A large white page area with a visible mouse cursor is also shown." />
</Frame>

3. PulseMCP Server Directory

* Find a catalog of MCP servers, release metadata, and usage metrics at [https://pulsemcp.com/servers](https://pulsemcp.com/servers). Each entry typically includes classification, weekly downloads, and release dates to help you choose stable or trending servers.

<Frame>
  <img alt="Screenshot of a webpage showing the MCP Server Directory with entries like &#x22;Fetch,&#x22; &#x22;GitHub,&#x22; &#x22;Toolbox for Databases,&#x22; and &#x22;Time.&#x22; Each card lists classification, estimated weekly downloads, and release date." />
</Frame>

4. Smithery.ai — Curated Integrations

* [https://smithery.ai](https://smithery.ai) offers a curated catalog of integrations with ready-to-use MCP servers (Supabase, GitHub, GitLab merge requests, weather APIs, and more). It’s a good place to find polished integrations and examples for common workflows.

<Frame>
  <img alt="A dark-themed webpage (smithery.ai) showing a catalog of integration/API cards organized under headings like &#x22;Code Repository Management&#x22; and &#x22;Weather Data APIs.&#x22; Each card lists services such as GitHub, GitLab Merge Request, Weather MCP Server, and United States Weather with brief descriptions and tags." />
</Frame>

5. Awesome MCP Servers (GitHub)

* The community-maintained list at [https://github.com/punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) aggregates many MCP servers, clients, tutorials, and related resources. Use it to discover community-contributed servers and learning material.

<Frame>
  <img alt="A dark-themed browser screenshot of a GitHub README titled about MCP (Model Context Protocol), showing sections like &#x22;What is MCP?&#x22;, &#x22;Clients&#x22;, and &#x22;Tutorials&#x22; with links. A large white mouse cursor is visible on the left." />
</Frame>

Table — Quick resource summary

| Resource                        | Best for                                                | Link                                                                                   |
| ------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Postman Explore — MCP Generator | Rapidly generate local MCP servers from API collections | [https://postman.com/explore/MCP-generator](https://postman.com/explore/MCP-generator) |
| OpenTools registry              | Production-grade, vendor-maintained integrations        | [https://opentools.com/registry](https://opentools.com/registry)                       |
| PulseMCP Server Directory       | Browse server metadata & download stats                 | [https://pulsemcp.com/servers](https://pulsemcp.com/servers)                           |
| Smithery.ai                     | Curated integration catalog for common services         | [https://smithery.ai](https://smithery.ai)                                             |
| Awesome MCP Servers (GitHub)    | Community examples, clients, and tutorials              | `https://github.com/punkpeye/awesome-mcp-servers`                                      |

## MCP Remote — Exposing Remote Servers to STDIO Clients

If you have a client that only supports local STDIO MCP servers (for example, certain desktop apps) but you want to connect it to a remote, authenticated MCP server, the mcp-remote bridge proxies a remote SSE/HTTP MCP endpoint to a local STDIO-style server. This lets legacy or local-only clients connect to a remote MCP endpoint as if it were running locally.

> **lightbulb** mcp-remote is very helpful when bridging remote MCP endpoints to local clients but can be experimental in some ecosystems. Pay attention to authentication, TLS, and network security when exposing remote services locally.

Example client config (JSON snippet that launches the proxy via `npx`):

```json theme={null}
{
  "mcpServers": {
    "remote-example": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://remote.mcp.server/sse"
      ]
    }
  }
}
```

Install the mcp-remote package:

```bash theme={null}
