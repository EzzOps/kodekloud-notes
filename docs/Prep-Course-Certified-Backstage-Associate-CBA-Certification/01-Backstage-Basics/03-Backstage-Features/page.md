# Stop the server (Ctrl+C in most terminals), then restart:
yarn dev
```

## Quick reference table

| Config file                  | Purpose                                 | Notes                                                                  |
| ---------------------------- | --------------------------------------- | ---------------------------------------------------------------------- |
| `app-config.yaml`            | Base configuration for all environments | Commit to repository; contains shared settings                         |
| `app-config.local.yaml`      | Local development overrides             | Only include keys that differ locally; do not commit secrets           |
| `app-config.production.yaml` | Production overrides                    | Reference environment variables for secrets and deploy-specific values |

## Summary

* `app-config.yaml` is the shared base config; commit this file.
* `app-config.local.yaml` provides local development overrides—keep sensitive values out of version control.
* `app-config.production.yaml` contains production-specific overrides and should rely on environment variables for secrets.
* Backstage merges the base and override files at startup; restart the process to load configuration changes.

Further reading and references:

* [Backstage Configuration documentation](https://backstage.io/docs/features/configuration)
* [YAML specification](https://yaml.org/spec/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/fcbbf923-69c3-4147-bd51-18db2bd18957/lesson/548b4bbc-0a5c-4d63-94ee-250dfd40cd25" />
</CardGroup>


# Backstage Features

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Backstage-Basics/Backstage-Features/page

Overview of Backstage, an open source React and Node.js framework for building extensible internal developer portals with catalog, scaffolding templates, TechDocs, unified search, and plugin architecture

Backstage is an open-source framework for building Internal Developer Portals (IDPs). It stands out because of its open-source community, familiar technology stack, and a plugin-first architecture that makes it highly extensible and easy to customize.

<Frame>
  <img alt="A slide titled &#x22;Backstage – Introduction&#x22; showing an orange circle labeled &#x22;IDP&#x22; with arrows pointing to three web-page icons below and a stacked logo above. It visually represents an IDP distributing to multiple applications." />
</Frame>

Key technical choices:

* Frontend: React
* Backend: Node.js (Express-based server)
  This combination means most JavaScript developers can extend and customize Backstage with minimal ramp-up.

<Frame>
  <img alt="A slide titled &#x22;Backstage – Benefits&#x22; showing a central Backstage logo connected to React (Frontend Library) on the left and Node.js (Backend Library) on the right. Labels above and below read &#x22;Open source&#x22; and &#x22;Highly customizable.&#x22;" />
</Frame>

Out of the box, Backstage includes several core capabilities that are essential for an IDP:

* Software catalog (inventory of services, packages, APIs, applications)
* Scaffolding templates for consistent project creation
* Built-in documentation via TechDocs
* Unified, extensible search across catalog and docs
* Plugin-based architecture (modular features and integrations)

Below we examine each of these features in detail.

Software catalog

The software catalog centralizes your organization’s software entities and metadata: owners, lifecycle (production/staging), type, and relationships. It enables navigation from a component to its documentation, owners, and dependent services.

<Frame>
  <img alt="A screenshot of a software catalog UI titled &#x22;example-website,&#x22; showing an About panel with metadata (owner, lifecycle, type) on the left and a Relations panel on the right with a small graph of connected components." />
</Frame>

Backstage can automatically parse entity metadata (YAML descriptors) and generate a relations graph that surfaces dependencies and service ownership. This improves incident response, impact analysis, and governance.

Templating (Scaffolding)

Backstage templates automate the repetitive steps of new-project onboarding: creating repositories, adding CI/CD, scaffolding code, applying linters and tests, provisioning infrastructure, and granting access. Templates enforce standards and reduce manual setup time.

<Frame>
  <img alt="A presentation slide titled &#x22;Out-of-the-Box Features – Templates&#x22; that highlights &#x22;Standardization&#x22; and lists three bullet points about templates helping consistency, onboarding, and smoother transitions. The right side features a decorative turquoise curved path graphic with a circular accent." />
</Frame>

You can author templates per language, framework, or deployment pattern (Node.js, Java, Python, React, microservices with API gateways, etc.). Developers simply complete a short form (name, owner, repo, target platform) to scaffold a project.

<Frame>
  <img alt="A presentation slide titled &#x22;Out-of-the-Box Features – Templates&#x22; showing several service template cards (Example Node.js, Java, nodejs api w/ api-gateway, Python, React) with &#x22;choose&#x22; buttons and user:guest icons." />
</Frame>

Example: a Python template wizard where the user selects the compute platform (EC2/ECS/EKS/Lambda), fills metadata, and clicks scaffold.

<Frame>
  <img alt="A UI screenshot titled &#x22;Out-of-the-Box Features – Templates&#x22; showing a &#x22;Python Template&#x22; setup wizard with a four-step progress bar (Fill in some steps, Choose a location, Deploy, Review) and &#x22;ec2&#x22; listed as the compute platform. Navigation &#x22;BACK&#x22; and &#x22;NEXT&#x22; buttons appear at the bottom." />
</Frame>

Under the hood, templates can:

* Create a `GitHub` repository populated with an initial codebase that follows organizational best practices.
* Add CI/CD configuration, linters, and developer tooling.
* Optionally provision and deploy to infrastructure (for example, EC2).

<Frame>
  <img alt="A slide titled &#x22;Out-of-the-Box Features — Templates&#x22; showing a GitHub logo and a &#x22;New Repository created&#x22; icon. An arrow leads to an AWS EC2 chip icon and a rocket icon labeled &#x22;Deploys the application,&#x22; illustrating an automated deployment workflow." />
</Frame>

Templates are flexible and can be customized for organization-specific frameworks like Next.js, Laravel, Django, or any internal stack.

Documentation (TechDocs)

Backstage surfaces documentation close to the code using the TechDocs plugin. The recommended pattern is to keep docs in the same repository (e.g., a `docs/` folder or `README.md`). TechDocs uses MkDocs to convert Markdown into browsable HTML that Backstage renders inline.

<Frame>
  <img alt="A screenshot of a web UI titled &#x22;Out-of-the-Box Features – Docs&#x22; showing a component/service page for &#x22;shopping-cart.&#x22; The page displays Overview tabs, an About panel with &#x22;View Techdocs&#x22; and metadata (description, owner, lifecycle, tags) and a Relations panel." />
</Frame>

<Callout icon="lightbulb">
  TechDocs typically uses MkDocs (for example with the mkdocs-material theme). Projects must include standard MkDocs configuration (like `mkdocs.yml`) and Markdown files in the repo for Backstage to render the documentation.
</Callout>

Recommended examples to include in your repo:

README example:

```markdown theme={null}
This service handles shopping cart operations.

