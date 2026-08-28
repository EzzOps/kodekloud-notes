# Resources vs Data Sources

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Data-Sources/Resources-vs-Data-Sources/page

Comparison of Terraform resources versus data sources, explaining roles, lifecycle differences, examples, and guidance on when to create managed resources or perform read-only lookups of existing infrastructure.

In Terraform, understanding the difference between resources and data sources is essential for predictable infrastructure as code. While they can look similar in HCL syntax, their roles, lifecycle behaviors, and impacts on state differ. This guide compares both, shows examples, and gives guidance on when to use each.

Why this matters: resources are objects Terraform creates and manages (tracked in state), whereas data sources are read-only lookups that retrieve information about infrastructure that Terraform does not own.

## Key differences at a glance

| Aspect            | Resource                                                           | Data Source                                                                           |
| ----------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| Keyword           | `resource`                                                         | `data`                                                                                |
| Primary action    | Creates, updates, destroys infrastructure                          | Reads existing infrastructure attributes                                              |
| Typical use case  | Manage objects Terraform should own (VMs, VNets, storage accounts) | Look up IDs/attributes of existing objects (VNet ID, AMI ID, subscription info)       |
| Lifecycle & state | Tracked in Terraform state; part of plan/apply lifecycle           | Not created/managed; fetched during planning/apply but not tracked as managed objects |
| Alternate term    | Managed resource                                                   | Data resource / lookup                                                                |

<Frame>
  <img alt="The image is a comparison table between &#x22;Resource&#x22; and &#x22;Data Source&#x22; in Terraform, detailing differences in keywords, functionality, infrastructure management, lifecycle involvement, and alternate names." />
</Frame>

Data sources only provide information about existing infrastructure; they do not modify or take ownership of it. Resources, by contrast, are owned and managed by Terraform.

<Callout icon="lightbulb">
  Use resources when Terraform should own the lifecycle of an object. Use data sources when you only need to look up existing information (for example, a VNet ID or an AMI ID).
</Callout>

## Examples (syntactic comparison)

resource example — Terraform will create and manage this virtual network:

```hcl theme={null}
