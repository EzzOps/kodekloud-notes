# Apply the agent manifest
kubectl apply -f /root/no_tool_aws-price-checker.yaml

# Watch pods in the kagent namespace
kubectl get pod -n kagent

# Inspect registered agents
kubectl get agent -n kagent
```

Representative status progression (condensed)

```bash theme={null}
# Shortly after apply:
NAME                                           READY   STATUS              RESTARTS   AGE
aws-price-check-694757df-x7552                 0/1     ContainerCreating   0          8s
awslabs-aws-pricing-mcp-server-latest-...      1/1     Running             0          12m
kagent-ui-...                                   1/1     Running             0          15m

# A short while later (agent pod ready):
NAME                                           READY   STATUS    RESTARTS   AGE
aws-price-check-694757df-x7552                 1/1     Running   0          69s
awslabs-aws-pricing-mcp-server-latest-...      1/1     Running   0          13m
kagent-ui-...                                   1/1     Running   0          16m

# Agent resource shows READY toggling to True once pod is ready
kubectl get agent -n kagent
NAME            TYPE          READY   ACCEPTED
aws-price-check Declarative    True    True
```

<Callout icon="lightbulb">
  Agents without declared tools rely entirely on the LLM and cannot fetch live pricing. To obtain live pricing you must attach MCP server tools to the agent.
</Callout>

Try a pricing query (LLM-only)

* Ask the LLM-only agent about the on-demand price for `g4dn.16xlarge` on Linux with shared tenancy in `us-east-1` and `ap-southeast-2`.
* Because the agent has no tool access, results will either be an LLM-derived estimate or a refusal like "Sorry, I do not have that pricing information available."

## Attach the AWS Pricing MCP server tools to the agent

Next, configure the agent to call the MCP server tools that expose the AWS Pricing List API.

In the KAgent UI:

* View → MCP servers → select the AWS Pricing MCP server (e.g. `awslabs-aws-pricing-mcp-server-latest`)
* View → Tools to inspect available functions such as `get_pricing`, `get_pricing_attribute_values`, `get_pricing_service_codes`, `generate_cost_report`, etc.

Image: list and search of AWS pricing API tools in the KAgent UI

<Frame>
  <img alt="A webpage screenshot of the &#x22;kagent&#x22; site showing a search bar and a list of AWS pricing API tools (e.g., get_pricing, get_pricing_attribute_values) with short descriptions. The interface shows navigation links at the top and a count of &#x22;9 tools found.&#x22;" />
</Frame>

Example tools block added to the agent manifest

```yaml theme={null}
tools:
- mcpServer:
    apiGroup: kagent.dev
    kind: MCPServer
    name: awslabs-aws-pricing-mcp-server-latest
    toolNames:
    - get_pricing_service_codes
    - get_pricing_service_attributes
    - get_pricing_attribute_values
    - get_pricing
    - get_price_list_urls
    - generate_cost_report
  type: McpServer
description: aws price checker api
type: Declarative
```

Apply the edited manifest and confirm

```bash theme={null}
kubectl apply -f /root/with_tool_aws-price-checker.yaml

# Confirm the agent's tools are registered in the resource YAML
kubectl get agent aws-price-check -n kagent -o yaml | grep -A20 "tools:"
```

Representative pod listing and agent YAML summary

```bash theme={null}
kubectl get pod -n kagent

NAME                                                    READY   STATUS    RESTARTS   AGE
aws-price-check-b9476b56c-qbpt5                         1/1     Running   0          28s
awslabs-aws-pricing-mcp-server-latest-58cc4cc799-6cgbs   1/1     Running   0          26m
kagent-ui-59d5bbd564-6ssnm                               1/1     Running   0          29m

