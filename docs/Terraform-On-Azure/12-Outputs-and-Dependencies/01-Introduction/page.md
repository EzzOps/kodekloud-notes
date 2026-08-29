# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Outputs-and-Dependencies/Introduction/page

Explains how Terraform shares data between resources, manages dependencies, uses targeting cautiously, and exposes important values via outputs for composing modules and debugging.

In this lesson we move beyond creating individual Terraform resources and focus on how Terraform connects them and shares information between them. Understanding these concepts helps you build reliable, maintainable infrastructure-as-code that scales.

We'll cover four core topics:

* How resource attributes work, and how values produced by one resource can be referenced by another.
* Resource dependencies: how Terraform infers them automatically, and when you must declare dependencies explicitly.
* Resource targeting: what it does and why it should be used sparingly.
* How to define and use output variables to expose important values from our Terraform configuration.

<Frame>
  <img alt="The image shows an agenda with four points related to Terraform, including understanding resource attributes, managing dependencies, using targeting, and defining output variables." />
</Frame>

<Callout icon="lightbulb">
  This lesson explains how Terraform passes data between resources, controls the order of operations, and surfaces useful values through outputs. These are essential for composing modules, integrating with other tools, and debugging your plans.
</Callout>

## What you'll learn (quick overview)

| Topic                 | Why it matters                                                         | Outcome                                              |
| --------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------- |
| Resource attributes   | Attributes expose produced values (IDs, endpoints, IPs) from resources | Reference attributes to wire resources together      |
| Resource dependencies | Ensures resources are created in the correct order                     | Avoids race conditions and configuration drift       |
| Targeting resources   | Lets you apply or destroy select resources                             | Use only for debugging or emergency fixes            |
| Output variables      | Surface important values to users or external systems                  | Export endpoints, connection strings, and IDs safely |

## Links and references

* [Terraform: Expressions and Attributes](https://www.terraform.io/docs/language/expressions/index.html)
* [Terraform: Resource Dependencies](https://www.terraform.io/docs/language/expressions/references.html#implicit-and-explicit-dependencies)
* [Terraform: Outputs](https://www.terraform.io/docs/language/values/outputs.html)

<Callout icon="warning">
  Resource targeting (using `-target`) can break dependency graphs and lead to drift. Only use targeting for troubleshooting or carefully planned changes.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/866718d2-695e-4ee4-b25d-1aab3b014e85/lesson/7bb1e0ce-6002-4bab-bf5b-c70d3f252d56" />
</CardGroup>
