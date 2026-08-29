# From your Backstage root directory
yarn --cwd packages/app add @backstage-community/plugin-github-actions
```

This adds `@backstage-community/plugin-github-actions` to `packages/app/package.json` so the frontend can import the plugin components.

Example dependency excerpt from `packages/app/package.json`:

```json theme={null}
"dependencies": {
  "@backstage-community/plugin-github-actions": "^0.8.0",
  "@backstage/app-defaults": "^1.5.16",
  "@backstage/catalog-model": "^1.7.3",
  "@backstage/cli": "^0.29.5",
  "@backstage/core-app-api": "^1.15.4",
  "@backstage/core-components": "^0.16.3",
  "@backstage/core-plugin-api": "^1.10.3"
}
```

After installation, the plugin components are available under `@backstage-community/plugin-github-actions`.

## Quick commands and files

| Action                        | Command / File                                                                          |
| ----------------------------- | --------------------------------------------------------------------------------------- |
| Install frontend plugin       | `yarn --cwd packages/app add @backstage-community/plugin-github-actions`                |
| Install backend auth provider | `yarn --cwd packages/backend add @backstage/plugin-auth-backend-module-github-provider` |
| Frontend entity page          | `[SECRET_REDACTED].tsx`                                    |
| Backend entrypoint            | `packages/backend/src/index.ts`                                                         |

## Back to the UI: the catalog and the entity page

Open your Backstage instance and navigate to the Software Catalog. Select a component (for example, "My Demo app"). Components include the Overview, CI/CD, Kubernetes, and other tabs. The GitHub Actions plugin renders CI/CD details on the CI/CD tab once configured.

<Frame>
  <img alt="A screenshot of the Backstage &#x22;My Company Catalog&#x22; web UI showing a searchable table of components (app1, app2, auth-service, etc.) with columns for owner, type, lifecycle, description and actions. A left sidebar shows navigation and filter options like Home, APIs, Docs and component kind/type." />
</Frame>

Open the component page and check tabs and relations. This entity page is where you will add the GitHub Actions tab.

<Frame>
  <img alt="A screenshot of the Backstage software catalog page for a component named &#x22;my-demo-app,&#x22; showing the Overview tab with About and Relations panels and a warning about an entity relation not found. The left navigation, top header (owner: user:guest, lifecycle: experimental), and a small relations graph are also visible." />
</Frame>

## What the plugin shows

The GitHub Actions plugin queries workflow runs for the repository referenced by the component annotation. It displays recent runs, statuses, commit messages, and links to run details on GitHub—mirroring the information on a repository's Actions page.

<Frame>
  <img alt="A screenshot of a GitHub repository's Actions page showing a list of recent workflow runs (e.g., &#x22;Update catalog-info.yaml&#x22;, &#x22;Create test.yaml&#x22;) with status icons, branch labels, and timestamps. The left sidebar shows the Actions navigation menu." />
</Frame>

If an entity is missing CI/CD annotations, the CI/CD tab will show an empty state prompting you to add the required annotation.

<Frame>
  <img alt="A screenshot of the Backstage UI for a component called &#x22;my-demo-app,&#x22; showing the CI/CD tab with the message &#x22;No CI/CD available for this entity&#x22; and a &#x22;Read more&#x22; button. The left sidebar displays navigation items (Home, APIs, Docs, Create, Register) and decorative chart graphics appear on the right." />
</Frame>

## Adding the plugin UI to an entity page

Import the plugin components and add a route to your entity layout. Edit `[SECRET_REDACTED].tsx` and insert the GitHub Actions route:

```tsx theme={null}
// In [SECRET_REDACTED].tsx
import {
  EntityGithubActionsContent,
  isGithubActionsAvailable,
} from '@backstage-community/plugin-github-actions';

// Example: add a GitHub Actions tab to the service entity page
const serviceEntityPage = (
  <EntityLayout>
    {/* other tabs... */}
    <EntityLayout.Route
      path="/github-actions"
      title="GitHub Actions"
      if={isGithubActionsAvailable}
    >
      <EntityGithubActionsContent />
    </EntityLayout.Route>
  </EntityLayout>
);
```

The plugin exports an availability helper (`isGithubActionsAvailable`) to conditionally render the tab only for entities that include the required annotations.

You can also combine multiple CI/CD providers using `EntitySwitch` to show the correct provider or an empty state:

```tsx theme={null}
// [SECRET_REDACTED].tsx (excerpt)
import { EntitySwitch } from '@backstage/plugin-catalog-react';
import { EntityGithubActionsContent, isGithubActionsAvailable } from '@backstage-community/plugin-github-actions';

