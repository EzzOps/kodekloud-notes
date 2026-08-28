# Designing an Agent Infrastructure

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-Pipelines/Designing-an-Agent-Infrastructure/page

This article explores designing and configuring build agent infrastructure in Azure DevOps, covering hosted vs. self-hosted agents and best practices for scaling and customization.

In this article, we’ll explore how to design and configure build agent infrastructure in [Azure DevOps][azure-devops]. You’ll learn the differences between hosted and self-hosted agents, see how to launch agents on Windows, Linux, Docker, and macOS, and review best practices for scaling and customization.

## Hosted vs. Self-Hosted Agents

Build agents in Azure Pipelines fall into two categories:

| Feature             | Hosted Agents                     | Self-Hosted Agents                       |
| ------------------- | --------------------------------- | ---------------------------------------- |
| Management          | Microsoft-maintained              | You manage VMs, servers or containers    |
| Supported platforms | Windows, Linux, macOS             | Any OS you provision                     |
| Customization       | Preinstalled tools, limited tweak | Full control over tool versions & images |
| Scaling & cost      | Auto-scaled, pay-per-minute       | Optimize infrastructure & licensing      |

Host agents are turnkey and zero-maintenance, while self-hosted agents give you full control over the software stack and cost structure.

## Viewing Agent Pools

Navigate in Azure DevOps to **Organization settings** → **Agent pools** to see all your pools and agents:

<Frame>
  ![The image shows the "Agent pools" settings page in Azure DevOps, listing different agent pools such as Azure Pipelines, Default, Linux, and Mac. The interface includes options for adding a new pool and managing security settings.](https://kodekloud.com/kk-media/image/upload/v1752867837/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Designing-an-Agent-Infrastructure/azure-devops-agent-pools-settings.jpg)
</Frame>

Here you’ll find pools like **Azure Pipelines** (hosted), **Default**, **Linux**, and **Mac**.

### Hosted Agents

The **Azure Pipelines** pool contains Microsoft-hosted agents:

<Frame>
  ![The image shows the Azure DevOps interface, specifically the "Agent pools" section under "Organization Settings," displaying details of a hosted agent that is currently running a build.](https://kodekloud.com/kk-media/image/upload/v1752867838/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Designing-an-Agent-Infrastructure/azure-devops-agent-pools-interface.jpg)
</Frame>

* Always online and listening
* Supports Windows, Linux, and macOS jobs
* No infrastructure maintenance required

## Setting Up Self-Hosted Agents

Self-hosted agents run on machines you control—physical servers, cloud VMs, or containers. Below are step-by-step examples for Windows, Docker, Linux (WSL & standalone), and macOS.

### 1. Windows Self-Hosted Agent

In the **Default** pool, you might see two offline Windows agents:

<Frame>
  ![The image shows an Azure DevOps interface displaying the "Agent pools" settings, with two agents listed as offline. The sidebar includes various options like Overview, Projects, and Security.](https://kodekloud.com/kk-media/image/upload/v1752867839/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Designing-an-Agent-Infrastructure/azure-devops-agent-pools-settings-offline.jpg)
</Frame>

To bring one online:

```powershell theme={null}
