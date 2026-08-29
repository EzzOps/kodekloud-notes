# Example k3d help summary
k3d --help
# Available Commands (examples)
#   cluster   Manage cluster(s)
#   node      Manage node(s)
#   image     Handle container images
#   version   Show k3d and default k3s version
```

Example `docker ps` output for a k3d cluster:

```text theme={null}
CONTAINER ID   IMAGE                                    COMMAND                  CREATED         STATUS         PORTS                    NAMES
460856a03c1    ghcr.io/k3d-io/k3d-tools:5.8.3          "/app/k3d-tools noop"    12 minutes ago  Up 12 minutes  0.0.0.0:52149->6443/tcp  k3d-datadog-cluster-tools
82f4a878a850    ghcr.io/k3d-io/k3d-proxy:5.8.3          "/bin/sh -c nginx-pr…"   4 days ago      Up 12 minutes  0.0.0.0:52148->80/tcp    k3d-datadog-cluster-serverlb
c73a12740bec    rancher/k3s:v1.31.5-k3s1                 "/bin/k3d-entrypoint…"   4 days ago      Up 12 minutes  0.0.0.0:52147->6443/tcp  k3d-datadog-cluster-agent-1
754962cb41     rancher/k3s:v1.31.5-k3s1                 "/bin/k3d-entrypoint…"   4 days ago      Up 12 minutes  0.0.0.0:52146->6443/tcp  k3d-datadog-cluster-agent-0
ce256fc721     rancher/k3s:v1.31.5-k3s1                 "/bin/k3d-entrypoint…"   4 days ago      Up 12 minutes  0.0.0.0:52145->6443/tcp  k3d-datadog-cluster-server-0
```

From inside the cluster, use kubectl to list nodes and pods:

```bash theme={null}
kubectl get nodes
# NAME                             STATUS   ROLES                  AGE    VERSION
# k3d-datadog-cluster-agent-0      Ready    <none>                4d7h   v1.31.5+k3s1
# k3d-datadog-cluster-agent-1      Ready    <none>                4d7h   v1.31.5+k3s1
# k3d-datadog-cluster-server-0     Ready    control-plane,master   4d7h   v1.31.5+k3s1
```

```bash theme={null}
kubectl get pods
# NAME                                      READY   STATUS    RESTARTS   AGE
# app-1                                     1/1     Running   2          13m
# datadog-agent-g5fd5                       2/2     Running   0          12m
# datadog-agent-xm9t                        2/2     Running   0          11m
# datadog-cluster-agent-79b5c775bb-rtcnf    2/2     Running   1          11m
# datadog-operator-6c9b7978f-r24mx          1/1     Running   1          13m
```

## Datadog components in Kubernetes

Common Datadog components deployed in Kubernetes (installed via Helm or Operator):

| Component                            | Purpose                                                                                       | Notes / Example                                       |
| ------------------------------------ | --------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `datadog-agent` (DaemonSet)          | Runs on every node to collect host & container metrics, logs, traces, and profiles            | Deployed as a DaemonSet to ensure per-node collection |
| `datadog-cluster-agent` (Deployment) | Cluster-level aggregator and API for cluster features (cluster checks, orchestrator metadata) | Scale based on cluster size                           |
| `datadog-operator` (Deployment)      | Reconciles Datadog custom resources when using the Operator                                   | Present only if operator-based install is used        |

Verify daemonsets and deployments:

```bash theme={null}
kubectl get daemonsets
# NAME          DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   AGE
# datadog-agent 3         3         3       3            3           4d7h
```

```bash theme={null}
kubectl get deployment
# NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
# datadog-cluster-agent  1/1     1            1           4d7h
# datadog-operator       1/1     1            1           4d7h
```

## Installing Datadog via Helm

Add the Datadog Helm repo and install the chart:

```bash theme={null}
helm repo add datadog https://helm.datadoghq.com
helm repo update
helm install datadog datadog/datadog
```

You can install the chart either before or after creating the Kubernetes secret that contains the Datadog API key, but the Agent requires credentials to authenticate and send telemetry.

## API keys and Kubernetes secrets

Create an API key in the Datadog web UI (Organization Settings → API keys). Store the key in a Kubernetes secret for the Agent to use:

```bash theme={null}
kubectl create secret generic datadog-secret --from-literal=api-key='<DATADOG_API_KEY>'
```

Replace `<DATADOG_API_KEY>` with the key you copied from Datadog.

Verify the secret exists:

```bash theme={null}
kubectl get secrets
# NAME            TYPE     DATA   AGE
kubectl describe secret datadog-secret
# Name:         datadog-secret
# Namespace:    default
# Type:         Opaque
# Data
# ====
# api-key: 32 bytes
```

Datadog UI views for API keys and cluster dashboards:

<Frame>
  <img alt="The image shows a Datadog dashboard displaying the state of Kubernetes resources, including clusters, namespaces, nodes, and other metrics, alongside information on autoscaling operations and resource costs." />
</Frame>

<Frame>
  <img alt="The image shows a screen from an application under &#x22;Organization Settings,&#x22; specifically displaying a list of API keys along with their details such as name, key ID, creation date, and last used date." />
</Frame>

## DatadogAgent (Operator) example

When using the Datadog Operator, the DatadogAgent CR references the secret with the API key. Example `DatadogAgent` manifest:

```yaml theme={null}
apiVersion: datadoghq.com/v1alpha1
kind: DatadogAgent
metadata:
  name: datadog
