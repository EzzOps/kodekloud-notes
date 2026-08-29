# Demo Trigger a CICD Workflow via MCP

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Leveraging-MCP-for-Daily-Work/Demo-Trigger-a-CICD-Workflow-via-MCP/page

Demo showing how to use an MCP server to trigger GitHub Actions workflows from an LLM client, covering setup, authentication, and workflow dispatch.

In this lesson you'll learn how to use an MCP server as a bridge to trigger a CI/CD workflow (GitHub Actions) from an LLM-enabled client. We'll:

* Run a local Vite dev server that hosts the Turbo Broccoli site.
* Install and run an MCP server that calls the GitHub Actions API.
* Configure authentication (GitHub Personal Access Token).
* Add the MCP server to your host/Claude configuration.
* Trigger a workflow and inspect the result in GitHub Actions.

<Frame>
  <img alt="A presentation slide that reads &#x22;Trigger a CI/CD Workflow via MCP&#x22; with a large &#x22;Demo&#x22; label on a dark curved shape. A small &#x22;© Copyright KodeKloud&#x22; appears in the lower-left." />
</Frame>

Overview:

* The MCP server acts as a bridge to a CI/CD platform (GitHub Actions in this example).
* The client (an LLM client such as [Claude](https://www.anthropic.com/claude)) runs inside your AI-enabled app/IDE and calls the MCP server for Actions operations.
* The host application is the UI you interact with (for example, the Claude desktop app).

## 1) Run the Vite site locally

Start the local dev server in your Turbo Broccoli project directory:

```bash theme={null}
jeremy@MACSTUDIO turbo-broccoli % npm run dev
```

You should see output similar to:

```text theme={null}
> vue-splash@0.0.0 dev
> vite

12:25:32 AM [vite] (client) Re-optimizing dependencies because vite config has changed
VITE v7.0.5 ready in 299 ms
→  Local:   http://localhost:5173/
→  Network: use --host to expose
press h + enter to show help
```

This serves the site at `http://localhost:5173/` so you can validate changes before or after triggering CI/CD. (See Vite docs: [https://vitejs.dev/](https://vitejs.dev/))

## 2) GitHub Actions workflow (what we will trigger)

The repo uses an Azure Static Web Apps CI/CD workflow implemented with GitHub Actions. The workflow runs on pushes to `main`, PR updates, or manual dispatch.

Example workflow header and a build job:

```yaml theme={null}
name: Azure Static Web Apps CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v3
        with:
          # additional configuration here
```

Quick reference — common workflow trigger types:

| Trigger type        | When it runs           | Typical use                        |
| ------------------- | ---------------------- | ---------------------------------- |
| `push` to branch    | On commit push         | Auto-build & deploy on main branch |
| `pull_request`      | On PR open/update      | Validate changes via CI            |
| `workflow_dispatch` | Manual dispatch or API | Manual redeploys or ad-hoc runs    |

Note: A `workflow_dispatch` can accept `inputs` which you may pass via the MCP server when triggering.

## 3) Install the GitHub Actions trigger MCP server

Install (or run via npx) the MCP package that exposes GitHub Actions operations:

```bash theme={null}
