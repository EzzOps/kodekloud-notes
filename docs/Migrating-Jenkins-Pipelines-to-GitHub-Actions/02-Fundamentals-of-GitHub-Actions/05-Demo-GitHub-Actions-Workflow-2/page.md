# This is a basic workflow to help you get started with Actions
name: CI

# Controls when the workflow will run
on:
  # Triggers the workflow on push or pull request events (example)
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

# Allows manual runs from the Actions tab
workflow_dispatch:

jobs:
  # A single job called "build"
  build:
    runs-on: ubuntu-latest

    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v4

      # Example steps
      - name: Run a one-line script
        run: echo Hello, world!
```

You can simplify the triggers and rename the job. This example triggers on any push and allows manual runs:

```yaml theme={null}
name: CI

on:
  push:
  workflow_dispatch:

jobs:
  first_job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Welcome Message
        run: echo "My first GitHub Action Job"

      - name: List files on repo
        run: ls

      - name: Read README
        run: cat README.md
```

A common mistake is omitting the checkout step. If you comment out or remove `actions/checkout`, the runner will not have your repository files by default — `ls` will show an empty workspace and `cat README.md` will fail.

When a workflow runs, GitHub prints runner setup information (OS, image versions, and a long list of preinstalled tools). You can review the hosted runner images and available tools in the documentation.

<Frame>
  <img alt="A GitHub repository page showing the Ubuntu2404-Readme.md file in a dark theme, listing installed languages (Node.js, Python, Ruby, etc.) and package management tools with a file tree in the left sidebar." />
</Frame>

If you remove checkout and push the workflow, the run will fail during the file-read step. Example failing run summary:

```text theme={null}
demo.yml
on: push

first_job
Process completed with exit code 1.
```

A failed "Read File" step appears like this in the Actions UI:

<Frame>
  <img alt="A GitHub Actions run page (dark theme) showing a failed workflow &#x22;Update README.md #2&#x22; for the repo, with the job &#x22;first_job&#x22; and a failed &#x22;Read File&#x22; step. Other steps like &#x22;Set up job&#x22; and &#x22;Welcome Message&#x22; are shown as completed." />
</Frame>

Example job log when the repository wasn't checked out:

```text theme={null}
Run echo "My first GitHub Action Job"
My first GitHub Action Job

Run ls
ls
shell: /usr/bin/bash -e {0}

Run cat README.md
cat: README.md: No such file or directory
Error: Process completed with exit code 1.
```

Why did this happen? By default the runner's workspace does not include your repository files. To make your repository available to the job, include the checkout action: `actions/checkout@v4`.

Key differences in workflow syntax:

| Keyword | Use case                                                   | Example                                              |
| ------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| `uses:` | Run a prebuilt action from the Marketplace or a repository | `actions/checkout@v4`, `docker/build-push-action@v6` |
| `run:`  | Execute inline shell commands on the runner                | `echo`, `ls`, `cat`, `npm`                           |

> **lightbulb** Always include `- uses: actions/checkout@v4` (or the appropriate version) as the first step if your job needs repository files. Note: hidden files (like `.github`) won't appear with `ls` unless you run `ls -a`.

After adding (or uncommenting) the checkout step and rerunning the workflow, the job has access to repository files and `cat README.md` will succeed. Here is the final example workflow:

```yaml theme={null}
name: CI

on:
  push:
  workflow_dispatch:

jobs:
  first_job:
    runs-on: ubuntu-latest
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v4

      - name: Welcome Message
        run: echo "My first GitHub Action Job"

      - name: List files on repo
        run: ls

      - name: Read README
        run: cat README.md
```

When the workflow runs successfully you'll see the checkout step complete, `ls` listing `README.md`, and the README content printed in the logs:

```text theme={null}
Run ls
README.md

