# my-scheduler-2-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: my-scheduler-2
  - schedulerName: my-scheduler-3
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

Each profile allows you to customize plugin configurations. For instance, you could disable specific plugins or enable custom ones. Below is an example where the "my-scheduler-2" profile disables the TaintToleration plugin and enables two custom plugins (MyCustomPluginA and MyCustomPluginB). Additionally, the "my-scheduler-3" profile disables all preScore and score plugins:

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
          - name: '*'
      score:
        disabled:
          - name: '*'
  - schedulerName: my-scheduler-4
```

In the plugins section, specify the extension point and then enable or disable plugins by name (or using a wildcard pattern).

<Callout icon="lightbulb">
  This flexible configuration allows you to tailor the scheduling behavior to meet your unique workload requirements by selectively enabling or disabling plugins across different profiles.
</Callout>

## Summary

This lesson provided an overview of Kubernetes scheduling and scheduler profiles. We covered:

* The phases of scheduling: queueing, filtering, scoring, and binding.
* The role of various scheduler plugins and extension points.
* How to configure multiple scheduler profiles within a single scheduler binary to customize scheduling behavior.

For further reading, consider exploring the official documentation on [Kubernetes Scheduling](https://kubernetes.io/docs/concepts/scheduling-eviction/) and multi-scheduler profiles.

That’s all for this lesson. See you in the next one!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/57fc8d59-a0cc-408b-b431-0547f576c6bd" />
</CardGroup>


# DaemonSets

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Scheduling/DaemonSets/page

This comprehensive guide explores DaemonSets in Kubernetes, their use cases, and provides a step-by-step example for deployment in your cluster.

Welcome to this comprehensive guide on DaemonSets in Kubernetes. In this article, we will dive deep into how DaemonSets work, explore their primary use cases, and provide a step-by-step example to help you deploy one in your cluster.

DaemonSets ensure that exactly one copy of a pod runs on every node in your Kubernetes cluster. When you add a new node, the DaemonSet automatically deploys the pod on the new node. Likewise, when a node is removed, the corresponding pod is also removed. This guarantees that a single instance of the pod is consistently available on each node.

<Frame>
  ![The image illustrates Kubernetes concepts: Daemon Sets, ReplicaSets, and Deployments, using colored dots within outlined boxes to represent different components and their distribution.](https://kodekloud.com/kk-media/image/upload/v1752869886/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-DaemonSets/frame_40.jpg)
</Frame>

## Use Cases for DaemonSets

DaemonSets are particularly useful in scenarios where you need to run background services or agents on every node. Some common use cases include:

* **Monitoring agents and log collectors:** Deploy monitoring tools or log collectors across every node to ensure comprehensive cluster-wide visibility without manual intervention.
* **Essential Kubernetes components:** Deploy critical components, such as kube-proxy, which Kubernetes requires on all worker nodes.
* **Networking solutions:** Ensure consistent deployment of networking agents like those used in VNet or weave-net across all nodes.

<Frame>
  ![The image illustrates a use case for Daemon Sets, showing their connection to a Monitoring Solution and Logs Viewer.](https://kodekloud.com/kk-media/image/upload/v1752869888/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-DaemonSets/frame_80.jpg)
</Frame>

<Frame>
  ![The image illustrates a Kubernetes DaemonSet use case for kube-proxy, showing multiple nodes each running a kube-proxy instance.](https://kodekloud.com/kk-media/image/upload/v1752869889/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-DaemonSets/frame_100.jpg)
</Frame>

<Frame>
  ![The image illustrates a networking use case for Daemon Sets, showing multiple nodes labeled "weave-net" with colored circles representing network components.](https://kodekloud.com/kk-media/image/upload/v1752869890/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-DaemonSets/frame_120.jpg)
</Frame>

## Creating a DaemonSet

Creating a DaemonSet is analogous to creating a ReplicaSet. The DaemonSet YAML configuration consists of a pod template under the `template` section and a selector that binds the DaemonSet to its pods. A typical DaemonSet definition includes the API version, kind, metadata, and specifications. Note that the API version is `apps/v1` and the kind is set to `DaemonSet`.

Below is an example DaemonSet definition file that deploys a monitoring agent:

```yaml theme={null}
