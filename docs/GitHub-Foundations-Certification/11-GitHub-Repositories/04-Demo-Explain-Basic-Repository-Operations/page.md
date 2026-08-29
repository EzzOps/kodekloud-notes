# or
git merge main
```

Best practices summary

* Work on feature branches, not `main`.
* Keep your fork in sync with `upstream`.
* Push branches to your fork and open a pull request for review when ready.

<Callout icon="lightbulb">
  Best practice: Work on feature branches (not `main`), keep your fork in sync with `upstream`, and open a pull request for review when your changes are ready.
</Callout>

Links and references

* GitHub Docs: [https://docs.github.com/](https://docs.github.com/)
* Git documentation: [https://git-scm.com/docs](https://git-scm.com/docs)
* GitHub CLI: [https://cli.github.com/](https://cli.github.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/8933863d-4b81-4c80-90af-2f28f8519020/lesson/47b405ec-c4d4-4cbf-8812-7a8e70957962" />
</CardGroup>


# Demo Explain Basic Repository Operations

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Repositories/Demo-Explain-Basic-Repository-Operations/page

Step by step tutorial for creating, cloning, branching, editing, and pushing changes to a GitHub repository, with authentication tips using personal access tokens

In this lesson we'll walk through creating a GitHub repository in the web UI, adding files, creating a branch, cloning the repo locally, making changes on a feature branch, and pushing those changes back to GitHub. Each image below corresponds to a step in the workflow and is shown in the original sequence so you can follow along visually.

## 1. Create a new repository on GitHub

Open GitHub in your browser and create a new repository. Choose a clear repository name (for example, `block-buster`) and add an optional description describing what the project does. For discoverability choose `Public` if you want anyone to view the repository.

Initialize the repository with a `README.md` (so visitors immediately see project context), add a `.gitignore` (to exclude editor or OS-specific files, e.g., VS Code artifacts), and optionally choose a license.

<Frame>
  <img alt="The image shows a GitHub dashboard with repositories listed on the left and a section promoting a GitHub for Beginners YouTube playlist on the right. There are various options for creating issues, writing code, and managing repositories at the top." />
</Frame>

When filling in repository details, the web UI guides you through the name, description, visibility, and initialization options.

<Frame>
  <img alt="This image shows a GitHub interface for creating a new repository, with fields for the repository name, description, and visibility settings. The visibility option is highlighted, with a choice between &#x22;Public&#x22; and &#x22;Private.&#x22;" />
</Frame>

## 2. Add project files via the web UI (optional)

You can upload your initial project files directly from the GitHub UI: use Add files → Upload files. Common files for a simple web project include `index.html`, `script.js`, and `style.css`. Provide a short commit message (for example, `init`) and commit directly to `main` or create a new branch from the UI.

<Frame>
  <img alt="The image shows a GitHub interface for uploading files to a repository, with fields for file selection and commit messages, and options for committing to a branch or creating a new branch." />
</Frame>

## 3. Create a feature branch in the GitHub UI

Working on a branch keeps `main` stable. From the repository page you can create a feature branch (for example, `feature-1`) and continue development there.

<Frame>
  <img alt="The image shows a GitHub repository page for a project named &#x22;block-buster&#x22; with a menu open to create a new branch named &#x22;feature-1.&#x22; It features information about the project, including its description and commit history." />
</Frame>

## 4. Clone the repository locally

On your machine, clone the repository to work locally. Copy the HTTPS clone URL from the GitHub repository page and run the commands below. This example creates a `~/github-repos` directory and clones `block-buster` into it:

```bash theme={null}
mkdir -p ~/github-repos
cd ~/github-repos
git clone https://github.com/sid-gh900/block-buster.git
cd block-buster
git branch --list
git branch --list -a
```

Example output after cloning:

```bash theme={null}
Cloning into 'block-buster'...
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (9/9), done.
Receiving objects: 100% (9/9), 13.95 KiB | 714.00 KiB/s, done.
Resolving deltas: 100% (1/1), done.
