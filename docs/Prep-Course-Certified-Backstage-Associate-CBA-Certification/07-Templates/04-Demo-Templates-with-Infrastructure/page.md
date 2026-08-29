# app-config.yaml (excerpt)
catalog:
  locations:
    - type: file
      target: ../../examples/entities.yaml

    # Local example template
    - type: file
      target: ../../examples/template/template.yaml
      rules:
        - allow: [Template]

    # Local example organizational data
    - type: file
      target: ../../examples/org.yaml
      rules:
        - allow: [User, Group]
```

The `target` above points to the example `template.yaml` that Backstage imports and lists in the Create UI.

## Minimal `template.yaml` example

A template descriptor follows the Scaffolder descriptor format. Here is a minimal cleaned `template.yaml` example:

```yaml theme={null}
apiVersion: scaffolder.backstage.io/v1beta3
# https://backstage.io/docs/features/software-catalog/descriptor-format#kind-template
kind: Template
metadata:
  name: example-nodejs-template
  title: Example Node.js Template
  description: An example template for the scaffolder that creates a simple Node.js service
spec:
  owner: user:guest
  type: service

  # Parameters define the form fields that appear in the UI.
  parameters:
    - title: Fill in some steps
      required:
        - name
      properties:
        name:
          title: Name
          type: string
          description: Unique name of the component
          ui:autofocus: true

    - title: Choose a location
      required:
        - repoUrl
      properties:
        repoUrl:
          title: Repository Location
          type: string
          ui:field: RepoUrlPicker
          ui:options:
            allowedHosts:
              - github.com
```

Parameters map directly to the Backstage form:

* `name` is a required string used as the project name.
* `repoUrl` uses the `RepoUrlPicker` UI component and restricts allowed hosts to `github.com`.

> **lightbulb** When authoring or editing template YAML and template files in MDX content, always place expressions such as `${{ parameters.name }}` or `{{ values.name }}` inside fenced code blocks or inline code backticks so MDX does not attempt to evaluate them.

## How the template executes — steps

The scaffolder runs a sequence of steps defined under `spec.steps`. A canonical Node.js blueprint flow includes:

1. Fetch the blueprint content and render it with provided values.
2. Publish the rendered files to GitHub (create repo and push).
3. Register the new service in the Backstage catalog.

A cleaned `steps` example:

```yaml theme={null}
spec:
  steps:
    # 1) Fetch the base template files and render them with provided values.
    - id: fetch-base
      name: Fetch Base
      action: fetch:template
      input:
        url: ./content
        values:
          name: ${{ parameters.name }}

    # 2) Publish rendered contents to GitHub (creates repo and pushes files).
    - id: publish
      name: Publish
      action: publish:github
      input:
        allowedHosts: ['github.com']
        description: This is ${{ parameters.name }}
        repoUrl: ${{ parameters.repoUrl }}

    # 3) Register the new component in the catalog using the published repo.
    - id: register
      name: Register
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['publish'].output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'

  # Outputs shown to the user after a successful run.
  output:
    links:
      - title: Repository
        url: ${{ steps['publish'].output.remoteUrl }}
      - title: Open in catalog
        icon: catalog
        entityRef: ${{ steps['register'].output.entityRef }}
```

Key points:

* The `fetch:template` action copies and renders files from the blueprint `./content` folder into a working directory. In this example we pass `values.name` as `name` using `name: ${{ parameters.name }}`.
* The `publish:github` action creates the repository and pushes the rendered files. It requires the `repoUrl` input derived from the UI parameter.
* The `catalog:register` action uses the `repoContentsUrl` output from the `publish` step and the `catalogInfoPath` (for example, `/catalog-info.yaml`) to register the entity in the catalog.

### Scaffolder actions at a glance

| Action             | Purpose                                                  | Key inputs / outputs                                             |
| ------------------ | -------------------------------------------------------- | ---------------------------------------------------------------- |
| `fetch:template`   | Copy and render blueprint files into a working directory | Input: `url`, `values`                                           |
| `publish:github`   | Create GitHub repo and push rendered files               | Input: `repoUrl`, output: `remoteUrl`, `repoContentsUrl`         |
| `catalog:register` | Register the new service entity in Backstage catalog     | Input: `repoContentsUrl`, `catalogInfoPath`, output: `entityRef` |

## Example blueprint content files

The blueprint `content` folder typically contains files that the scaffolder renders with template expressions.

package.json (in `content/package.json`):

```json theme={null}
{
  "name": "${{ values.name }}",
  "private": true,
  "dependencies": {
    "express": "^4.18.2"
  },
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  }
}
```

index.js (in `content/index.js`):

```javascript theme={null}
console.log('Hello from ${{ values.name }}!');
```

catalog-info.yaml (in `content/catalog-info.yaml`):

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: {{ values.name | dump }}
spec:
  type: service
  owner: user:guest
  lifecycle: experimental
```

