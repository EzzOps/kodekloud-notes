# Demo Terraform Cloud Run Agents

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Advanced-Topics/Demo-Terraform-Cloud-Run-Agents/page

This guide covers setting up Terraform Clouds self-hosted agents for secure execution of Terraform runs within private networks.

In this guide, we’ll walk through setting up Terraform Cloud’s self-hosted agents—a Business tier feature that allows Terraform runs to execute within your private network. By using agents, you eliminate the need to expose sensitive endpoints publicly, making them ideal for on-premises data centers, private VPCs, or any environment where Terraform Cloud cannot directly reach your infrastructure.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Creating an Agent Pool and Token](#creating-an-agent-pool-and-token)
3. [Installing and Running an Agent on Linux](#installing-and-running-an-agent-on-linux)
4. [Running an Agent in Docker](#running-an-agent-in-docker)
5. [Agent Auto-Update Behavior](#agent-auto-update-behavior)
6. [Configuring a Workspace for Agent Execution](#configuring-a-workspace-for-agent-execution)
7. [Running Terraform via the Agent](#running-terraform-via-the-agent)
8. [Scaling with Multiple Agents](#scaling-with-multiple-agents)
9. [Managing Pools and Tokens](#managing-pools-and-tokens)
10. [References](#references)

## Prerequisites

* A Terraform Cloud organization on the Business tier
* Permissions to manage **Settings → Agents**
* Outbound TCP/443 connectivity to `app.terraform.io`

<Callout icon="lightbulb">
  Agents use a pull-based model and require **only outbound TCP/443** access to Terraform Cloud.
</Callout>

## Creating an Agent Pool and Token

An **Agent Pool** is a logical group of self-hosted agents. You scope pools to environments (e.g., `development`, `production`) and assign tokens for authentication.

| Component  | Description                                       | Example Command                         |
| ---------- | ------------------------------------------------- | --------------------------------------- |
| Agent Pool | Logical grouping of agents                        | Manage under **Settings → Agents**      |
| API Token  | Scoped to one pool; used by each registered agent | Created via the **Create token** button |
| Agent Name | Unique identifier for each host/container         | `east-dc-1`, `us-west-2`                |

1. Navigate to **Settings → Agents** in your Terraform Cloud organization.
2. Click **New Agent Pool**, name it (e.g., **development**), and save.
3. In the pool’s page, click **Create token**, scope it to your data center or environment (e.g., `EastDC`), and copy the value.

<Callout icon="triangle-alert">
  Keep your agent tokens confidential. Rotate or revoke tokens regularly to maintain security.
</Callout>

## Installing and Running an Agent on Linux

Download and unzip the latest agent binary on any Linux host:

```bash theme={null}
