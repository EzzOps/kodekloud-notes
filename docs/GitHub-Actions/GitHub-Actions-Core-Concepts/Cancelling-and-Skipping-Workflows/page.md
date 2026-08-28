# .github/workflows/deploy.yml
on:
  workflow_dispatch:
jobs:
  deploy:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, ubuntu-20.04, windows-latest]
        images: [hello-world, alpine]
        exclude:
          - os: windows-latest
            images: alpine
    steps:
      - name: Echo Docker Details
        run: docker info
      - name: Run Image on ${{ matrix.os }}
        run: docker run ${{ matrix.images }}
```

With this configuration, GitHub Actions will skip the `windows-latest` + `alpine` job, reducing the total from six to five.

<Callout icon="lightbulb">
  Excluding unsupported combinations helps save build minutes and avoids predictable failures.
</Callout>

## 2. Including Additional Combinations

Use `include` to add custom pairs beyond the default matrix. For instance, to run `amd64/alpine` only on Ubuntu 20.04:

```yaml theme={null}
# .github/workflows/deploy.yml
on:
  workflow_dispatch:
jobs:
  deploy:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, ubuntu-20.04, windows-latest]
        images: [hello-world, alpine]
        exclude:
          - os: windows-latest
            images: alpine
        include:
          - os: ubuntu-20.04
            images: amd64/alpine
    steps:
      - name: Echo Docker Details
        run: docker info
      - name: Run Image on ${{ matrix.os }}
        run: docker run ${{ matrix.images }}
```

This ensures `amd64/alpine` builds only on Ubuntu 20.04, while still excluding Alpine on Windows.

## 3. Controlling Failure Behavior and Parallelism

By default, `fail-fast: true` cancels all remaining jobs if one fails. You can disable this and control concurrency:

```yaml theme={null}
# .github/workflows/deploy.yml
on:
  workflow_dispatch:
jobs:
  deploy:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false       # Continue running all matrix jobs even on failure
      max-parallel: 2        # Limit to 2 concurrent jobs
      matrix:
        os: [ubuntu-latest, ubuntu-20.04, windows-latest]
        images: [hello-world, alpine]
        exclude:
          - os: windows-latest
            images: alpine
        include:
          - os: ubuntu-20.04
            images: amd64/alpine
    steps:
      - name: Echo Docker Details
        run: docker info
      - name: Run Image on ${{ matrix.os }}
        run: docker run ${{ matrix.images }}
