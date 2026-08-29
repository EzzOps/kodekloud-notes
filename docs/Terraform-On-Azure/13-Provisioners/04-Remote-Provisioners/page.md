# Remote Provisioners

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Provisioners/Remote-Provisioners/page

Guide to using Terraform remote-exec provisioner to run commands on newly created VMs via SSH or WinRM, including an Azure Apache example, requirements, and troubleshooting.

This lesson covers remote provisioners in Terraform and how to use the `remote-exec` provisioner to run commands inside newly created virtual machines. Remote provisioners let Terraform connect to a VM over the network and execute commands inside the guest operating system — for Linux VMs Terraform typically uses SSH, and for Windows VMs it uses WinRM. This is distinct from configuring a VM through cloud-provider APIs; remote provisioners log into the machine and run commands directly.

<Frame>
  <img alt="The image is an infographic explaining remote provisioning (remote-exec) methods for virtual machines, showing Linux VMs using SSH and Windows VMs using WinRM." />
</Frame>

## Typical use cases

Remote provisioners are best for targeted, small-scale bootstrapping tasks that should run immediately after a VM is created:

* Install software right after deployment (e.g., Nginx, Docker, or other runtime dependencies).
* Run initialization or bootstrap scripts to prepare the system before apps are deployed.
* Apply small configuration tweaks after infrastructure creation (e.g., enable a service, update a config file, restart a daemon).

Remote provisioners are useful for quick post-deployment steps when you do not want to introduce a full configuration-management system (Ansible, Chef, Puppet) for minor tasks. They are not designed to replace configuration management for long-term, complex configuration.

<Frame>
  <img alt="The image lists three use cases: installing software (with logos for NGINX and Docker), running initialization scripts (with PowerShell logos), and applying configuration tweaks post-deployment." />
</Frame>

## Requirements and constraints

Before using remote provisioners ensure the following:

| Requirement            | Details                                                                                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Network reachability   | The machine running `terraform apply` must be able to reach the VM over the appropriate port (SSH: `22` for Linux; WinRM: `5985` HTTP or `5986` HTTPS for Windows). |
| Authentication         | Valid credentials are required: SSH username + private key (preferred) or password, or WinRM credentials for Windows.                                               |
| Reachable endpoint     | The VM needs a reachable public IP or a hostname accessible via VPN/peering.                                                                                        |
| Security groups / NSGs | In cloud environments ensure security rules allow the required inbound traffic; otherwise the provisioner will fail.                                                |

<Frame>
  <img alt="The image displays a list of requirements for network access, including the need for a specific port for SSH, a correct username and private key, and a public IP or reachable hostname." />
</Frame>

> **lightbulb** Prefer SSH key-based authentication for Linux VMs and avoid embedding plaintext secrets in your Terraform files. Use an absolute path or pass keys via variables (Terraform does not expand `~` in `file()` calls).

## Example: remote-exec to install Apache (apache2)

This concise example shows a core Terraform configuration that creates a Linux VM on Azure and uses a `remote-exec` provisioner to update packages, install Apache, and write a simple index page.

Notes on the example:

* Add the `provisioner "remote-exec"` block inside the VM resource.
* Use the `connection` block to tell Terraform how to reach the VM (SSH for Linux).
* Prefer SSH key authentication. Never store production secrets inline.

main.tf (core resources and provisioner)

```hcl theme={null}
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = var.rg
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "subnet" {
  name                 = var.subnet
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_security_group" "nsg" {
  name                = var.nsg
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "nsg_snet" {
  subnet_id                 = azurerm_subnet.subnet.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

resource "azurerm_public_ip" "pip" {
  name                = var.pip
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
}

resource "azurerm_network_interface" "nic" {
  name                = var.nic
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.pip.id
  }
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                = var.vm
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_B1s"

  admin_username = "azureuser"

  # Choose one of these authentication methods.
  # Method A: SSH key (recommended)
  admin_ssh_key {
    username   = "azureuser"
    # Note: Terraform's file() does not expand '~'. Use an absolute path or a variable for portability.
    public_key = file("~/.ssh/id_rsa.pub")
  }

  # Method B: Password (not recommended for production)
  # admin_password = "YourStrongPasswordHere"

  source_image_reference {
    publisher = "Canonical"
    offer     = "ubuntu-25_04"
    sku       = "server"
    version   = "latest"
  }

  network_interface_ids = [azurerm_network_interface.nic.id]

  # Remote provisioner that runs after the VM is created
  provisioner "remote-exec" {
    inline = [
      "sudo apt update -y",
      "sudo apt install apache2 -y",
      "echo '<h1>Welcome to Azure VM</h1>' | sudo tee /var/www/html/index.html"
    ]

    connection {
      type        = "ssh"
      host        = azurerm_public_ip.pip.ip_address
      user        = "azureuser"
      # Note: Terraform's file() does not expand '~'. Use an absolute path or a variable for the private key.
      private_key = file("~/.ssh/id_rsa")
      # Alternatively, if using password authentication:
      # password = var.vm_password
    }
  }
}

output "vm_public_ip" {
  value = azurerm_public_ip.pip.ip_address
}
```

variables.tf

```hcl theme={null}
variable "rg" {}
variable "location" {}
variable "vnet" {}
variable "subnet" {}
variable "nsg" {}
variable "pip" {}
variable "nic" {}
variable "vm" {}
