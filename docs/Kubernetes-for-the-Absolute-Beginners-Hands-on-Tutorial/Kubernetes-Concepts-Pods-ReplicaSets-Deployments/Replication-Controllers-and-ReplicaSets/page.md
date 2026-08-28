# Replication Controllers and ReplicaSets

Source: https://notes.kodekloud.com/docs/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial/Kubernetes-Concepts-Pods-ReplicaSets-Deployments/Replication-Controllers-and-ReplicaSets/page

This article explores Replication Controllers and ReplicaSets in

Kubernetes controllers are the brains behind orchestrating your application's containers. In this article, we dive into two important controllers: the classic Replication Controller and its modern successor, the ReplicaSet. Both ensure high availability and load balancing, but they differ in their API versions and configuration nuances.

<Frame>
  ![The image features three open box icons and the text "Replication Controller" on a blue background.](https://kodekloud.com/kk-media/image/upload/v1752884863/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Replication-Controllers-and-ReplicaSets/frame_20.jpg)
</Frame>

Imagine an application running on a single pod. If that pod fails, your application becomes unavailable. The Replication Controller prevents this by maintaining multiple instances of a pod. It automatically replaces any pod that fails, ensuring continuous availability whether you need one or one hundred pods.

<Frame>
  ![The image illustrates a high availability setup using Kubernetes, featuring a user, replication controller, and two pods within a node.](https://kodekloud.com/kk-media/image/upload/v1752884864/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Replication-Controllers-and-ReplicaSets/frame_70.jpg)
</Frame>

Even if you choose to run only one pod, the Replication Controller immediately replaces a failed pod, guaranteeing that the desired number of pods remains active.

<Frame>
  ![The image illustrates high availability using Kubernetes, showing nodes with replication controllers managing pods for redundancy and load balancing.](https://kodekloud.com/kk-media/image/upload/v1752884865/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Replication-Controllers-and-ReplicaSets/frame_90.jpg)
</Frame>

In addition to providing high availability, the Replication Controller helps distribute the load. When user demand increases, additional pods can be deployed, balancing the load across nodes and enhancing performance.

<Frame>
  ![The image illustrates load balancing and scaling with a replication controller managing two pods within a Kubernetes node.](https://kodekloud.com/kk-media/image/upload/v1752884867/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Replication-Controllers-and-ReplicaSets/frame_120.jpg)
</Frame>

The controller can even span multiple nodes, ensuring that pods are distributed to maintain optimal performance and scalability.

<Frame>
  ![The image illustrates load balancing and scaling using Kubernetes, showing users accessing multiple pods managed by a replication controller across two nodes.](https://kodekloud.com/kk-media/image/upload/v1752884868/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Replication-Controllers-and-ReplicaSets/frame_130.jpg)
</Frame>

<Callout icon="lightbulb">
  Both Replication Controllers and ReplicaSets serve the same fundamental purpose: they ensure that your desired number of pod replicas are running. However, the ReplicaSet, which is part of the `apps/v1` API, introduces improvements such as the mandatory selector field.
</Callout>

The ReplicaSet replaces the older Replication Controller. Although they share core functionality, ReplicaSets offer a more explicit configuration, particularly with required label selectors. In our examples below, we will illustrate both methods, though future implementations will favor ReplicaSets.

<Frame>
  ![The image shows a comparison between "Replication Controller" and "Replica Set," separated by a vertical line, on a white background with a blue border.](https://kodekloud.com/kk-media/image/upload/v1752884869/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Replication-Controllers-and-ReplicaSets/frame_160.jpg)
</Frame>

***

## Creating a Replication Controller

Begin by creating a Replication Controller definition file named `rc-definition.yml`. This file is structured in four sections: API version, kind, metadata, and spec. The API version for a Replication Controller is `v1`, and the kind must be set as `ReplicationController`. Under metadata, assign a name (for instance, `myapp-rc`) and labels such as `app` and `type`. In the spec section, detail the pod template and specify the number of desired replicas.

Below is an example of a Replication Controller definition:

```yaml theme={null}
