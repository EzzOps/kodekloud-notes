# create and activate a venv
python3 -m venv venv
source venv/bin/activate

# install the markitdown MCP package
pip install markitdown-mcp

# run an HTTP MCP server on localhost:3001
markitdown-mcp --http --host 127.0.0.1 --port 3001
```

Typical startup logs (representative):

```text theme={null}
INFO: Waiting for application startup.
StreamableHTTP session manager started
Application started with StreamableHTTP session manager!
INFO: Application startup complete.
INFO: Uvicorn running on http://127.0.0.1:3001 (Press CTRL+C to quit)
```

Docker-based usage and CLI configuration

If you prefer Docker, the MarkItDown README includes Docker instructions. Example Claude desktop MCP server configuration (JSON) that runs the MCP server in Docker:

```json theme={null}
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "markitdown-mcp:latest"
      ]
    }
  }
}
```

If you need to mount a work directory into the container, include a `-v` bind mount:

```json theme={null}
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "/home/user/data:/workdir",
        "markitdown-mcp:latest"
      ]
    }
  }
}
```

Build and run the Docker image locally:

```bash theme={null}
# build
docker build -t markitdown-mcp:latest .

# run interactively
docker run -it --rm markitdown-mcp:latest

# run with a mounted workdir
docker run -it --rm -v /home/user/data:/workdir markitdown-mcp:latest
```

Add a custom connector in Claude

1. Start your MCP server (example: `http://127.0.0.1:3001`).
2. In Claude go to Tools → Add connectors → Add custom connector.
3. Enter the MCP HTTP endpoint. Typical endpoints:
   * Streamable HTTP: `http://127.0.0.1:3001/mcp`
   * SSE: `http://127.0.0.1:3001/sse`
4. Confirm you trust the connector when prompted.

Once connected, upload a file in Claude and ask it to "Convert to Markdown." Claude will call your MCP server, which returns the converted Markdown content.

<Callout icon="lightbulb">
  When adding a custom connector pointing to a local server, verify the MCP service is reachable at the URL you provide (correct host, port, and path). If you run behind a firewall or use a different network interface, update the host accordingly.
</Callout>

Inspector and developer tools

* Model Context Protocol (MCP) Inspector (npm): run `npx @modelcontextprotocol/inspector` and open `http://localhost:5173/` to inspect MCP traffic.
* Useful for debugging request/response flows, session management, and events.

Connector types you may encounter

| Connector Type            |                                             Description | Typical Endpoint / Example  |
| ------------------------- | ------------------------------------------------------: | --------------------------- |
| STDIO-backed MCP servers  |           Local processes invoked by the desktop client | N/A (process-level)         |
| Streamable HTTP endpoints |      HTTP endpoints supporting Streamable HTTP sessions | `http://127.0.0.1:3001/mcp` |
| SSE endpoints             | Server-Sent Events endpoints used for streaming updates | `http://127.0.0.1:3001/sse` |

Deployment and operational suggestions

| Goal                       | Recommendation                                                                               |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| Keep services up long-term | Run MCP servers as background services (systemd, launchd)                                    |
| Isolate dependencies       | Run MCP servers in Docker containers                                                         |
| Team/internal access       | Host MCP servers on an internal network, or expose public endpoints only after securing them |

<Callout icon="warning">
  Do not expose MCP endpoints publicly unless you understand and have implemented proper authentication, TLS, and access controls. Exposing local connectors without protection can leak sensitive data.
</Callout>

Troubleshooting checklist

* Is the MCP server running? Check logs for successful startup.
* Is the URL/path correct? Confirm whether the server expects `/mcp` (Streamable HTTP) or `/sse`.
* Is the host reachable from the machine running Claude? Replace `127.0.0.1` with the machine's IP if necessary for networked setups.
* Use the MCP Inspector to view session traffic and errors.

Conclusion

Claude integrates with many web and desktop connectors by default. When a connector isn’t available, you can implement a custom MCP server—locally, on your network, or in Docker—and register it as a custom connector in Claude to perform tasks such as converting documents to Markdown. Community registries list many community MCP servers you can adapt or reuse.

Links and references

* Claude: [https://claude.ai](https://claude.ai)
* Model Context Protocol Inspector (npm): [https://www.npmjs.com/package/@modelcontextprotocol/inspector](https://www.npmjs.com/package/@modelcontextprotocol/inspector)
* OpenTools (community registries): [https://opentools.com](https://opentools.com)
* Docker: [https://www.docker.com](https://www.docker.com)
* Python venv: [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/910a0b7a-ac6e-43f1-956e-203a70c3d455/lesson/4410741d-0261-4a26-a421-687e357f3cc6" />
</CardGroup>


# Demo Creating a Resource in Terraform

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Leveraging-MCP-for-Daily-Work/Demo-Creating-a-Resource-in-Terraform/page

Guide demonstrating how to run Terraform via the tfmcp MCP bridge using JSON-RPC over stdio to plan and apply a simple local file resource, including setup and security notes

This guide shows how to run Terraform operations through an MCP (Message Control Plane) server using the Terraform MCP bridge (`tfmcp`). You will learn to initialize a Terraform workspace, plan and apply a simple configuration that creates a local file — all triggered by MCP-style JSON-RPC calls (stdio). This workflow is useful when you want programmatic, message-driven control of Terraform from agents, automation pipelines, or AI assistants that already speak MCP/JSON-RPC.

## Prerequisites (Ubuntu)

Install the required system packages, Rust toolchain, and the Terraform MCP bridge. The following table summarizes the key prerequisites and where to find them.

| Requirement          | Purpose                                         | Install / Reference                                     |
| -------------------- | ----------------------------------------------- | ------------------------------------------------------- |
| build tools          | Compile native dependencies                     | See the command below                                   |
| Rust (rustup)        | Build the `tfmcp` crate                         | See the command below                                   |
| Terraform MCP bridge | Runs the MCP server and handles Terraform calls | `cargo install tf-mcp` or `cargo install terraform-mcp` |

Install the build tools:

```bash theme={null}
sudo apt-get update
sudo apt-get install -y build-essential
```

Install Rust via rustup:

```bash theme={null}
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
