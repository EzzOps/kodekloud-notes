# Authorization

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Cluster-Setup-and-Hardening/Authorization/page

This article explains how Kubernetes manages authorization to control user operations within a cluster.

In this article, we explain how Kubernetes handles authorization. After establishing access to a cluster through authentication (as discussed in our previous article), authorization determines which operations a user—whether human or machine—can perform within the cluster.

For example, a cluster administrator can view, create, or delete objects such as pods, nodes, and deployments. However, when granting access to additional users (e.g., developers, testers, other administrators, or external applications like [Jenkins](https://learn.kodekloud.com/user/courses/jenkins) and monitoring tools), it is best practice to restrict their privileges. Developers might be allowed to view pods and deploy applications but should not modify cluster configurations or delete nodes. Similarly, when sharing a cluster among multiple organizations or teams using namespaces, each user’s access should be confined to their designated namespace.

<Callout icon="lightbulb">
  Adjust user privileges using authorization policies to ensure cluster security and maintain operational integrity.
</Callout>

Below are some example commands demonstrating typical administrative operations:

```bash theme={null}
kubectl get pods
