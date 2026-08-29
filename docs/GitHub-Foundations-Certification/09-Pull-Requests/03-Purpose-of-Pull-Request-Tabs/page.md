# resolve conflicts in files, then:
git add .
git commit
git push
```

Rebase approach (keeps a cleaner linear history):

```bash theme={null}
git fetch origin
git rebase origin/main
# resolve conflicts during rebase, then:
git add .
git rebase --continue
git push --force-with-lease
```

Review workflow and automation
Typical reviewer actions:

* Leave inline comments on specific lines.
* Request changes or approve the PR.
* Verify passing CI checks and automated tests.
* Ensure code owners or maintainers sign off if required.

Automations to enforce quality:

* CI pipelines (tests, builds).
* Linters and static analysis.
* Protected branch rules (require reviews, passing checks).

> **lightbulb** Keep pull requests small and focused. Small PRs are easier to review, test, and merge. Include a clear description, testing steps, and references to related issues or tickets.

> **warning** Do not merge a pull request while checks are failing or when review comments are unresolved. Merging under these conditions can introduce regressions or unstable code into the base branch.

Best practices summary

* Use descriptive branch names and PR titles (e.g., `feature/auth-login`, `fix/typo-readme`).
* Write a clear PR description with the motivation, changes, and testing steps.
* Run and ensure CI checks pass before requesting review.
* Address requested changes and keep the PR updated with the base branch as needed.
* Prefer smaller, frequent PRs over large, monolithic ones to reduce review friction and risk.

Further reading and references

* [GitHub Pull Requests documentation](https://docs.github.com/en/pull-requests)
* [Git documentation](https://git-scm.com/doc)
* [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)

This lesson explained what a pull request is, how it fits into the branch-and-merge workflow, and the typical interactions that reviewers and contributors perform to safely integrate changes into the main codebase.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/d1fa4e43-2a65-4de9-8da8-dc9ea7cede8e/lesson/d0e16d35-7cda-4851-a60c-05a18831381f)


# Purpose of Pull Request Tabs

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Pull-Requests/Purpose-of-Pull-Request-Tabs/page

Explains GitHub pull request tabs and how to use Conversation, Commits, Checks, and Files changed to streamline code reviews and improve merge confidence.

In this lesson we’ll explain the purpose of the primary pull request (PR) tabs on GitHub and how to use them effectively during code review. GitHub organizes PRs into distinct tabs—Conversation, Commits, Checks, and Files changed—so reviewers can quickly find the right context (discussion, history, automated results, or diffs) and make high-quality decisions. Understanding each tab helps streamline reviews, reduce back-and-forth, and improve merge confidence.

The four PR tabs covered here:

* Conversation
* Commits
* Checks
* Files changed

Conversation tab

The Conversation tab is the PR’s communication center. It contains the initial PR description, threaded comments, reviewer feedback, and chronological events (branch updates, reviewer assignments, CI/bot notifications). Use this tab to align on scope, technical direction, and acceptance criteria.

When to use the Conversation tab:

* Read the PR description to understand intent and scope.
* Follow threaded discussions to track unresolved questions and decisions.
* Review timeline events to see when and why the branch changed (rebases, force-pushes, merges).
* Summarize outcomes or link to follow-up issues.

<Frame>
  <img alt="The image depicts a pull request discussion interface on GitHub, highlighting tabs for conversation, commits, and checks. It also explains that the discussion thread is a central place for PR discussions, including descriptions, comments, and feedback." />
</Frame>

Commits tab

The Commits tab shows a chronological, commit-by-commit history of changes on the branch. It helps reviewers follow the developer’s incremental thought process—useful for complex refactors or feature work split across multiple commits.

Use this tab to:

* Inspect individual commits for intent, scope, and descriptive messages.
* Detect problematic commits that should be squashed, split, or amended.
* Match a particular change to the author and timestamp for context.
* Step through commits while reading diffs to see how the code evolved.

<Frame>
  <img alt="The image explains the purpose of pull request tabs, specifically the &#x22;Commits&#x22; tab, highlighting its role in showing granular history and progressive context in code changes. It includes a screenshot of a pull request with a specific focus on commits." />
</Frame>

Checks tab

The Checks tab is your automated gatekeeper: it aggregates CI build results, test outcomes, linters, and security scans. Before investing time in a manual review, check this tab to ensure programmatic gates have passed.

Typical items shown in Checks:

* CI status (build and test pass/fail).
* Security and compliance reports (vulnerabilities, secrets scanning, static analysis).
* Linter/style violations and coverage reports.
* Links to logs and artifacts for troubleshooting.

A green checks summary usually indicates the repository’s automated requirements are satisfied and the PR is ready for focused human review.

<Frame>
  <img alt="The image explains the purpose of pull request tabs related to checks on GitHub, highlighting status reporting for tests and builds, and security & compliance for scan and linting results." />
</Frame>

Files changed tab

The Files changed tab is where the detailed technical review happens. It shows a unified diff across all modified files, lets you comment inline on specific lines, and provides suggested changes authors can apply directly.

When reviewing files:

* Verify changes are minimal and scoped to the issue or feature.
* Leave precise, line-specific comments for clarity or suggested fixes.
* Use the “suggested change” feature for small edits contributors can accept.
* Confirm documentation and tests accompany behavior changes when applicable.

This tab is also where reviewers formally approve the PR, request changes, or resolve comments. After approvals and passing checks, follow your repository’s merge policy to complete the PR.

Summary table

| Tab           | Primary purpose                                    | Reviewer actions                                                                 |
| ------------- | -------------------------------------------------- | -------------------------------------------------------------------------------- |
| Conversation  | Discussion, PR description, and timeline of events | Read description, follow threaded discussions, summarize decisions               |
| Commits       | Granular history of incremental changes            | Inspect commit intent, request squash/split, correlate changes to authors        |
| Checks        | Automated CI, tests, linters, and security scans   | Verify green status, inspect failing logs, confirm artifacts                     |
| Files changed | Unified diff and inline comments                   | Perform line-by-line review, leave suggested changes, approve or request changes |

Additional resources

* [GitHub Pull Requests documentation](https://docs.github.com/en/pull-requests)

> **lightbulb** Tip: Start reviews by checking the Checks tab to confirm automated tests and linters pass. Then use the Commits tab to understand the author's intent and the Files changed tab to leave targeted, inline feedback. Use the Conversation tab to resolve discussions and document final decisions.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/d1fa4e43-2a65-4de9-8da8-dc9ea7cede8e/lesson/b83617e1-ea46-4efc-917f-0a8a55472b18)
