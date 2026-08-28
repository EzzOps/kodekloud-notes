# Stage all changes (new files must be added explicitly)
git add .

# Commit staged changes with a message
git commit -m "Your commit message"
```

If you only modified files that are already tracked by Git, you can stage and commit in one step using `-a`:

```bash theme={null}
git commit -am "Update existing files with fixes"
```

Best practices for commit messages

<Callout icon="lightbulb">
  Write concise, meaningful commit messages that explain the why, not just the what. For new files, remember to stage them with `git add` before committing. Use the imperative tense for messages (e.g., "Fix bug in parser" instead of "Fixed bug in parser").
</Callout>

Commit metadata — what Git stores

| Field            | Description                        | Example                       |
| ---------------- | ---------------------------------- | ----------------------------- |
| Author           | Who made the change                | `Jane Doe <jane@example.com>` |
| Timestamp        | When the commit was created        | `2026-07-29 14:32:10 -0400`   |
| Message          | Short description of the change    | `Add user authentication`     |
| SHA (identifier) | Unique hash identifying the commit | `9fceb02`                     |

Inspect recent commits

Use `git log` to review history. For a compact view:

```bash theme={null}
git log --oneline
```

Example output:

```text theme={null}
9fceb02 Fix bug in parser
6a1b2c3 Add user authentication
e5f6a7d Initial commit
```

Why commits matter

Because each commit is a snapshot, your team can see how the project evolved, identify when and why a change happened, and revert to a known-good state when mistakes occur. Commits form the backbone of version control workflows like feature branching, code review, and continuous integration.

Further reading and references

* [Pro Git Book — Git Basics: Recording Changes to the Repository](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
* [Git Documentation — git-commit](https://git-scm.com/docs/git-commit)
* [Writing Good Commit Messages — Best Practices](https://chris.beams.io/posts/git-commit/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/1ee16c93-8e3a-4cf7-ab1d-c494e58ebad6" />
</CardGroup>


# Version Control

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Version-Control/page

Explains why Git and GitHub solve team version control problems and outlines a course roadmap to prepare for GitHub Foundations Certification.

Version control is the foundation of reliable software development. This article uses a realistic team scenario to explain why Git and GitHub are essential, then outlines the course roadmap to prepare you for the GitHub Foundations Certification.

Imagine Technova, a small startup with three team members: Alice (UI designer), Bob (backend developer), and Charlie (content writer). With their e-commerce launch tomorrow, lacking a proper version control system pushes them into fragile workflows that quickly break.

First, overwrites happen frequently. Bob uploads backend code and accidentally overwrites the brand-new layout Alice spent three days building.

<Frame>
  <img alt="The image shows three team members from &#x22;TechNova&#x22; with their roles: Alice (UI Designer), Bob (Backend Developer), and Charlie (Content Writer), and depicts a &#x22;Failure 01&#x22; scenario involving a ZIP file overwrite." />
</Frame>

Second, there are no rollbacks. Charlie updates a product description but accidentally removes a crucial piece of code that breaks the checkout page — and there's no simple way to revert to the prior working version.

<Frame>
  <img alt="The image shows three characters labeled as Alice (UI Designer), Bob (Backend Developer), and Charlie (Content Writer), along with a &#x22;Failure 02&#x22; message indicating a &#x22;ZIP&#x22; file with &#x22;No Rollback.&#x22;" />
</Frame>

Third, accountability is missing. When the website crashes at 5 p.m. on a Friday, no one can easily determine who changed what, when, or why — and everyone points fingers.

<Frame>
  <img alt="The image depicts a team interaction involving a UI designer, a backend developer, and a content writer, followed by a website crash labeled &#x22;Friday – 5 PM.&#x22; Below, it highlights &#x22;Failure 03: Lack of Accountability&#x22; with pointing finger icons." />
</Frame>

Finally, collaboration stalls. Alice and Bob cannot safely work on the same file at the same time without constantly breaking each other's work, slowing the team and increasing risk.

<Frame>
  <img alt="The image shows three team members: Alice (UI Designer), Bob (Backend Developer), and Charlie (Content Writer) from TechNova. Below them is &#x22;Failure 04,&#x22; depicting a collaboration issue due to ZIP files." />
</Frame>

<Callout icon="lightbulb">
  Version control removes these blockers by providing structured workflows for saving, collaborating, auditing, and recovering code. It replaces fragile ad-hoc methods (like zipped emails) with repeatable, auditable practices.
</Callout>

What solves Technova’s problems? Version control systems — specifically Git — combined with a collaborative hosting platform like GitHub. Together they deliver:

* Time machine: Each save (a commit) is a permanent snapshot of tracked files. If a change breaks the site, you can revert to a previous commit to restore a working state quickly.

<Frame>
  <img alt="The image shows three cartoon avatars labeled Alice, Bob, and Charlie with their respective roles, and below them, icons related to a &#x22;Solution 01&#x22; with the concept of a &#x22;Time Machine&#x22; and symbols like ZIP, commit, and save." />
</Frame>

* Parallel workspaces: Branching creates isolated lines of development so Alice and Bob can edit the same file concurrently in different branches. Changes can be validated before merging into the main site.

<Frame>
  <img alt="The image features three people with their roles—UI Designer, Backend Developer, and Content Writer—under a company name, with a proposed solution involving branching and parallel workspaces." />
</Frame>

* Audit trail: Git records who changed each line, when it changed, and includes commit messages that explain why. This auditability accelerates troubleshooting and reduces conflict.

* Single source of truth: GitHub stores the team’s history and collaboration artifacts (commits, branches, pull requests, reviews) in one secure location, replacing messy folders and zipped files.

<Frame>
  <img alt="The image shows three team roles—UI Designer, Backend Developer, and Content Writer—with their respective names under the banner &#x22;TechNova&#x22; and &#x22;Solution 04,&#x22; featuring the GitHub logo." />
</Frame>

Now that we’ve established why Git and GitHub are essential, below is the course roadmap to prepare you for the GitHub Foundations Certification. Each domain targets practical skills and industry best practices.

| Topic                                 | What you’ll learn                                                                                                                                          | Typical examples / outcomes                                                            |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Introduction to Git and GitHub        | Differences between Git (distributed VCS) and GitHub (hosting/collaboration). Core Git concepts: repositories, commits, branches.                          | Understand `git init`, `git commit`, and the role of a remote repository.              |
| Working with GitHub Repositories      | Initialize repositories, stage and commit changes, manage branch structure, and use essential Git commands.                                                | Practice `git add`, `git commit`, `git branch`, `git merge`, and `git log`.            |
| Collaboration Features                | Engineering workflows for proposing changes, code review processes, resolving merge conflicts, and using pull requests.                                    | Create and review pull requests, resolve conflicts, and apply branch protection rules. |
| Modern Development                    | GitHub ecosystem tools: automate CI/CD with GitHub Actions, develop in Codespaces, host content with GitHub Pages, and use Copilot for AI-assisted coding. | Build a simple GitHub Action workflow; deploy a static site to GitHub Pages.           |
| Project Management                    | Track work with Issues, labels, milestones, and GitHub Projects. Integrate task management with code.                                                      | Create issues, link PRs to issues, and manage an agile board.                          |
| Privacy, Security, and Administration | Enterprise governance, repository visibility, access controls, branch protection, Dependabot, and secret scanning.                                         | Configure branch protection, set repository permissions, and enable Dependabot alerts. |
| The GitHub Community                  | Open source collaboration patterns, forking workflows, contributing back, and building a professional GitHub profile.                                      | Fork a repo, submit a pull request, and manage a contributions graph.                  |

Below are the same topics presented visually in the learning materials you’ll encounter during the course.

<Frame>
  <img alt="The image is a part of a presentation slide showing a learning module outline related to Git and GitHub, including topics like version control fundamentals and key Git terminology." />
</Frame>

<Frame>
  <img alt="The image shows a learning progression chart for working with GitHub repositories, detailing tasks like repository creation, staging changes, branch management, merging strategies, essential Git commands, and commit history structuring." />
</Frame>

<Frame>
  <img alt="The image shows a timeline with steps for learning Git and GitHub, specifically focusing on collaboration features such as pull requests, code review, and managing merge conflicts. Each step is highlighted with a colored dot." />
</Frame>

<Frame>
  <img alt="The image shows a list of GitHub features related to modern development, including GitHub Actions, Codespaces, GitHub Pages, Copilot, marketplace integrations, and workflow tools. It appears to be part of a course or presentation outline from KodeKloud." />
</Frame>

<Frame>
  <img alt="The image outlines a project management section of a Git and GitHub course, highlighting concepts such as GitHub Issues, labels, milestones, projects, and agile workflows." />
</Frame>

<Frame>
  <img alt="The image shows a timeline or list related to Git and GitHub topics, focusing on privacy, security, and administration. It includes headings like repository visibility, access control, branch protection, and organizational policies." />
</Frame>

<Frame>
  <img alt="The image outlines a Git and GitHub learning path featuring seven topics, focusing on open-source collaboration, managing contributions, and networking within the GitHub community." />
</Frame>

By completing these seven domains you’ll gain hands-on, practical skills in Git and GitHub: creating and managing repositories, collaborating safely across branches, automating workflows, securing code, and contributing to the open-source community — all aligned with the GitHub Foundations Certification objectives.

Links and references

* Official Git documentation: [https://git-scm.com/doc](https://git-scm.com/doc)
* GitHub Docs: [https://docs.github.com/](https://docs.github.com/)
* GitHub Actions: [https://docs.github.com/en/actions](https://docs.github.com/en/actions)
* GitHub Pages: [https://pages.github.com/](https://pages.github.com/)
* GitHub Learning Lab: [https://lab.github.com/](https://lab.github.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/283f1e98-efc7-4003-9946-920de806da32/lesson/7b406a54-a35d-4464-a1bf-c7d549484bcf" />
</CardGroup>
