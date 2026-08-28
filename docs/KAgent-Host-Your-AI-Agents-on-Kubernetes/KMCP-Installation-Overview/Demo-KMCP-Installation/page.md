# Controller logs
kubectl -n kagent logs -l app.kubernetes.io/component=controller -f
```

## Inspect KAgent pods and services

Confirm pods and services in the `kagent` namespace:

```bash theme={null}
kubectl get pod -n kagent
```

Example output:

```text theme={null}
NAME                                              READY   STATUS    RESTARTS   AGE
kagent-controller-6886fc4f5c-4t7gd                0/1     ContainerCreating   0   16s
kagent-kmcp-controller-manager-76645f577f-fbqqs   1/1     Running             0   16s
kagent-ui-59d5bbd564-lssv4                        0/1     Running             0   16s
```

```bash theme={null}
kubectl get svc -n kagent
```

Example output:

```text theme={null}
NAME                                                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
kagent-controller                                   ClusterIP   172.20.160.95   <none>        8083/TCP                     30s
kagent-kmcp-controller-manager-metrics-service      ClusterIP   172.20.74.151   <none>        8443/TCP                     30s
kagent-ui                                           NodePort    172.20.42.19    <none>        8080:32165/TCP               30s
```

If you want to access the UI on a specific NodePort (for example `30080`), patch the `kagent-ui` service:

```bash theme={null}
kubectl patch svc kagent-ui -n kagent \
  -p '{"spec":{"type":"NodePort","ports":[{"name":"ui","port":8080,"targetPort":8080,"nodePort":30080}]}}'
```

After image pulls and initialization complete, pods should reach `Running`:

```bash theme={null}
kubectl get pod -n kagent
```

Example final output:

```text theme={null}
NAME                                   READY   STATUS    RESTARTS   AGE
kagent-controller-6886fc4f5c-4t7gd     1/1     Running   0          63s
kagent-kmcp-controller-manager-76645f577f-fbqqs   1/1   Running   0   63s
kagent-ui-59d5bbd564-lssv4              1/1     Running   0          63s
```

## AWS credentials used by MCP servers

MCP servers require AWS credentials (or other supported credential delivery methods). In this lab environment, credentials are stored at `/root/.aws/credentials`:

```bash theme={null}
cat /root/.aws/credentials
```

Example output:

```text theme={null}
[default]
aws_access_key_id = [AWS_ACCESS_KEY_ID]
aws_secret_access_key = [AWS_SECRET_ACCESS_KEY]
```

Region used in this lesson: `us-east-1`.

<Callout icon="lightbulb">
  MCP servers support multiple credential delivery methods (plain keys, IAM roles, etc.). Follow security best practices for credential handling and avoid checking credentials into source control.
</Callout>

## Install AWS Pricing MCP Server via the KAgent UI

1. Ensure the KAgent UI is accessible (port-forward or use the NodePort you set, e.g., `30080`).
2. Open the KAgent UI in your browser (use the lab environment link or Node IP + NodePort).
3. In the UI:
   * Click Create → New MCPServer.
   * Click Add MCP Server.
   * Enter the server name exactly: `AWS Pricing MCP Server`.
   * Namespace: `kagent` (default).
   * Choose the "Command" option (not URL).
   * Command executor: select `uvx` (Python-based executor).
   * Package name: `awslabs.aws-pricing-mcp-server@latest`.
   * Provide environment variables copied from `/root/.aws/credentials` using these exact keys:
     * `AWS_ACCESS_KEY_ID`
     * `AWS_SECRET_ACCESS_KEY`
     * `AWS_REGION` (for example, `us-east-1`)

Example command used by the package:

```bash theme={null}
uvx awslabs.aws-pricing-mcp-server@latest
```

After adding the server, KAgent creates a pod for the MCP Server. Monitor resources:

```bash theme={null}
kubectl get pod -n kagent -w
kubectl get mcpserver -n kagent
```

You may first see the MCPServer with `False` readiness while images are pulling:

```text theme={null}
NAME                      READY   AGE
aws-pricing-mcp-server    False   51s
```

Wait until the MCPServer is `True` and the pod is `Running`:

```bash theme={null}
kubectl get mcpserver -n kagent
kubectl get pod -n kagent
```

Example final output:

```text theme={null}
# kubectl get mcpserver -n kagent
# kubectl get pod -n kagent
# aws-pricing-mcp-server-6f59fd7dd8-5j7wh             1/1     Running   0          2m40s
```

If readiness stays `False`, inspect events, pod describe, and pod logs:

```bash theme={null}
kubectl describe mcpserver aws-pricing-mcp-server -n kagent
kubectl describe pod <pod-name> -n kagent
kubectl logs <pod-name> -n kagent
```

## Install AWS Well-Architected Security MCP Server via manifest

Create a file named `mcp-server.yaml` with the following MCPServer manifest. Populate AWS credentials in the `env` section before applying:

```yaml theme={null}
apiVersion: kagent.dev/v1alpha1
kind: MCPServer
metadata:
  name: awslabs-well-architected-security-mcp-server
  namespace: kagent
