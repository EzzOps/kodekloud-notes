# Options for Collaboration in SageMaker Studio

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-User-Interface/Options-for-Collaboration-in-SageMaker-Studio/page

Explains collaboration in SageMaker Studio, comparing EBS/EFS storage limits and advocating using Git inside JupyterLab for versioning, branching, reviews, and reproducible ML workflows.

In this article we cover collaboration patterns inside SageMaker Studio with a focus on managing multiple copies of notebooks and development assets using Git from within the JupyterLab interface. You’ll learn where notebooks are stored, the limits of filesystem-based sharing, and why using Git inside JupyterLab provides a scalable, auditable collaboration workflow for .ipynb, .py and other code assets.

## Problem context: where are notebook files stored?

A JupyterLab space in SageMaker Studio runs on a managed compute “app” (the JupyterLab server). Depending on the Studio configuration the app’s filesystem may be:

* Backed by an EBS volume attached to the compute instance, or
* Mounted from a shared EFS filesystem.

When using an EBS-backed app, saving a notebook writes to that attached EBS volume; when using an EFS-backed Studio, files are persisted on EFS. Neither EBS nor EFS provides line-level version control, branching, or an integrated code review workflow — those features come from Git.

Important characteristics and limitations of EBS:

* EBS volumes are replicated across underlying hardware but are scoped to a single Availability Zone (AZ).
* An AZ is a failure domain within a region; EBS volumes do not cross AZ boundaries.
* EBS is not a version-control system. Saving files to EBS alone does not provide shareable commit history or collaboration primitives.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Collaboration&#x22; that lists limitations of EBS (EBS volumes stay in one AZ, AZ is a failure domain, and ipynb files remain on the shared EBS volume). A diagram shows an EBS volume with a jupyter-notebook.ipynb file next to a SageMaker Domain containing a JupyterLab Space and Server." />
</Frame>

## EFS (Elastic File System) and Studio

Many SageMaker Studio deployments use EFS to provide a persistent home directory shared across app sessions. EFS can simplify sharing a home directory across multiple app sessions and supports snapshots, but it is not a replacement for Git-based versioning.

Key points about EFS in Studio:

* EFS provides shared storage that multiple app sessions can mount.
* Snapshots are not the same as granular commit history: snapshots are coarse-grained and not suited to code review workflows.
* EFS requires NFS mounts and possibly additional configuration in custom deployments.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Collaboration&#x22; that lists three limitations of EFS: requires a custom NFS mount, needs specific infrastructure, and has no version tracking (only snapshots). To the right is a diagram showing an EFS storage icon next to a SageMaker Domain containing a JupyterLab Space and JupyterLab Server." />
</Frame>

## Storage options — quick comparison

| Storage type            | Best use case                                               | Limitations                                                                |
| ----------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------- |
| EBS (instance-attached) | Fast local storage for a single app/session                 | Single AZ; tied to lifecycle of the app; not version control               |
| EFS (shared)            | Persistent home directories shared by multiple apps         | Requires NFS mounts/configuration; snapshots only — no commit history      |
| Git (remote)            | Source control for notebooks, scripts, and workflow configs | Not a file server for large binary datasets — pair with S3 or DVC for data |

## A better approach: Git inside JupyterLab

JupyterLab is extensible, and SageMaker Studio includes the JupyterLab Git extension. Using Git from inside JupyterLab gives you:

* Line-level change tracking (who changed what and when).
* The ability to create commits and push/pull to a central Git server (GitHub, GitLab, Bitbucket, or self-hosted).
* Support for branching, pull requests (code review), and CI/CD integrations.
* Offline local commits that can be pushed when connectivity is available.

Git is a distributed version control system; teams typically maintain a central remote repository and developers clone repositories into their workspaces, commit locally, and push to the central server.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Git Version Control&#x22; listing four key points about Git (tracks changes/enables collaboration, stores code/data/history, works offline with central server, and popular platforms like GitHub/GitLab/BitBucket). To the right is a layered diagram showing a SageMaker Domain containing a JupyterLab Space with a JupyterLab Server and a JupyterLab Git Extension." />
</Frame>

## Terminology and roles

* Git — the version control system and the command-line tool.
* Git servers — hosting providers that implement Git over HTTP/SSH and add collaboration features (e.g., GitHub, GitLab, Bitbucket, or private servers).
* JupyterLab Git extension — the UI layer inside JupyterLab/Studio that lets you clone, stage, commit, push, and pull without leaving the notebook environment.

## Typical workflow using the JupyterLab Git extension

1. Create an empty repository on your Git server or use an existing repo.
2. In JupyterLab, open the Git extension and clone the repository into your workspace (this copies files into your workspace storage — EBS or EFS).
3. Create or edit notebooks and scripts inside the cloned repository.
4. Stage changes, write a commit message, and commit locally.
5. Push commits to the central Git server so teammates can fetch or open pull requests.

Example: cloning a public repo URL (use the Git clone dialog in the UI)

