# Demo Configure Service Account with RBAC Settings

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/Demo-Configure-Service-Account-with-RBAC-Settings/page

Configuring a dedicated ServiceAccount and RBAC so an Argo Events Sensor can securely submit Argo Workflows into a target namespace, avoiding permission errors.

In this lesson you'll configure a dedicated ServiceAccount and RBAC rules so an Argo Events Sensor can submit Argo Workflows into a target namespace. This resolves "permission denied" errors when the Sensor attempts to create a Workflow using the cluster default ServiceAccount.

Why this matters:

* Using a scoped ServiceAccount with minimal RBAC permissions is more secure than relying on the default ServiceAccount.
* It prevents permission errors and enables the Sensor to create Workflows in a separate namespace.

Problem evidence (sensor error when using the default ServiceAccount):

```json theme={null}
{
  "namespace": "argo-events",
  "sensorName": "webhook-sensor",
  "level": "error",
  "time": "2025-10-25T11:00:39Z",
  "msg": "Create request failed",
  "error": "workflows.argoproj.io is forbidden: User \"system:serviceaccount:argo-events:default\" cannot create resource \"workflows\" in API group \"argoproj.io\" in the namespace \"argo\""
}
```

This shows the Sensor (running in `argo-events`) attempted to create a Workflow in the `argo` namespace using the `default` ServiceAccount and was forbidden.

Planned steps:

1. Create a ServiceAccount in the Sensor's namespace (`argo-events`).
2. Create a Role and RoleBinding in the target namespace (`argo`) to allow the ServiceAccount to create/read Workflows.
3. Update the Sensor to use the new ServiceAccount.
4. Trigger the Sensor and confirm the Workflow is created.

***

## Resources Overview

| Resource Type     | Purpose                                                           | Example                            |
| ----------------- | ----------------------------------------------------------------- | ---------------------------------- |
| ServiceAccount    | Identity used by the Sensor when creating Workflows               | `workflow-trigger-sa`              |
| Role              | Grants Workflow permissions in the target namespace               | `submit-workflow-role`             |
| RoleBinding       | Binds the ServiceAccount from `argo-events` to the Role in `argo` | `trigger-workflow-binding`         |
| Sensor spec field | Instructs the Sensor which ServiceAccount to use                  | `spec.template.serviceAccountName` |

References:

* [Argo Events - Sensor](https://argoproj.github.io/argo-events/reference/sensor/)
* [Argo Workflows](https://argoproj.github.io/argo-workflows/)
* [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

***

## 1. Create the ServiceAccount

First, list existing ServiceAccounts in the `argo-events` namespace, then create a new one called `workflow-trigger-sa`:

```bash theme={null}
