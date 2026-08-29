# Demo Migrating existing Terraform configuration to OpenTofu

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Beyond-Basics/Demo-Migrating-existing-Terraform-configuration-to-OpenTofu/page

This guide explains how to migrate a Terraform project to OpenTofu, verify changes, and roll back to Terraform.

In this guide, you’ll learn how to migrate an existing Terraform project to OpenTofu, verify the changes, and then roll back to Terraform. We’ll cover:

* Applying the initial Terraform configuration
* Installing OpenTofu
* Backing up state files
* Initializing and planning with OpenTofu
* Updating resources and applying changes
* Rolling back to Terraform

***

## 1. Apply the Initial Terraform Configuration

1. Navigate to your project directory and review **main.tf**:

   ```hcl theme={null}
   resource "local_file" "file" {
     filename = "terraform.txt"
     content  = "This file has been created with Terraform"
   }
   ```

2. Initialize and apply:

   ```bash theme={null}
   cd ~/opentofu-projects/migration
   terraform init
   terraform apply
   ```

3. When prompted, enter `yes`. You should see:

   ```plaintext theme={null}
   local_file.file: Creating...
   local_file.file: Creation complete after 0s [id=342bd3c96f4da9100a6360378942400b96bfb5]
   Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
   ```

4. Verify that **terraform.txt** exists with the correct content.

***

## 2. Install OpenTofu

Refer to the [OpenTofu installation guide](https://docs.opentofu.org/intro/getting-started/#installation) and select the installer for your OS.

<Callout icon="lightbulb">
  Make sure to check your distribution using `cat /etc/os-release` before running the installer.
</Callout>

<Frame>
  ![The image shows a webpage for installing OpenTofu, detailing various installation methods for different operating systems like Alpine Linux, Debian, Fedora, and more. The page includes a navigation menu on the left and installation options in the main section.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882836/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-Migrating-existing-Terraform-configuration-to-OpenTofu/opentofu-installation-methods-webpage.jpg)
</Frame>

### Automated Debian/Ubuntu Installer

```bash theme={null}
curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh
chmod +x install-opentofu.sh
./install-opentofu.sh --install-method deb
rm install-opentofu.sh
```

Or bundle the commands in **install.sh**:

```bash theme={null}
#!/bin/bash
curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh
chmod +x install-opentofu.sh
./install-opentofu.sh --install-method deb
rm install-opentofu.sh
```

Then run:

```bash theme={null}
chmod +x install.sh
./install.sh
```

Verify the installation:

```bash theme={null}
tofu version
```

***

## 3. Backup the Terraform State

<Callout icon="triangle-alert">
  Always archive your existing Terraform state before migrating. Losing state can lead to resource drift or duplicates.
</Callout>

```bash theme={null}
tar czf terraform.tfstate.tar.gz terraform.tfstate
```

Confirm the archive:

```bash theme={null}
ls
