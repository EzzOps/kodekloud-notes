# Start dev server
> yarn dev
[app]: Loaded config from app-config.yaml
[app]: NOTE: Did not compute git version or commit hash, could not execute the git command line utility
[app]: [webpack-dev-server] Project is running at: http://localhost:3000/
[backend]: Loading config from MergedConfigSource{FileConfigSource{path="/root/demo/backstage/app-config.yaml"}, FileConfigSource{path="/root/demo/backstage/app-config.local.yaml"}, EnvConfigSource{count=0}}
[backend]: 2025-02-13T00:04:45.134Z rootHttpRouter info Listening on :7007
[backend]: 2025-02-13T00:04:45.136Z backstage info Plugin initialization started
```

You may see the browser show a connection refused error when navigating to the server IP on port 3000 (because `app.baseUrl` is `localhost`):

<Frame>
  <img alt="A Chrome browser window displaying a &#x22;This site can't be reached&#x22; error (147.182.170.10 refused to connect, ERR_CONNECTION_REFUSED) with a reload button and troubleshooting suggestions. The address bar and several tabs are visible at the top and a teal mouse cursor is near the bottom right." />
</Frame>

Initial (problematic) app-config snippet

```yaml theme={null}
app:
  title: Scaffolded Backstage App
  baseUrl: http://localhost:3000

organization:
  name: My Company

backend:
  # Used for enabling authentication, secret is shared by all
  # backend plugins
  # See https://backstage.io/docs/auth/service-to-service-auth for
  # information on the format
  # auth:
  #   keys:
  #     - secret: ${BACKEND_SECRET}
```

Fix: update the shared app-config to use the server IP or DNS
Follow these steps to allow external browser access and correct frontend↔backend communication:

1. Set `app.baseUrl` to the server IP or DNS with port `3000`.
2. Set `backend.baseUrl` to the same server IP or DNS with port `7007`.
3. Configure the backend `listen.host` to `0.0.0.0` (or remove `host` to bind all interfaces) so it accepts external connections.
4. Add the frontend origin to `backend.cors.origin` so the browser is allowed to call the backend.

Example updated `app-config.yaml` for this demo (replace `147.182.170.10` with your server IP or DNS name):

```yaml theme={null}
app:
  title: Scaffolded Backstage App
  baseUrl: http://147.182.170.10:3000

organization:
  name: My Company

backend:
  # Used for enabling authentication, secret is shared by all
  # backend plugins
  # See https://backstage.io/docs/auth/service-to-service-auth for
  # information on the format
  # auth:
  #   keys:
  #     - secret: ${BACKEND_SECRET}
  baseUrl: http://147.182.170.10:7007
  listen:
    host: 0.0.0.0
    port: 7007
  cors:
    origin:
      - http://147.182.170.10:3000

csp:
  connect-src: ["'self'", 'http:', 'https:']
```

Configuration quick reference

| Setting               | Purpose                                               | Example value (demo)         |
| --------------------- | ----------------------------------------------------- | ---------------------------- |
| `app.baseUrl`         | URL advertised to users and used for frontend routing | `http://147.182.170.10:3000` |
| `backend.baseUrl`     | Backend URL used by frontend for API calls            | `http://147.182.170.10:7007` |
| `backend.listen.host` | Interface the backend binds to                        | `0.0.0.0`                    |
| `backend.cors.origin` | Allowed origins for browser requests                  | `http://147.182.170.10:3000` |

Note: If you have a DNS name for your server, prefer that instead of a raw IP address for better maintainability and SSL/HTTPS compatibility.

Restart the dev server
After changing configuration files you must restart Backstage to load the new settings.

Steps:

1. Stop the running dev server (Ctrl+C in the terminal; press again if necessary to force exit).
2. Start it again:

```bash theme={null}
yarn dev
```

You should see the backend and frontend log successful startup and listening on the configured addresses. After restarting, the frontend should be reachable at `http://147.182.170.10:3000` and be able to communicate with the backend at `http://147.182.170.10:7007`.

Using app-config.local.yaml for local overrides

* Prefer placing machine-specific or development-only overrides in `app-config.local.yaml` so the shared `app-config.yaml` remains suitable across environments.
* Backstage merges configuration files; `app-config.local.yaml` (if present during development) overrides keys in `app-config.yaml`.

Example `app-config.local.yaml` with minimal overrides:

```yaml theme={null}
app:
  baseUrl: http://147.182.170.10:3000

backend:
  baseUrl: http://147.182.170.10:7007
  cors:
    origin:
      - http://147.182.170.10:3000
```

Restore the shared `app-config.yaml` to scaffold defaults for portability:

```yaml theme={null}
app:
  title: Scaffolded Backstage App
  baseUrl: http://localhost:3000

organization:
  name: My Company

backend:
  # Shared defaults; local overrides will take precedence in dev
  baseUrl: http://localhost:7007
  listen:
    port: 7007
```

