# local_sensitive_file.name will be created with 3 instances
+ resource "local_sensitive_file" "name" {
    + count    = 3
    + filename = "/root/user-data"
    + content  = (sensitive)
  }
```

Apply the changes:

```bash theme={null}
opentofu apply
```

All three instances target the same filepath, so you end up with just **one** actual file on disk.

> **lightbulb** Although Terraform plans three resources, they all write to `/root/user-data`. Use unique filenames or a loop index to avoid overwriting.

***

## Task 3: Accessing Resources by Index

Resources managed with `count` form a **list**. To view the ID of the second element (index 1):

```bash theme={null}
opentofu state show local_sensitive_file.name[1]
```

Look for the `id` attribute in the output.

***

## Task 4: Parameterize with Variables and `count`

Define variables in `variables.tf`:

```hcl theme={null}
variable "users" {
  type = list(string)
}

variable "content" {
  default = "password: S3Cr3tP@ssw0rd"
}
```

Update `main.tf`:

```hcl theme={null}
resource "local_sensitive_file" "name" {
  count    = length(var.users)
  filename = var.users[count.index]
  content  = var.content
}
```

Now each `users` element becomes a filename. Initialize and apply:

```bash theme={null}
opentofu init
opentofu plan
opentofu apply
```

***

## Task 5: Set Default Values for Variables

Add sensible defaults in `variables.tf`:

```hcl theme={null}
variable "users" {
  type    = list(string)
  default = ["/root/user1", "/root/user11", "/root/user12"]
}

variable "content" {
  default = "password: S3Cr3tP@ssw0rd"
}
```

Key points:

* **Type** of `users`: `list(string)`
* **List vs. set**: Lists allow duplicates; sets do not.

Example of a duplicate in a list (invalid for a set):

```hcl theme={null}
variable "users" {
  default = [
    "/root/user10",
    "/root/user1",
    "/root/user12",
    "/root/user10"  # duplicate
  ]
}
```

***

## Task 6: Ensure Unique Instances with `for_each`

Refactor `main.tf` to use `for_each` on a set:

```hcl theme={null}
resource "local_sensitive_file" "name" {
  for_each = toset(var.users)
  filename = each.value
  content  = var.content
}
```

The `toset()` function removes duplicates, and `for_each` creates a **map** keyed by each unique filename.

Initialize and apply:

```bash theme={null}
opentofu init
opentofu plan
opentofu apply
```

Expected output:

```plaintext theme={null}
local_sensitive_file.name["/root/user10"]: Creating...
local_sensitive_file.name["/root/user11"]: Creating...
local_sensitive_file.name["/root/user12"]: Creating...
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```

> **lightbulb** * Eliminates duplicates automatically
  * Creates a map, so you can reference resources by key:\
    `local_sensitive_file.name["/root/user11"]`

***

## Comparing `count` vs. `for_each`

| Feature             | count                         | for\_each                      |
| ------------------- | ----------------------------- | ------------------------------ |
| Data structure      | List (indexed)                | Map (keyed by value)           |
| Handling duplicates | Requires manual deduplication | Automatic when using `toset()` |
| Reference syntax    | `resource.name[0]`            | `resource.name["key"]`         |

***

## Q\&A

1. **What data structure does `for_each` produce?**\
   A **map**, keyed by each unique element.

2. **How do you address the resource for `/root/user11` with `for_each`?**\
   `local_sensitive_file.name["/root/user11"]`

***

## Further Reading

* [OpenTofu Documentation](https://opentofu.io/docs/)
* [Terraform Meta-Arguments](https://www.terraform.io/language/meta-arguments)
* [Understanding Lists and Sets](https://www.terraform.io/language/types)

That’s a wrap for this lab. Happy automating!

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/5793a08d-f6f5-4739-a570-1038b3ed8619)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/cdab854b-91b9-4e7f-bd0a-f409fa4b1021)


# Demo Data Sources

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Working-with-OpenTofu/Demo-Data-Sources/page

This lesson covers using data sources in OpenTofu to read existing infrastructure or local data without managing new resources.

Welcome to this lesson on using data sources in OpenTofu. Data sources let you read and reference existing infrastructure or local data, without creating or managing new resources.

## Quiz Questions

1. **Can a data source be used to create, update, and destroy infrastructure?**\
   Answer: False. A data source only reads resource data and makes it available in OpenTofu.\
   For more details, see the official [OpenTofu documentation][opentofu-docs].

2. **Can a data source be created using the `data` block?**\
   Answer: True. Data sources are defined with a `data` block, analogous to `resource` blocks.

***

## Hands-On: Local File Data Source

In the directory `/root/OpenTofu/project/lexcorp`, update `main.tf` to:

* Read the contents of `/etc/os-release` via the `local_file` data source.
* Output that content as an OpenTofu output variable.

### Incorrect Configuration

```hcl theme={null}
output "os-version" {
  value = data.local_file.content
}

datasource "local_file" "os" {
  filename = "/etc/os-release"
}
```

> **triangle-alert** 1. The block keyword must be `data`, not `datasource`.
  2. The output reference requires the data source name (`os`).

### Corrected Configuration

```hcl theme={null}
data "local_file" "os" {
  filename = "/etc/os-release"
}

output "os-version" {
  value = data.local_file.os.content
}
```

### Apply the Configuration

```bash theme={null}
opentofu init
opentofu plan
opentofu apply
```

Expected output:

```plaintext theme={null}
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:
os-version = <<EOT
PRETTY_NAME="Ubuntu 22.04.3 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
...
EOT
```

***

## AWS Data Sources

Next, we’ll work with AWS data sources. Below is a quick reference table for the examples covered.

| AWS Data Source  | Required Argument | Description                        |
| ---------------- | ----------------- | ---------------------------------- |
| aws\_ebs\_volume | volume\_id        | Fetches the EBS volume ID          |
| aws\_s3\_bucket  | bucket            | Specifies the existing bucket name |

### EBS Volume

Open `ebs.tf` to find a data source block for an AWS EBS volume:

```hcl theme={null}
data "aws_ebs_volume" "gpt_volume" {
  # configuration...
}
```

**Question:** Which attribute fetches the volume ID?\
**Answer:** `volume_id`

### S3 Bucket

In `s3.tf`, you’ll see a data source intended to read an existing S3 bucket:

```hcl theme={null}
data "aws_s3_bucket" "selected" {
  bucket_name = "bucket.test.com"
}
```

> **triangle-alert** The argument `bucket_name` is invalid. The correct argument is `bucket`.

Correct configuration:

```hcl theme={null}
data "aws_s3_bucket" "selected" {
  bucket = "bucket.test.com"
}
```

***

That completes this lesson on OpenTofu data sources. In upcoming modules, you’ll get more hands-on practice with AWS data sources and resources. Happy building!

## Links and References

* [OpenTofu Documentation][opentofu-docs]
* [AWS EBS Volume Data Source][aws-ebs-docs]
* [AWS S3 Bucket Data Source][aws-s3-docs]

[opentofu-docs]: https://docs.opentofu.org

[aws-ebs-docs]: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ebs_volume

[aws-s3-docs]: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/s3_bucket

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/420e1e82-8822-4b98-b49c-feff9ec4c1c2)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/38d2db09-c3d2-4582-94a0-8fe0271ed1fe)
