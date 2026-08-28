# Demo Running Vault in Production

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Installing-Vault/Demo-Running-Vault-in-Production/page

This hands-on tutorial guides setting up HashiCorp Vault on AWS EC2 with integrated Raft storage and AWS KMS auto-unseal.

In this hands-on tutorial, you'll set up a single HashiCorp Vault node on an [AWS EC2][ec2] instance using integrated Raft storage, AWS KMS auto-unseal, and a basic TCP listener. We assume you’ve already provisioned your EC2 instance (e.g., via [Packer][packer]) and dropped the Vault binary and example configs into `/tmp`.

## Table of Contents

1. [Install the Vault Binary](#1-install-the-vault-binary)
2. [Create a Vault System User and Directories](#2-create-a-vault-system-user-and-directories)
3. [Define the Systemd Service](#3-define-the-systemd-service)
4. [Vault Configuration (`vault.hcl`)](#4-vault-configuration-vaulthcl)
5. [Start and Verify Vault](#5-start-and-verify-vault)
6. [References](#6-references)

## 1. Install the Vault Binary

SSH into your EC2 instance and place the Vault executable in your `PATH`.

```bash theme={null}