const cicdContent = (
  <EntitySwitch>
    <EntitySwitch.Case if={isGithubActionsAvailable}>
      <EntityGithubActionsContent />
    </EntitySwitch.Case>

    <EntitySwitch.Case>
      <EmptyState
        title="No CI/CD available for this entity"
        missing="info"
        description="You need to add an annotation to your component if you want CI/CD information to appear."
      />
    </EntitySwitch.Case>
  </EntitySwitch>
);
```

## Handling authentication on the backend

Although the GitHub Actions plugin runs in the frontend, it requires authenticated GitHub API requests. Backstage handles OAuth and tokens on the backend using auth modules such as `@backstage/plugin-auth-backend-module-github-provider`.

Install the GitHub auth provider into your backend workspace:

```bash theme={null}
# From your Backstage root directory
yarn --cwd packages/backend add @backstage/plugin-auth-backend-module-github-provider
```

This will add the module to `packages/backend/package.json` dependencies:

```json theme={null}
"dependencies": {
  "@backstage/plugin-auth-backend": "^0.24.2",
  "@backstage/plugin-auth-backend-module-github-provider": "^0.3.0",
  "@backstage/plugin-auth-backend-module-guest-provider": "^0.2.4"
}
```

Register the provider in your backend entrypoint (`packages/backend/src/index.ts`) by adding it to the backend registry:

```ts theme={null}
// packages/backend/src/index.ts (excerpt)
import { createBackend } from '@backstage/backend-defaults';

const backend = createBackend();

backend.add(import('@backstage/plugin-app-backend'));
backend.add(import('@backstage/plugin-proxy-backend'));
backend.add(import('@backstage/plugin-scaffolder-backend'));
// ...
backend.add(import('@backstage/plugin-auth-backend'));
backend.add(import('@backstage/plugin-auth-backend-module-github-provider'));

// other backend plugins...
backend.start();
```

<Callout icon="lightbulb">
  After installing a backend package, you must both add it to `packages/backend/package.json` and register it in the backend `index.ts` with `backend.add(...)`, then restart your backend.
</Callout>

## Configuring GitHub OAuth and Backstage auth

Create a GitHub OAuth App under GitHub → Settings → Developer settings → OAuth Apps. Set the callback URL to Backstage’s OAuth handler, for local development:

`http://localhost:7007/api/auth/github/handler/frame`

Add the client ID and client secret to your Backstage configuration. For development you can add them to `app-config.yaml`; for production use environment variables or a secrets store.

Example `auth` section in `app-config.yaml`:

```yaml theme={null}
auth:
  providers:
    github:
      development:
        clientId: ${AUTH_GITHUB_CLIENT_ID}
        clientSecret: ${AUTH_GITHUB_CLIENT_SECRET}
    guest: {}
```

After creating the OAuth app GitHub presents a client ID and lets you generate a client secret. Store these securely.

<Callout icon="warning">
  Do not commit OAuth client secrets to your repository. Use environment variables or a secrets manager (`AUTH_GITHUB_CLIENT_ID`, `AUTH_GITHUB_CLIENT_SECRET`) for production deployments.
</Callout>

<Frame>
  <img alt="A screenshot of the GitHub Developer settings for an OAuth application named &#x22;backstage.&#x22; It shows the client ID and a generated client secret along with buttons for transfer ownership, listing in the Marketplace, revoking tokens, and uploading an application logo." />
</Frame>

## Annotate your component with the repository project slug

To map a Backstage component to a GitHub repository, add the `github.com/project-slug` annotation to the component's `catalog-info.yaml`. The slug is typically `owner/repo` (for example, `backstage/backstage`).

Example `catalog-info.yaml` excerpt:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: backstage
  description: backstage.io
  annotations:
    github.com/project-slug: 'backstage/backstage'
spec:
  type: website
  lifecycle: production
  owner: user:guest
