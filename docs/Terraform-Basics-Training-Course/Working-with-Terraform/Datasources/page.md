# local_file.pet[2] will be created
+ resource "local_file" "pet" {
    + directory_permission = "0777"
    + file_permission      = "0777"
    + filename             = "/root/pets.txt"
    + id                   = (known after apply)
}
Plan: 3 to add, 0 to change, 0 to destroy.
```

Each resource is indexed as `pet[0]`, `pet[1]`, and `pet[2]`. Although three resources are created, all instances share the same file name, which means Terraform creates the same file three times rather than three unique files.

***

## Creating Unique Resources by Using a List Variable

To generate unique resources, update the variable definition to a list and reference each element using `count.index`. Here is the modified configuration:

```hcl theme={null}
resource "local_file" "pet" {
  filename = var.filename[count.index]
  count    = 3
}
```

Define the list variable as follows:

```hcl theme={null}
variable "filename" {
  default = [
    "/root/pets.txt",
    "/root/dogs.txt",
    "/root/cats.txt"
  ]
}
```

In this configuration:

* The first iteration (index 0) creates `/root/pets.txt`.
* The second iteration (index 1) creates `/root/dogs.txt`.
* The third iteration (index 2) creates `/root/cats.txt`.

After executing `terraform apply`, listing the `/root` directory produces:

```bash theme={null}
$ ls /root
pets.txt
dogs.txt
cats.txt
```

This confirms that each resource is now unique.

***

## Dynamically Adjusting the Count with the length() Function

A drawback of the previous approach is its fixed count. If you wish to add more file names, the configuration would still create only three resources. To adapt dynamically to the number of elements, use the built-in `length()` function:

```hcl theme={null}
resource "local_file" "pet" {
  filename = var.filename[count.index]
  count    = length(var.filename)
}
```

You can now define the variable with any number of file names:

```hcl theme={null}
variable "filename" {
  default = [
    "/root/pets.txt",
    "/root/dogs.txt",
    "/root/cats.txt",
    "/root/cows.txt",
    "/root/ducks.txt"
  ]
}
```

When running `terraform apply`, Terraform will automatically create five resources—one for each element in the list. To revert back to testing with three elements, simply modify the list back to three filenames:

```hcl theme={null}
variable "filename" {
  default = [
    "/root/pets.txt",
    "/root/dogs.txt",
    "/root/cats.txt"
  ]
}
```

After applying these changes, the `/root` directory will properly contain the three files.

***

<Callout icon="triangle-alert">
  Modifying a list that drives the count parameter can lead to resource replacements due to index shifts. This may trigger unwanted service interruptions or data loss if the resources are critical.
</Callout>

## A Pitfall: List Element Removal and Resource Replacement

When using count with a list, removing an element causes a shift in resource indices. Consider this configuration:

```hcl theme={null}
resource "local_file" "pet" {
  filename = var.filename[count.index]
  count    = length(var.filename)
}
```

Initially, the variable is defined with three elements:

```hcl theme={null}
variable "filename" {
  default = [
    "/root/pets.txt",
    "/root/dogs.txt",
    "/root/cats.txt"
  ]
}
```

After a successful apply, Terraform recognizes three resources: `pet[0]`, `pet[1]`, and `pet[2]`. Now, if you remove the first element (`/root/pets.txt`), the updated variable becomes:

```hcl theme={null}
variable "filename" {
  default = [
    "/root/dogs.txt",
    "/root/cats.txt"
  ]
}
```

Running `terraform plan` now shows:

* The resource at index 0 is updated from `/root/pets.txt` to `/root/dogs.txt`.
* The resource at index 1 is updated from `/root/dogs.txt` to `/root/cats.txt`.
* The resource at index 2 is marked for destruction as there is no corresponding list element.

An abbreviated plan output looks like this:

```bash theme={null}
$ terraform plan
...
# local_file.pet[0] must be replaced
-/+ resource "local_file" "pet" {
    directory_permission = "0777"
    file_permission      = "0777"
    ~ filename           = "/root/pets.txt" -> "/root/dogs.txt" #
}
# local_file.pet[1] must be replaced
-/+ resource "local_file" "pet" {
    directory_permission = "0777"
    file_permission      = "0777"
    ~ filename           = "/root/dogs.txt" -> "/root/cats.txt" #
}
# local_file.pet[2] will be destroyed
-/+ resource "local_file" "pet" {
    directory_permission = "0777" -> null
    file_permission      = "0777" -> null
    ~ filename           = "/root/cats.txt" -> null #
}
```

This behavior occurs because the resource indices are directly linked to the order of the list elements. Removing an element causes subsequent elements to shift, resulting in the unnecessary replacement or destruction of resources.

***

## Viewing Resource Details

It is often useful to confirm resource details created with count. Adding an output variable lets you verify each resource's configuration:

```hcl theme={null}
output "pets" {
  value = local_file.pet
}
```

After running `terraform output`, you should see similar details for each resource:

```bash theme={null}
$ terraform output
Outputs:
pets = [
  {
    "directory_permission" = "0777"
    "file_permission"      = "0777"
    "filename"             = "/root/pets.txt"
    "id"                   = "da39a3ee5e6b4d3255bef95601890afd80709"
  },
  {
    "directory_permission" = "0777"
    "file_permission"      = "0777"
    "filename"             = "/root/dogs.txt"
    "id"                   = "da39a3ee5e6b4d3255bef95601890afd80709"
  },
  {
    "directory_permission" = "0777"
    "file_permission"      = "0777"
    "filename"             = "/root/cats.txt"
    "id"                   = "da39a3ee5e6b4d3255bef95601890afd80709"
  },
]
```

This output confirms that Terraform manages the resources as a list, allowing each element to be accessed individually by its index.

***

## Conclusion

In this article, we demonstrated how to use the count meta-argument in Terraform to create multiple resource instances. We examined both static and dynamic count methods using a list variable and the `length()` function, respectively. Additionally, we discussed a common pitfall—removing an element from the list can trigger resource replacements due to index shifting.

Practice using the count meta-argument in your Terraform projects to automate resource creation and better manage infrastructure changes.

For more detailed information on Terraform and its resource management, refer to the [Terraform Documentation](https://www.terraform.io/docs).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/98de9b33-985e-4ec4-9903-b39856d309e8/lesson/7a326097-ef01-44ef-99b1-f4ca9402a910" />
</CardGroup>


# Datasources

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Working-with-Terraform/Datasources/page

This article explains how Terraform uses data sources to read information from externally managed resources for infrastructure provisioning.

In this lesson, we explore how Terraform utilizes data sources to read information from resources that are managed externally. Terraform leverages configuration files and a state file to provision infrastructure resources, but it can also interact with resources that are created manually, by other tools (such as Puppet, CloudFormation, SaltStack, Ansible, etc.), ad-hoc scripts, or even resources provisioned by another Terraform configuration.

For instance, consider a database instance that was manually provisioned in the AWS cloud. Even though Terraform does not manage this resource, it can still read attributes—such as the database name, host address, or DB user details—and use that information to provision an application resource managed by Terraform.

<Frame>
  ![The image illustrates infrastructure management tools, highlighting Terraform's role in managing real-world infrastructure and state files, alongside other tools like CloudFormation and Ansible.](https://kodekloud.com/kk-media/image/upload/v1752884244/notes-assets/images/Terraform-Basics-Training-Course-Datasources/frame_50.jpg)
</Frame>

Now, consider a simpler scenario with a local file resource named "pet" containing the text "We love pets!" When Terraform creates this resource, it generates the file `/root/pets.txt` and stores its information in the state file. Meanwhile, another file—created by an external shell script—is located at `/root/dog.txt` and contains "Dogs are awesome!" Because `dog.txt` is not managed by Terraform, we can use it as a data source to supply content for our managed resource `pets.txt`.

<Callout icon="lightbulb">
  Data sources in Terraform enable you to use attributes from external resources, integrating them into your Terraform-managed infrastructure.
</Callout>

Data sources are defined using the `data` block in your configuration. Although these blocks resemble resource blocks, they start with the keyword `data` instead of `resource`. Below is an example configuration that demonstrates this process:

```bash theme={null}
$ cat /root/dog.txt
Dogs are awesome!
```

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = data.local_file.dog.content
}

data "local_file" "dog" {
  filename = "/root/dog.txt"
}
```

