# Demo RBAC Roles and Bindings

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/Demo-RBAC-Roles-and-Bindings/page

Guide to Kubernetes RBAC explaining Roles, ClusterRoles, RoleBindings, ClusterRoleBindings, service account bindings, testing permissions with kubectl auth can-i and debugging for least privilege

Everything in Kubernetes starts with one question: who is allowed to do what and where? Role-Based Access Control (RBAC) answers that question. It's a cornerstone of Kubernetes security: misconfigured RBAC can leave your cluster unusable or dangerously over-permissive.

The model is simple and powerful:

* Roles (or ClusterRoles) define permissions (verbs on resources).
* RoleBindings (or ClusterRoleBindings) attach those permissions to identities: users, groups, or service accounts.

In this guide we'll cover namespaced Roles and cluster-scoped ClusterRoles, show how to bind them to users and service accounts, and demonstrate how to test and debug permissions.

## Check namespaces and service accounts

Start by listing your namespaces and the service accounts in team namespaces:

```bash theme={null}
