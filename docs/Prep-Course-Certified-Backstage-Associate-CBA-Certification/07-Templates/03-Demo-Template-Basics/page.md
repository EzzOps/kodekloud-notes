# https://backstage.io/docs/features/software-catalog/descriptor-format#kind-template
kind: Template
metadata:
  name: api-express-template
  title: Node.JS API w/ express.js
  description: A template for provisioning APIs with Express.JS
spec:
  owner: user:guest
  type: service

  # These parameters are used to generate the input form in the frontend, and are
  # used to gather input data for the execution of the template.
  parameters:
    - title: Project Info
      required:
        - name
      properties:
        name:
          title: Name
          type: string
          description: Unique name of the component
          'ui:autofocus': true
          'ui:options':
            rows: 5
        owner:
          title: Owner
          type: string
          description: Owner of the component
```

For more on descriptor fields and supported kinds, see the Backstage descriptor format documentation: [Descriptor format — Backstage](https://backstage.io/docs/features/software-catalog/descriptor-format).

## Why use entity providers?

Previously you might manually import a template by copying a template file URL and using "Register Existing Component" in Backstage. That works for a few templates but becomes tedious and error-prone at scale.

Entity providers solve this by scanning configured locations (for example, GitHub repositories or organizations) and registering any entity descriptors they find — including `kind: Template` files. Providers can be configured to search specific paths or globs, filter repositories, and run on a schedule.

## Scaffolder and auth settings

To enable the Scaffolder and its runner/publisher behavior you typically configure scaffolder-related settings in `app-config.yaml`. Example:

```yaml theme={null}
scaffolder:
  builder: 'local'           # Alternatives: 'external'
  generator:
    runIn: 'docker'         # Alternatives: 'local'
  publisher:
    type: 'local'           # Alternatives: 'googleGcs' or 'awsS3'. See documentation for details.

auth:
  # see https://backstage.io/docs/auth/ to learn about auth providers
  providers:
    # See https://backstage.io/docs/auth/guest/provider
    guest: {}
```

See Backstage Scaffolder docs for full configuration options: [Scaffolder — Backstage](https://backstage.io/docs/features/software-templates/scaffolder-overview).

## Default GitHub provider behavior

Many examples use a GitHub provider that looks for a single file path such as `/catalog-info.yaml`. If your templates are stored under different filenames or a dedicated `templates/` folder, the provider won't find or register them unless you adjust `catalogPath`.

Example of providers configured to look for `/catalog-info.yaml`:

```yaml theme={null}
github:
  shoppingHub:
    organization: 'shopping-hub'
    catalogPath: '/catalog-info.yaml'
    filters:
      branch: 'main'
      repository: '.*'
    schedule:
      frequency: { minutes: 20 }
      timeout: { minutes: 2 }
  sanjeevAccount:
    organization: 'Sanjeev-Thiyagarajan'
    catalogPath: '/catalog-info.yaml'
    filters:
      branch: 'main'
      repository: '.*'
    schedule:
      frequency: { minutes: 20 }
      timeout: { minutes: 2 }
```

If your repository uses a layout like `templates/api-template.yaml`, `templates/template10.yaml`, etc., the provider above will not discover them.

<Frame>
  <img alt="A screenshot of a GitHub repository page showing the &#x22;backstage-templates/templates&#x22; folder. The file list displays three YAML files (api-template.yaml, template10.yaml, template11.yaml) along with recent commit info." />
</Frame>

## Configure a provider to discover template files under a folder

Add a new GitHub provider (name it as you like) and set `catalogPath` to a glob that matches YAML files under your `templates/` directory. Example:

```yaml theme={null}
github:
  shoppingHub:
    organization: 'shopping-hub'
    catalogPath: '/catalog-info.yaml'
    filters:
      branch: 'main'
      repository: '.*'
    schedule:
      frequency: { minutes: 20 }
      timeout: { minutes: 2 }

  sanjeevAccount:
    organization: 'Sanjeev-Thiyagarajan'
    catalogPath: '/catalog-info.yaml'
    filters:
      branch: 'main'
      repository: '.*'
    schedule:
      frequency: { minutes: 20 }
      timeout: { minutes: 2 }

  github-templates:
    organization: 'Sanjeev-Thiyagarajan'
    catalogPath: 'templates/**/*.yaml'
    filters:
      branch: 'main'
      repository: 'backstage-templates'
    schedule:
      frequency: { minutes: 20 }
      timeout: { minutes: 2 }
