# Same-repo shorthand
#1347

# Cross-repo reference
octocat/Hello-World#1347

# Direct URL (the UI will shorten this)
https://github.com/octocat/Hello-World/issues/1347

# Legacy format
GH-1347
```

Regardless of the syntax you choose, GitHub will convert recognized references into links and maintain back-references on the referenced issue/PR timeline.

## Commit references

GitHub also auto-detects and links commit identifiers in comments, descriptions, and PR bodies. Use the format that best balances readability and precision for your workflow.

Common commit reference types:

* Commit URL — paste the full commit web address; GitHub displays a shortened seven-character SHA.
* Full SHA — include the full 40-character commit SHA when you need an exact identifier.
* Short SHA — the seven-character SHA shown in GitHub is usually sufficient for human-readable references.
* Username + SHA — `username@SHA` to indicate a specific user's commit (e.g., `octocat@7fd1a60`).
* Cross-repo commit — reference a commit in another repo with `owner/repository@SHA` (e.g., `octocat/Hello-World@7fd1a60`).

| Reference style   |                                Use case | Example                                                                                  |
| ----------------- | --------------------------------------: | ---------------------------------------------------------------------------------------- |
| Direct commit URL |       Copying directly from the browser | `https://github.com/octocat/Hello-World/commit/7fd1a604d4f2b3d2f3c9a9f1b6c2e5a6f7d8c9b0` |
| Full SHA          |            Exact, unambiguous reference | `7fd1a604d4f2b3d2f3c9a9f1b6c2e5a6f7d8c9b0`                                               |
| Short SHA         |     Readable, commonly used in comments | `7fd1a60`                                                                                |
| Username + SHA    |                Clarifies author context | `octocat@7fd1a60`                                                                        |
| Cross-repo commit | Reference commits in other repositories | `octocat/Hello-World@7fd1a60`                                                            |

<Frame>
  <img alt="The image is a table explaining GitHub autolinking for referencing specific commits, detailing different reference types, how to write them, their display format, and when to use each." />
</Frame>

Examples

```text theme={null}
# Direct commit URL (UI shortens this)
https://github.com/octocat/Hello-World/commit/7fd1a604d4f2b3d2f3c9a9f1b6c2e5a6f7d8c9b0

# Full SHA (40 chars)
7fd1a604d4f2b3d2f3c9a9f1b6c2e5a6f7d8c9b0

# Shortened (displayed by GitHub as 7 chars)
7fd1a60

# Username + SHA (contextual reference)
octocat@7fd1a60

# Cross-repo commit
octocat/Hello-World@7fd1a60
```

<Callout icon="lightbulb">
  Best practice: use `#number` for references within the same repository and `owner/repo#number` for cross-repo links. For commits, prefer the 7-character SHA shown in the UI for readability; use the full SHA when you need an exact, unambiguous identifier.
</Callout>

These autolinking conventions keep conversations tidy, make references clickable, and ensure context is preserved across issues, PRs, and commits. For more details, see GitHub's documentation on linking references and commit SHAs:

* [About referencing issues and pull requests](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)
* [Viewing commits on GitHub](https://docs.github.com/en/repositories/committing-changes-to-your-project/viewing-contributions-and-commits)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/d1fa4e43-2a65-4de9-8da8-dc9ea7cede8e/lesson/17aecaf3-3e8f-4bec-8097-d8c0eb4f9c93" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/d1fa4e43-2a65-4de9-8da8-dc9ea7cede8e/lesson/458ae912-79af-4d74-b3c3-1c303bb0de3e" />
</CardGroup>


# Options for Providing a Code Review on a Pull Request

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Pull-Requests/Options-for-Providing-a-Code-Review-on-a-Pull-Request/page

Explains when and how to use Comment, Approve, or Request changes during GitHub pull request reviews and best practices for constructive feedback

In GitHub's collaborative workflow, a code review is the formal mechanism for giving feedback on a pull request (PR). When you submit a review you must select a status that signals the next steps for the contributor and the repository: Comment, Approve, or Request changes. Choose the status that matches the severity of your feedback and the repository's branch protection rules so the team knows whether the PR can be merged.

<Callout icon="lightbulb">
  Best practices for constructive reviews:

  * Focus on scope and clarity: flag only issues that affect correctness, security, or maintainability.
  * Use `Comment` for stylistic or non-blocking suggestions to avoid unnecessary workflow friction.
  * When requesting changes, include clear reproduction steps and a prioritized list of fixes.
</Callout>

Below are the three review submission states you can use and when to use each.

* Comment — Use this to provide general feedback, ask technical questions, or note observations without changing the formal status of the pull request. This is a non-binding option intended to facilitate discussion and clarification without blocking or approving the merge.

* Approve — This is the formal sign-off. Choose Approve when the proposed changes meet project requirements and are verified for integration into the base branch. An approval is often required by branch protection rules before a pull request can be merged.

<Frame>
  <img alt="The image shows a code review interface for a pull request, with options to comment, approve, or request changes. There's also a description of what each submission state entails." />
</Frame>

* Request changes — Use this when you identify critical bugs, security vulnerabilities, or architectural issues that must be fixed before the pull request can be merged. This status formally blocks the pull request until the author addresses the requested changes and you re-review.

<Callout icon="warning">
  Requesting changes prevents the pull request from being merged until the issues are resolved and the reviewer either re-approves or the branch protection rules are satisfied.
</Callout>

Summary table — quick reference

|   Review status | Use case (when to pick)                                 | Effect on PR                                      |
| --------------: | ------------------------------------------------------- | ------------------------------------------------- |
|         Comment | Minor suggestions, questions, or discussion items       | No formal block — PR remains mergeable by policy  |
|         Approve | Changes are correct, tested, and ready for integration  | Signals readiness; may satisfy branch protections |
| Request changes | Critical bugs, security, or design issues needing fixes | Blocks merging until addressed and re-reviewed    |

Guidance for reviewers

* Match the review status to impact: non-blocking feedback = Comment, acceptance = Approve, blocking issues = Request changes.
* Be specific in comments: link to failing tests, include code snippets, or point to relevant docs.
* If a change is required but small, consider leaving a clear `Comment` and following up with a suggested patch; otherwise use `Request changes`.

Links and references

* [GitHub: Reviewing changes in pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)
* [GitHub: About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-protected-branches)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/d1fa4e43-2a65-4de9-8da8-dc9ea7cede8e/lesson/4d5bbfcd-6732-4377-8e88-5a05a7e1a52e" />
</CardGroup>
