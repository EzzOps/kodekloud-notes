# Demo Authentication

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Production-Backstage/Demo-Authentication/page

Guide to configure GitHub OAuth sign-in for Backstage, including OAuth app setup, frontend and backend configuration, sign-in resolvers, and resolving user identity mapping errors

In previous examples we used the built-in `guest` user. This guide shows how to let users sign in with GitHub by:

* Registering a GitHub OAuth App.
* Configuring Backstage frontend and backend to use GitHub as an auth provider.
* Adding a sign-in resolver to map GitHub identities to Backstage `User` entities.
* Reproducing and resolving the common "unable to resolve user identity" error by importing or creating matching user entities.

Prerequisites: a running Backstage app (frontend typically at `http://localhost:3000`, backend at `http://localhost:7007` in development).

Quick overview of the flow:

1. GitHub performs OAuth and returns an identity.
2. Backstage auth backend validates the OAuth flow.
3. The Sign-in resolver maps the identity to a Backstage `User` entity in the catalog.
4. If no matching `User` exists, sign-in fails with the resolver error.

***

You may already have some of the configuration in place. Example `publish`/`auth` snippet (use environment variables for secrets in production):

```yaml theme={null}
runIn: 'docker' # Alternatives - 'local'
publisher:
  type: 'local' # Alternatives - 'googleGcs' or 'awsS3'

auth:
  # see https://backstage.io/docs/auth/ to learn about auth providers
  providers:
    github:
      development:
        clientId: YOUR_GITHUB_CLIENT_ID
        clientSecret: YOUR_GITHUB_CLIENT_SECRET
  # See https://backstage.io/docs/auth/guest/provider
  guest: {}
```

Example catalog provider for importing organization data from GitHub:

```yaml theme={null}
catalog:
  providers:
    githubOrg:
      - id: github
        githubUrl: https://github.com
        orgs: ['shopping-hub']
        schedule:
          initialDelay: { seconds: 30 }
          frequency: { hours: 1 }
          timeout: { minutes: 50 }
```

If you want to demonstrate the resolver error, temporarily disable user-importing providers so no `User` entities are imported from GitHub — this reproduces the "unable to resolve user identity" case later.

## 1. Create a GitHub OAuth App

Register an OAuth App in your GitHub account to get a Client ID and Client Secret:

* GitHub → Settings → Developer settings → OAuth Apps → New OAuth App.
* Application name: e.g. `backstage-auth`.
* Homepage URL: your Backstage frontend URL, e.g. `http://localhost:3000` or `http://<IP_ADDRESS>:3000`.
* Authorization callback URL: your auth backend handler, e.g. `http://localhost:7007/api/auth/github/handler/frame`.

<Frame>
  <img alt="A screenshot of the GitHub Developer Settings page showing the OAuth Apps section with two registered applications named &#x22;backstage&#x22; and &#x22;test,&#x22; each with an Edit button. The left sidebar also shows navigation for GitHub Apps and Personal access tokens." />
</Frame>

After registering, GitHub provides a Client ID and allows you to generate a Client Secret. Copy both values — you will use them in Backstage configuration.

<Frame>
  <img alt="A screenshot of GitHub's &#x22;Register a new OAuth app&#x22; page showing form fields including Application name (&#x22;backstage-auth&#x22;), a Homepage URL with an IP address and port, and an Authorization callback URL. The &#x22;Register application&#x22; button is visible at the bottom." />
</Frame>

> **warning** GitHub shows the client secret only once when you create it. Copy it immediately and store it securely (for example, in environment variables or a secrets manager). Do not commit secrets to source control.

You can view the Client ID and manage Client Secrets from the OAuth app settings page. If you lose the secret, generate a new one.

<Frame>
  <img alt="A screenshot of a GitHub OAuth application settings page showing the Client ID and Client secrets sections with buttons to generate or revoke secrets and a notice to copy the secret. The page also shows &#x22;0 users&#x22; and an area to upload an application logo." />
</Frame>

## 2. Configure Backstage auth in app-config.yaml

Add the GitHub provider configuration to `app-config.yaml`. Use environment variables rather than hard-coded secrets for production.

Example minimal development config with a sign-in resolver:

