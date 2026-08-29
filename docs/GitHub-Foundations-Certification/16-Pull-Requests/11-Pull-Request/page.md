# Pull Request

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Pull-Requests/Pull-Request/page

Explains pull requests within branch and merge workflows, covering branches, PR creation, reviews, merge methods, conflict resolution, CI checks, and best practices for safe collaborative development.

Let's talk about pull requests and how they fit into a branch-and-merge workflow.

What is a branch?
A branch is an isolated development environment that diverges from the main line of development. It provides a sandbox where developers can implement features, fix bugs, or experiment without impacting the main codebase or the work of others. Using independent branches enables multiple contributors to work in parallel and reduces risk to production.

<Frame>
  <img alt="The image explains the concept of a code branch as an isolated development environment. It highlights the purposes of safety in development and parallelism, allowing teams to work independently with later merges." />
</Frame>

Why branches matter
Branches let teams focus on different parts of a project simultaneously. Changes in one branch remain invisible to others until you intentionally integrate them. That integration step is where coordination and quality assurance occur.

The challenge of integration
While branches increase individual productivity, they must eventually be synchronized. Merging integrates independent work back into a shared destination (often `main`). As projects grow, unmanaged merges can cause regressions, lost work, or conflicting changes. A structured review process reduces these risks.

<Frame>
  <img alt="The image explains pull requests (PR) in the context of merging branches, highlighting the concepts of merging changes and scalability challenges as projects grow." />
</Frame>

What is a pull request?
A pull request (PR) is a formal proposal to merge changes from a compare (source) branch into a base (target) branch. You push your branch to a remote repository and open a PR so others can inspect, discuss, and approve the changes before they are merged into the stable codebase.

<Frame>
  <img alt="The image explains a pull request (PR) workflow with an interface showing a pull request in a repository and a diagram illustrating the starting point and discussion process of a pull request." />
</Frame>

Why use PRs?

* Enable code review and collaboration.
* Run automated checks (CI) before integration.
* Create an auditable history of why changes were made.
* Facilitate discussion and discovery of design or implementation issues.

Compare branch vs. base branch
Every PR is defined by two branches: the compare branch (source) with the new commits and the base branch (target) where changes will land—commonly `main`. When a PR is opened, GitHub generates a diff highlighting file and line changes so reviewers can focus on the actual modifications.

<Frame>
  <img alt="The image is a diagram explaining a pull request, showing a relationship between a &#x22;Compare Branch&#x22; which is the source branch with new changes, and a &#x22;Base Branch&#x22; which is the target branch where changes are merged." />
</Frame>

What GitHub shows in a PR

* The list of commits included in the PR.
* All changed files with a line-by-line diff and inline commenting.
* Status checks and CI results (passing or failing).
* Mergeability status (clean merge vs. conflicts).
* A discussion thread for comments, requested changes, and resolutions.

Typical pull request workflow (commands)

| Purpose                               | Command                                                               |
| ------------------------------------- | --------------------------------------------------------------------- |
| Create and switch to a feature branch | `git checkout -b feature/my-feature`                                  |
| Stage and commit changes              | `git add .`<br />`git commit -m "Add my feature"`                     |
| Push branch and set upstream          | `git push -u origin feature/my-feature`                               |
| Open a PR on GitHub                   | Open a PR from `feature/my-feature` into `main` via the repository UI |

Merge methods: when to use each

| Merge method     | Description                                                     | When to use                                                           |
| ---------------- | --------------------------------------------------------------- | --------------------------------------------------------------------- |
| Merge commit     | Preserves full history and creates a merge commit               | When you want an explicit merge node showing branch integration       |
| Squash and merge | Combines all PR commits into a single commit on the base branch | When you want a concise, linear history for the base branch           |
| Rebase and merge | Rebases PR commits onto the base branch without a merge commit  | When you want linear history but retain individual commit granularity |

Handling merge conflicts
If GitHub reports merge conflicts, update your branch and resolve them locally, then push the resolved branch back to the remote. Two common approaches are merge or rebase:

Merge approach:

```bash theme={null}
git checkout feature/my-feature
git fetch origin
git merge origin/main
