# Demo Integrations Private Repository

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Catalog/Demo-Integrations-Private-Repository/page

Guide to configuring Backstage to access and import catalog files from private GitHub repositories using a personal access token and integrations in app-config.yaml

This lesson shows how to configure Backstage so it can fetch catalog entity files from a private GitHub repository. By default Backstage reads public repositories without authentication, but private repositories require a GitHub integration and an access token (Personal Access Token — PAT).

What you'll see here:

* Turn a repository private and reproduce the import error.
* Generate a GitHub PAT with minimal scopes.
* Configure Backstage to use the token and allow access to `raw.githubusercontent.com`.
* Restart Backstage and successfully import the entity.

We begin with a repository that was public and has been changed to private in the GitHub repository settings:

<Frame>
  <img alt="A screenshot of a GitHub repository's Settings → General page for &#x22;backstage-auth-service,&#x22; showing the repository name, options to rename, and the default branch set to &#x22;main.&#x22; The left sidebar lists settings sections like Collaborators, Branches, Actions, Webhooks, and Security." />
</Frame>

When you attempt to register the existing component by pointing Backstage at the repository `catalog-info.yaml`, the backend will return a 404 because it cannot read the `raw.githubusercontent.com` URL without authentication. Example error returned by the Backstage backend:

```json theme={null}
{
  "error": {
    "name": "InputError",
    "message": "NotFoundError: Unable to read url, NotFoundError: Request failed for https://raw.githubusercontent.com/Sanjeev-Thiyagarajan/backstage-auth-service/main/catalog-info.yaml, 404 Not Found",
    "stack": "InputError: NotFoundError: Unable to read url, NotFoundError: Request failed for https://raw.githubusercontent.com/Sanjeev-Thiyagarajan/backstage-auth-service/main/catalog-info.yaml, 404 Not Found\n    at DefaultLocationService.processEntities (/root/demo/backstage/node_modules/@backstage/plugin-catalog-[SECRET_REDACTED].ts:110:15)\n    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)\n    at DefaultLocationService.tryRunCreateLocation (/root/demo/backstage/node_modules/@backstage/plugin-catalog-[SECRET_REDACTED].ts:148:32)\n    at <anonymous> (/root/demo/backstage/node_modules/@backstage/plugin-catalog-backend/src/service/createRouter.ts:322:24)"
  },
  "request": {
    "method": "POST",
    "url": "/locations?dryRun=true"
  },
  "response": {
    "statusCode": 400
  }
}
```

The 404 indicates Backstage was blocked from accessing the raw URL — because the repository is private. To allow Backstage to fetch files from private repositories you must configure the GitHub integration and provide a token that permits reading private repo contents.

The entity file we attempted to import (`catalog-info.yaml`) looks like this:

```yaml theme={null}
apiVersion: backstage.io/v1beta1
kind: Component
metadata:
  name: auth-service
  description: authentication service
  tags:
    - javascript
  links:
    - url: https://google.com
      title: Admin Dashboard
      icon: dashboard
      type: admin-dashboard
spec:
  type: service
  lifecycle: production
  owner: guests
  providesApis:
    - auth-api
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: auth-api
  description: Verify user authentication status
spec:
  type: openapi
  lifecycle: production
  owner: guests
  apiProvidedBy: auth-service
```

## Backstage configuration required

Backstage uses an `integrations` section in `app-config.yaml` to authorize GitHub requests. At minimum you must:

* Allow reading `raw.githubusercontent.com` in the `reading.allow` list.
* Add a `github` integration entry and provide a token (via environment variable is recommended).

Example `app-config.yaml` snippet:

```yaml theme={null}
reading:
  allow:
    - host: 'raw.githubusercontent.com'

integrations:
  github:
    - host: github.com
      # This is a Personal Access Token (PAT) from GitHub.
      # Prefer reading this from an environment variable rather than hardcoding.
      token: ${GITHUB_TOKEN}
