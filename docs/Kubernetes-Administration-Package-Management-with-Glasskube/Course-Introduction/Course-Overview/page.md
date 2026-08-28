# or
kubectl describe pod <pod-name> -n kserve-inference
kubectl logs <pod-name> -c storage-initializer -n kserve-inference
```

With Hugging Face URIs, if you must be logged in on huggingface.co to view the model, KServe also needs credentials (for example, set `HF_TOKEN`). If the path is wrong, correct the `storageUri` in your manifest and reapply.

***

## Scenario 2 — Out of memory (OOMKilled)

ML models include weights that must be loaded into RAM. If a container is constrained to less memory than required, the kubelet will kill it (OOMKilled). This leads to restarts and the Revision/Deployment failing to reach minimum availability, causing the InferenceService to remain `False`.

Apply a manifest that intentionally causes OOM:

```bash theme={null}
kubectl apply -f qwen-model-oomkilled.yaml
kubectl get pods -n kserve-inference
```

You may observe init containers or the main container being restarted with `OOMKilled`. Describing the InferenceService will show `PredictorReady: False` and messages about minimum availability or scheduling:

```yaml theme={null}
Predictor:
  Conditions:
    - Last Transition Time: 2026-05-29T18:10:52Z
      Reason: Predictor ingress not created
      Status: False
      Type: IngressReady
    - Last Transition Time: 2026-05-29T18:10:52Z
      Message: Deployment does not have minimum availability.
      Reason: MinimumReplicasUnavailable
      Status: False
      Type: PredictorReady
    - Last Transition Time: 2026-05-29T18:11:24Z
      Reason: Predictor ingress not created
      Status: False
      Type: Ready
      Severity: Info
  Last Transition Time: 2026-05-29T18:10:52Z
  Status: False
  Type: Stopped
  Deployment Mode: Standard
  Model Status:
    Copies:
      Failed Copies: 0
    States:
      Active Model State:
      Target Model State: Pending
      Transition Status: InProgress
  Observed Generation: 1
Events:
  Warning  VirtualServiceCRDNotFound  Istio VirtualService CRD not present; VirtualService reconciliation skipped. If you do not use Istio, set ingress.disableIstioVirtualHost=true.
```

`Deployment does not have minimum availability` commonly indicates:

* Kubernetes couldn't schedule the pod because nodes lack sufficient memory.
* Or the pod is repeatedly OOMKilled because requests/limits are too low.

Example manifest that intentionally sets too-small memory requests/limits:

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
      storageUri: "hf://Qwen/Qwen-2.5-0.5B-Instruct"
      args:
        - --backend=huggingface
    resources:
      requests:
        memory: "512Mi"
      limits:
        memory: "512Mi"
```

Setting both `requests` and `limits` to `512Mi` is too small for the Qwen model and will likely produce `OOMKilled`. A common starting point for Qwen is `requests: 2Gi` and `limits: 4Gi`. Adjust these values according to the model size and available node resources, or schedule on nodes with more memory.

<Frame>
  <img alt="The image displays a terminal output with information on a deployment, showing status updates and reasons for issues related to a predictor ingress and minimum replicas." />
</Frame>

When you see `Deployment does not have minimum availability`, either increase the pod memory request/limit or provision nodes with sufficient memory so Kubernetes can schedule the pod.

***

## Troubleshooting checklist (quick reference)

| Step                   | Command / Action                                                     | Purpose                                                   |
| ---------------------- | -------------------------------------------------------------------- | --------------------------------------------------------- |
| Check InferenceService | `kubectl get inferenceservice -n kserve-inference`                   | See basic `READY`, `URL`, `AGE` status                    |
| Inspect conditions     | `kubectl describe inferenceservice qwen-model -n kserve-inference`   | Read `status.conditions` -> `reason` and `message`        |
| Watch pods             | `kubectl get pods -n kserve-inference -w`                            | See pod creation, restarts, scheduling events             |
| Pod details            | `kubectl describe pod <pod-name> -n kserve-inference`                | Check events, status, and reasons (OOMKilled, scheduling) |
| Init container logs    | `kubectl logs <pod-name> -c storage-initializer -n kserve-inference` | See storage initialization errors (auth, repo not found)  |
| Predictor logs         | `kubectl logs <pod-name> -c predictor -n kserve-inference`           | Runtime errors from the serving process                   |

<Callout icon="lightbulb">
  Read the `conditions` -> `message` field first. It's the single most useful piece of information KServe provides about why an InferenceService isn't becoming ready.
</Callout>

Practical troubleshooting based on messages:

