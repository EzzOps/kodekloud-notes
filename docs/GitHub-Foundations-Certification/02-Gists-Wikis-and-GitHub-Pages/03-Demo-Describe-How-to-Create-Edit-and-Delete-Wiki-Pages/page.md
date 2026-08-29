# Demo Describe How to Create Edit and Delete Wiki Pages

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Gists-Wikis-and-GitHub-Pages/Demo-Describe-How-to-Create-Edit-and-Delete-Wiki-Pages/page

Explains GitHub draft pull requests, their non mergeable state, suppressed notifications, visual indicators, benefits like early feedback and CI checks, and recommended best practices.

What is a draft pull request?

A draft pull request (draft PR) is a GitHub pull request state indicating the contribution is a work in progress. It gives teams early visibility into proposed changes—allowing design and integration feedback—while preventing the PR from being treated as ready to merge.

Key characteristics of a draft pull request

* Non-mergeable state\
  Draft PRs are locked and cannot be merged until the author converts them to a ready-for-review state. This prevents accidental merges into the base branch.

* Suppressed notifications\
  Creating a draft PR does not automatically notify repository owners or designated reviewers. This reduces unnecessary review pings and prevents review fatigue.

* Visual indicators\
  Draft PRs are visibly labeled with a draft badge and use a distinct gray icon in lists so reviewers can quickly distinguish them from active PRs.

Summary table

| Characteristic           |                       What it means | Why it matters                                   |
| ------------------------ | ----------------------------------: | ------------------------------------------------ |
| Non-mergeable state      | PR cannot be merged until converted | Protects the base branch from incomplete changes |
| Suppressed notifications |      Reviewers aren’t auto-notified | Reduces noise and prevents premature reviews     |
| Visual indicators        |           Draft badge and gray icon | Makes WIP contributions easy to spot             |

<Frame>
  <img alt="The image is an infographic titled &#x22;Draft Pull Request,&#x22; highlighting three key characteristics: non-mergeable state, suppressed notifications, and visual indicators, each represented by arrows with icons." />
</Frame>

<Callout icon="lightbulb">
  Converting a draft pull request to "Ready for review" is a deliberate, manual step. Only after that conversion will the PR become mergeable and trigger reviewer notifications.
</Callout>

Why use a draft pull request?

* Early feedback\
  Draft PRs let you share high-level direction, architecture, or approach so teammates can give early feedback before you finalize the implementation. This early collaboration helps catch design issues and reduces rework.

* CI/CD validation\
  Most repositories run continuous integration checks (builds, tests, linters) on draft PRs. That lets authors verify the code compiles and tests pass as they iterate, reducing trivial failures when the PR is later marked ready for review.

<Frame>
  <img alt="The image explains the benefits of using draft pull requests, highlighting early feedback loops and CI/CD validation." />
</Frame>

Best practices

* Use draft PRs for early design reviews and integration checks, not for finalized changes.
* Update the PR description as work progresses so reviewers understand the current scope.
* Convert to "Ready for review" only when the implementation and CI results are stable.

Links and references

* [GitHub: About pull requests](https://docs.github.com/en/pull-requests)
* [GitHub: Draft pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-draft-pull-requests)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/276e82b4-df95-4d98-ace5-3bf4e5889b26/lesson/506cbe4e-0de6-4b12-bf22-d9a93dd2095f" />
</CardGroup>
