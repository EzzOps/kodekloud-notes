# Demo OpenTofu State Commands

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Remote-State/Demo-OpenTofu-State-Commands/page

Master OpenTofu state commands to manage your Terraform state file effectively.

In this step-by-step guide, you’ll master OpenTofu state commands to manage your Terraform state file. We’ll cover how to:

* List resources in state
* Inspect resource attributes
* Retrieve specific IDs
* Remove resources from state
* Work with a remote S3 backend
* Rename resources in both configuration and state

***

## Table of State Commands

| Command           | Description                                  |
| ----------------- | -------------------------------------------- |
| `tofu state list` | List all resources tracked in the state file |
| `tofu state show` | Display all attributes for a resource        |
| `tofu state rm`   | Remove one or more resources from state      |
| `tofu state mv`   | Rename a resource in the state               |

***

## 1. Inspecting State Resource Names

First, navigate to your project directory and list the tracked resources:

```bash theme={null}
cd ~/opentofu-projects/project-anime/
tofu state list
```

You should see output similar to:

```bash theme={null}
local_file.classics
local_file.hall_of_fame
local_file.new_shows
local_file.top10
```

These correspond to the resource blocks in `main.tf`:

```hcl theme={null}
resource "local_file" "top10" {
  filename = "/root/anime/top10.txt"
  content  = "1. Naruto\n2. DragonBallZ\n3. Death Note\n"
}

resource "local_file" "hall_of_fame" {
  filename = "/root/anime/hall-of-fame.txt"
  content  = "1. Attack On Titan\n2. Naruto\n3. Bleach\n"
}

resource "local_file" "new_shows" {
  filename = "/root/anime/new_shows.txt"
  content  = "1. Cannon Busters\n2. Last Hope\n3. Lost Song\n"
}

resource "local_file" "classics" {
  filename = "/root/anime/classic_shows.txt"
  content  = "1. DragonBall\n"
}
```

Any resource not listed (e.g., `super_pets`) is not managed in the current state.

***

## 2. Showing Resource Attributes

To view every attribute stored for a single resource, run:

```bash theme={null}
tofu state show local_file.classics
```

Example output:

```bash theme={null}
