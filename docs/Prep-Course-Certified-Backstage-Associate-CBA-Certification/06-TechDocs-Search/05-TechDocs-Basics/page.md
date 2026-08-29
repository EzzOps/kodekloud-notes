# TechDocs Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/TechDocs-Search/TechDocs-Basics/page

Overview of Backstage TechDocs workflow for authoring, building, publishing, and serving component documentation using MkDocs, local or CI/CD builds, and storage backends

This lesson explains TechDocs in Backstage: how documentation is authored, built, published, and served so teams can find docs next to code.

Backstage is a developer portal that centralizes software metadata and documentation. When you import a component into Backstage, its entity page includes a Docs tab that opens the generated documentation for that component—keeping docs and code discoverable from one place.

<Frame>
  <img alt="A screenshot of a web UI for a &#x22;shopping-cart&#x22; service component showing the Docs tab and overview. The page shows an About panel with &#x22;View source&#x22; and &#x22;View techdocs&#x22; buttons, a Relations panel, and a warning about missing related entities." />
</Frame>

When a user clicks the Docs tab, Backstage serves the pre-built HTML documentation for that component. The recommended pattern is to author docs as Markdown next to your code (same repository), so code and docs changes can be reviewed together. TechDocs also supports alternative workflows where docs are built externally.

Example: small code and docs snippet

```text theme={null}
// Some comments
line 1 of code
line 2 of code
line 3 of code

Sample text here...

var foo = function (bar) {
    return bar++;
};

console.log(foo(5));
```

How Backstage builds and serves documentation

Backstage uses MkDocs (a static site generator) together with the TechDocs tooling to convert Markdown into static HTML which is then stored and served. High-level flow:

* Developers author Markdown and commit it alongside code (recommended).
* Backstage or a CI/CD job runs MkDocs / TechDocs generator to convert Markdown into HTML.
* Generated HTML is published to a storage backend (local filesystem, S3, GCS, etc.).
* When a user requests docs, Backstage reads and serves the stored HTML.

<Frame>
  <img alt="A diagram showing MkDocs (stacked green document icon and a small red book labeled &#x22;MKDOCS&#x22;) with a right-pointing arrow to a blue HTML document icon, illustrating docs being converted to HTML." />
</Frame>

TechDocs build stages

TechDocs performs three main stages to produce documentation:

1. Prepare — fetch the Markdown source from the repository (for example, GitHub).
2. Generate — convert the Markdown into HTML (using MkDocs / TechDocs generator).
3. Publish — store the generated HTML in a publisher backend.

When a user requests documentation, the publisher serves the stored HTML to Backstage, which displays it in the Docs tab.

<Frame>
  <img alt="A &#x22;Prepare Step&#x22; diagram showing a user and a pipeline of components: Preparer → Generator → Publisher. The Publisher reads HTML documentation from the local file system or an S3 bucket to deliver to the user." />
</Frame>

Local builder vs external builder

The generate step (Markdown → HTML) can run inside Backstage (local builder) or in an external CI/CD pipeline (external builder). Choose the approach that fits your team’s scale and security policies.

Table: Builder types at a glance

| Builder  | Who runs the generator                  | Typical config                                               | When to use                                                                     |
| -------- | --------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| Local    | Backstage server (in-process or Docker) | `techdocs.builder: 'local'`                                  | Small teams, simple setups, or when you want Backstage to manage builds         |
| External | CI/CD pipeline (e.g., GitHub Actions)   | `techdocs.builder: 'external'` and external publisher config | Teams that want reproducible builds, custom environments, or to offload compute |

Local builder behavior

* Backstage pulls the repository source, runs the generator (binary or Docker), generates HTML, and publishes it.
* Configure example:

```yaml theme={null}
techdocs:
  builder: 'local'
  generator:
    runIn: 'docker'         # or 'local' to run the CLI binary directly
    dockerImage: 'spotify/techdocs'
  publisher:
    type: 'local'
    local:
      publishDirectory: '/path/to/local/directory'
```

Note: setting `builder: 'local'` instructs Backstage to perform generation. If you use CI/CD to build docs, set `builder: 'external'` and ensure Backstage points to the published artifacts.

Build docs in CI/CD (external builder)

Offloading the generate step to CI/CD provides a controlled, repeatable build environment and reduces load on the Backstage instance. Typical flow:

* Developer pushes changes to `docs/` or `mkdocs.yml`.
* CI job installs TechDocs CLI and MkDocs, generates HTML, and publishes it to a storage backend (e.g., S3 or GCS).
* Backstage is configured to read the published artifacts from that storage.

High-level CI/CD flow:

<Frame>
  <img alt="A CI/CD workflow diagram for generating and publishing documentation. It shows steps (Generate Docs Workflow → Install Techdocs CLI → Generate Docs → Publish Docs) with source input from GitHub/developer and output to an S3 bucket." />
</Frame>

