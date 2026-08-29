# Success! Enabled the kv secrets engine at: kv/
```

Enable KV v1 at a custom path:

```bash theme={null}
vault secrets enable -path=training kv
# Success! Enabled the kv secrets engine at: training/
```

List mounts with version info:

```bash theme={null}
vault secrets list -detailed
# Path       Plugin    Accessor       Options
# ----       ------    --------       -------
# cubbyhole/ cubbyhole cubbyhole_xyz  map[]
# kv/        kv        kv_abc123      map[]        # v1
# training/  kv        kv_def456      map[]        # v1
```

Enable KV v2 at a new mount:

```bash theme={null}
vault secrets enable -path=kv-v2 -version=2 kv
# Success! Enabled the kv-v2 secrets engine at: kv-v2/
```

Verify mounts:

```bash theme={null}
vault secrets list -detailed
# kv-v2/ kv kv_ghi789 map[version:2]   # v2
```

> **triangle-alert** Upgrading an existing KV v1 mount to v2 is irreversible. Plan carefully before enabling versioning.

Enable versioning on an existing mount:

```bash theme={null}
vault kv enable-versioning training/
# Success! Tuned the secrets engine at: training/
```

## Organizing Secrets with KV Paths

Plan a path hierarchy to simplify policies and discovery.

Option A: Single mount with folders

```text theme={null}
kv/
├── cloud/
│   ├── aws/
│   ├── gce/
│   └── …
├── automation/
│   ├── dev/
│   ├── prod/
│   └── …
└── data/
    ├── warehousing/
    └── analytics/
```

Option B: Multiple mounts per domain

| Mount Path  | Purpose                 | Version |
| ----------- | ----------------------- | ------- |
| cloud/      | Cloud credentials       | v2      |
| automation/ | CI/CD & scripts         | v2      |
| data/       | Analytics & warehousing | v2      |

![The image is a diagram illustrating a Key/Value Secrets Engine, showing how data can be organized into categories like cloud, automation, and data, with subcategories for each.](https://kodekloud.com/kk-media/image/upload/v1752878110/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-KeyValue-Secrets-Engine/key-value-secrets-engine-diagram.jpg)

![The image illustrates a Key/Value Secrets Engine with multiple KV stores, showing a hierarchical organization of data related to cloud, data, and automation. It includes various nodes like "cloud," "data," and "automation," each branching into specific categories such as "aws," "jenkins," and "prod."](https://kodekloud.com/kk-media/image/upload/v1752878111/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-KeyValue-Secrets-Engine/key-value-secrets-engine-hierarchy.jpg)

### Path Example: `apps/`

```text theme={null}
apps/
└─ aws/
   ├─ prod/   ← { user, password, API }
   └─ dev/    ← { certificate, private_key }
