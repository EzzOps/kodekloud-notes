# Argo Workflow Artifacts

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Argo-Workflow-Artifacts/page

Explains how Argo Workflows passes files between steps using artifacts, configuring repositories, wiring outputs to inputs, garbage collection strategies, examples and best practices.

Artifacts are the primary mechanism for passing files between Argo Workflow steps. One step can generate a file and expose it as an output artifact; the Argo Workflows controller uploads that file to your configured artifact repository (for example, [S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3), [Minio](https://min.io), or [Google Cloud Storage (GCS)](https://cloud.google.com/storage)). A later step can declare the corresponding input artifact; the controller downloads that artifact and places it inside the step’s container so the step can read it.

This guide explains:

* How artifact I/O works in Argo Workflows
* How to wire output artifacts to input artifacts across steps
* How to manage artifact lifecycle with garbage collection strategies

## How artifact input/output works

* Producer step: writes a file inside its container (for example, `/tmp/hello.txt`), and declares it as an output artifact in the template.
* Controller action: Argo Workflows uploads that artifact to the configured artifact repository on step completion.
* Consumer step: declares an input artifact. Before the step runs, Argo downloads the artifact and places it inside the container at the path you specify (for example, `/tmp/message.txt`).

To run workflows that use artifacts, you must configure an artifact repository for Argo Workflows. Argo supports S3-compatible repositories (AWS S3, Minio) as well as cloud providers like GCS through repository-specific configuration.

## Example: a simple two-step workflow (generate → consume)

The following example shows a two-step workflow:

* `generate-file` creates `/tmp/hello.txt` and exposes it as an output artifact named `MyGeneratedArtifact`.
* `consume-file` receives that artifact as an input named `MessageFromProducer` and maps it to `/tmp/message.txt`.
* The `main` template wires the producer’s output to the consumer’s input using `arguments.artifacts.from`.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: artifact-passing-example
spec:
  entrypoint: main
  templates:
    - name: main
      steps:
        - - name: generate-file
            template: generate-file
        - - name: consume-file
            template: consume-file
            arguments:
              artifacts:
                - name: MessageFromProducer
                  from: "{{steps.generate-file.outputs.artifacts.MyGeneratedArtifact}}"

    - name: generate-file
      script:
        image: busybox
        command: [sh, -c]
        source: |
          echo "Hello from the producer!" > /tmp/hello.txt
      outputs:
        artifacts:
          - name: MyGeneratedArtifact
            path: /tmp/hello.txt

    - name: consume-file
      inputs:
        artifacts:
          - name: MessageFromProducer
            path: /tmp/message.txt
      container:
        image: busybox
        command: [sh, -c]
        args: ["cat /tmp/message.txt"]
```

Flow summary:

* `generate-file` writes `/tmp/hello.txt` and declares it as an output artifact named `MyGeneratedArtifact`.
* `consume-file` declares an input artifact `MessageFromProducer` mounted at `/tmp/message.txt`.
* The `arguments.artifacts.from` expression in `main` maps `MyGeneratedArtifact` from `generate-file` into `MessageFromProducer` for `consume-file`.
* Before `consume-file` starts, Argo downloads the artifact and places it at `/tmp/message.txt`, allowing the container to run `cat /tmp/message.txt` to print the file contents.

> **lightbulb** Argo Workflows (controller) handles artifact upload/download. Don’t confuse this with [Argo CD](https://learn.kodekloud.com/user/courses/gitops-with-argocd), which is a separate tool for GitOps and application delivery.

## Artifact garbage collection (GC) — manage storage and retention

Stored artifacts consume space in the artifact repository. Argo provides artifact garbage collection (GC) strategies so you can automatically delete artifacts according to a policy. You can define a workflow-level default GC policy and override it for individual artifacts when you need finer control.

Common strategies, use cases, and examples:

| Strategy             | Use case                                                 | Recommended for                                  |
| -------------------- | -------------------------------------------------------- | ------------------------------------------------ |
| OnWorkflowCompletion | Delete artifacts when the workflow finishes successfully | Temporary or intermediate artifacts              |
| OnWorkflowDeletion   | Keep artifacts until the Workflow resource is deleted    | When you want to inspect artifacts after success |
| Never                | Retain artifacts permanently                             | Critical outputs that must be preserved          |

Example: set an artifact-level GC strategy for a temporary artifact (YAML snippet):

```yaml theme={null}
spec:
  entrypoint: main
  templates:
    - name: main
      script:
        image: busybox
        command: [sh, -c]
        source: "echo 'This file is temporary.' > /tmp/temporary-data.log"
      outputs:
        artifacts:
          - name: temp-log
            path: /tmp/temporary-data.log
            artifactGC:
              strategy: OnWorkflowCompletion
```

Notes on policy layering:

* Use a conservative workflow-level default (for example, `OnWorkflowDeletion`) to preserve artifacts unless explicitly discarded.
* Override individual artifact GC to `OnWorkflowCompletion` for ephemeral outputs that can be deleted when the workflow completes.
* Mark critical artifacts with `Never` to ensure long-term retention.

This two-tiered approach (workflow-level default + per-artifact overrides) provides safe default storage management while allowing fine-grained control for important outputs.

## Best practices and tips

* Always configure an artifact repository before using artifact I/O. For S3-compatible storage, ensure credentials and endpoint configuration are set in the Argo artifact repository config.
* Use descriptive artifact names (for example, `build-log`, `model-checkpoint`) to make tracing outputs easier.
* Combine artifact GC policies with a retention and backup plan for production workflows that produce important outputs.
* For large files or many artifacts, consider storage costs and lifecycle rules on the remote repository (e.g., S3 lifecycle policies).

## Links and references

* [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
* [Kubernetes Documentation: Volumes and Storage](https://kubernetes.io/docs/concepts/storage/)
* [S3 (Amazon Simple Storage Service)](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [Minio](https://min.io)
* [Google Cloud Storage (GCS)](https://cloud.google.com/storage)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/615aaf0f-c29e-4f9d-9169-7b514d3cec8f)