```text theme={null}
https://github.com/kodekloudhub/git-for-beginners-course
```

Common Git commands you will encounter (the JupyterLab Git extension provides UI equivalents for many of these):

| Action                         | Command                                                                   |
| ------------------------------ | ------------------------------------------------------------------------- |
| Stage and commit local changes | git add . && git commit -m "Add notebook cells to send user notification" |
| Push local commits to remote   | git push                                                                  |
| Fetch and merge remote changes | git pull                                                                  |

You can still run these commands in a terminal inside Studio if you prefer the CLI.

## User interface experience in JupyterLab

* The Git icon appears in the left sidebar. If the current directory is not a Git repo, the extension prompts to initialize or clone.
* The clone dialog accepts a repository URL and an optional local target directory; you can also opt to open README.md after cloning.
* After cloning, the file browser shows the repository root and you can open and edit files as normal.
* The Git view shows unstaged/staged changes, lets you write commit messages, and exposes push/pull controls.
* Use branches and the Git extension to create feature branches, switch contexts, and manage PR workflows.

<Frame>
  <img alt="A slide titled &#x22;Solution: Git Version Control&#x22; showing a three-step workflow (create a repo, clone to workspace, commit and push) alongside an architecture diagram of a SageMaker domain with a JupyterLab space, JupyterLab Git extension, and a linked repository/storage holding a jupyter-notebook.ipynb." />
</Frame>

## Why Git works well for notebooks

* Jupyter Notebook files (.ipynb) are JSON text files; Git can diff, track, and merge text files.
* Notebook diffs can be noisy because of cell metadata and output. Use notebook-aware tools to improve diffs and merges:
  * nbdime: a dedicated diff/merge tool for notebooks — [https://nbdime.readthedocs.io](https://nbdime.readthedocs.io)
  * jupytext: pairs notebooks with plain-text representations (e.g., .py), making diffs much cleaner — [https://jupytext.readthedocs.io](https://jupytext.readthedocs.io)
* Git enables reproducibility: by tagging commits or checking out specific commit SHAs, you can reproduce experiments with the exact code used for training or evaluation.
* For large datasets, avoid committing binaries to Git. Store bulk data in Amazon S3 ([https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)) or use a data-versioning system such as DVC ([https://dvc.org](https://dvc.org)) and keep pointers/metadata in Git.

> **lightbulb** Avoid adding large datasets directly into Git repositories. For large input data, use S3 or a data-versioning system (for example, DVC) and keep pointers or metadata in Git.

## Collaboration workflows and quality control

* Use feature branches and pull requests to enable code review and approvals before merging to main branches.
* Commits and push events can be triggers for CI/CD systems and for SageMaker automations such as SageMaker Pipelines ([https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)).
* Enforce policies (branch protection, required reviews) on the Git server to improve code quality and reduce accidental merges.

## Benefits recap

* Better collaboration: track who changed what and when; support code review workflows.
* Reproducible ML experiments: checkout exact commit snapshots for training and evaluation.
* Automation: commits and merges can trigger CI/CD pipelines and SageMaker automation.
* Code quality: pull requests and reviews help catch issues before they reach production.

<Frame>
  <img alt="An infographic titled &#x22;Results: Code Integrity and Improved Productivity&#x22; showing four numbered cards describing benefits: faster collaboration with version control, reproducible ML experiments with rollback, integration with SageMaker Pipelines, and better code quality via Git workflows and reviews. Each benefit is shown as a colored card with a simple line icon." />
</Frame>

## Summary

* SageMaker Studio’s JupyterLab is extensible and includes a Git extension to clone, initialize, commit, and synchronize repositories from the UI.
* Studio workspaces use attached storage (EBS or EFS) depending on configuration; these filesystems are not substitutes for Git-based version control.
* Git is the appropriate tool for line-level versioning of code and JSON-based notebooks; central Git servers add hosting, access control, and collaboration features.
* Combine Git with S3 or data-versioning tools for large datasets, and integrate commits with CI/CD and SageMaker Pipelines for reproducible automation.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; showing four numbered points (05–08) about version control and Jupyter: line-level change tracking, JSON-based notebooks compatible with Git, JupyterLab support for GitHub/GitLab/Bitbucket, and improved collaboration via version control." />
</Frame>

Note: This article focuses on collaboration inside SageMaker Studio. The SageMaker code editor is a separate topic. For further reading, see:

* Git official docs: [https://git-scm.com/doc](https://git-scm.com/doc)
* nbdime: [https://nbdime.readthedocs.io](https://nbdime.readthedocs.io)
* jupytext: [https://jupytext.readthedocs.io](https://jupytext.readthedocs.io)
* DVC: [https://dvc.org](https://dvc.org)
* SageMaker Pipelines: [https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b5e72234-012c-4793-ad8c-e1a7c6d3b8be/lesson/8dc8f29f-ca27-4808-a168-be26206fb428)
