# random_pet.my-pet will be created
+ resource "random_pet" "my-pet" {
+   id        = (known after apply)
+   length    = 1
+   prefix    = "Mrs"
+   separator = "."
}

Plan: 1 to add, 0 to change, 0 to destroy.
```

## Applying the Configuration

Once you are satisfied with the execution plan, apply the configuration using Terraform apply. This step creates the new resource for the random pet while leaving the local file resource unchanged. Notice that the random provider outputs the generated pet name:

```bash theme={null}
$ terraform apply
local_file.pet: Refreshing state...
[id=d1a31467f206d6ea8ab1cad382bc106bf46df69e]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

# random_pet.my-pet will be created
+ resource "random_pet" "my-pet" {
  + id        = (known after apply)
  + length    = 1
  + prefix    = "Mrs"
  + separator = "."
}

Plan: 1 to add, 0 to change, 0 to destroy.

random_pet.my-pet: Creating...
random_pet.my-pet: Creation complete after 0s [id=Mrs.hen]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

Notice that an attribute called "id" appears in the output, reflecting the generated pet name.

<Callout icon="lightbulb">
  Although this example uses a pet symbol for demonstration, the random pet resource can generate a variety of pet names and is not limited to any specific animal type.
</Callout>

## Next Steps

Now that you have learned how to work with multiple providers in Terraform, continue experimenting with additional providers and resource types to further expand your infrastructure automation skills. For more detailed information on Terraform providers and best practices, visit the [Terraform Documentation](https://terraform.io/docs).

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/1d2c3002-ead1-4ee8-8b41-cc60bebd6315" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/9ddacf3d-182a-4932-80b4-da86babc0a2a" />
</CardGroup>


# Output Variables

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Basics/Output-Variables/page

Terraform output variables store results from configuration files for later use, enhancing resource management and integration with other tools.

Terraform output variables are a powerful feature that allow you to store the results of expressions from your configuration files for later use. In previous lessons, we covered input variables and reference expressions; output variables complement these by enabling you to retrieve and present important output information after your infrastructure has been provisioned.

## Capturing Resource Attributes

Consider a configuration that creates a random pet name using Terraform's resource definitions. In this example, a resource called random\_pet generates a pet name, and an output variable called pet-name captures the generated id. This is especially useful for passing data to other tools or for quick resource verification.

Below is an example configuration:

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

output "pet-name" {
  value = random_pet.my-pet.id
  desc  = ""
}
```

The output block starts with the keyword `output` followed by the variable name. Inside the block, the **value** argument is required and uses a reference expression (`random_pet.my-pet.id`). Although the **desc** argument is optional, it is a good practice to include a brief description of the output's purpose.

<Callout icon="lightbulb">
  Use meaningful descriptions for your output variables. This practice enhances code readability and aids in documentation, especially when collaborating with other team members.
</Callout>

## Configuration of Related Variables

To support the resources defined above, ensure the following variables are declared in your configuration:

```hcl theme={null}
variable "filename" {
  default = "/root/pets.txt"
}

variable "content" {
  default = "I love pets!"
}

variable "prefix" {
  default = "Mrs"
}

variable "separator" {
  default = "."
}

variable "length" {
  default = "1"
}
```

These variable definitions set the necessary defaults and ensure the configuration runs smoothly during execution.

## Displaying Outputs with Terraform

When you run `terraform apply`, Terraform automatically displays the output variables after resource creation. For example:

```bash theme={null}
$ terraform apply
...
Outputs:
  pet-name = Mrs.gibbon
```

You can also retrieve the value of output variables at any time using the `terraform output` command. Running the command without any arguments lists all outputs:

```bash theme={null}
$ terraform output
pet-name = Mrs.gibbon
```

To display an individual output variable, simply specify its name:

```bash theme={null}
$ terraform output pet-name
Mrs.gibbon
```

<Callout icon="lightbulb">
  Output variables are invaluable for quickly viewing details about your provisioned resources and for integrating with other infrastructure as code tools, ad hoc scripts, or configuration management systems like Ansible.
</Callout>

## Further Reading

For more comprehensive information on Terraform output variables and other configuration concepts, please refer to the following resources:

* [Terraform Official Documentation](https://www.terraform.io/docs)
* [Terraform CLI Documentation](https://www.terraform.io/cli)

By incorporating output variables into your Terraform configurations, you can streamline the process of accessing essential resource details and improve the overall management of your infrastructure.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/5b60fceb-9041-4f11-9cb2-24a04cf37e94" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/6026caa5-ccaf-41f9-8842-6e2ff319231c" />
</CardGroup>