```

Commit and push the updated `catalog-info.yaml`. Backstage will refresh the entity and, if correctly configured, the GitHub Actions tab will appear and show workflow runs for the annotated repository.

You can find the repository slug on the GitHub repo page.

<Frame>
  <img alt="A screenshot of a GitHub repository page for a demo app, showing a list of folders and files (e.g., .github/workflows, src, tests, package.json) in the main pane and repo details and language/activity stats in the right sidebar. The top navigation (Code, Issues, Pull requests, etc.) is also visible." />
</Frame>

## Using the plugin in Backstage

When you visit the component's CI/CD tab, the plugin will trigger an authentication prompt handled by the backend provider. After authorizing with GitHub, the plugin will list workflow runs and provide links to the GitHub run detail pages and step logs. The experience mirrors what you get in GitHub Actions but embedded inside Backstage.

<Frame>
  <img alt="A screenshot of a GitHub Actions workflow run page showing a successful &#x22;test&#x22; job. The dark log pane lists steps like &#x22;Set up job&#x22;, &#x22;Checkout code&#x22;, &#x22;Setup Node.js&#x22; and &#x22;Post Setup Node.js&#x22;." />
</Frame>

## Key takeaways

* Community plugins may be frontend-only or include backend parts. The repository structure clarifies which is which.
* Frontend plugins are installed into `packages/app`; backend plugins and auth modules go in `packages/backend`.
  * Example: `yarn --cwd packages/app add @backstage-community/plugin-github-actions`
  * Example: `yarn --cwd packages/backend add @backstage/plugin-auth-backend-module-github-provider`
* Backend modules must be registered with `backend.add(import('...'))` in `packages/backend/src/index.ts` and require a backend restart.
* Many frontend plugins rely on backend auth modules or proxies to keep API tokens secret.
* Annotate components with `github.com/project-slug: 'owner/repo'` to enable CI/CD data for that entity.

Plugins can render in multiple ways:

* A full-page plugin (own route)
* A tab inside an entity page (like CI/CD)
* A small card or block on an entity page

Explore the community plugins repository and each plugin’s README for provider-specific setup instructions.

<Frame>
  <img alt="A screenshot of the Backstage Documentation page showing a list of two services (recommendation-service and shopping-cart) with a left navigation menu, search bar, and filters." />
</Frame>

## Links and references

* Backstage plugins: [https://backstage.io/plugins](https://backstage.io/plugins)
* Backstage community plugins repository: [https://github.com[AWS_SECRET_ACCESS_KEY]](https://github.com[AWS_SECRET_ACCESS_KEY])
* Backstage authentication docs: [https://backstage.io/docs/auth](https://backstage.io/docs/auth)
* GitHub OAuth apps: [https://github.com/settings/developers](https://github.com/settings/developers)

For further customization, consult the specific community plugin README and Backstage developer documentation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/aad867ea-baf2-4ca7-b722-ad38ea794a7e/lesson/1e3ae2bd-4bb1-4a35-b0af-8f7c5f2129f8" />
</CardGroup>


# Demo Customizing UI Part 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Customization-Plugins/Demo-Customizing-UI-Part-2/page

Shows how to add a SidebarItem to Backstage Root.tsx linking to /catalog-import and explains routes, permissions, and sidebar customization.

In this lesson you'll add a direct sidebar link in Backstage that navigates straight to the "Register existing component" page. The goal is to illustrate how Backstage pages map to routes and how to modify the sidebar (Root.tsx) to add a new `SidebarItem` that points to `/catalog-import`.

<Frame>
  <img alt="A screenshot of the Backstage &#x22;Create a new component&#x22; dialog showing a search box and a list of scaffolder templates (generated IDs, Example Node.js Template, app3, example-grpc-api, shopping-cart). The modal is overlaid on a dark left navigation with items like Home, APIs, and Docs." />
</Frame>

Overview

* Backstage renders each page as a React component.
* Navigation is implemented by mapping URL paths to components using React Router.
* The left sidebar is defined in `Root.tsx` — add or update `SidebarItem` entries there.

How Backstage routes map to pages
Every page in Backstage has a unique URL path. When the browser navigates to a path, React Router renders the corresponding React component. Use `FlatRoutes` / `Route` elements to wire a path to a page component.

Common page paths in this example:

| Page                                         | Path                                        |
| -------------------------------------------- | ------------------------------------------- |
| Home (Catalog index)                         | `/catalog`                                  |
| APIs (API docs)                              | `/api-docs`                                 |
| Docs (TechDocs index/reader)                 | `/docs` or `/docs/:namespace/:kind/:name/*` |
| Create (Scaffolder)                          | `/create`                                   |
| Register existing component (Catalog Import) | `/catalog-import`                           |

Example route configuration (from `App.tsx`)

```tsx theme={null}
// App.tsx (relevant parts)
import React from 'react';
import { Navigate, Route } from 'react-router-dom';
import { FlatRoutes } from '@backstage/core-app-api';
import {
  CatalogIndexPage,
  CatalogEntityPage,
} from '@backstage/plugin-catalog';
import { TechDocsIndexPage, TechDocsReaderPage } from '@backstage/plugin-techdocs';
import { ScaffolderPage } from '@backstage/plugin-scaffolder';
import { ApiExplorerPage } from '@backstage/plugin-api-docs';
import { CatalogImportPage } from '@backstage/plugin-catalog-import';
import { RequirePermission } from '@backstage/core-components';
import { catalogEntityCreatePermission } from '@backstage/plugin-catalog';

const routes = (
  <FlatRoutes>
    <Route path="/" element={<Navigate to="/catalog" replace />} />
    <Route path="/catalog" element={<CatalogIndexPage />} />
    <Route path="/catalog/:namespace/:kind/:name" element={<CatalogEntityPage />}>
      {/* entityPage routes / sub-routes go here */}
    </Route>

    <Route path="/docs" element={<TechDocsIndexPage />} />
    <Route path="/docs/:namespace/:kind/:name/*" element={<TechDocsReaderPage />} />

    <Route path="/create" element={<ScaffolderPage />} />
    <Route path="/api-docs" element={<ApiExplorerPage />} />

    <Route
      path="/catalog-import"
      element={
        <RequirePermission permission={catalogEntityCreatePermission}>
          <CatalogImportPage />
        </RequirePermission>
      }
    />
  </FlatRoutes>
);

