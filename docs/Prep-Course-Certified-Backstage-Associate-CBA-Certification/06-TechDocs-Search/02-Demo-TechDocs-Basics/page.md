# Demo TechDocs Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/TechDocs-Search/Demo-TechDocs-Basics/page

Guide to Backstage TechDocs setup, MkDocs integration, repository layout, configuration, and production recommendations for building, publishing, and serving component documentation inside Backstage.

In this lesson we'll walk through Backstage TechDocs — the built-in documentation system that lets each catalog component expose and render documentation directly inside Backstage. You'll learn the minimal configuration and repository layout required to enable TechDocs for a component, how Backstage builds and serves the docs, and recommendations for production deployments.

<Frame>
  <img alt="A screenshot of the Backstage catalog showing the &#x22;shopping-cart&#x22; service page with an About panel, tabs (Overview, CI/CD, API, Dependencies, Docs), and a warning about missing related entities. On the right is a relations graph linking the shopping-cart to auth-api and auth-service." />
</Frame>

What is TechDocs?

* TechDocs is a Backstage plugin (backend + frontend) that generates and displays static documentation for catalog entities.
* It typically uses MkDocs (often with the mkdocs-material theme) to render Markdown into a static site that Backstage can serve or publish to object storage.

Overview — high-level steps

| Step | Goal                                                        | Where to configure               |
| ---- | ----------------------------------------------------------- | -------------------------------- |
| 1    | Ensure TechDocs backend plugin is enabled                   | Backstage backend bootstrap file |
| 2    | Configure builder/generator/publisher behavior              | `app-config.yaml`                |
| 3    | Add MkDocs config and documentation files to the repository | `mkdocs.yml` and `docs/`         |
| 4    | Annotate the catalog entity with TechDocs location          | `catalog-info.yaml`              |
| 5    | Import the component into Backstage and view TechDocs       | Backstage catalog UI             |

Backstage backend: enable the TechDocs backend plugin
Open your backend bootstrap (where backend plugins are wired) and confirm TechDocs backend is added. Example:

```javascript theme={null}
// backend/index.js
import { createBackend } from '@backstage/backend-defaults';

const backend = createBackend();

backend.add(import('@backstage/plugin-app-backend'));
backend.add(import('@backstage/plugin-proxy-backend'));
backend.add(import('@backstage/plugin-scaffolder-backend'));
backend.add(import('@backstage/plugin-scaffolder-backend-module-github'));
backend.add(import('@backstage/plugin-techdocs-backend'));

// auth plugin
backend.add(import('@backstage/plugin-auth-backend'));
backend.add(import('@backstage/plugin-auth-backend-module-guest-provider'));

// catalog plugin
backend.add(import('@backstage/plugin-catalog-backend'));
```

Repository integrations (example)
Backstage typically stores Git host integrations in `app-config.yaml`. Use environment variables for secrets — never hardcode tokens.

```yaml theme={null}
integrations:
  github:
    - host: github.com
      # Use an environment variable for the token, do not hardcode secrets.
      token: ${GITHUB_TOKEN}
```

TechDocs configuration in app-config.yaml
Configure the TechDocs builder, generator, and publisher. For experimentation you can use local options; for production prefer CI-built artifacts and cloud storage.

```yaml theme={null}
