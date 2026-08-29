# Install Terraform on MacOS and Linux

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Preparing-Your-Environment/Install-Terraform-on-MacOS-and-Linux/page

Installing Terraform on macOS and Linux using Homebrew, package managers, manual binaries, and automated scripts, with troubleshooting and exam version guidance

In this lesson/article you will learn how to install Terraform on macOS and Linux. Recommended installation options covered here:

* macOS — Homebrew (recommended)
* Manual install — download a specific Terraform binary
* Linux — Debian/Ubuntu (apt)
* Linux — RHEL/CentOS/Amazon Linux (yum/dnf)
* Automation-friendly installs using `releases.hashicorp.com`

> **lightbulb** If you are preparing for the [HashiCorp Certified: Terraform Associate 004](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-certification) exam, practice with Terraform 1.2 since the exam content focuses on that version. You do not always need the latest version for learning or exam prep.

Quick comparison of installation methods:

| Method                             | Best for                                | Notes / Link                                                           |
| ---------------------------------- | --------------------------------------- | ---------------------------------------------------------------------- |
| Homebrew (macOS)                   | macOS users who want a packaged install | Uses HashiCorp Homebrew tap                                            |
| Manual (ZIP)                       | Pinning an exact Terraform version      | Use `releases.hashicorp.com` or HashiCorp downloads page               |
| apt (Debian/Ubuntu)                | APT-based Linux distributions           | Adds HashiCorp apt repository and GPG key                              |
| yum/dnf (RHEL/CentOS/Amazon Linux) | RPM-based Linux distributions           | Add HashiCorp RPM repo and install with `yum` or `dnf`                 |
| Automated scripts / CI             | Non-interactive installs                | Download specific zip from `releases.hashicorp.com` and install binary |

## 1) macOS — Homebrew (recommended)

If you use macOS and have Homebrew installed, use the HashiCorp Homebrew tap for the simplest install:

```bash theme={null}
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

This installs the latest Terraform from the tap. If you require a specific version (for example, Terraform 1.2.x) for exam practice, use the manual download instructions below to get the exact binary for your CPU/OS (darwin\_amd64 or darwin\_arm64).

<Frame>
  <img alt="The image shows a webpage from HashiCorp’s site displaying download options for Terraform, with separate sections for different operating systems like macOS and Windows." />
</Frame>

Notes for Homebrew + Apple Silicon:

* Homebrew installs to `/opt/homebrew/bin` on Apple Silicon and to `/usr/local/bin` on Intel macOS. Ensure the Homebrew `bin` path is in your `PATH`.

## 2) Download a specific Terraform version (manual install)

To pin a precise release (recommended for predictable exam/CI environments), download the platform-specific ZIP for the release you need from:

* HashiCorp downloads page: [https://developer.hashicorp.com/terraform/downloads](https://developer.hashicorp.com/terraform/downloads)
* Releases mirror: [https://releases.hashicorp.com/terraform](https://releases.hashicorp.com/terraform)

After downloading the ZIP (it contains a single `terraform` executable):

1. Unzip the archive.
2. Move the `terraform` binary into a directory that appears in your `PATH` (example: `/usr/local/bin` or `/opt/homebrew/bin`).
3. Make it executable (`chmod +x` if necessary).
4. Verify the installation.

Example commands (macOS or Linux):

```bash theme={null}