Because `app-config.local.yaml` has precedence in development, the effective configuration used by `yarn dev` is the merge of `app-config.yaml` and the local overrides. After creating or modifying `app-config.local.yaml`, restart the dev server.

> **lightbulb** Use `app-config.local.yaml` for developer- or machine-specific settings (like using an external IP for a demo server). Keep `app-config.yaml` for defaults shared among environments, and use production-specific files (e.g., `app-config.production.yaml`) when deploying to production.

Security reminder

> **warning** Exposing a development server on a public IP can expose sensitive endpoints or secrets. Avoid using production secrets in development configs and secure access with firewall rules or VPNs when demoing externally.

Troubleshooting checklist

* Confirm the server firewall/security group allows ports `3000` and `7007`.
* Verify Backstage logs show the backend listening on `0.0.0.0:7007` (or expected host/port).
* Inspect browser DevTools Console and Network tab for CORS errors; adjust `backend.cors.origin` as needed.
* If the frontend still advertises `localhost`, clear caches and ensure `yarn dev` restarted after config changes.

Summary

* The frontend refused external connections because `app.baseUrl` was set to `localhost`. The backend may also have been bound only to localhost or rejected cross-origin requests.
* Update `app.baseUrl`, `backend.baseUrl`, and `backend.cors.origin` to the server IP or DNS name and ensure the backend binds to an interface that accepts external connections.
* Prefer `app-config.local.yaml` for local overrides to keep shared configuration environment-agnostic.
* Always restart Backstage after modifying configuration and double-check firewall and CORS settings.

References and further reading

