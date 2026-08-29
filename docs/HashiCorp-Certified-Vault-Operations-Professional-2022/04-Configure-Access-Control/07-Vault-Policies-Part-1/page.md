# Vault Policies Part 1

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Configure-Access-Control/Vault-Policies-Part-1/page

This guide explains how Vault policies control access to secrets and paths in HashiCorp Vault.

Welcome to Vault Policies Part 1. Whether you’re a Vault operator or preparing for the [Certified Vault Operations Professional exam](https://www.hashicorp.com/certification/vault-operations-professional), mastering policies is essential. In this guide, you’ll learn how Vault policies define which clients—CI/CD pipelines, auditors, Terraform, DevOps engineers, admins, Packer, web apps, and more—can access specific secrets and paths.

![The image is a diagram illustrating how different roles and applications, such as admins, DevOps engineers, and CI/CD pipelines, interact with a central system to determine access to secrets. It includes various icons and arrows indicating the flow of access.](https://kodekloud.com/kk-media/image/upload/v1752878365/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Policies-Part-1/access-secrets-diagram-roles-flow.jpg)

## What Are Vault Policies?

Vault policies are declarative rules (in HCL or JSON) that grant or deny capabilities on Vault paths. They provide fine-grained, RBAC-style access control. Most operators prefer HCL for readability.

> **lightbulb** Always adhere to the principle of least privilege. Grant only the permissions required for an entity to perform its tasks.

By default, Vault enforces an implicit deny: if no policy grants access to a path, the request is denied. You can also add explicit `deny` rules to override grants. Policies are attached to tokens and other auth entities; multiple policies on a token combine their permissions cumulatively.

![The image is a slide about Vault Policies, explaining their role in access control, the use of JSON or HCL for writing policies, and the importance of following the principle of least privilege. It includes a Vault certification badge.](https://kodekloud.com/kk-media/image/upload/v1752878367/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Policies-Part-1/vault-policies-access-control-principle.jpg)

## Built-In (Out-of-the-Box) Policies

Immediately after deployment, Vault includes two default policies:

| Policy Name | Type      | Description                                                                                                                                            |
| ----------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **root**    | Superuser | Full privileges (`create, read, update, delete, list, sudo`). Non-editable and auto-attached only to root tokens.                                      |
| **default** | Baseline  | Basic token operations (`lookup-self`, `renew-self`, `revoke-self`, `capabilities-self`). Editable but cannot be deleted; auto-attach can be disabled. |

![The image describes "Out of the Box Policies" for a system, detailing the default "root" and "default" policies, their permissions, and their attachment to tokens. It also features a Vault certification badge.](https://kodekloud.com/kk-media/image/upload/v1752878368/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Vault-Policies-Part-1/out-of-the-box-policies-defaults-vault.jpg)

To list and inspect these policies:

```bash theme={null}
vault policy list
