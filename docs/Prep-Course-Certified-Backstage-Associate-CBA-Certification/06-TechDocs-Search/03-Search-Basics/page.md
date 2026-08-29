# Reference: https://backstage.io/docs/features/techdocs/
techdocs:
  builder: 'local'         # Alternatives: 'external'
  generator:
    runIn: 'docker'       # Alternatives: 'local'
  publisher:
    type: 'local'         # Alternatives: 'googleGcs' or 'awsS3'
```

TechDocs options at a glance

| Option            | Typical values                | Notes                                                                                                                  |
| ----------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `builder`         | `local`, `external`           | `local` runs the build inside the backend; `external` delegates to an external builder (recommended for CI workflows). |
| `generator.runIn` | `docker`, `local`             | `docker` uses the TechDocs Docker image; `local` requires installing the TechDocs binary on the host.                  |
| `publisher.type`  | `local`, `googleGcs`, `awsS3` | Use `googleGcs` or `awsS3` for production (object storage) to serve static builds at scale.                            |

Project repository layout
Place MkDocs config and Markdown documentation alongside your code so documentation is versioned with the project.

| File / Folder       | Purpose                                                    |
| ------------------- | ---------------------------------------------------------- |
| `package.json`      | Project dependencies / build scripts (if applicable)       |
| `catalog-info.yaml` | Backstage entity definition and annotations                |
| `mkdocs.yml`        | MkDocs site configuration (nav, theme, plugins)            |
| `docs/`             | Markdown files to be rendered by MkDocs (e.g., `index.md`) |

Example `package.json` (trimmed):

```json theme={null}
{
  "name": "recommendation-service",
  "version": "1.0.0",
  "main": "index.js",
  "type": "module",
  "dependencies": {
    "express": "^4.21.2"
  }
}
```

`.gitignore` (example):

```text theme={null}
node_modules/
```

MkDocs configuration
Place `mkdocs.yml` (or `mkdocs.yaml`) at repo root. TechDocs commonly uses mkdocs-material.

```yaml theme={null}
site_name: 'example-docs'

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - API Reference: api.md

theme:
  name: material

plugins:
  - techdocs-core
```

If you store your docs in a non-default directory, set `docs_dir`:

```yaml theme={null}
# Example to use a directory named "documentation" instead of "docs"
# docs_dir: documentation
```

Documentation content example
Create Markdown under `docs/`. Example `docs/index.md`:

```markdown theme={null}
## Getting Started

Welcome to the docs for the recommendation service.

### Examples

- Step 1
- Step 2
```

Catalog entity annotation
Point Backstage to the repository location containing `mkdocs.yml` and the `docs/` folder by adding the TechDocs annotation to `catalog-info.yaml`. Quote the annotation value to avoid YAML parsing issues.

```yaml theme={null}
apiVersion: backstage.io/v1beta1
kind: Component
metadata:
  name: recommendation-service
  description: Recommendation service api
  annotations:
    'backstage.io/techdocs-ref': 'dir:.'
  tags:
    - javascript
  links:
    - url: https://google.com
      title: Admin Dashboard
      icon: dashboard
      type: admin-dashboard
spec:
  type: service