You can cache externally-published docs in Backstage so the storage backend is not queried on every page view—this improves performance and reduces read costs.

<Frame>
  <img alt="A CI/CD workflow diagram showing build artifacts (stacked build icon) being stored in an S3 bucket and HTML documentation cached for easy access." />
</Frame>

Example: GitHub Actions workflow

Below is a practical GitHub Actions workflow that builds TechDocs and publishes them to an S3 bucket. It triggers on pushes to `main` when `docs/**` or `mkdocs.yml` change.

```yaml theme={null}
name: Publish TechDocs Site

on:
  push:
    branches: [main]
    paths:
      - "docs/**"
      - "mkdocs.yml"

jobs:
  publish-techdocs-site:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install techdocs-cli
        run: sudo npm install -g @techdocs/cli

      - name: Install mkdocs and mkdocs plugins
        run: python -m pip install mkdocs-techdocs-core==1.*

      - name: Generate docs site
        run: techdocs-cli generate --no-docker --verbose

      - name: Publish docs site
        env:
          TECHDOCS_S3_BUCKET_NAME: ${{ secrets.TECHDOCS_S3_BUCKET_NAME }}
          ENTITY_NAMESPACE: ${{ env.ENTITY_NAMESPACE }}
          ENTITY_KIND: ${{ env.ENTITY_KIND }}
          ENTITY_NAME: ${{ env.ENTITY_NAME }}
        run: |
          techdocs-cli publish \
            --publisher-type awsS3 \
            --storage-name "$TECHDOCS_S3_BUCKET_NAME" \
            --entity "$ENTITY_NAMESPACE/$ENTITY_KIND/$ENTITY_NAME"
```

When using CI/CD, configure Backstage to use the external publisher and point it at the storage location your pipeline uses.

Repository files and Backstage configuration

To enable TechDocs for a component you usually add or verify these files in the repository:

| File                | Purpose                     | Example / Notes                                             |
| ------------------- | --------------------------- | ----------------------------------------------------------- |
| `mkdocs.yml`        | MkDocs site configuration   | Root of the repo; includes `techdocs-core` plugin           |
| `docs/`             | Markdown pages for the site | e.g., `index.md`, subpages                                  |
| `catalog-info.yaml` | Backstage entity metadata   | Add `backstage.io/techdocs-ref` annotation to point to docs |

Project example file tree:

<Frame>
  <img alt="A slide titled &#x22;Configuring Docs in Entity&#x22; showing a file tree diagram for an &#x22;app&#x22; directory. The tree lists files like .gitignore, catalog-info.yaml, mkdocs.yml, package.json (and lock), a docs folder with index.md, and a src folder." />
</Frame>

Example minimal `mkdocs.yml`

```yaml theme={null}
site_name: 'example-docs'

nav:
  - Home: index.md

plugins:
  - techdocs-core
```

Annotate your `catalog-info.yaml`

Add the `backstage.io/techdocs-ref` annotation to your entity metadata so Backstage can locate the docs. The `dir:` value should be relative to the `catalog-info.yaml` location.

Example `catalog-info.yaml` for a component:

```yaml theme={null}
apiVersion: backstage.io/v1beta1
kind: Component
metadata:
  name: shopping-cart
  description: shopping cart api
  annotations:
    backstage.io/techdocs-ref: 'dir:.'
  tags:
    - javascript
spec:
  type: service
  lifecycle: production
  owner: shopping-team
```

> **lightbulb** Store `mkdocs.yml` at the repository root and set `backstage.io/techdocs-ref` in `catalog-info.yaml` to point to your docs folder. This ensures TechDocs can find and build your documentation.

Quick recommendations and links

* Keep docs close to code (e.g., `docs/`) for easier authoring and PR reviews.
* Choose local or external builder based on scale, reproducibility, and resource constraints.
* Use S3 or GCS for scalable storage when publishing from CI/CD.
* Consider caching in Backstage for externally published docs to reduce storage reads.

References

* MkDocs: [https://www.mkdocs.org](https://www.mkdocs.org)
* Backstage TechDocs: [https://backstage.io/docs/features/techdocs](https://backstage.io/docs/features/techdocs)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* Google Cloud Storage: [https://cloud.google.com/storage](https://cloud.google.com/storage)
* TechDocs CLI: [https://github.com/spotify/techdocs-cli](https://github.com/spotify/techdocs-cli)

Summary

* TechDocs converts Markdown to HTML in three stages: prepare → generate → publish.
* Generation can run inside Backstage (local) or in CI/CD (external); configure `techdocs.builder` accordingly.
* Publish generated HTML to a storage backend (local, S3, GCS) and configure Backstage to serve it.
* Add `backstage.io/techdocs-ref` in `catalog-info.yaml` to tell TechDocs where your docs live.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/ea371bfc-3770-4d25-80ef-e464e4b24fda/lesson/1401121b-7c6d-480b-8c78-0df1a6d9e346)
