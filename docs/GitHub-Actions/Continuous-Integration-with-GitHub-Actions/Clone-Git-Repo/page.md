# Clone Git Repo

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/Clone-Git-Repo/page

This article explains how to migrate a GitLab repository to GitHub and set up for CI/CD workflows.

In this lesson, we’ll migrate the Solar System application source code from GitLab to GitHub. Once imported, you can start building GitHub Actions workflows for CI/CD.

## Step 1: Copy the GitLab Repository URL

On GitLab, navigate to the **Solar-System** project and copy its HTTPS clone URL:

<Frame>
  ![The image shows a GitLab repository page for a project named "Solar-System," displaying files, commit history, and project details.](https://kodekloud.com/kk-media/image/upload/v1752876496/notes-assets/images/GitHub-Actions-Clone-Git-Repo/gitlab-repository-solar-system-project.jpg)
</Frame>

## Step 2: Import the Repository into GitHub

1. Go to GitHub’s import interface at `https://github.com/new/import`.
2. Paste the GitLab URL into the **Your old repository’s clone URL** field.
3. Set the **Owner** and enter `solar-system` as the **Repository Name**.
4. Choose **Public** visibility.
5. Click **Begin import**.

<Frame>
  ![The image shows a GitHub interface for importing a project from another version control system, with fields for entering the repository URL and details for the new repository. Options for setting the repository as public or private are also visible.](https://kodekloud.com/kk-media/image/upload/v1752876497/notes-assets/images/GitHub-Actions-Clone-Git-Repo/github-import-project-interface-repo.jpg)
</Frame>

<Callout icon="lightbulb">
  Large repositories may take several minutes to import. You can monitor progress on the same page.
</Callout>

## Step 3: Verify the Imported Files

After the import completes, navigate to your new `solar-system` repository. Confirm that all files—such as `README.md`, `Dockerfile`, and JavaScript source files—have been migrated successfully:

<Frame>
  ![The image shows a GitHub repository page for a project named "solar-system," displaying a list of files and directories along with commit messages and timestamps. The repository includes files like README.md, Dockerfile, and several JavaScript files.](https://kodekloud.com/kk-media/image/upload/v1752876498/notes-assets/images/GitHub-Actions-Clone-Git-Repo/github-repo-solar-system-files.jpg)
</Frame>

## Quick Reference

| Step | Action                          | Location                    |
| ---- | ------------------------------- | --------------------------- |
| 1    | Copy GitLab clone URL           | GitLab project overview     |
| 2    | Import repository via GitHub UI | `github.com/new/import`     |
| 3    | Verify files in new GitHub repo | GitHub repository main page |

## Next Steps

With your code now on GitHub, you can:

* Create a workflow file in `.github/workflows/`
* Define jobs for linting, testing, and building
* Trigger CI/CD on each push or pull request

## Links and References

* [GitHub: Importing a repository](https://docs.github.com/en/repositories/importing-your-projects-to-github/importing-a-repository-with-github-importer)
* [GitLab Documentation](https://docs.gitlab.com/)
* [GitHub Actions Overview](https://docs.github.com/en/actions/learn-github-actions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/6136c7b5-8fe0-4a84-ae77-0274623512d5/lesson/c5badd11-273f-4ca5-a348-126cf202273c" />
</CardGroup>
