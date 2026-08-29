# Upgrade a specific node pool in a cluster
gcloud container clusters upgrade CLUSTER_NAME \
  --region=REGION \
  --node-pool=POOL_NAME
```

![The image is a diagram illustrating node upgrades, highlighting automatic upgrades and regular updates, with sections labeled "Autopilot," "Upgrades," and "Standard."](https://kodekloud.com/kk-media/image/upload/v1752875661/notes-assets/images/GKE-Google-Kubernetes-Engine-How-to-protect-your-GKE-cluster-components-using-Network-Policies/node-upgrades-automatic-regular-diagram.jpg)

## Protecting Instance Metadata

By default, nodes fetch credentials and configuration from the Compute Engine metadata server. Pods shouldn't inherit node service account keys. Enabling **Workload Identity** filters metadata access, exposing only pod-level credentials.

> **lightbulb** Workload Identity replaces node-level metadata access, preventing privilege escalation from pods to node credentials.

![The image is a diagram showing nodes with a focus on securing instance metadata, providing nodes with credentials and configurations.](https://kodekloud.com/kk-media/image/upload/v1752875662/notes-assets/images/GKE-Google-Kubernetes-Engine-How-to-protect-your-GKE-cluster-components-using-Network-Policies/instance-metadata-security-nodes-diagram.jpg)

## Managing Pod Access and Credentials

Apply the principle of least privilege to your workloads:

* **Security Contexts**: Define user IDs, restrict Linux capabilities, and disable privilege escalation.
* **Workload Identity**: Map Kubernetes ServiceAccounts to IAM ServiceAccounts for granular permissions.
* **Binary Authorization**: Enforce image signing and attestation before deployment.

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  containers:
  - name: app
    image: gcr.io/my-project/secure-app:latest
    securityContext:
      runAsUser: 1000
      allowPrivilegeEscalation: false
      capabilities:
        drop:
          - ALL
```

