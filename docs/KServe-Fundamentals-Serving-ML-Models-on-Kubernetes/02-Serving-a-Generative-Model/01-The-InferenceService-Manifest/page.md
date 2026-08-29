# The InferenceService Manifest

Source: https://notes.kodekloud.com/docs/KServe-Fundamentals-Serving-ML-Models-on-Kubernetes/Serving-a-Generative-Model/The-InferenceService-Manifest/page

Describes KServe InferenceService manifest for deploying Hugging Face models, explaining modelFormat, storageUri, resource settings, and deployment lifecycle

Welcome to this lesson of KServe Fundamentals.

Earlier we built the mental model for model serving: what it is, how KServe sits on top of Kubernetes, and what the pieces are. In this lesson we begin using that model. We'll deploy a real language model — a small, quantized Qwen variant pulled from the Hugging Face Hub — and focus on the InferenceService manifest, the single Kubernetes resource that drives a KServe deployment.

<Frame>
  <img alt="The image is a list of objectives related to deploying a language model, using a quantized version of Qwen, pulling it from Hugging Face, and understanding the KServe InferenceService manifest." />
</Frame>

If you've used Kubernetes before this will look familiar: every desired object in the cluster is declared in YAML — Deployment, Service, ConfigMap, etc. KServe follows the same declarative pattern by introducing a custom resource (CRD) named InferenceService. You declare what you want (model name, format, storage location, resource needs) and KServe reconciles that desired state into running pods and services.

<Frame>
  <img alt="The image depicts a flowchart illustrating the relationship between KServe, a custom resource definition (CRD), and Kubernetes with the text &#x22;It's Just a YAML File&#x22; above and &#x22;InferenceService&#x22; below." />
</Frame>

## Minimal InferenceService manifest for a Hugging Face model

Below is a compact InferenceService manifest that instructs KServe to serve a Hugging Face model. This minimal YAML is sufficient to get a model running with the appropriate KServe runtime:

```yaml theme={null}
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: qwen-model
  namespace: kserve-inference
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      storageUri: "hf://Qwen/Qwen2.5-0.5B-Instruct"
      args:
        - --backend=huggingface
```

Key parts explained:

* `apiVersion` and `kind` identify the resource type to the Kubernetes API server.
* `metadata.name` is the InferenceService name; it appears in logs, events, and URLs.
* `metadata.namespace` scopes the resource. Use a dedicated namespace (e.g., `kserve-inference`) to separate concerns and apply RBAC cleanly.
* `spec.predictor` is the core section that defines the model, runtime selection, and serving behavior.

Use the following resources to learn more:

* KServe docs: [https://kserve.github.io](https://kserve.github.io)
* Kubernetes concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* Hugging Face Hub: [https://huggingface.co](https://huggingface.co)

<Frame>
  <img alt="The image is a diagram titled &#x22;SPEC.PREDICTOR – The Heart of It,&#x22; showing two components: &#x22;modelFormat.name&#x22; which tells KServe the model type, and &#x22;storageUri,&#x22; which defines where the model is stored." />
</Frame>

## predictor.model — the two fields you’ll set most often

Two fields under `spec.predictor.model` are nearly always required:

* `modelFormat.name` — picks the serving runtime to use. For Hugging Face models set `huggingface`. KServe maps this to the appropriate serving runtime automatically (no image specification needed).
* `storageUri` — where your model files come from. For Hugging Face Hub models use an `hf://` URI, e.g. `hf://Qwen/Qwen2.5-0.5B-Instruct`. KServe's storage initializer downloads these files into the pod before the server starts.

> **lightbulb** If your model is private on Hugging Face, you must provide credentials (e.g., a token) via a Kubernetes Secret and reference it in the InferenceService (or configure cluster-level storage credentials). Check the KServe documentation for the correct secret keys and mounting patterns.

## Resource requests and limits — why they matter

The minimal manifest will work, but production deployments should include resource requests and limits so pods schedule reliably and cannot consume unlimited cluster resources.

* `resources.requests` — the minimum CPU/memory required to schedule the pod.
* `resources.limits` — the maximum CPU/memory the pod may consume.

Example manifest with CPU and memory set. This quantized Qwen model runs on CPU-only hardware, which is a common and cost-effective choice for smaller quantized language models:

```yaml theme={null}
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: qwen-model
  namespace: kserve-inference
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      storageUri: "hf://Qwen/Qwen2.5-0.5B-Instruct"
      args:
        - --backend=huggingface
    resources:
      requests:
        cpu: "1"
        memory: "2Gi"
      limits:
        cpu: "2"
        memory: "6Gi"
```

Quick guidance table:

| Field                | Purpose                                                 | Example                           |
| -------------------- | ------------------------------------------------------- | --------------------------------- |
| `modelFormat.name`   | Selects the KServe runtime for your model type          | `huggingface`                     |
| `storageUri`         | Model storage location; supports `hf://`, S3, GCS, etc. | `hf://Qwen/Qwen2.5-0.5B-Instruct` |
| `resources.requests` | Minimum resources to schedule the pod                   | `cpu: "1"`, `memory: "2Gi"`       |
| `resources.limits`   | Upper bound for container resource consumption          | `cpu: "2"`, `memory: "6Gi"`       |

> **warning** Sizing resources incorrectly can cause pods to evict, fail to schedule, or starve other workloads. Start with conservative requests, test throughput and latency, then adjust limits. Monitor CPU, memory, and pod restarts after deployment.

## What happens when you apply the manifest

When you run:

kubectl apply -f \<manifest.yaml>

the KServe controller reconciles the InferenceService:

1. It reads `modelFormat` and selects the matching cluster serving runtime (e.g., the Hugging Face runtime).
2. The controller synthesizes a pod spec. An init container (the storage initializer) downloads model files from `storageUri` into local volume storage.
3. Once the files are in place, the serving container starts, loads the model, and exposes an HTTP endpoint.
4. The controller updates the InferenceService status with an externally reachable URL when the service becomes ready. Use that URL to send prediction requests.

This flow is fully declarative: you describe the desired state and KServe makes the cluster match it.

## Recap — the InferenceService manifest is the core

The InferenceService manifest is the single source of truth for model serving in KServe:

* Choose `modelFormat.name` to automatically select the right runtime.
* Point `storageUri` to your model storage (Hugging Face Hub, S3, GCS, etc.).
* Set `resources.requests` and `resources.limits` so the deployment schedules predictably.

We will now walk through the full deployment used for this module and explain why each choice was made.

- [Watch Video](https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/a270a816-b8e6-47f2-8ef9-7cf5b97f8890/lesson/f2c42add-90db-4b30-af7e-d3472936ec5a)
