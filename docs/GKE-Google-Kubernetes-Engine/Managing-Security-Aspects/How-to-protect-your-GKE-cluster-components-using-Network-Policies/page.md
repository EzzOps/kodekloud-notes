# How to protect your GKE cluster components using Network Policies

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/Managing-Security-Aspects/How-to-protect-your-GKE-cluster-components-using-Network-Policies/page

This guide explains how to secure GKE cluster components using network policies and various security measures.

Google Kubernetes Engine (GKE) provides built-in security features and supports Kubernetes Network Policies to safeguard your cluster. In this guide, you'll learn how to secure the control plane, worker nodes, instance metadata, pod access, and network traffic to maintain a robust security posture.

## Securing the Control Plane

The control plane orchestrates your cluster, managing nodes, pods, and services. GKE secures it by running on a hardened Container-Optimized OS with SELinux, AppArmor, and kernel hardening. All communication with the API server is encrypted using TLS, and certificates are rotated automatically. Access is audited for traceability.

<Frame>
  ![The image illustrates the concept of securing a control plane with elements like hardened OS, encryption, certificate rotation, and auditing access. It includes icons representing each security measure.](https://kodekloud.com/kk-media/image/upload/v1752875658/notes-assets/images/GKE-Google-Kubernetes-Engine-How-to-protect-your-GKE-cluster-components-using-Network-Policies/securing-control-plane-security-measures.jpg)
</Frame>

You can tighten control plane access even further:

* **Authorized Networks**: Restrict API endpoint access to whitelisted IP ranges.
* **Private Clusters**: Use private IPs for nodes and the API server, isolating them from the public internet.
* **Identity and Access Management (IAM)**: Assign fine-grained roles and permissions to limit who can perform actions on the control plane.

<Frame>
  ![The image illustrates the concept of securing a control plane, highlighting elements like authorized networks, private clusters, and IAM (Identity and Access Management).](https://kodekloud.com/kk-media/image/upload/v1752875659/notes-assets/images/GKE-Google-Kubernetes-Engine-How-to-protect-your-GKE-cluster-components-using-Network-Policies/securing-control-plane-iam-diagram.jpg)
</Frame>

## Securing Worker Nodes

Worker nodes run your containerized workloads and must be locked down:

* **Container-Optimized OS**: Google-maintained, read-only root filesystem with a built-in firewall and no root SSH access.
* **Autopilot Enforcement**: Autopilot clusters apply these OS controls by default.
* **Limited Accounts**: Only essential user accounts exist with privileges scoped to required operations.

<Frame>
  ![The image illustrates a container-optimized operating system with features like a locked-down firewall, a read-only filesystem, limited user accounts, and disabled root login. It includes icons representing security measures.](https://kodekloud.com/kk-media/image/upload/v1752875660/notes-assets/images/GKE-Google-Kubernetes-Engine-How-to-protect-your-GKE-cluster-components-using-Network-Policies/container-optimized-os-security-features.jpg)
</Frame>

### Node Upgrades

Regular updates close security gaps and ensure compatibility:

* **Autopilot Clusters**: Automatic node upgrades are enabled by default.
* **Standard Clusters**: Choose between automatic or manual upgrades with customizable windows.

```bash theme={null}
