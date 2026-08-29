# Demo Reading InferenceService Status

Source: https://notes.kodekloud.com/docs/KServe-Fundamentals-Serving-ML-Models-on-Kubernetes/Troubleshooting-Basics/Demo-Reading-InferenceService-Status/page

Guide to diagnosing and fixing KServe InferenceService readiness failures when serving Qwen on Kubernetes, covering storage authentication/path errors and memory OOMKilled issues.

If you've deployed models on Kubernetes before, you've probably seen `READY: False` and had to wait. That's normal — downloading and initializing a model from remote storage can take time.

But what if `READY` stays `False` for many minutes? Or never becomes `True`? Kubernetes contains the diagnostic information you need — you just need to know where to look and how to interpret it.

<Frame>
  <img alt="The image shows a user icon labeled &#x22;Users&#x22; connected to a text document with Kubernetes and a magnifying glass symbol, likely illustrating user interaction with Kubernetes documentation or logs." />
</Frame>

This article walks through two realistic failure scenarios when serving the Qwen model with KServe, and shows how to read the Kubernetes/KServe output to find root causes and fixes. One scenario involves an authentication/path issue that can be misleading at first.

Quick first step — check the InferenceService status:

```bash theme={null}
kubectl get inferenceservice -n kserve-inference
```

* If `READY` is `False` and `AGE` is only tens of seconds, the service is usually still initializing (storage initializer downloading files).
* If several minutes pass with no `URL` and `READY: False`, start troubleshooting — something likely failed.

<Frame>
  <img alt="The image shows the text &#x22;Qwen&#x22; with a star-like symbol above a brain icon labeled &#x22;Model.&#x22; It has a dark background with &#x22;© Copyright KodeKloud&#x22; at the bottom left." />
</Frame>

The `AGE` column is a helpful clue: if a service deployed five minutes ago is still `False` with no URL, it likely failed during initialization.

<Frame>
  <img alt="The image displays a user interface element titled &#x22;Kubectl&#x22; with a model icon and a &#x22;Still false&#x22; button, alongside an &#x22;Age Column&#x22; label." />
</Frame>

Below are two common scenarios, how the failure appears, and how to fix it.

***

## Scenario 1 — Broken storage URI (typo or wrong repo)

Apply a deliberately broken InferenceService to reproduce the error:

```bash theme={null}
kubectl apply -f qwen-model-broken.yaml
kubectl get inferenceservice -n kserve-inference
```

Short example output:

```bash theme={null}
NAME         URL   READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION   AGE
qwen-model   False
```

Describe the InferenceService for more detail:

```bash theme={null}
kubectl describe inferenceservice qwen-model -n kserve-inference
```

Look at the `status` section, especially `conditions`. A healthy condition shows `Status: True` and `Type: PredictorReady` (or `Ready`). For failures, you'll see `Status: False` and `reason` + `message` fields with diagnostic text.

Example storage-initializer failure (truncated for clarity):

```plaintext theme={null}
Status: False
Type: Stopped
Deployment Mode: Standard
Model Status:
Copies: 
Failed Copies: 0
Last Failure Info:
  Exit Code: 1

2026-05-29 18:05:31.179  storage.initialize INFO  Initializing, args: (src_uri, dest_path)
2026-05-29 18:05:31.179  storage.initialize INFO  Copying contents of hf://Qwen/Qwen2.5-0.5B-Instruct to local
2026-05-29 18:05:31.615  storage.initialize ERROR Storage error when accessing hf://Qwen/Qwen2.5-0.5B-Instruct: 401 Client Error.
Repository Not Found for url: https://huggingface.co/api/models/Qwen/Qwen2.5-0.5B-Instruct/revision/main.
Please make sure you specified the correct `repo_id` and `repo_type`.
If you are trying to access a private or gated repo, make sure you are authenticated. For more details, see https://huggingface.co/docs/huggingface_hub/authentication
Invalid username or password.
2026-05-29 18:05:31.615  storage.initialize ERROR  Storage initialization failed: HuggingFace authentication failed. Set HF_TOKEN or request access to the gated repository.
Reason: ModelLoadFailed
States:
  Active Model State: FailedToLoad
  Target Model State: FailedToLoad
  Transition Status: BlockedByFailedLoad
Observed Generation: 1
Events:
  Warning  VirtualServiceCRDNotFound  Istio VirtualService CRD not present; VirtualService reconciliation skipped. If you do not use Istio, set ingress.disableIstioVirtualHost=true.
```

Important context: the combination of `Repository Not Found` and `401` can be confusing. It may indicate:

* A typo in the `storageUri` (e.g., `Instruct` vs `Instuct`) — the path is wrong, so the API returns "not found".
* Or a private/gated repository that requires authentication (e.g., an `HF_TOKEN`).

When `kubectl describe` is ambiguous, inspect pod and init container logs:

```bash theme={null}
kubectl get pods -n kserve-inference -w
