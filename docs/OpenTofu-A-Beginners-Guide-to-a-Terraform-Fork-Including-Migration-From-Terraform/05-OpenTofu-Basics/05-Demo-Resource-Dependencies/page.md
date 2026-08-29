# local_file.time:
resource "local_file" "time" {
  filename = "/root/time.txt"
  content  = "Timestamp of this file: 2024-04-09T09:52:41Z"
  id       = "f095dbo698d1e64f847e39f01fc9f7d4592ff48"
}

# time_static.time_update:
resource "time_static" "time_update" {
  id      = "2024-04-09T09:52:41Z"
  rfc3339 = "2024-04-09T09:52:41Z"
  day     = 9
  month   = 4
  year    = 2024
  hour    = 9
  minute  = 52
  second  = 41
  unix    = 1712656361
}
```

**Question:** What is the `id` of `local_file.time`?\
**Answer:** `f095dbo698d1e64f847e39f01fc9f7d4592ff48`

***

## 8. Retrieve the `rfc3339` Timestamp

From the same output, you can also see:

```hcl theme={null}
rfc3339 = "2024-04-09T09:52:41Z"
```

**Question:** What is the `rfc3339` value?\
**Answer:** `2024-04-09T09:52:41Z`

***

## 9. Final Configuration Snapshot

After apply, your resources look like this:

```hcl theme={null}
resource "local_file" "time" {
  filename = "/root/time.txt"
  content  = "Timestamp of this file: ${time_static.time_update.id}"
}

resource "time_static" "time_update" {
  day     = 9
  month   = 4
  year    = 2024
  hour    = 9
  minute  = 52
  second  = 41
  unix    = 1712656361
  id      = "2024-04-09T09:52:41Z"
  rfc3339 = "2024-04-09T09:52:41Z"
}
```

That wraps up this demo on using resource attributes in OpenTofu. Happy provisioning!

***

## Links and References

* OpenTofu Documentation: [https://docs.opentofu.org/](https://docs.opentofu.org/)
* [time\_static resource][time_static_docs]
* [OpenTofu CLI Reference](https://docs.opentofu.org/cli/)

[time_static_docs]: https://docs.opentofu.org/providers/time/latest/resources/time_static

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/61653bc6-12ac-4e0e-aa02-418c66a4c897)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/e7474bbe-4cb3-4d66-ab87-1b33a6510ca4)


# Demo Resource Dependencies

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Demo-Resource-Dependencies/page

This lesson demonstrates managing resource dependencies in OpenTofu using explicit and implicit approaches.

This lesson demonstrates how to manage resource dependencies in OpenTofu, covering both explicit and implicit approaches using `depends_on` and attribute references.

## Table of Contents

1. [Understanding Resource Dependencies](#understanding-resource-dependencies)
2. [Generating a TLS Private Key](#generating-a-tls-private-key)
3. [Writing the Key to a Local File](#writing-the-key-to-a-local-file)
4. [Cleanup](#cleanup)
5. [Explicit Dependency with depends\_on](#explicit-dependency-with-depends_on)
6. [Links and References](#links-and-references)

## Understanding Resource Dependencies

OpenTofu resources can depend on each other in two ways:

| Dependency Type | Definition                                                                 | Syntax Example                                     |
| --------------- | -------------------------------------------------------------------------- | -------------------------------------------------- |
| Explicit        | Resource A waits for Resource B without accessing its attributes directly. | `depends_on = [local_file.krill]`                  |
| Implicit        | Resource A references Resource B’s attribute in its arguments.             | `content = tls_private_key.pvtkey.private_key_pem` |

First, we set an **explicit dependency** using the `depends_on` argument when Resource A does not reference Resource B’s attributes:

![The image shows a Visual Studio Code editor with a welcome message for KodeKloud OpenTofu Lab on the right, and a multiple-choice question about dependencies on the left.](https://kodekloud.com/kk-media/image/upload/v1752882826/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-Resource-Dependencies/vscode-kodekloud-opentofu-lab-question.jpg)

Next, an **implicit dependency** is created by referencing one resource’s attributes inside another:

![The image shows a KodeKloud OpenTofu Lab interface with a Visual Studio Code editor on the right, displaying a welcome message and terminal, and a quiz question on the left about implicit dependency.](https://kodekloud.com/kk-media/image/upload/v1752882827/notes-assets/images/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform-Demo-Resource-Dependencies/kodekloud-opentofu-lab-vscode-quiz.jpg)

## Generating a TLS Private Key

Navigate to your project’s `key-generator` directory and create `key.tf`:

```hcl theme={null}
resource "tls_private_key" "pvtkey" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
```

Initialize, plan, and apply the configuration:

```bash theme={null}
opentofu init
opentofu plan
opentofu apply
