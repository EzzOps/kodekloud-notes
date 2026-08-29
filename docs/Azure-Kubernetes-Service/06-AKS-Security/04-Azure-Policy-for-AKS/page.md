# Azure Policy for AKS

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/AKS-Security/Azure-Policy-for-AKS/page

This article explains how to use Azure Policy for governance and compliance in Azure Kubernetes Service (AKS).

Before diving into Azure Policy for Azure Kubernetes Service (AKS), let's review Azure Policy fundamentals: what it is, why it exists, and how to use it.

As enterprises deploy resources in Azure, they need to enforce organizational requirements—such as restricting deployments by region or controlling VM types. Common scenarios include:

* Ensuring business-critical applications remain in Australia for data-residency compliance.
* Preventing AKS clusters from using costly GPU-enabled VMs.

Azure Policy enables you to define and apply governance and compliance rules at scale. It uses JSON-based definitions to validate resource configurations during provisioning and continuously audit existing resources.

![The image illustrates an Azure Policy concept, showing a GPU-based machine with a red cross and a cost symbol with a green checkmark, suggesting a focus on cost management over GPU usage.](https://kodekloud.com/kk-media/image/upload/v1752869428/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-policy-gpu-cost-management.jpg)

You can scope policies to subscriptions, resource groups, or individual resources, ensuring a consistent security posture across your Azure estate.

![The image is a diagram illustrating Azure Policy, showing its application to Azure Subscriptions, Individual Resources, and Resource Groups.](https://kodekloud.com/kk-media/image/upload/v1752869429/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-policy-subscriptions-resources-diagram.jpg)

By enforcing policies, you reduce misconfiguration risks and maintain compliance with internal and external standards.

![The image illustrates the concept of Azure Policy, highlighting its role in ensuring a secure, compliant, and well-governed Azure environment.](https://kodekloud.com/kk-media/image/upload/v1752869430/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-policy-secure-compliant-governance.jpg)

***

## Assigning a Built-in Policy to Restrict AKS Deployments by Location

To block AKS clusters outside Australia, use a built-in Azure Policy definition:

1. In the Azure portal, navigate to **Policy** > **Authoring** > **Definitions**.
2. Search for built-in definitions and filter by **Type**.

![The image shows a Microsoft Azure portal page displaying a list of policy definitions. It includes options for filtering by scope, definition type, and category, with a table listing various built-in policies.](https://kodekloud.com/kk-media/image/upload/v1752869431/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-portal-policy-definitions-list.jpg)

3. Note the two definition types:

| Definition Type | Purpose                                                            |
| --------------- | ------------------------------------------------------------------ |
| Policy          | Single rule to enforce or audit (e.g., allowed locations)          |
| Initiative      | Logical grouping of multiple policies (e.g., AKS governance suite) |

4. Find **Allowed locations** and click **Assign**.

![The image shows a Microsoft Azure Policy Definitions page, displaying a list of policy initiatives with details such as name, definition location, number of policies, type, and category. The interface includes options for filtering and searching through the policies.](https://kodekloud.com/kk-media/image/upload/v1752869433/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-policy-definitions-page-details.jpg)

5. On the **Assignment** tab, set your subscription as the scope and click **Next**.
6. (Optional) Under **Advanced**, exclude specific resource types if needed.

![The image shows a Microsoft Azure portal page for assigning a policy titled "Allowed locations," with fields for scope, exclusions, and policy details. The policy enforcement is set to "Enabled."](https://kodekloud.com/kk-media/image/upload/v1752869434/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-portal-allowed-locations-policy.jpg)

7. In **Parameters**, pick `Australia East` and `Australia Southeast`. Resources outside these regions will be denied.

![The image shows a Microsoft Azure portal screen where a user is selecting allowed locations, with options related to Australia being displayed in a dropdown menu.](https://kodekloud.com/kk-media/image/upload/v1752869435/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-portal-allowed-locations-dropdown.jpg)

> **triangle-alert** If you enable **Remediation**, Azure Policy may move or delete non-compliant resources. Review potential impacts before proceeding.

8. Optionally, configure **Remediation** to correct existing resources, then add a custom message and click **Create**.

![The image shows a Microsoft Azure portal page for assigning a policy related to "Allowed locations." It includes sections for remediation, managed identity, and permissions, with a warning about missing role definitions.](https://kodekloud.com/kk-media/image/upload/v1752869436/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-portal-allowed-locations-policy-2.jpg)

9. Return to **Policy** > **Assignments** and refresh to confirm your new control.

![The image shows the Microsoft Azure Policy Assignments page, displaying details about policy and initiative assignments within a specified scope. It indicates one initiative assignment and zero policy assignments.](https://kodekloud.com/kk-media/image/upload/v1752869437/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-policy-assignments-page-details.jpg)

***

## Testing the Location Policy

Attempt to create an AKS cluster in `East US`:

* In the **Create a Kubernetes cluster** wizard, select **East US**, then **Review + create**.
* The deployment will fail with your custom message.

![The image shows a Microsoft Azure portal screen for creating a Kubernetes cluster, with a validation error indicating that the resource was disallowed by policy due to location restrictions.](https://kodekloud.com/kk-media/image/upload/v1752869438/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/azure-portal-kubernetes-cluster-error.jpg)

***

## Extending Governance Inside AKS with OPA & Gatekeeper

Azure Policy enforces resource-level rules but doesn’t inspect workloads inside AKS. For cluster-native policy enforcement, integrate [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) with Gatekeeper:

* **OPA**: cloud-native policy engine.
* **Gatekeeper**: Kubernetes admission controller for OPA policies.

Gatekeeper intercepts API requests, applies policies, and rejects non-compliant objects.

![The image illustrates the Open Policy Agent's role in evaluating and enforcing policies, with connections to an AKS Cluster and API Server.](https://kodekloud.com/kk-media/image/upload/v1752869439/notes-assets/images/Azure-Kubernetes-Service-Azure-Policy-for-AKS/open-policy-agent-aks-api-server.jpg)

***

## Enabling the Azure Policy Add-on in AKS

To deploy OPA Gatekeeper via Azure Policy:

1. Create an AKS cluster—e.g., `AKSPolicyDemo`.
2. In the Azure portal, open the cluster’s **Policies** blade (initially disabled).
3. From your CLI:

```bash theme={null}
