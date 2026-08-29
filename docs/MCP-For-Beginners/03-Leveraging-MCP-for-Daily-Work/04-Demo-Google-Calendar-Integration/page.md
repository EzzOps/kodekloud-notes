# follow the prompts and add Rust to your PATH (typically by sourcing ~/.cargo/env)
source "$HOME/.cargo/env"
```

Install the Terraform MCP bridge (the binary is commonly named `tfmcp`):

```bash theme={null}
# Either of these may be available depending on the crate name/version
cargo install tf-mcp
# or
cargo install terraform-mcp
```

Cargo will download and compile crates during installation; when complete the `tfmcp` binary should be on your PATH.

## Start the MCP bridge / server

Start the MCP server so it can accept MCP-style requests over stdio in this demo:

```bash theme={null}
tfmcp mcp
```

The server will run in the foreground and listen for JSON-RPC messages on stdin/stdout.

## Create a sample Terraform project

Create a working directory and a minimal Terraform configuration that writes a local file.

Create the directory and enter it:

```bash theme={null}
mkdir terraform-demo
cd terraform-demo
```

Create `main.tf` with the following content:

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

provider "local" {}

resource "local_file" "example" {
  filename = "${path.module}/example.txt"
  content  = "Hello from tfmcp!"
}
```

Initialize and validate the workspace, then create a plan:

```bash theme={null}
terraform init
terraform validate
terraform plan
```

Sample (cleaned) plan output:

