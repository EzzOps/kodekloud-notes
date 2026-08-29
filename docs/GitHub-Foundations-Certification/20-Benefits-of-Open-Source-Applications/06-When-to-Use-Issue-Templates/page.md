# When to Use Issue Templates

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Benefits-of-Open-Source-Applications/When-to-Use-Issue-Templates/page

Guidance on when to use GitHub issue versus pull request templates, where to store them, and how to configure templates for consistent contributor submissions.

This guide explains when to use GitHub issue templates versus pull request (PR) templates, where to store them, and how to configure them so contributors and maintainers get consistent, high-quality information up front.

GitHub starter templates for issues and pull requests inject structure directly into the contributor’s workflow. Instead of asking contributors to hunt for contribution guidelines, templates put required fields and checklists into the editor as work begins. This reduces back-and-forth, surfaces actionable details on the first interaction, and shifts some of the organizational effort from maintainers to contributors.

## When to use each

Use issue templates when you need structured input from reporters (e.g., bug reports, feature requests, or support questions). Use pull request templates when you want every proposed change to follow a checklist that enforces testing, documentation, changelog updates, and links to related issues.

| Topic           |                                                                                   Issue Templates | Pull Request Templates                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------: | --------------------------------------------------------------------------------------------- |
| Primary purpose |                     Guide reporters to provide structured context for bugs, features, or feedback | Enforce a checklist and guidance to ensure quality and traceability of code changes           |
| User experience | Reporter selects a template (e.g., "Bug report" or "Feature request") and fills prompted sections | Template content automatically populates the PR description when a new PR is created          |
| Key benefits    |                     Reduces follow-up by mandating logs, environment info, and reproduction steps | Ensures PRs include tests, docs, changelog, and linked issues — improving reviewer confidence |
| Selection logic |                                                                  Manual selection by the reporter | Automatic insertion for every new PR (or default PR template)                                 |

To summarize: issue templates help you clearly understand the problem being reported; pull request templates help you assess and trust the proposed solution. Together, they streamline contributions and protect the project’s health.

<Frame>
  <img alt="The image is a comparison table between Issue Templates and Pull Request Templates, outlining their primary purpose, user experience, key benefits, and logic type. It highlights manual selection for issue templates and automatic injection for pull request templates." />
</Frame>

## Technical requirements and where to put templates

GitHub only recognizes templates that meet a few repository and location rules. Follow these to ensure templates appear when contributors create issues or pull requests.

### Default branch

Templates must exist on the repository’s default branch (for example, `main`). If templates live only on feature branches, they will not be available to contributors.

> **warning** Always commit template files to the repository’s default branch (e.g., `main` or `master`). Templates on non-default branches will be ignored by GitHub.

### Recognized locations

GitHub scans the following locations (checked in the repository’s default branch):

* Repository root (e.g., `PULL_REQUEST_TEMPLATE.md`)
* `.github` directory (recommended)
* `docs` directory

Example valid paths:

```text theme={null}
/.github/ISSUE_TEMPLATE/bug_report.md
/.github/ISSUE_TEMPLATE/config.yml
/.github/PULL_REQUEST_TEMPLATE.md
/PULL_REQUEST_TEMPLATE.md
/docs/ISSUE_TEMPLATE/feature_request.md
```

### Filenames and casing

Filenames are not case-sensitive. For example, `PULL_REQUEST_TEMPLATE.md` and `pull_request_template.md` are equivalent.

### File formats

* Markdown (`.md`) is supported for both issue and pull request templates.
* Structured issue forms use YAML (`.yml` or `.yaml`) and must be placed in `.github/ISSUE_TEMPLATE/`. These forms let you define fields, types, and validation to guide reporters more strictly.
* When using multiple issue templates, include a `config.yml` inside `.github/ISSUE_TEMPLATE/` to control the template chooser, contact links, and whether blank issues are allowed.

> **lightbulb** If you provide multiple issue templates, include a `config.yml` file inside `.github/ISSUE_TEMPLATE/` to control which templates are shown and whether GitHub displays an issue form or a template chooser.

## Example templates

Here are common examples you can copy and adapt.

* Simple pull request template (`.github/PULL_REQUEST_TEMPLATE.md`):

```markdown theme={null}
## Summary

Please describe the changes introduced by this PR.

## Related issue

Fixes `#<issue-number>`

## Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changelog entry added (if applicable)
```

* Multiple issue templates with configuration (`.github/ISSUE_TEMPLATE/config.yml` and `.github/ISSUE_TEMPLATE/bug_report.md`):

`.github/ISSUE_TEMPLATE/config.yml`:

```yaml theme={null}
blank_issues_enabled: false
contact_links:
  - name: Support
    url: https://example.com/support
    about: For help with using the project
```

`.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown theme={null}
---
name: Bug report
about: Create a report to help us improve
labels: bug
---
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment**
- OS: 
- Browser:
- Version:
```

## Best practices summary

* Use issue templates when you expect diverse reporter input (bugs, feature requests, security reports).
* Use pull request templates to enforce a consistent submission checklist and tie PRs to issues.
* Store templates on the repository’s default branch and in one of the recognized locations (`root`, `.github`, or `docs`).
* When offering multiple issue templates, include `.github/ISSUE_TEMPLATE/config.yml` to control presentation and contact links.
* Prefer structured issue forms (YAML) when you need validation and typed fields; use Markdown templates for flexible, free-form input.

## Links and references

* [GitHub Docs: Creating issue templates for your repository](https://docs.github.com/en/issues/creating-labels-and-milestones-for-issues-and-pull-requests/about-issue-and-pull-request-templates)
* [GitHub Docs: About pull request templates](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/creating-a-pull-request-template)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/1231fb21-5b25-4a68-8d38-373808b0ba92/lesson/ba689bf5-78b2-422a-b9f7-7cea1dcb7b41)