* Backstage Configuration: [https://backstage.io/docs/configuration/overview](https://backstage.io/docs/configuration/overview)
* Backstage Dev Mode: [https://backstage.io/docs/development/dev-setup](https://backstage.io/docs/development/dev-setup)
* CORS and browser security: [https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/fcbbf923-69c3-4147-bd51-18db2bd18957/lesson/2093a42d-0510-427e-b3c3-2f1e3c932bd4)


# Demo Exploring Backstage

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Backstage-Basics/Demo-Exploring-Backstage/page

Overview demo of Backstage showing its catalog, component and API pages, relations graph, TechDocs, templates and scaffolding, search, settings, and ownership navigation.

In this lesson we walk through Backstage and inspect its primary features: the Catalog, entities (Components, APIs, Groups, Users, Systems), TechDocs (documentation), templates and scaffolding, search, and Settings. With Backstage running you can navigate the UI to discover ownership, relationships, source links, and documentation for your organization’s software.

## Home / My Company Catalog

The Home page opens to the "My Company Catalog" — the central index of every software entity your organization manages. Use the catalog to discover components, APIs, systems, groups, and users, and to filter views by kind, owner, lifecycle, or other metadata.

In this demo instance there is a single registered application: `example-website`. The catalog card shows metadata such as owner (a group named `guests` in this demo), kind (Component), component type (Website), and lifecycle (Experimental). You can switch filters to list Users, Groups, or APIs as needed.

<Frame>
  <img alt="A web application dashboard titled &#x22;My Company Catalog&#x22; with a left sidebar menu and a filter dropdown set to &#x22;Component.&#x22; The main pane shows an &#x22;All Components (1)&#x22; list containing one item named &#x22;example-website.&#x22;" />
</Frame>

Click the `example-website` card to open its component details page.

## Component details and relations

The component details page combines overview metadata, navigation to source or docs, and a relations graph that visualizes ownership, system membership, provided and consumed APIs, and subcomponents. The relations graph is one of Backstage’s most powerful discovery tools for understanding architecture and team responsibilities.

<Frame>
  <img alt="A screenshot of the Backstage web UI showing a component page for &#x22;example-website,&#x22; with an About panel on the left and a Relations graph on the right. The left sidebar shows navigation items like Home, APIs, and Docs." />
</Frame>

A typical component entity in Backstage looks like this:

```yaml theme={null}
apiVersion: backstage.io/v1beta1
kind: Component
metadata:
  name: example
  links:
    - url: https://dashboard.example.com
      title: My Dashboard
      icon: dashboard
spec:
  type: website
  lifecycle: experimental
  owner: group:guests
```

In the relations graph for this component you’ll see:

* Ownership: `group:guests`
* System membership: `examples`
* Provided API: `example-grpc-api`
* Subcomponents (if any)

Clicking an API node in the graph navigates to the API entity page. You can also filter the catalog by API kind to find API entries directly.

## API entity page and API definitions

The API entity view displays owner, lifecycle, relations, and—where available—the API definition itself (for example, gRPC proto files or OpenAPI specs). Backstage renders common API formats to make exploration and onboarding easy.

<Frame>
  <img alt="A screenshot of the Backstage web UI displaying an API entity page titled &#x22;example-grpc-api.&#x22; The page shows an About panel with owner/lifecycle details on the left and a Relations graph on the right." />
</Frame>

Example gRPC (proto3) service definition:

```protobuf theme={null}
syntax = "proto3";

service ExampleService {
  rpc Example (ExampleMessage) returns (ExampleMessage) {}
}

message ExampleMessage {
  string example = 1;
}
```

For REST APIs, Backstage will surface OpenAPI (Swagger) specs or other supported API documentation formats in the same view, enabling quick inspection and navigation.

## Home overview, users, and groups

The Home tab provides quick access to every entity type. Key points:

* Users: lists individual users (e.g., `guest`).
* Groups: shows groups and the components they own — useful to understand team responsibilities.
* Ownership in Backstage must reference either a user or a group string, for example `user:alice` or `group:frontend-team`.

> **lightbulb** Ownership must be assigned to an individual (`user:...`) or a group (`group:...`). Use consistent naming to keep ownership and the relations graph accurate.

## Documentation (TechDocs) and global search

TechDocs (Backstage documentation) is available from component and API pages via the docs icon, or from the global Docs view. The top search bar indexes both catalog metadata and TechDocs content so you can find components, APIs, teams, and documentation from a single place.

Searching for the term "example" in this demo returns the example website, the example API, and any TechDocs pages that contain the term.

<Frame>
  <img alt="Screenshot of a Backstage documentation search overlay showing results for the query &#x22;example&#x22; (e.g., &#x22;Example Node.js Template&#x22;, &#x22;example-website&#x22;). The app has a dark left sidebar with navigation items like Home, APIs, and Docs." />
</Frame>

## Create — Templates and scaffolding

The Create workflow launches Backstage templates used to scaffold new projects (applications, libraries, services) consistently. Templates collect inputs (project name, owner, repository location) and provision code and metadata according to your organization’s standards. In this demo you’ll find an Example Node.js template.

<Frame>
  <img alt="A screenshot of the Backstage web interface on the &#x22;Create a new component&#x22; page showing a Templates section with an &#x22;Example Node.js Template&#x22; card. The page also shows a left navigation menu and a &#x22;Register Existing Component&#x22; button." />
</Frame>

Templates are a core automation feature — explore them to standardize onboarding, CI/CD, repository layout, and scaffolding across teams.

## Settings, appearance, and authentication

The Settings page controls UI-level preferences: appearance (Light/Dark theme), profile details, authentication providers, and feature flags. These options let individuals and organizations tune Backstage behavior and sign-in methods.

<Frame>
  <img alt="Screenshot of the Backstage web app Settings page, showing a user Profile card and Backstage Identity panel on the left and Appearance options (Light/Dark theme toggle and pin sidebar) on the right, with a dark left navigation menu." />
</Frame>

Adjust settings to match your personal preferences or organization defaults (e.g., default theme and sidebar behavior).

## Stars, Owned filter, and quick access

* Star frequently used components to access them quickly (Show starred components).
* The Owned filter shows only components owned by your user or group. If your account isn’t a member of any group, the Owned filter may be disabled until group membership is configured.

## Useful internal links and example catalog query

Backstage catalog pages are addressable via URL parameters so you can link directly to filtered views or specific entity pages.

Example filtered catalog query (replace the host and parameters to match your installation):

`147.182.170.10:3000/catalog?filters%5Bkind%5D=api&filters%5Buser%5D=all&limit=20`

Table — Common catalog entity kinds and examples:

| Entity Type | Use Case                                       | Example            |
| ----------- | ---------------------------------------------- | ------------------ |
| Component   | Software components (apps, services, websites) | `example-website`  |
| API         | API definitions (gRPC, OpenAPI)                | `example-grpc-api` |
| Group       | Team or organization unit that owns components | `group:guests`     |
| User        | Individual developer account                   | `user:alice`       |
| System      | Collection of related components               | `examples`         |

## Links and references

* Backstage project: [https://backstage.io](https://backstage.io)
* Backstage Catalog docs: [https://backstage.io/docs/features/software-catalog/what-is-software-catalog](https://backstage.io/docs/features/software-catalog/what-is-software-catalog)
* Backstage TechDocs: [https://backstage.io/docs/features/techdocs/what-is-techdocs](https://backstage.io/docs/features/techdocs/what-is-techdocs)
* Backstage Scaffolder (Templates): [https://backstage.io/docs/features/software-templates/using-templates](https://backstage.io/docs/features/software-templates/using-templates)

## Wrap-up

You’ve explored the Backstage Catalog, component and API entity pages, relations graphs, TechDocs search, templates/scaffolding, and settings. Next steps:

* Open a component or API and inspect its relations graph.
* Browse TechDocs content and try the global search.
* Create a new component using a template to experience the scaffolding workflow.

Further hands-on exploration will deepen your understanding of Backstage and how it centralizes software metadata, documentation, and developer workflows.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/fcbbf923-69c3-4147-bd51-18db2bd18957/lesson/2fb83ce7-f036-4c36-8faf-35a4c24d5096)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/fcbbf923-69c3-4147-bd51-18db2bd18957/lesson/ab74222d-b1db-4adc-8205-098552e46ba6)
