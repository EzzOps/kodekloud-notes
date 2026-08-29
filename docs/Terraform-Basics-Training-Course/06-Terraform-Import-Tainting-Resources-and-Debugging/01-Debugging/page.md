# main.tf
resource "local_file" "pet" {
  filename = var.filename
  content  = var.content
}

resource "random_pet" "my-pet" {
  prefix    = var.prefix
  separator = var.separator
  length    = var.length
}
```

```hcl theme={null}
# variables.tf
variable "filename" {
  default = "/root/pets.txt"
}

variable "content" {
  default = "We love pets!"
}

variable "prefix" {
  default = "Mrs"
}

variable "separator" {
  default = "."
}

variable "length" {
  default = 2
}
```

In this example, each variable is provided with a default value. This approach ensures that Terraform has a fallback value when none is explicitly supplied, making your configurations more robust.

***

## Providing Variable Values Interactively and via the Command Line

If a variable does not have a default value or if you want to override an existing default, Terraform will prompt you for a value during `terraform apply`. To streamline automation and avoid interactive prompts, you can pass values using the `-var` flag. You can supply multiple `-var` flags as needed:

```bash theme={null}
$ terraform apply -var "filename=/root/newfile.txt" -var "content=Hello, Terraform!"
```

Alternatively, you can set environment variables by prefixing the variable name with `TF_VAR_`. For example, you can configure your shell as follows:

```bash theme={null}
$ export TF_VAR_filename="/root/pets.txt"
$ export TF_VAR_content="We love pets!"
$ export TF_VAR_prefix="Mrs"
$ export TF_VAR_separator="."
$ export TF_VAR_length="2"
$ terraform apply
```

In this scenario, Terraform automatically picks up the environment variable values during execution, providing a convenient method for variable assignment.

***

## Using Variable Definition Files

When managing many variables, it becomes practical to store their values in a dedicated variable definition file. These files typically have a `.tfvars` or `.tfvars.json` extension. For example, you can create a file named `terraform.tfvars` with the following contents:

```hcl theme={null}
filename = "/root/pets.txt"
content  = "We love pets!"
prefix   = "Mrs"
separator = "."
length   = "2"
```

Terraform automatically loads files named `terraform.tfvars`, `terraform.tfvars.json`, or files with extensions like `.auto.tfvars` or `.auto.tfvars.json`. If you use a differently named file (e.g., `variables.tfvars`), be sure to specify it explicitly with the `-var-file` flag:

```bash theme={null}
$ terraform apply -var-file="variables.tfvars"
```

This approach centralizes your variable definitions and simplifies the management of Terraform environments.

***

## Variable Definition Precedence

Terraform allows you to set variable values from multiple sources. When the same variable is defined in multiple places, Terraform uses a specific order of precedence to determine which value to apply. Consider the following scenario where a variable is defined in various ways:

* **Environment Variable:**
  ```bash theme={null}
  $ export TF_VAR_filename="/root/cats.txt"
  ```

* **terraform.tfvars File:**
  ```hcl theme={null}
  filename = "/root/pets.txt"
  ```

* **File Ending with .auto.tfvars:**
  ```hcl theme={null}
  filename = "/root/mypet.txt"
  ```

* **Command-Line Flag:**
  ```bash theme={null}
  $ terraform apply -var "filename=/root/best-pet.txt"
  ```

Below is the sample configuration file:

```hcl theme={null}
# main.tf
resource "local_file" "pet" {
  filename = var.filename
}

# variables.tf
variable "filename" {
  type = string
}
```

Terraform follows this strict order of precedence when assigning variable values:

| Precedence Level                                           | Example Call or File                               |
| ---------------------------------------------------------- | -------------------------------------------------- |
| 1. Environment variables (`TF_VAR_`)                       | export TF\_VAR\_filename="/root/cats.txt"          |
| 2. terraform.tfvars file                                   | filename = "/root/pets.txt"                        |
| 3. Files ending with `.auto.tfvars` or `.auto.tfvars.json` | filename = "/root/mypet.txt"                       |
| 4. Command-line flags (`-var` or `-var-file`)              | terraform apply -var "filename=/root/best-pet.txt" |

Since the command-line flag (`-var`) has the highest precedence in this example, the variable `filename` will ultimately be assigned the value `/root/best-pet.txt`.

<Callout icon="lightbulb">
  Remember, the order in which variable values are applied ensures predictability in your deployment. This hierarchy allows you to override defaults and maintain control over your configuration settings.
</Callout>

***

That's it for this lesson. With these variable assignment techniques, you're ready to build flexible and maintainable Terraform configurations. Now, let's head to the hands-on lab and put these concepts into practice!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/8a48cd5b-2303-43e2-b469-f7b40951d650" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/df2660a4-c959-4fa7-bfa8-0700885b598e/lesson/a4f921ce-6e6f-4029-b0c0-9d2692f18c88" />
</CardGroup>


# Debugging

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Import-Tainting-Resources-and-Debugging/Debugging/page

This article explores enabling and using debugging in Terraform to troubleshoot and resolve issues effectively.

In this article, we explore how to enable and use debugging in Terraform to effectively troubleshoot and resolve issues. When Terraform errors occur, the first step is to review the log output. While Terraform’s error messages during provisioning are helpful, sometimes you need to dive deeper for an internal view.

Terraform allows you to increase the debugging output by setting the environment variable TF\_LOG to one of the available log level values. The supported log levels are: info, warning, error, debug, and trace—with trace providing the most detailed output.

<Callout icon="lightbulb">
  For the most verbose logging, use TF\_LOG=TRACE. This is particularly useful when facing complex issues that require insight into Terraform's inner workings.
</Callout>

## Enabling Debugging

To enable the trace log level, set the TF\_LOG environment variable as follows:

```bash theme={null}
