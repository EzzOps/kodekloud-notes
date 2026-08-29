# AppRole Auth Method

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Create-a-working-Vault-server-configuration-given-a-scenario/AppRole-Auth-Method/page

HashiCorp Vault’s AppRole auth method allows machines and automated pipelines to authenticate securely using a predefined role with Role ID and Secret IDs.

HashiCorp Vault’s AppRole auth method enables machines and automated pipelines to authenticate securely using a predefined role. Each AppRole consists of:

* A static **Role ID** (like a username).
* One or more **Secret IDs** (like one-time passwords).

Combining Role ID + Secret ID grants a Vault token, similar to how users log in with username and password.

> **lightbulb** AppRole is ideal for non-interactive workloads (CI/CD pipelines, containers, VMs) that require short-lived credentials.

## What Is AppRole?

AppRole is a secrets-engine authentication method in Vault. It’s commonly used when human interaction isn’t possible or desired. You:

1. Enable the `approle` auth method.
2. Create a role with policies, TTLs, and CIDR restrictions.
3. Distribute the static Role ID and dynamically generate Secret IDs.

## Authentication Workflow

1. Vault Admin enables AppRole and creates a role (e.g., `hcvop`).
2. Developer reads the static Role ID and bakes it into the container image.
3. CI/CD pipeline requests a new Secret ID (optionally wrapped).
4. Pipeline deploys the container, injecting Role ID + Secret ID.
5. Application logs in and receives a Vault token.

## Configuration Workflow

1. Enable the AppRole auth method at a path (default or custom).
2. Create a role with policies, TTL settings, and CIDR restrictions.
3. Read the constant Role ID.
4. Generate a unique Secret ID at deployment time.

## Why Use AppRole for a Fleet of Web Servers?

Multiple instances share the same Role ID but each receives a unique Secret ID. This approach:

* Prevents credential sharing between workloads.
* Enables single-workload revocation and auditing.

## AppRole Configuration Tips

Use the table below to tune your AppRole role:

| Parameter           | Description                                                               |
| ------------------- | ------------------------------------------------------------------------- |
| token\_policies     | Vault policies attached to the generated token (e.g., `web-app`).         |
| token\_ttl          | Default TTL for tokens issued under this role (e.g., `1h`).               |
| token\_max\_ttl     | Maximum TTL users can renew tokens to (e.g., `24h`).                      |
| secret\_id\_ttl     | Time-to-live for unused Secret IDs to limit exposure.                     |
| token\_bound\_cidrs | List of CIDR blocks from which the token is valid (e.g., `10.1.16.0/16`). |
| token\_type         | Token type (`service` or `batch`). Batch tokens cannot be renewed.        |

## Step-by-Step Guide

### 1. Enable the AppRole Auth Method

```bash theme={null}
