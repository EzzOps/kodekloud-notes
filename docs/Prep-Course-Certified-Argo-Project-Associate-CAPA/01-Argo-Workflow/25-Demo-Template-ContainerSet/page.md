# Demo Template ContainerSet

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Template-ContainerSet/page

Explains Argo Workflows containerSet templates that run multiple containers in one pod for shared networking, storage and lifecycle, and how to inspect their logs in the UI.

In this lesson we examine a containerSet template example in Argo Workflows. A `containerSet` template runs multiple containers inside a single Kubernetes Pod (similar to sidecars), allowing the containers to share the same network namespace, volumes, and lifecycle. This pattern is useful when containers must communicate over localhost, share mounted storage, or depend on the same init/wait logic.

Below is a minimal workflow that defines a single template named `main`. The template type is `containerSet` and declares two containers (`a` and `b`) that run together in the same pod:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: container-set-template-
spec:
  entrypoint: main
  templates:
  - name: main
    containerSet:
      containers:
      - name: a
        image: rancher/cowsay
        command: [cowsay]
        args: ["Container A!!!!"]
      - name: b
        image: rancher/cowsay
        command: [cowsay]
        args: ["Container B!!!!"]
```

Key points about this example:

* Both containers (`a` and `b`) are created in a single pod and run concurrently.
* Containers can use different images and commands.
* Pods created by `containerSet` will also show the template name (here `main`) and any init containers in the UI and Kubernetes API.

<Frame>
  <img alt="Screenshot of the Argo Workflows web UI displaying a workflow graph with a completed &#x22;container-set-template-9bd5v&#x22; node and two child nodes labeled &#x22;a&#x22; and &#x22;b&#x22; (green checkmarks). The right pane shows container details (NAME: main, IMAGE, COMMAND, ARGS, ENV) and the top toolbar has buttons like RESUBMIT, DELETE, LOGS, SHARE, and WORKFLOW LINK." />
</Frame>

When you open this workflow in the Argo UI, the graph shows the `container-set-template-...` node and its child containers (`a`, `b`) because both ran inside the same pod. The right-hand pane lists template metadata such as `NAME`, `IMAGE`, `COMMAND`, `ARGS`, and environment variables.

Inspecting logs and individual container output

* The Argo UI exposes logs for each container in the pod through the Logs modal.
* Use the container dropdown to switch between logs for `init`, `wait` (if present), and each container from the `containerSet` (e.g., `a`, `b`).

<Frame>
  <img alt="A screenshot of an Argo Workflows web UI showing a &#x22;Logs&#x22; modal with a container dropdown (showing options like main, init, wait, a, b), an empty log area, and filter/UTC fields. A dark left sidebar with app icons and a top bar with workflow controls (RESUBMIT, DELETE) is visible behind it." />
</Frame>

<Callout icon="lightbulb">
  Container set templates run multiple containers in the same pod (sidecars). Use the Logs dropdown in the Argo UI to select logs for each container (init, wait, a, b, etc.). Choose `containerSet` when containers must share networking, storage, or lifecycle; choose separate templates when you need separate pods or separate scheduling/scaling behavior.
</Callout>

When to use containerSet vs separate templates

| Resource Pattern           | Use Case                                                                                                      | Behavior                                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| containerSet               | Multiple cooperating containers that must share the same pod resources (localhost networking, shared volumes) | All containers run in one pod, start concurrently (plus init containers), share network and storage |
| Separate templates / steps | Sequential tasks, parallel tasks in separate pods, or workloads requiring independent scaling                 | Each template runs in its own pod; containers do not share pod-level resources                      |

Best practices and considerations

* Use `containerSet` when containers need low-latency local communication or shared volume access.
* Avoid `containerSet` if you require independent lifecycle, autoscaling, or separate scheduling for containers.
* Remember to include any required init containers (for setup) or a `wait` sidecar if you need coordination before/after the main containers run.

References and further reading

* Argo Workflows Templates: containerSet (see official docs) — [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/) (search for "containerSet")
* Kubernetes Pods and Containers — [https://kubernetes.io/docs/concepts/workloads/pods/](https://kubernetes.io/docs/concepts/workloads/pods/) (background on shared namespaces and volumes)

This example demonstrates how `containerSet` enables sidecar-like behavior inside Argo Workflows and how to inspect and debug those containers via the Argo UI.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/3dafa9f3-9427-4f69-8d97-4f9ba1fd7523" />
</CardGroup>