![The image illustrates "Pod Access" with three security measures: limiting pod container process privileges, giving pods access to Google Cloud resources, and using binary authorization, connected to a "Control Plane" section.](https://kodekloud.com/kk-media/image/upload/v1752875664/notes-assets/images/GKE-Google-Kubernetes-Engine-How-to-protect-your-GKE-cluster-components-using-Network-Policies/pod-access-security-measures-control-plane.jpg)

GKE Autopilot enforces these settings automatically. In Standard clusters, include securityContext fields in your Pod specs:

```yaml theme={null}
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

![The image illustrates pod access with a focus on limiting container process privileges, highlighting that autopilot restricts privileges and allows security-related options.](https://kodekloud.com/kk-media/image/upload/v1752875665/notes-assets/images/GKE-Google-Kubernetes-Engine-How-to-protect-your-GKE-cluster-components-using-Network-Policies/pod-access-limiting-container-privileges.jpg)

Binary Authorization integrates with Artifact Registry to allow only trusted, signed images:

![The image illustrates a process for pod access using binary authorization, ensuring only trusted container images are deployed and internal processes are completed for safeguarding software quality and integrity.](https://kodekloud.com/kk-media/image/upload/v1752875666/notes-assets/images/GKE-Google-Kubernetes-Engine-How-to-protect-your-GKE-cluster-components-using-Network-Policies/pod-access-binary-authorization-process.jpg)

## Network Security with Network Policies

Kubernetes Network Policies control traffic based on pod labels, enforcing a zero-trust network. For example, restrict an `app=my-app` pod to only communicate with `db=my-db` pods:

![The image illustrates a network security diagram for a GKE cluster, showing the VPC network with subnets, nodes, and pods, along with network policies for "app:my-app" and "app:my-db."](https://kodekloud.com/kk-media/image/upload/v1752875668/notes-assets/images/GKE-Google-Kubernetes-Engine-How-to-protect-your-GKE-cluster-components-using-Network-Policies/gke-cluster-network-security-diagram.jpg)

First, label your workloads:

```bash theme={null}
kubectl label pods my-app app=my-app
kubectl label pods my-db db=my-db
```

Then, apply this NetworkPolicy:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-app-to-db
spec:
  podSelector:
    matchLabels:
      db: my-db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: my-app
```

> **triangle-alert** Without a default deny policy, unintended traffic might still flow. Always set a global deny-all policy if no rules match.

## Summary

By securing the control plane, hardening nodes, protecting metadata, enforcing least privilege, and applying Network Policies, you fortify your GKE cluster against threats.

## Links and References

* [Google Kubernetes Engine Overview](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview)
* [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Workload Identity Documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)
* [Binary Authorization](https://cloud.google.com/binary-authorization)

- [Watch Video](https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine/module/225743c4-eb6e-4393-a51e-4ed7d41dbe51/lesson/b78dfb07-049f-4756-9448-58f217778698)


# Section Introduction

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/Managing-Security-Aspects/Section-Introduction/page

This article covers key security layers and best practices for securing Google Kubernetes Engine clusters.

> **lightbulb** This module assumes you are already familiar with [Kubernetes basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) and have access to a Google Cloud project with billing enabled.

Google Kubernetes Engine (GKE) is a powerful platform for running containerized workloads at scale. As adoption grows, it’s critical to build a robust security posture around your clusters. In this lesson, we’ll cover the key security layers in GKE and best practices for each.

## What You’ll Learn

| Security Domain                | Key Concepts                                                                      |
| ------------------------------ | --------------------------------------------------------------------------------- |
| Shared Responsibility Model    | Division of security duties between Google and customers                          |
| Authentication & Authorization | Kubernetes RBAC, Google Cloud IAM integration, service account mapping            |
| Control Plane & Node Hardening | Securing the Kubernetes API server, node configuration, and credential management |
| Network Security               | VPC-native clusters, network policies, audit logging for visibility               |
| Data Protection                | Encryption at rest, in transit, and in use via Google Cloud encryption services   |

## 1. Shared Responsibility Model

Understanding who manages which layer of the stack is fundamental to securing GKE workloads.

* Google Cloud is responsible for the underlying infrastructure, control plane, and host OS patching.
* You, the customer, manage your container images, Kubernetes configurations, network policies, and workload permissions.

> **triangle-alert** Misconfiguring your side of the shared responsibility model can expose your applications to threats. Always verify IAM roles and network policies.

## 2. Authentication and Authorization

Securing access to your cluster begins with strong identity controls:

* **Kubernetes RBAC**\
  Define Roles and RoleBindings to grant fine-grained permissions within your cluster.
* **Google Cloud IAM**\
  Assign IAM roles at the project, folder, or organization level to control who can create and manage clusters.
* **Service Account Mapping**\
  Link Kubernetes ServiceAccounts to Google Service Accounts for workload identity and least-privilege access.

## 3. Control Plane and Node Hardening

Locking down your control plane and nodes ensures that only trusted workloads and administrators can interact with your cluster:

* Enable private clusters and restrict public endpoint access.
* Use Binary Authorization to enforce image attestation.
* Rotate and securely store cluster credentials.

## 4. Network Security

Effective network controls help prevent lateral movement and data exfiltration:

* Leverage VPC-native clusters to use [VPC Service Controls](https://cloud.google.com/vpc-service-controls) and private IPs.
* Define Kubernetes NetworkPolicies to restrict pod-to-pod communication.
* Enable VPC Flow Logs and Cloud Audit Logs for full visibility.

## 5. Data Protection

Protect sensitive information throughout its lifecycle:

* **At Rest**: Use Google-managed encryption keys or bring your own keys (BYOK) with Cloud Key Management Service.
* **In Transit**: Enforce TLS for all service-to-service and client-to-cluster communications.
* **In Use**: Explore Confidential GKE nodes to keep data encrypted even during processing.

***

By the end of this lesson, you’ll have a clear roadmap for implementing GKE security best practices across all layers of your cluster architecture. Proceed to the next section to dive into the Shared Responsibility Model in detail.

- [Watch Video](https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine/module/225743c4-eb6e-4393-a51e-4ed7d41dbe51/lesson/3922d8f9-c8f9-41f4-b5cb-aef2606195ab)
