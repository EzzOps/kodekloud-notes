# Azure AD Connect Demonstration

Source: https://notes.kodekloud.com/docs/Microsoft-Azure-Security-Technologies-AZ-500/Hybrid-Identity/Azure-AD-Connect-Demonstration/page

This guide covers deploying Azure AD Connect for hybrid identity, including setting up a Domain Controller and synchronizing on-premises users with Azure AD.

Welcome to this detailed guide on deploying Azure AD Connect for a hybrid identity environment. In this lesson, you'll learn how to set up a Domain Controller (DC), a domain-joined client machine, and synchronize on-premises users with Azure AD. Although these machines can be created manually, pre-written PowerShell scripts are available in a repository (which will be public after the recording). These scripts automate the following tasks:

1. Preparing the virtual machines (VMs)
2. Preparing the users
3. Preparing the Domain Controller

<Frame>
  ![The image shows a GitHub repository interface with a list of PowerShell script files related to "Hybrid Identity" under the "kodekloud-az500" project. The files include "prep-dc.ps1," "prep-users.ps1," "prep-vms.ps1," and "prepare-vms.ps1."](https://kodekloud.com/kk-media/image/upload/v1752881899/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Azure-AD-Connect-Demonstration/github-repo-hybrid-identity-scripts.jpg)
</Frame>

<Callout icon="lightbulb">
  To deploy all required resources, clone the repository and execute the scripts from the specified deployment directory. Running the scripts from a different directory may lead to internal script reference issues.
</Callout>

## Running the Deployment Scripts

Once you have cloned the repository, run the scripts from the deployment directory. The only manual steps are logging into the client server, joining it to the domain, and installing Azure AD Connect. All other configurations are handled by the scripts.

Below is an example command to run one of the scripts locally:

```powershell theme={null}
PS C:\Users\RithinSkaria\Documents\kodekloud-az500> & '.\30-Hybrid Identity\prep-vms.ps1'
```

When executed, the script will prompt you for a resource group name. For example, entering "azure-dc-connect" initiates the following output:

```powershell theme={null}
PS C:\Users\RithinSkaria\Documents\kodekloud-az500> & '.\30-Hybrid Identity\prep-vms.ps1'
Azure AD Connect Demo - v1.0, written by Rithin Skaria
(new) Resource Group Name: azure-dc-connect
INFO: Az Module is already installed, skipping to next step
WARNING: To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code L8KN8A64WG to authenticate.
```

<Callout icon="triangle-alert">
  Ensure you run the console window as an administrator. The script needs administrator privileges to update the execution policy and import necessary modules.
</Callout>

After authentication via the Microsoft device login, the script deploys the resource group, subnet, virtual network, and the domain controller.

<Frame>
  ![The image shows a Microsoft Azure portal interface with a PowerShell window open, displaying a command prompt in a specific directory.](https://kodekloud.com/kk-media/image/upload/v1752881899/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Azure-AD-Connect-Demonstration/azure-portal-powershell-command.jpg)
</Frame>

During deployment, you might see output similar to this:

```plaintext theme={null}
ps C:\Users\RithinSkaria\Documents\kodekloud-az500> & '.\30-Hybrid Identity\prep-vms.ps1'
Azure AD Connect Demo - v1.0, written by Rithin Skaria
Creating Azure resources
27% [oooooooooooooooooooooooo]
Creating virtualMachines/dc=01.
rithinskariaq@kodekloud.com Kodekloud - AZ500 - POC 1e0fa212-37dc-45f5-bb6f-b60867cacc64b AzureCloud
ResourceGroupName: azure-dc-connect
Location               : eastus
ProvisioningState      : Succeeded
...
Creating domain controller
```

After the DC is provisioned, additional resources, including the client VM and user accounts, are automatically deployed. The on-premises users are later synchronized to Azure AD.

<Frame>
  ![The image shows a Microsoft Azure portal interface displaying a list of virtual machines, including details like name, type, subscription, location, status, operating system, and IP address.](https://kodekloud.com/kk-media/image/upload/v1752881902/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Azure-AD-Connect-Demonstration/azure-portal-virtual-machines-list.jpg)
</Frame>

## Deploying and Logging Into the Domain Controller

Once the deployment completes, navigate to the virtual machine named "dc-01" in the Azure portal and copy its public IP address for Remote Desktop (RDP) access. The username and password details are provided at the top of the `prep-dc.ps1` module.

<Frame>
  ![The image shows a Microsoft Azure portal interface with a virtual machine named "dc-01" selected, displaying its details and a Windows Security prompt for entering credentials.](https://kodekloud.com/kk-media/image/upload/v1752881903/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Azure-AD-Connect-Demonstration/azure-portal-virtual-machine-dc-01.jpg)
</Frame>

Below is an example snippet used in the domain controller configuration script:

```powershell theme={null}
Write-Host "Azure AD Connect Demo - v1.0, written by Rithin Skaria" `
    -ForegroundColor "Red" -BackgroundColor "White"
