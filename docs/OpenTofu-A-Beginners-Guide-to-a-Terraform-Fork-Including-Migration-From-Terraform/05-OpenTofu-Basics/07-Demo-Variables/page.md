# Demo Variables

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Demo-Variables/page

Hands-on lab on defining and using variables in Terraform (OpenTofu) for cleaner, reusable configurations.

Welcome to this hands-on lab on defining and using variables in Terraform (OpenTofu). By the end of this tutorial, you’ll understand how to declare different variable types, fetch elements from maps and lists, and refactor resources to leverage variables for cleaner, reusable configurations.

***

## 1. Variable Type Quiz

**Question:** Which of the following is **not** a valid Terraform variable type?

* object
* item
* tuple
* list
* map

**Answer:** `item` is not a valid variable type in Terraform/OpenTofu.

| Variable Type | Description                                               |
| ------------- | --------------------------------------------------------- |
| object        | Collection of named attributes with specific types        |
| tuple         | Ordered list of elements with potentially different types |
| list          | Ordered homogeneous collection                            |
| map           | Unordered key–value pairs with homogeneous values         |

For more details, see the [Terraform Variable Types](https://developer.hashicorp.com/terraform/language/values/variables#type-constraints).

***

## 2. Data Type Quiz

**Question:** Which of the following is **not** a valid data type in OpenTofu?

* list
* tuple
* map
* array
* set

**Answer:** `array` is not a valid data type in OpenTofu.

***

## Setup: Navigate to the Variables Directory

```bash theme={null}
cd /root/OpenTofu-project/variables
```

***

## 3. Inspecting `number`

Open **variables.tf** and locate:

```hcl theme={null}
variable "number" {
  type    = bool
  default = false
}
```

**Question:** Which type does `number` belong to?\
**Answer:** It’s a **boolean**.

***

## 4. Fetching a Map Value

In **variables.tf**, you have:

```hcl theme={null}
variable "hard_drive" {
  type = map(string)
  default = {
    slow = "HDD"
    fast = "SSD"
  }
}
```

**Question:** How do you retrieve the `"slow"` entry?

```hcl theme={null}
var.hard_drive["slow"]
```

> **lightbulb** You can also use the dot notation if your key is a valid identifier, e.g., `var.hard_drive.slow`.

***

## 5. List Indexing

Definition in **variables.tf**:

```hcl theme={null}
variable "gender" {
  type    = list(string)
  default = ["Male", "Female"]
}
```

* Lists are zero-indexed.
* `"Male"` → index 0
* `"Female"` → index 1

**Answer:** The index of `"Female"` is **1**.

***

## 6. Identifying a Set Definition Error

```hcl theme={null}
variable "users" {
  type    = set(string)
  default = ["tom", "jerry", "pluto", "daffy", "donald", "jerry"]
}
```

* **Type:** `set(string)`
* **Mistake:** Sets must not contain duplicates; `"jerry"` appears twice.

> **triangle-alert** Defining duplicate elements in a `set` will cause validation errors. Ensure each member is unique.

***

## 7. Inspecting a Resource Block

In **main.tf**, you added:

```hcl theme={null}
resource "local_file" "jedi" {
  filename = "/root/first-jedi"
  content  = "phanius"
}
```

**Question:** What is the value of the `content` argument?\
**Answer:** `"phanius"`

***

## 8. Refactoring to Use Variables

1. **Declare a map variable** in **variables.tf**:

   ```hcl theme={null}
   variable "jedi" {
     type = map(string)
     default = {
       filename = "/root/first-jedi"
       content  = "phanius"
     }
   }
   ```

2. **Update the resource** in **main.tf**:

   ```hcl theme={null}
   resource "local_file" "jedi" {
     filename = var.jedi["filename"]
     content  = var.jedi["content"]
   }
   ```

This makes your configuration more modular and easier to maintain.

***

## 9. Initialize, Plan, and Apply

```bash theme={null}
cd /root/OpenTofu-project/variables
opentofu init
opentofu plan
```

Expected output snapshot:

```plaintext theme={null}
+ resource "local_file" "jedi" {
    + content     = "phanius"
    + filename    = "/root/first-jedi"
    ...
  }

Plan: 1 to add, 0 to change, 0 to destroy.
```

Apply the changes:

```bash theme={null}
opentofu apply
