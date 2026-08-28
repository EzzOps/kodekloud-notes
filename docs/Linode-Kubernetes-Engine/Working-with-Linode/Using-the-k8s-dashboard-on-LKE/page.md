# Using the k8s dashboard on LKE

Source: https://notes.kodekloud.com/docs/Linode-Kubernetes-Engine/Working-with-Linode/Using-the-k8s-dashboard-on-LKE/page

This article explains how to use the Kubernetes Dashboard for managing and troubleshooting workloads on Linode Kubernetes Engine.

There will come a time when you need a live visualization of your Kubernetes clusters—seeing deployments, pods, secrets, monitoring metrics, and more. The **Kubernetes Dashboard** offers an intuitive web UI to manage and troubleshoot your workloads on Linode Kubernetes Engine (LKE).

<Frame>
  ![The image shows a Kubernetes management dashboard displaying details of a cluster named "kodekloudtest9292," including version, resources, and node pool status. It lists nodes with their status as "Running" and associated IP addresses."](https://kodekloud.com/kk-media/image/upload/v1752881224/notes-assets/images/Linode-Kubernetes-Engine-Using-the-k8s-dashboard-on-LKE/kubernetes-dashboard-kodekloudtest9292.jpg)
</Frame>

From this single pane of glass, you can:

* Deploy or edit containerized applications
* Monitor pod and deployment status
* View logs and resource usage
* Troubleshoot issues with real-time metrics

## 1. Accessing the Dashboard

1. Log in to the [Linode Cloud Manager](https://cloud.linode.com/).
2. Navigate to **Kubernetes** and select your cluster.
3. Click **Kubernetes Dashboard**.

You’ll be redirected to the login screen:

<Frame>
  ![The image shows a login screen for the Kubernetes Dashboard, offering options to sign in using a token or kubeconfig file.](https://kodekloud.com/kk-media/image/upload/v1752881225/notes-assets/images/Linode-Kubernetes-Engine-Using-the-k8s-dashboard-on-LKE/kubernetes-dashboard-login-screen.jpg)
</Frame>

### Authentication Methods

| Method     | Steps                                                                                 |
| ---------- | ------------------------------------------------------------------------------------- |
| kubeconfig | Click the ⋮ menu, upload your local `kubeconfig` file, then **Sign In**.              |
| Token      | Copy the bearer token from Cloud Manager and paste it into the **Token** field below. |

```yaml theme={null}
apiVersion: v1
kind: Config
clusters:
- name: lke61875
  cluster:
    server: https://5d8f062c-9683-4326-8882-4cd8c1e02405.cpc-...
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJJVUS...
users:
- name: lke61875-admin
  user:
    token: eyJhbGciOiJSUzI...
contexts:
- name: lke61875-ctx
  context:
    cluster: lke61875
    namespace: default
    user: lke61875-admin
current-context: lke61875-ctx
```

```plaintext theme={null}
/HQTFVZEVRUU8KTUF50QNtDFZbV5YmlWFpYTxdEUVlKS29aWh2Y05BUUVMQ
```

<Callout icon="lightbulb">
  Tokens are scoped by RBAC rules. Ensure your service account has the correct role bindings to view the resources you need.
</Callout>

Click **Sign In** to open the dashboard.

## 2. Dashboard Overview

Upon first login (in the `default` namespace), you may see an empty view:

<Frame>
  ![The image shows a Kubernetes dashboard with a sidebar menu listing various options like Workloads, Services, and Config and Storage. The main area indicates that there is nothing to display.](https://kodekloud.com/kk-media/image/upload/v1752881226/notes-assets/images/Linode-Kubernetes-Engine-Using-the-k8s-dashboard-on-LKE/kubernetes-dashboard-sidebar-menu.jpg)
</Frame>

<Callout icon="triangle-alert">
  If you leave the dashboard exposed without proper authentication, anyone with the URL and token can view or modify your cluster. Always secure access.
</Callout>

### Switching Namespaces

Use the namespace dropdown in the top-right corner to choose **kube-system** and inspect core components:

<Frame>
  ![The image shows a Kubernetes dashboard displaying a list of running pods with details such as names, images, labels, nodes, and statuses.](https://kodekloud.com/kk-media/image/upload/v1752881227/notes-assets/images/Linode-Kubernetes-Engine-Using-the-k8s-dashboard-on-LKE/kubernetes-dashboard-running-pods.jpg)
</Frame>

## 3. Inspecting Deployments

Select **Deployments** under **Workloads** to view system controllers like CoreDNS and Calico:

<Frame>
  ![The image shows a Kubernetes dashboard displaying the "Deployments" section, listing two deployments: "coredns" and "calico-kube-controllers," along with their respective images and labels.](https://kodekloud.com/kk-media/image/upload/v1752881228/notes-assets/images/Linode-Kubernetes-Engine-Using-the-k8s-dashboard-on-LKE/kubernetes-dashboard-deployments-coredns-calico.jpg)
</Frame>

## 4. Workloads Overview

Under **Workloads**, you can monitor all controllers:

| Workload Type | Description                             |
| ------------- | --------------------------------------- |
| Daemon Sets   | Run one pod per node (e.g., kube-proxy) |
| Deployments   | Declarative updates & scaling           |
| Replica Sets  | Maintain a stable set of replicas       |
| Pods          | The smallest deployable unit            |

<Frame>
  ![The image shows a Kubernetes dashboard interface displaying various workloads such as Daemon Sets, Deployments, Pods, and Replica Sets, each with a green circle indicating the number of running instances.](https://kodekloud.com/kk-media/image/upload/v1752881229/notes-assets/images/Linode-Kubernetes-Engine-Using-the-k8s-dashboard-on-LKE/kubernetes-dashboard-workloads-overview.jpg)
</Frame>

Click on any workload—for example, the **kube-proxy** DaemonSet—to inspect pod details:

<Frame>
  ![The image shows a Kubernetes dashboard displaying the status of "kube-proxy" daemon sets, with details about pods, images, labels, nodes, and their running status.](https://kodekloud.com/kk-media/image/upload/v1752881230/notes-assets/images/Linode-Kubernetes-Engine-Using-the-k8s-dashboard-on-LKE/kubernetes-dashboard-kube-proxy-status.jpg)
</Frame>

## 5. Services, Config & Storage

Beyond workloads, the sidebar lets you explore:

* **Services**: ClusterIP, NodePort, LoadBalancer endpoints
* **Config and Storage**: ConfigMaps, Secrets, PersistentVolumes, PVCs
* **Access Control**: Roles, RoleBindings, ServiceAccounts

## 6. Additional Resources

* [Kubernetes Dashboard Official Guide](https://github.com/kubernetes/dashboard)
* [Linode Kubernetes Engine Documentation](https://www.linode.com/docs/products/kubernetes/)
* [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linode-kubernetes-engine/module/9702fbe2-4321-41c5-87e8-8ea364da097d/lesson/28009004-8ff1-4872-9741-822f4cfc3d29" />
</CardGroup>
