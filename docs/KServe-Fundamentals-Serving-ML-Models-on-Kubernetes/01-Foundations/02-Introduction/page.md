# If the release exists or was partially created, uninstall (adjust namespace if needed)
helm uninstall kserve --namespace kserve || true
```

After a successful install you should see output like:

```text theme={null}
Pulled: ghcr.io/kserve/charts/kserve-resources
Digest: sha256:[SECRET_REDACTED]
NAME: kserve
LAST DEPLOYED: Wed May 27 09:35:25 2026
NAMESPACE: kserve
STATUS: deployed
```

Wait for the KServe controller and its webhook to be fully ready before creating any InferenceService resources:

```bash theme={null}
kubectl rollout status deployment/kserve-controller-manager -n kserve
```

Expected success message:

```text theme={null}
deployment/kserve-controller-manager successfully rolled out
```

Step 3 — Install serving runtimes and LLM configs
Serving runtimes register templates used to deploy model servers (scikit-learn, XGBoost, Hugging Face, TorchServe, Triton, etc.). LLMInferenceService configs provide LLM-specific runtime settings.

Install the runtime configs:

```bash theme={null}
helm install kserve-runtime-configs oci://ghcr.io/kserve/charts/kserve-runtime-configs \
  --version v0.17.0 \
  --namespace kserve
```

Inspect the release and installed resources:

```bash theme={null}
helm status kserve-runtime-configs
helm get all kserve-runtime-configs
```

You may see output indicating whether ClusterServingRuntimes or LLM configs are enabled:

```text theme={null}
✔ ClusterServingRuntimes: Enabled
✖ LLMInferenceServiceConfigs: Disabled
```

Quick verification checks

1. Confirm KServe controller pods are running:

```bash theme={null}
kubectl get pods -n kserve
```

Example:

```text theme={null}
NAME                                          READY   STATUS    RESTARTS   AGE
kserve-controller-manager-6c6d84c696-lfws4    2/2     Running   0          98s
```

2. Confirm CRDs are installed (look for KServe CRDs):

```bash theme={null}
kubectl get crds | grep kserve
```

Example output:

```text theme={null}
clusterservingruntimes.serving.kserve.io
clusterstoragecontainers.serving.kserve.io
inferencegraphs.serving.kserve.io
inferenceservices.serving.kserve.io
llminferenceserviceconfigs.serving.kserve.io
llminferenceservices.serving.kserve.io
servingruntimes.serving.kserve.io
trainedmodels.serving.kserve.io
```

If `inferenceservices.serving.kserve.io` appears, Kubernetes recognizes the InferenceService API.

3. Confirm serving runtimes are registered:

```bash theme={null}
kubectl get clusterservingruntimes
```

You should see entries for supported runtimes (scikit-learn, XGBoost, Hugging Face, Triton, etc.). These are the templates KServe uses when creating model deployments.

Summary

* Installation consists of three Helm installs: CRDs, controller, and runtime configs.
* Typical verification: controller pods (`kubectl get pods -n kserve`), CRDs (`kubectl get crds | grep kserve`), and registered serving runtimes (`kubectl get clusterservingruntimes`).
* Use `RawDeployment` mode in demos/local clusters to avoid installing Knative/Istio and enable direct access via port-forwarding.

Once all components are healthy, you're ready to create `InferenceService` and `LLMInferenceService` resources. These steps will be applied live in the subsequent demonstration.

Links and references

* KServe repository and charts: [https://github.com/kserve/kserve](https://github.com/kserve/kserve)
* Helm documentation: [https://helm.sh/docs/](https://helm.sh/docs/)
* cert-manager: [https://cert-manager.io/](https://cert-manager.io/)
* Kubernetes concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/5231587b-53d5-4ea2-a084-44550d4ce9bb/lesson/43f31c93-c249-44ea-b581-f71091f4a80e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/5231587b-53d5-4ea2-a084-44550d4ce9bb/lesson/a357e18b-d68a-4427-9760-2415a5adb9cf" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/KServe-Fundamentals-Serving-ML-Models-on-[AWS_SECRET_ACCESS_KEY]

Guide to deploying and operating generative and predictive ML models on Kubernetes using KServe, including installation, InferenceService and LLMISvc, serving patterns, and troubleshooting

Welcome to *KServe Fundamentals: Serving ML Models on Kubernetes*. I'm Chris Short, and I'll guide you through deploying and operating machine learning models on Kubernetes using KServe.

As organizations adopt AI and machine learning, the ability to reliably deploy models at scale has become essential. Model development is only part of the journey — production delivery requires a platform that can handle deployment, autoscaling, routing, and operational observability. KServe is a Kubernetes-native model serving platform built to simplify these tasks for both traditional ML and generative AI (LLM) workloads. It standardizes model serving while leveraging Kubernetes' orchestration features.

This lesson covers KServe fundamentals and provides hands-on experience serving models on Kubernetes. We'll prepare your environment, install KServe, and walk through both generative and predictive serving patterns.

Prerequisites

* A Kubernetes cluster with sufficient resources (CPU, RAM, and storage) for model serving.
* kubectl configured to point to your target cluster.
* Helm 3 installed.
* Appropriate cluster permissions to create CRDs and namespace resources.

Install KServe (example)

* The following Helm commands install the KServe CRDs and the KServe controller in `RawDeployment` mode. Adjust versions or values to match your environment.

```bash theme={null}
helm install kserve-llmisvc-crd oci://ghcr.io/kserve/charts/kserve-llmisvc-crd --version v0.17.0
helm install kserve oci://ghcr.io/kserve/charts/kserve --version v0.17.0 \
  --namespace kserve \
  --create-namespace \
  --set kserve.controller.deploymentMode=RawDeployment
