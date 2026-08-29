# Draft Pull Requests

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Pull-Requests/Draft-Pull-Requests/page

Explains draft pull requests, their non-mergeable state, suppressed reviewer notifications, visual indicators, benefits for early feedback and CI validation, conversion steps and best practices.

A draft pull request (Draft PR) is a special pull request state used to indicate that a contribution is still a work in progress. It gives teams early visibility into ongoing changes while preventing the contribution from entering the full review-and-merge workflow prematurely. Draft PRs are especially useful for collaborative development, exploratory work, or when you want CI feedback before inviting formal reviews.

## Key characteristics of a draft pull request

* Non-mergeable state: Draft PRs are initially locked and cannot be merged until the author explicitly converts them to a ready-for-review status.
* Suppressed reviewer notifications: Creating a draft does not automatically request reviewers, reducing unnecessary notifications while the work is incomplete.
* Visual indicators: Draft PRs are clearly labeled with a draft badge and a distinctive gray icon in the pull request list so collaborators can quickly identify WIP contributions.

<Frame>
  <img alt="The image shows an infographic about the key characteristics of a draft pull request, highlighting that it is in a non-mergeable state, has suppressed notifications, and includes visual indicators." />
</Frame>

Summary table

| Characteristic               |                             What it does | Why it matters                                  |
| ---------------------------- | ---------------------------------------: | ----------------------------------------------- |
| Non-mergeable                |         Prevents merging until converted | Avoids prematurely merging incomplete work      |
| Suppressed reviewer requests | Does not automatically request reviewers | Reduces review fatigue during early stages      |
| Visual indicators            |     Displays a draft badge and gray icon | Makes WIP PRs easy to spot in lists and filters |

## Why create a draft pull request?

* Early feedback loops: Share the design, architecture, or high-level approach to get input before finalizing implementation details.
* CI/CD validation: Many continuous integration pipelines and automated checks still run for draft PRs (depending on your CI config), allowing you to validate builds and tests earlier in the process.
* Incremental visibility: Team members can see progress and leave comments or suggestions that shape the final implementation.

<Frame>
  <img alt="The image contains a presentation slide discussing the benefits of using draft pull requests, highlighting &#x22;Early feedback loops&#x22; and &#x22;CI/CD validation.&#x22;" />
</Frame>

This approach lets developers confirm that code compiles and tests pass before converting the draft into a ready-for-review pull request.

## Converting a draft to ready-for-review

When the work is complete and you're ready for formal review, follow these steps:

1. Open the draft pull request in GitHub.
2. Click the **Ready for review** button at the top of the PR page to convert it to a standard PR.
3. After conversion, the PR becomes mergeable subject to branch protection rules and required status checks.
4. The repository workflow will then typically request reviewers and begin any configured review processes.

Checklist before conversion

* Ensure automated tests and CI checks pass.
* Confirm code style and linting issues are resolved.
* Add a clear description, task list, and any necessary context for reviewers.
* Tag or request appropriate reviewers if your repo requires manual selection.

<Callout icon="lightbulb">
  Draft pull requests are ideal for incremental collaboration: they combine early CI feedback and team visibility while avoiding premature review requests and merges.
</Callout>

## Best practices

* Use draft PRs for exploratory work, rough implementations, or when you want CI validation before soliciting reviews.
* Add a short summary of what remains to be done in the PR description so collaborators understand the status.
* Keep draft PRs focused and update them regularly to reflect progress.

## Links and references

* [GitHub Docs: Creating a draft pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/creating-and-managing-pull-requests/about-pull-requests)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/d1fa4e43-2a65-4de9-8da8-dc9ea7cede8e/lesson/b4050770-196c-47d3-936c-8692774f8216" />
</CardGroup>
