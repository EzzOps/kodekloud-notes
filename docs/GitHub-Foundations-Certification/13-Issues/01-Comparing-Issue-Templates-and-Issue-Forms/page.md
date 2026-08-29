# clone a repository
git clone git@github.com:owner/repo.git

# make changes, stage, and commit
git add .
git commit -m "Add feature X"

# fetch and merge remote changes, then push your commit
git fetch origin
git merge origin/main
git push origin feature-branch
```

## Exploring the GitHub platform

You’ll get hands-on with the GitHub UI and features that help teams collaborate and deliver reliably. Topics include repository insights (code frequency, dependency graph, network), forks, and how to configure visibility and branch protection.

<Frame>
  <img alt="The image displays a GitHub repository insights page, highlighting features like code frequency, dependency graph, network visualization, and a list of forks. A person appears in a circular cutout at the bottom right, wearing a KodeKloud shirt." />
</Frame>

## Course outline (at a glance)

| Module                  | Focus                           | Example outcomes                                |
| ----------------------- | ------------------------------- | ----------------------------------------------- |
| Git basics              | Local repo, staging, commits    | `git init`, `git add`, `git commit`             |
| Branching & merging     | Feature branches, pull requests | Create & review PRs, resolve merge conflicts    |
| GitHub platform         | Repos, insights, forks          | Configure repo settings, analyze graphs         |
| Collaboration           | Issues, discussions, docs       | Use issues, link PRs to issues, maintain README |
| Automation              | GitHub Actions & workflows      | CI pipeline that runs tests on PRs              |
| Developer tools         | Copilot, Codespaces             | Use AI suggestions and cloud dev environments   |
| Security & permissions  | Auth, access control            | Set branch protection, manage teams             |
| Open source & community | Contributing & inner source     | Forking workflow, CLA basics                    |
| Exam prep               | Practice assessments            | Mock exams and knowledge checks                 |

## Who this course is for

* Developers and engineers new to GitHub who want practical, job-ready skills.
* DevOps professionals seeking to automate CI/CD using GitHub Actions.
* Contributors to open source projects who want to understand collaboration workflows.
* Teams adopting GitHub for code review, security, and project management.

## How you’ll learn

* Short conceptual lessons followed by hands-on labs in realistic scenarios.
* Step-by-step exercises to practice Git commands, create PRs, configure Actions, and manage security.
* Practice assessments that simulate the certification exam experience.

## Useful links and references

* [GitHub Actions](https://learn.kodekloud.com/user/courses/github-actions)
* [GitHub Copilot](https://learn.kodekloud.com/user/courses/github-copilot-in-action)
* [GitHub Codespaces](https://github.com/features/codespaces)
* [Git documentation](https://git-scm.com/doc)
* [GitHub Docs - Getting started](https://docs.github.com/en/get-started)

Ready to become proficient with GitHub? Enroll now to start learning one of the most important skills in modern software development.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/6a8acd05-8655-4850-a5bf-bc3320d9feb3/lesson/2200940a-bc54-4cc4-89fe-4a51d4f70462" />
</CardGroup>


# Comparing Issue Templates and Issue Forms

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Issues/Comparing-Issue-Templates-and-Issue-Forms/page

Comparison of GitHub Markdown issue templates and YAML issue forms, their differences, use cases, validation, and guidance for choosing and authoring templates or forms.

What’s the difference between GitHub issue templates (Markdown) and issue forms (YAML)? Both are designed to standardize how contributors open issues and to improve the quality of incoming reports. They differ mainly by format, user experience, enforcement options, and ideal use cases. This guide explains those differences, provides examples, and highlights when to use each approach.

## File format and user experience

* Issue templates are plain Markdown files that pre-fill the issue description with headings, prompts, and checklists. Contributors see editable text in the description box and can change anything before submitting.
* Issue forms are defined in YAML and render as a structured UI made of fields (text inputs, textareas, checkboxes, dropdowns, etc.), giving contributors a guided experience and clearer prompts.

Benefits at a glance:

* Markdown templates: easy to author, flexible, familiar to contributors.
* YAML issue forms: structured data, better validation, easier to use for automation and triage.

## Examples

Example: a simple Markdown issue template

```markdown theme={null}
---
name: Bug report
about: Create a report to help us improve
---

**Describe the bug**
A clear and concise description of what the bug is.

**Steps to reproduce**
1. Go to ...
2. Click on ...
3. See error

**Expected behavior**
A short description of what you expected to happen.

**Environment**
- OS: 
- Browser:
```

Example: an issue form (YAML) that enforces structured input

```yaml theme={null}
name: Bug report
description: Report a bug affecting the project
body:
  - type: input
    id: title
    attributes:
      label: Short summary
      description: One-line summary of the issue
      placeholder: "e.g. Crash when opening settings"
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: Provide step-by-step instructions
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Operating system
      options:
        - Windows
        - macOS
        - Linux
    validations:
      required: true
```

## Side-by-side comparison

|           Feature | Issue Templates (Markdown)                               | Issue Forms (YAML)                                             |
| ----------------: | -------------------------------------------------------- | -------------------------------------------------------------- |
|       File format | Markdown (`.md`)                                         | YAML (`.yml`)                                                  |
|   User experience | Free-form description box (editable text)                | Structured UI with labeled fields                              |
| Input flexibility | Contributors can edit or remove prompts                  | Fields can be required and validated                           |
|  Data enforcement | No built-in validation; easy to submit incomplete issues | `required` validations and field types enforce input           |
|          Best for | Lightweight guidance, checklists, small projects         | Bugs, feature requests, triage flows needing consistent fields |

<Frame>
  <img alt="The image is a table comparing &#x22;Issue Templates&#x22; and &#x22;Issue Forms&#x22; across several features like file format, user experience, input flexibility, data enforcement, and best use case. The table highlights key differences between the two in terms of configuration, interaction, and application." />
</Frame>

While both mechanisms share the same goal—collecting better information from contributors—they diverge in how they guide users and how much structure and validation they provide.

## When to use which

* Use issue templates (Markdown) when:
  * You want quick, flexible guidance or checklists.
  * The project is small or contributions are informal.
  * You don’t need strict, machine-readable fields.

* Use issue forms (YAML) when:
  * You need consistent, structured input (e.g., OS, reproduction steps, logs).
  * You want to enforce required fields to improve triage.
  * You plan to automate issue handling, labels, or routing based on field values.

## Quick tips for authors

* Convert high-value templates to forms if you repeatedly need the same structured fields.
* Keep forms concise: too many required fields can discourage contributors.
* Provide helpful placeholders and examples to reduce low-quality reports.
* Use labels, issue actions, or GitHub Actions to automate workflows based on form fields.

## Links and references

* [GitHub Docs: About issue templates](https://docs.github.com/en/issues/managing-your-work-on-github/managing-issues/about-issue-templates)
* [GitHub Docs: Creating issue forms](https://docs.github.com/en/issues/creating-cloning-and-archiving-repositories/creating-issue-forms-for-your-repository)

<Callout icon="lightbulb">
  Choose Markdown templates when you need flexibility and light guidance. Choose YAML-based issue forms when you need consistent, enforceable fields that improve triage, automation, and data quality.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/3105bbb3-1ddf-433d-9b4f-15a905853817/lesson/6d88c1f2-6902-4d7e-ae09-505bf28daab5" />
</CardGroup>
