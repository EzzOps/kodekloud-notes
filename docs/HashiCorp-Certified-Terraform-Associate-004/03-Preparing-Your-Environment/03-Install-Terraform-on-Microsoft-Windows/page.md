# From your Downloads folder (adjust paths as needed)
cd ~/Downloads
unzip terraform_1.2.2_darwin_arm64.zip

# Move the binary to a directory in your PATH (use sudo if required)
sudo mv terraform /usr/local/bin/terraform
sudo chmod +x /usr/local/bin/terraform

# Verify installation
terraform version
which terraform
echo $PATH
```

When selecting the correct ZIP on the downloads page, pick the build that matches your CPU and OS: `darwin_amd64`, `darwin_arm64`, `linux_amd64`, `linux_arm64`, etc.

<Frame>
  <img alt="The image shows a computer screen with the HashiCorp Terraform download page open in a browser, alongside a file explorer window highlighting a &#x22;terraform&#x22; executable file and a &#x22;LICENSE.txt&#x22; file." />
</Frame>

Expected example output after a correct manual install:

```bash theme={null}
$ terraform version
Terraform v1.2.2
on darwin_arm64

$ which terraform
/usr/local/bin/terraform
```

> **warning** If `terraform` is not found after copying the binary, confirm the target directory is in your `PATH` (`echo $PATH`) and that the binary is executable (`chmod +x terraform`). Use `which terraform` to locate the active binary. When in doubt, remove older copies or adjust your `PATH` to prioritize the intended installation.

## 3) Linux — Debian / Ubuntu (apt)

HashiCorp maintains an apt repository for Debian/Ubuntu. To add the GPG key, register the repository, and install Terraform:

```bash theme={null}
# Add HashiCorp GPG key to a keyring
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg >/dev/null

# Add the repository (replace $(lsb_release -cs) with your distro codename if needed)
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

# Update and install terraform
sudo apt update && sudo apt install -y terraform
```

This installs the latest Terraform available in the HashiCorp apt repository. If you need a specific release version not available in the repo, use the manual ZIP install (see section 2).

## 4) Linux — RHEL / CentOS / Amazon Linux (yum / dnf)

For RPM-based distributions, enable the HashiCorp RPM repository and install via `yum` or `dnf`:

```bash theme={null}
# Add repo and install terraform
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum install -y terraform
```

If your distro uses `dnf`, replace `yum` with `dnf`. This approach installs the latest package available in HashiCorp's RPM repository.

## 5) Using releases.hashicorp.com for automation

For scripted installs in CI/CD or automated provisioning, prefer the releases listing to fetch exact ZIP URLs directly (no interactive UI). Example release listing for a version like 1.2.2:

```text theme={null}
terraform_1.2.2_SHA256SUMS
terraform_1.2.2_darwin_amd64.zip
terraform_1.2.2_darwin_arm64.zip
terraform_1.2.2_linux_386.zip
terraform_1.2.2_linux_amd64.zip
terraform_1.2.2_linux_arm.zip
terraform_1.2.2_linux_arm64.zip
...
```

Script approach (example pattern):

1. Download the chosen ZIP from `https://releases.hashicorp.com/terraform/<version>/terraform_<version>_<platform>.zip`
2. Unzip, move binary into a `PATH` directory, and set executable permissions.

This approach ensures reproducible installs across build agents and containers.

## Quick troubleshooting

* `command not found` after copying the binary:
  * Confirm the install directory is in your `PATH` (`echo $PATH`).
  * Confirm the binary is executable: `chmod +x /path/to/terraform`.
* Multiple Terraform versions:
  * `which terraform` shows which binary will be executed. Remove or reorder binaries to control which version is active.
* Permission errors:
  * Use `sudo` when moving or writing to system `bin` directories, or install to a user-writable directory and add it to your `PATH`.

Useful links and references:

