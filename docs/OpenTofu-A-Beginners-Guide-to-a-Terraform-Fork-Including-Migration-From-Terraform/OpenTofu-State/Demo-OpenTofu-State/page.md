# Demo OpenTofu State

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-State/Demo-OpenTofu-State/page

This lesson covers OpenTofu state management, including state file locations, resource tracking, default filenames, and working with local and AWS resources.

Welcome to this lesson on OpenTofu state management. In this guide, we’ll cover where the state file lives, how OpenTofu tracks resources, default filenames, inspecting state, and working with both local and AWS resources.

## Default State File Location

After you provision resources with OpenTofu, the state file is created in your current working directory by default.

<Frame>
  ![The image shows a KodeKloud OpenTofu Lab interface with a task question on the left and a Visual Studio Code editor on the right, displaying a welcome message and terminal.](https://kodekloud.com/kk-media/image/upload/v1752882885/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-OpenTofu-State/kodekloud-opentofu-lab-vscode-editor.jpg)
</Frame>

## Disabling State

OpenTofu always relies on a state file to track existing resources. There is no option to disable this behavior.

<Callout icon="triangle-alert">
  OpenTofu **always** maintains a local state file (`terraform.tfstate`). You cannot disable state management.
</Callout>

<Frame>
  ![The image shows a Visual Studio Code editor with a welcome message for KodeKloud OpenTofu Lab on the right, and a task question about disabling state on the left.](https://kodekloud.com/kk-media/image/upload/v1752882886/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-OpenTofu-State/vscode-kodekloud-opentofu-lab-task.jpg)
</Frame>

## State File Format

Open the `terraform.tfstate` file and you’ll see it’s formatted in JSON.

<Callout icon="lightbulb">
  The JSON format makes it easy to parse the state file with tools like `jq` or programmatic scripts.
</Callout>

<Frame>
  ![The image shows a Visual Studio Code editor with a welcome message for the KodeKloud OpenTofu Lab on the right, and a multiple-choice question about file formats on the left.](https://kodekloud.com/kk-media/image/upload/v1752882888/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-OpenTofu-State/vscode-kodekloud-opentofu-lab-question.jpg)
</Frame>

## Commands and State Refresh

Some OpenTofu commands automatically refresh the state to match real-world resources:

| Command          | Refreshes State? | Description                           |
| ---------------- | ---------------- | ------------------------------------- |
| `opentofu plan`  | Yes              | Generates and shows an execution plan |
| `opentofu apply` | Yes              | Applies changes and refreshes state   |
| `opentofu init`  | No               | Initializes the working directory     |

<Frame>
  ![The image shows a Visual Studio Code editor with a welcome message for KodeKloud OpenTofu Lab on the right, and a multiple-choice question about command usage on the left.](https://kodekloud.com/kk-media/image/upload/v1752882889/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-OpenTofu-State/vscode-kodekloud-opentofu-lab-question-2.jpg)
</Frame>

## Default State File Name

By default, the state file created is:

```plaintext theme={null}
terraform.tfstate
```

<Frame>
  ![The image shows a Visual Studio Code interface with a welcome message for KodeKloud OpenTofu Lab on the right and a multiple-choice question about a Terraform state file on the left.](https://kodekloud.com/kk-media/image/upload/v1752882890/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-OpenTofu-State/vscode-kodekloud-opentofu-lab-question-3.jpg)
</Frame>

***

## Working with State in a Configuration

Navigate into your configuration directory:

```bash theme={null}
cd /root/OpenTofu-project/project
```

You’ve already run `opentofu init`, so the `.terraform` folder exists—but no `terraform.tfstate` file yet, since `opentofu apply` hasn’t been executed.

### 1. Showing the State

```bash theme={null}
opentofu show
```

No output appears because no state file exists yet.

### 2. Applying the Configuration

Run:

```bash theme={null}
opentofu apply
```

When prompted, type `yes`. Sample output:

```plaintext theme={null}
local_file.zoom: Creating...
local_file.ridder: Creating...
local_file.reverse-flash: Creating...
local_file.speed_force: Creating...
local_file.zoom: Creation complete after 0s [id=49a99e298eb6c5658742c255584f940948]
local_file.ridder: Creation complete after 0s [[AWS_SECRET_ACCESS_KEY]]
Apply complete! Resources: 4 added, 0 changed, 0 destroyed.
```

### 3. Inspecting the New State

Now re-run:

```bash theme={null}
opentofu show
```

Search for the resource `local_file.speed_force`. In HCL form, it appears as:

```hcl theme={null}
