# examples/Entities.yaml (excerpt)
owner: guests
---
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: example-website
spec:
  type: website
  lifecycle: experimental
  owner: guests
  system: examples
  providesApis: [example-grpc-api]
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: example-grpc-api
spec:
  type: grpc
  lifecycle: experimental
  owner: guests
  system: examples
  definition: |
    syntax = "proto3";
```

This is why the Catalog UI shows example components — they are imported from that file.

## Registering a real component (auth service)

Below is a minimal Node.js Express service that we'll register with Backstage:

```javascript theme={null}
import express from "express";

const app = express();

app.get("/", (req, res) => {
  res.send("Hello World!");
});

const port = 3000;
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
```

To register this service, create a `catalog-info.yaml` at the root of your project describing the component. The required fields are `apiVersion`, `kind`, `metadata`, and `spec`. Example:

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
```

Notes:

* `spec.type` is a free-form string; teams should agree on a consistent taxonomy (e.g., `service`, `website`, `library`) so catalog browsing and filtering remain useful.
* `owner` should point to an existing user or group entity in the Catalog. The default Backstage instance includes example entities such as `guest` and `guests`; this is why `guests` works in examples.

When the auth component is present in the Catalog, Backstage displays its metadata (owner, type, lifecycle, tags, and links):

<Frame>
  <img alt="A screenshot of the Backstage &#x22;My Company Catalog&#x22; web UI showing a table of two components (auth-service and example-website) with columns for owner, type, lifecycle, and tags. The page includes a left navigation sidebar, filters on the left, and a &#x22;CREATE&#x22; button plus a search field." />
</Frame>

## Four common ways to import a component into Backstage

* Static import from the Backstage repository (local file)
* Static import from a URL (e.g., a `catalog-info.yaml` stored on GitHub)
* Register via the Backstage UI (Register Existing Component)
* Automatic registration via templates or repository-scanning integrations

A concise overview:

| Method                   | When to use                                                    | Example                                                                                  |
| ------------------------ | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Local `file` import      | For local/backstage-repo-driven demos or self-hosted examples  | Add `- type: file` with `target: ../../examples/auth-entity.yaml` in `app-config.yaml`   |
| Remote `url` import      | When `catalog-info.yaml` lives with your source code in a repo | Add `- type: url` with `target: https://github.com/you/repo/blob/main/catalog-info.yaml` |
| UI registration          | Quick one-off imports without editing backend config           | Use "Register Existing Component" in Backstage and paste the `catalog-info.yaml` URL     |
| Templates / integrations | For automated at-scale registration across many repos          | Use scaffolding templates or code host scanning/integrations                             |

### Static import (local file)

1. Save your `catalog-info.yaml` as a local entity file, for example `examples/auth-entity.yaml`.
2. Add a `file` location to `app-config.yaml` (paths are relative to `packages/backend`):

```yaml theme={null}
catalog:
  import:
    entityFilename: catalog-info.yaml
    pullRequestBranchName: backstage-integration
  rules:
    - allow: [Component, System, API, Resource, Location]
  locations:
    - type: file
      target: ../../examples/Entities.yaml

    - type: file
      target: ../../examples/auth-entity.yaml

    - type: file
      target: ../../examples/template/template.yaml
      rules:
        - allow: [Template]
```

3. Restart the Backstage backend (or `yarn dev` in development). After the backend restarts, the new component should appear in the Catalog.

### Static import (from GitHub)

A common pattern is to keep `catalog-info.yaml` in the same repository as the service and let Backstage import it via URL.

Example Git commands to push your project to GitHub:

```bash theme={null}
echo "# backstage-auth-service" >> README.md
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Sanjeev-Thiyagarajan/backstage-auth-service.git
git push -u origin main
```

Add the remote `catalog-info.yaml` as a `url` location in `app-config.yaml`:

```yaml theme={null}
catalog:
  import:
    entityFilename: catalog-info.yaml
    pullRequestBranchName: backstage-integration
  rules:
    - allow: [Component, System, API, Resource, Location]
  locations:
    - type: file
      target: ../../examples/Entities.yaml

    - type: url
      target: https://github.com/Sanjeev-Thiyagarajan/backstage-auth-service/blob/main/catalog-info.yaml

    - type: file
      target: ../../examples/template/template.yaml
      rules:
        - allow: [Template]
```

Restart the backend. When Backstage imports the entity from GitHub, the Catalog will show the `auth-service` entry and the provided repository link will be clickable.

