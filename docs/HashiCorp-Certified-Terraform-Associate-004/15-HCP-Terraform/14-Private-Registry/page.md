# Private Registry

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/HCP-Terraform/Private-Registry/page

Explains HCP Terraform Private Registry, its purpose, features, versioning, publishing workflow, private and curated modules, and how to reference organization scoped modules in Terraform.

In this lesson we’ll cover the HCP Terraform Private Registry: what it is, why it exists, and how teams use it to share versioned, organization-specific Terraform modules and providers.

Why modules matter

* Teams create reusable Terraform modules to standardize common infrastructure patterns (TLS certificates, load balancers, message queues, Kubernetes clusters, databases).
* Modules let application teams consume tested building blocks instead of reimplementing infrastructure logic, reducing risk and accelerating delivery.
* Modules also enable consistency across teams while allowing environment-specific inputs.

For example, a marketing app team can consume a TLS certificate, load balancer, and Kubernetes cluster module without reimplementing them.

<Frame>
  <img alt="The image is a diagram outlining &#x22;Modules for Repeatability&#x22; within a &#x22;Marketing Application,&#x22; listing modules like TLS Certificate, Load Balancer, Message Queuing, Kubernetes Cluster, and Database Cluster." />
</Frame>

Another team building a GenAI service can reuse the same modules with different inputs — demonstrating the "write once, use everywhere" value of modules.

<Frame>
  <img alt="The image illustrates a modular framework for repeatability, depicting a central module block that provides infrastructure components like TLS Certificate, Load Balancer, and Kubernetes Cluster, connected to both a Marketing Application and a GenAI Service." />
</Frame>

Versioning matters

* Modules evolve (for example: 5.10.0 → 5.11.0 → 5.12.0). With many consumers, semantic versioning is essential so teams can pin versions and upgrade on their own schedule.
* The public Terraform Registry offers browsable versions and docs, but it is public. For internal, security-sensitive, or compliance-driven modules you need a private, organization-scoped solution.

What the HCP Terraform Private Registry provides

* Private sharing of modules and providers — visible only to members of your HCP Terraform organization.
* Semantic versioning and version constraints equivalent to the public registry.
* A way to enforce standards by publishing approved, tested, and secure modules for team consumption.

Below is a quick comparison (for quick scanning) followed by an illustrative image.

| Area                  | Public Registry              | HCP Terraform Private Registry                                    |
| --------------------- | ---------------------------- | ----------------------------------------------------------------- |
| Hosting / visibility  | Publicly visible to everyone | Scoped to your HCP Terraform organization (requires credentials)  |
| Who can publish       | Any community member         | Only approved organization members via connected VCS repos        |
| Typical content       | Community-maintained modules | Organization-private modules + curated public modules you approve |
| Source address format | `namespace/name/provider`    | `app.terraform.io/<ORG>/<MODULE_NAME>/<PROVIDER>`                 |

<Frame>
  <img alt="The image is a comparison table between a public and private registry, highlighting differences in hosting, visibility, content publishing, and source format within the context of Terraform." />
</Frame>

Key distinctions explained

* Hosting/visibility: Public registry = global visibility; Private registry = organization-scoped visibility with access control.
* Publishing: Public = open publishing; Private = controlled publishing from connected VCS repositories by authorized maintainers.
* Content: Private registry aggregates your internal modules and any curated public modules you choose to expose for team discovery.
* Source format: Private modules include the hostname prefix so Terraform queries your private registry: `app.terraform.io/<ORG>/<MODULE_NAME>/<PROVIDER>`.

What lives inside a private registry?
There are two main categories:

1. Private modules and providers — authored and maintained in your organization’s connected VCS repositories and surfaced only to organization members.
2. Curated public modules — pointers or mirrored entries for vetted public registry modules, so teams can find both internal and approved external modules in one place.

<Frame>
  <img alt="The image explains what is inside a private registry, featuring &#x22;Private Modules & Providers&#x22; and &#x22;Curated Public Modules&#x22; with brief definitions for each." />
</Frame>

How modules get into the private registry
Publishing to the Private Registry is a simple three-step flow:

1. Develop and commit the module code to a VCS repository (GitHub, GitLab, Bitbucket, Azure DevOps, etc.) using the standard Terraform module layout (README, inputs, outputs, examples).
2. Connect that repository to your HCP Terraform organization and publish it to the Private Registry. HCP Terraform imports the module metadata and generates browsable docs.
3. Create new module versions by pushing semantic Git tags (for example, `1.0.0`, `1.1.0`); the registry automatically creates version entries from those tags.

Once published, organization members can browse module docs, copy usage snippets, and reference the modules in Terraform configurations.

<Frame>
  <img alt="The image outlines three steps for publishing private modules in Terraform: storing module code in a VCS repo, publishing to HCP Terraform, and enabling organization members to use the modules." />
</Frame>

Referencing a private module in your configuration
Private registry module source addresses include the registry hostname so Terraform knows to query your organization’s registry instead of the public one. Use the following source format:

`app.terraform.io/<ORG>/<MODULE_NAME>/<PROVIDER>`

Example HCL module block:

```hcl theme={null}
module "webapp" {
  source  = "app.terraform.io/krausen-hcp/webapp/gcp"
  name    = var.name
  prefix  = var.prefix
  version = "1.0.0"
}
```

* `app.terraform.io` — hostname indicating the private registry
* `krausen-hcp` — organization name
* `webapp` — module name
* `gcp` — provider
* `version` — pins the module to a specific released version

Everything else works the same as public modules: pass variables, Terraform downloads the module source, and the module is included in plan/apply. If you see a source beginning with `app.terraform.io`, it’s a private registry module.

> **lightbulb** The private registry auto-creates module versions when you push semantic Git tags (for example, `1.0.0`). Ensure your repository follows the standard Terraform module layout so the registry can detect and import it correctly.

Key takeaways

* The HCP Terraform Private Registry lets you share modules and providers privately within your organization, maintaining access control and governance.
* You can curate approved public modules and surface them next to your private modules to create a single source of truth for teams.
* Private modules are published from connected VCS repositories and are versioned automatically via semantic Git tags.
* Private module source addresses include the hostname prefix `app.terraform.io` so Terraform queries your private registry.
* Publishing to the Private Registry requires the "Manage Private Registry" permission — limit this to trusted maintainers.

> **warning** Publishing modules to the private registry requires the Manage Private Registry permission. Ensure only trusted maintainers have this permission to prevent unauthorized module publication.

That wraps up this lesson on the HCP Terraform Private Registry. Keep these concepts in mind when designing a module publishing workflow for your organization or preparing for certification exams.

Links and references

* [Terraform Registry — Private Module Sources](https://www.terraform.io/docs/registry/private/index.html)
* [Semantic Versioning](https://semver.org/)
* [GitHub](https://github.com) | [GitLab](https://gitlab.com) | [Bitbucket](https://bitbucket.org) | [Azure DevOps](https://dev.azure.com)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/110bee15-3e45-411c-a55c-e8dfff73d23a/lesson/601a5d5e-5856-45e8-ade3-8bae5df02fc9)
