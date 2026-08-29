# Installing Terraform

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Setting-up-environment/Installing-Terraform/page

Guide for installing and verifying Terraform locally and via Azure Cloud Shell across Windows macOS and Linux

This guide shows multiple ways to install Terraform so you can run infrastructure-as-code across different platforms. It covers local installations for Windows, macOS, and Linux, plus an option to use Terraform from Azure Cloud Shell. Follow the steps that best match your workflow and operating system.

Installing Terraform locally is a straightforward three-step process:

1. Download the Terraform binary (or install via a package manager) for your operating system.
2. Ensure Terraform is available on your system `PATH`.
3. Verify the installation.

<Frame>
  <img alt="The image outlines the steps for installing Terraform locally, including downloading the Terraform binary, installing and configuring the PATH, and verifying the installation." />
</Frame>

Installation quick reference

| Platform        |         Recommended method | Example / Notes                                                                   |
| --------------- | -------------------------: | --------------------------------------------------------------------------------- |
| Windows         | Official MSI or Chocolatey | `choco install terraform -y` (places `terraform.exe` on `PATH`)                   |
| macOS           |   Homebrew (HashiCorp tap) | `brew tap hashicorp/tap` then `brew install hashicorp/tap/terraform`              |
| Debian / Ubuntu |   HashiCorp APT repository | Add GPG key & repo, then `sudo apt-get install -y terraform` (see commands below) |
| Any OS          |                 Zip binary | Download ZIP, extract `terraform`/`terraform.exe` and place it on `PATH`          |

Windows

* Easiest approaches:
  * Download and run the official MSI from HashiCorp: [https://developer.hashicorp.com/terraform/downloads](https://developer.hashicorp.com/terraform/downloads) (this places `terraform.exe` on the system `PATH`).
  * Use Chocolatey for automated installs and updates.

Example (Chocolatey):

```bash theme={null}
choco install terraform -y
```

If you downloaded the portable ZIP, extract `terraform.exe` and move it into a directory on the system `PATH` (for example `C:\Program Files\Terraform`), or add the directory to the system `PATH`.

macOS

* Recommended: Homebrew with the HashiCorp tap. This handles installation and updates for you.

```bash theme={null}
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

Alternatively, download the correct binary for Intel or Apple Silicon from the official Terraform releases page and place the `terraform` binary in a directory on your `PATH` (for example `/usr/local/bin`).

Linux (Debian / Ubuntu example)

* Use the official HashiCorp APT repository to get signed packages and automatic updates. Run these commands:

```bash theme={null}