```yaml theme={null}
auth:
  # see https://backstage.io/docs/auth/ to learn about auth providers
  environment: development
  providers:
    guest: {}
    github:
      development:
        clientId: ${AUTH_GITHUB_CLIENT_ID}
        clientSecret: ${AUTH_GITHUB_CLIENT_SECRET}
        signIn:
          resolvers:
            # Matches the GitHub username with the Backstage user entity metadata.name
            - resolver: usernameMatchingUserEntityName
```

Notes:

* `environment: development` selects the credentials under `github.development`.
* `signIn.resolvers` tells Backstage how to map the identity returned by GitHub to a Backstage `User` entity.
* `usernameMatchingUserEntityName` attempts to match the GitHub username (login) to a `User` entity's `metadata.name`.

Other resolvers are available (for example, email-based resolvers). See the Backstage authentication docs for the full list and pick the one that fits your user model: [https://backstage.io/docs/auth/](https://backstage.io/docs/auth/)

## 3. Backend — register the GitHub auth backend module

Install and register the GitHub auth backend provider module so the backend can handle the OAuth flow.

Install the provider module from the workspace root:

```bash theme={null}
yarn --cwd packages/backend add @backstage/plugin-auth-backend-module-github-provider
```

Register it in your backend startup file (example `packages/backend/src/index.ts`):

```typescript theme={null}
import { createBackend } from '@backstage/backend-plugin-api';
import authPlugin from '@backstage/plugin-auth-backend';
// import the provider module
import githubProviderModule from '@backstage/plugin-auth-backend-module-github-provider';

const backend = createBackend();

backend.add(authPlugin);
backend.add(githubProviderModule);

backend.start();
```

Important: ensure the provider `id` exposed by the backend matches the frontend provider `id` (commonly `github`). Backend registration details depend on your backend structure, but the provider module must be added and active.

## 4. Frontend — enable GitHub on the SignIn page

To display a GitHub sign-in button, add the GitHub provider to the `SignInPage` component (e.g., `packages/app/src/app.tsx`).

Import the API ref:

```typescript theme={null}
import { githubAuthApiRef } from '@backstage/core-plugin-api';
```

Then add the provider to the `SignInPage` components config:

```tsx theme={null}
components: {
  SignInPage: props => (
    <SignInPage
      {...props}
      auto
      provider={{
        id: 'github',
        title: 'GitHub',
        message: 'Sign in using GitHub',
        apiRef: githubAuthApiRef,
      }}
    />
  ),
},
```

You can include multiple providers (for example both `guest` and `github`) so users can choose their sign-in method. Rebuild/restart the frontend after changes.

## 5. Clear cookies to test a fresh sign-in

Backstage uses HTTP cookies for sessions. To test first-run behavior:

* Clear cookies/site data for your Backstage origin in the browser.
* Reload the SignIn page.

If GitHub is misconfigured (missing `environment`, `clientId`, or `clientSecret`), the SignIn page may show an error like "The GitHub provider is not configured to support sign-in."

> **lightbulb** Clearing cookies ensures you test the full OAuth flow from the beginning. This helps validate that the frontend, backend, and GitHub OAuth callback are wired correctly.

## 6. Common error: "unable to resolve user identity"

After GitHub consent you might see this error:

```text theme={null}
Login failed: failed to sign in, unable to resolve user identity.
Please verify that your catalog contains the expected user entities
that would match your configured sign-in resolver.
```

<Frame>
  <img alt="A web app login screen titled &#x22;Scaffolded Backstage App&#x22; showing two sign-in cards for &#x22;Guest&#x22; and &#x22;Github.&#x22; A red error banner at the top reports a login failure saying it can't resolve the user identity." />
</Frame>

This means GitHub authenticated you, but Backstage could not map the returned identity to any `User` entity in the catalog using the configured resolver.

> **lightbulb** The sign-in resolver maps identity attributes returned by GitHub (e.g., username or email) to a Backstage `User` entity. If no matching user entity exists, sign-in fails with the "unable to resolve user identity" error.

Options to fix the error:

1. Create a `User` entity that matches the resolver's expectations. Example YAML if using `usernameMatchingUserEntityName`:

```yaml theme={null}
