# A quick note about Helm2 vs Helm3

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Helm-Basics-2025-Updates/A-quick-note-about-Helm2-vs-Helm3/page

This article explains the differences between Helm 2 and Helm 3, focusing on improvements in usability and security for Kubernetes charts.

Helm has evolved significantly since its inception, and understanding the differences between Helm 2 and Helm 3 is crucial when working with Kubernetes charts. This article provides a brief history of Helm and highlights the key improvements introduced in Helm 3, offering insights into its enhanced usability and security.

## A Brief History of Helm

Helm's journey began in February 2016 with Helm 1.0, followed by Helm 2.0 in November 2016. The major milestone was achieved with the release of Helm 3.0 in November 2019. As Kubernetes itself advanced, Helm matured to better leverage Kubernetes functionalities, resulting in a more robust and secure package management experience.

<Frame>
  ![The image is a timeline titled "Helm History," showing the release dates of Helm versions 1.0 in February 2016, 2.0 in November 2016, and 3.0 in November 2019.](https://kodekloud.com/kk-media/image/upload/v1752869777/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-A-quick-note-about-Helm2-vs-Helm3/helm-history-timeline-releases.jpg)
</Frame>

## Helm 2: The Role of Tiller

In the era of Helm 2, Kubernetes limitations such as the absence of role-based access control (RBAC) and custom resource definitions (CRDs) meant that an additional component, Tiller, was required. Tiller acted as an intermediary between the Helm CLI and the Kubernetes cluster, managing the installation and upgrade of charts. However, this approach introduced several challenges:

* **Complexity:** The interaction between the CLI and Tiller added an extra layer to the deployment process.
* **Security Risks:** Tiller operated with broad privileges, often referred to as running in "God mode," increasing the risk of potential security issues.

<Frame>
  ![The image is a diagram illustrating the architecture of Helm 2, showing the interaction between the Helm CLI and Tiller within a Kubernetes environment, with notes on Role-Based Access Control and Custom Resource Definitions.](https://kodekloud.com/kk-media/image/upload/v1752869777/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-A-quick-note-about-Helm2-vs-Helm3/helm-2-architecture-diagram-kubernetes.jpg)
</Frame>

<Callout icon="triangle-alert">
  Using Tiller in Helm 2 means that any misconfiguration could lead to elevated security risks due to its extensive privileges.
</Callout>

## Helm 3: Simplified and Secure

Helm 3 brings notable improvements by eliminating the need for Tiller. Instead, the Helm client now communicates directly with Kubernetes, leveraging its native RBAC capabilities. This change simplifies the architecture and enhances security, as every Helm action is subject to the same RBAC permissions applied when using kubectl.

<Frame>
  ![The image is a diagram illustrating Helm 3's architecture, showing the interaction between the Helm CLI, Kubernetes, and the use of role-based access control and custom resource definitions.](https://kodekloud.com/kk-media/image/upload/v1752869778/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-A-quick-note-about-Helm2-vs-Helm3/helm-3-architecture-diagram.jpg)
</Frame>

## Key Differences Between Helm 2 and Helm 3

| Feature                | Helm 2                                | Helm 3                                       |
| ---------------------- | ------------------------------------- | -------------------------------------------- |
| Intermediary Component | Requires Tiller                       | No intermediary; direct communication        |
| Security Model         | Elevated risk due to broad privileges | Enhanced security leveraging Kubernetes RBAC |
| Rollback Mechanism     | Basic revision comparison             | Three-way strategic merge patch              |

## Improved Rollback and Upgrade Process in Helm 3

One of the significant advancements in Helm 3 is the handling of rollbacks through a three-way strategic merge patch, resembling a snapshot mechanism. Consider the example of deploying a WordPress website using a Helm chart:

1. **Installation:** When you install the chart, Helm creates revision 1.
2. **Upgrade:** After changing configurations, such as upgrading the WordPress image, Helm creates revision 2.
3. **Rollback:** If needed, reverting to revision 1 will restore the previous state.

Below is an example of the process:

```bash theme={null}
$ helm install wordpress
$ helm upgrade wordpress
```

### Revision Changes in YAML

```yaml theme={null}