<Frame>
  <img alt="A screenshot of a GitHub repository page showing a file list (folders like openapi and src and files such as .gitignore and package.json) with a prompt to add a README. The right sidebar shows repo details and language stats (JavaScript) along with suggested workflows." />
</Frame>

## Entity updates and refresh behavior

* Backstage polls configured locations on a schedule (the default may be tens of minutes). If you change the `catalog-info.yaml` in GitHub, the Catalog might not reflect the change immediately.
* To fetch updates sooner, use the Catalog UI's refresh action for the entity; this schedules a refresh run for that location.

Example: change the `owner` in GitHub from `guests` to `auth-team`:

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
  owner: auth-team
```

If `auth-team` is not present as a group entity in the Catalog, Backstage will surface a missing-relation warning on the component page. The default Backstage example includes `guest` and `guests` entities; here's the example `org.yaml` that provides them:

```yaml theme={null}
---
apiVersion: backstage.io/v1alpha1
kind: User
metadata:
  name: guest
spec:
  memberOf: [guests]
---
apiVersion: backstage.io/v1alpha1
kind: Group
metadata:
  name: guests
spec:
  type: team
  children: []
```

If you reference a non-existent owner like `auth-team`, either add a corresponding group entity or reference an existing group location in `app-config.yaml`.

## Inspecting and unregistering entities

* From the Catalog UI you can inspect an entity, view its raw YAML/JSON, and perform actions like unregistering the entity.
* Unregistering removes the location Backstage used to import the entity (file or URL).

<Frame>
  <img alt="A screenshot of the Backstage developer portal showing an &#x22;auth-service&#x22; component page with Overview/About and Relations panels, a warning about missing related entities, and a dropdown menu with actions like &#x22;Unregister entity.&#x22;" />
</Frame>

## Registering via the UI

Alternatively, use the Backstage UI to "Register Existing Component" and paste the URL to your `catalog-info.yaml`. Backstage will analyze the entity and show what will be imported; you can then import it directly without editing backend config.

<Frame>
  <img alt="A screenshot of the Backstage web UI's &#x22;Create a new component&#x22; page showing a Templates panel with an &#x22;Example Node.js Template&#x22; card and a left-hand navigation menu. The page includes search and filter controls and a &#x22;Register Existing Component&#x22; button." />
</Frame>

## Templates and repository scanning

* Scaffolding templates can create and register `catalog-info.yaml` automatically when you generate new projects.
* Integrations and code-host scanning allow Backstage to discover `catalog-info.yaml` files across many repositories and import them at scale.

## Summary — choosing an approach

1. Add a local `file` location in `app-config.yaml` and restart the backend — useful for demos and local Backstage repo examples.
2. Add a `url` location pointing to a remote `catalog-info.yaml` and restart the backend — recommended for production repositories.
3. Use the Backstage UI (“Register Existing Component”) to import an entity by URL — convenient for quick imports.
4. Use templates or repository-scanning integrations to auto-create and register `catalog-info.yaml` files across many repositories.

<Callout icon="lightbulb">
  After changing `app-config.yaml`, restart the Backstage backend (or `yarn dev` when developing) so new locations are picked up. If you update a `catalog-info.yaml` in a remote repository, use the Catalog's refresh action to fetch updates sooner than the configured polling interval.
</Callout>

## Links and references

* Backstage Catalog documentation: [https://backstage.io/docs/features/software-catalog/what-is-the-software-catalog](https://backstage.io/docs/features/software-catalog/what-is-the-software-catalog)
* Backstage entity model overview: [https://backstage.io/docs/features/software-catalog/descriptor-format](https://backstage.io/docs/features/software-catalog/descriptor-format)
* Backstage scaffolder & templates: [https://backstage.io/docs/features/software-templates/creating-templates](https://backstage.io/docs/features/software-templates/creating-templates)

This completes the demo for registering a component with Backstage.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/f9244f9d-083a-4acd-a518-549f54b644b5/lesson/f07e27d6-12c8-4688-a61b-a1fc9df9b291" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/f9244f9d-083a-4acd-a518-549f54b644b5/lesson/71558f5a-be40-4d55-836f-2d73ac1c8aea" />
</CardGroup>


# Demo Relationships

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Catalog/Demo-Relationships/page

Guide demonstrating how to model and register Backstage catalog entities and relationships, including components, groups, users, systems, domains, resources, ownership and dependencies

This guide demonstrates how to model and register Backstage catalog entities and their relationships: Components, Groups, Users, Systems, Domains, and Resources. You will create example entities—`shopping-cart`, `inventory`, `ecommerce` group, user `john`, `purchasing` system, `shopping-app` domain, and `inventory-db` resource—and wire ownership and dependency relationships between them.

What you'll learn:

* How to author entity descriptors (YAML) for common Backstage kinds
* How to import entities into the Backstage catalog
* How to express ownership, system membership, and dependency relationships
* How to update `app-config.yaml` import rules when a kind is blocked

***

## 1. Create a Component (shopping-cart)

Create a simple website component descriptor named `shopping-cart`. Save this YAML into the repository you use for Backstage catalog imports (for example `entity.yaml`):

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: shopping-cart
spec:
  type: website
  lifecycle: production
  owner: guests
```