Run cat README.md
# Exploring Actions
We will be learning GitHub Actions,
- a robust automation tool that empowers you to streamline repetitive tasks
- how to automate your software development workflows
- techniques to enhance productivity and code quality
```

Marketplace and useful community actions

* Browse the GitHub Marketplace for pre-built actions: [https://github.com/marketplace](https://github.com/marketplace)
* Each action repository documents inputs, outputs, and examples.

Example: a Docker build-and-push job using popular Marketplace actions:

```yaml theme={null}
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
```

You can also manually trigger workflows from the Actions tab (Run workflow) or rely on triggers such as pushes and pull requests. The basic flow is:

1. Define triggers in your workflow YAML.
2. Run jobs on runners (hosted or self-hosted).
3. Use `actions/checkout` to access repository files.
4. Combine Marketplace `uses` actions with `run` shell steps to build, test, and deploy.

> **warning** If your job needs repository content, do not forget `actions/checkout`. Missing this step is the most common cause of "No such file or directory" errors when reading files in Actions.

That's the basics of creating and troubleshooting your first GitHub Actions workflow. For deeper reference and runner images, see:

* GitHub Actions documentation: [https://docs.github.com/en/actions](https://docs.github.com/en/actions)
* About GitHub-hosted runners: [https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/7d6172e9-5a43-4701-9feb-e4cfdb65b256/lesson/81c93a39-28b3-4d89-9ef5-612fc4e584e5)


# Demo GitHub Actions Workflow 2

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Fundamentals-of-GitHub-Actions/Demo-GitHub-Actions-Workflow-2/page

Explains GitHub Actions workflow features including manual triggers, uploading and downloading artifacts to share files between jobs, ordering jobs with needs, and skipping CI on push

In this lesson we expand a simple GitHub Actions workflow to demonstrate:

* manual triggers (`workflow_dispatch`),
* transferring files between jobs using artifacts,
* avoiding race conditions by ordering jobs with `needs`,
* and how to skip CI when pushing changes.

This guide walks through the workflow step-by-step with practical YAML examples and troubleshooting tips.

## 1. Initial demo workflow (manual trigger)

This workflow, named `Demo-2`, runs only when manually triggered from the Actions tab (`workflow_dispatch`). It contains a single `build` job that creates `hello.txt`:

```yaml theme={null}
name: Demo-2

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Create a text file
        run: echo "Hello, world!" > hello.txt
```

After committing and pushing this file you must manually trigger it from the Actions tab because it does not run on `push` or other events.

## 2. Understanding existing CI workflows and skipping CI on push

If your repository already has another workflow that triggers on `push`, pushing commits can inadvertently trigger that existing workflow. To avoid triggering push-based workflows while you push changes, include `[skip CI]` or `[ci skip]` in your commit message.

> **lightbulb** Include `[skip CI]` (or `[ci skip]`) in the commit message to prevent workflows that trigger on `push` from running for that commit.

A common CI workflow configuration that supports both `push` and manual dispatch looks like this:

```yaml theme={null}
name: CI

on:
  push:
  workflow_dispatch:

jobs:
  first_job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Welcome Message
        run: echo "My first GitHub Action Job"
      - name: List files on repo
        run: ls
      - name: Read File
        run: cat README.md
```

## 3. Adding a second job (and the inter-job file-sharing problem)

Next, we add a `test` job that expects to read `hello.txt` created by the `build` job:

```yaml theme={null}
name: Demo-2

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Create a text file
        run: echo "Hello, world!" > hello.txt

  test:
    runs-on: ubuntu-latest
    steps:
      - name: List files
        run: ls
      - name: Test file
        run: cat hello.txt | grep -i "Hello, world!"
```

Because each job runs on its own runner (a separate virtual machine), files produced in one job are not automatically available in another. The `test` job will typically fail with:

```text theme={null}
cat: hello.txt: No such file or directory
Error: Process completed with exit code 1.
```

## 4. Use artifacts to transfer files between jobs

To share files between jobs, use `actions/upload-artifact` in the producing job and `actions/download-artifact` in the consuming job. These actions are available in the [GitHub Marketplace](https://github.com/marketplace?type=actions\&q=artifact) (search for "artifact").

<Frame>
  <img alt="A screenshot of the GitHub Marketplace in dark mode showing search results for &#x22;artifact&#x22; under Actions, with action cards like Cache, Upload a Build Artifact, and Download a Build Artifact. The page header reads &#x22;Enhance your workflow with extensions&#x22; and includes a prominent search box." />
</Frame>

Example: upload the file in `build` and download it in `test`:

```yaml theme={null}
name: Demo-2

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Create a text file
        run: echo "Hello, world!" > hello.txt
      - uses: actions/upload-artifact@v4
        with:
          name: hello-file
          path: hello.txt

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: hello-file
      - name: List files
        run: ls
      - name: Test file
        run: grep -i "Hello, world!" hello.txt