* HashiCorp Terraform downloads: [https://developer.hashicorp.com/terraform/downloads](https://developer.hashicorp.com/terraform/downloads)
* Releases mirror: [https://releases.hashicorp.com/terraform](https://releases.hashicorp.com/terraform)
* Terraform documentation: [https://developer.hashicorp.com/terraform/docs](https://developer.hashicorp.com/terraform/docs)

Go get Terraform downloaded — for the [HashiCorp Certified: Terraform Associate 004](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-certification) exam, download and use 1.2.x if you want to practice on the same major/minor release used by the exam.

In the next lesson/article I'll show you...

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/df5b5815-c1ea-45f5-ba18-7a5c53ded28a/lesson/c5c8bb8b-29c1-4b7f-b310-2c7b38af8182)


# Install Terraform on Microsoft Windows

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Preparing-Your-Environment/Install-Terraform-on-Microsoft-Windows/page

Instructions to install and verify Terraform on Windows, covering manual binary placement in PATH and package manager options WinGet and Chocolatey with examples and troubleshooting tips

This guide shows how to install Terraform on a Windows machine. It covers the manual binary method and two package-manager approaches (WinGet and Chocolatey). Links and examples for other platforms (macOS/Homebrew and Debian/apt) are included for context but are not required on Windows.

Why this matters: installing Terraform correctly ensures the `terraform` CLI is available from any command prompt or PowerShell session and lets you manage infrastructure with consistent tooling.

## Other-platform examples (for context)

* Homebrew (macOS) example:

```bash theme={null}
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

* Debian/Ubuntu (apt) example:

```bash theme={null}
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

## Manual Windows download and installation

1. Visit the Terraform install page: [https://developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install) and download the Windows AMD64 binary (`terraform.exe`).
2. Move the downloaded `terraform.exe` to a permanent folder, for example `C:\Terraform`.

<Frame>
  <img alt="The image shows a download page for Terraform from HashiCorp, specifically highlighting binary download options for Windows and Linux operating systems. A user is selecting the AMD64 version for Windows." />
</Frame>

## Add the folder to the system PATH

Make the `terraform.exe` executable available from any shell by adding its folder to `PATH`:

* Right-click Start → System → Advanced system settings → Environment Variables.
* Under System variables, select `Path` → Edit → New and add `C:\Terraform`.
* Click OK to close all dialogs.

> **warning** When editing system environment variables, be careful not to modify or delete other existing `Path` entries. Incorrect changes can affect other programs.

<Frame>
  <img alt="The image shows a Windows environment variables window, listing different system paths, overlaid on a system properties panel." />
</Frame>

If you keep several HashiCorp tools together, you might prefer a folder like `C:\HashiCorp` containing multiple executables (for example `consul.exe`, `vault.exe`, etc.). The key is that the folder containing `terraform.exe` is included in `PATH`.

<Frame>
  <img alt="The image shows a Windows File Explorer window open to a folder named &#x22;hashicorp&#x22; on the local disk (C:), containing several executable files with names like &#x22;consul.exe&#x22; and &#x22;vault.exe&#x22;." />
</Frame>

After adding the folder to `PATH` and reopening PowerShell, confirm the binary is in place (example view in File Explorer):

<Frame>
  <img alt="The image shows a Windows File Explorer window displaying the contents of a folder named &#x22;terraform&#x22; on the C: drive. It contains a single file named &#x22;terraform.exe&#x22; with details such as date modified, type, and size." />
</Frame>

## Verify the manual installation

Open a new PowerShell window and run:

```powershell theme={null}
PS C:\Users\btkra> terraform version
Terraform v1.12.2
on windows_amd64

Your version of Terraform is out of date! The latest version
is 1.14.3. You can update by downloading from https://developer.hashicorp.com/terraform/install
PS C:\Users\btkra>
```

If `terraform.exe` is removed from the folder on `PATH`, the `terraform` command will no longer be recognized.

## Install using WinGet (recommended for modern Windows)

WinGet provides a simple one-line installation and straightforward uninstallation.

Install Terraform:

```powershell theme={null}
winget install --id HashiCorp.Terraform
```

After installation, you may need to close and reopen PowerShell to pick up PATH changes. Then verify:

```powershell theme={null}
PS C:\Users\btkra> terraform version
Terraform v1.12.12
on windows_amd64
...
PS C:\Users\btkra>
```

Uninstall with WinGet:

```powershell theme={null}
winget uninstall --id HashiCorp.Terraform -e
```

After uninstalling, running `terraform version` will return an error like:

```powershell theme={null}
PS C:\Users\btkra> terraform version
terraform : The term 'terraform' is not recognized as the name of a cmdlet,
function, script file, or operable program. Check the spelling of the name, or
if a path was included, verify that the path is correct and try again.
```

## Chocolatey alternative

If you use Chocolatey, install Terraform with:

```powershell theme={null}
choco install terraform -y --version=1.12.2
```

Omit `--version` to install the latest available package, or change it to pin a specific version.

## Quick reference: installation methods

| Method                  | Command                                                             | Notes                                                   |
| ----------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- |
| Manual binary           | Download `terraform.exe` from HashiCorp and place in `C:\Terraform` | Add `C:\Terraform` to system `Path`                     |
| WinGet (recommended)    | `winget install --id HashiCorp.Terraform`                           | Simple install/uninstall; may require restarting shells |
| Chocolatey              | `choco install terraform -y`                                        | Useful if you already manage packages with Chocolatey   |
| macOS (context)         | `brew tap hashicorp/tap && brew install hashicorp/tap/terraform`    | Homebrew example (not for Windows)                      |
| Debian/Ubuntu (context) | See apt example above                                               | apt example (not for Windows)                           |

> **lightbulb** After changing the system `PATH` or installing via a package manager, restart any open PowerShell or command prompt windows so they pick up the updated `PATH`.

## Summary

* Manual method: download `terraform.exe`, put it in `C:\Terraform`, and add that folder to `PATH`.
* Recommended: use `winget install --id HashiCorp.Terraform` for a one-line install and easier uninstallation.
* Verify your install with `terraform version`.
* Optionally use Chocolatey if it fits your workflow.

## Links and references

* HashiCorp Terraform installation: [https://developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install)
* Visual Studio Code (recommended editor for Terraform): [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download)
* WinGet documentation: [https://learn.microsoft.com/windows/package-manager/winget/](https://learn.microsoft.com/windows/package-manager/winget/)
* Chocolatey: [https://chocolatey.org/](https://chocolatey.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/df5b5815-c1ea-45f5-ba18-7a5c53ded28a/lesson/9e4e4804-ab3b-4705-b806-309ffec63ab9)
