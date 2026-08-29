# Demo Unsealing with Transit Auto Unseal

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Learning-the-Vault-Architecture/Demo-Unsealing-with-Transit-Auto-Unseal/page

This guide explains how to configure a Vault cluster for centralized Transit auto-unseal, automating the unsealing process during initialization.

In this guide, we’ll show you how to configure one Vault cluster as a centralized Transit auto-unseal backend for another Vault cluster. Using Vault’s Transit Secrets Engine, the target cluster will automatically unseal during initialization, reducing manual intervention.

## Environment Overview

We have two Vault clusters running in an AWS environment:

| Cluster         | IP Address | Role                          |
| --------------- | ---------- | ----------------------------- |
| Transit Cluster | 10.0.1.209 | Transit Secrets Engine server |
| Target Cluster  | 10.0.1.37  | Raft-backed Vault instance    |

Open SSH sessions to both nodes before proceeding:

```bash theme={null}
