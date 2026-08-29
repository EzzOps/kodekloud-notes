# Example commands in sequence
wget https://releases.hashicorp.com/terraform/1.8.3/terraform_1.8.3_linux_amd64.zip
apt update && apt install -y unzip
unzip terraform_1.8.3_linux_amd64.zip
chmod +x terraform && mv terraform /usr/bin/
rm terraform_1.8.3_linux_amd64.zip
terraform version
```

> **lightbulb** ```plaintext theme={null}
  Terraform v1.8.3
  ```

Once you see **Terraform v1.8.3**, return to the lab interface and mark **Question 1** complete.

***

## Question 2: Install Terragrunt 0.58.8 and Verify the Version

Next, install Terragrunt. First, confirm it’s missing:

```bash theme={null}
terragrunt --version
```

Expected result:

```plaintext theme={null}
bash: terragrunt: command not found
```

1. Navigate to the [Terragrunt GitHub releases][2] page and locate **v0.58.8**.
2. Under **Assets**, copy the link for **terragrunt\_linux\_amd64**.

![The image shows a GitHub release page for version 0.58.8 of a software, listing assets for download, including various platform-specific files and source code. The description notes a fix related to S3 bucket URL modifying.](https://kodekloud.com/kk-media/image/upload/v1752884286/notes-assets/images/Terragrunt-for-Beginners-Demo-of-Lab-1/github-release-0-58-8-assets.jpg)

3. Download, make executable, and move it into your PATH:

```bash theme={null}
# Download Terragrunt v0.58.8 for Linux AMD64
wget https://github.com/gruntwork-io/terragrunt/releases/download/v0.58.8/terragrunt_linux_amd64

# Install the binary
chmod +x terragrunt_linux_amd64
mv terragrunt_linux_amd64 /usr/bin/terragrunt

# Verify installation
terragrunt --version
```

> **lightbulb** ```plaintext theme={null}
  terragrunt version v0.58.8
  ```

After confirming **v0.58.8**, return to the lab and proceed to **Question 3**.

***

## Question 3: Beautify Terraform Code with Terragrunt

Terragrunt can wrap and extend Terraform commands. To format all `.tf` files in your directory:

```bash theme={null}
terragrunt fmt
```

This ensures consistent indentation and style across your Terraform modules.

***

## Question 4: Beautify Terragrunt HCL Configuration

To format a Terragrunt HCL file (`.hcl`), use:

```bash theme={null}
terragrunt hclfmt
```

This command tidies up your Terragrunt `*.hcl` configuration, making it easier to read and maintain.

***

Congratulations—**Lab 1** is now complete!

***

## Links and References

* [HashiCorp Terraform releases][1]
* [Terragrunt GitHub releases][2]

[1]: https://releases.hashicorp.com/terraform/

[2]: https://github.com/gruntwork-io/terragrunt/releases

- [Watch Video](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/9618155f-f613-4c7b-92c7-9be9ddfa22b5/lesson/88627ebf-779f-46c0-a0b7-054b1ffa3eef)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/9618155f-f613-4c7b-92c7-9be9ddfa22b5/lesson/687c7569-fd0e-4f75-9c11-b7d4551cacd5)


# Installing Terragrunt

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Basic-Concepts/Installing-Terragrunt/page

Learn how to install Terragrunt on Windows, macOS, and Linux to streamline your Terraform workflows.

Learn how to install Terragrunt on Windows, macOS, and Linux to streamline your Terraform workflows. Follow the steps below to get up and running in minutes.

> **lightbulb** * Ensure you have Terraform installed and configured: [Terraform Documentation](https://www.terraform.io/docs).
  * Verify you have permissions to modify your `PATH` environment variable.
  * For macOS users, Homebrew must be installed: `brew --version`.

## Installation Summary

| Operating System | Method          | Quick Command or Action                                                  |
| ---------------- | --------------- | ------------------------------------------------------------------------ |
| Windows          | Download Binary | Download from GitHub, place `terragrunt.exe` in a directory under `PATH` |
| macOS            | Homebrew        | `brew install terragrunt`                                                |
| Linux            | Download Binary | Download from GitHub, move to `/usr/local/bin`, then `chmod +x`          |

***

## Windows

1. Download the latest `terragrunt.exe` from the [official GitHub releases page][gh-releases].
2. Move the executable into a folder included in your `PATH` (for example, `C:\Windows\System32` or a custom tools directory).
3. Open a new Command Prompt or PowerShell window and verify:

```shell theme={null}
terragrunt --version
```

You should see output similar to:

```text theme={null}
terragrunt version v0.x.x
```

> **triangle-alert** Be careful when editing system environment variables. Incorrect changes to `PATH` can prevent other applications from running.

***

## macOS

On macOS, use Homebrew to install Terragrunt:

```bash theme={null}
brew install terragrunt
```

Once the installation completes, confirm it’s successful:

```shell theme={null}
terragrunt --version
```

If you see the version printed, Terragrunt is ready to use.

***

## Linux

First, download the appropriate binary for your CPU architecture from the [official GitHub releases page][gh-releases].

![The image provides instructions for installing Terragrunt, showing a list of downloadable assets for different operating systems, including Windows, macOS, and Linux. It also includes a link to the GitHub releases page for Terragrunt.](https://kodekloud.com/kk-media/image/upload/v1752884287/notes-assets/images/Terragrunt-for-Beginners-Installing-Terragrunt/terragrunt-installation-instructions-assets.jpg)

Then move the binary into a directory on your `PATH` (e.g., `/usr/local/bin`) and make it executable:

```bash theme={null}
sudo mv terragrunt /usr/local/bin/
sudo chmod +x /usr/local/bin/terragrunt
```

Finally, verify the installation:

```shell theme={null}
terragrunt --version
```

***

With Terragrunt installed on your platform of choice, you can now leverage its features—such as DRY configurations, remote state management, and automated locking—to enhance your Terraform projects.

## Links and References

* [Terragrunt GitHub Releases][gh-releases]
* [Terraform Documentation](https://www.terraform.io/docs)
* [Homebrew](https://brew.sh/)

[gh-releases]: https://github.com/gruntwork-io/terragrunt/releases

- [Watch Video](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/9618155f-f613-4c7b-92c7-9be9ddfa22b5/lesson/f8f916fd-7f10-40df-aada-8f5e7a3cc6f8)