In the configuration above:

* The resource block creates a file called `/root/pets.txt` with its content dynamically populated using data from `dog.txt`.
* The data block reads from the local file located at `/root/dog.txt` and makes its content available via the expression `data.local_file.dog.content`.

According to the Terraform documentation on the [Terraform Registry](https://registry.terraform.io/), the local file data source exports two attributes:

* The raw content of the file.
* The base64-encoded version of the file's content.

This feature allows you to easily integrate external data into your Terraform configurations.

<Frame>
  ![The image shows a documentation page for a local provider, detailing argument references and exported attributes for reading a file, including filename, content, and base64 encoding.](https://kodekloud.com/kk-media/image/upload/v1752884245/notes-assets/images/Terraform-Basics-Training-Course-Datasources/frame_210.jpg)
</Frame>

To clearly distinguish between resources and data sources in Terraform:

| Type        | Purpose                                                 | Management by Terraform                          |
| ----------- | ------------------------------------------------------- | ------------------------------------------------ |
| Resource    | Create, update, and destroy infrastructure elements     | Managed; stored in the state file                |
| Data Source | Read and reference information from unmanaged resources | Not managed; used for reference within Terraform |

This distinction is further illustrated in the following comparison diagram:

<Frame>
  ![The image compares Terraform resources and data sources, highlighting their keywords, functions, and alternative names, alongside a "terraform.tfstate" file icon.](https://kodekloud.com/kk-media/image/upload/v1752884246/notes-assets/images/Terraform-Basics-Training-Course-Datasources/frame_240.jpg)
</Frame>

That concludes this article on data sources in Terraform. For further information on utilizing Terraform with external resources, refer to the official [Terraform Documentation](https://www.terraform.io/docs).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/98de9b33-985e-4ec4-9903-b39856d309e8/lesson/891baedf-ffb0-4f4c-969f-c9ac9668fedf" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/98de9b33-985e-4ec4-9903-b39856d309e8/lesson/0a7ce33b-d179-4a84-ad51-665242858993" />
</CardGroup>
