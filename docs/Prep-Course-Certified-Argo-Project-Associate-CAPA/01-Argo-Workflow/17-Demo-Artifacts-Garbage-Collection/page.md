# change "type: ClusterIP" to "type: NodePort" and save
```

After editing, confirm the NodePort mapping:

```bash theme={null}
kubectl -n argo get po,svc | grep -i minio
```

Example output showing NodePorts (9000 and 9001 mapped to high-numbered node ports):

```bash theme={null}
pod/minio-5cb4ff75c9-stmmw   1/1   Running   0   4h40m
service/minio               NodePort    10.108.36.67   <none>   9000:30648/TCP,9001:30731/TCP   4h40m
```

* Internal MinIO UI port: 9001
* Example NodePort for the UI: `30731` (your cluster will assign different high ports)

Table: quick port summary

| Internal port | Example NodePort | Purpose                             |
| ------------- | ---------------: | ----------------------------------- |
| 9000          |            30648 | S3 API endpoint (object operations) |
| 9001          |            30731 | MinIO web console (UI)              |

Note: For secure/demo access without changing services, you can run:

```bash theme={null}
kubectl -n argo port-forward svc/minio 9001:9001
# then open http://localhost:9001 in your browser
```

## 3. Retrieve MinIO credentials

Argo stores the MinIO credentials as Kubernetes secrets in the `argo` namespace. Decode them with:

```bash theme={null}
kubectl -n argo get secrets my-minio-cred -o json | jq -r .data.accesskey | base64 --decode
kubectl -n argo get secrets my-minio-cred -o json | jq -r .data.secretkey | base64 --decode
```

Example output:

```text theme={null}
admin
adminpassword
```

Use these values to sign in to the MinIO web console (NodePort or port-forward URL).

## 4. Browse buckets and archived workflow logs

Once authenticated, you will see buckets created by Argo Workflows (for example `my-bucket`) and the objects within. These objects include archived logs and workflow artifacts produced by completed runs.

If you browse into a bucket you will see items corresponding to workflows and their logs:

<Frame>
  <img alt="A screenshot of the MinIO Object Store web console showing the contents of a bucket named &#x22;my-bucket&#x22; with a list of object/folder names (e.g., cowsay-template, daemon-workflow, retry-workflow). The left sidebar shows navigation items like Buckets, Access Keys, and Administrator settings." />
</Frame>

All completed workflow logs are persisted to the MinIO object store by default when Argo is configured to archive logs.

## 5. Inspect the `artifact-repositories` ConfigMap

Argo’s artifact repository configuration (which controls archiving behavior and S3/MinIO connection details) lives in a ConfigMap named `artifact-repositories` in the `argo` namespace. View it with:

```bash theme={null}
kubectl -n argo get cm artifact-repositories -o yaml
```

Example excerpt (showing the relevant `default-v1` entry):

```yaml theme={null}
apiVersion: v1
data:
  default-v1: |
    archiveLogs: true
    s3:
      bucket: my-bucket
      endpoint: minio:9000
      insecure: true
      accessKeySecret:
        name: my-minio-cred
        key: accesskey
      secretKeySecret:
        name: my-minio-cred
        key: secretkey
kind: ConfigMap
metadata:
  name: artifact-repositories
  namespace: argo
```

Key points:

* archiveLogs: true — instructs Argo to persist workflow logs to the artifact store.
* endpoint: minio:9000 — hostname and port of the S3-compatible MinIO service as seen from within the cluster.
* Credentials are referenced via the `my-minio-cred` secret.

<Callout icon="lightbulb">
  The quick-start bundles MinIO for convenience and local testing. For production use, point Argo to a managed S3-compatible provider (e.g., AWS S3, Google Cloud Storage) and manage credentials using a secure secrets workflow.
</Callout>

<Callout icon="warning">
  Do not expose MinIO (or any artifact store) publicly without proper authentication and network restrictions. For ad-hoc demos, prefer `kubectl port-forward` or restrict NodePort access to trusted networks.
</Callout>

## 6. Verify artifact uploads

Because `archiveLogs: true`, completed workflow logs appear in the configured bucket automatically. To test artifact uploads, run a workflow that produces an artifact (or archive logs) and then check the bucket in the MinIO console or via an S3 client:

Example quick verification with `mc` (MinIO client) after port-forward or using NodePort with S3 endpoint:

```bash theme={null}
# Example: using AWS CLI S3-compatible endpoint (set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY)
aws --endpoint-url http://localhost:9000 s3 ls s3://my-bucket
```

Replace endpoint and credentials to match your environment.

## Links and references

* Argo Workflows — [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Kubernetes documentation — [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* MinIO documentation — [https://min.io/docs/](https://min.io/docs/)
* jq JSON processor — [https://stedolan.github.io/jq/](https://stedolan.github.io/jq/)
* AWS S3 — [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* Google Cloud Storage — [https://cloud.google.com/storage](https://cloud.google.com/storage)

This process helps you access, inspect, and verify artifacts and archived logs stored by the Argo Workflows' bundled MinIO server.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/37cae24d-46ec-4607-a662-3b3b990d95d8" />
</CardGroup>


# Demo Artifacts Garbage Collection

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Artifacts-Garbage-Collection/page

Explains Argo Workflows Artifact Garbage Collection, demonstrating workflow-level defaults and per-artifact overrides with examples, behaviors, strategies, and best practices for managing artifact lifecycle.

When workflows generate artifacts and logs over time, stored files consume space in your artifact repository. Artifact Garbage Collection (Artifact GC) in [Argo Workflows](https://argoproj.github.io/argo-workflows/) lets you automatically remove artifacts you no longer need. You can configure deletion either when a workflow completes or when a workflow is deleted. Artifact GC can be set globally at the workflow level (as a default for all artifacts) and selectively overridden per artifact.

<Callout icon="lightbulb">
  Artifact-level settings override the workflow-level default. The available strategies are: OnWorkflowDeletion, OnWorkflowCompletion, and Never.
</Callout>

This document provides two practical examples and explains common behaviors and lifecycle considerations:

* Example 1 — A workflow-level default GC strategy with an artifact-level override.
* Example 2 — A producer-consumer steps workflow that passes an artifact between steps while using a workflow-level GC policy.

Example 1 — Workflow-level Artifact GC with an artifact-level override

* Purpose: Demonstrates setting a default artifact GC strategy at the workflow level and overriding it for a specific artifact.
* Behavior: The workflow default is `OnWorkflowDeletion`. One artifact will follow that policy; another will override it to `OnWorkflowCompletion`.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: artifact-gc-
spec:
  entrypoint: main
  # Default artifact GC strategy applied to all artifacts unless overridden
  artifactGC:
    strategy: OnWorkflowDeletion

  templates:
  - name: main
    container:
      image: argoproj/argosay:v2
      command: ["sh", "-c"]
      args:
      - |
        echo "can throw this away" > /tmp/temporary-artifact.txt
        echo "keep this" > /tmp/keep-this.txt
    outputs:
      artifacts:
      - name: temporary-artifact
        path: /tmp/temporary-artifact.txt
        # Will follow the workflow-level strategy (OnWorkflowDeletion)
      - name: persistent-artifact
        path: /tmp/keep-this.txt
        s3:
          key: keep-this.txt
        artifactGC:
          strategy: OnWorkflowCompletion  # overrides workflow-level strategy
```

