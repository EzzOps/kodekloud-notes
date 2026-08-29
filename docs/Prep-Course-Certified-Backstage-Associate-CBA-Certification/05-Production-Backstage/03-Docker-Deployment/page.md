# Example user entity in the catalog
apiVersion: backstage.io/v1alpha1
kind: User
metadata:
  name: sanjeev  # must match the GitHub username if using usernameMatchingUserEntityName
spec:
  memberOf: [guests]
```

2. Import users (and optionally groups) from GitHub into the catalog by enabling a `catalog.providers.githubOrg` (or other GitHub provider) configuration and restarting the backend so entities are ingested automatically.

If you prefer to import users automatically, re-enable or add the appropriate catalog provider and ensure it imports `User` and `Group` descriptors (or repositories containing `catalog-info.yaml` that describe them).

## 7. Final verification

Verify each step:

* OAuth app registered on GitHub with the correct callback URL.
* `auth.providers.github` set in `app-config.yaml` with `environment` and credentials.
* GitHub provider module registered on the backend.
* Backstage catalog contains `User` entities that match your sign-in resolver (manually created or imported).

On success you will be able to sign in with GitHub and see your account in the Software Catalog (Users).

<Frame>
  <img alt="A web application dashboard titled &#x22;My Company Catalog&#x22; with a left sidebar menu and a main panel listing &#x22;All Users (3)&#x22;. The user table shows three entries (guest, Jenny Doe, and Sanjeev Thiyagarajan) with search and action icons." />
</Frame>

That completes the GitHub authentication integration for Backstage. You can adapt the same steps for other providers (Google, OAuth2, SAML) by consulting the Backstage authentication docs and selecting sign-in resolvers appropriate for your user identity model:

* Backstage Authentication docs: [https://backstage.io/docs/auth/](https://backstage.io/docs/auth/)
* Backstage Catalog docs: [https://backstage.io/docs/features/software-catalog/overview](https://backstage.io/docs/features/software-catalog/overview)

Useful configuration summary

| Item                    | Location / File                       | Purpose / Example                                                                                                |
| ----------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Auth provider config    | `app-config.yaml`                     | Set `auth.providers.github` and `environment` with `${AUTH_GITHUB_CLIENT_ID}` and `${AUTH_GITHUB_CLIENT_SECRET}` |
| Backend provider module | `packages/backend`                    | `@backstage/plugin-auth-backend-module-github-provider` must be added and registered                             |
| Frontend sign-in        | `packages/app/src/app.tsx`            | Add provider to `SignInPage` using `githubAuthApiRef`                                                            |
| Catalog import          | `app-config.yaml` (catalog.providers) | `githubOrg` or `github` provider to import `User`/`Group` entities                                               |
| User entity example     | `catalog-info.yaml`                   | `kind: User` with `metadata.name` matching GitHub username if using username resolver                            |

Tips:

* Use environment variables or a secrets manager for `clientSecret`.
* If you see a sign-in resolver error, check the catalog contents and the resolver type you configured.
* Test locally by clearing cookies and running the full sign-in flow.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/d82fc857-4b5c-42a7-ab46-3772f749a741/lesson/4f04b6c3-8db2-41b9-95b1-c073d12298e2)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/d82fc857-4b5c-42a7-ab46-3772f749a741/lesson/12c3e3e6-cee7-4e60-a3fc-67e323f12a35)


# Docker Deployment

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Production-Backstage/Docker-Deployment/page

Guide to building and deploying a Backstage backend Docker image, covering the generated Dockerfile, build steps, BuildKit requirements, and CI/CD considerations.

This guide shows how to package a Backstage backend into a Docker container so you can run it locally or deploy it with your preferred orchestrator (for example, Kubernetes or Amazon ECS). It walks through the generated backend Dockerfile, local preparation steps, image build and run commands, and CI/CD considerations.

Key terms: Backstage Docker image, Docker BuildKit, Yarn v3 (Berry), backend bundle, CI/CD build agents.

> **lightbulb** Before building, make sure you understand where the Docker build context should be. The Dockerfile expects the backend bundle artifacts under `packages/backend/dist` in the build context (usually the repository root).

## Where the Dockerfile lives

When you create a Backstage app using `backstage create-app`, a production-ready Dockerfile is generated for the backend package.

Dockerfile path:
`packages/backend/Dockerfile`

Below is the generated Dockerfile (unchanged):

```dockerfile theme={null}
FROM node:20-bookworm-slim
