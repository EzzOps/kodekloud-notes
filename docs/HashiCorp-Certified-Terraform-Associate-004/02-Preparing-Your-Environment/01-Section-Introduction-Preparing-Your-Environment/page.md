# Section Introduction Preparing Your Environment

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Preparing-Your-Environment/Section-Introduction-Preparing-Your-Environment/page

Guide to install and verify Terraform, configure VS Code, set cloud provider credentials for AWS Azure GitHub, and run basic Terraform workflow commands

Welcome to this lesson on preparing your local machine to run Terraform. This guide walks you through the minimal, practical steps required to get a working Terraform environment for exercises and labs, with verification commands so you can confirm each step completed successfully.

What you'll get from this lesson

* Clear installation options for Terraform across macOS, Linux, and Windows
* Recommended code editor setup (Visual Studio Code) and useful extensions
* How to configure cloud provider credentials (AWS, Azure, GitHub) so Terraform can authenticate securely
* A short checklist of basic Terraform workflow commands to validate your environment

## Installing Terraform

You can install Terraform either via your platform's package manager or by downloading the official binary from HashiCorp: [https://developer.hashicorp.com/terraform/downloads](https://developer.hashicorp.com/terraform/downloads).

Use the method that suits your environment (package managers keep Terraform up to date; manual downloads give you more control).

Package-manager examples

| Platform               | Recommended approach                          | Example command / notes                                    |
| ---------------------- | --------------------------------------------- | ---------------------------------------------------------- |
| macOS                  | Homebrew                                      | `brew install terraform`                                   |
| Ubuntu / Debian        | HashiCorp apt repository or manual binary     | Follow HashiCorp's repo instructions to enable apt updates |
| RHEL / CentOS / Fedora | HashiCorp yum/dnf repository or manual binary | Configure HashiCorp yum/dnf repo for updates               |
| Windows                | Chocolatey or official MSI/zip                | `choco install terraform` or download MSI from HashiCorp   |

After installation, verify Terraform is available:

```bash theme={null}
