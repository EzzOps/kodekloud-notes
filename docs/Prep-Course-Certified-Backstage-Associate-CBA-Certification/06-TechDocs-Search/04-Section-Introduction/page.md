# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/TechDocs-Search/Section-Introduction/page

Explains Backstage TechDocs and Search integration with the Software Catalog, showing authoring, configuration, building, and indexing to make documentation discoverable across a developer portal

In this lesson/article, we'll explore two core Backstage capabilities that help teams build, document, and discover software: TechDocs (the built-in documentation system) and Backstage Search (the unified discovery experience). You'll learn how each feature works, how they connect to the Backstage software catalog, and the basic authoring and indexing steps to make documentation discoverable across your developer portal.

<Frame>
  <img alt="A presentation slide titled &#x22;Docs and Search&#x22; with the subtitle &#x22;Section Introduction&#x22; on a blue-to-teal gradient background. A small &#x22;© Copyright KodeKloud&#x22; is visible in the bottom-left." />
</Frame>

This section covers:

* An overview of TechDocs: how Backstage renders and hosts documentation alongside software components.
* An overview of Search: how Backstage indexes catalog entities and TechDocs content to deliver unified discovery.
* A high-level workflow: authoring docs, connecting them to catalog entities, and ensuring they are indexed by Search.

> **lightbulb** Tip: Treat TechDocs and the Software Catalog as a combined workflow—author documentation in your repo, point a catalog entity to that repo, and Backstage will render and index the docs so your team can discover them via Search.

Why this matters

* Faster onboarding: Centralized docs and search reduce time-to-context for new contributors.
* Single source of truth: Docs stored with code and surfaced in Backstage stay up-to-date.
* Discoverability: Indexing both entities and TechDocs content makes it easy to find components, APIs, and guides in one place.

Key features at a glance:

| Feature          | What it provides                                                                            | Integration point                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| TechDocs         | Renders Markdown/MDX documentation into a static documentation site served within Backstage | `catalog-info.yaml` links an entity to its docs repo and `techdocs` plugin builds/hosts content |
| Backstage Search | Indexes catalog entities and TechDocs pages to provide full-text, cross-entity search       | Search plugin integrates with the catalog and TechDocs indexing pipeline                        |
| Software Catalog | A registry of components, services, APIs, and more with metadata and links                  | Catalog entities connect docs and runtime metadata for discoverability                          |

What you'll see in this section

1. Setup and configuration steps to enable TechDocs and Search in a Backstage instance.
2. Examples showing how to author documentation (Markdown), link it from a `catalog-info.yaml`, and trigger TechDocs builds.
3. How Backstage Search indexes the rendered documentation and catalog entities so content is returned in search results.

Links and references

* Backstage TechDocs plugin: [https://backstage.io/docs/features/techdocs/intro](https://backstage.io/docs/features/techdocs/intro)
* Backstage Search: [https://backstage.io/docs/features/search/overview](https://backstage.io/docs/features/search/overview)
* Backstage Software Catalog: [https://backstage.io/docs/features/software-catalog/what-is-catalog](https://backstage.io/docs/features/software-catalog/what-is-catalog)

This article will include setup instructions, configuration examples, and practical guidance to help you author TechDocs content so it becomes discoverable through Backstage Search.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-backstage-associate-cba/module/ea371bfc-3770-4d25-80ef-e464e4b24fda/lesson/7729e54c-1815-464d-9556-ce07f7afb7cb)
