# 1. Create and enter a directory for the runner
mkdir actions-runner && cd actions-runner

# 2. Download the latest runner package
curl -o actions-runner-linux-x64-2.310.2.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.310.2/actions-runner-linux-x64-2.310.2.tar.gz

# 3. (Optional) Verify checksum
echo "fb23a1c715ea0c501fa60beefcf295e26cfbbf849f3  actions-runner-linux-x64-2.310.2.tar.gz" \
  | sha256sum --check

# 4. Unpack the archive
tar xzf ./actions-runner-linux-x64-2.310.2.tar.gz
```

<Callout icon="lightbulb">
  Ensure your VM meets the [runner requirements](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners#self-hosted-runner-requirements): at least 2 CPU cores, 8 GB RAM, and Docker if you plan on containerized jobs.
</Callout>

After extraction, verify the scripts:

```bash theme={null}
ls
# bin  config.sh  env.sh  externals  run-helper.cmd.template \
# run-helper.sh.template  run.sh  safe_sleep.sh
```

## 3. Configure the Runner

Use the registration token provided in the GitHub UI:

```bash theme={null}
./config.sh --url https://github.com/your-username/your-repo \
  --token YOUR_TOKEN_HERE
```

<Callout icon="triangle-alert">
  By default, running the runner as root is disabled for security. To override (at your own risk), export:

  ```bash theme={null}
  export RUNNER_ALLOW_RUNASROOT=1
  ```
</Callout>

Follow the interactive prompts:

```text theme={null}
GitHub Actions self-hosted runner registration
✓ Connected to GitHub
Enter the name of runner group: [Default]
Enter name of runner: [press Enter for ubuntu-host] prod-ubuntu-runner
Labels: self-hosted, Linux, X64
Enter additional labels (comma-separated): [skip]
✓ Runner successfully added
✓ Runner connection is good
Enter work folder name: [press Enter for _work]
```

## 4. Verify the Runner in GitHub

Return to **Settings** → **Actions** → **Runners** and refresh. You should see `prod-ubuntu-runner` listed (initially offline):

<Frame>
  ![The image shows a GitHub Actions runner configuration page for a "prod-ubuntu-runner" with no active jobs running. It displays labels such as "self-hosted," "Linux," and "X64."](https://kodekloud.com/kk-media/image/upload/v1752876771/notes-assets/images/GitHub-Actions-Installing-a-Self-Hosted-Runner/github-actions-prod-ubuntu-runner.jpg)
</Frame>

## 5. Start the Runner

Launch the runner process:

```bash theme={null}
./run.sh
```

Sample output:

```bash theme={null}
Current runner version: '2.310.2'
2023-10-24 14:51:44Z: Listening for Jobs
```

After a moment, refresh the GitHub **Runners** page—it should display **online** and **idle**, ready to accept jobs.

***

## Links and References

* [GitHub Actions Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners/using-self-hosted-runners)
* [GitHub Actions Runner Releases](https://github.com/actions/runner/releases)
* [Runner Requirements](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners#self-hosted-runner-requirements)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/8d91a711-49f5-449c-9531-393bfdc7d9b5/lesson/f617a099-2b54-45ea-b90d-e0026762441c" />
</CardGroup>


# Running Workflow on Self Hosted Runner

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Self-Hosted-Runner/Running-Workflow-on-Self-Hosted-Runner/page

Execute GitHub Actions workflows on your infrastructure using a self-hosted runner with this comprehensive guide.

Leverage a self-hosted runner to execute your GitHub Actions workflows on your own infrastructure. This guide walks you through verifying the runner in the GitHub UI, starting it on the VM, creating a test workflow, targeting the self-hosted runner, dispatching the job, and reviewing the results.

***

## 1. Verify Your Self-Hosted Runner in GitHub

1. In your repository, navigate to **Settings > Actions > Runners**.
2. Confirm the runner (e.g., `prod-ubuntu-runner`) appears in an **idle** state with its labels listed.

<Frame>
  ![The image shows a GitHub settings page for actions, specifically the "Runners" section, displaying a self-hosted runner named "prod-ubuntu-runner" with an idle status.](https://kodekloud.com/kk-media/image/upload/v1752876772/notes-assets/images/GitHub-Actions-Running-Workflow-on-Self-Hosted-Runner/github-actions-runners-prod-ubuntu.jpg)
</Frame>

***

## 2. Start the Runner Process

On the VM hosting your runner, launch the runner service:

```bash theme={null}
cd ~/actions-runner
sudo ./run.sh
```

You should see:

```plaintext theme={null}
Current runner version: '2.310.2'
2023-10-24 14:51:44Z: Listening for Jobs
```

<Callout icon="lightbulb">
  If you don’t see “Listening for Jobs,” verify your network connectivity and runner configuration.\
  Refer to the [GitHub Actions Runners documentation][runners-docs] for troubleshooting.
</Callout>

***

## 3. Inspect Available Workflows

Because this runner is scoped to the current repository, only workflows in `.github/workflows` are dispatched here. Check the YAML files:

<Frame>
  ![The image shows a GitHub repository interface displaying a list of YAML workflow files under the .github/workflows directory, with details about their last commit messages and times.](https://kodekloud.com/kk-media/image/upload/v1752876774/notes-assets/images/GitHub-Actions-Running-Workflow-on-Self-Hosted-Runner/github-repo-yaml-workflows-list.jpg)
</Frame>

***

## 4. Define a Simple Test Workflow

Create `.github/workflows/example.yaml`:

```yaml theme={null}
name: Test Self-Hosted Runner
on:
  workflow_dispatch:

