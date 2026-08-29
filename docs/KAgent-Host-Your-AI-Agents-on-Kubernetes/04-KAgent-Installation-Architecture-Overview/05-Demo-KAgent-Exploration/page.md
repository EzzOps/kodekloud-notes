# Demo KAgent Exploration

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KAgent-Installation-Architecture-Overview/Demo-KAgent-Exploration/page

Step-by-step guide to install and configure KAgent on Kubernetes, manage ModelConfig and provider secrets, enable tools and k8s-agent, and interact via UI and kagent CLI.

This guide walks through a progressive installation and configuration of KAgent on Kubernetes. You'll learn how to:

* Install KAgent CRDs and the KAgent Helm chart.
* Store LLM provider secrets and create a ModelConfig CRD.
* Install KAgent with a minimal configuration, then enable the built-in tools and the `k8s-agent`.
* Interact with the Kubernetes agent via the KAgent UI and the `kagent` CLI.
* Inspect controller logs and observe agent-driven actions (e.g., creating manifests).

Prerequisites, example commands, and troubleshooting tips are included. Ensure you have a Kubernetes cluster, `kubectl`, `helm`, and the `kagent` CLI (if invoking agents from the terminal). Also set any referenced environment variables (for example, `OPENAI_API_KEY`) in your shell.

***

## Prerequisites

| Requirement           | Purpose                     | Example / Notes                              |
| --------------------- | --------------------------- | -------------------------------------------- |
| Kubernetes cluster    | Run KAgent components       | Minikube, Kind, or managed cluster           |
| kubectl               | Inspect cluster resources   | `kubectl version --client`                   |
| helm                  | Install KAgent charts       | `helm version`                               |
| kagent CLI (optional) | Invoke agents from CLI      | See `kagent invoke` examples below           |
| API keys / secrets    | LLM provider authentication | `OPENAI_API_KEY` stored as Kubernetes secret |

***

## 1) Install the KAgent CRDs

The KAgent Helm charts are published to an OCI registry on GitHub: `oci://ghcr.io/kagent`. Install the CRDs into the `kagent` namespace (the namespace will be created if missing):

```bash theme={null}
