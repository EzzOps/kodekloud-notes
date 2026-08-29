# Demo Describe Repository Templates

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Repositories/Demo-Describe-Repository-Templates/page

Describes GitHub repository templates, how to enable and use them to create new repositories, and key differences compared to forking.

In this lesson we explain GitHub repository templates: what they are, how they differ from forks, and how to mark a repository as a template and create a new repository from it.

Repository templates let you generate a new repository that copies the directory structure and files of the template repository without copying its commit history (unless you explicitly include branches). Templates are ideal for starter kits, examples, classroom assignments, and boilerplate projects where you want contributors to begin from a clean snapshot rather than inheriting an unrelated commit history.

<Callout icon="lightbulb">
  Use repository templates to provide a clean starting point for new projects (e.g., starter kits, examples, or classroom assignments). Use forks when you need to continue work on a project while keeping the full history and a link to the upstream repository.
</Callout>

## Fork vs Template — Key Differences

Below is a concise comparison of forks and repositories created from templates so you can choose the right workflow for your project.

| Aspect                       | Fork                                                                         | Repository created from a template                                                               |
| ---------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Commit history               | Includes the entire commit history of the parent repository.                 | Starts with a single commit containing the template's files (unless you include other branches). |
| Contribution graph           | Commits generally do not appear on your GitHub contribution graph.           | Commits do appear on your GitHub contribution graph.                                             |
| Branch selection at creation | Not applicable — fork is an exact copy of all branches.                      | You can choose to include only the default branch or include all branches from the template.     |
| Typical use cases            | Continued development of an existing project, contributing back to upstream. | Creating new projects from standardized starter code or examples.                                |

For authoritative guidance see the GitHub documentation: [https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)

## Create a repository from a template using the GitHub CLI

You can also generate a new repository from a template with the GitHub CLI. Example:

```bash theme={null}
gh repo create my-new-repo --template owner/template-repo
```

This command creates `my-new-repo` using the repository `owner/template-repo` as the template source.

Now let's walk through marking an existing repository as a template and creating a new repo from it.

I’ll open the Block Buster repository in GitHub (this repository contains files such as `.gitignore`, `README.md`, `index.html`, `script.js`, and `style.css`).

<Frame>
  <img alt="This image shows a GitHub repository named &#x22;block-buster&#x22; with several files like .gitignore, README.md, index.html, script.js, and style.css. The repository is described as an enhanced version of the Block Buster Brick Breaker game with advanced features." />
</Frame>

To make the repository a template, open the repository Settings and enable the “Template repository” option. Toggle it on to allow others to use the repository as a template.

<Frame>
  <img alt="The image shows the settings page of a GitHub repository where options for general settings, default branch, releases, and social preview are displayed. The repository is named &#x22;block-buster,&#x22; and the &#x22;Template repository&#x22; option is highlighted." />
</Frame>

After enabling the template option, return to the repository's Code view. You’ll notice a “Use this template” button in the UI. Clicking that starts the process for creating a new repository based on the template. In the new-repository dialog you can set:

* Owner (your account or an organization)
* Repository name
* Description
* Visibility (public or private)
* Whether to include all branches from the template or only the default branch

<Frame>
  <img alt="The image shows a GitHub interface for creating a new repository, with options for using a template, setting the owner, repository name, description, and visibility." />
</Frame>

<Callout icon="warning">
  If you choose “only the default branch,” the new repository will start with a single commit (a snapshot of that branch). If you choose to include all branches, those branches (and their histories) will be copied into the new repository. Be intentional when including branches to avoid importing unwanted history.
</Callout>

A few important details about the resulting repository:

* Choosing only the default branch creates a new repository with the template files and a single initial commit that represents the snapshot.
* Choosing to include all branches will copy the selected branches into the new repository.
* The new repository’s commit history is independent of the template (unless you include branches with history explicitly). It will not automatically contain the original repository’s full commit history unless those branches are included.

## When to use templates vs forks (quick guidance)

* Use a repository template when you want to give users a starting point without exposing or carrying over the original commit history. Ideal for templates, examples, and classroom assignments.
* Use a fork to create a linked copy when you intend to continue development, retain full history, and contribute changes back to the upstream project.

## Links and References

* GitHub Docs — Create a repository from a template: [https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
* GitHub CLI docs — `gh repo create`: [https://cli.github.com/manual/gh\_repo\_create](https://cli.github.com/manual/gh_repo_create)

That’s how you mark a repository as a template and create a new repository from it. Templates help maintain consistent, clean starting points for new projects, while forks are better when you need continuity with the original repository’s history.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/8933863d-4b81-4c80-90af-2f28f8519020/lesson/9b5b2109-6821-43c7-a468-9511eeb7824b" />
</CardGroup>