```

This setup runs only two jobs at a time. As each finishes, the next queued jobs start.

<Frame>
  ![The image shows a GitHub Actions interface with a matrix configuration for deploying various environments, including Ubuntu and Windows. The workflow is queued, and different deployment jobs are listed with their statuses.](https://kodekloud.com/kk-media/image/upload/v1752876617/notes-assets/images/GitHub-Actions-Additional-Matrix-Configuration/github-actions-matrix-deployment-interface.jpg)
</Frame>

Notice Alpine is excluded on Windows, and `amd64/alpine` is included only on Ubuntu 20.04:

<Frame>
  ![The image shows a GitHub Actions workflow interface with a matrix configuration for deployment jobs, indicating various operating systems and environments being tested. The workflow is currently in progress.](https://kodekloud.com/kk-media/image/upload/v1752876618/notes-assets/images/GitHub-Actions-Additional-Matrix-Configuration/github-actions-workflow-matrix-deployment.jpg)
</Frame>

## Matrix Strategy Options at a Glance

| Option       | Description                                                                 |
| ------------ | --------------------------------------------------------------------------- |
| matrix       | Defines axes (e.g., OS, images) to combine                                  |
| exclude      | Omits specific combinations                                                 |
| include      | Adds custom combinations beyond the default                                 |
| fail-fast    | `true` (default) cancels on first failure; `false` runs all jobs regardless |
| max-parallel | Limits how many matrix jobs run concurrently                                |

## References

* [GitHub Actions Matrix Documentation](https://docs.github.com/en/actions/using-jobs/using-a-matrix)
* [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/0ac6c98f-7100-471e-b9aa-037f25cb58d7/lesson/6d55fd41-0fdc-44a6-b9f5-0d7bd313f09c" />
</CardGroup>


# Cancelling and Skipping Workflows

Source: https://notes.kodekloud.com/docs/GitHub-Actions/GitHub-Actions-Core-Concepts/Cancelling-and-Skipping-Workflows/page

Learn to optimize CI pipelines by skipping unnecessary GitHub Actions runs and cancelling in-progress jobs.

Optimize your continuous integration (CI) pipeline by learning how to prevent unnecessary GitHub Actions runs and how to stop jobs that are already in progress. This guide covers:

* How to skip workflows using commit-message directives
* How to cancel an in-progress workflow from the GitHub UI

***

## Skipping Workflow Runs via Commit Messages

By including specific keywords in your commit messages, you can tell GitHub Actions to bypass workflow triggers for `push` and `pull_request` events. This is particularly useful when making non-code changes like documentation updates.

<Callout icon="lightbulb">
  The directives below are case-insensitive and must appear anywhere in your **commit message**.
</Callout>

| Directive           | Behavior                                           |
| ------------------- | -------------------------------------------------- |
| `skip ci`           | Skip all workflow runs for this commit             |
| `ci skip`           | Alias for `skip ci`                                |
| `no ci`             | Skip all workflow runs for this commit             |
| `skip-checks: true` | Add after two blank lines at end of commit message |

<Frame>
  ![The image shows a GitHub documentation page about skipping workflow runs, explaining how to prevent workflows from triggering by using specific commands in commit messages.](https://kodekloud.com/kk-media/image/upload/v1752876620/notes-assets/images/GitHub-Actions-Cancelling-and-Skipping-Workflows/github-skipping-workflow-runs-documentation.jpg)
</Frame>

<Callout icon="triangle-alert">
  Skipping CI can hide build failures. Use these directives only for trivial changes (e.g., spelling fixes, docs).
</Callout>

***

## Example: Skipping Workflows for Documentation Changes

When you update files like `README.md`, you often don’t need to rebuild or redeploy your application. Here’s how to skip CI for pure documentation commits:

<Frame>
  ![The image shows a Visual Studio Code interface with a README.md file open, displaying text about exploring GitHub Actions. The file explorer on the left lists several YAML and script files.](https://kodekloud.com/kk-media/image/upload/v1752876621/notes-assets/images/GitHub-Actions-Cancelling-and-Skipping-Workflows/vscode-readme-github-actions-file-explorer.jpg)
</Frame>

1. Edit your documentation file:
   ```bash theme={null}
   git add README.md
   git commit -m "Refresh markdown formatting [ci skip]"
   ```
2. Push the commit:
   ```bash theme={null}
   git push origin main
   ```
3. Confirm no workflows ran by checking the **Actions** tab in your repository.

***

## Cancelling an In-Progress Workflow

If you realize a running workflow is no longer needed—perhaps it was triggered by mistake or contains a broken job—you can cancel it in just a few clicks:

1. Go to the **Actions** tab in your GitHub repository.
2. Click the workflow run that’s currently in progress.
3. Hit **Cancel workflow** in the upper-right corner of the run details page.

Your job will be immediately terminated, freeing up your runner capacity.

***

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/en/actions)
* [Commit Message Guidelines](https://www.conventionalcommits.org/)
* [GitHub Actions: Skipping Workflows](https://docs.github.com/en/actions/learn-github-actions/avoiding-frequent-workflow-runs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/0ac6c98f-7100-471e-b9aa-037f25cb58d7/lesson/815bd28b-c2d7-4f39-b8e5-2fc0420446ac" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/github-actions/module/0ac6c98f-7100-471e-b9aa-037f25cb58d7/lesson/aa1efd6b-0a53-4116-88a7-d3ca5705fa35" />
</CardGroup>