spec:
  global:
    clusterName: datadog-k3d-cluster
    site: us5.datadoghq.com
  credentials:
    secret:
      secretName: datadog-secret
      keyName: api-key
  features:
    orchestratorExplorer:
      enabled: true
    logCollection:
      enabled: true
      containerCollectAll: true
    apm:
      enabled: true
      unixDomainSocketConfig:
        path: /var/run/datadog/apm.socket # default
```

Important fields:

* `clusterName` — how the cluster will appear in Datadog.
* `site` — Datadog site/region (e.g., `us5.datadoghq.com`).
* `credentials.secret` — Kubernetes secret name/key that contains the API key.
* `features` — enable `orchestratorExplorer`, `logCollection`, `apm`, and profiling.

Apply the DatadogAgent manifest:

```bash theme={null}
kubectl apply -f datadog-agent.yaml
```

If the Agents start without a valid secret or with an incorrect secret reference, they will fail to authenticate. Use `kubectl logs` on the Agent pods to diagnose authentication errors.

> **warning** Ensure the secret name and key in the DatadogAgent manifest match the actual Kubernetes secret. Missing or incorrect API key references will prevent the Agent from sending telemetry.

## Application instrumentation (Node.js)

This demo uses a simple Node.js REST API with three routes. To enable Datadog tracing for Node.js, install `dd-trace` and initialize it as early as possible — before other imports or application initialization.

> **lightbulb** Always require and initialize `dd-trace` at the top of your application entrypoint (before requiring frameworks like `express`) so auto-instrumentation captures requests and internal spans.

Example `index.js` (tracing + basic routes):

```javascript theme={null}
const tracer = require('dd-trace').init();
const express = require('express');
const app = express();
const port = 80;

app.get('/', (req, res) => {
  console.log('Request received at root route');
  res.send('Hello, World!');
});

app.get('/route1', (req, res) => {
  console.error('Error simulated on route 1');
  sum();
  subtraction();
  res.send('This is route 1');
});

