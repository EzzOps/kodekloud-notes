# Record local work
git add .
git commit -m "Describe changes"

# Send local commits to a remote
git push origin main

# Retrieve remote changes (two common ways)
git fetch origin
git merge origin/main

# or (shortcut)
git pull origin main
```

> **lightbulb** Distributed does not mean “no server.” Most teams use remote hosting (for example, GitHub, GitLab, or a self-hosted Git server) to simplify collaboration, code review, CI/CD, and backups while still benefiting from Git’s distributed model.

<Frame>
  <img alt="The image illustrates a team workflow involving three roles—UI Designer, Backend Developer, and Content Writer—interacting through Git, with no central server present." />
</Frame>

In practical team environments, a hybrid approach is the norm: developers use full local history for offline work and fast local operations, and they rely on one or more remote hosts to coordinate sharing, run CI/CD, and enforce access control.

> **warning** Beware of shallow clones (e.g., `git clone --depth <n>`). They omit older history and can prevent full repository recovery if a remote is lost. Use shallow clones only when you understand the trade-offs.

Summary comparison

| Model       | Server role                                    | Failure impact                                                   | Typical examples / hosts                                |
| ----------- | ---------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- |
| Centralized | Central server holds the authoritative history | Single point of failure; clients need server for many operations | `CVS`, `Subversion`, `Perforce`                         |
| Distributed | Every clone contains full history              | Any up-to-date clone can restore the repository                  | `Git`, hosted on GitHub, GitLab, or self-hosted servers |

Links and references

* [Git — official site](https://git-scm.com/)
* [GitHub](https://github.com/)
* [GitLab](https://gitlab.com/)
* [Subversion — Apache](https://subversion.apache.org/)
* [CVS — Wikipedia](https://en.wikipedia.org/wiki/Concurrent_Versions_System)

In short: Git’s distributed architecture removes the single point of failure inherent in centralized systems, enables robust offline workflows, and gives teams flexible options for sharing and backing up history — while remote hosts provide the coordination and services teams typically depend on.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/a8cfd928-d761-4e99-9511-6320d7196077)


# Git and GitHub

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Git-and-GitHub/page

Explains Git and GitHub, their differences, and how they integrate in team workflows for version control, collaboration, and remote repository management.

In this lesson we’ll define Git and GitHub, explain how they differ, and show how they work together in a typical team workflow.

## What is Git?

Git is a distributed version control system you install and run locally. It acts as the underlying engine that records snapshots of your project, tracks file history, and manages branches. Because Git is local-first, you can create commits, explore history, and switch branches entirely offline.

Example: inspect recent commits with `git log`

```bash theme={null}
$ git log --oneline
b38d48f (HEAD -> main) added new image tag
```

Git is the technology actually performing versioning: commits, diffs, branches, merges, and local history are all handled by Git itself.

## What is GitHub?

GitHub is a cloud-based collaboration platform built on top of Git. It hosts remote repositories and adds tools and workflows that simplify team collaboration: code hosting, pull requests, issue tracking, CI/CD integrations, code review, and security scanning. GitHub stores authoritative remote copies of repositories and coordinates contributions across teams.

> **lightbulb** A helpful analogy: Git is the underlying technical protocol that routes messages, while GitHub is like the email client (Outlook or Gmail) that provides the interface, security filters, and organizational tools you interact with.

<Frame>
  <img alt="The image shows a diagram with GitOps and GitHub icons on the left, and Outlook and Gmail icons on the right, connected by an envelope symbol in the center, representing a technical protocol routing messages." />
</Frame>

## How Git and GitHub work together (typical team workflow)

1. Development begins locally:
   * A developer (e.g., Alice) edits files and makes commits in her local Git repository. Git records those commits on her machine.
2. Share changes to a remote:
   * When ready, Alice pushes her commits to a remote repository hosted on GitHub.
3. Collaborate via GitHub:
   * Team members (Bob, Charlie) pull the updates to their machines, review code, open pull requests, or create new branches for features or fixes.

This local-to-remote architecture keeps distributed teams synchronized while preventing accidental overwrites.

<Frame>
  <img alt="The image is a workflow diagram illustrating the process of writing and committing code changes locally, pushing them to a remote repository, and collaborating with team members who pull the latest changes." />
</Frame>

## Quick comparison: Git vs GitHub

| Aspect          | Git                                           | GitHub                                              |
| --------------- | --------------------------------------------- | --------------------------------------------------- |
| Purpose         | Local distributed version control system      | Cloud-hosted collaboration and repository service   |
| Runs on         | Developer's machine (CLI, GUI clients)        | Remote servers (web UI, APIs)                       |
| Examples        | `git commit`, `git branch`, `git log`         | Pull requests, Issues, Actions, repository settings |
| Offline support | Fully usable offline for commits and branches | Requires internet to push/pull and use web features |
| Primary value   | Precise versioning, local history, branching  | Collaboration, code review, CI/CD, audit trail      |

## Why this workflow matters

* Asynchronous collaboration: Developers can work concurrently without blocking one another, making distributed teams productive across time zones.
* Scalability: The same Git + GitHub workflows scale from small teams to enterprise organizations.
* Security and compliance: GitHub preserves a record of changes—who made them and when—providing an authoritative audit trail.
* Risk management and rollback: Commit history allows teams to revert to a known-good state if deployments fail. Note that while Git supports history rewriting (e.g., `rebase`, `--force`), best practices treat shared remote history as immutable to keep auditability and safe rollbacks.

Together, Git (local version-control engine) and GitHub (cloud collaboration platform) provide a reliable, scalable foundation for modern software development.

## Links and references

* [Git documentation](https://git-scm.com/doc)
* [GitHub Docs](https://docs.github.com/)
* [GitHub Learning Lab](https://lab.github.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/cdef17b5-1627-40d6-a9fd-14dca372739f)
