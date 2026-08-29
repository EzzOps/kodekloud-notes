# Executing Shell Scripts in Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/GitHub-Actions-Core-Concepts/Executing-Shell-Scripts-in-Workflow/page

This article explains how to execute shell scripts in GitHub Actions workflows to simplify command management and improve readability.

Running multiple commands as separate `run` steps can clutter your GitHub Actions workflow. By bundling them into a single shell script, you simplify maintenance, improve readability, and reduce duplication.

## 1. Why Consolidate `run` Steps?

When you split each command into its own `run`, your workflow becomes long and harder to manage:

```yaml theme={null}
jobs:
  ascii_job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4

      - name: Install Cowsay
        run: sudo apt-get install cowsay -y

      - name: Generate ASCII Art
        run: cowsay -f dragon "Run for cover; I am a DRAGON... RAWR!" >> dragon.txt

      - name: Search for "dragon"
        run: grep -i "dragon" dragon.txt

      - name: Display File Contents
        run: cat dragon.txt

      - name: List Repo Files
        run: ls -ltra
```

| Approach                 | Pros                          | Cons                         |
| ------------------------ | ----------------------------- | ---------------------------- |
| Multiple `run` steps     | Easy to read individual steps | Repetitive YAML; longer file |
| Single shell script call | Cleaner workflow; reusability | Must manage external script  |

## 2. Create a Reusable Shell Script

Add a file named `ascii-script.sh` at the root of your repository with all commands:

```bash theme={null}
#!/bin/sh
sudo apt-get update
sudo apt-get install cowsay -y
cowsay -f dragon "Run for cover; I am a DRAGON... RAWR!" >> dragon.txt
grep -i "dragon" dragon.txt
cat dragon.txt
ls -ltra
```

Make sure to commit this script:

```bash theme={null}
git add ascii-script.sh
git commit -m "Add ASCII art shell script"
```

> **lightbulb** You can reference this pattern for any multi-step process—testing, building, or deployment—by swapping commands in your script.

## 3. Refactor Your Workflow to Invoke the Script

Update your workflow to run only the script:

```yaml theme={null}
jobs:
  ascii_job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: List Current Files
        run: ls -ltra

      - name: Run ASCII Art Script
        run: ./ascii-script.sh
```

After pushing, navigate to the **Actions** tab to see your new workflow run:

![The image shows a GitHub Actions page with a list of workflow runs, displaying their status, branch, and timestamps. Some workflows are marked as successful, while others have failed or are in progress.](https://kodekloud.com/kk-media/image/upload/v1752876142/notes-assets/images/GitHub-Actions-Certification-Executing-Shell-Scripts-in-Workflow/github-actions-workflow-runs-status.jpg)

## 4. Troubleshoot “Permission denied”

If you see an exit code 126, it means the script lacks execute permissions:

![The image shows a GitHub Actions page where a workflow named "Executing Shell Script" has failed. The job "ascii\_job" completed with an exit code 126.](https://kodekloud.com/kk-media/image/upload/v1752876143/notes-assets/images/GitHub-Actions-Certification-Executing-Shell-Scripts-in-Workflow/github-actions-executing-shell-script-failed.jpg)

```text theme={null}
/home/runner/work/_temp/.../script.sh: line 1: ./ascii-script.sh: Permission denied
Error: Process completed with exit code 126
```

> **triangle-alert** Always ensure your script is executable. You can either set the permission locally with `chmod +x ascii-script.sh` before committing, or update your workflow to grant permissions at runtime.

## 5. Grant Execute Permissions in the Workflow

Modify the step to add execution rights before running the script:

```yaml theme={null}
jobs:
  ascii_job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: List Current Files
        run: ls -ltra

      - name: Run ASCII Art Script
        run: |
          chmod +x ascii-script.sh
          ./ascii-script.sh
```

Commit and push these changes to restart the workflow.

## 6. Verify the Successful Run

When the workflow reruns, you’ll see:

```text theme={null}
Run ls -ltra
total 24
-rw-r--r-- 1 runner docker 161 Oct 11 11:17 ascii-script.sh
-rw-r--r-- 1 runner docker 227 Oct 11 11:17 README.md
...
```

And then:

```bash theme={null}
chmod +x ascii-script.sh
./ascii-script.sh
shell: /usr/bin/bash -e {0}
