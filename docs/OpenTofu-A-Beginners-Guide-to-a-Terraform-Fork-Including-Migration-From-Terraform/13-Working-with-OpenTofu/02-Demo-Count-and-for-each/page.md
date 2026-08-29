# Demo Count and for each

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Working-with-OpenTofu/Demo-Count-and-for-each/page

Learn to use `count` and `for_each` in OpenTofu for dynamic resource creation through practical tasks and examples.

In this lab, you’ll learn how to leverage the `count` and `for_each` meta-arguments to create multiple resource instances dynamically in OpenTofu. We’ll work through a series of tasks:

* Inspecting a basic configuration
* Scaling with `count`
* Parameterizing with variables
* Ensuring uniqueness with `for_each`

***

## Task 1: Inspect the Base Configuration

Navigate to your project directory:

```bash theme={null}
cd /root/opentofu-projects/project-shade
```

Open the default `main.tf`:

```hcl theme={null}
resource "local_sensitive_file" "name" {
  filename = "/root/user-data"
  content  = "password: S3cr3tP@ssw0rd"
}
```

Since there’s only **one** resource block, running `opentofu plan` would create **one** file at `/root/user-data`.

***

## Task 2: Create Multiple Instances with `count`

Add the `count` argument to generate three instances:

```hcl theme={null}
resource "local_sensitive_file" "name" {
  filename = "/root/user-data"
  content  = "password: S3cr3tP@ssw0rd"
  count    = 3
}
```

Initialize and preview:

```bash theme={null}
opentofu init
opentofu plan
```

Expected plan excerpt:

```plaintext theme={null}
