# (job will remain active)
```

### 3.4 After Job Initialization

Re-execute the tree command:

```bash theme={null}
root@ubuntu-host:~/actions-runner$ tree _work/
_work/
├── actions-1
│   ├── actions-1
│   ├── PipelineMapping
│   │   └── your-org-demo-1
│   │       └── actions-1
│   │           └── PipelineFolder.json
└── _temp
    ├── 06abcca7-d09b-406e-ba2e-f87e625ac8db.sh
    ├── _github_workflow/event.json
    └── runner_file_commands
        ├── add_path_*.txt
        ├── save_state_*.txt
        ├── set_env_*.txt
        ├── set_output_*.txt
        └── step_summary_*.txt

9 directories, 8 files
```

#### 3.4.1 PipelineFolder.json

Metadata about your repo and workspace:

```json theme={null}
{
  "repositoryName": "your-org/demo-repo",
  "workspaceDirectory": "actions-1/actions-1",
  "lastRunOn": "2023-10-24T15:34:10Z",
  "repositories": {
    "your-org/demo-repo": {
      "repositoryPath": "actions-1/actions-1",
      "lastRunOn": "2023-10-24T15:23:59Z"
    }
  }
}
```

#### 3.4.2 Generated Shell Script

Your `run:` commands are translated into a shell script:

```bash theme={null}
root@ubuntu-host:~/actions-runner$ cat _work/_temp/06abcca7-d09b-406e-ba2e-f87e625ac8db.sh
echo "Runner is active"
sleep 1500s
```

#### 3.4.3 Workflow Event Payload

The full event that triggered the job lives in `event.json`:

```json theme={null}
{
  "inputs": null,
  "ref": "refs/heads/main",
  "repository": {
    "clone_url": "https://github.com/your-org/demo-repo.git",
    "default_branch": "main",
    ...
  }
}
```

#### 3.4.4 Runner File Commands

Commands such as `::set-env` and `::add-path` are materialized into files under `runner_file_commands`. The runner engine reads these to adjust environment variables, outputs, and step summaries.

***

## 4. Real-Time Diagnostics

While the job is running, new logs continuously populate `_diag`:

```bash theme={null}
root@ubuntu-host:~/actions-runner$ tree _diag/
_diag/
├── blocks
│   ├── ..._1.log
│   └── ..._2.log
└── pages
    ├── ..._1.log
    └── ..._2.log
```

Live snippet from a worker log:

```text theme={null}
[2023-10-24 15:34:11Z INFO ProcessInvokerWrapper] Starting process:
[2023-10-24 15:34:11Z INFO ProcessInvokerWrapper] File name: '/usr/bin/bash'
[2023-10-24 15:34:11Z INFO ProcessInvokerWrapper] Arguments: '-e /root/actions-runner/_work/_temp/06abcca7-d09b-406e-ba2e-f87e625ac8db.sh'
[2023-10-24 15:35:11Z INFO JobServerQueue] Stop aggressive web console lines queue.
```

***

## 5. Cleanup

When you’ve finished inspecting logs and workspace files, stop the runner:

```bash theme={null}
# In the runner terminal:
^C
Stopping runner...
```

This terminates the current job and shuts down the service.

***

## 6. Summary

* **`_diag/`**: Central location for runner and worker diagnostics.
* **`_work/`**: Contains your repo checkout, generated scripts, event payloads, and runner file commands.
* Monitoring these folders in real time is essential for debugging connectivity, authentication, and workflow execution on self-hosted runners.

***

## Links and References

* [GitHub Actions: Self-hosted runners](https://docs.github.com/actions/hosting-your-own-runners/about-self-hosted-runners)
* [Workflow syntax for GitHub Actions](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
* [Viewing runner diagnostic logs](https://docs.github.com/actions/monitoring-and-troubleshooting-workflows/managing-workflow-runner-logs)

Dry-run these steps to gain confidence in troubleshooting and customizing your self-hosted GitHub Actions runners.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/7cc7bcee-0af6-41af-9653-dfd6e0403fe9/lesson/b2bb21f7-ac54-45af-8d41-f8b7a03a9c53)


# Installing a Self Hosted Runner

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Self-Hosted-Runner/Installing-a-Self-Hosted-Runner/page

This guide explains how to install and configure a self-hosted runner for GitHub Actions at the repository level.

In this guide, you’ll learn how to install and configure a self-hosted runner at the repository level. You can also set up runners at the organization or enterprise level—see the [GitHub documentation](https://docs.github.com/actions/hosting-your-own-runners) for autoscaling, requirements, and limits.

## Step 1: Register a New Runner on GitHub

1. Open your repository on GitHub.
2. Navigate to **Settings** → **Actions** → **Runners**.
3. Click **New self-hosted runner**.
4. Select **Linux** and **x64**, then copy the setup commands provided.

## Step 2: Download and Extract the Runner

SSH into your Ubuntu VM (or another Linux host), then run:

```bash theme={null}
