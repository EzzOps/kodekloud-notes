# Example: create a feature branch from main
git checkout main
git pull origin main
git checkout -b feature/user-authentication
```

> **lightbulb** Always branch off the latest `main` (or `develop`) to incorporate recent updates and avoid merge conflicts.

***

## Opening a Pull Request

When your branch is ready, open a PR to initiate feedback and track changes.

1. Push your branch to the remote:
   ```bash theme={null}
   git push -u origin feature/user-authentication
   ```
2. In your repository UI (GitHub/GitLab/Azure Repos), click **New Pull Request**.
3. Fill in:
   * **Title**: concise, descriptive (e.g., “Add JWT-based authentication”)
   * **Description**: summary, related issues, screenshots, test steps
4. Assign reviewers, add labels, and select appropriate milestone.

> **lightbulb** Use templates for consistent PR descriptions: link to the issue, outline changes, list test instructions.

***

## Collaborating & Reviewing

A healthy review process reduces defects and spreads knowledge across the team.

* **Line-by-line comments**\
  Suggest improvements or ask questions on specific code sections.
* **Threaded discussions**\
  Resolve design debates without cluttering commit history.
* **Automated checks**\
  Integrate CI/CD pipelines to run tests, linting, and security scans.

| Review Stage       | Action                                | Tooling Example                          |
| ------------------ | ------------------------------------- | ---------------------------------------- |
| Automated Builds   | Validate code compiles and tests pass | GitHub Actions, Jenkins, Azure Pipelines |
| Peer Review        | Manual code inspection & feedback     | GitHub Reviews, GitLab Approvals         |
| Policy Enforcement | Enforce branch protection & sign-offs | Required reviewers, status checks        |

> **triangle-alert** Do not merge before all required checks and approvals are completed. Merging early can introduce regressions or untested code into `main`.

***

## Merging & Cleanup

Once approved and green, it’s time to merge and tidy up.

```bash theme={null}
# Switch to main and pull latest changes
git checkout main
git pull origin main

# Merge with squash or merge commit
git merge --no-ff feature/user-authentication

# Push merged code
git push origin main

# Delete feature branch locally and remotely
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

Selecting **Squash and Merge** creates a single commit per PR for a cleaner history, while **Rebase and Merge** preserves each commit’s detail.

***

![The image illustrates the process of enhancing teamwork via pull requests, highlighting three stages: "Branch Out," "Collaborate," and "Merge." It emphasizes pull requests as communication tools, shared development, and code management best practices.](https://kodekloud.com/kk-media/image/upload/v1752867328/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Collaborate-with-pull-requests/teamwork-pull-requests-process-diagram.jpg)

***

## References & Resources

* [GitHub Pull Requests](https://docs.github.com/en/pull-requests)
* [GitLab Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
* [Azure Repos PR Overview](https://docs.microsoft.com/azure/devops/repos/git/pull-requests)
* [Atlassian Bitbucket Pull Requests](https://support.atlassian.com/bitbucket-cloud/docs/create-a-pull-request/)

By following this structured workflow—**Branch**, **Open PR**, **Collaborate**, and **Merge**—teams maintain code quality, foster knowledge sharing, and streamline releases.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/8e033a7f-4740-4d37-9f97-54ebc9c54fd1/lesson/d3079e50-2c63-4e48-97ed-b65dda9e29b6)


# Creating an Effective Change Log

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Branching-Strategies-for-Source-Code/Creating-an-Effective-Change-Log/page

An up-to-date changelog is essential for tracking a project’s evolution and communicating changes effectively to contributors and users.

An up-to-date changelog is essential for tracking a project’s evolution, communicating new features, fixes, and deprecations. By following best practices, you ensure that contributors, stakeholders, and end users can quickly understand what’s changed between releases.

![The image outlines the purpose of a change log, highlighting three key aspects: addition of new features, modifications to existing features, and deletion of outdated features.](https://kodekloud.com/kk-media/image/upload/v1752867339/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Creating-an-Effective-Change-Log/change-log-purpose-new-features-modifications.jpg)

## 1. Key Principles for a Maintainable Changelog

### 1.1 Clarity Over Quantity

Focus on concise, relevant entries. Avoid verbose descriptions—each item should add clear value so readers can scan updates efficiently.

> **lightbulb** A streamlined changelog encourages adoption and reduces confusion. Keep each bullet to one idea and link to detailed issues or PRs when needed.

## 2. Changelog Generation Strategies

Choose an approach that fits your team’s workflow and project size. Below is a comparison of the three most common methods:

| Strategy             | Pros                               | Cons                              | Example Tool                                          |
| -------------------- | ---------------------------------- | --------------------------------- | ----------------------------------------------------- |
| Manual entries       | High accuracy, contextual comments | Time-consuming, error-prone       | —                                                     |
| Automated population | Fast, consistent format            | May lack semantic grouping        | [GitHub Actions](https://github.com/features/actions) |
| Hybrid method        | Best of both worlds                | Requires setup and review process | Custom scripts + manual review                        |

![The image outlines three strategies for change log generation: manual entries for clarity, automated population for efficiency, and hybrid methods combining automation with oversight.](https://kodekloud.com/kk-media/image/upload/v1752867340/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Creating-an-Effective-Change-Log/change-log-generation-strategies-outline.jpg)

## 3. Essential Tools to Assist

There are several popular utilities designed to simplify changelog maintenance:

| Tool                         | Description                                    | Link                                                                                                               |
| ---------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Standard `git log`           | Base command-line history export               | —                                                                                                                  |
| `gitchangelog`               | Generates Markdown from git history            | [https://github.com/vaab/gitchangelog](https://github.com/vaab/gitchangelog)                                       |
| `github_changelog_generator` | Produces GitHub-style changelogs automatically | [https://github.com/skywinder/github-changelog-generator](https://github.com/skywinder/github-changelog-generator) |

![The image is a slide titled "Tools to Assist," featuring two numbered sections: one about using the standard git log for command-line entries, and another about using gitchangelog and github\_changelog\_generator for automated solutions.](https://kodekloud.com/kk-media/image/upload/v1752867341/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Creating-an-Effective-Change-Log/tools-to-assist-git-log-automation.jpg)

### 3.1 Practical Example: Customizing `git log` Output

Below is a sample Bash command to extract commits between two tags, format the output, and save it as a Markdown file:

```bash theme={null}
git log --pretty=format:"%h - %s (%an, %ar)" \
  v1.2.0..v1.3.0 \
  | script-to-format-changelog \
  > projectchangelogs/1.3.0.md
```

* `--pretty=format:"%h - %s (%an, %ar)"`
  * `%h` : abbreviated commit hash
  * `%s` : commit message
  * `%an`: author name
  * `%ar`: author date, relative
* `v1.2.0..v1.3.0` specifies the tag range to compare
* `script-to-format-changelog` represents your custom formatting script
* Redirect output into `projectchangelogs/1.3.0.md` for Markdown storage

> **triangle-alert** Be mindful of exposing sensitive or internal details in public changelogs. Always review entries before publishing.

## Links and References

* [Conventional Commits](https://www.conventionalcommits.org/)
* [Keep a Changelog](https://keepachangelog.com/)
* [Git Documentation – git log](https://git-scm.com/docs/git-log)
* [GitHub Actions](https://github.com/features/actions)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/8e033a7f-4740-4d37-9f97-54ebc9c54fd1/lesson/f2fe8fb3-27fa-423e-97cd-8b74ccfa07b9)
