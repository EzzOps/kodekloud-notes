# Type "yes" at the prompt
```

Confirm the state file:

```bash theme={null}
ls -l
# terraform.tfstate  main.tf  variables.tf
```

***

## 2. Inspect the Local State Output

After `apply`, view the generated file:

```bash theme={null}
cat /root/local
# This configuration uses local state
```

***

## 3. Set Up MinIO and Identify the Bucket

We’ll use [MinIO](https://min.io/) as our S3-compatible object store. In your browser’s MinIO console, log in with:

* **Access Key**: `foo`
* **Secret Key**: `barbarbar`

Locate the `remote-state` bucket under **Object Browser**.

***

## 4. Switch to the Remote State Variable

Edit `main.tf` to use `var.remote_state`:

```hcl theme={null}
resource "local_file" "state" {
  filename = "/root/${var.remote_state}"
  content  = "This configuration uses ${var.remote_state} state"
}
```

Re-plan and apply:

```bash theme={null}
tofu plan
tofu apply
# confirm with "yes"
```

This destroys `/root/local` and creates `/root/remote`.

***

## 5. Configure the S3 Backend

Create `terraform.tf` with the S3 backend block:

```hcl theme={null}
terraform {
  backend "s3" {
    bucket = "remote-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
```

<Callout icon="lightbulb">
  When using MinIO, add these settings under the `s3` backend:

  ```text theme={null}
  endpoint   = "http://<MINIO_HOST>:<PORT>"
  access_key = "foo"
  secret_key = "barbarbar"
  ```
</Callout>

**Do not** run `tofu init` yet.

***

## 6. Initialize the Backend and Migrate State

If you try to apply, you’ll see:

```plaintext theme={null}
Error: Backend initialization required, please run "tofu init"
```

Run:

```bash theme={null}
tofu init
```

You’ll be prompted:

```plaintext theme={null}
Pre-existing state was found while migrating the previous "local" backend
to the newly configured "s3" backend.
Do you want to copy this state to the new "s3" backend? Enter "yes" to copy...
Enter a value: yes
```

After migration, remove the local state:

```bash theme={null}
rm terraform.tfstate
```

<Callout icon="triangle-alert">
  Deleting the local `terraform.tfstate` is irreversible. Ensure the remote copy is present before removal.
</Callout>

***

## 7. Verify Remote State in MinIO

Go back to the MinIO console and open the `remote-state` bucket. You should see `terraform.tfstate` uploaded—confirming your remote backend is working.

<Frame>
  ![The image shows a user interface of an object storage system with a bucket named "remote-state," displaying its creation date, usage, and access permissions. The sidebar includes options like Object Browser, Access Keys, and various administrative tools.](https://kodekloud.com/kk-media/image/upload/v1752882893/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-Remote-State/object-storage-user-interface-remote-state.jpg)
</Frame>

***

## Links and References

* [OpenTofu Documentation](https://docs.opentofu.org/)
* [Terraform Remote State](https://developer.hashicorp.com/terraform/language/state/remote)
* [MinIO Quickstart Guide](https://docs.min.io/docs/minio-quickstart-guide.html)
* [AWS S3 Documentation](https://aws.amazon.com/s3/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/dd54768d-8454-44bd-bab2-99f8f7b5f145/lesson/ff1df9b3-f33a-4bd0-a830-9b3fba34a27d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/dd54768d-8454-44bd-bab2-99f8f7b5f145/lesson/43c8ff37-5548-4482-9fd7-35f6d4d78e85" />
</CardGroup>


# OpenTofu State Commands

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Remote-State/OpenTofu-State-Commands/page

This article explains how to manage the OpenTofu state file using various commands for safe resource handling.

Managing the OpenTofu state file directly is error-prone. Instead, use the `tofu state` subcommands to list, inspect, rename, pull, remove, and push resources safely.

| Command      | Description                                            |
| ------------ | ------------------------------------------------------ |
| `state show` | Display detailed attributes of a resource in state     |
| `state list` | List all resource addresses or filter by pattern       |
| `state mv`   | Rename or move resources within or between state files |
| `state pull` | Download remote state to your local machine            |
| `state rm`   | Remove a resource from the state without destroying it |
| `state push` | Overwrite remote state with a local state file         |

## Viewing Resource Attributes with `state show`

To inspect resource attributes in the state file:

```bash theme={null}
tofu state show aws_s3_bucket.finance
```

Example (truncated):

```json theme={null}
{
  "mode": "managed",
  "type": "aws_s3_bucket",
  "name": "finance",
  "provider": "provider[\"registry.opentofu.org/hashicorp/aws\"]",
  "instances": [
    {
      "attributes": {
        "bucket": "finance",
        "arn": "arn:aws:s3:::finance",
        "region": "us-west-2",
        "tags": {
          "Environment": "Production"
        },
        "versioning": [
          {
            "enabled": false,
            "mfa_delete": false
          }
        ]
      }
    }
  ]
}
```

## Listing Resources with `state list`

Show all resource addresses in your state:

```bash theme={null}
tofu state list
```

Sample output:

```text theme={null}
aws_dynamodb_table.cars
aws_s3_bucket.finance-2020922
```

Filter by a resource pattern:

```bash theme={null}
tofu state list aws_s3_bucket.cerberus-finance
