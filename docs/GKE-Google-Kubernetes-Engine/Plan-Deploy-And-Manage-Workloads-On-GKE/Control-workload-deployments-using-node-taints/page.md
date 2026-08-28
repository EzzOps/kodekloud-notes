# Control workload deployments using node taints

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/Plan-Deploy-And-Manage-Workloads-On-GKE/Control-workload-deployments-using-node-taints/page

This article explains how to control workload deployments in GKE using node taints and pod tolerations for better resource management.

Node taints and pod tolerations in Google Kubernetes Engine (GKE) give you fine-grained control over where your workloads run. By marking nodes with taints and adding matching tolerations to pods, you ensure that only eligible pods land on specific nodes.

## Taints and Tolerations Analogy

Imagine a birthday party with two zones: a colorful play area for kids and a quiet lounge for adults. You hand out blue bracelets to kids and green bracelets to adults so everyone stays in the right spot. In GKE:

* Nodes are the party zones.
* A taint on a node labels its “zone” (e.g., Music Area, Reading Area).
* A pod’s toleration is its bracelet—pods with a matching toleration can be scheduled on that node.

<Frame>
  ![The image is an overview diagram of node taints and tolerations in Google Kubernetes Engine (GKE), showing two nodes with specific taints and corresponding tolerations for "Music Area" and "Reading Area."](https://kodekloud.com/kk-media/image/upload/v1752875714/notes-assets/images/GKE-Google-Kubernetes-Engine-Control-workload-deployments-using-node-taints/node-taints-tolerations-gke-diagram.jpg)
</Frame>

Pods with a `music-area` toleration will only run on nodes tainted for music, just like kids gathering in their play zone. Pods tolerating `reading-area` run on the quiet nodes.

## Autopilot vs. Standard Clusters

Depending on your cluster mode, taint configuration changes:

| Cluster Mode | Node Management         | Taint Setup                        | Automation                      |
| ------------ | ----------------------- | ---------------------------------- | ------------------------------- |
| Autopilot    | Fully managed by GKE    | Taints applied automatically       | GKE assigns taints at scale     |
| Standard     | User-defined node pools | You add taints when creating pools | You must update taints manually |

<Frame>
  ![The image is an overview of node taints in Google Kubernetes Engine (GKE), comparing Autopilot and Standard modes, highlighting tasks like node provisioning, scheduling, taint, and toleration.](https://kodekloud.com/kk-media/image/upload/v1752875715/notes-assets/images/GKE-Google-Kubernetes-Engine-Control-workload-deployments-using-node-taints/node-taints-gke-autopilot-standard-overview.jpg)
</Frame>

* In **Autopilot**, GKE handles node lifecycles and taints based on pod requirements.
* In **Standard** mode, you configure node pools, labels, and taints yourself.

## Why Use Node Taints?

Taints help isolate workloads with specific needs—whether resources, hardware, or compliance:

<Frame>
  ![The image is a diagram explaining the need for node taint in GKE, highlighting workloads like batch coordination, game server matchmaking, server/database separation, and compliance reasons.](https://kodekloud.com/kk-media/image/upload/v1752875716/notes-assets/images/GKE-Google-Kubernetes-Engine-Control-workload-deployments-using-node-taints/gke-node-taint-workload-diagram.jpg)
</Frame>

### Batch Coordinator Workloads

Time-sensitive, resource-intensive jobs should run on dedicated nodes to avoid interference.

<Frame>
  ![The image is a diagram illustrating "Node Taint" with a focus on "Batch Coordinator Workload," highlighting aspects like being time-intensive, requiring significant resources, and ensuring no interference.](https://kodekloud.com/kk-media/image/upload/v1752875718/notes-assets/images/GKE-Google-Kubernetes-Engine-Control-workload-deployments-using-node-taints/node-taint-batch-coordinator-diagram.jpg)
</Frame>

### Game Server Matchmaking

Low-latency and specialized hardware are critical for matchmaking. A unique taint guarantees these pods land on the right machines.

<Frame>
  ![The image is a diagram illustrating a "Node Taint" concept, showing a game server with matchmaking workload, labeled with "Unique Taint," and highlighting features like low latency and specialized hardware.](https://kodekloud.com/kk-media/image/upload/v1752875719/notes-assets/images/GKE-Google-Kubernetes-Engine-Control-workload-deployments-using-node-taints/node-taint-game-server-diagram.jpg)
</Frame>

### Server–Database Separation

By tainting web servers and database nodes differently, you prevent resource contention and improve performance.

* Web server nodes: `server-role=web:NoSchedule`
* Database nodes: `server-role=db:NoSchedule`

### Compliance and Policy Requirements

Some workloads must adhere to privacy regulations or internal policies. Assign compliance-specific taints to enforce workload isolation.

<Frame>
  ![The image is a diagram titled "Node Taint," illustrating the concept of compliance and policy reasons, with two subcategories: privacy requirements and regulatory constraints.](https://kodekloud.com/kk-media/image/upload/v1752875720/notes-assets/images/GKE-Google-Kubernetes-Engine-Control-workload-deployments-using-node-taints/node-taint-compliance-policy-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  Node taints are not a security boundary. For untrusted workloads or strict isolation, use network policies, dedicated clusters, or virtualization.
</Callout>

## Applying Node Taints in GKE

You can apply taints directly with `kubectl` or configure them in GKE for greater reliability:

* **GKE Console / gcloud**
* **`kubectl taint`**
* **Terraform** or other IaC tools

<Frame>
  ![The image illustrates ways of applying node taints in Kubernetes, highlighting "kubectl taint" and features like taint persistence, automatic taint creation, and seamless cluster autoscaling.](https://kodekloud.com/kk-media/image/upload/v1752875721/notes-assets/images/GKE-Google-Kubernetes-Engine-Control-workload-deployments-using-node-taints/kubernetes-node-taints-kubectl-diagram.jpg)
</Frame>

### Example: Tainting with kubectl

```bash theme={null}
