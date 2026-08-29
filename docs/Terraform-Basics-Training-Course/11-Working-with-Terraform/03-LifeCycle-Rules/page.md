# LifeCycle Rules

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Working-with-Terraform/LifeCycle-Rules/page

This article explores configuring lifecycle rules in Terraform to manage resource creation and deletion effectively, ensuring service continuity during infrastructure updates.

In this article, we explore how to configure lifecycle rules in Terraform to control the order of resource creation and deletion. Managing resource lifecycles can help ensure service continuity and prevent unintended disruptions during your infrastructure updates.

By default, when Terraform updates a resource, it treats it as immutable. This means the existing resource is deleted before a new one is created with the updated configuration. For example, if you update the file permissions on a local file resource from 0777 to 0700 and then run `terraform apply`, Terraform will first delete the old file and then create a new one.

> **lightbulb** By default, Terraform’s update process deletes the existing resource before creating a new one, which may not be desirable in all scenarios.

## Understanding Terraform's Update Mechanism

Consider the following example where we update the file permission of a local file resource:

```hcl theme={null}
resource "local_file" "pet" {
  filename        = "/root/pets.txt"
  content         = "We love pets!"
  file_permission = "0700"
}
```

When you run the `terraform apply` command, you might see an output similar to:

```bash theme={null}
$ terraform apply
