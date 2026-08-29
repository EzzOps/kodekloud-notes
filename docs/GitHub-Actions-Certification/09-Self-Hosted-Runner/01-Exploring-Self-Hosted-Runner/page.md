# Exploring Self Hosted Runner

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Self-Hosted-Runner/Exploring-Self-Hosted-Runner/page

This guide explores key directories of a self-hosted GitHub Actions runner, focusing on diagnostics and workflow workspaces.

In this guide, we’ll dive into the key directories of a self-hosted GitHub Actions runner. You’ll learn how to inspect diagnostics in `_diag/` and explore workflow workspaces in `_work/`. We’ll keep the runner process running in one shell while using a second terminal to inspect its file structure in real time.

***

## Table of Contents

1. [Directory Layout](#directory-layout)
2. [Inspecting Diagnostic Logs (`_diag/`)](#inspecting-diagnostic-logs-_diag)
3. [Exploring the Workflow Workspace (`_work/`)](#exploring-the-workflow-workspace-_work)
4. [Real-Time Diagnostics](#real-time-diagnostics)
5. [Cleanup](#cleanup)
6. [Summary](#summary)
7. [Links and References](#links-and-references)

***

## 1. Directory Layout

Start the runner in one terminal:

```bash theme={null}
root@ubuntu-host:~/actions-runner$ ./run.sh
```

Open a second terminal to inspect the directory structure:

```bash theme={null}
root@ubuntu-host:~$ cd actions-runner/
root@ubuntu-host:~/actions-runner$ ls -l
total 183128
drwxr-xr-x  4 1001 127    16384 Oct 18 18:27 bin/
-rwxr-xr-x  1 root root     266 Oct 24 14:50 config.sh*
drwxr-xr-x  1 root root    4096 Oct 24 14:48 .credentials/
drwxr-xr-x  1 root root    4096 Oct 24 14:48 .credentials_rsaparams/
drwxr-xr-x  4 root root    4096 Oct 24 14:49 _diag/
-rw-r--r--  1 root root      17 Oct 24 14:48 .env
drwxr-xr-x  4 1001 127    4096 Oct 24 14:48 externals/
-rw-r--r--  1 root root     259 Oct 24 14:48 run-helper.sh.template*
-rwxr-xr-x  1 root root     382 Oct 24 14:50 run-helper.sh*
-rw-r--r--  1 root root     718 Oct 24 14:50 .runner
-rwxr-xr-x  1 root root    2537 Oct 24 15:26 run.sh*
drwxr-xr-x  6 root root    4096 Oct 24 14:48 _work/
```

| Directory       | Purpose                           |
| --------------- | --------------------------------- |
| `bin/`          | Runner executables                |
| `config.sh`     | Configuration script              |
| `.credentials/` | Authentication material           |
| `_diag/`        | Diagnostic and worker logs        |
| `_work/`        | Workflow checkout & runtime files |
| `externals/`    | External dependencies             |

* `_diag/`: Contains both runner and worker logs.
* `_work/`: Hosts the workspace where jobs execute.

***

## 2. Inspecting Diagnostic Logs (`_diag`)

Use `tree` to view the log layout:

```bash theme={null}
root@ubuntu-host:~/actions-runner$ tree _diag/
_diag/
├── blocks
└── pages
    ├── Runner_20231024-144833-utc.log
    ├── Runner_20231024-145143-utc.log
    └── Worker_20231024-152375-utc.log

2 directories, 3 files
```

Display the contents of a runner log:

```bash theme={null}
root@ubuntu-host:~/actions-runner$ cat _diag/pages/Runner_20231024-145143-utc.log
[2023-10-24 14:51:43Z INFO HostContext] Well known directory 'Root': '/root/actions-runner'
[2023-10-24 14:51:43Z INFO RunnerServer] EstablishSvsConnection with 60 seconds timeout.
[2023-10-24 14:51:43Z INFO GitHubActionsService] Starting operation Location.GetConnectionData
...
```

<Callout icon="lightbulb">
  If you encounter connectivity or authentication issues, always start with the latest entries in `_diag/pages/Runner_*.log` and `_diag/pages/Worker_*.log`.
</Callout>

***

## 3. Exploring the Workflow Workspace (`_work`)

### 3.1 Before Any Job Runs

By default, the workspace is mostly empty:

```bash theme={null}
root@ubuntu-host:~/actions-runner$ tree _work/
_work/
└── actions-1
    └── actions-1

7 directories, 1 file
```

### 3.2 Preparing a Long-Running Workflow

To observe changes in `_work/` during execution, use a simple workflow that sleeps:

```yaml theme={null}
name: Self-Hosted Runner Demo
on:
  workflow_dispatch:

jobs:
  demo:
    runs-on: [self-hosted, linux]
    steps:
      - name: Echo and Pause
        run: |
          echo "Runner is active"
          sleep 1500s
```

Commit and trigger via **Run workflow** in the GitHub UI.

<Callout icon="triangle-alert">
  Using `sleep 1500s` keeps the job alive long enough to explore file changes. Remember to cancel or stop the runner when done.
</Callout>

### 3.3 Monitoring Job Start

In the runner terminal you’ll see:

```bash theme={null}
root@ubuntu-host:~/actions-runner$ ./run.sh
Current runner version: '2.310.2'
2023-10-24 14:52:57Z: Running job: demo