spec:
  deployment:
    args:
    - awslabs.well-architected-security-mcp-server
    cmd: uvx
    env:
      AWS_ACCESS_KEY_ID:
      AWS_REGION: us-east-1
      AWS_SECRET_ACCESS_KEY:
    image: ghcr.io/astral-sh/uv:debian
    port: 3000
  stdioTransport: {}
  transportType: stdio
```

Important: do not change the `port` (must remain `3000`) or the `transportType` (`stdio`) — these are required by the package.

Steps:

1. Edit `mcp-server.yaml` and set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` with values from `/root/.aws/credentials`.
2. Apply the manifest:

```bash theme={null}
kubectl apply -f mcp-server.yaml
```

Example output:

```text theme={null}
mcpserver.kagent.dev/awslabs-well-architected-security-mcp-server created
```

Check status and pods:

```bash theme={null}
kubectl get mcpserver -n kagent
kubectl get pod -n kagent
```

Example output:

```text theme={null}
# kubectl get mcpserver -n kagent
# NAME                                             READY   AGE
# aws-pricing-mcp-server                           True    6m31s
# kubectl get pod -n kagent
# NAME                                                            READY   STATUS    RESTARTS   AGE
# aws-pricing-mcp-server-6f59fd7dd8-5j7wh                         1/1     Running   0          6m44s
# awslabs-well-architected-security-mcp-server-8b68c79f9-v6x7v    1/1     Running   0          26s
```

## Viewing tools exposed by an MCP Server in the UI

In the KAgent UI:

* Click the MCPServer entry, then click View → Tools.
* Each MCP Server lists how many tools it exposes. Example:
  * AWS Well-Architected Security MCP Server — may show `6` tools.
  * AWS Pricing MCP Server — may show `9` tools.
* Click the number to inspect individual tools exposed by the MCP Server.

## Notes and troubleshooting tips

* Environment variables must use the exact key names required by the package: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`.
* `uvx` runs Python-based packages. Some packages may use `npx` (npm). Choose the executor that matches the package.
* Image pulls and container initialization can take time. Use `kubectl logs`, `kubectl describe`, and `kubectl get -w` to monitor readiness.
* For persistent issues, inspect controller logs:

```bash theme={null}
kubectl -n kagent logs -l app.kubernetes.io/component=controller -f
```

## Links and references

* KAgent: Host Your AI Agents on Kubernetes (course): [https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* AWS CLI / Credentials best practices: [https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

That's it — you installed one MCP Server via the UI and one via a manifest, verified both, and viewed the tools each server exposes. See you in the next lab.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/e50e4420-d5bb-46a9-b9fd-b1e827a675dc/lesson/eeb4f7f4-b8e5-4765-9495-b928e2be1db2" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/e50e4420-d5bb-46a9-b9fd-b1e827a675dc/lesson/1e3a41d4-84a4-4395-b384-dbd444ef8720" />
</CardGroup>


# Demo KMCP Installation

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KMCP-Installation-Overview/Demo-KMCP-Installation/page

Guide to installing and verifying the KMCP controller bundled with KAgent, checking CRDs and resources, inspecting components, and deploying a sample MCPServer to validate reconciliation.

Welcome to this KMCP controllers lesson. Here you'll learn how to install the KMCP controller (bundled with KAgent), confirm CRDs and API resources, inspect controller components, and deploy a sample MCPServer to verify reconciliation behavior.

This guide assumes the KMCP CRDs and model config were already installed. We'll begin by reviewing the Helm values file used to install KAgent.

## 1) Values file used for Helm install

Inspect the values file located at `/root/01-values-min.yaml`:

```yaml theme={null}
