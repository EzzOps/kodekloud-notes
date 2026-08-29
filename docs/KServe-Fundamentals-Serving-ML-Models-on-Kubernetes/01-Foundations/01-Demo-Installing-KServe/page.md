# Demo Installing KServe

Source: https://notes.kodekloud.com/docs/KServe-Fundamentals-Serving-ML-Models-on-Kubernetes/Foundations/Demo-Installing-KServe/page

Step-by-step guide to installing and verifying KServe on Kubernetes using Helm, covering CRDs, controller, serving runtime and LLM configs, cert-manager dependency, and verification commands

Welcome back.

Previously we covered what model serving is and how KServe fits together. In this lesson we'll install KServe on a Kubernetes cluster, explain what each component does, and show how to verify the installation. The commands below are the exact steps used in the demo along with concise verification commands and expected outputs.

<Frame>
  <img alt="The image presents a slide titled &#x22;Before the Demo: The Mental Model,&#x22; highlighting three questions: what to install, why each piece is needed, and how to verify, as part of preparation for a demonstration." />
</Frame>

The mental model: install what KServe needs, understand why each piece is required, and verify the cluster is ready to accept InferenceService or LLMInferenceService manifests.

KServe is distributed as Helm charts. If you haven't used Helm before, think of it as a package manager for Kubernetes—similar to apt or brew, but for deploying complex applications into a cluster.

<Frame>
  <img alt="The image illustrates the installation of KServe using Helm, a package manager for Kubernetes, with icons representing Helm and Kubernetes." />
</Frame>

KServe depends on cert-manager for TLS certificate provisioning and renewal. cert-manager automates creating and managing the certificates many KServe components require.

<Callout icon="lightbulb">
  If your environment is provided as a lab, cert-manager may already be installed. On a fresh cluster you must install cert-manager before KServe; it is a hard dependency.
</Callout>

<Frame>
  <img alt="The image compares a &#x22;Lab Environment&#x22; with a &#x22;Fresh Cluster&#x22; regarding the installation of a cert-manager, noting the lab environment has it pre-installed while the fresh cluster requires it as a hard dependency." />
</Frame>

Overview: KServe installation proceeds in three logical steps

1. Install KServe CRDs (cluster-scoped API types).
2. Install the KServe controller (operator that reconciles InferenceService resources).
3. Install serving runtime and LLM configurations (pre-built templates for model servers and LLM runtimes).

Quick reference: Helm installs and their purpose

| Helm chart      | Purpose                                                                                                          | Example install command                                                                                                                                                         |
| --------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CRDs            | Register cluster-scoped API types such as `InferenceService` and `LLMInferenceService`. Must be installed first. | `helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version v0.17.0`                                                                                              |
| Controller      | KServe controller manager that watches KServe CRs and creates underlying workloads.                              | `helm install kserve oci://ghcr.io/kserve/charts/kserve-resources --version v0.17.0 --namespace kserve --create-namespace --set kserve.controller.deploymentMode=RawDeployment` |
| Runtime configs | ClusterServingRuntimes and LLM config templates used to launch specific model servers.                           | `helm install kserve-runtime-configs oci://ghcr.io/kserve/charts/kserve-runtime-configs --version v0.17.0 --namespace kserve`                                                   |

Step 1 — Install CRDs
CRDs define the Kubernetes API types KServe uses (for example `inferenceservices.serving.kserve.io` and `llminferenceservices.serving.kserve.io`). These are cluster-scoped and must be installed before the controller.

Run:

```bash theme={null}
helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version v0.17.0
helm install kserve-llmisvc-crd oci://ghcr.io/kserve/charts/kserve-llmisvc-crd --version v0.17.0
```

Example (condensed) output:

```text theme={null}
Pulled: ghcr.io/kserve/charts/kserve-crd:v0.17.0
Digest: sha256:0a0ec0cdffd297ce9154ca02dedb544cb797d2ba9ee08009dc06582f2c53e22
NAME: kserve-crd
LAST DEPLOYED: Wed May 27 09:32:01 2026
NAMESPACE: default
STATUS: deployed

Pulled: ghcr.io/kserve/charts/kserve-llmisvc-crd:v0.17.0
Digest: sha256:702f93b1b1975808f8cb2db6586eb4979f06ecbcfe943a994ebd95b0ddfa02b
NAME: kserve-llmisvc-crd
LAST DEPLOYED: Wed May 27 09:32:15 2026
NAMESPACE: default
STATUS: deployed
```

Why this matters: without CRDs, Kubernetes rejects any `InferenceService` or `LLMInferenceService` manifest before KServe has a chance to process it.

Step 2 — Install KServe (controller)
Install the controller into the `kserve` namespace. For demos and local clusters we use `RawDeployment` mode so the controller creates standard Kubernetes Deployments instead of requiring Knative and Istio. This makes it easy to use `kubectl port-forward` and `curl` directly.

Install command:

```bash theme={null}
helm install kserve oci://ghcr.io/kserve/charts/kserve-resources \
  --version v0.17.0 \
  --namespace kserve \
  --create-namespace \
  --set kserve.controller.deploymentMode=RawDeployment
```

If you get a Helm error about a release name already in use, uninstall and retry:

```bash theme={null}
