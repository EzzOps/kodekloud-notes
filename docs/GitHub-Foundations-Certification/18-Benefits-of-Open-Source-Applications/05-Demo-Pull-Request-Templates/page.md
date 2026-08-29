# Demo Pull Request Templates

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Benefits-of-Open-Source-Applications/Demo-Pull-Request-Templates/page

Guide on creating and storing GitHub pull request templates, showing single or multiple template setups, benefits, examples, and best practices to standardize PR descriptions.

Adding a pull request (PR) template to your repository helps contributors provide consistent, actionable PR descriptions. This guide explains where to place templates, how to create a single or multiple templates, and how the template appears when opening a PR on GitHub.

Create a single template or multiple templates

* Single template: Add a file named `pull_request_template.md` in one of these locations: repository root, the `docs` directory, or the `.github` directory.
* Multiple templates: Create a folder such as `PULL_REQUEST_TEMPLATE/` inside `.github` and add multiple Markdown files there. GitHub will surface those templates when a contributor opens a new PR.

<Frame>
  <img alt="The image shows a screenshot of a GitHub Docs page providing instructions on creating a pull request template, with details on how to name and store the template files." />
</Frame>

Why use PR templates

* Promote consistent PR descriptions that make reviews faster and more effective.
* Encourage contributors to link related issues and indicate the type of change.
* Ensure required checks or test confirmations are documented before merging.

Quick comparison: single vs multiple templates

| Use case           | Where to add                          | Example path                               |
| ------------------ | ------------------------------------- | ------------------------------------------ |
| Single template    | Repository root, `docs`, or `.github` | `.github/pull_request_template.md`         |
| Multiple templates | Folder inside `.github`               | `.github/PULL_REQUEST_TEMPLATE/feature.md` |

<Callout icon="lightbulb">
  Use the `.github` directory to keep repository metadata centralized. If you store templates in `docs` or the repository root, make sure contributors know where to find them.
</Callout>

Example: add a single template

* Create a single PR template file at `.github/pull_request_template.md`.
* The template should request a clear description, a reference to related issues, the type of change, and a minimal checklist to confirm tests and documentation.

Create a file named `pull_request_template.md` and paste the following content (customize it to match your project’s workflow):

```markdown theme={null}
## Description

Please provide a clear description of the changes in this PR.

Fixes: #<issue-number>

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist

- [ ] I have added tests where applicable
- [ ] I have updated the documentation
- [ ] I have run the project tests locally
```

Open the repository in the web editor or in your local editor (for example, VS Code), add the file under `.github`, and commit with a descriptive message like `Add PR template`.

<Frame>
  <img alt="The image shows a Visual Studio Code interface with a file named &#x22;pull_request_template.md&#x22; open, displaying markdown text related to descriptions, types of changes, and a checklist for code contributions. The sidebar lists files in a GitHub repository." />
</Frame>

How the template appears in a new pull request

* When a contributor creates a new PR, GitHub automatically pre-populates the PR description with the template content.
* Contributors replace placeholders with the actual description, reference issues with `Fixes: #<issue-number>`, and select the appropriate checkboxes.
* If the PR includes code changes, the PR editor displays file diffs below the description area. For example, a CSS change might show:

```css theme={null}
--accent-cyan: #a81566;
```

When the contributor clicks Create Pull Request, the content from the template remains editable and can be previewed before submission.

<Frame>
  <img alt="The image shows a GitHub interface for creating a pull request. It includes sections for adding a title, description, related issues, and type of change, along with checkboxes for a checklist and other project management options." />
</Frame>

Best practices

* Keep templates concise and focused—use checkboxes for required confirmations (tests, docs, security review).
* Include example issue links using `Fixes: #<issue-number>` so GitHub can auto-close linked issues when the PR is merged.
* Avoid placing secrets or sensitive info in templates.
* Consider adding different templates for bug fixes, features, or release changes in a `.github/PULL_REQUEST_TEMPLATE/` folder to help contributors select the right format.

<Callout icon="warning">
  Do not include sensitive data or credentials in PR templates. Templates are visible to all repository contributors and may be copied into PR histories.
</Callout>

Summary

* For a single template, add `pull_request_template.md` to `.github`, `docs`, or the repository root.
* For multiple templates, create a folder inside `.github` (for example, `.github/PULL_REQUEST_TEMPLATE/`) and add each Markdown file.
* Templates standardize PR descriptions, streamline reviews, and help ensure contributors link issues and confirm required checks.

Links and references

* [GitHub: Creating a pull request template](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-issue-and-pull-request-templates)
* [GitHub Docs: Managing PR templates](https://docs.github.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/1231fb21-5b25-4a68-8d38-373808b0ba92/lesson/1df80f62-8cdf-4b35-99a5-5e652b357c0c" />
</CardGroup>
