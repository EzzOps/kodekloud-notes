# local_file.pet must be replaced
resource "local_file" "pet" {
  content              = "My favorite pet is Mrs.Cat!" -> "My favorite pet is Mr.bull" # forces replacement
  directory_permission = "0777"
  file_permission      = "0777"
  filename             = "/roots/pets.txt"
  id                   = "[AWS_SECRET_ACCESS_KEY]" -> (known after apply)
}
.
.
local_file.pet: Destroying...
  [id=[AWS_SECRET_ACCESS_KEY]]
local_file.pet: Destruction complete after 0s
local_file.pet: Creating...
local_file.pet: Creation complete after 0s
  [[SECRET_REDACTED]]
Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```

<Callout icon="lightbulb">
  Explore working with resource taints and various resource attributes in Terraform to further optimize your infrastructure management.
</Callout>

For more detailed information, refer to the [Terraform Documentation](https://registry.terraform.io) and [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/983ca20c-8d60-4254-ae4c-f6526851e757" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/4ee0f042-a6f5-4d0e-9956-5f0f1f72ec2d" />
</CardGroup>


# Resource Dependencies

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Basics/Resource-Dependencies/page

This lesson explores resource dependencies in Terraform, focusing on implicit and explicit dependencies for resource creation and deletion management.

In this lesson, we explore various types of resource dependencies in Terraform and how they affect resource creation and deletion. Terraform uses both implicit and explicit dependencies to manage the order in which resources are provisioned.

Terraform automatically detects implicit dependencies through reference expressions. For example, when you pass the output of one resource (like a random pet) to another resource (such as a local file), Terraform understands that the random pet must be created before the local file. Similarly, during deletion, Terraform removes the resources in reverse order to maintain consistency.

Below is an example of an implicit dependency:

```hcl theme={null}
resource "local_file" "pet" {
  filename = var.filename
  content  = "My favorite pet is ${random_pet.my-pet.id}"
}

resource "random_pet" "my-pet" {
  prefix    = var.prefix
  separator = var.separator
  length    = var.length
}
```

<Callout icon="lightbulb">
  Implicit dependencies require no manual configuration; Terraform deduces the correct order from references, ensuring that resources are created or destroyed accordingly.
</Callout>

In some scenarios, a resource might indirectly rely on another resource without any direct reference. In these cases, you can explicitly specify the dependency using the `depends_on` argument. This method ensures that Terraform provisions and destroys resources in the intended order.

The following configuration illustrates an explicit dependency where the local file resource explicitly depends on the random pet resource:

```hcl theme={null}
resource "local_file" "pet" {
  filename   = var.filename
  content    = "My favorite pet is Mr.Cat"
  depends_on = [
    random_pet.my-pet
  ]
}

resource "random_pet" "my-pet" {
  prefix    = var.prefix
  separator = var.separator
  length    = var.length
}
```

<Callout icon="lightbulb">
  Explicit dependencies are especially useful in complex configurations where resources are indirectly interconnected without a clear reference link. They help prevent race conditions and ensure that resources are managed in the correct order.
</Callout>

In the upcoming sections, we will delve into real-world use cases and best practices for managing resource dependencies in Terraform. Up next, we'll move into hands-on labs where you can practice working with both implicit and explicit dependencies to deepen your understanding of Terraform resource management.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/793316ce-6a9b-40ac-bde0-54afb04e5206" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/1a286bc1-8798-4f21-8764-2d9781efee7a" />
</CardGroup>