export default routes;
```

Notes

* A `Navigate` at `/` commonly redirects users to a landing page (here `/catalog`).
* Protect sensitive pages (like `catalog-import`) with permission checks (`RequirePermission`).

Where to update the sidebar: Root.tsx
The sidebar lives in `src/components/Root/Root.tsx`. Sidebar navigation is built with components such as `SidebarGroup` and `SidebarItem`. Each `SidebarItem` accepts props like `icon`, `to`, and `text` to control where it navigates and how it appears.

Example excerpt from `Root.tsx` showing the existing menu:

```tsx theme={null}
// src/components/Root/Root.tsx (excerpt)
import React, { PropsWithChildren } from 'react';
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core';
import HomeIcon from '@material-ui/icons/Home';
import ExtensionIcon from '@material-ui/icons/Extension';
import LibraryBooksIcon from '@material-ui/icons/LibraryBooks';
import CreateComponentIcon from '@material-ui/icons/AddCircleOutline';
import {
  SidebarPage,
  Sidebar,
  SidebarLogo,
  SidebarGroup,
  SidebarItem,
  SidebarDivider,
  SidebarScrollWrapper,
} from '@backstage/core-components';
import LogoFull from './LogoFull';
import LogoIcon from './LogoIcon';
import { SidebarSearchModal } from '@backstage/plugin-search';
import SearchIcon from '@material-ui/icons/Search';
import GroupIcon from '@material-ui/icons/Group';