```

Notes:

* `actions/upload-artifact@v4` creates a named artifact (`hello-file`) that persists for the run.
* `actions/download-artifact@v4` finds that artifact by name and restores the file(s) into the runner workspace.

## 5. Race condition when jobs run in parallel

By default, jobs that have no explicit dependency may run in parallel. If `test` starts before `build` has finished uploading the artifact, the download will fail with an artifact-not-found error:

```text theme={null}
Run actions/download-artifact@v4
Downloading single artifact
Error: Unable to download artifact(s): Artifact not found for name: hello-file
Please ensure that your artifact is not expired and the artifact was uploaded using a compatible version of toolkit/upload-artifact.
```

This failure usually happens because the `test` job started before `build` finished:

<Frame>
  <img alt="A dark-mode GitHub Actions run details page for a workflow named &#x22;Demo-2 #3&#x22; showing the overall run marked Failure. The build job passed but the test job failed with an artifact-not-found error." />
</Frame>

## 6. Make one job depend on another with needs

To ensure `test` runs only after `build` completes, add the `needs` keyword to the `test` job:

```yaml theme={null}
name: Demo-2

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Create a text file
        run: echo "Hello, world!" > hello.txt
      - uses: actions/upload-artifact@v4
        with:
          name: hello-file
          path: hello.txt

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: hello-file
      - name: List files
        run: ls
      - name: Test file
        run: grep -i "Hello, world!" hello.txt
```

* `needs: build` guarantees `test` will not start until `build` has completed (and the artifact is uploaded).
* `needs` accepts an array when a job depends on multiple jobs, for example: `needs: [build, job-xyz]`.
* If you specify a non-existent job in `needs`, the workflow will fail to parse or run.

> **warning** Do not reference job names that don't exist in `needs` (for example: `needs: [build, job-xyz]` where `job-xyz` is not defined). That causes the workflow to fail to parse or execute.

## 7. Successful artifact download logs (example)

When `test` runs after `build` finishes, the `download-artifact` step will find and download the artifact. Example logs show the download flow and the restored file:

```text theme={null}
Run actions/download-artifact@v4
Downloading single artifact
Preparing to download the following artifacts:
- hello-file (ID: 3167026637, Size: 148, Expected Digest: sha256:...)
Redirecting to blob download url: https://...
Starting download of artifact to: /home/runner/work/repo/repo
SHA256 digest of downloaded artifact is ...
Artifact download completed successfully.
Total of 1 artifact(s) downloaded
Download artifact has finished successfully

Run ls
hello.txt
```

## Summary and quick reference

* Jobs run on separate runners and do not share the filesystem by default.
* Use `actions/upload-artifact@v4` to upload files from a job.
* Use `actions/download-artifact@v4` to download artifacts in subsequent jobs.
* Use `needs` to serialize jobs so a job waits for one or more other jobs to finish.
* Use `[skip CI]` or `[ci skip]` in commit messages to avoid triggering push-based workflows.

Quick reference table:

| Feature           | Purpose                               | Example                                     |
| ----------------- | ------------------------------------- | ------------------------------------------- |
| Manual trigger    | Run workflow from Actions UI          | `on: workflow_dispatch`                     |
| Upload artifact   | Persist files from a job              | `uses: actions/upload-artifact@v4`          |
| Download artifact | Restore files in another job          | `uses: actions/download-artifact@v4`        |
| Job dependency    | Ensure job order                      | `needs: build` or `needs: [build, job-xyz]` |
| Skip CI on push   | Prevent `push` workflows from running | include `[skip CI]` in commit message       |

## Links and references

* [GitHub Actions: upload-artifact action (marketplace)](https://github.com/marketplace/actions/upload-a-build-artifact)
* [GitHub Actions: download-artifact action (marketplace)](https://github.com/marketplace/actions/download-a-build-artifact)
* [GitHub Actions documentation — workflow syntax for GitHub Actions](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
* [GitHub Marketplace (search: artifact)](https://github.com/marketplace?type=actions\&q=artifact)

That covers uploading/downloading artifacts between jobs and controlling job order using `needs`.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/7d6172e9-5a43-4701-9feb-e4cfdb65b256/lesson/6ed2faac-6e72-4472-ae10-22607c581542)