Commit and push the file:

```bash theme={null}
git add entity.yaml
git commit -m "Add shopping-cart component"
git push origin main
```

Then open the repository on GitHub to confirm the entity file is present.

<Frame>
  <img alt="A screenshot of a GitHub repository page for &#x22;backstage-guest-user-domain-system&#x22; showing the main branch, a highlighted entity.yaml file, and a prompt to &#x22;Add a README.&#x22;" />
</Frame>

***

## 2. Register the component in Backstage

In Backstage, go to Create → Register Existing Component and point to the GitHub repo URL (or your configured file location). If Backstage previously fetched the file and returned an error due to a transient issue (such as a typo you already fixed), wait a minute and try Analyze again.

<Callout icon="lightbulb">
  Backstage may cache a location's content for a short period. If you fixed a typo in your repository and the UI still shows the old error, wait a minute and click Analyze again before re-importing.
</Callout>

<Frame>
  <img alt="A Backstage web UI showing the &#x22;Create a new component&#x22; page with a left navigation menu and a central Templates area. The main card displays an &#x22;Example Node.js Template&#x22; with search and filter options on the left." />
</Frame>

If the UI or backend returns an InputError indicating an unrecognized kind or apiVersion, it usually means a typo in the YAML or that the catalog import rules for that location don't permit the kind. Example backend error (keep JSON inside a code block to avoid MDX parsing issues):

```json theme={null}
{
  "error": {
    "name": "InputError",
    "message": "InputError: No processor recognized the entity component:default/shopping-cart as valid, possibly caused by a foreign kind or apiVersion",
    "stack": "InputError: InputError: No processor recognized the entity component:default/shopping-cart as valid, possibly caused by a foreign kind or apiVersion\n at DefaultLocationService.processEntities (/root/demo/backstage/node_modules/@backstage/plugin-catalog-[SECRET_REDACTED].ts:110:15)\n at process.processTicksAndRejections (node:internal/process/task_queues:95:5)\n at DefaultLocationService.dryRunCreateLocation (/root/demo/backstage/node_modules/@backstage/plugin-catalog-[SECRET_REDACTED].ts:148:32)\n at <anonymous> (/root/demo/backstage/node_modules/@backstage/plugin-catalog-backend/src/service/createRouter.ts:322:24)"
  },
  "request": { "method": "POST", "url": "/locations?dryRun=true" },
  "response": { "statusCode": 400 }
}
```

Once Analyze succeeds, click Import to add the component to the catalog.

***

## 3. Define and import a Group (e-commerce)

You can include multiple YAML entities in a single file separated by `---`. Add a `Group` entity to the same file (or as a separate file) like this:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: shopping-cart
spec:
  type: website
  lifecycle: production
  owner: guests
---
apiVersion: backstage.io/v1alpha1
kind: Group
metadata:
  name: ecommerce
spec:
  type: team
  children: []
```

If importing the Group fails, it may be because your `app-config.yaml` import rules exclude `Group`. A default config might look like:

```yaml theme={null}
catalog:
  import:
    entityFilename: catalog-info.yaml
  rules:
    - allow: [Component, System, API, Resource, Location]
```

Add `Group` to the allowed list and restart Backstage:

```yaml theme={null}
catalog:
  import:
    entityFilename: catalog-info.yaml
  rules:
    - allow: [Component, System, API, Resource, Location, Group]
  locations:
    - type: file
      target: ../../examples/entities.yaml