```text theme={null}
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_file.example will be created
  + resource "local_file" "example" {
      + content               = "Hello from tfmcp!"
      + filename              = "./example.txt"
      + directory_permission  = "0777"
      + file_permission       = "0777"
      + id                    = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

## Interact with the Terraform MCP server via JSON-RPC (stdio)

While `tfmcp mcp` is running in one terminal, send JSON-RPC messages from another terminal using a heredoc. The example sequence below performs:

1. An `initialize` request to the MCP server.
2. A `tools/call` request for `get_terraform_plan`.
3. A `tools/call` request for `apply_terraform` with `auto_approve=true`.

Send these requests via stdio:

```bash theme={null}
tfmcp mcp <<EOF
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_terraform_plan", "arguments": {}}}
{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "apply_terraform", "arguments": {"auto_approve": true}}}
EOF
```

For quick reference, common MCP tool calls used in this demo:

| Method                                 | Purpose                      | Example                                                                                                                |
| -------------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `initialize`                           | Prepare the MCP tool session | `{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}`                                                           |
| `tools/call` with `get_terraform_plan` | Request a Terraform plan     | `{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_terraform_plan","arguments":{}}}`                 |
| `tools/call` with `apply_terraform`    | Apply the Terraform plan     | `{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"apply_terraform","arguments":{"auto_approve":true}}}` |

Wrap any JSON examples containing curly braces in code blocks to avoid parsing issues (as done above).

## Security policy and auto-approve

By default the MCP bridge may block automated apply operations for safety. If auto-approve is blocked, you will see an error such as:

```json theme={null}
{
  "jsonrpc":"2.0",
  "id":3,
  "error":{
    "code":-32603,
    "message":"Failed to apply Terraform configuration: Auto-approve for apply operation blocked by security policy. Set TFMCP_ALLOW_AUTO_APPROVE=true to enable."
  }
}
```

> **lightbulb** Setting `TFMCP_ALLOW_AUTO_APPROVE=true` allows automated apply operations. Only enable this when you trust the Terraform configuration and understand the security implications.

If you decide to allow auto-approve, export the environment variable and re-run the JSON-RPC sequence:

```bash theme={null}
export TFMCP_ALLOW_AUTO_APPROVE=true

# Re-send the JSON-RPC sequence (initialize, plan, apply)
tfmcp mcp <<EOF
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_terraform_plan", "arguments": {}}}
{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "apply_terraform", "arguments": {"auto_approve": true}}}
EOF
```

## Successful apply and verification

When the apply completes, the MCP server will return the standard Terraform apply summary, for example:

```text theme={null}
local_file.example: Creation complete after 0s [id=<resource-id>]
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

Verify the created file:

```bash theme={null}
cat example.txt
# Output:
# Hello from tfmcp!
```

## Why use Terraform with MCP?

* Consistent control channel: If your orchestration or automation stack already uses MCP/JSON-RPC, adding Terraform as an MCP tool keeps infrastructure control within the same messaging paradigm.
* Programmatic integration: Enables other agents, CI/CD pipelines, or AI assistants to request Terraform operations programmatically without shelling out or managing separate APIs.
* Auditability & policy: An MCP gateway can centralize security checks, logging, and policy enforcement around Terraform operations.

## Troubleshooting tips

* Ensure `tfmcp` is on your PATH after `cargo install` (check `~/.cargo/bin`).
* If `terraform init` fails, review provider version constraints and network access to provider registries.
* If JSON-RPC messages are not being processed, confirm `tfmcp mcp` is running in the terminal where you expect it and that your heredoc is directed at the same `tfmcp` instance.

## Summary

* Installed the Terraform MCP bridge (`tfmcp`) and required toolchain.
* Created a simple Terraform configuration that writes a local file.
* Executed Terraform init/plan/apply through MCP JSON-RPC calls (stdio).
* Addressed auto-approve security via the `TFMCP_ALLOW_AUTO_APPROVE` environment variable.
* Verified the resulting resource and discussed reasons to use Terraform via MCP in automated systems.

## Links and references

* [Terraform](https://www.terraform.io)
* [JSON-RPC specification](https://www.jsonrpc.org/specification)
* [Rustup (install Rust)](https://rustup.rs)
* Terraform local provider: [https://registry.terraform.io/providers/hashicorp/local](https://registry.terraform.io/providers/hashicorp/local)

If you need an example for integrating this into a CI pipeline or automating the JSON-RPC calls programmatically (Python, Node, etc.), I can provide sample clients that interact with `tfmcp` via stdio.

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/910a0b7a-ac6e-43f1-956e-203a70c3d455/lesson/ebcb2c5e-7537-4c08-a561-8f09c05276c8)


# Demo Google Calendar Integration

Source: https://notes.kodekloud.com/docs/MCP-For-Beginners/Leveraging-MCP-for-Daily-Work/Demo-Google-Calendar-Integration/page

Guide to set up a local Google Calendar MCP server, configure OAuth, connect it to Claude Desktop, and enable the assistant to read and create calendar events.

This guide shows how to integrate a pre-built MCP (Model-Capability-Plugin) server for Google Calendar so a local assistant (Claude Desktop in this example) can read and create events using your Google account. Follow these high-level steps:

* Clone the MCP server repository
* Enable the Google Calendar API and configure OAuth consent
* Create OAuth credentials (Desktop app) and download the JSON
* Point the MCP server at your credentials and run it
* Add the MCP server to your Claude Desktop configuration
* Interact with your Google Calendar from Claude

## 1. Clone the repository

Open a terminal and clone the repo:

```bash theme={null}
git clone https://github.com/nspady/google-calendar-mcp.git
```

Example output on macOS:

```bash theme={null}
jeremy@MACSTUDIO mcpstuff % git clone https://github.com/nspady/google-calendar-mcp.git
```

## 2. Enable the Google Calendar API and configure OAuth

1. Open the Google Cloud Console — APIs Library: [https://console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)
2. Search for and enable the Google Calendar API: [https://developers.google.com/calendar](https://developers.google.com/calendar)
3. After enabling the API, go to APIs & Services → Credentials to configure OAuth: [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)

<Frame>
  <img alt="A screenshot of the Google Cloud Console &#x22;APIs & Services → Credentials&#x22; page showing API Keys and OAuth 2.0 client IDs. One Generative Language API key is listed, and the left sidebar and a code editor are visible in the background." />
</Frame>

## 3. Create an OAuth consent screen and client

1. Visit the OAuth consent screen: [https://console.cloud.google.com/apis/credentials/consent](https://console.cloud.google.com/apis/credentials/consent)
2. Set an app name (for example, "MCP calendar tool").
3. Choose the user type:
   * Internal — restricts use to your organization.
   * External — allows any Google account to authorize the app (typical for local personal use).
4. Provide contact info and save.

<Frame>
  <img alt="A browser window showing the Google Cloud Console &#x22;Project configuration&#x22; page with App Information and Audience options (Internal/External) selected. A dark-themed code editor/desktop is visible in the background." />
</Frame>

## 4. Create OAuth client credentials

1. Create an OAuth 2.0 Client ID and choose **Desktop app** as the application type: [https://developers.google.com/identity/protocols/oauth2](https://developers.google.com/identity/protocols/oauth2)
2. Click **Download JSON** for the client credentials and save the file locally.
3. Optionally rename the downloaded file to `credentials.json` (or another descriptive filename).

## 5. Set the GOOGLE\_OAUTH\_CREDENTIALS environment variable and start the MCP server

Export an environment variable pointing to the absolute path of your credentials file, then start the MCP server. Example:

```bash theme={null}
export GOOGLE_OAUTH_CREDENTIALS="/Users/jeremy/demos/mcpstuff/google-calendar-mcp/credentials.json"
npm run start
```

When the server starts, it will open a browser window asking you to choose an account and authorize the app. If you see a "Google hasn't verified this app" warning, that is expected for a local/test app. You can proceed after clicking the advanced option and continuing — only do this for apps you trust.

> **warning** If you see the "Google hasn't verified this app" page, proceed only if you trust the app and the credentials. Do not authorize unknown or public apps with your primary Google account.

<Frame>
  <img alt="A browser window showing Google's &#x22;Google hasn't verified this app&#x22; warning (red triangle icon and &#x22;Back to safety&#x22; button) overlaid on a code editor/IDE in the background." />
</Frame>

After allowing access you should see confirmation in the console that authentication succeeded and tokens were saved locally. Typical console output:

```bash theme={null}
http://localhost:3500/oauth2callback?code=4/0AVMBsJiQmpdFfFIB1ArXnIZn8182nNKCBL72RB3A43btCF5c6ZP6Xg4mJtqWZeEE8xYkUw&scope=...
Authentication successful. Tokens saved to /Users/jeremy/.config/google-calendar-mcp/tokens.json
```

## 6. Add the MCP server to Claude Desktop

Edit your Claude Desktop configuration file and add a new MCP server entry under `mcpServers`. The config file location depends on your OS:

| OS      | Config path                                                       |
| ------- | ----------------------------------------------------------------- |
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json`                     |

Example minimal JSON to add the Google Calendar MCP server:

```json theme={null}
{
  "mcpServers": {
    "google-calendar": {
      "command": "npx",
      "args": ["@cocal/google-calendar-mcp"],
      "env": {
        "GOOGLE_OAUTH_CREDENTIALS": "/path/to/your/gcp-oauth.keys.json"
      }
    }
  }
}
```

A fuller example that includes multiple MCP servers:

```json theme={null}
{
  "mcpServers": {
    "Meteo API": {
      "command": "/usr/local/bin/node",
      "args": ["/Users/jeremy/demos/Weather-MCP-Server/server.js"]
    },
    "Hacker News API 2": {
      "command": "/usr/local/bin/node",
      "args": ["/Users/jeremy/demos/mcpstuff/postman-mcp/postman-mcp-server/mcpServer.js"]
    },
    "google-calendar": {
      "command": "npx",
      "args": ["@cocal/google-calendar-mcp"],
      "env": {
        "GOOGLE_OAUTH_CREDENTIALS": "/Users/jeremy/demos/mcpstuff/google-calendar-mcp/credentials.json"
      }
    }
  }
}
```

After saving the config, restart Claude Desktop. Claude will detect the new MCP server and surface calendar-related tools.

## 7. Interacting with the calendar from Claude

Once the MCP server is connected, use natural-language prompts like:

* "What do I have on my calendar this week?"
* "Create a new event on Saturday at 3 p.m. titled 'Take a Walk'."

Claude will display the MCP tool UI and request permission to use the calendar tool. You can grant permission temporarily ("Allow once") or permanently ("Allow always").

<Frame>
  <img alt="A computer desktop screenshot showing a code editor (file explorer on the left) and a dark pop-up window in the center displaying a &#x22;Weekly Calendar Overview&#x22; with listed events and times. The editor looks like Visual Studio Code with project files and a JSON file open." />
</Frame>

Here is the permission modal that Claude shows before creating an event:

<Frame>
  <img alt="A screenshot of a code editor (likely VS Code) showing a project folder named &#x22;GOOGLE-CALENDAR-MCP&#x22; in the sidebar. In the center is a modal from &#x22;Claude&#x22; requesting permission to use a Google Calendar &#x22;create-event&#x22; tool with buttons for &#x22;Allow always,&#x22; &#x22;Allow once,&#x22; and &#x22;Decline.&#x22;" />
</Frame>

After creating an event from Claude, verify it directly in Google Calendar:

<Frame>
  <img alt="A screenshot of Google Calendar in dark mode showing the week of July 20–26, 2025 with events like &#x22;Night of Fire,&#x22; &#x22;Christi and AJ's wedding,&#x22; and a highlighted &#x22;take a walk&#x22; event on Saturday, July 26 from 3–4 PM. The left sidebar with mini calendar and calendar list plus an event details pop-up are visible." />
</Frame>

## Why use an MCP server?

MCP servers provide a consistent, tool-like interface that LLMs can call to perform API actions on your behalf. Benefits include:

* Simplified authorization: OAuth flows and token storage are handled by the MCP server.
* Structured responses: The MCP server returns parsed, predictable results for the assistant to consume.
* Reusability: The same MCP server can be reused across multiple assistant deployments without re-implementing API logic.

This reduces the need to write custom API glue code every time you want the assistant to interact with an external service.

> **lightbulb** Keep your downloaded credential files and token files private. Do not commit `credentials.json` or `tokens.json` to a public repository.

## Closing

This walkthrough demonstrates how to run a Google Calendar MCP server locally, authorize it with Google OAuth, register it with Claude Desktop, and use natural language to read and create events. MCP servers let you expose APIs to LLM-based assistants cleanly while isolating authorization and API logic from the assistant itself.

## Links and references

* Google Cloud Console — APIs Library: [https://console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)
* Google Calendar API docs: [https://developers.google.com/calendar](https://developers.google.com/calendar)
* OAuth 2.0 for Desktop Apps: [https://developers.google.com/identity/protocols/oauth2](https://developers.google.com/identity/protocols/oauth2)
* Google unverified apps doc: [https://support.google.com/cloud/answer/7519473](https://support.google.com/cloud/answer/7519473)
* google-calendar-mcp README: [https://github.com/nspady/google-calendar-mcp#readme](https://github.com/nspady/google-calendar-mcp#readme)

- [Watch Video](https://learn.kodekloud.com/user/courses/mcp-for-beginners/module/910a0b7a-ac6e-43f1-956e-203a70c3d455/lesson/c016ef00-0fea-40ad-8187-b983c50665be)
