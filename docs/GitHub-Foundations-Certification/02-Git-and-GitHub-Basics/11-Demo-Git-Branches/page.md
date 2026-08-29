# Initialize a repository
git init

# Stage and commit changes
git add .
git commit -m "Describe changes"

# Create and switch to a branch
git checkout -b feature-branch

# Push to a remote repository
git push origin feature-branch
```

What GitHub provides

* A web interface for browsing and managing repositories
* Collaboration via [pull requests](https://docs.github.com/en/pull-requests) for code review and discussion before merging
* [Issue tracking](https://docs.github.com/en/issues) and threaded discussions for planning and communication
* Project management tools such as [project boards](https://docs.github.com/en/issues/planning-and-tracking-with-projects/using-projects/about-projects) and [labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work)
* Automation and CI/CD with [GitHub Actions](https://docs.github.com/en/actions)

<Frame>
  <img alt="The image is an infographic illustrating the components of GitHub as &#x22;The Collaboration Platform&#x22; with features like Pull Requests and GitHub Actions, and Git as &#x22;The Engine&#x22; with functionalities such as Command Line and Local Version Control." />
</Frame>

Quick comparison

| Aspect                | Git (local)                                         | GitHub (remote platform)                                                  |
| --------------------- | --------------------------------------------------- | ------------------------------------------------------------------------- |
| Primary purpose       | Distributed version control, history, branching     | Remote hosting, collaboration, automation, project management             |
| Typical commands      | `git init`, `git commit`, `git branch`, `git merge` | Web UI, pull requests, Actions, Issues                                    |
| Offline support       | Full workflow available locally                     | Requires internet for remote features and collaboration                   |
| Collaboration         | Manual (push/pull, email, patches)                  | Built-in: forks, pull requests, reviews, discussions                      |
| CI / Automation       | External tools or custom scripts                    | Built-in with [GitHub Actions](https://docs.github.com/en/actions)        |
| Security & governance | Local policies and tooling                          | Enterprise features: code scanning, secret scanning, Dependabot, and more |

GitHub also supports open collaboration workflows: you can fork repositories to experiment independently and then submit pull requests to propose changes back to the original project.

Beyond basic collaboration, GitHub Enterprise extends productivity and security for organizations. It integrates features such as [Copilot](https://github.com/features/copilot), [Copilot Chat](https://docs.github.com/en/copilot/getting-started-with-github-copilot-chat), and Copilot Agents ([https://github.blog/2024-03-05-introducing-github-copilot-agents/](https://github.blog/2024-03-05-introducing-github-copilot-agents/)) to assist developers, and provides built-in security tooling like [CodeQL](https://docs.github.com/en/code-security/code-scanning/using-codeql-code-scanning), [secret scanning](https://docs.github.com/en/code-security/secret-scanning), [Dependabot](https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically), and a consolidated [Security Overview](https://docs.github.com/en/organizations/keeping-your-organization-secure/about-security-overview) to surface risks earlier in the development lifecycle.

> **lightbulb** Git manages the history and structure of your code locally. GitHub layers collaboration, code review, automation, and security on top of Git so teams can build, test, and deliver software together.

<Frame>
  <img alt="The image displays a grid of labeled icons related to GitHub features, including Issues, Pull Requests, GitHub Actions, Projects, Labels, and more. Each icon is enclosed in a box with its corresponding label beneath it." />
</Frame>

In short: use Git as your local version control engine and GitHub as the platform for sharing, reviewing, automating, and securing your projects. For further reading and official guides, see the Git documentation and the GitHub Docs.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/9376ab80-5da3-4f55-91cc-f43a650fd052)


# Demo Git Branches

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Demo-Git-Branches/page

A practical guide to using Git branches to develop features, commit changes, and merge safely, demonstrated with a sample feature changing game colors and starting lives.

Once a project is in version control, you need a safe way to try new ideas without destabilizing the main codebase. Branching in Git is the standard way to:

* develop multiple features in parallel,
* iterate on experiments, and
* isolate bug fixes until they’re ready to land.

A branch is simply a lightweight pointer to a commit. Create a branch for each independent piece of work so you can iterate safely and merge only when ready.

> **lightbulb** Create a branch for each independent piece of work. Branches are cheap and let you iterate safely.

## Inspecting branches

List branches in your repository:

```bash theme={null}
git branch --list
```

Typical output when only `main` exists:

```bash theme={null}
* main
```

## Creating and switching branches

Create a new branch without switching to it:

```bash theme={null}
git branch exploring-coloring
```

Switch to that branch:

```bash theme={null}
git checkout exploring-coloring
```

You can create and switch in a single step:

```bash theme={null}
git checkout -b exploring-coloring
