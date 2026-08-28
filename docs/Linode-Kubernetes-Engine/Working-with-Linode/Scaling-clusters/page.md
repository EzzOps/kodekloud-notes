# Scaling clusters

Source: https://notes.kodekloud.com/docs/Linode-Kubernetes-Engine/Working-with-Linode/Scaling-clusters/page

This article explains how to manually scale a Kubernetes cluster on Linode Kubernetes Engine, covering autoscaling, resizing, and adding node pools.

In this lesson, we’ll cover how to manually scale your Kubernetes cluster on Linode Kubernetes Engine (LKE) before automating with tools like Terraform. Understanding these steps is essential for one-off adjustments, troubleshooting, and verifying your infrastructure changes.

<Frame>
  ![The image shows a Kubernetes cluster management interface with details about the cluster's configuration, including CPU, RAM, and storage, as well as the status and IP addresses of node pools.](https://kodekloud.com/kk-media/image/upload/v1752881215/notes-assets/images/Linode-Kubernetes-Engine-Scaling-clusters/kubernetes-cluster-management-interface.jpg)
</Frame>

Under the **Node Pools** section, you have three main actions:

* Enable autoscaling for a pool
* Resize an existing pool
* Add a new node pool

## 1. Autoscaling a Node Pool

To configure horizontal autoscaling:

1. Click **Autoscale Pool**.
2. In the **Autoscale Pool** dialog, check **Autoscaler**.
3. Set the **Min** and **Max** worker node counts (for example, Min = 3, Max = 6).
4. Click **Save**.

<Frame>
  ![The image shows a dialog box titled "Autoscale Pool" with options to set minimum and maximum node pool constraints for LKE, including a checkbox for "Autoscaler" and fields for "Min" and "Max" values.](https://kodekloud.com/kk-media/image/upload/v1752881216/notes-assets/images/Linode-Kubernetes-Engine-Scaling-clusters/autoscale-pool-dialog-box-options.jpg)
</Frame>

<Callout icon="lightbulb">
  You can automate this step with Terraform using the `linode_lke_node_pool` resource. See [Terraform LKE Provider](https://registry.terraform.[SECRET_REDACTED]lke_node_pool) for details.
</Callout>

With autoscaling enabled, LKE will automatically adjust the number of nodes based on your cluster’s scheduling demands.

## 2. Resizing a Node Pool

To manually change the node count:

1. Click **Resize Pool** for your target pool.
2. Enter the desired number of nodes (e.g., increase from 3 to 4).
3. Optionally, select **Recycle Pool** to replace all nodes.

<Frame>
  ![The image shows a confirmation dialog box asking if the user wants to recycle a node pool, with options to cancel or proceed with recycling the pool nodes.](https://kodekloud.com/kk-media/image/upload/v1752881217/notes-assets/images/Linode-Kubernetes-Engine-Scaling-clusters/recycle-node-pool-confirmation-dialog.jpg)
</Frame>

<Callout icon="triangle-alert">
  Recycling a pool deletes and re-provisions all nodes, which can cause downtime for pods running on those nodes. Schedule this during maintenance windows.
</Callout>

## 3. Adding a New Node Pool

For specialized workloads—such as high-memory or GPU-intensive applications—you can add a separate node pool:

1. Click **Add Pool**.
2. Choose the plan that fits your requirements.
3. Click **Add Pool** to provision the nodes.

<Frame>
  ![The image shows a pricing table for adding a node pool to a Kubernetes cluster, listing options for dedicated CPU plans with varying RAM, CPU, and storage specifications, along with their monthly and hourly costs.](https://kodekloud.com/kk-media/image/upload/v1752881218/notes-assets/images/Linode-Kubernetes-Engine-Scaling-clusters/kubernetes-node-pool-pricing-table.jpg)
</Frame>

Once provisioned, both pools appear in your dashboard, showing status and IP addresses.

<Frame>
  ![The image shows a dashboard for managing node pools, displaying the status and IP addresses of nodes in "Linode 4 GB" and "Linode 24 GB" pools. The "Linode 4 GB" nodes are running, while the "Linode 24 GB" node is provisioning.](https://kodekloud.com/kk-media/image/upload/v1752881220/notes-assets/images/Linode-Kubernetes-Engine-Scaling-clusters/node-pool-dashboard-linode-status.jpg)
</Frame>

## Scaling Options Overview

| Action         | Use Case                 | Description                                 |
| -------------- | ------------------------ | ------------------------------------------- |
| Autoscale Pool | Dynamic workloads        | Automatically adjusts node count (Min/Max). |
| Resize Pool    | Predictable scaling      | Manually set the node count.                |
| Recycle Pool   | Updates or recovery      | Deletes and re-provisions all nodes.        |
| Add Pool       | Mixed-instance workloads | Create additional pools with new specs.     |

## Links and References

* [Linode Kubernetes Engine (LKE)](https://www.linode.com/kubernetes/)
* [Terraform | Infrastructure as Code](https://www.terraform.io/)
* [Kubernetes Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
* [Terraform LKE Node Pool Resource](https://registry.terraform.[SECRET_REDACTED]lke_node_pool)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linode-kubernetes-engine/module/9702fbe2-4321-41c5-87e8-8ea364da097d/lesson/443dd592-98ba-4338-9341-57ee5858620d" />
</CardGroup>