jobs:
  test-job:
    runs-on: ubuntu-latest
    steps:
      - name: Echo and Sleep
        run: |
          echo "Runner check: OK"
          sleep 15s
```

Commit this to the default branch to verify it runs on GitHub-hosted runners first.

***

## 5. Target Your Self-Hosted Runner

Update `runs-on` to use all labels from the **Runners** settings (e.g., `self-hosted`, `linux`, `prod`):

```yaml theme={null}
name: Test Self-Hosted Runner
on:
  workflow_dispatch:

jobs:
  test-job:
    runs-on: [self-hosted, linux, prod]
    steps:
      - name: Echo and Sleep
        run: |
          echo "Self-hosted runner: OK"
          sleep 15s
```

All labels must match exactly.

<Callout icon="triangle-alert">
  Any typo or missing label (for example, using `production` instead of `prod`) will cause the job to remain pending until it times out.
</Callout>

Commit your changes directly to the `main` branch:

<Frame>
  ![The image shows a GitHub interface with a "Commit changes" dialog box open, where a commit message is being entered. The background displays a repository with YAML workflow files.](https://kodekloud.com/kk-media/image/upload/v1752876775/notes-assets/images/GitHub-Actions-Running-Workflow-on-Self-Hosted-Runner/github-commit-changes-dialog-repository.jpg)
</Frame>

***

## 6. Dispatch the Workflow Manually

1. Go to the **Actions** tab.
2. Select **Test Self-Hosted Runner**.
3. Click **Run workflow** and choose the branch.

The job enters the self-hosted queue, then starts:

<Frame>
  ![The image shows a GitHub Actions interface displaying a list of workflow runs with their statuses, branches, and timestamps. The sidebar includes options for different workflows and management tools like caches and runners.](https://kodekloud.com/kk-media/image/upload/v1752876776/notes-assets/images/GitHub-Actions-Running-Workflow-on-Self-Hosted-Runner/github-actions-workflow-runs-interface.jpg)
</Frame>

***

## 7. Review Logs and Runner Output

Once the run completes:

* In GitHub, click the run to see **Setup job** details, including:
  * Runner name (`prod-ubuntu-runner`)
  * Runner group (`default`)
  * Host machine name (`ubuntu-host`)
* On the VM, the runner console confirms success:

```plaintext theme={null}
root@ubuntu-host ~/actions-runner ➜ ./run.sh
Job test-job completed with result: Succeeded
```

<Frame>
  ![The image shows a GitHub Actions interface with a successful job run for "Testing Self-Hosted Runner," displaying job details and logs.](https://kodekloud.com/kk-media/image/upload/v1752876777/notes-assets/images/GitHub-Actions-Running-Workflow-on-Self-Hosted-Runner/github-actions-successful-job-testing-runner.jpg)
</Frame>

***

## 8. Key Takeaways

| Label       | Purpose                                  |
| ----------- | ---------------------------------------- |
| self-hosted | Routes the job to any self-hosted runner |
| linux       | Targets Linux-based runners              |
| prod        | Custom label for production environment  |

* Always list **all** runner labels in `runs-on`.
* Jobs with mismatched labels remain **pending**.
* Multiple jobs can run in parallel if matching runners are available.

***

## Links and References

* [GitHub Actions Runners documentation][runners-docs]
* [Workflow syntax for GitHub Actions][workflow-syntax]
* [GitHub Actions Overview](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)

[runners-docs]: https://docs.github.com/en/actions/hosting-your-own-runners

[workflow-syntax]: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/8d91a711-49f5-449c-9531-393bfdc7d9b5/lesson/96d064c2-6736-47cc-aa45-c3e40f661837" />
</CardGroup>