```

We'll start with the fundamentals: what model serving is, KServe architecture, and the core components (InferenceService, LLMISvc, predictors, and transformers) that power model serving on Kubernetes.

<Frame>
  <img alt="The image shows a man speaking into a microphone with a presentation slide titled &#x22;KServe Fundamentals&#x22; displaying a bulleted list of topics related to models and troubleshooting." />
</Frame>

What you'll do in this course

* Deploy a quantized Qwen large language model using KServe, creating the appropriate KServe serving resources (`LLMISvc` or `InferenceService`) and sending inference requests.
* Serve generative AI workloads and observe how request formats and response handling differ from traditional predictive models.
* Deploy a text-classification model to learn patterns for predictive inference (batch vs. real-time, request/response schemas).
* Inspect InferenceService status, identify deployment issues, and troubleshoot common problems in KServe environments.
* Reinforce concepts with demonstrations, hands-on labs, and quizzes.

Comparing LLM and predictive model request formats

* Generative LLMs often use chat-style prompts or structured inputs with streaming responses and token-level outputs.
* Predictive/classification models typically accept plain text or feature vectors and return structured labels or probabilities.

<Frame>
  <img alt="The image is a slide from a presentation titled &#x22;KServe Fundamentals: Serving ML Models on Kubernetes,&#x22; comparing two request formats: Qwen, which uses chat-style prompts, and Classifier, which takes plain text input. A person is shown in the corner." />
</Frame>

Course outline (high level)

| Module                | Focus                                                      | Outcomes                                                            |
| --------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------- |
| Fundamentals          | KServe architecture and core components                    | Understand CRDs, controllers, predictors, and routing               |
| Generative (LLMs)     | Deploying and serving LLMs with `LLMISvc`                  | Deploy a quantized Qwen model, send chat-style requests             |
| Predictive models     | Serving classifiers and regressors with `InferenceService` | Deploy text-classification models and validate responses            |
| Troubleshooting & Ops | Inspecting status and resolving deployments                | Learn to debug InferenceService conditions and common failure modes |
| Labs & Community      | Hands-on exercises and support                             | Apply concepts in real clusters and collaborate in CodeCloud        |

Links and references

* [KServe Documentation](https://kserve.github.io/website/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Helm Documentation](https://helm.sh/docs/)

Throughout the course you'll practice deploying, serving, and troubleshooting both generative and predictive ML models using KServe on Kubernetes. Each hands-on module includes sample manifests and inference examples so you can reproduce the demos in your own cluster.

<Callout icon="lightbulb">
  Before running the Helm commands, ensure your kubectl context points to the Kubernetes cluster where you intend to install KServe and that you have sufficient permissions to create cluster-level resources.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/5231587b-53d5-4ea2-a084-44550d4ce9bb/lesson/92be25d3-6011-4a0d-a9fc-68982ee9d025" />
</CardGroup>
