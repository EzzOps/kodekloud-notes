# Azure Automation State Configuration

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-Infrastructure-as-Code-IaC/Azure-Automation-State-Configuration/page

Azure Automation Desired State Configuration (DSC) automates system configurations, ensuring consistency and drift correction across Azure and on-premises environments.

Azure Automation Desired State Configuration (DSC) is a powerful service for defining, deploying, and enforcing system configurations at scale. By authoring PowerShell-based DSC scripts, you can automate consistency checks and drift correction across Azure and on-premises environments—eliminating manual errors and saving operational time.

<Frame>
  ![The image is an infographic titled "Azure Automation State Configuration," showing three steps: automating checking, updating, and deployment configurations.](https://kodekloud.com/kk-media/image/upload/v1752867688/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Automation-State-Configuration/azure-automation-state-configuration-infographic.jpg)
</Frame>

## Key Benefits

| Benefit                       | Description                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| Centralized Management        | Single pane of glass to manage DSC configurations across subscriptions and regions. |
| Automatic Drift Correction    | Continuous monitoring with automatic remediation of configuration drift.            |
| Detailed Compliance Reporting | Out-of-the-box dashboards and logs to track node compliance over time.              |

***

## Scenario: Enforce Software on Multiple Windows VMs

In this walkthrough, we'll ensure a scheduled PowerShell task is installed and maintained on several Azure Windows VMs using Azure Automation DSC.

<Frame>
  ![The image is an example of Azure Automation State Configuration, detailing a scenario of managing configurations for multiple VMs, with the objective of ensuring specific software installation on Windows VMs, using tools like Azure Automation State Configuration and Azure VMs.](https://kodekloud.com/kk-media/image/upload/v1752867690/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Automation-State-Configuration/azure-automation-state-configuration-vms.jpg)
</Frame>

### Prerequisites

* Azure subscription with contributor or automation operator role
* Azure VM Agent installed on each target VM
* [Az.Automation PowerShell module](https://www.powershellgallery.com/packages/Az.Automation) installed locally

<Callout icon="triangle-alert">
  Before registering VMs for DSC, ensure the Azure VM Agent is up to date. Without it, DSC cannot communicate with the Automation account.
</Callout>

***

## Step 1: Create an Automation Account

Your Automation Account is the central hub for DSC configurations, runbooks, and assets.

1. In the Azure portal, search for **Automation Accounts**.
2. Click **+ Create**, fill in the name, resource group, and region.
3. Review and **Create**.

<Frame>
  ![The image shows a Microsoft Azure interface for creating an automation account, with a highlighted button to "Create automation account." It indicates that there are currently no automation accounts to display.](https://kodekloud.com/kk-media/image/upload/v1752867691/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Automation-State-Configuration/azure-automation-account-creation-interface.jpg)
</Frame>

***

## Step 2: Register Your VM as a DSC Node

Once the Automation Account is active, add your Windows VM as a DSC node.

1. Navigate to **State Configuration (DSC)** > **Nodes**.
2. Click **Add** > **Azure VM**.
3. Select your subscription, resource group, and VM.
4. Configure:
   * **Refresh Frequency**: Interval for DSC pull (e.g., 30 minutes)
   * **Configuration Mode**: `ApplyAndAutoCorrect` or `ApplyAndMonitor`

<Frame>
  ![The image shows a screenshot of the Azure Automation State Configuration interface, highlighting the "TestAutomationAccount" with options for managing configurations and nodes. It includes a navigation menu on the left and a status dashboard on the right.](https://kodekloud.com/kk-media/image/upload/v1752867692/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Automation-State-Configuration/azure-automation-state-configuration-screenshot.jpg)
</Frame>

On the registration settings page, enter the **Registration Key**, **Node Configuration Name**, and **Refresh Interval**.

<Frame>
  ![The image shows a screenshot of the Azure Automation State Configuration interface, specifically the registration settings for configuring DSC (Desired State Configuration) for a virtual machine. It includes fields for registration key, node configuration name, refresh frequency, and other options.](https://kodekloud.com/kk-media/image/upload/v1752867693/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Automation-State-Configuration/azure-automation-dsc-registration-settings.jpg)
</Frame>

After registration, the VM appears in the DSC **Nodes** view marked **Compliant** (no custom configurations yet).

***

## Step 3: Author and Import Your DSC Configuration

Define a DSC configuration that schedules a PowerShell task to run daily at midnight and repeat every 15 minutes for 8 hours.

```powershell theme={null}
Configuration ScheduledTaskDaily {
    Node 'localhost' {
        ScheduledTask ScheduledTaskDailyAdd {
            TaskName         = 'Test task Daily'
            TaskPath         = 'MyTasks'
            ActionExecutable = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
            ScheduleType     = 'Daily'
            DaysInterval     = 1
            RepeatInterval   = '00:15:00'
            StartBoundary    = '2023-10-01T00:00:00'
            RepeatDuration   = '08:00:00'
        }
    }
}
