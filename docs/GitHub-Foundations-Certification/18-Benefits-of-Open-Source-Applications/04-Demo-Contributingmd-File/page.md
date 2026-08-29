# file in root directory
```

When a `README.md` exists in the repository root, GitHub will render that content on the repository home page instead of `docs/README.md`. If multiple README files exist (root, `docs/`, and `.github/`), GitHub chooses which to display based on its rendering rules and repository configuration. To avoid ambiguity, place the README you want visitors to see in the repository root.

<Frame>
  <img alt="This is a screenshot of a GitHub repository named &#x22;block-buster,&#x22; showing its file structure, recent commits, and repository details. The repository includes folders like .devcontainer, .github, and docs, as well as files like README.md, LICENSE, and others." />
</Frame>

Example README files used in this demo

* `docs/README.md`

```markdown theme={null}
## file in docs folder
```

* `README.md` (root)

```markdown theme={null}
# file in root directory
```

* `.github/README.md`

```markdown theme={null}
# file in **.GITHUB** directory
```

<Frame>
  <img alt="The image shows a Visual Studio Code interface displaying a file explorer pane with a directory structure for a GitHub project called &#x22;BLOCK-BUSTER&#x22; and a README.md file open in the editor." />
</Frame>

Recommendation: if you want a specific README shown to visitors, place it in the repository root. This avoids surprises caused by multiple READMEs competing for rendering priority.

Four elements that make a repository discoverable

<Frame>
  <img alt="The image shows a GitHub repository named &#x22;block-buster&#x22; with a list of files and folders, including details about commits and timing. On the right, there's a description stating it's an enhanced version of a brick breaker game." />
</Frame>

* A clear, descriptive repository name
* A short, helpful repository description
* A license file (e.g., MIT or Apache 2.0)
* A README placed where it will be rendered for visitors (commonly the repository root)

<Callout icon="lightbulb">
  A well-written README and an explicit license dramatically increase the chances that others will find, trust, and contribute to your project. Invest a little time up front—clear names, a concise description, and the right README placement improve visibility, search ranking, and contributor confidence.
</Callout>

Links and resources

* [MIT License](https://opensource.org/licenses/MIT)
* [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
* Open a repo in the browser editor: `https://github.dev/<owner>/<repo>`

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/1231fb21-5b25-4a68-8d38-373808b0ba92/lesson/1aeeae77-0bef-4504-9b82-94fe3c6c6709" />
</CardGroup>


# Demo Contributingmd File

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Benefits-of-Open-Source-Applications/Demo-Contributingmd-File/page

Guide for creating a CONTRIBUTING.md to help contributors report bugs, request features, submit pull requests, and follow project workflows and best practices

A CONTRIBUTING.md file documents how people can contribute to your repository. It clarifies expectations, streamlines the contribution process, and reduces friction for maintainers and contributors alike.

Why include a CONTRIBUTING.md

* Improves onboarding for new contributors.
* Sets clear guidelines for reporting bugs and proposing features.
* Documents project-specific workflows (branching, commit messages, PR process).
* Enables GitHub to surface the guidelines in the issues and pull request flows.

What to include (typical sections)

| Section                    | Purpose                                                          | Example / Notes                                                              |
| -------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Welcome & thanks           | Make contributors feel welcome and explain the project's purpose | A short sentence like “Thanks for contributing — here’s how to get started.” |
| Table of contents          | Quick navigation for longer docs                                 | Use anchors for headings.                                                    |
| Code of conduct            | Link or include your code of conduct                             | Reference a `CODE_OF_CONDUCT.md` if present.                                 |
| How to report bugs         | Steps to file a useful issue (template, required info)           | Include reproduction steps and expected vs actual behavior.                  |
| How to request features    | Explain what information helps evaluate requests                 | Provide use case, goals, and alternatives considered.                        |
| How to submit a PR         | PR checklist, branch naming, commit message style                | Example: `feat/<short-description>`, include tests and a changelog entry.    |
| Local dev & tests          | Step-by-step setup and commands to run tests                     | Provide commands and common troubleshooting tips.                            |
| CI / contribution workflow | How contributions are validated and merged                       | Explain required status checks and who can merge.                            |
| Contact / support          | Where to ask for help (chat, mail, issue labels)                 | Link maintainers or support channels.                                        |

Where to put the file

* Create `CONTRIBUTING.md` at the repository root or inside the `.github` directory. GitHub displays the content in issue and PR flows when present.

Example workflow (create the file and push it to the repo)

1. Add a new file: `.github/CONTRIBUTING.md` (or `CONTRIBUTING.md` at the repo root).
2. Populate it with the sections above, replacing placeholders with project-specific links and examples.
3. Commit and push the change so it’s discoverable in the repository.

Example git commands:

```bash theme={null}
git add .github/CONTRIBUTING.md
git commit -m "Add CONTRIBUTING.md"
git push origin main
```

Back in the repository view you should see the new file listed with the recent commit message.

<Frame>
  <img alt="The image shows a GitHub repository page with directories and files listed, along with recent commit messages. On the right, there is a brief description of the repository and options related to repository management and settings." />
</Frame>

How contributors see the file

* When a contributor opens a new issue or creates a pull request, GitHub will show a reminder if your repository includes contribution guidelines.
* The reminder appears as a short prompt like “contributions to this repository should follow its contributing guidelines” and links directly to the `CONTRIBUTING.md` file so contributors can review it before submitting.

<Frame>
  <img alt="The image shows a GitHub interface with a pop-up window for creating a new issue in a repository named &#x22;block-buster.&#x22; The window includes a form for inputting screenshots, device information, and additional context." />
</Frame>

Best practices for writing your CONTRIBUTING.md

* Be specific and actionable: provide step-by-step setup instructions and exact commands for tests and builds.
* Link to related documents: `CODE_OF_CONDUCT.md`, issue/PR templates, and relevant project docs.
* Keep it up to date: revise the file when workflows, CI, or maintainers change.
* Make it welcoming: include a short thank-you and clear next steps for first-time contributors.
* Use examples: show a sample issue report and a sample PR description to set expectations.
* Document automation: clarify required CI checks, labels, and who handles approvals and merges.

Additional resources

* GitHub: CONTRIBUTING guidelines — [https://docs.github.com/en/github/building-a-strong-community/setting-guidelines-for-repository-contributors](https://docs.github.com/en/github/building-a-strong-community/setting-guidelines-for-repository-contributors)
* Example templates and community standards — search popular open-source projects for real-world examples.

<Callout icon="lightbulb">
  Place `CONTRIBUTING.md` at the repository root or in the `.github` directory. GitHub automatically links to it from the new issue and pull request interfaces, helping contributors follow your project's process.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/1231fb21-5b25-4a68-8d38-373808b0ba92/lesson/a4a1120d-140f-45f5-8098-0602c192d3bf" />
</CardGroup>
