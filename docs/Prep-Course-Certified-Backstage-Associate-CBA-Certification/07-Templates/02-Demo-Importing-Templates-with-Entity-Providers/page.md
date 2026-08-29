# Playground example showing two parameter pages and a single fetch step
parameters:
  - title: Fill in some steps
    required:
      - name
    properties:
      name:
        title: Name
        type: string
        description: Unique name of the component
      owner:
        title: Owner
        type: string
        description: Owner of the component
        ui:field: OwnerPicker
        ui:options:
          catalogFilter:
            kind: Group
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

steps:
  - id: fetch-base
    name: Fetch Base
    action: fetch:template
```

> **warning** The Template Form Playground validates as you type and can show transient validation errors. If you see unexpected errors, edit the YAML in an external editor and paste it back into the playground.

## Create the actual template file (api-template.yaml)

Below is a consolidated, working example of a scaffolder Template for a Node.js Express API. Important notes:

* Use parameter names without hyphens (e.g., prefer `name` over `project-name`).
* The `fetch:template` step downloads a skeleton and applies `values` to files in the skeleton.
* `publish:github` needs repository creation permissions on the GitHub token configured in Backstage.
* `catalog:register` needs the `catalog-info.yaml` path inside the new repo.

```yaml theme={null}
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: api-express-template
  title: Node.JS API w/ express.js
  description: A template for provisioning APIs with Express.JS
spec:
  owner: user:guest
  type: service

  parameters:
    - title: Project Info
      required:
        - name
        - owner
      properties:
        name:
          title: Name
          type: string
          description: Unique name of the component
          ui:autofocus: true
        owner:
          title: Owner
          type: string
          description: Owner of the component
          ui:field: OwnerPicker
          ui:options:
            catalogFilter:
              kind: [User, Group]

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

  # Steps executed by the scaffolder backend
  steps:
    - id: fetch-base
      name: Fetch Base
      action: fetch:template
      input:
        # URL of the skeleton repository or a relative path (if the template bundle contains the skeleton)
        url: https://github.com/Sanjeev-Thiyagarajan/backstage-express-api-blueprint
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}

    - id: publish
      name: Publish
      action: publish:github
      input:
        allowedHosts: ["github.com"]
        description: ${{ parameters.name }}
        repoUrl: ${{ parameters.repoUrl }}

    - id: register
      name: Register
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'

  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
      - title: Open in Catalog
        icon: catalog
        entityRef: ${{ steps.register.output.entityRef }}
```

### Notes about the template and skeleton

* `fetch:template` downloads a skeleton and applies templating replacements using `values`.
* Provide `values` for each placeholder used inside the skeleton (e.g., package.json, catalog-info.yaml).
* Avoid hyphens in parameter names to prevent parsing ambiguities.
* Ensure the GitHub token used by Backstage has repository creation and workflow write permissions if your skeleton includes GitHub Actions.

Fetch template docs (reference image):

<Frame>
  <img alt="A screenshot of the Backstage web UI showing documentation for fetch actions (including &#x22;fetch:template&#x22;), with input parameter tables, descriptions and examples. A dark left sidebar displays navigation items like Search, Home, APIs, Docs and a highlighted Create button." />
</Frame>

## Make the skeleton template-ready

Replace hard-coded values in the skeleton repo with templating placeholders so the scaffolder can inject values at runtime.

package.json (template-ready):

```json theme={null}
{
  "name": "${{ values.name }}",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "jest",
    "test:ci": "jest --ci",
    "dev": "nodemon src/index.js",
    "format": "prettier --write",
    "format:check": "prettier --check",
    "lint": "eslint .",
    "lint:fix": "eslint --fix ."
  },
  "type": "module",
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "nodemon": "^2.0.20",
    "prettier": "^2.8.8",
    "eslint": "^9.17.0"
  }
}
```

catalog-info.yaml (template-ready):

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: ${{ values.name | dump }}
spec:
  type: service
  owner: ${{ values.owner }}
  lifecycle: experimental
```

## Uploading the template to Backstage

You can make templates available to Backstage in several ways:

* Add the template YAML to a location listed in `app-config.yaml` (file or URL).
* Register it through the Backstage UI: Create → Manage Templates → Register an existing component.
* Use an entity provider to discover templates dynamically from a repository.

If you register via the UI and see "template not of allowed kind for that location", ensure your catalog integration `rules` include `Template`.

Store templates in a dedicated repo (recommended) — for example `backstage-templates` with a `templates/` directory:

<Frame>
  <img alt="A screenshot of a GitHub repository page showing the backstage-templates/templates directory with files like api-template.yaml, template10.yaml, and template11.yaml. A green pointer/cursor is clicking the api-template.yaml entry in the file list." />
</Frame>

Registering a template via the UI:

<Frame>
  <img alt="Screenshot of the Backstage web UI showing the &#x22;Register an existing component&#x22; wizard with steps to select a URL, select locations, review discovered entities, and an emphasized &#x22;IMPORT&#x22; button. A left navigation bar lists Home, APIs, Docs and Create, while the right panel explains linking to an entity file or repository." />
</Frame>

## GitHub authentication & permissions

* The GitHub integration token used by Backstage must have permissions to create repositories if you use `publish:github`.
* If your skeleton includes GitHub Actions workflows, ensure the token has the required workflow permissions to push workflows.
* Configure the token in Backstage integrations (e.g., `app-config.yaml`) so `publish:github` works.

## Create a component with the template

Once the template is registered, use the Create flow to provision a component. Example run progress:

<Frame>
  <img alt="A screenshot of the Backstage web UI showing a run page for &#x22;api-express-template&#x22; with a horizontal progress timeline of completed steps (Fetch Base, Publish, Register). The left sidebar displays navigation items like Home, APIs, Docs, and Create." />
</Frame>

The created component page shows ownership and relations:

<Frame>
  <img alt="A Backstage web UI page for a &#x22;video-processing&#x22; service component, showing the About panel (with owner &#x22;dev&#x22; and lifecycle &#x22;experimental&#x22;) and options like View Source and View TechDocs. The right side displays a relations graph linking the &#x22;dev&#x22; owner to the video-processing component." />
</Frame>

Resulting package.json example (after templating):

```json theme={null}
{
  "name": "video-processing",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "jest",
    "test:ci": "jest --ci",
    "dev": "nodemon src/index.js",
    "format": "prettier --write",
    "format:check": "prettier --check",
    "lint": "eslint .",
    "lint:fix": "eslint --fix ."
  },
  "type": "module",
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@eslint/js": "^9.17.0",
    "eslint": "^9.17.0",
    "eslint-config-prettier": "^9.1.0",
    "eslint-plugin-jest": "^28.10.0",
    "globals": "^15.14.0",
    "jest": "^29.7.0",
    "nodemon": "^2.0.20",
    "prettier": "^2.8.8"
  }
}
```

Resulting `catalog-info.yaml` example:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: "video-processing"
spec:
  type: service
  owner: group:default/dev
  lifecycle: experimental
```

## Recap / tips

* Design the user interface with `parameters`; reuse Backstage UI widgets using `ui:field` (e.g., `OwnerPicker`, `RepoUrlPicker`).
* Use `fetch:template` to download and template a skeleton; map `parameters` to `values`.
* Use `publish:github` to create and push the repository (requires appropriately permissioned GitHub token).
* Use `catalog:register` to add the new component to Backstage.
* Avoid hyphens in parameter names; prefer `name`, `owner`.
* If the Template Form Playground behaves oddly, edit YAML in an external editor and paste it back.

This pattern enables platform teams to bake best practices and guardrails into starter repositories so developers can quickly create production-ready services.

## Links and references

* Backstage Scaffolder docs: [https://backstage.io/docs/features/software-templates/using-templates](https://backstage.io/docs/features/software-templates/using-templates)
* Backstage Scaffolder actions (fetch, publish, register): [https://backstage.io/docs/features/software-templates/actions](https://backstage.io/docs/features/software-templates/actions)
* Backstage Catalog entities: [https://backstage.io/docs/features/software-catalog/overview](https://backstage.io/docs/features/software-catalog/overview)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/1c7142e3-0cb6-40ae-b5b6-77252f8c85b2/lesson/bdcf9a0b-92e8-4ce6-80c9-187b0e117a98)


# Demo Importing Templates with Entity Providers

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Templates/Demo-Importing-Templates-with-Entity-Providers/page

Explains using Backstage entity providers to automatically discover and register template YAML files from repositories, configuring catalogPath globs and provider settings to scale template management

In this lesson you'll learn how to import Backstage templates automatically using entity providers so you don't have to register each template manually. This approach scales much better when you maintain many templates in a repository.

## Template descriptor example

Below is an example Template descriptor (Node.js Express API) you might store as a YAML file inside your templates repository.

```yaml theme={null}
apiVersion: scaffolder.backstage.io/v1beta3