Example 2 — Steps-based producer/consumer (passing artifacts between steps)

* Purpose: Shows a multi-step workflow that produces an artifact in one step and consumes it in another.
* Behavior: The workflow-level `artifactGC` is set to `OnWorkflowDeletion` and applies to artifacts unless individually overridden.

<Frame>
  <img alt="A screenshot of the Argo Workflows web UI showing a &#x22;Submit new workflow&#x22; panel with options to select a workflow template or edit using full workflow options. The left sidebar displays workflow summary stats and namespace/filters." />
</Frame>

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: artifact-
  namespace: argo
spec:
  entrypoint: main
  artifactGC:
    strategy: OnWorkflowDeletion  # default for all artifacts in this workflow

  templates:
  - name: main
    steps:
    # Step 1: generate the artifact
    - - name: generate
        template: generate-file
    # Step 2: consume the artifact produced by 'generate'
    - - name: consume
        template: consume-file
        arguments:
          artifacts:
            - name: message-from-producer
              from: "{{steps.generate.outputs.artifacts.my-generated-artifact}}"

  - name: generate-file
    script:
      image: busybox
      command: [sh, -c]
      source: |
        echo "Hello from an artifact!" > /tmp/hello.txt
    outputs:
      artifacts:
      - name: my-generated-artifact
        path: /tmp/hello.txt

  - name: consume-file
    container:
      image: busybox
      command: [sh, -c]
      args: ["cat /tmp/message.txt || true"]
    inputs:
      artifacts:
      - name: message-from-producer
        path: /tmp/message.txt
```

How Artifact GC behaves in practice

* workflow-level default: With `artifactGC.strategy: OnWorkflowDeletion` at the workflow level, artifacts produced by that workflow are removed when the workflow is deleted.
* artifact-level overrides: To change behavior for specific artifacts, set `artifactGC.strategy` on the artifact:
  * `Never` — retain the artifact regardless of workflow deletion.
  * `OnWorkflowCompletion` — delete the artifact when the workflow completes (not waiting for deletion).
  * `OnWorkflowDeletion` — delete the artifact only when the workflow is deleted (this is the default in our examples).
* precedence: Artifact-level settings always override the workflow-level default.

Artifact GC strategies at a glance

| Strategy             | When the artifact is deleted         | Use case                                                     |
| -------------------- | ------------------------------------ | ------------------------------------------------------------ |
| OnWorkflowDeletion   | When the workflow is deleted         | Default for ephemeral artifacts tied to a workflow lifecycle |
| OnWorkflowCompletion | Immediately after workflow completes | Artifacts needed only during runtime or post-processing      |
| Never                | Not deleted by GC                    | Long-term storage or archival artifacts                      |

Example real-world workflow lifecycle

* Submit the workflow (for example via the Argo UI or `kubectl`). The produced artifact is stored in the configured artifact store (e.g., [MinIO](https://min.io/)) under the workflow's folder/bucket.
* Inspect the artifact store to confirm artifact presence while the workflow exists or after completion.
* Delete the workflow:
  * Artifacts with `OnWorkflowDeletion` will be removed by the garbage collector.
  * Artifacts with `Never` or `OnWorkflowCompletion` will follow their explicit artifact-level setting and may remain or be removed based on that configuration.

Best practices

* Use workflow-level defaults to enforce cluster-wide conventions for ephemeral artifacts.
* Override per-artifact when specific artifacts must be retained or cleaned up at a different time.
* Monitor your artifact store capacity and configure lifecycle rules as needed in addition to Argo GC for long-term retention policies.

Links and references

* [Argo Workflows documentation — Artifact Garbage Collection](https://argoproj.github.io/argo-workflows/)
* [MinIO — High performance object storage](https://min.io/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

This concludes the demo article showing how to use Artifact Garbage Collection in Argo Workflows to manage artifact lifecycles and control storage usage.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/c7b5450c-0cbf-4b83-9163-c3c0dc46b4ba" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/84b27352-b3f7-47ba-81bd-ee76ba6c49ef" />
</CardGroup>