```

* Mount: `apps/`
* Secret path: `apps/aws/prod`
* Read: `vault kv get apps/aws/prod`

![The image illustrates a Key/Value Secrets Engine with a hierarchical path structure for storing secrets, showing paths for "prod" and "dev" environments under "apps/aws".](https://kodekloud.com/kk-media/image/upload/v1752878112/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-KeyValue-Secrets-Engine/key-value-secrets-engine-hierarchy-2.jpg)

## KV v2 Metadata & API Prefixes

KV v2 adds metadata (versions, timestamps, deletion status). It introduces two API prefixes:

* `data/` – stores secret values
* `metadata/` – tracks version history

Mounting v2 at `cloud/` yields:

* `/v1/cloud/data/...` for secret operations
* `/v1/cloud/metadata/...` for metadata

The CLI abstracts these, so `vault kv get cloud/apps/aws` works without prefix.

![The image explains how KV V2 is different by adding metadata to key-value entries, supporting versioning, and introducing two prefixes for data and metadata.](https://kodekloud.com/kk-media/image/upload/v1752878114/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-KeyValue-Secrets-Engine/kv-v2-metadata-versioning-prefixes.jpg)

![The image explains the structure and path differences in KV V2, highlighting a hierarchy of cloud data paths and the use of a "data/" prefix to read secrets.](https://kodekloud.com/kk-media/image/upload/v1752878115/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-KeyValue-Secrets-Engine/kv-v2-structure-data-paths-diagram.jpg)

![The image explains differences in KV V2, highlighting the requirement of "data/" and "metadata/" prefixes for API and Vault policies, and notes that CLI interaction remains unchanged. It reassures with a message about upcoming examples.](https://kodekloud.com/kk-media/image/upload/v1752878116/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-KeyValue-Secrets-Engine/kv-v2-api-metadata-prefixes-explained.jpg)

## Versioning Workflow in KV v2

Leverage versioning for history, rollback, undelete, and destruction:

1. Write v1
   ```bash theme={null}
   vault kv put cloud/apps/aws user=admin password=123 api=XYZ
   ```
2. Update → v2
   ```bash theme={null}
   vault kv put cloud/apps/aws user=admin password=456 api=ABC
   ```
3. Delete latest
   ```bash theme={null}
   vault kv delete cloud/apps/aws
   ```
4. Undelete v2 → creates v3
   ```bash theme={null}
   vault kv undelete cloud/apps/aws --versions=2
   ```
5. Destroy v3
   ```bash theme={null}
   vault kv destroy cloud/apps/aws --versions=3
   ```
6. New write → v4

![The image explains the versioning process in KV V2, showing steps for writing, updating, deleting, and rolling back a secret, with different versions indicated.](https://kodekloud.com/kk-media/image/upload/v1752878118/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-KeyValue-Secrets-Engine/kv-v2-versioning-process-diagram.jpg)

## Next Steps

* Practice writing, reading, updating, and deleting KV secrets
* Explore versioning and metadata queries
* Define Vault policies to secure KV paths

## Links and References

* [Vault KV Secrets Engine Documentation](https://www.vaultproject.io/docs/secrets/kv)
* [HashiCorp Vault Overview](https://www.vaultproject.io/docs/)
* [Terraform Registry](https://registry.terraform.io/)
* [Jenkins Plugins](https://plugins.jenkins.io/)
* [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/cb962cde-84d3-4b26-8875-e8f093d77244/lesson/1860f23b-0aeb-4406-8f17-c67b91cf1a3f)


# Section Overview

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-and-Configure-Secrets-Engines/Section-Overview/page

This article covers Vault Secrets Engines, their functions, and exam objectives related to selecting and understanding different types of secrets in HashiCorp Vault.

Vault Secrets Engines are the core building blocks of any [HashiCorp Vault](https://www.vaultproject.io/) deployment. They handle everything from storing static secrets and generating dynamic credentials to issuing certificates and performing encryption. In fact, every Vault feature you interact with is delivered via a Secrets Engine.

Below are the Vault Associate Exam objectives related to Secrets Engines:

| Exam Objective                           | Description                                                      |
| ---------------------------------------- | ---------------------------------------------------------------- |
| Choose a secret method based on use case | Identify the appropriate Secrets Engine for different scenarios  |
| Contrast static vs. dynamic secrets      | Explain the differences and ideal use cases for each secret type |
| Define the Transit Secrets Engine        | Understand the purpose and functionality of the Transit engine   |
| Define what Secrets Engines are          | Describe the role and mechanics of Secrets Engines in Vault      |

Although the exam lists these objectives in the order above, this guide follows a more natural progression:

1. What is a Secrets Engine?
2. Static vs. Dynamic Secrets
3. Selecting the Right Secrets Engine for Your Use Case
4. Deep Dive: The Transit Secrets Engine

Let’s get started!

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/cb962cde-84d3-4b26-8875-e8f093d77244/lesson/9217c679-60fb-40ac-ad9c-def62caf4b54)
