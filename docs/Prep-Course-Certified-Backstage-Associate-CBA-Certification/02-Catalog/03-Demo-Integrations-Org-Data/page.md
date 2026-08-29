# Demo Integrations Org Data

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Catalog/Demo-Integrations-Org-Data/page

Guide to importing GitHub organizational users and teams into Backstage, covering plugin installation, provider configuration, token scopes, scheduling, and verifying imported catalog entities.

In this guide you'll learn how to import organizational data (users and teams) from GitHub into Backstage so that catalog entities can reference existing users and groups. This is useful when you want Backstage to reflect your source of truth for people and team structure — GitHub in this example.

Overview

* Install the GitHub org backend module.
* Register the module in your backend entrypoint (`index.ts`).
* Configure the provider in `app-config.yaml` under `catalog.providers.githubOrg`.
* Ensure the GitHub integration token has the required scopes (`read:org`).
* Restart the backend and verify users/groups are imported into the catalog.

Step 1 — Install the GitHub org backend module
Install the module into the backend workspace:

```bash theme={null}
yarn --cwd packages/backend add @backstage/plugin-catalog-backend-module-github-org
```

So for the first thing that we have to do is install the plugin called `@backstage/plugin-catalog-backend-module-github-org`.

<Frame>
  <img alt="A screenshot of the Backstage documentation page titled &#x22;GitHub Organizational Data,&#x22; showing a dark-themed layout with a left navigation menu for integrations and main content about permissions, installation, and notes. The page includes info/notice boxes and links related to GitHub org data setup." />
</Frame>

Step 2 — Register the module in your backend entrypoint
Add the GitHub org module import to your backend entrypoint file, commonly `packages/backend/src/index.ts`. Register it alongside other catalog backend modules so Backstage can instantiate the provider.

Example registration snippet:

```typescript theme={null}
// packages/backend/src/index.ts

// auth plugin
backend.add(import('@backstage/plugin-auth-backend'));
backend.add(import('@backstage/plugin-auth-backend-module-guest-provider'));

// catalog plugin
backend.add(import('@backstage/plugin-catalog-backend'));
backend.add(import('@backstage/plugin-catalog-backend-module-github'));
backend.add(import('@backstage/plugin-catalog-backend-module-github-org'));
backend.add(
  import('@backstage/plugin-catalog-backend-module-scaffolder-entity-model'),
);
```

After installing the package you should see output similar to this:

```bash theme={null}
YN0000: Completed
YN0000: Fetch step
YN0013: A package was added to the project (+ 45.92 KiB).
YN0000: Completed in 2s 902ms
YN0000: Link step
YN0000: Completed in 2s 261ms
YN0000: Done with warnings in 7s 407ms
```

Step 3 — Configure the GitHub org provider in app-config.yaml
Add a `githubOrg` provider under `catalog.providers`. Provide an `id`, the `githubUrl` (e.g., `https://github.com` or your GitHub Enterprise hostname), the `orgs` array, and a `schedule` for scanning.

Example configuration:

```yaml theme={null}
catalog:
  providers:
    githubOrg:
      - id: production
        githubUrl: https://github.com
        orgs: ['shopping-hub']
        schedule:
          initialDelay: { seconds: 30 }
          frequency: { hours: 1 }
          timeout: { minutes: 50 }

    # The existing github provider for scanning catalog-info.yaml in repositories
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
```

Configuration notes

* `id`: arbitrary provider identifier.
* `githubUrl`: GitHub base URL or enterprise hostname.
* `orgs`: list of GitHub organization names to import (e.g., `['shopping-hub']`).
* `schedule`: controls how often Backstage queries GitHub for org data. Org membership and teams change infrequently — hourly is a reasonable default.

For quick reference, here are the main config properties:

| Property                                  | Description                                              | Example              |
| ----------------------------------------- | -------------------------------------------------------- | -------------------- |
| `catalog.providers.githubOrg[].id`        | Provider identifier                                      | `production`         |
| `catalog.providers.githubOrg[].githubUrl` | GitHub base URL or enterprise hostname                   | `https://github.com` |
| `catalog.providers.githubOrg[].orgs`      | Array of GitHub organization names                       | `['shopping-hub']`   |
| `catalog.providers.githubOrg[].schedule`  | Scan scheduling (`initialDelay`, `frequency`, `timeout`) | See example above    |

Step 4 — Ensure the GitHub token has the correct scopes
Backstage uses the GitHub integration token configured under `integrations.github` in `app-config.yaml`. That token must include permissions to read org membership and team data.

Minimum recommended scopes:

* `read:org` — required to read organizations, teams, and membership.
* `read:user` — optional, to fetch additional user profile information.

<Frame>
  <img alt="A screenshot of the GitHub personal access token settings page showing selectable OAuth scopes with checkboxes (the &#x22;repo&#x22; and &#x22;read:org&#x22; scopes are checked). The page also displays an expiration date for the token: Sat, Mar 15 2025." />
</Frame>

Permissions table

| Scope       | Purpose                                               |
| ----------- | ----------------------------------------------------- |
| `read:org`  | Read organizations, teams, and memberships (required) |
| `read:user` | Read additional user profile data (optional)          |

If the token lacks `read:org`, Backstage cannot import users or groups. Update the token scopes in GitHub or create a new token, then update your Backstage integration configuration.

Step 5 — Restart the backend
After installing the plugin or changing configuration or token scopes, restart the Backstage backend so the provider picks up the new settings and runs its initial scan. Some deployments allow manually triggering a provider run; otherwise restart is the simplest approach.

Verify results in the Backstage catalog

* Users page: user entities imported from the GitHub org will appear.
* Groups page: GitHub teams become Backstage group entities. Nested GitHub teams are represented as parent/child groups in Backstage (e.g., `dev` and `dev/auth`).

Example: after the provider runs, a GitHub team named `dev` becomes a Backstage group `dev`, and its members are imported as group members. Nested teams such as `dev/auth` will appear as child groups under `dev`.

Troubleshooting

<Callout icon="lightbulb">
  If users or groups are not imported after configuring the provider, confirm that:

  * The `catalog.providers.githubOrg` configuration points to the correct GitHub organizations.
  * The GitHub integration token has the `read:org` scope.
  * The backend has been restarted so the provider can perform an initial scan (or manually trigger the provider run if your deployment supports it).
    You can also check backend logs for provider scheduling and any error messages.
</Callout>

Example scanned entity link metadata (reference)

```yaml theme={null}
metadata:
  name: example
  links:
    - url: https://dashboard.example.com
      title: My Dashboard
      icon: dashboard
```

Additional resources

* Backstage catalog provider documentation: [https://backstage.io/docs/features/software-catalog](https://backstage.io/docs/features/software-catalog)
* GitHub personal access tokens: [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

That covers importing organizational data from GitHub into Backstage. Once configured, the org provider keeps your catalog in sync according to the schedule you define so teams and users stay up to date.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/f9244f9d-083a-4acd-a518-549f54b644b5/lesson/a0f304c9-fe03-4770-9ad0-a9c124022d00" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/f9244f9d-083a-4acd-a518-549f54b644b5/lesson/f46885a4-ee59-448f-aa0e-b13bca1bdbf3" />
</CardGroup>
