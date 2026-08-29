# Demo Creating a Template

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Templates/Demo-Creating-a-Template/page

Guide to building a Backstage Scaffolder template that provisions Node.js Express starter repositories with ESLint, Prettier, Jest, GitHub Actions, and automatic catalog registration

In this guide you'll learn how to create a Backstage Scaffolder template that provisions a starter Node.js API repository (Express) with your organization conventions baked in. The template will:

* scaffold a repository with ESLint, Prettier, Jest, GitHub Actions CI, and a sample Express app
* create the GitHub repository
* register the new component in the Backstage catalog

This enables developers to create new services quickly with the correct tooling and guardrails in place.

## Organization requirements (example)

Use these as a checklist when building the skeleton (blueprint) repository.

| Requirement   | Example                              |
| ------------- | ------------------------------------ |
| Linter        | ESLint                               |
| Formatter     | Prettier                             |
| Testing       | Jest                                 |
| CI/CD         | GitHub Actions (`.github/workflows`) |
| API framework | Express.js                           |

## High-level flow

1. Platform team creates a skeleton (blueprint) repository that contains:
   * `package.json`, ESLint & Prettier config, tests, GitHub workflows
   * a sample Express app (`src/`), and a `catalog-info.yaml`
2. Upload the skeleton to GitHub (e.g., `backstage-express-api-blueprint`).
3. Create a Scaffolder `Template` YAML that:
   * renders a multi-page form for the developer (project name, owner, repo location)
   * fetches the skeleton, templates values into files, publishes the repo, and registers the component
4. Developer uses the template through Backstage Create UI — Backstage runs the template and provisions the repo and catalog entry.

<Callout icon="lightbulb">
  Design templates so platform-spec decisions (lint, test, CI) are enforced by the skeleton. Use consistent parameter names (e.g., `name`, `owner`) to simplify templating and avoid parsing pitfalls.
</Callout>

This is what the template tile will look like inside Backstage:

<Frame>
  <img alt="A web app screenshot of the Backstage &#x22;Create a new component&#x22; page showing template cards for Node.js services (e.g., &#x22;Node.JS API w/ express.js&#x22; and &#x22;Example Node.js Template&#x22;). The left sidebar shows navigation items like Home, APIs, Docs and Create." />
</Frame>

Developer fills in the template form (example):

<Frame>
  <img alt="A screenshot of the Backstage &#x22;Create a new component&#x22; page showing the Node.JS API w/ express.js template. The form displays a component name &#x22;inventory-service&#x22; and an owner field set to &#x22;group:default/dev.&#x22;" />
</Frame>

Backstage runs the template and shows run progress (fetch, publish, register):

<Frame>
  <img alt="A screenshot of the Backstage web UI showing a run titled &#x22;Run of api-express-template&#x22; with a three-step progress bar where &#x22;Fetch Base&#x22; is complete, &#x22;Publish&#x22; is in progress, and &#x22;Register&#x22; is pending. The left sidebar shows navigation items like Home, APIs, Docs and a highlighted &#x22;Create...&#x22; option." />
</Frame>

After completion, the new repository appears in GitHub with the skeleton files (package.json, `.github/workflows`, `src/`, tests, etc.):

<Frame>
  <img alt="A screenshot of a GitHub repository page for &#x22;inventory-service,&#x22; showing the file list (folders like .github/workflows, src, tests and files such as .gitignore, package.json) and the repo sidebar with activity and language info." />
</Frame>

The scaffolder injects the provided values (for example, `inventory-service` in `package.json` and `catalog-info.yaml`):

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: "inventory-service"
spec:
  type: service
  owner: group:default/dev
  lifecycle: experimental
  dependsOn:
    - "resource:inventory-service-ec2"
```

Backstage catalog shows the registered component:

<Frame>
  <img alt="A screenshot of the Backstage catalog showing the &#x22;inventory-service&#x22; component overview page with an alert about missing related entities and panels for About (owner: dev, lifecycle: experimental) and Relations (graph linking dev to inventory-service)." />
</Frame>

## Template Form Playground

Backstage includes a Template Form Playground to design and test scaffolder form UI interactively. Use it to verify pages, required fields, and UI widgets like `OwnerPicker` and `RepoUrlPicker`.

A minimal playground example (two parameter pages and one fetch step):

```yaml theme={null}