```

* `'backstage.io/techdocs-ref': 'dir:.'` tells Backstage to read `mkdocs.yml` from the repository root and use the default `docs/` folder.
* To point to a subfolder, update the `dir:` path (for example `'dir:docs/subfolder'`) or set `docs_dir` in `mkdocs.yml`.

Build and publish behavior
How the docs get built and served depends on your `techdocs` config:

1. Backstage fetches the repository referenced by the catalog entity.
2. The generator runs MkDocs (inside Docker or locally) to produce a static site.
3. The publisher stores the generated site (local storage or cloud object storage) and the frontend serves it when you click "View TechDocs".

Example developer workflow:

1. Push repository changes (include `catalog-info.yaml`, `mkdocs.yml`, and `docs/`) to your Git host.
2. Import or refresh the component in the Backstage catalog.
3. Open the component page and click "View TechDocs" (or the Docs tab). Backstage will generate and display the documentation according to your configured builder/generator/publisher.

<Frame>
  <img alt="A screenshot of a Backstage documentation page titled &#x22;example-docs&#x22; showing a large heading &#x22;This is the documentation for my app!&#x22; with example h1–h6 headings. A dark left sidebar displays navigation items like Home, APIs, Docs, and Create." />
</Frame>

Production considerations

<Callout icon="lightbulb">
  For production, Backstage recommends generating TechDocs artifacts in CI and publishing the generated static site to cloud storage ([Google Cloud Storage](https://cloud.google.com/storage) or [AWS S3](https://aws.amazon.com/s3)) instead of using the local publisher. This improves scalability, reduces on-demand build latency, and allows serving docs from highly-available object storage.
</Callout>

Best practices and tips

* Never commit secrets or tokens to `app-config.yaml`. Use environment variables or secret management.
* Prefer CI-based builds and cloud publishers (`googleGcs` or `awsS3`) for production workloads.
* Use `mkdocs-material` for a polished default theme that integrates well with TechDocs.
* If using generator `runIn: docker`, ensure your backend host can run Docker, or switch to CI-based generation for environments where Docker isn’t available.

Summary

* TechDocs integrates MkDocs with Backstage to render component docs inside the catalog.
* Enable the TechDocs backend plugin and configure builder/generator/publisher in `app-config.yaml`.
* Add `mkdocs.yml` and a `docs/` folder to your repository and annotate the entity with `'backstage.io/techdocs-ref'`.
* For production, build docs in CI and publish to cloud storage for scalability and faster page loads.

Links and references

* Backstage TechDocs docs: [https://backstage.io/docs/features/techdocs/](https://backstage.io/docs/features/techdocs/)
* MkDocs: [https://www.mkdocs.org/](https://www.mkdocs.org/)
* mkdocs-material theme: [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
* Google Cloud Storage: [https://cloud.google.com/storage](https://cloud.google.com/storage)
* AWS S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/ea371bfc-3770-4d25-80ef-e464e4b24fda/lesson/44ce2ea1-2bd5-4c6d-99ee-6159d2786336" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/ea371bfc-3770-4d25-80ef-e464e4b24fda/lesson/3c1a8d11-3762-4160-805d-6294b7c934ee" />
</CardGroup>


# Search Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/TechDocs-Search/Search-Basics/page

Overview of Backstage search features, covering indexing, collators, backend choices (Lunr, Postgres, Elasticsearch/OpenSearch), scheduling, external source integration and deployment best practices.

In this lesson we explore Backstage's search capabilities: how it indexes content, the components that power search, and how to extend it to include external sources like Confluence or Stack Exchange.

Backstage centralizes developer tools and documentation, and its search is designed to surface everything relevant — from catalog entities to TechDocs and external knowledge bases. Out of the box, Backstage lets you query your software catalog and the documentation linked to those entries, helping you find features or identify responsible services even when you don't know exact names.

Backstage search is also extensible: you can add collators to index external resources such as Confluence, Stack Exchange, or any other data source with an available collator.

<Frame>
  <img alt="A slide titled &#x22;Search&#x22; featuring a teal stacked-logo graphic and a highlighted &#x22;Plugin&#x22; label. To the right are icons and labels for Confluence and Stack Exchange, with &#x22;© Copyright KodeKloud&#x22; in the corner." />
</Frame>

Backstage gives you control over what gets indexed and how results are presented. You can aggregate content from multiple sources and present unified search results to users, improving discoverability across your organization.

Search engine backends

Backstage supports multiple search engine backends. The default is Lunr (an in-memory index suitable for small to medium installations), but for larger or persistent indexes you can use Postgres or Elasticsearch/OpenSearch.

<Frame>
  <img alt="A &#x22;Search Engine&#x22; diagram showing three backend options: Lunr Search (Default), Postgres, and Elastic Search. Each option is displayed with its icon (magnifier, PostgreSQL elephant, Elasticsearch logo) beneath a central stacked &#x22;B&#x22; logo." />
</Frame>

Use the table below to quickly compare common backend choices and when to pick each:

| Backend                    | Best for                                                 | Notes                                                                                                                                  |
| -------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Lunr                       | Small deployments, low operational overhead              | In-memory index; simple to run with Backstage defaults.                                                                                |
| Postgres                   | Moderate scale, use existing DB infrastructure           | Persists index in your Postgres database.                                                                                              |
| Elasticsearch / OpenSearch | Large scale, advanced search features, distributed index | Use when you need scalability, analytics, or cross-cluster setups. Configure provider as `elasticsearch` or `opensearch` in Backstage. |

Collators — what they do

Collators determine which data is discovered and indexed. A collator:

* Discovers content in a specified location (catalog entities, TechDocs, Confluence spaces, Stack Exchange data, etc.).
* Converts that content into canonical "documents" for the search indexer to consume.

Backstage ships with collators for catalog entities and built-in TechDocs. To index additional sources (for example Confluence or Stack Exchange), add and configure a collator for each source.

Index scheduling

Backstage maintains an index for all configured sources and lets you control how frequently each collator runs. Scheduling collators independently helps balance freshness and system load: frequently changing content can be indexed more often than stable sources.

<Frame>
  <img alt="A schematic titled &#x22;Scheduler&#x22; showing a &#x22;Collators&#x22; search function feeding a &#x22;Collecting index&#x22; that polls multiple sources. It lists targets like Catalog, Docs, Confluence and Stack Exchange with polling intervals (30 mins, 1 hr, 6 hrs, 2 days)." />
</Frame>

Example scheduling strategy:

| Source                                                 | Example poll interval |
| ------------------------------------------------------ | --------------------- |
| Catalog (service listing)                              | 30 minutes            |
| Internal TechDocs                                      | 1 hour                |
| Confluence spaces                                      | 6 hours               |
| External knowledge base (e.g., Stack Exchange dataset) | 2 days                |

Adjust polling intervals to match the change frequency and operational cost for each source in your environment.

Switching to Elasticsearch / OpenSearch

If your installation needs a persistent, scalable index, switch from the default Lunr to Elasticsearch or OpenSearch. Steps:

1. Add the Elasticsearch/OpenSearch backend collator module to your backend packages.
2. Register the module with your backend at startup.
3. Configure the connection details in `app-config.yaml`.

Install the backend module (run from your repository root or the workspace that contains `packages/backend`):

```bash theme={null}
yarn --cwd packages/backend add @backstage/plugin-search-backend-module-elasticsearch
```

Register the search backend and Elasticsearch/OpenSearch module with your backend. Many Backstage backends perform dynamic imports, so you may need to `await` these imports. A typical pattern:

```javascript theme={null}
// backend/start.js (or index.ts)
const backend = createBackend();

