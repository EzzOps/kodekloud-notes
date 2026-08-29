# Recognizing Repository Visibility Levels

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Administration/Recognizing-Repository-Visibility-Levels/page

Explains GitHub repository visibility levels and guidance for choosing public private or internal settings to balance collaboration security and discoverability

In this lesson we review GitHub repository visibility levels and how to choose the right one for collaboration, security, and discoverability. Setting repository visibility appropriately is a key early step in repository design: it determines who can find your code, who can fork or contribute, and how easily teams can share work internally.

When creating a repository within an organization, repository owners and maintainers should decide how broadly the repository should be accessible. Correct visibility settings reduce risk (by limiting accidental exposure) and enable the right level of collaboration across teams.

GitHub provides three repository visibility levels:

* Public
  * Accessible to anyone on the internet.
  * Ideal for open-source projects, public documentation, or developer portfolios where discoverability and broad collaboration are desired.

* Private
  * Access is restricted to repository owners and explicitly invited collaborators or teams.
  * Appropriate for sensitive or proprietary code, pre-release work, or private experiments.

* Internal
  * Visible to members of the same organization or enterprise (but not to the general public).
  * Useful for InnerSource practices: sharing code, tools, and knowledge across teams inside a company to reduce duplication and encourage reuse.

<Frame>
  <img alt="The image shows a table outlining different types of repository visibility (Public, Private, Internal) along with their technical access and primary use cases." />
</Frame>

Practical guidance and comparison

* Public repositories encourage contributions and external adoption, but should never contain secrets, credentials, or proprietary IP.
* Private repositories are the default choice for sensitive code or early-stage projects; use protected branches and required reviews for extra control.
* Internal repositories are effective when an enterprise wants to allow discoverability and reuse inside an organization without exposing assets to the public internet.

| Visibility | Who can see it                                  | Best use cases                                                       | Example considerations                                                                            |
| ---------: | ----------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
|     Public | Anyone on the internet                          | Open-source projects, public docs, demos, community-driven libraries | Use for projects intended for wide adoption; always remove secrets and rotate exposed credentials |
|    Private | Repository owners & invited collaborators/teams | Proprietary code, early development, closed beta work                | Manage access via teams, invite-only collaborators, and use branch protections                    |
|   Internal | Members of the same organization or enterprise  | InnerSource practices, shared tooling, cross-team libraries          | Requires an enterprise or organization plan; enables internal discovery without public exposure   |

<Callout icon="lightbulb">
  Internal visibility is available to organizations that are part of an enterprise account (for example, on [GitHub Enterprise](https://github.com/enterprise)). It makes repositories visible to organization/enterprise members but keeps them hidden from the public internet.
</Callout>

<Callout icon="warning">
  Never commit secrets, API keys, or credentials to any repository. If secrets are accidentally committed, rotate them immediately and remove them from history using tools like `git filter-repo` or GitHub’s secret scanning/remediation features.
</Callout>

Quick checklist for choosing visibility

* Is the code intended to be discovered or reused externally? → Public
* Does the repository contain sensitive IP, customer data, or pre-release work? → Private
* Should the repo be discoverable across teams but not public? → Internal (requires enterprise/organization support)

Further resources and references

* [GitHub Docs — About repository visibility](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/about-repository-visibility)
* [GitHub Enterprise](https://github.com/enterprise) — Enterprise features including internal repositories
* [Best practices for secret management](https://docs.github.com/en/code-security/secret-security)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e1fb240f-a163-45b7-ae70-61c1e162023f/lesson/1e7ece65-294b-4c70-a904-62bd7dd89363" />
</CardGroup>
