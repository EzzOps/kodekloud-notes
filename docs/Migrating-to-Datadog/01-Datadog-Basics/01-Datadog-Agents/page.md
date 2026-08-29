# Datadog Agents

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Datadog-Basics/Datadog-Agents/page

Overview of Datadog Agents, their deployment on hosts and Kubernetes, telemetry collection, installation, integrations, authentication, and troubleshooting

In this lesson we explain what Datadog agents are, where they run, and how they collect telemetry (metrics, traces, and logs) from your environment.

An agent is a lightweight software component that runs on a host whose telemetry you want to collect. A host can be a virtual machine (server), a Kubernetes worker node, or a standalone Linux server. The agent runs on that host, gathers metrics/traces/logs and forwards them to Datadog for processing and visualization.

<Frame>
  <img alt="The image illustrates a diagram showing the deployment of a Datadog Agent on a host and within a Kubernetes cluster, with worker nodes." />
</Frame>

## Agent compatibility and integrations

Choose the agent variant that matches the environment where it will run. For example, use the Kubernetes DaemonSet-based Datadog Agent for an EKS cluster (to collect node- and pod-level telemetry) rather than a host-only Linux agent image that isn’t optimized for Kubernetes.

Datadog provides built-in agent integrations for many common platforms and distributions such as Kubernetes, Ubuntu, Docker, Fedora, Red Hat Enterprise Linux, Debian, and SUSE. These integrations simplify setup and enable collection of platform-specific metrics and metadata.

<Frame>
  <img alt="The image lists host integrations with Datadog Agent, featuring logos for Kubernetes, Ubuntu, Docker, Fedora, Red Hat, Debian, and SUSE." />
</Frame>

## Prerequisites: API key and authentication

Before installing or configuring an agent you must generate a Datadog API key in the Datadog console. The agent uses this key to authenticate requests to the Datadog backend; telemetry data is accepted only after successful authentication.

> **lightbulb** Keep your Datadog API key secret. Do not commit it to source control; store it in a secrets manager or environment variables instead.

<Frame>
  <img alt="The image shows a flowchart illustrating the Datadog Agent installation and authentication process. It includes elements labeled &#x22;Sources,&#x22; &#x22;Agent,&#x22; and &#x22;Datadog Site,&#x22; with arrows indicating the flow of information." />
</Frame>

## Installing the agent on Linux hosts

On Linux, select the installation instructions that match your distribution (for example, Ubuntu or RHEL) and follow the distro-specific steps in the Datadog docs. After installing and configuring the agent (including setting the API key and enabling any integrations), the agent starts sending telemetry to Datadog.

<Frame>
  <img alt="The image outlines steps for installing the Datadog Agent on a Linux host, including selecting a Linux distribution, following installation steps, and running the agent to send data to Datadog." />
</Frame>

For detailed distro-specific installation instructions, see the Datadog Agent documentation: [https://docs.datadoghq.com/agent/](https://docs.datadoghq.com/agent/)

## Datadog Agents in Kubernetes

In Kubernetes environments there are two complementary agent types:

| Agent Type                 | Runs As                      | Primary Responsibility                                      | Typical Configuration                                    |
| -------------------------- | ---------------------------- | ----------------------------------------------------------- | -------------------------------------------------------- |
| Datadog Cluster Agent      | Deployment                   | Cluster-wide telemetry, coordination, and API aggregation   | Set replicas appropriately for cluster size and workload |
| Datadog Agent (Node Agent) | DaemonSet (one pod per node) | Node- and application-level telemetry for pods on each node | Deploy Cluster Agent + Node Agent for full coverage      |

Each agent has distinct responsibilities; configure both so you get complete telemetry coverage (cluster-level and node/pod-level).

> **warning** Ensure the Cluster Agent has sufficient replicas for your cluster size and telemetry volume. Underprovisioning can overload instances; overprovisioning wastes resources. Monitor resource usage and scale replicas accordingly.

## Troubleshooting and debugging tools

Datadog agents include built-in debugging tools you can run inside the agent container (or on the host) to inspect configuration, check status, validate connectivity, and create diagnostic bundles for Datadog Support.

Common steps:

* Exec into a Datadog agent container (adjust namespace and selector to match your deployment):

```bash theme={null}
kubectl -n datadog exec -it $(kubectl -n datadog get pods -l app=datadog -o jsonpath='{.items[0].metadata.name}') -- bash
```

* Check agent status:

```bash theme={null}
datadog-agent status
```

* Generate a diagnostic bundle (flare) for Datadog support:

```bash theme={null}
datadog-agent flare
```

These commands can quickly surface configuration issues, integration failures, and connectivity problems.

<Frame>
  <img alt="The image describes the internal functioning of a Datadog Agent with two steps: running commands on the agent, and verifying its configuration and status." />
</Frame>

## Summary and next steps

* Datadog Agents run on hosts or in Kubernetes to collect metrics, traces, and logs, and forward them to Datadog.
* Choose the correct agent variant for your environment (Linux distro vs Kubernetes DaemonSet/Deployment).
* Keep your API key secure and follow Datadog’s distro-specific installation steps.
* Use the built-in debugging commands to validate agent status and create diagnostic bundles when needed.

References and further reading:

* Datadog Agent documentation: [https://docs.datadoghq.com/agent/](https://docs.datadoghq.com/agent/)
* Datadog console (API keys): [https://app.datadoghq.com/account/settings#api](https://app.datadoghq.com/account/settings#api)

That’s it for this lesson — hope you found it useful.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/10421186-d141-4fde-9847-73ea4e4e675a/lesson/bfa65100-db9e-44de-90c3-9968676e7a86)
