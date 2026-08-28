# Recap ReplicaSets

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Core-Concepts/Recap-ReplicaSets/page

This article explores Kubernetes controllers, focusing on replication controllers and ReplicaSets for managing application availability and scalability.

Hello and welcome to this Kubernetes controllers lesson. I’m Mumshad Mannambeth, and today we will explore how controllers manage your applications’ availability and scalability. Controllers are the brains behind Kubernetes—they monitor objects and respond to any change in the cluster. In this lesson, we will focus on the replication controller and its more advanced successor, the ReplicaSet.

Imagine you have a single Pod running your application. If that Pod crashes, your users immediately lose access. To overcome this, you can run multiple instances (Pods) of the application. The replication controller ensures that a specified number of Pods are running at all times, providing high availability even during failures.

Even when running a single Pod, a replication controller is beneficial because it automatically replaces a failed Pod, ensuring continuous availability. For instance, if one instance fails, another is promptly created to maintain the required Pod count.

<Frame>
  ![The image illustrates a high availability setup with Kubernetes, showing a replication controller managing multiple pods across nodes.](https://kodekloud.com/kk-media/image/upload/v1752871197/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Recap-ReplicaSets/frame_80.jpg)
</Frame>

Another important use of the replication controller is load distribution. As user demand grows, additional Pods can be deployed under the controller’s management. If one node runs out of resources, Kubernetes schedules new Pods across other nodes. This efficiently balances the load and scales the application dynamically.

<Frame>
  ![The image illustrates load balancing and scaling using Kubernetes, showing users accessing multiple pods managed by a replication controller across two nodes.](https://kodekloud.com/kk-media/image/upload/v1752871199/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Recap-ReplicaSets/frame_150.jpg)
</Frame>

It’s important to understand the difference between a replication controller and a ReplicaSet. While both ensure the desired number of Pods are running, the replication controller is an older technology that is gradually being replaced by the more advanced ReplicaSet. In our examples and demos going forward, we will focus on ReplicaSets, though the core concepts apply to both.

## Creating a Replication Controller

Let’s start by creating a replication controller definition file named `rc-definition.yaml`. Every Kubernetes definition file comprises four main sections: API version, kind, metadata, and spec. For our replication controller:

* **apiVersion:** Set to `v1` because the Replication Controller is supported under this version.
* **kind:** Set to `ReplicationController`.
* **metadata:** Contains the name (`myapp-rc`) and labels (`app` and `type`) for identification.
* **spec:** Defines the desired state, including the number of replicas and a Pod template.

Move the Pod definition (excluding the API version and kind) into the `template` section. Ensure the Pod details are indented correctly under `template` to nest them properly as the replication controller's child.

Below is the combined definition:

```yaml theme={null}