```

<Callout icon="warning">
  Any changes to `app-config.yaml` require you to restart the Backstage dev server for the new rules to take effect.
</Callout>

After restarting, re-import the location. If you want faster iteration, unregister the location in the UI and register it again to force immediate processing.

<Frame>
  <img alt="A screenshot of the Backstage &#x22;My Company Catalog&#x22; web UI showing the &#x22;All Groups (1)&#x22; table with a single &#x22;guests&#x22; group. A green hand cursor points at the &#x22;guests&#x22; entry and a left navigation sidebar lists Home, APIs, Docs, and Create." />
</Frame>

You can review configured locations in Backstage under Catalog → Locations:

<Frame>
  <img alt="A screenshot of the Backstage web UI titled &#x22;My Company Catalog,&#x22; showing a left navigation sidebar and a green header. The main panel lists &#x22;All Locations (4)&#x22; with generated location entries, their types (file/url) and target paths." />
</Frame>

When import completes, the Register wizard will list the discovered entities ready to import:

<Frame>
  <img alt="Screenshot of the Backstage &#x22;Register an existing component&#x22; page showing a multi-step wizard that found a repository and added entities (including &#x22;shopping-cart&#x22;) to the catalog. The app's left navigation and instructions for linking a repository are visible." />
</Frame>

***

## 4. Create a User (john)

Backstage supports a `User` kind. Add this user entry to your entities file:

```yaml theme={null}
---
apiVersion: backstage.io/v1alpha1
kind: User
metadata:
  name: john
spec:
  memberOf: [ecommerce]
```

If `User` is not allowed for the location, you will see a NotAllowedError. Example:

```json theme={null}
{
  "error": {
    "name": "InputError",
    "message": "NotAllowedError: Entity user:default/john at url:https://github.com/.../entity.yaml is not of an allowed kind for that location.",
    "stack": "InputError: NotAllowedError: Entity user:default/john at url:... \n    at DefaultLocationService.processEntities (...)"
  },
  "request": { "method": "POST", "url": "/locations?dryRun=true" },
  "response": { "statusCode": 400 }
}
```

Add `User` (and any other required kinds like `Domain`) to `app-config.yaml` and restart Backstage:

```yaml theme={null}
catalog:
  import:
    entityFilename: catalog-info.yaml
  rules:
    - allow: [Component, System, API, Resource, Location, Group, User, Domain]
```

Once the user is imported, you can open `john`'s profile to see relations such as `memberOf: ecommerce` and any ownership cards.

<Frame>
  <img alt="A screenshot of the Backstage web UI showing a user profile page for &#x22;john&#x22; with an overview panel. The page shows an &#x22;ecommerce&#x22; relation and an Ownership card displaying a WEBSITE component." />
</Frame>

***

## 5. Set an owner to a User (owner reference format)

By default, `owner` values are interpreted as groups. To assign an individual user as owner, use a fully qualified entity reference such as `user:default/john` (or `user:john` if your location uses the default namespace). Example:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: shopping-cart
spec:
  type: website
  lifecycle: production
  owner: user:john
```

After updating and importing, `shopping-cart` will show `john` as owner.

***

## 6. Add another Component (inventory) and a dependency

Create an `inventory` component and make `shopping-cart` depend on it using `spec.dependsOn`. Place both components in the same file if convenient:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: shopping-cart
spec:
  dependsOn:
    - component: inventory
  type: website
  lifecycle: production
  owner: user:john
---
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: inventory
spec:
  type: service
  lifecycle: production
  owner: ecommerce
```

After importing, the `shopping-cart` component page will show a relation to the `inventory` component.

<Frame>
  <img alt="A Backstage web UI showing the &#x22;shopping-cart&#x22; component with an About panel on the left. On the right is a Relations graph linking the shopping-cart component to an inventory service." />
</Frame>

***

## 7. Create a System and associate components

Systems group components delivering a bounded feature set. Example `System` descriptor:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: purchasing
  description: system for managing user purchases
spec:
  owner: ecommerce
```

Associate components with the `purchasing` system by setting `system: purchasing` in their `spec`:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: inventory
spec:
  type: service
  lifecycle: production
  owner: ecommerce
  system: purchasing
