# Example for GitHub Enterprise:
# - host: ghe.example.net
#   apiBaseUrl: https://ghe.example.net/api/v3
#   rawBaseUrl: https://ghe.example.net/raw
#   token: ${GHE_TOKEN}
```

Table — key configuration items

| Item                          | Purpose                                     | Example / Note                         |
| ----------------------------- | ------------------------------------------- | -------------------------------------- |
| `reading.allow`               | Permit Backstage to fetch raw URLs          | `- host: 'raw.githubusercontent.com'`  |
| `integrations.github[].host`  | GitHub host for the integration             | `github.com`                           |
| `integrations.github[].token` | Token used to authenticate API/raw requests | `token: ${GITHUB_TOKEN}` (use env var) |

## Generate a GitHub Personal Access Token (PAT)

Steps to create a PAT:

1. In GitHub go to: Profile → Settings → Developer settings → Personal access tokens → Classic tokens → Generate new token (classic).
2. Give it a descriptive name (e.g., "Backstage"), choose an expiration, and grant the minimal scope(s) needed to read private repos — typically the `repo` scope.
3. Generate and copy the token; store it securely.

<Frame>
  <img alt="A screenshot of the GitHub &#x22;New personal access token (classic)&#x22; settings page showing fields for the token note, expiration (30 days), and selectable scopes. The &#x22;repo&#x22; scope is checked among other permissions like workflow and package-related options." />
</Frame>

> **warning** Personal access tokens are sensitive credentials. Grant the least privilege required (e.g., `repo` for reading private repos), and avoid long-lived tokens when possible. Use a secrets manager or short expirations in production.

## Set the token in the environment (recommended)

Export the token into the environment used by the Backstage backend process. For example, in a POSIX shell:

```bash theme={null}
export GITHUB_TOKEN="paste_your_token_here"
```

Then restart your Backstage backend so it picks up the environment variable (for example `yarn dev` or `yarn start` depending on your setup).

> **lightbulb** Do not commit personal access tokens to source control. Use environment variables or a secrets manager for production deployments.

> Note: For local testing you can temporarily hardcode the token in `app-config.yaml`, but never commit such changes.

## Retry the Register an existing component flow

After restarting Backstage with the GitHub integration configured and the token available, retry the "Register an existing component" flow in the Backstage UI. Backstage should now be able to access the raw file on GitHub and import the entity.

Register an existing component — Import flow:

<Frame>
  <img alt="A screenshot of the Backstage web UI showing the &#x22;Register an existing component&#x22; wizard with steps to select a URL and locations and an &#x22;Import&#x22; button. The right pane describes linking to an existing entity file or repository (GitHub) to add components to the catalog." />
</Frame>

After the import completes, you can view the component in the catalog. For example, the imported `auth-service` component overview:

<Frame>
  <img alt="A screenshot of the Backstage web UI showing the &#x22;auth-service&#x22; component overview page with an About panel, Relations graph, and a warning about related entities not found. The left sidebar shows navigation items like Home, APIs, Docs, and Create." />
</Frame>

## Summary / Checklist

* Private repositories require a configured GitHub integration so Backstage can authenticate and read raw files.
* Add `raw.githubusercontent.com` to `reading.allow` and configure a `github` integration in `app-config.yaml`.
* Generate a GitHub PAT with the `repo` scope (least privilege) and set it via an environment variable (e.g., `GITHUB_TOKEN`).
* Restart the Backstage backend after configuration changes.
* Re-run "Register an existing component" to import the entity into the catalog.

Further reading and references:

* Backstage docs — Integrations: [https://backstage.io/docs/integrations](https://backstage.io/docs/integrations)
* GitHub docs — Creating a personal access token: [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

This completes the walkthrough for configuring Backstage to read catalog files from private GitHub repositories.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/f9244f9d-083a-4acd-a518-549f54b644b5/lesson/0b0b01d9-69a2-4dab-a159-e9ae7c0bf049)


# Demo Registering a Component

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Catalog/Demo-Registering-a-Component/page

Guide showing how to register and import components into Backstage, including local and remote catalog imports, UI registration, refreshing, and unregistering entities.

In this lesson we'll walk through registering your first real component in Backstage. You'll learn where Backstage loads example entities from, how to register a local component, how to import a `catalog-info.yaml` from a remote Git repository, and how to refresh or unregister entities from the Catalog.

## Where the examples come from

A newly provisioned Backstage instance includes example entities imported via the backend configuration (`app-config.yaml`). At the top of the config you typically have base URLs:

```yaml theme={null}
app:
  baseUrl: http://147.182.170.10:3000

backend:
  baseUrl: http://147.182.170.10:7007

cors:
  origin: http://147.182.170.10:3000
```

Search for the `catalog` section to find static imports (locations). Files referenced with `type: file` are resolved relative to the backend process (usually `packages/backend`):

```yaml theme={null}
catalog:
  import:
    entityFilename: catalog-info.yaml
    pullRequestBranchName: backstage-integration
  rules:
    - allow: [Component, System, API, Resource, Location]
  locations:
    # Local example data, file locations are relative to the backend process, typically `packages/backend`
    - type: file
      target: ../../examples/Entities.yaml

    # Local example template
    - type: file
      target: ../../examples/template/template.yaml
      rules:
        - allow: [Template]
```

Follow the relative path to `examples/Entities.yaml` and you'll find example entities such as an `example-website` component and an example API:

```yaml theme={null}