# Agent resource shows the tools block (see example above)
kubectl get agent aws-price-check -n kagent -o yaml | grep -A20 "tools:"
```

Table: Common tool names exposed by the AWS Pricing MCP server

| Tool name                        | Purpose / Example usage                                                |
| -------------------------------- | ---------------------------------------------------------------------- |
| `get_pricing_service_codes`      | Enumerate available pricing service codes (e.g., `AmazonEC2`).         |
| `get_pricing_service_attributes` | Retrieve service attributes (e.g., `instanceType`, `operatingSystem`). |
| `get_pricing_attribute_values`   | Fetch all values for an attribute (e.g., all EC2 instance families).   |
| `get_pricing`                    | Query price terms and priceDimensions for a specific product filter.   |
| `get_price_list_urls`            | Get Price List API URLs for a service and region.                      |
| `generate_cost_report`           | Produce aggregated cost reports across resources or time windows.      |

## Run the same pricing query with tools attached

Re-run the earlier query for `g4dn.16xlarge` (Linux, shared tenancy) in `us-east-1` and `ap-southeast-2`. With tools attached:

How the call flow works

1. The agent invokes an MCP server tool such as `get_pricing` with filters for `region`, `operatingSystem`, `instanceType`, and `tenancy`.
2. The MCP server calls the AWS Pricing List API and returns structured JSON to the agent.
3. The agent's LLM processes the JSON and formats a human-readable response (tables, lists, or cost recommendations).

Tool response (excerpt)

```json theme={null}
{
  "terms": {
    "OnDemand": {
      "MD2NZEY6DE5PD6FG.JRTCKXETXF": {
        "priceDimensions": {
          "MD2NZEY6DE5PD6FG.JRTCKXETXF.6YS6EN2CT7": {
            "unit": "Hrs",
            "endRange": "Inf",
            "description": "$5.659 per Unused Reservation Linux g4dn.16xlarge Instance Hour",
            "appliesTo": [],
            "rateCode": "MD2NZEY6DE5PD6FG.JRTCKXETXF.6YS6EN2CT7",
            "beginRange": "0",
            "pricePerUnit": {
              "USD": "5.6590000000"
            }
          }
        }
      }
    }
  }
}
```

Agent response (with tools)

* Using the returned pricing data the agent can provide accurate results, for example:
  * us-east-1 on-demand price for Linux `g4dn.16xlarge`: approximately \$4.35/hour
  * ap-southeast-2 on-demand price for Linux `g4dn.16xlarge`: approximately \$5.65/hour

Image: chat UI showing pricing result for g4dn.16xlarge in us-east-1

<Frame>
  <img alt="Screenshot of a chat-style interface displaying AWS pricing results for a g4dn.16xlarge Linux instance in us‑east‑1 with an on‑demand price of about $4.35/hr. The right sidebar shows agent details and available pricing API functions." />
</Frame>

## Run more complex queries

You can request multi-dimensional comparisons in a single user prompt. The agent will orchestrate multiple tool calls (one per region/offer/purchase option), aggregate results, and return a consolidated table or list.

Example complex query:

* Compare on-demand and 1-year reserved pricing for an `m7g` instance across `ap-southeast-2` (Sydney) and `us-east-1` (N. Virginia). The agent will:
  * Call `get_price_list_urls` and `get_pricing` for each region and purchase option
  * Parse `pricePerUnit` from the returned JSON
  * Compute and present the comparisons in a table

Image: chat UI where the user requests a cross-region comparison for m7g instances

<Frame>
  <img alt="A screenshot of a chatbot UI where the user asks to compare on‑demand and 1‑year reserved pricing for AWS m7g EC2 instances across Sydney and N. Virginia. The right sidebar shows agent details and tool names, and the lower pane shows an &#x22;Executing tools...&#x22; area with Send/Cancel buttons." />
</Frame>

## Operational notes and best practices

Table: Troubleshooting checklist

| Symptom                            | Check                                                                                                                         |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Agent does not return pricing      | Verify agent pod is Running; check agent YAML includes `tools → mcpServer → toolNames`.                                       |
| Tools not listed in UI             | Verify MCP server is Running and healthy; open View → Tools for that MCP server.                                              |
| Tool calls time out or fail        | Check network connectivity, MCP server logs, and required AWS credentials/permissions.                                        |
| Slow responses for complex queries | Reduce parallel calls or cache repeated price list results; consider pre-generating cost reports with `generate_cost_report`. |

Additional patterns

* Team workflow: Expose centralized pricing tools via an MCP server and create a pricing agent teams can call from CI/CD or chat to get cost estimates during planning or deployment.
* Debugging: Review logs for the MCP server and agent pods (`kubectl logs`) to troubleshoot tool invocation failures.
* Performance: Tool calls depend on MCP server latency, AWS Pricing API response time, and the number of distinct queries; batch or cache where appropriate.

<Callout icon="warning">
  Ensure the MCP server has the necessary AWS credentials and IAM permissions to call the AWS Pricing API. Without proper credentials, tool calls will fail even if the MCP server pod is Running.
</Callout>

## References and further reading

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [AWS Pricing API / Pricing List API](https://docs.aws.amazon.[SECRET_REDACTED]-changes.html)
* KAgent documentation (see your platform’s KAgent docs for agent manifest details and modelConfig options)

That’s it for this lab-style lesson. Experiment with different tool combinations, regions, instance families, and purchase options to explore the full capabilities of agents + MCP servers.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/e50e4420-d5bb-46a9-b9fd-b1e827a675dc/lesson/ac1a2bc1-d370-4437-a106-08f51f7064bb" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/e50e4420-d5bb-46a9-b9fd-b1e827a675dc/lesson/eb1b0566-4e83-43ad-a38e-fb8124e42e0e" />
</CardGroup>


# Demo Deploying MCP Server KMCP Way Part 2

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KMCP-Installation-Overview/Demo-Deploying-MCP-Server-KMCP-Way-Part-2/page

Guide to adding a crypto price MCP tool, building and deploying an MCP server and declarative agent, and testing tool usage via MCP Inspector and KAgent UI

In this lesson we stop a running MCP server, add a new MCP tool (`crypto_price`), inspect the tool, build the MCP server image, deploy the server and a declarative agent, then interact with the agent via the KAgent UI. The steps below follow the same sequence used in the video; examples and commands are included for reproducibility.

## 1. Stop the running MCP server

Terminate the running MCP server with Ctrl+C in the terminal where it’s running.

## 2. Add a new tool using kmcp

Tools must use snake\_case names (for example: `crypto_price`). Add the tool to your KMCP project with:

```bash theme={null}
kmcp add tool crypto_price /root/crypto-price-mcp
```

This creates the tool registration file(s) inside your project. Verify the generated tool configuration in the project directory — the registration file is what agents query for tool discovery.

Quick command reference

| Action         | Command / Example                                                                                         |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| Add tool       | `kmcp add tool crypto_price /root/crypto-price-mcp`                                                       |
| Build image    | `kmcp build --project-dir /root/crypto-price-mcp -t kodekloud/kmcp-server:bitcoin --platform linux/amd64` |
| Copy tool file | `cp /root/crypto_price.py /root/crypto-price-mcp/src/tools/crypto_price.py`                               |
| Check agent    | `kubectl get agent -n kagent`                                                                             |

## 3. MCP protocol and tool discovery (overview)

* When an AI agent connects to the MCP server it queries for available tools.
* The MCP server returns metadata for each tool: name, description, parameters, return type, etc.
* Agents rely heavily on the tool’s function docstring (included in the MCP response) to understand usage, parameters and expected return values.
* Use the decorator `@mcp.tool()` to register a Python function as an MCP-invokable tool.

## 4. Example: simple MCP tool implementation

Place this template under `src/tools/crypto_price.py` in the MCP project:

```python theme={null}
