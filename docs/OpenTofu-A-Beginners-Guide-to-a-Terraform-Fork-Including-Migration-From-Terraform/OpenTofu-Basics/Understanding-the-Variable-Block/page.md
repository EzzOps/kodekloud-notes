# Understanding the Variable Block

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Understanding-the-Variable-Block/page

Explains how to define and use OpenTofu variable blocks, covering defaults, types, validation, sensitive flag, collections like list map set object tuple, and best practices for security

In this lesson we recap how to use variables within an OpenTofu configuration. Variables let you parameterize your configuration, provide defaults, validate input, and mark values as sensitive to reduce accidental exposure in CLI output.

A variable block is valid even when it declares no arguments. If no `default` is provided, you must supply a value at runtime (via CLI flags like `-var`, environment variables, or tfvars files). Within a `variable` block you can include:

* `default` — a default value used when no other value is provided
* `description` — a helpful human-readable explanation (recommended)
* `type` — constrains accepted values (e.g., `string`, `list(string)`, `object({...})`)
* `sensitive` — if `true`, hides the value in CLI plan/apply output

Example: default, description, type, and sensitive

```hcl theme={null}
variable "ami" {
  default     = "ami-0edab43b6fa892279"
  description = "Type of AMI to use"
  type        = string
  sensitive   = true
}

variable "instance_type" {
  default     = "t2.micro"
  description = "Size of EC2 instance"
  type        = string
  sensitive   = false
}
```

<Callout icon="warning">
  Setting sensitive = true suppresses the value in plan/apply output, but the value will still be recorded in the OpenTofu state file. Protect state (for example, by enabling encryption and restricting access) to keep secrets safe.
</Callout>

## Validation rules for variables

You can add a `validation` block inside a variable to enforce constraints and return helpful error messages. For example, AWS AMI IDs typically start with `ami-`. The following variable enforces that rule and provides a custom error message.

```hcl theme={null}
variable "ami" {
  type        = string
  description = "The id of the machine image (AMI) to use for the server."

  validation {
    condition     = substr(var.ami, 0, 4) == "ami-"
    error_message = "The AMI should start with \"ami-\"."
  }
}
```

If you pass an invalid value at the CLI, OpenTofu runs the validation and returns the error.

Example CLI invocation:

```bash theme={null}
$ tofu apply -var "ami=abc-11223"
```

Example console output:

```text theme={null}
Error: Invalid value for variable

on main.tf line 1:
1: variable "ami" {

The ami value must be a valid AMI id, starting with "ami-".

This was checked by the validation rule at main.tf:5,3-13.
```

## Basic scalar types

OpenTofu supports these basic HCL scalar types: `string`, `number`, and `bool` (HCL uses `bool` rather than the word "boolean"). If you omit `type`, it defaults to `any`.

<Callout icon="lightbulb">
  If `type` is omitted, the variable's type is `any` by default—using explicit types is recommended to catch configuration errors early.
</Callout>

Examples for `number` and `bool`:

```hcl theme={null}
variable "count" {
  default     = 2
  type        = number
  description = "Count of VMs"
}

variable "monitoring" {
  default     = true
  type        = bool
  description = "Enable detailed monitoring"
}
```

### Type coercion and mismatches

* If you provide both `type` and `default`, the default must match the declared type.
* OpenTofu will attempt some conversions (for example, string ↔ number or string ↔ bool), but relying on coercion is error-prone.
* If coercion is impossible (for example, `type = bool` with `default = 1`), OpenTofu will error and you must fix the mismatch.

Invalid example (this will error):

```hcl theme={null}
variable "monitoring" {
  default     = 1
  type        = bool
  description = "Enable detailed monitoring"
}
```

## Collections and complex types

Beyond scalars, OpenTofu supports: `list`, `set`, `map`, `object`, and `tuple`. Use typed constructors such as `list(string)` or `map(number)` to enforce element types.

Type reference table:

| HCL Type | Use Case                                       | Example                               |
| -------: | ---------------------------------------------- | ------------------------------------- |
|   string | Simple text values                             | `"/root/pets.txt"`                    |
|   number | Numeric values                                 | `1`                                   |
|     bool | true/false flags                               | `true`                                |
|      any | Accept any type (default when omitted)         | `default = "value"`                   |
|     list | Ordered sequence                               | `["web1", "web2"]`                    |
|      set | Unordered unique collection                    | `["db1","db2"]`                       |
|      map | Key-value lookup                               | `{ region1 = "us-east-1" }`           |
|   object | Structured named attributes with types         | `object({ name=string, age=number })` |
|    tuple | Fixed-length sequence with heterogeneous types | `tuple([string, number])`             |

### Lists

A `list` is an ordered sequence (index starts at 0). Use `list(string)` (or `list(number)`, etc.) to constrain element types.

```hcl theme={null}
variable "servers" {
  default = ["web1", "web2", "web3"]
  type    = list(string)
}
```

Access an element by index:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  tags = {
    name = var.servers[0]  # "web1"
  }
}
```

### Maps

A `map` is a key-value collection. Use `map(string)` or `map(number)` to constrain value types.

```hcl theme={null}
variable "instance_type" {
  type = map(string)

  default = {
    production  = "m5.large"
    development = "t2.micro"
  }
}
```

Access a value by key:

```hcl theme={null}
resource "aws_instance" "development" {
  ami           = var.ami
  instance_type = var.instance_type["development"]
  tags = {
    name = var.servers[0]
  }
}
```

### Combining types with constraints

You can declare lists of specific types or maps of numbers. If values don't match the declared constraint and cannot be coerced, OpenTofu will fail.

```hcl theme={null}
variable "prefixes" {
  default = ["web1", "web2", "web3"]
  type    = list(string)
}

variable "server_count" {
  default = {
    web   = 3
    db    = 1
    agent = 2
  }
  type = map(number)
}
```

### Sets

A `set` is an unordered collection that forbids duplicates. Use `set(string)` or `set(number)`.

Valid set example:

```hcl theme={null}
variable "db_hosts" {
  default = ["db1", "db2"]
  type    = set(string)
}
```

Invalid (contains duplicates; will error):

```hcl theme={null}