When the scaffolder runs:

* It renders files by replacing template placeholders (e.g., `package.json`'s `name` becomes the project name entered in the UI because `${{ values.name }}` is substituted).
* The `publish` step uploads the rendered files to the created GitHub repository (using the `repoUrl` supplied by the user).
* The `register` step registers the `catalog-info.yaml` entity in the Backstage catalog using `repoContentsUrl` from the `publish` step and the `catalogInfoPath`.

## Outputs and UX

After a successful run, `template.yaml`'s `output.links` field surfaces useful links to the user:

* Repository: `steps['publish'].output.remoteUrl` — opens the newly created repo.
* Open in catalog: `steps['register'].output.entityRef` — opens the newly registered entity in Backstage.

This provides immediate access to both the code repo and the catalog entry.

## Summary

Templates let platform teams encode organizational best practices into reproducible blueprints. With only a couple of form fields, Backstage can:

* Create a new repository from a standardized blueprint,
* Render project-specific values into files,
* Publish the project to GitHub,
* Register the service in the Backstage catalog.

You can author your own templates: create content in a `content` folder, write your `template.yaml` with `spec.steps`, and test the end-to-end scaffolding flow from the Backstage Create UI.

## Links and References

* Backstage Scaffolder docs: [https://backstage.io/docs/features/software-templates/creating-templates](https://backstage.io/docs/features/software-templates/creating-templates)
* Descriptor format: [https://backstage.io/docs/features/software-catalog/descriptor-format#kind-template](https://backstage.io/docs/features/software-catalog/descriptor-format#kind-template)
* Scaffolder actions reference: [https://backstage.io/docs/features/software-templates/available-actions](https://backstage.io/docs/features/software-templates/available-actions)
* GitHub repository: [https://github.com/](https://github.com/) (for `publish:github`)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/1c7142e3-0cb6-40ae-b5b6-77252f8c85b2/lesson/a5782c98-c489-465b-9386-c4b71ed6543a)


# Demo Templates with Infrastructure

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Templates/Demo-Templates-with-Infrastructure/page

Building a Backstage scaffolder template that creates a Node.js Express app, templatizes and publishes infra and app repos, registers catalog entities, and provisions an EC2 instance with Terraform

In this lesson you'll build a Backstage scaffolder template that creates a Node.js + Express API repository and provisions the underlying infrastructure (an EC2 instance) with Terraform. The template will:

* Clone an infrastructure blueprint (Terraform code), templatize it, and publish it as a new repo.
* Register the resulting Resource entity in the Backstage catalog.
* Clone an application blueprint (Node.js + Express skeleton), templatize it, publish it as a new repo, and register the Component in the catalog.
* Wire the created Component to depend on the newly created Resource so relations appear in Backstage.

<Frame>
  <img alt="A simple architecture diagram titled &#x22;Template Demo&#x22; showing an Organization icon on the left connected to a Template box containing an API icon and the Node.js logo. An arrow leads from the template to an AWS box with a chip/processor symbol, and a &#x22;Developers&#x22; label appears below." />
</Frame>

## Flow overview

1. Platform/infrastructure teams maintain blueprint repositories:
   * `infrastructure-IAC` — core infra managed by the infra team (VPCs, shared resources).
   * `ec2-infra-blueprint` — per-app Terraform module/skeleton used by the template.
   * `backstage-express-api-blueprint` — Node.js + Express app skeleton.
2. A developer opens the Backstage template UI, supplies project metadata (name, owner, destination repo), and selects an EC2 instance size.
3. Backstage templatizes the infra blueprint, publishes it as `<repo>-infra`, and registers a Resource entity (type: `compute`).
4. Backstage templatizes the app blueprint, publishes it as `<repo>`, and registers a Component entity that declares a `dependsOn` relation to the infra Resource.
5. Terraform Cloud (or another runner) performs `terraform apply` for the new infra repo, provisioning the EC2 instance.

Below is a compact sequence illustration of these steps.

<Frame>
  <img alt="A diagram titled &#x22;Demo Steps&#x22; showing Infrastructure, Platform and Developer team icons on the left and a central form with Project Name &#x22;Demo-App&#x22; and Instance Type &#x22;t2.small.&#x22; To the right are GitHub and YAML file icons labeled repos and Template.yaml representing the infrastructure code." />
</Frame>

## Roles and repositories

Use this quick reference for which team owns which repository:

| Role / Team         | Repository                        | Purpose                                                                          |
| ------------------- | --------------------------------- | -------------------------------------------------------------------------------- |
| Infrastructure team | `infrastructure-IAC`              | Core shared Terraform state and shared resources (VPCs, subnets).                |
| Infra blueprint     | `ec2-infra-blueprint`             | Per-application Terraform skeleton/module that gets templatized.                 |
| App blueprint       | `backstage-express-api-blueprint` | Node.js + Express scaffolding used to create new services.                       |
| Template repo       | (your templates repo)             | Contains the scaffolder YAML (`nodejs-ec2-template`) that coordinates the steps. |

Example: here’s the Express API skeleton used as the app blueprint.

<Frame>
  <img alt="A screenshot of a GitHub repository page for &#x22;backstage-express-api-blueprint,&#x22; showing a list of files and folders (e.g., .github/workflows, src, tests, package.json) and repository details like branches, commits, and language stats." />
</Frame>

And this is the main organization infra repository that contains shared Terraform configuration other per-app infra will reference:

<Frame>
  <img alt="A GitHub repository webpage showing the repo header, branch info, a folder entry, and a large prompt to &#x22;Add a README&#x22; with a green button. The right sidebar displays repository stats and a language bar (HCL)." />
</Frame>

## Example infra blueprint (ec2-infra-blueprint)

The infra blueprint accepts templated inputs:

* `name` — project name used for resource naming.
* `instance_type` — EC2 size chosen by the developer.

It references the `infrastructure-IAC` remote state to obtain a subnet ID. An example main Terraform module (simplified):

```terraform theme={null}
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

data "terraform_remote_state" "core" {
  backend = "remote"

  config = {
    organization = "sanjeevkt720"
    workspaces = {
      name = "infrastructure-iac"
    }
  }
}

module "my_ec2" {
  source        = "app.terraform.io/sanjeevkt720/ec2-infra/aws"
  version       = "1.0.0"
  name          = "file-manager-service"           # to be templatized
  instance_type = "t2.micro"                      # to be templatized
  subnet        = data.terraform_remote_state.core.outputs.subnet3_id
}
```

Resource entity for the EC2 instance (`resource.yaml` in the infra blueprint):

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: file-manager-service-ec2    # to be templatized, e.g. "${{ values.name + '-ec2' }}"
  description: EC2 instance for "file-manager-service"
spec:
  type: compute
  owner: infra
```

## Template form and user experience

The template provides a multi-step Create flow in Backstage:

* Project Info — component name and metadata.
* Choose Location — repository location / owner.
* Deploy EC2 — select instance size (e.g., `t2.micro`, `t2.small`, `t2.medium`).

Example Create flow UI:

<Frame>
  <img alt="Screenshot of a web interface titled &#x22;Create a new component&#x22; for a Node.JS App on EC2, showing a multi-step progress bar (Project Info, Choose a location, Deploy EC2, Review). The form displays repository location fields (host, owner, repository name) with Back and Next buttons." />
</Frame>

Choosing an instance size:

<Frame>
  <img alt="A screenshot of a web UI titled &#x22;Create a new component&#x22; for provisioning a Node.JS app on EC2, showing progress steps and the &#x22;Deploy EC2&#x22; step. A dropdown of EC2 instance types is open with &#x22;t2.micro&#x22; highlighted and a cursor pointing at it." />
</Frame>

High-level result: the template produces two repositories:

* `file-manager-service` — application code (from the app blueprint).
* `file-manager-service-infra` — Terraform code to provision the EC2 instance (from the infra blueprint).

Backstage will display the Component and Resource relations once both entities are registered.

<Frame>
  <img alt="A web dashboard titled &#x22;user-service&#x22; showing an Overview page with an About panel (owner &#x22;dev&#x22;, lifecycle &#x22;experimental&#x22;) on the left. On the right is a Relations graph linking &#x22;dev&#x22; to &#x22;user-service&#x22; and to &#x22;user-service-ec2.&#x22;" />
</Frame>

<Frame>
  <img alt="A web dashboard page for a resource named &#x22;user-service-ec2&#x22; with an About panel describing it as an EC2 instance and links to source/techdocs. The right side shows a Relations graph illustrating dependencies between &#x22;user-service&#x22;, &#x22;infra&#x22;, and &#x22;user-service-ec2&#x22;." />
</Frame>

## Template design — parameters and ordered steps

The single scaffolder template (`nodejs-ec2-template`) will:

* Show a three-page form (project info, repo location, deploy EC2).
* Execute the following steps, in order:

  1. fetch infra base (clone `ec2-infra-blueprint` into `./infra` and provide values)
  2. publish infra (push `./infra` to a new repo `<repo>-infra`)
  3. register infra Resource (`catalog:register` using `resource.yaml`)
  4. fetch app base (clone `backstage-express-api-blueprint` into `./code` and provide values)
  5. publish app (push `./code` to `<repo>`)
  6. register app Component (`catalog:register` using `catalog-info.yaml`)
  7. provide output links (Repository, Open in Catalog)

Below is a complete example Backstage Scaffolder template. Make sure your Backstage instance has the `fetch:template`, `publish:github` and `catalog:register` actions installed and configured.

```yaml theme={null}
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: nodejs-ec2-template
  title: Node.JS App on EC2
  description: A template for provisioning a Node.js app and an EC2 instance via Terraform
spec:
  owner: user:guest
  type: service

  parameters:
    - title: Project Info
      required:
        - name
      properties:
        name:
          title: Name
          type: string
          description: Unique name of the component
          ui:autofocus: true

    - title: Choose Location
      required:
        - repoUrl
      properties:
        repoUrl:
          title: Repository Location
          type: string
          ui:field: RepoUrlPicker
          ui:options:
            allowedHosts:
              - github.com
        owner:
          title: Owner
          type: string
          description: Owner of the component
          ui:field: OwnerPicker
          ui:options:
            catalogFilter:
              - kind: [User, Group]

    - title: Deploy EC2
      properties:
        instanceType:
          title: Instance Type
          type: string
          description: What size EC2 instance
          default: "t2.micro"
          enum:
            - "t2.micro"
            - "t2.small"
            - "t2.medium"

  steps:
    # 1) Fetch and templatize infrastructure skeleton into ./infra
    - id: fetch-infra-base
      name: Fetch Infrastructure base
      action: fetch:template
      input:
        url: https://github.com/Sanjeev-Thiyagarajan/ec2-infra-blueprint
        targetPath: ./infra
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}
          instanceType: ${{ parameters.instanceType }}

    # 2) Publish infra (push ./infra to repoUrl + "-infra")
    - id: publish-infra
      name: Publish Infrastructure
      action: publish:github
      input:
        sourcePath: ./infra
        repoUrl: ${{ parameters.repoUrl }}-infra
        description: This is ${{ parameters.name }}-infra
        allowedHosts: ["github.com"]

    # 3) Register resource created by infra (resource.yaml)
    - id: register-infra
      name: Register Infrastructure Resource
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['publish-infra'].output.repoContentsUrl }}
        catalogInfoPath: /resource.yaml

    # 4) Fetch and templatize app skeleton into ./code
    - id: fetch-app-base
      name: Fetch App base
      action: fetch:template
      input:
        url: https://github.com/Sanjeev-Thiyagarajan/backstage-express-api-blueprint
        targetPath: ./code
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}

    # 5) Publish app (push ./code to repoUrl)
    - id: publish-app
      name: Publish App
      action: publish:github
      input:
        sourcePath: ./code
        repoUrl: ${{ parameters.repoUrl }}
        description: This is ${{ parameters.name }}
        allowedHosts: ["github.com"]

    # 6) Register the app component (catalog-info.yaml)
    - id: register-app
      name: Register App
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['publish-app'].output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml

  output:
    links:
      - title: Repository
        url: ${{ steps['publish-app'].output.remoteUrl }}
      - title: Open in Catalog
        url: ${{ steps['register-app'].output.entityRef }}
```

## Templatizing blueprints — key snippets

Infra blueprint: replace placeholders in `main.tf` and `resource.yaml` with scaffolder values. Example module block (templated):

```terraform theme={null}
module "my_ec2" {
  source        = "app.terraform.io/sanjeevkt720/ec2-infra/aws"
  version       = "1.0.0"
  name          = "${{ values.name }}"
  instance_type = "${{ values.instanceType }}"
  subnet        = data.terraform_remote_state.core.outputs.subnet3_id
}
```

Templatized `resource.yaml`:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: "${{ values.name + '-ec2' }}"
  description: EC2 instance for "${{ values.name }}"
spec:
  type: compute
  owner: infra
```

App blueprint: update `catalog-info.yaml` so the Component depends on the infra Resource:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: ${{ values.name | dump }}
spec:
  type: service
  owner: ${{ values.owner }}
  lifecycle: experimental
  dependsOn:
    - "${{ 'resource:' + values.name + '-ec2' }}"
```

## Note about Terraform execution

> **lightbulb** This example uses Terraform Cloud to detect new infra repositories and run `terraform apply`. If you do not use Terraform Cloud (or a similar runner), you must add an extra step that runs Terraform (for example, a CI workflow or a scaffolder action that executes `terraform init` and `terraform apply`) after publishing the infra repository.

## Running the template

* Add the `nodejs-ec2-template` YAML to your templates repo and let Backstage pick it up.
* From the Backstage Create flow, select *Node.js App on EC2*, fill out project name, owner, repo location, and instance type, then run the template.
* The template creates two Git repositories: `<repo>` (app) and `<repo>-infra` (Terraform).
* Catalog registration will create a Component entity for the app and a Resource entity for the EC2 instance. The Component will declare a `dependsOn` relation to the Resource.

Example run completion UI:

<Frame>
  <img alt="A screenshot of a web dashboard showing a completed &#x22;Run of nodejs-ec2-template&#x22; with a horizontal progress bar of steps (Fetch Infrastructure base, Publish Infrastructure, Register, Fetch App Base, Publish App, Register App) each marked complete. There are buttons for &#x22;Repository&#x22; and &#x22;Open in Catalog&#x22; and a green mouse cursor pointing near the first step." />
</Frame>

## Post-run verification

* Confirm the two GitHub repositories were created:
  * `file-manager-service` — app skeleton with templated `catalog-info.yaml`.
  * `file-manager-service-infra` — contains `main.tf` with `name` and `instance_type` set according to inputs.
* In Backstage catalog, inspect the Component and Resource entities. The Component should depend on the `file-manager-service-ec2` Resource and relations should be visible.

Example GitHub profile with created repos:

<Frame>
  <img alt="A screenshot of a GitHub profile page for &#x22;Sanjeev Thiyagarajan&#x22; with a large circular avatar on the left. The right side lists repositories (e.g., file-manager-service, user-service) with language tags, privacy labels, and star buttons." />
</Frame>

Example resource and relation in Backstage:

<Frame>
  <img alt="Screenshot of a web dashboard for a resource titled &#x22;file-manager-service-ec2.&#x22; The page shows an About panel (noting &#x22;EC2 instance for 'myapp'&#x22;) and a Relations graph linking the entity to &#x22;file-manager-service&#x22; and &#x22;infra.&#x22;" />
</Frame>

If Terraform Cloud (or your runner) performs the apply, you should see a running EC2 instance in AWS:

<Frame>
  <img alt="A screenshot of the AWS EC2 Instances console showing one running instance named &#x22;file-manager-service&#x22; (t2.micro) with 2/2 status checks passed. The left navigation pane lists EC2 sections like Instances, Images, and Elastic Block Store." />
</Frame>

## Summary and next steps

* This pattern connects repository templating, GitHub publishing, Backstage catalog registration, and infrastructure provisioning.
* You can extend it to provision other resource types (databases, load balancers, clusters) by creating additional infra blueprints and wiring them into the template steps.
* Decide where Terraform should run (Terraform Cloud, CI runner, or a Backstage action) and update the scaffolder actions accordingly.

Useful links and references:

* [Backstage](https://backstage.io/)
* [Terraform Cloud](https://www.terraform.io/cloud)
* [Terraform documentation](https://www.terraform.io/docs)
* [Node.js](https://nodejs.org/)
* [Express](https://expressjs.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/1c7142e3-0cb6-40ae-b5b6-77252f8c85b2/lesson/5cb603dc-208b-45f1-911b-2a7c443208f1)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/1c7142e3-0cb6-40ae-b5b6-77252f8c85b2/lesson/ef1d61cc-154f-43f3-ada0-3f6c1df79970)