## Endpoints

- `GET /cart/{id}` — Retrieve a cart
- `POST /cart` — Create a cart
```

Small JavaScript example in the same repo:

```javascript theme={null}
function add(a, b) {
  return a + b;
}

console.log(add(2, 3)); // 5
```

Search

Backstage provides a unified, extensible search index that can include:

* Catalog entities and metadata
* TechDocs content (rendered Markdown)
* External content via integrations (Confluence, Stack Overflow, vendor data sources)

This lets developers find services, docs, and knowledge from a single interface.

<Frame>
  <img alt="A presentation slide titled &#x22;Out-of-the-Box Features – Search&#x22; showing a teal stacked-logo on the left and a blue search ribbon with icons for Search, Catalog, and Docs on the right. The slide is branded with a small &#x22;© Copyright KodeKloud&#x22; in the bottom-left." />
</Frame>

Plugins

Plugins are Backstage’s primary extension mechanism. Core features (catalog, templates, TechDocs, search) are implemented as plugins, and all new integrations follow the same pattern. Plugins fetch data, transform it, and render UI components.

<Frame>
  <img alt="A screenshot of a software UI titled &#x22;Out-of-the-Box Features – Plugins&#x22; showing a grid of dark-themed plugin cards. Each card has an icon, a short description (e.g., APIs with 3scale, AI Assistant, Airbrake, analytics modules) and an &#x22;Explore&#x22; button." />
</Frame>

You can:

* Install community and vendor plugins
* Build custom plugins to integrate internal systems (monitoring, billing, ticketing)
* Replace core functionality by swapping or extending the corresponding plugin

Feature Summary

| Feature                 | Purpose                                    | Examples / Notes                              |
| ----------------------- | ------------------------------------------ | --------------------------------------------- |
| Software catalog        | Central inventory of software and metadata | Ownership, lifecycle, relations graph         |
| Templates (Scaffolding) | Standardized project creation              | Repo creation, CI/CD, infra provisioning      |
| TechDocs                | Inline documentation rendering             | MkDocs-based, keep docs with code             |
| Search                  | Unified discovery across catalog and docs  | Integrations for Confluence, external sources |
| Plugins                 | Extensible architecture for integrations   | Community, vendor, and custom plugins         |

Links and references

* Backstage website: [https://backstage.io](https://backstage.io)
* Backstage documentation: [https://backstage.io/docs](https://backstage.io/docs)
* MkDocs: [https://www.mkdocs.org/](https://www.mkdocs.org/)
* mkdocs-material theme: [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
* GitHub: [https://github.com](https://github.com)
* Confluence: [https://www.atlassian.com/software/confluence](https://www.atlassian.com/software/confluence)
* Stack Overflow: [https://stackoverflow.com](https://stackoverflow.com)

Summary

Backstage is an open-source framework for building internal developer portals (IDPs). It uses a familiar stack (React + Node.js), provides essential features out of the box (software catalog, templates, TechDocs, search), and uses a plugin-based architecture so you can extend or replace functionality consistently and modularly.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/fcbbf923-69c3-4147-bd51-18db2bd18957/lesson/e41823d1-f7ba-4b00-babc-aa7df827f09e" />
</CardGroup>
