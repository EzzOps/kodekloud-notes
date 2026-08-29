# my-scheduler-2-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: my-scheduler-2
```

```yaml theme={null}
# my-scheduler-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: my-scheduler
```

```yaml theme={null}
# scheduler-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: default-scheduler
```

Each scheduler profile functions as an independent scheduler within the same binary. To further customize these profiles, you can manipulate the plugin settings by disabling default plugins or enabling custom ones. Below is a sample configuration showcasing these customizations:

```yaml theme={null}
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: my-scheduler-2
  plugins:
    score:
      disabled:
      - name: TaintToleration
      enabled:
      - name: MyCustomPluginA
      - name: MyCustomPluginB

- schedulerName: my-scheduler-3
  plugins:
    preScore:
      disabled:
      - name: "*"
    score:
      disabled:
      - name: "*"

- schedulerName: my-scheduler-4
```

Under the plugins section for each profile, you can specify which extension points to modify and choose to selectively enable or disable plugins by name or using a pattern.

<Callout icon="lightbulb">
  For more information on multi-scheduling profiles, refer to the [Kubernetes enhancement proposal CAP-1451](https://github.com/kubernetes/enhancements/tree/master/keps/sig-scheduling/1451-kube-scheduler-multiple-profiles) and other related scheduling framework articles.
</Callout>

<Frame>
  ![The image shows a slide titled "References" with two URLs related to Kubernetes scheduling concepts.](../../../../images/kodekloud.com/kk-media/image/upload/v1752880686/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Configuring-Kubernetes-Scheduler-Profiles/frame_590.jpg)
</Frame>

That concludes our overview of configuring Kubernetes scheduler profiles. Happy scheduling!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/4fab542c-3091-4f8e-ad7c-91d96d54b049/lesson/e0e31e44-c495-45e4-8244-3b602733e2a1" />
</CardGroup>


# DaemonSets

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Scheduling/DaemonSets/page

This guide explains DaemonSets in Kubernetes, their use cases, and how to create one for managing Pods on every node.

Welcome to this guide on DaemonSets in Kubernetes. In this tutorial, you'll learn how DaemonSets work, their common use cases, and how to create one.

DaemonSets enable you to run exactly one instance of a Pod on every node within your cluster. As your cluster scales—by adding or removing nodes—the DaemonSet automatically ensures that each node has the designated Pod running. This approach is particularly useful for deploying essential services like monitoring agents, log collectors, and networking components (for example, kube-proxy) consistently across all nodes.

<Callout icon="lightbulb">
  While ReplicaSets ensure that a set number of Pod replicas are running across the cluster, DaemonSets guarantee that one copy of the Pod is present on every node.
</Callout>

## Use Cases for DaemonSets

DaemonSets are primarily used in the following scenarios:

* **Monitoring and Logging:** Deploy agents responsible for system monitoring and log collection across all nodes.
* **Networking:** Ensure a networking solution agent (e.g., VNet components or weave-net) is deployed on every node.
* **Critical Infrastructure Components:** Deploy essential components like kube-proxy that need to reside on every node.

Below is an image that illustrates the use case for DaemonSets, highlighting the connection between a monitoring solution, a logs viewer, and multiple nodes:

<Frame>
  ![The image illustrates a use case for Daemon Sets, showing a connection between a monitoring solution, logs viewer, and multiple nodes with colored indicators.](../../../../images/kodekloud.com/kk-media/image/upload/v1752880688/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-DaemonSets/frame_80.jpg)
</Frame>

Another common scenario involves networking. As mentioned, some networking solutions require an agent on every node. Understanding this use case is vital before diving deeper into networking concepts later in the course:

<Frame>
  ![The image illustrates the use case of Daemon Sets in Kubernetes, specifically for deploying kube-proxy across multiple nodes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752880689/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-DaemonSets/frame_100.jpg)
</Frame>

<Frame>
  ![The image illustrates a networking use case for Daemon Sets, showing multiple nodes with "weave-net" components distributed across them.](../../../../images/kodekloud.com/kk-media/image/upload/v1752880692/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-DaemonSets/frame_120.jpg)
</Frame>

## Creating a DaemonSet

Creating a DaemonSet is quite similar to creating a ReplicaSet. The YAML definition file begins with `apiVersion`, `kind`, `metadata`, and `spec` sections. The primary difference is that the `kind` is set to DaemonSet, and it manages a Pod on every node rather than a specified number of replicas.

Below is an example DaemonSet definition file:

```yaml theme={null}
