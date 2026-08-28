# /root/crypto-price-mcp/src/tools/crypto_price.py
"""Crypto price tool for MCP server.
"""

from core.server import mcp
from core.utils import get_tool_config

@mcp.tool()
def crypto_price(message: str) -> str:
    """Crypto_price tool implementation.

    This is a template function. Replace this implementation with your tool logic.
    """
    # Get tool-specific configuration from kmcp.yaml
    config = get_tool_config("crypto_price")

    # Basic example implementation — replace with actual logic
    prefix = config.get("prefix", "echo: ")
    return f"{prefix}{message}"
```

Note: This template shows how to register a tool with `@mcp.tool()` and access per-tool configuration through `get_tool_config()`.

## 5. A robust crypto price tool (CoinGecko)

Below is a fuller example that calls CoinGecko’s simple price API, includes a thorough docstring (agents parse this), basic validation, error handling, and returns a structured dictionary:

```python theme={null}
# /root/crypto-price-mcp/src/tools/crypto_price.py
"""Crypto price tool for MCP server.
"""

import requests
from core.server import mcp
from core.utils import get_tool_config

@mcp.tool()
def get_crypto_price(symbol: str = "bitcoin", currency: str = "usd") -> dict:
    """Fetch the current live price for a cryptocurrency.

    Args:
        symbol: Cryptocurrency ID as used by CoinGecko (e.g., 'bitcoin', 'ethereum', 'cardano').
        currency: Target currency (e.g., 'usd', 'eur', 'gbp', 'aud').

    Returns:
        dict: On success, returns:
            {
                "symbol": "<symbol>",
                "currency": "<CURRENCY>",  # uppercased
                "price": <numeric_price>
            }
        On failure, returns:
            { "error": "<error message>" }
    """
    # Normalize inputs
    symbol = (symbol or "bitcoin").strip().lower()
    currency = (currency or "usd").strip().lower()

    # Allow overriding URL via kmcp.yaml tool config
    config = get_tool_config("crypto_price")
    base_url = config.get("coingecko_url", "https://api.coingecko.com/api/v3/simple/price")

    url = f"{base_url}?ids={symbol}&vs_currencies={currency}"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        data = resp.json()
        price = data.get(symbol, {}).get(currency)

        if price is None:
            return {"error": f"No price data found for '{symbol}' in '{currency}'"}

        return {
            "symbol": symbol,
            "currency": currency.upper(),
            "price": price,
        }
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
```

<Callout icon="lightbulb">
  Provide detailed docstrings: agents parse the docstring to learn the tool’s parameters, behavior and return format. Clear examples and error cases make tool usage more reliable and reduce unexpected behavior from LLM agents.
</Callout>

## 6. Copy the tool file into the project

If you implemented the tool outside the project tree, copy it into the MCP project tools folder:

```bash theme={null}
cp /root/crypto_price.py /root/crypto-price-mcp/src/tools/crypto_price.py
```

## 7. Run the MCP Inspector to validate the tool

Start the MCP Inspector script (example name in this environment: `run-mcp-inspector`). The Inspector exposes a web UI and prints a proxy address plus a session token; use the token to authenticate in the UI.

Example Inspector output (truncated):

```console theme={null}
⚙️ Proxy server listening on 127.0.0.1:6277
🔑 Session token: [SECRET_REDACTED]
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

Open the Inspector URL, authenticate with the printed session token, and confirm that `get_crypto_price` appears in the Tools list.

<Frame>
  <img alt="A screenshot of a developer web UI (MCP Inspector v0.15.0) showing a Tools panel with a hand cursor over a &#x22;get_crypto_price&#x22; entry and other tool items like &#x22;echo.&#x22; The left side shows configuration settings and the right pane prompts to &#x22;Select a tool,&#x22; with a history list below." />
</Frame>

## 8. Run the tool from the Inspector

* Select `get_crypto_price`.
* Default inputs: `symbol: bitcoin`, `currency: usd`.
* Click "Run tool" to invoke the MCP server and retrieve the live price.

Example Inspector response (JSON):

```json theme={null}
{
  "symbol": "bitcoin",
  "currency": "USD",
  "price": 87742
}
```

## 9. Package the MCP server into a Docker image

Build the MCP server image using the `kmcp build` command from your project directory:

```bash theme={null}
kmcp build --project-dir /root/crypto-price-mcp \
  -t kodekloud/kmcp-server:bitcoin \
  --platform linux/amd64
```

Build logs will show Docker layers and an exported image. Example truncated output:

```console theme={null}
#24 exporting to image
#24 writing image sha256:1df91f67cb9a... done
#24 naming to docker.io/kodekloud/kmcp-server:bitcoin done
✓ Successfully built Docker image: kodekloud/kmcp-server:bitcoin
```

Tip: Use the `--platform` flag to control the target CPU architecture (e.g., `linux/amd64`, `linux/arm64`) when cross-building.

## 10. Deploy the MCP server to Kubernetes