app.get('/route2', (req, res) => {
  console.warn('Warn log on route 2');
  subtraction();
  res.send('This is route 2');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

function sum() {
  let a = 10;
  let b = 20;
  return a + b;
}

function subtraction() {
  let a = 20;
  let b = 10;
  return a - b;
}
```

## Dockerfile

Make sure `dd-trace` is installed in the image so the tracer import resolves at runtime.

```dockerfile theme={null}
FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies (copy package files first for layer caching)
COPY package*.json ./
RUN npm install --production && npm cache clean --force

# Install Datadog tracer
RUN npm install dd-trace

# Bundle app source
COPY . .

# Expose the port the app runs on
EXPOSE 80

# Start the app
CMD [ "node", "index.js" ]
```

## Pod manifest (example)

The application pod example includes environment variables used by the Datadog tracer/agent and references the `datadog-secret` for the API key.

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: app-1
  labels:
    app: app-1
spec:
  containers:
    - name: app-teste-node-container
      image: pedroignacio/app-teste-node:0.2
      imagePullPolicy: Never
      ports:
        - containerPort: 80
      env:
        - name: DD_TRACE_AGENT_URL
          value: "http://datadog-agent.default.svc.cluster.local:8126"
        - name: DD_AGENT_HOST
          value: "datadog-agent.default.svc.cluster.local"
        - name: DD_TRACE_AGENT_PORT
          value: "8126"
        - name: DD_ENV
          value: "prod"
        - name: DD_SERVICE
          value: "node-app"
        - name: DD_PROFILING_ENABLED
          value: "true"
        - name: DD_PROFILING_TIMELINE_ENABLED
          value: "true"
        - name: DD_LOGS_INJECTION
          value: "true"
        - name: DD_APM_ENABLED
          value: "true"
        - name: DD_TRACE_SAMPLE_RATE
          value: "1.0"
        - name: DATADOG_API_KEY
          valueFrom:
            secretKeyRef:
              name: datadog-secret
              key: api-key
```

Apply the pod manifest and check pods:

```bash theme={null}
kubectl apply -f trace-pod-manifest.yaml
kubectl get pods
```

## Traffic generation with k6

Use a lightweight k6 script to exercise the Node.js routes and quickly create traces and logs.

`load.js`:

```javascript theme={null}
import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  duration: '1m',
  vus: 10, // Number of virtual users
};

const endpoint1 = __ENV.ENDPOINT1 || 'http://localhost:3030/';
const endpoint2 = __ENV.ENDPOINT2 || 'http://localhost:3030/route1';
const endpoint3 = __ENV.ENDPOINT3 || 'http://localhost:3030/route2';

export default function () {
  http.get(endpoint1);
  http.get(endpoint2);
  http.get(endpoint3);
  sleep(1);
}
```

Run k6 (after port-forwarding or deploying the service so the endpoints are reachable):

```bash theme={null}
k6 run load.js
```

## Logs and traces in Datadog

The Datadog Agent forwards logs and receives traces (APM) on port 8126. After generating traffic, you can inspect application logs and traces in Datadog.

Logs Explorer (filter by service, host, or container) shows timestamp, host, service, content, and extracted severity levels (info/warn/error).

<Frame>
  <img alt="The image shows a Datadog interface displaying log data, with filters and sources listed on the left and detailed logs including dates, hosts, services, and content in the main view." />
</Frame>

Use the left sidebar filters to narrow logs to your `node-app` service or to a specific host/container.

<Frame>
  <img alt="The image shows a Datadog Log Explorer interface displaying log data with details such as date, host, service, and content, alongside filtering options on the left sidebar." />
</Frame>

Click into an application log to see extracted fields and severity. The example below shows an error emitted by `route1` in the Node.js app.

<Frame>
  <img alt="The image shows a screenshot of the Datadog Log Explorer interface, displaying logs for the &#x22;node-app&#x22; service with a visible error message dated July 5, 2025. It includes filters and details about hosts, sources, and containers." />
</Frame>

APM → Trace Explorer displays traces composed of spans (Express handlers, DB calls, HTTP calls, etc.). Click a trace to view span breakdowns, attributes (environment, user agent, route, status code), and timings. This example shows a GET /route2 trace.

<Frame>
  <img alt="The image shows a Datadog APM interface displaying traces and span details for an HTTP GET request to a &#x22;node-app&#x22; service on route &#x22;/route2.&#x22; The HTTP request was successful with a status code of 200." />
</Frame>

Traces are critical for distributed systems — they reveal service call flows, span durations, and where latencies or errors occur.

## Wrap up — What you accomplished

This lesson demonstrated how to:

* Deploy and validate Datadog components (Agent, Cluster Agent, Operator) in Kubernetes and verify daemonsets/pods.
* Create a Kubernetes secret for the Datadog API key and reference it in the DatadogAgent configuration.
* Instrument a Node.js application with `dd-trace` (initialize at the top of the entrypoint) and include the tracer in the Docker image.
* Configure the application pod with environment variables so the Agent can collect traces, logs, and profiles.
* Generate traffic with k6 and observe logs/traces inside Datadog.

Final dashboard view:

<Frame>
  <img alt="The image shows a Datadog dashboard displaying the state of Kubernetes resources, including clusters, namespaces, nodes, and other metrics, alongside information on autoscaling operations and resource costs." />
</Frame>

Follow these steps — install the Helm chart or operator, create the API key secret, apply the DatadogAgent CR (if using the operator), instrument your app, and generate traffic — to capture rich telemetry in Datadog: metrics, logs, traces, and profiles for monitoring and troubleshooting.

Links and references

* Datadog Docs — APM & Tracing: [https://docs.datadoghq.com/tracing/](https://docs.datadoghq.com/tracing/)
* Datadog Helm Chart: [https://helm.datadoghq.com](https://helm.datadoghq.com)
* Kubernetes Basics: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* k3d: [https://k3d.io/](https://k3d.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/fd555480-82df-40f4-b8ad-2ea920d51077/lesson/b0118949-6f1c-4ae5-8c71-353a44bee142)


# Demo Data Visualization

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-Structuring-your-Platform/Demo-Data-Visualization/page

A Datadog walkthrough demonstrating metrics, logs, traces, Kubernetes visibility, query building, tag management, dashboards, and cost monitoring for operational observability and FinOps.

This lesson demonstrates Datadog’s data visualization capabilities across metrics, logs, APM traces, and Kubernetes visibility. The walkthrough follows the Datadog left-side navigation to show how to inspect telemetry, manage tags to control metric cardinality, build queries, and create dashboards that support operational monitoring and FinOps goals.

## Metrics overview

From the left panel, click **Metrics** to open the Metrics overview. The top section provides a platform-level snapshot of metric sources, the configurable processing pipeline, and an overview of ingested metrics (agents, integrations, API).

<Frame>
  <img alt="The image is a screenshot from Datadog's metrics overview page, showing a flowchart of how metrics flow through Datadog, with sections for metric sources, configurable processing, and available metrics. It includes data on active agents, cloud integrations, and API metrics." />
</Frame>

This demo environment reports only standard metrics via the Datadog Agent. There are no cloud integrations or API-generated metrics in this account, and logs/APM are not generating metrics here. All ingested telemetry passes through Datadog’s backend processing pipeline where you can add processing steps or scripts to transform data before indexing.

### Standard vs custom metrics

Standard metrics are typically collected by Datadog agents or integrations and usually do not incur additional per-metric costs. Custom metrics (user-created or high-cardinality metrics) can increase billing, so controlling which tags and metrics you emit is important for cost management and platform health.

> **lightbulb** Pay attention to tag cardinality: reducing unnecessary high-cardinality tags (for example, unique container IDs) helps control custom metric growth and platform costs.

## Metrics by source

Scroll down to see a breakdown of metrics by source: Kubernetes, APM, profiling, CSM, and others. This view helps you identify where your metrics originate and prioritize optimizations (for example, convert high-cardinality custom metrics to aggregated forms).

<Frame>
  <img alt="The image shows a Datadog dashboard displaying metrics by source, with visual blocks representing &#x22;Other&#x22; at 13.89 and &#x22;APM&#x22; at 10.39, along with smaller segments for &#x22;Profiling&#x22; and &#x22;CSM&#x22;." />
</Frame>

Further options list additional metric sources (logs, APM, RUM, processes, events) and provide links to guidance for optimizing tag usage for analytics.

<Frame>
  <img alt="The image shows the Datadog Metrics Overview interface, highlighting options for generating metrics from various sources like logs, APM, and processes. There are navigation items on the left and options to configure tags for analytics optimization." />
</Frame>

### Metric tagging and cost management

Datadog alerts you to tag growth because many metrics are created with default tags. Excessive tag cardinality increases ingestion and indexing volume. Where appropriate, remove low-value tags (especially on custom metrics) and prefer higher-level aggregation tags like `kube_namespace`, `kube_deployment`, or `service`.

> **warning** Before removing tags, verify Related Assets (dashboards, monitors, alerts) that depend on them — deleting tags can break visualizations and alerts that rely on those tag dimensions.

## Metrics Summary

Click **Summary** in the left panel to list all metrics ingested within a chosen time window (this example uses the past two weeks). Selecting a metric reveals its type, unit, description, historical points, and associated tags.

<Frame>
  <img alt="The image shows a software interface displaying container metrics, including CPU usage details, metadata, and tag information. It includes options for editing metrics and configuring historical data points." />
</Frame>

For example, the `container.cpu.usage` metric in this demo is a gauge measured in nanocores and labeled as container total CPU usage. The tags panel lists all tags attached to the metric — e.g., `container_id` indicates how many distinct container IDs reported during the selected interval (44 distinct IDs in this example). Clicking the tag count expands the list of values.

<Frame>
  <img alt="The image displays a data analytics dashboard, showcasing various container metrics such as CPU and memory usage, alongside Kubernetes-related data such as services and deployments." />
</Frame>

If this were a custom metric, use **Manage Tags** to delete or rename tags to reduce cardinality. For standard metrics, many default tags may carry less cost but still require review before removal because other assets may depend on them. The **Related Assets** section helps find dashboards and monitors that reference the metric.

<Frame>
  <img alt="This image shows a Datadog Metrics Summary page displaying container CPU usage metrics and related configuration details. It includes information about metric types, historical metrics, and related dashboards." />
</Frame>

## Metrics Explorer

Open **Explorer** to build and preview metric queries interactively. Search for metrics like `container.cpu.usage`, set the desired time range (e.g., past month), and experiment with functions and groupings to understand behavior over time.

<Frame>
  <img alt="The image shows a Datadog Metrics Explorer interface displaying a graph of average system CPU usage over time, with a search for container CPU usage metrics." />
</Frame>

Group by higher-level tags such as `kube_deployment` to compare CPU usage across deployments instead of individual containers. This produces cleaner, more actionable dashboards and reduces noise from high-cardinality dimensions.

<Frame>
  <img alt="The image shows a Datadog Metrics Explorer dashboard displaying a line graph of average container CPU usage over time, categorized by Kubernetes deployment." />
</Frame>

## Kubernetes metrics

Datadog collects standard Kubernetes metrics (pod counts, container restarts, node metrics, etc.). Use these metrics to evaluate cluster stability and resource utilization. Note that aggregation functions (avg, sum) change the displayed context — switching from average to sum reveals total counts across the cluster.

<Frame>
  <img alt="The image shows a Datadog Metrics Explorer interface displaying a line graph of Kubernetes container restarts over a period from July 5th to July 10th. The graph indicates a spike in restarts on July 6th." />
</Frame>

Example metric query (Datadog’s metric query syntax combines metric names and aggregation functions):

```text theme={null}
sum:kubernetes.containers.restarts(*)
```

## Volume and cost monitoring

Monitor metric volume with the Volume Overview to track estimated indexed and ingested custom metrics over time. This helps teams spot spikes in metric creation and make targeted changes to avoid unexpected billing.

<Frame>
  <img alt="The image shows a Datadog dashboard displaying Volume Overview graphs for estimated indexed and ingested custom metrics, with filters and configuration options on the sidebar." />
</Frame>

## Logs

Open **Logs Explorer**, set a time range (for example, past 15 days), then review the timeline and log counts. Click a log to inspect raw content and the parsed fields available for filtering.

Example log message from the timeline:

```text theme={null}
[WARNING] No files matching import glob pattern: /etc/coredns/custom/*.server
```

<Frame>
  <img alt="The image is a screenshot of the Datadog Log Explorer interface, showing log details and filtering options within a web browser." />
</Frame>

Use structured fields like `container_name`, `kube_deployment`, `kube_namespace`, and `cluster_name` to filter and isolate issues. Datadog’s search supports natural-language and AI-assisted query generation to speed up filter creation.

## APM (Application Performance Monitoring)

Under **APM → Services (Software Catalog)** Datadog lists instrumented services. Select a service to view traffic, error rates, latency, and suggested SLOs or monitoring actions. You can also link to source code and commits (for example, GitHub) to improve traceability between telemetry and code changes.

<Frame>
  <img alt="The image shows a software management dashboard from a developer portal displaying setup guidance and telemetry recommendations for a Node.js application in a production environment, with status indicators for various services like monitors and error tracking." />
</Frame>

### Trace Explorer and flame graphs

Use Trace Explorer to view traces across a selected window. Clicking a trace shows spans, a flame graph (time spent per operation), and a waterfall view for parent/child relationships and latency breakdown.

<Frame>
  <img alt="The image shows a Datadog dashboard displaying APM traces for a Node.js application, with details on HTTP requests and execution time in a graphical and textual format." />
</Frame>

The flame graph and span table expose middleware, routers, handlers, and downstream calls. For example, a `GET /route2` trace shows spans with duration, HTTP attributes, and additional metadata.

<Frame>
  <img alt="The image is a screenshot of the Datadog application showing APM trace details for a GET /route2 request, including duration, HTTP request details, and span attributes." />
</Frame>

The waterfall view is especially helpful to pinpoint slow downstream services or inefficient middleware chains.

## Dashboards and Infrastructure

Dashboards consolidate metrics, logs, traces, and synthetics to provide a unified observability view. The **Infrastructure** section includes explorers like Kubernetes Explorer for cluster-level troubleshooting and capacity planning.

<Frame>
  <img alt="The image shows a Datadog APM (Application Performance Monitoring) interface displaying traces data with spans, latency breakdown, and a navigation menu on the left." />
</Frame>

### Kubernetes Explorer

Kubernetes Explorer delivers a consolidated view of workloads (Deployments, ReplicaSets, CronJobs), autoscaling status (HPA/VPA), CRDs, storage controllers (CSI), and networking policies. Use it to investigate pod health, HPA behavior, network issues, and resource utilization. If the cluster is offline, the explorer will display no data; when active it surfaces the telemetry you need for debugging and capacity decisions.

## Quick reference — Telemetry types and common tasks

| Telemetry Type      |                                       Use Case | Quick Action                                                     |
| ------------------- | ---------------------------------------------: | ---------------------------------------------------------------- |
| Metrics             |         Resource utilization, trends, alerting | Use Metrics Explorer and group by `kube_deployment` or `service` |
| Logs                | Troubleshooting application errors and context | Filter by `kube_namespace`, `container_name`, or text search     |
| Traces (APM)        |        Latency analysis and dependency mapping | Open Trace Explorer → view flame graph and waterfall             |
| Kubernetes Explorer |      Cluster health and autoscaling visibility | Inspect pods, HPA events, CSI, and network policies              |

## Conclusion

What you learned in this lesson:

* How to navigate the Metrics overview and the difference between standard and custom metrics.
* Inspecting metric details, tags, and related assets in Metrics Summary.
* Querying, grouping, and visualizing metrics in Metrics Explorer to reduce noise and improve dashboards.
* Monitoring metric volume with Volume Overview to manage costs.
* Using Logs Explorer to filter and troubleshoot application logs.
* Navigating APM traces, flame graphs, and Trace Explorer to locate latency sources.
* Leveraging Kubernetes Explorer for cluster-level visibility and capacity planning.

Explore these tools to design dashboards and alerts that meet your operational reliability and FinOps objectives.

## Links and references

* Datadog Metrics documentation: [https://docs.datadoghq.com/metrics/](https://docs.datadoghq.com/metrics/)
* Datadog Logs documentation: [https://docs.datadoghq.com/logs/](https://docs.datadoghq.com/logs/)
* Datadog APM documentation: [https://docs.datadoghq.com/tracing/](https://docs.datadoghq.com/tracing/)
* Kubernetes Basics: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/fd555480-82df-40f4-b8ad-2ea920d51077/lesson/cd6bf4bf-a3bf-477b-9880-1757ec0eb4e8)
