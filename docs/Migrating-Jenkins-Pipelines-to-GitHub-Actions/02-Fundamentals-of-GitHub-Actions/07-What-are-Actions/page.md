# What are Actions

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Fundamentals-of-GitHub-Actions/What-are-Actions/page

Explains GitHub Actions as reusable workflow automation, how to reference and pin actions, types, security considerations, and best practices for safe, reproducible CI usage.

Actions are the reusable automation building blocks used inside GitHub Workflows. They encapsulate a single task—such as checking out source code, setting up a runtime, or publishing artifacts—and can be authored by you, by your organization, or by the broader community. Sharing actions enables consistent, composable automation across repositories and teams.

You can discover and evaluate actions on the GitHub Marketplace:

<Frame>
  <img alt="A screenshot of an &#x22;Actions&#x22; page divided into &#x22;GitHub-Verified Actions&#x22; and &#x22;Third-Party/Community Actions&#x22; sections. Each section shows example action cards like &#x22;Setup Java JDK,&#x22; &#x22;Authenticate to Google Cloud,&#x22; and &#x22;Deploy to GitHub Pages.&#x22;" />
</Frame>

Actions in the Marketplace fall into two broad categories:

* GitHub-verified actions: maintained or verified by GitHub; carry a verified badge.
* Community (third-party) actions: created and maintained by individuals or organizations.

Always review an action’s source repository and the permissions it requests before adding it to production workflows—particularly any actions that will run against private repositories or that may receive secrets. Inspecting the action’s code helps prevent accidental leakage of secrets or sensitive data.

> **lightbulb** Before adding an action, verify its source and the permissions it requires. This minimizes risk of secret exposure and unexpected side effects in your workflows.

## How to reference an action in your workflow

Every action published in the Marketplace exposes a `uses` reference that you include in a job step. You can pin an action to a specific:

* Tag (recommended for controlled versioning)
* Branch (tracks latest on that branch)
* Commit SHA (immutable and most reproducible)

The differences are summarized below.

| Pinning method |                   What it points to | Typical example                   | Pros                                              | Cons                                                            |
| -------------- | ----------------------------------: | --------------------------------- | ------------------------------------------------- | --------------------------------------------------------------- |
| Tag            | A release tag (semantic versioning) | `actions/checkout@v3.6.0`         | Easy to update, can follow major versions (`@v3`) | Tag updates can still introduce changes if not strictly managed |
| Branch         |        A branch name (e.g., `main`) | `actions/checkout@main`           | Always gets latest changes on branch              | Can introduce breaking changes unexpectedly                     |
| Commit SHA     |               A specific commit SHA | `actions/checkout@a8240080857...` | Immutable and reproducible                        | Harder to track when to update                                  |

> **warning** Referencing a branch (for example, `@main`) means the action may change without any changes to your workflow. This can introduce breaking behavior if the upstream branch receives incompatible updates.

Examples of referencing an action in a workflow:

```yaml theme={null}
