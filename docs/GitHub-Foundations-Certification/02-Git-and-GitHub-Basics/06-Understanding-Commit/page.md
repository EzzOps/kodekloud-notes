# Create and switch to a feature branch
git checkout -b feature/login-form

# Stage and commit changes
git add .
git commit -m "Add login form component"

# Push branch to remote and set upstream
git push -u origin feature/login-form

# Update branch from main (merge)
git checkout feature/login-form
git fetch origin
git merge origin/main

# Or rebase onto main (see warning below)
git checkout feature/login-form
git fetch origin
git rebase origin/main
```

Merge strategies

* Merge commit: preserves all commits and creates a merge commit (`git merge`).
* Squash-and-merge: combines all branch commits into a single commit on `main`.
* Rebase-and-merge: rewrites branch commits on top of `main` to create a linear history.

Table: Branch types and use cases

| Branch type    | Use case                                   | Example              |
| -------------- | ------------------------------------------ | -------------------- |
| `main`         | Production-ready code, deployed frequently | `main`               |
| Feature branch | New features, experiments                  | `feature/login-form` |
| Hotfix branch  | Critical bug fixes for production          | `hotfix/urgent-500`  |
| Release branch | Preparing a release, last-minute fixes     | `release/1.2.0`      |

Best practices

* Use short, descriptive branch names, e.g. `feature/login-form`, `fix/calc-bug-123`.
* Keep `main` deployable at all times.
* Run CI locally (or via pre-commit hooks) to reduce failing checks in PRs.
* Keep branches up to date with `main` by merging or rebasing regularly to minimize conflicts.
* Prefer small, focused pull requests for easier review.

> **lightbulb** Use clear, short branch names (for example `feature/login-form` or `fix/calc-bug-123`) and keep `main` deployable. Run CI locally (or via pre-commit hooks) before pushing to reduce noisy failures in pull requests.

> **warning** Avoid rebasing branches that are already pushed and shared with others unless your team agrees—rewriting history can disrupt collaborators. Use `merge` for shared branches, or coordinate a force-push after rebasing.

Keeping branches healthy

* Regularly merge or rebase changes from `main` into your feature branch.
* Address CI failures quickly and update the PR with fixes.
* Use branch protection rules (required reviews, required status checks) to enforce quality gates.

Links and references

* [Git Documentation](https://git-scm.com/doc)
* [Git Branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
* [GitHub Docs: About Branches](https://docs.github.com/en/get-started/using-git/about-branches)

Summary
Branching is a core Git workflow that enables safe, parallel development and a controlled review-and-merge process so `main` remains stable and ready for deployment. Follow naming conventions, keep branches current with `main`, and use CI and code reviews to ensure high-quality merges.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/2141e09c-1f74-4971-b9be-47947931f60c)


# Understanding Commit

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Understanding-Commit/page

Explains Git commits as permanent snapshots, how to stage and create them, commit message best practices, metadata, commands like git add and git commit, importance in version control

What is a commit?

In Git, saving files isn't just a simple "save" — you create a commit. A commit records a permanent snapshot of your project at a specific moment in time. It captures the exact state of tracked files so you can inspect, compare, or revert changes later.

<Frame>
  <img alt="The image features two panels illustrating the concept of a Git commit. The left panel shows buttons labeled &#x22;Save&#x22; and &#x22;Commit,&#x22; while the right panel depicts a camera icon with text explaining a commit as a &#x22;permanent snapshot of your work at a specific moment.&#x22;" />
</Frame>

How commits work — quick overview

* You stage changes you want to include in the next snapshot.
* You create a commit with a short, descriptive message that explains the reason for the change.
* The commit records the staged content and stores metadata such as author, timestamp, message, and a unique identifier (SHA).
* The repository history becomes a sequence of commits (snapshots) that can be reviewed or restored.

Staging and creating commits

Before a commit, changes must be staged. Typical commands:

```bash theme={null}
