# Service Accounts

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Cluster-Setup-and-Hardening/Service-Accounts/page

This article provides a comprehensive guide on service accounts in Kubernetes, focusing on their creation, management, and security features.

Welcome to this comprehensive guide on service accounts in Kubernetes. In this article, we will explain how to work with service accounts—an essential mechanism that enables applications and machines to interact securely with the Kubernetes API. While Kubernetes includes various security features, such as authentication, authorization, and role-based access controls, this guide specifically focuses on service accounts to support application development. For more details on broader security topics, please refer to the [CKA Certification Course - Certified Kubernetes Administrator](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator).

## Account Types in Kubernetes

Kubernetes supports two types of accounts:

* **User Account:** Used by humans (e.g., administrators or developers).
* **Service Account:** Used by applications or machines (e.g., monitoring tools like Prometheus or CI/CD systems like Jenkins).

Consider a simple example of a Kubernetes dashboard written in Python. The dashboard queries the Kubernetes API to list all Pods and displays the output on a web interface. To authenticate with the Kubernetes API, the dashboard leverages a service account.

<Frame>
  ![The image shows a Kubernetes dashboard interface connected to a Kubernetes cluster with three nodes via the kube-api.](https://kodekloud.com/kk-media/image/upload/v1752871397/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Service-Accounts/frame_110.jpg)
</Frame>

## Creating and Managing Service Accounts

To create a service account for your application, run the following command. In this example, we create a service account named `dashboard-sa`:

```bash theme={null}
kubectl create serviceaccount dashboard-sa
```

After creation, view all service accounts in the current namespace using:

```bash theme={null}
kubectl get serviceaccount
```

When a service account is created, Kubernetes automatically generates a token and stores it as a Secret object. This token is then used by your application for API authentication. An example output could be:

```bash theme={null}
kubectl create serviceaccount dashboard-sa