* If `message` indicates storage or repository errors:
  * Verify the `storageUri` for typos (e.g., `Instruct` vs `Instuct`).
  * If the model is private/gated, set `HF_TOKEN` in your environment or use a repo you have access to. See Hugging Face authentication docs: [https://huggingface.co/docs/huggingface\_hub/authentication](https://huggingface.co/docs/huggingface_hub/authentication)
  * Inspect storage-initializer logs:
    ```bash theme={null}
    kubectl logs <pod-name> -c storage-initializer -n kserve-inference
    ```

* If `message` indicates scheduling/minimum availability or pods show `OOMKilled`:
  * Check pod status and events:
    ```bash theme={null}
    kubectl get pods -n kserve-inference
    kubectl describe pod <pod-name> -n kserve-inference
    ```
  * Increase `resources.requests.memory` and `resources.limits.memory` in your InferenceService manifest to meet the model’s RAM needs (for example, `requests: "2Gi"`, `limits: "4Gi"` for Qwen as a starting point), then reapply.

After applying fixes, watch the InferenceService until `READY` becomes `True`:

```bash theme={null}
kubectl get inferenceservice -n kserve-inference -w
```

If the `conditions`/`events` don’t provide enough detail, inspect pod logs (init and main containers). Storage initializer and predictor logs typically reveal the root cause: bad path, authentication failure, or memory allocation problems.

Useful links and references:

* KServe documentation: [https://kserve.github.io/](https://kserve.github.io/) (KServe concepts and troubleshooting)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/) (kubectl, pods, events)
* Hugging Face authentication: [https://huggingface.co/docs/huggingface\_hub/authentication](https://huggingface.co/docs/huggingface_hub/authentication)

By following this checklist and reading the `reason` and `message` fields in KServe conditions, you can distinguish a slow initial load from an actual failure and take the correct corrective action.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/a36eb0a9-2bc9-49ad-81eb-911c642e9b74/lesson/a48f15fe-664e-4047-b40f-54bfe40e0e05" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/a36eb0a9-2bc9-49ad-81eb-911c642e9b74/lesson/73db3bbb-9a03-45e6-b30b-d2289401fd9f" />
</CardGroup>


# Course Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Course-Introduction/Course-Overview/page

Hands-on course teaching Kubernetes package management with Glasskube, covering Helm, installing five packages, observability, lifecycle strategies, and GitOps through browser-based labs.

Welcome to "Kubernetes Administration: Install Your First Five Packages with Glasskube."

I'm Jake Page, and in this lesson we'll cover practical Kubernetes package management using Glasskube. This course emphasizes hands-on, browser-based labs so you can immediately apply the commands and configurations demonstrated here. If you want to move from theory to practice in minutes, this course is built for that.

Quick cluster checks and Glasskube installation (example session)

```bash theme={null}
controlplane ~ ➜ kubectl get nodes
NAME            STATUS   ROLES           AGE     VERSION
control-plane   Ready    control-plane   82s     v1.21.5

controlplane ~ ➜ kubectl get ns
NAME              STATUS   AGE
default           Active   82s
kube-node-lease   Active   82s
kube-public       Active   82s
kube-system       Active   82s

controlplane ~ ➜ curl -LO https://github.com/glasskube/glasskube/releases/download/v0.17.0/glasskube_v0.17.0.deb
controlplane ~ ➜ sudo dpkg -i glasskube_v0.17.0.deb
(Reading database ... 21876 files and directories currently installed.)
Preparing to unpack glasskube (0.17.0) ...
Unpacking glasskube (0.17.0) ...
Setting up glasskube (0.17.0) ...

controlplane ~ ➜
```

What you'll learn — course map

| Section                           | Key topics covered                                                                         | Tools & references                                                                                                                                                                      |
| --------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package management fundamentals   | Current landscape of Kubernetes package management; how packages differ from raw manifests |                                                                                                                                                                                         |
| Tooling                           | Kubernetes manifests best practices; packaging and releasing with Helm                     | [Helm](https://helm.sh)                                                                                                                                                                 |
| Glasskube (core focus)            | Where Glasskube fits in workflows; installing and managing packages with Glasskube         | Glasskube CLI and UI                                                                                                                                                                    |
| Package installation (hands-on)   | Deploy advanced monitoring and observability stacks; tailing logs and metrics              | `kube-prometheus-stack` ([chart repo](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)); [KubeTail](https://github.com/johanhaleby/kubetail) |
| Lifecycle & multi-repo strategies | Package lifecycle management, multi-repo approaches, and version control                   | Git + Glasskube patterns                                                                                                                                                                |
| GitOps with Glasskube             | Managing packages via GitOps workflows and automation                                      | GitOps workflows, CI/CD integration                                                                                                                                                     |

This course is focused on actionable workflows:

* Start with cluster validation and environment setup.
* Learn manifest and Helm best practices to keep deployments predictable.
* Use Glasskube to simplify package installations, updates, and rollbacks.
* Apply observability patterns: monitoring, logging, and alerting using community charts.
* Explore lifecycle and multi-repo strategies that scale across teams.
* Adopt GitOps practices for declarative, auditable package management.

<Frame>
  <img alt="A person is sitting in front of a microphone with a list of topics related to package and lifecycle management displayed beside them." />
</Frame>

Course format and labs

* Interactive browser labs let you run the same commands shown in the lesson against a live cluster sandbox.
* Step-by-step exercises guide you through installing five common packages with Glasskube, validating deployments, and troubleshooting common issues.
* Each lab includes expected outputs, troubleshooting tips, and links to the upstream chart or project.

<Callout icon="lightbulb">
  Join the community to ask questions, share insights, and collaborate with fellow learners as you progress through the labs and exercises.
</Callout>

Ready to get started? Enroll now and take the first step toward mastering Kubernetes package management with Glasskube.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/6a6d19ed-9f2a-45fc-8c60-f748be0831b2/lesson/eecd6706-9e26-4f67-ab88-476af9ddf006" />
</CardGroup>