Apply the provided Kubernetes manifest for the MCP server (included in the exercise). After applying, verify the MCP server pod is running and that the `MCPServer` resource reports an accepted/ready state.

## 11. Deploy the declarative agent that uses the MCP server

Apply the declarative agent manifest (for example `crypto-price-agent.yaml`). The declarative Agent references the `MCPServer` and lists the tool names the agent can invoke.

Example agent manifest:

```yaml theme={null}
apiVersion: kagent.dev/v1alpha2
kind: Agent
metadata:
  name: crypto-price-agent
  namespace: kagent
spec:
  declarative:
    modelConfig: default-model-config
    stream: true
    systemMessage: |-
      You're a helpful agent, made by the kagent team.

      # Instructions
      - If user question is unclear, ask for clarification before running any tools
      - Always be helpful and friendly
      - If you don't know how to answer the question DO NOT make things up, tell the user "Sorry, I don't know how to answer that" and ask them to clarify the question further
      - If you are unable to help, or something goes wrong, refer the user to https://kagent.dev for more information or support.

      # Response format:
      - ALWAYS format your response as Markdown
      - Your response will include a summary of actions you took and an explanation of the result

      - If you created any artifacts such as files or resources, you will include those in your response as well
    tools:
      - mcpServer:
          apiGroup: kagent.dev
          kind: MCPServer
          name: crypto-price-mcp
          toolNames:
            - echo
            - get_crypto_price
          type: McpServer
description: crypto price agent
type: Declarative
```

Verify the agent is ready:

```bash theme={null}
kubectl get agent -n kagent
```

Expected output (example):

```console theme={null}
NAME               TYPE         READY   ACCEPTED
crypto-price-agent Declarative  True    True
```

## 12. Interact with the agent via KAgent UI

Open the KAgent UI, select `crypto-price-agent`, and ask natural-language questions such as:

* "What's the current price of Bitcoin?"
* "What's the current price of Ethereum in USD?"
* "Compare the price between Bitcoin and Ethereum."

The declarative agent will call the MCP server tool `get_crypto_price`, aggregate results and return a Markdown-formatted reply summarizing the results and actions taken. Example: a response listing Bitcoin at \~$87,870 USD and Ethereum at ~$2,947.37 USD.

<Frame>
  <img alt="A screenshot of a chat interface showing a &#x22;crypto-price-agent&#x22; response that lists Bitcoin at about 87,870 USD and Ethereum at about 2,947.37 USD. The page also shows chat controls, a sidebar with &#x22;New Chat,&#x22; and agent details/tools." />
</Frame>

## Notes and best practices

* Provide clear, example-rich docstrings — agents parse them to determine how to call your tool.
* Validate and normalize inputs (e.g., lowercase `symbol`/`currency`) before calling external APIs.
* Add timeouts and robust exception handling for network calls.
* Return structured results (not freeform text) so agents can programmatically use the returned values.
* Allow configurable endpoints and timeouts via `kmcp.yaml` so deployments can override defaults.

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [KAgent docs](https://kagent.dev)
* [CoinGecko API — Simple Price](https://www.coingecko.com/en/api/documentation)
* [Docker Hub](https://hub.docker.com/)

That’s all for this lesson — see you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/e50e4420-d5bb-46a9-b9fd-b1e827a675dc/lesson/89ce4b4d-8cc1-46f1-a598-78d86e9fb270" />
</CardGroup>


# Demo Deploying MCP Server KMCP Way

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KMCP-Installation-Overview/Demo-Deploying-MCP-Server-KMCP-Way/page

Guide to scaffolding, running, debugging, building, and deploying a Python MCP server with KMCP and MCP Inspector exposing cryptocurrency price tools

Hello everyone.

<Frame>
  <img alt="A presentation slide titled &#x22;Deploying MCP Server KMCP Way&#x22; with the word &#x22;Demo&#x22; on a dark curved design element to the right. The slide also shows a small &#x22;© Copyright KodeKloud&#x22; notice in the corner." />
</Frame>

Welcome to this hands-on lab. In this lesson we'll scaffold a Python-based MCP server using the kmcp CLI. The example MCP server will fetch real-time cryptocurrency prices and expose that functionality as MCP tools that agents can call.

High-level flow:

* An agent requests a tool (for example, "get Bitcoin price").
* The agent calls the MCP server’s tool endpoints.
* The MCP server executes the tool code (fetches live price), processes the response, and returns it.
* KMCP helps scaffold the project, run locally with the Inspector, build a container image, and deploy the MCP server to Kubernetes.

<Callout icon="lightbulb">
  KMCP is the CLI for building and managing Model Context Protocol (MCP) servers. Do not confuse it with the [KAgent CLI](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes) — KAgent CLI focuses on building and interacting with agents, while KMCP focuses on MCP server tooling, scaffolding, local debugging, builds, and deployments.
</Callout>

## Install KMCP CLI and MCP Inspector

Install the MCP Inspector (GUI for testing/debugging) and the kmcp CLI.

```bash theme={null}