```

Viewing the `purchasing` system in Backstage will list related components, APIs, and resources. See the Backstage docs for more descriptor examples:

* Descriptor format: [https://backstage.io/docs/features/software-catalog/descriptor-format](https://backstage.io/docs/features/software-catalog/descriptor-format)

<Frame>
  <img alt="A screenshot of the Backstage documentation page titled &#x22;Descriptor Format of Catalog Entities.&#x22; It shows a left navigation menu, the main content and contents list in the center, and a right-hand sidebar with section details." />
</Frame>

***

## 8. Create a Domain (shopping-app) and assign systems

Domains are a higher-level grouping for systems. Example `Domain` descriptor:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Domain
metadata:
  name: shopping-app
  description: Handles everything in the ecommerce portion of the business
spec:
  owner: ecommerce
```

If `Domain` is blocked by import rules, add it to `app-config.yaml` (see earlier example), restart Backstage, and import. After importing, the `shopping-app` domain will list its systems (for example `purchasing`).

<Frame>
  <img alt="A Backstage web UI showing an &#x22;About&#x22; overview for an ecommerce domain/shopping-app, with a description that it handles the ecommerce portion of the business and a relations graph linking &#x22;ecommerce&#x22; to &#x22;shopping-app.&#x22; The left sidebar shows navigation items like Home, APIs, and Docs." />
</Frame>

To assign a system to a domain, set `spec.domain` on the system to the domain name (for example `spec.domain: shopping-app`). You can also use `spec.subdomainOf` in domains for hierarchical structuring.

***

## 9. Create a Resource (inventory-db) and connect it

A `Resource` models infrastructure or external services such as databases. Example `Resource` descriptor for an inventory database:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: inventory-db
  description: Stores inventory details
spec:
  type: database
  owner: ecommerce
  system: purchasing
```

Make the `inventory` component depend on the resource by referencing it in `spec.dependsOn`:

```yaml theme={null}
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: inventory
spec:
  dependsOn:
    - resource: inventory-db
  type: service
  lifecycle: production
  owner: ecommerce
  system: purchasing
```

Ensure `Resource` is permitted by your catalog rules. After importing, the `inventory` component will show a relation to `inventory-db`, and clicking it will open the resource overview.

<Frame>
  <img alt="A screenshot of the Backstage service catalog showing the &#x22;inventory-db&#x22; resource overview, with an About panel listing description, owner (ecommerce) and system, and a Relations graph on the right. The left sidebar shows navigation (Home, APIs, Docs, Create) and the top header displays the inventory-db title." />
</Frame>

***

## Reference: Common Backstage Entity Kinds

| Entity Kind | Typical Use                                       | Example field                 |
| ----------- | ------------------------------------------------- | ----------------------------- |
| Component   | Deployable software (service, website)            | `spec.type: website`          |
| Group       | Teams or organizational groups                    | `metadata.name: ecommerce`    |
| User        | Individual identity                               | `metadata.name: john`         |
| System      | Logical grouping of components                    | `metadata.name: purchasing`   |
| Domain      | High-level business area grouping systems         | `metadata.name: shopping-app` |
| Resource    | Infrastructure or external systems (DBs, buckets) | `spec.type: database`         |

***

## Summary & Best Practices

* Backstage catalog supports first-class entity kinds: Components, Groups, Users, Systems, Domains, and Resources.
* Use `owner` to indicate ownership; prefix with `user:` for individual owners (for example `owner: user:john`). Groups can be referenced by plain names (for example `owner: ecommerce`).
* Use `spec.system` to associate a component with a system.
* Use `spec.dependsOn` to model dependencies between components and resources (for example `- component: inventory` or `- resource: inventory-db`).
* If you encounter NotAllowed errors when importing entities, review the `catalog.import.rules` in `app-config.yaml`, add the missing kinds, and restart Backstage.
* For details and more descriptor examples, consult the Backstage documentation:
  * Descriptor format: [https://backstage.io/docs/features/software-catalog/descriptor-format](https://backstage.io/docs/features/software-catalog/descriptor-format)
  * Software catalog overview: [https://backstage.io/docs/features/software-catalog/what-is-the-software-catalog](https://backstage.io/docs/features/software-catalog/what-is-the-software-catalog)

API entities and more advanced relationship modeling (custom relations, annotations, and entity refs across namespaces) are useful next topics to explore as you expand your catalog.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/f9244f9d-083a-4acd-a518-549f54b644b5/lesson/9d4c3f12-387c-4851-b681-c49ad9bc636e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/f9244f9d-083a-4acd-a518-549f54b644b5/lesson/1dbf42bd-8fab-446b-91f1-dcea0ff429f7" />
</CardGroup>