```

This `github-templates` provider will:

* Search any folder under `templates/` for files that end with `.yaml`.
* Only scan the `backstage-templates` repository on the `main` branch.
* Register any valid entity descriptors it finds, including Template entities.

> **lightbulb** Use a glob like `templates/**/*.yaml` in `catalogPath` when your repository stores many template files under a common folder. Ensure the YAML files contain valid entity descriptors (for templates, `kind: Template`).

## Quick reference — GitHub provider settings

| Field          | Purpose                                            | Example                                                                   |
| -------------- | -------------------------------------------------- | ------------------------------------------------------------------------- |
| `organization` | GitHub organization or owner to scan               | `shopping-hub`                                                            |
| `catalogPath`  | File path or glob to locate entity descriptors     | `templates/**/*.yaml`                                                     |
| `filters`      | Limit by `branch` and `repository` (regex allowed) | `branch: 'main'` `repository: 'backstage-templates'`                      |
| `schedule`     | How often to rescan                                | `frequency: { minutes: 20 }` (wrap curly braces in code when used inline) |

## Apply and verify

1. Add the new provider configuration to your `app-config.yaml` (or environment-specific config).
2. Restart the Backstage backend so the new provider configuration is picked up.
   * On startup you will see logs indicating providers are being scanned. Example log snippets:

```text theme={null}
[backend]: 2025-02-14T04:23:45.901Z backstage info Found 2 new secrets in config that will be redacted
[app]: [webpack-dev-middleware] wait until bundle finished: callback
```

3. After the provider runs its scan, open the Backstage Create flow. Discovered templates appear alongside other catalog entities and are immediately usable.
4. The provider schedule keeps templates in sync automatically, so changes in your templates repository will be discovered on the next scan.

## Further reading

* Backstage software catalog and descriptor format: [https://backstage.io/docs/features/software-catalog/descriptor-format](https://backstage.io/docs/features/software-catalog/descriptor-format)
* Backstage scaffolder docs: [https://backstage.io/docs/features/software-templates/scaffolder-overview](https://backstage.io/docs/features/software-templates/scaffolder-overview)
* Backstage auth providers: [https://backstage.io/docs/auth/](https://backstage.io/docs/auth/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/1c7142e3-0cb6-40ae-b5b6-77252f8c85b2/lesson/70d3e032-2511-4846-8c95-3d4f3b31f7c9)


# Demo Template Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Templates/Demo-Template-Basics/page

How to create and run a Backstage scaffolder template to generate Node.js starter repositories, push to GitHub, and register services in the Backstage catalog

In this lesson you'll create a first Backstage scaffolder template and follow the end-to-end flow: author a blueprint, surface it in Backstage, run the template from the Create UI, and inspect the published repository and catalog registration.

The example use case: your organization wants every Node.js API to include ESLint, Prettier, Jest, GitHub Actions CI/CD, and Express.js. A platform team can bake those standards into a template so developers get a ready-made starter repo when they scaffold a new service.

<Frame>
  <img alt="A slide titled &#x22;Steps We Will Perform&#x22; showing a diagram where a Platform Team and Developer fill out a &#x22;Form&#x22; to create a Demo-App. The flow points to a GitHub repository and a Template.yaml file as outputs." />
</Frame>

## Conceptual workflow

High-level flow for templated scaffolding:

* Platform team maintains a blueprint repository with starter code (linter, formatter, tests, CI workflow, Express app).
* The blueprint + its `template.yaml` descriptor are made available to Backstage (for example, registered via `app-config.yaml` static entries).
* Developers open Backstage → Create → select the template → fill a brief form → the scaffolder:
  1. fetches the blueprint,
  2. renders files with the form values,
  3. creates a new GitHub repository and pushes the rendered files,
  4. registers the new service in the Backstage catalog.

Below is the example template that ships with Backstage and appears under Create → Templates.

<Frame>
  <img alt="A screenshot of the Backstage &#x22;Create a new component&#x22; page showing a Templates section with an &#x22;Example Node.js Template&#x22; card. The left sidebar displays navigation items like Home, APIs, Docs and Create, and a green cursor is visible on the screen." />
</Frame>

## Where does that example template come from?

Backstage can import static templates via `app-config.yaml`. A representative static entry that imports the local example template looks like this:

```yaml theme={null}