await backend.add(await import('@backstage/plugin-search-backend'));
await backend.add(await import('@backstage/plugin-search-backend-module-elasticsearch'));

await backend.start();
```

<Callout icon="lightbulb">
  When using dynamic imports, ensure the surrounding context supports `await` (for example, by using top-level await in an ES module) or wrap this logic inside an async function. Restart the backend after adding new modules.
</Callout>

Configure the Elasticsearch/OpenSearch connection in `app-config.yaml`. Example:

```yaml theme={null}
search:
  elasticsearch:
    provider: opensearch
    node: http://0.0.0.0:9200
    auth:
      username: opensearch
      password: changeme
```

Set `provider` to `elasticsearch` or `opensearch` depending on your server, and update `node` and credentials to match your deployment.

Best practices

* Start with Lunr for small teams or evaluations; move to Postgres or Elasticsearch/OpenSearch as scale demands.
* Use per-source scheduling to reduce unnecessary indexing load.
* Add collators only for data sources you need in search to keep the index relevant and performant.
* Secure your Elasticsearch/OpenSearch endpoints and credentials (use secrets management where possible).

Summary

* Backstage search indexes catalog entities, TechDocs, and any additional sources you enable via collators.
* Choose Lunr for simplicity, Postgres for DB-backed indices, or Elasticsearch/OpenSearch for large-scale, feature-rich search.
* Collators define what gets indexed and can be scheduled independently to balance freshness and cost.
* To add Elasticsearch/OpenSearch: install the backend module, register it during backend startup, and configure connection settings in `app-config.yaml`.

Links and References

* Backstage Search docs: [https://backstage.io/docs/search/](https://backstage.io/docs/search/)
* Lunr: [https://lunrjs.com](https://lunrjs.com)
* PostgreSQL: [https://www.postgresql.org](https://www.postgresql.org)
* Elasticsearch: [https://www.elastic.co](https://www.elastic.co)
* OpenSearch: [https://opensearch.org](https://opensearch.org)
* Confluence: [https://www.atlassian.com/software/confluence](https://www.atlassian.com/software/confluence)
* Stack Exchange: [https://stackexchange.com](https://stackexchange.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/ea371bfc-3770-4d25-80ef-e464e4b24fda/lesson/53322bb2-0984-402b-80c8-c88c4e98e72e" />
</CardGroup>
