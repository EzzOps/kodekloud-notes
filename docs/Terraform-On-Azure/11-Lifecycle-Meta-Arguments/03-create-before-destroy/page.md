# create before destroy

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Lifecycle-Meta-Arguments/create-before-destroy/page

Explains Terraform's create_before_destroy lifecycle setting enabling zero downtime replacements with Azure guidance on naming, indirection, coexistence, and migration strategies.

This lesson explains the Terraform lifecycle meta-argument `create_before_destroy`, how it changes replacement ordering, and what to consider when using it with Azure to support zero-downtime deployments.

What `create_before_destroy` does

* By default, Terraform replaces resources using a destroy-then-create sequence. Enabling `create_before_destroy` reverses that order: Terraform will create the replacement resource first, then destroy the original.
* This approach lets the original resource remain available while the new one is provisioned, reducing the risk of outages or broken dependents.
* It enables blue/green, canary, and other parallel-deployment patterns where both old and new resources coexist briefly and traffic is switched only after verification.

Key effects (at-a-glance)

| Effect                                             | Why it matters                                                                    |
| -------------------------------------------------- | --------------------------------------------------------------------------------- |
| Creates replacement before destroying the original | Minimizes downtime and prevents mid-replacement outages                           |
| Old and new resources coexist temporarily          | Enables verification and traffic-switching strategies (blue/green, canary)        |
| Requires resources to be able to coexist           | May need different names, addresses, or an indirection layer (DNS, load balancer) |

Example lifecycle configuration (HCL)

```hcl theme={null}
resource "azurerm_public_ip" "example" {
  name                = "example-pip"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  allocation_method   = "Static"

  lifecycle {
    create_before_destroy = true
  }
}
```

<Callout icon="lightbulb">
  Use `create_before_destroy` when you design for parallel resources (for example, blue/green deployments) and can ensure the replacement can be created alongside the existing resource. This may require versioned naming, DNS indirection, or a load-balancer swap strategy.
</Callout>

Azure-specific considerations

* Many Azure resources support in-place updates for most properties. Because Azure often updates resources in place, Terraform's default destroy-then-create behavior combined with Azure's update model is usually sufficient and simpler.
* Some Azure services enforce globally unique names (for example, storage account names, CDN endpoint names) or unique DNS labels. If a name or label must be unique, you cannot create a new resource with the same identifier while the old one still exists.
* To use `create_before_destroy` effectively on Azure you usually need one or more of the following:
  * Versioned or suffixed names so two resources can coexist (for example, `app-v1`, `app-v2`).
  * An indirection layer such as DNS, Traffic Manager, or an Application Gateway/load balancer to switch traffic after the new resource is ready.
  * A migration or synchronization plan for stateful resources (databases, storage) so data is consistent between versions.

Common patterns and mitigations

|                        Constraint | Impact when using `create_before_destroy`                                     | Typical mitigation                                                    |
| --------------------------------: | ----------------------------------------------------------------------------- | --------------------------------------------------------------------- |
|             Globally-unique names | Replacement creation will fail if it uses the same unique identifier          | Use versioned names or an indirection layer (DNS, load balancer)      |
| Public IP or DNS label collisions | Cannot provision parallel public endpoints with identical addresses or labels | Allocate additional addresses/labels and switch traffic via DNS or LB |
|                 Stateful services | Coexistence requires data synchronization or replication                      | Use replication, backups, or a migration plan before cutover          |

<Callout icon="warning">
  Some Azure resources require globally unique names or DNS labels. Attempting to create a replacement with the same unique identifier will fail because Azure does not allow two resources or DNS labels with the same identifier to coexist.
</Callout>

Best practices

* Favor Terraform’s default behavior for simple updates; use `create_before_destroy` only when your architecture supports parallel instances.
* Design naming conventions and indirection early (DNS, load balancer, feature flags) so replacements can coexist without collisions.
* Test replacement flows in a staging environment that mirrors production constraints (naming, quotas, IP limits).
* Document the cutover steps and rollback plan for each resource type that will be replaced using `create_before_destroy`.

References and further reading

* [Terraform Lifecycle Meta-Argument: create\_before\_destroy](https://www.terraform.io/docs/language/meta-arguments/lifecycle.html)
* [Azure Resource Manager documentation](https://learn.microsoft.com/azure/azure-resource-manager/)
* [Designing for zero-downtime deployments on Azure](https://learn.microsoft.com/azure/architecture/best-practices/availability)

With that, this lesson concludes.

<Frame>
  <img alt="The image explains the benefits of a process that first creates a new version before destroying the old one, helping avoid downtime and broken dependencies, and is useful for zero-downtime deployments." />
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/82cd6352-f026-4f6f-b739-634e56558de4/lesson/6ffef105-43c5-4dfc-914b-a15e10beeda3" />
</CardGroup>