export const Root = ({ children }: PropsWithChildren<{}>) => (
  <SidebarPage>
    <Sidebar>
      <SidebarLogo />
      <SidebarGroup label="Search" icon={<SearchIcon />} to="/search">
        <SidebarSearchModal />
      </SidebarGroup>

      <SidebarDivider />

      <SidebarGroup label="Menu" icon={<HomeIcon />}>
        {/* Global nav, not org-specific */}
        <SidebarItem icon={<HomeIcon />} to="/catalog" text="Home" />
        <SidebarItem
          singularTitle="My Group"
          pluralTitle="My Groups"
          icon={<GroupIcon />}
        />
        <SidebarItem icon={<ExtensionIcon />} to="/api-docs" text="APIs" />
        <SidebarItem icon={<LibraryBooksIcon />} to="/docs" text="Docs" />
        <SidebarItem icon={<CreateComponentIcon />} to="/create" text="Create..." />
      </SidebarGroup>

      <SidebarDivider />
      <SidebarScrollWrapper>{children}</SidebarScrollWrapper>
    </Sidebar>
  </SidebarPage>
);
```

Add a direct link to "Register existing component"
To add a sidebar link that navigates directly to the Catalog Import page (`/catalog-import`):

1. Import an icon (e.g., Material UI's `AssignmentReturned`):

```tsx theme={null}
import AssignmentReturnedIcon from '@material-ui/icons/AssignmentReturned';
```

2. Add a `SidebarItem` inside the "Menu" `SidebarGroup` near the other top-level items:

```tsx theme={null}
<SidebarItem
  icon={<AssignmentReturnedIcon />}
  to="/catalog-import"
  text="Register"
/>
```

Complete snippet in context:

```tsx theme={null}
// inside the SidebarGroup labeled "Menu"
<SidebarItem icon={<ExtensionIcon />} to="/api-docs" text="APIs" />
<SidebarItem icon={<LibraryBooksIcon />} to="/docs" text="Docs" />
<SidebarItem icon={<CreateComponentIcon />} to="/create" text="Create..." />
<SidebarItem icon={<AssignmentReturnedIcon />} to="/catalog-import" text="Register" />
```

After saving and restarting (or rebuilding) your Backstage app, the new "Register" sidebar link will appear and navigate directly to `/catalog-import`, streamlining the Create → Register flow.

<Frame>
  <img alt="A split-screen screenshot showing a code editor (Visual Studio Code) with a project file tree and TypeScript code on the left, and a web UI for &#x22;My Company Catalog&#x22; (Backstage) displaying a table of components on the right. The left panel shows folders like src/components/Root, while the right shows component names, owners, types, and lifecycle statuses." />
</Frame>

<Callout icon="lightbulb">
  Tip: Use a distinct icon and clear label to make the new link discoverable. Keep `SidebarItem` placement near related items so users learn the menu layout quickly.
</Callout>

Permission considerations

* The Catalog Import page (`/catalog-import`) typically requires a permission check such as `catalogEntityCreatePermission`. If you add the sidebar link but users lack permission, they’ll be prevented from accessing the page.
* Wrap the target page in `RequirePermission` (as shown in the routes example) to enforce access control.

<Callout icon="warning">
  Important: If you add a `SidebarItem` that points to a protected route, ensure the route itself enforces permissions. The sidebar link does not implicitly grant access.
</Callout>

Visual confirmation of the change
The screenshots below demonstrate the code edits in VS Code and the resulting direct navigation to the "Register an existing component" page.

<Frame>
  <img alt="A split-screen screenshot showing a code editor (VS Code) with a project/file explorer and TypeScript/React files on the left, and the Backstage &#x22;Register an existing component&#x22; web UI (URL input and instructions) open in a browser on the right." />
</Frame>

Summary & next steps

* Backstage pages are React components mapped to routes — update `App.tsx` (or equivalent) to wire new pages.
* Modify `Root.tsx` to change or add sidebar entries using `SidebarItem`, `SidebarGroup`, and `SidebarDivider`.
* Use the `to` prop to point `SidebarItem` at the route you want (e.g., `/catalog-import`).
* Choose distinct icons and labels to improve usability.
* Ensure protected pages enforce permissions using `RequirePermission`.

References

* Backstage docs: [https://backstage.io/docs](https://backstage.io/docs)
* React Router: [https://reactrouter.com/](https://reactrouter.com/)
* Backstage core components: [https://backstage.io/docs/components/core-features](https://backstage.io/docs/components/core-features)

This change is standard React work inside a Backstage app — once you understand routes and `Root.tsx` you can customize the UI to match your team's workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/aad867ea-baf2-4ca7-b722-ad38ea794a7e/lesson/be06c121-f4fc-4356-be75-81d42ca1778c" />
</CardGroup>
