# Custom Modules vs Community Modules

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Modules/Custom-Modules-vs-Community-Modules/page

This article explores the benefits and trade-offs of using Community modules versus building Custom modules in Terraform.

In this lesson, we’ll explore the benefits and trade-offs of using Community modules versus building Custom modules from scratch in Terraform. Mickey faces this choice on his project: should he leverage pre-built solutions or invest time crafting bespoke infrastructure components?

***

## The Dilemma

Community modules deliver speed and convenience with battle-tested building blocks for common infrastructure patterns. Custom modules, by contrast, give you full control and tailorability but demand more time and expertise. Is there a strategy that combines the best of both worlds?

***

## Custom Modules

Custom modules are developed in-house to address project-specific requirements and constraints. Key advantages include:

* **Full Control**\
  Define every variable, output, and resource to match exact specifications.

* **Tailored Fit**\
  Align module behavior with your organization’s unique infrastructure needs and policies.

* **Ownership & Governance**\
  Teams retain authority over updates, security audits, and versioning.

### When to Choose Custom Modules

* You require specialized configurations not covered by existing modules.
* Strict compliance with internal security or regulatory standards is mandatory.
* You need seamless integration with legacy systems or proprietary tooling.

### Example: Simple Custom Module Structure

```bash theme={null}
my-terraform-project/
├── modules/
│   └── custom_vpc/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    └── prod/
        └── main.tf
```

```hcl theme={null}
