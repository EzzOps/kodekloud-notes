# Demo Convert multi stage Jenkins Job to a GitHub Actions Workflow

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Manual-Migration-From-Jenkins-to-GitHub-Actions/Demo-Convert-multi-stage-Jenkins-Job-to-a-GitHub-Actions-Workflow/page

Convert a multi-stage Jenkins scripted pipeline into an equivalent GitHub Actions workflow using jobs and needs to preserve sequential staging and execution

In this guide you'll convert a multi-stage Jenkins *scripted* pipeline into an equivalent GitHub Actions workflow that preserves the same pipeline semantics: Greet → Build → Result. We'll use the same repository and trigger the workflow manually via `workflow_dispatch`.

<Frame>
  <img alt="A dark-themed Jenkins dashboard screenshot showing a list of CI pipeline jobs with status icons, last success/failure times, and run durations. The left sidebar displays navigation options like New Item, Build History, and Manage Jenkins." />
</Frame>

Original Jenkins scripted pipeline (runs on any available agent):

```groovy theme={null}
node { // Runs on any available agent
    stage('Greet') {
        echo 'Hello, World!'
    }

    stage('Build') {
        echo 'Pretending to build...'
        sleep 5 // Simulate work
    }

    stage('Results') {
        def now = new Date()
        echo "Job completed at ${now}"
    }
}
```

Goal: model these three Jenkins stages as three GitHub Actions jobs named `Greet`, `Build`, and `Result`. Each job will run on an `ubuntu-latest` runner. By default GitHub Actions runs jobs in parallel; to preserve sequential behavior use the `needs` keyword to declare dependencies.

Job mapping (Jenkins stage → GitHub Actions job):

| Jenkins Stage | GitHub Actions Job | Purpose                       |
| ------------- | ------------------ | ----------------------------- |
| `Greet`       | `Greet`            | Print greeting message        |
| `Build`       | `Build`            | Simulate a build step (sleep) |
| `Results`     | `Result`           | Emit completion timestamp     |

Save the following workflow as `.github/workflows/scripted-pipeline.yml`:

```yaml theme={null}
name: Scripted Pipeline

on:
  workflow_dispatch:

jobs:
  Greet:
    runs-on: ubuntu-latest
    steps:
      - name: Greet
        run: echo 'Hello, World!'

  Build:
    runs-on: ubuntu-latest
    needs: Greet
    steps:
      - name: Build (simulate)
        run: |-
          echo 'Pretending to build...'
          sleep 5s  # Simulate work

  Result:
    runs-on: ubuntu-latest
    needs: Build
    steps:
      - name: Results
        run: echo "Job completed at $(date)"
```

<Callout icon="lightbulb">
  Quick tips:

  * YAML comments use `#`. `//` is NOT valid YAML and will break the workflow.
  * When using `sleep` in a shell step prefer an explicit time unit like `5s` for portability.
  * Use `needs` to control job ordering; omit it to allow jobs to run in parallel.
</Callout>

If you prefer `Greet` and `Build` to run in parallel (and still have `Result` run after `Build`), remove the `needs: Greet` line from the `Build` job:

```yaml theme={null}
name: Scripted Pipeline (Parallel Greet & Build)

on:
  workflow_dispatch:

jobs:
  Greet:
    runs-on: ubuntu-latest
    steps:
      - name: Greet
        run: echo 'Hello, World!'

  Build:
    runs-on: ubuntu-latest
    # no needs -> runs in parallel with Greet
    steps:
      - name: Build (simulate)
        run: |-
          echo 'Pretending to build...'
          sleep 5s  # Simulate work

  Result:
    runs-on: ubuntu-latest
    needs: Build
    steps:
      - name: Results
        run: echo "Job completed at $(date)"
```

Behavioral notes:

* With `needs` chaining (Greet → Build → Result), jobs execute serially; the total workflow time includes runner startup + each job's runtime.
* Allowing parallel jobs can reduce wall-clock time but consumes more concurrent runners.
* If you want to avoid multiple runner spin-ups, combine multiple stages into a single job (multiple `steps`) to reuse the same runner instance.

Example of the workflow result in the GitHub Actions UI (Greet, Build, Result):

<Frame>
  <img alt="A dark‑themed GitHub Actions run summary for a &#x22;Scripted Pipeline&#x22; showing three successful jobs — Greet, Build, and Result — with a total duration of 27s. The workflow diagram and run details are displayed on the page." />
</Frame>

Console log snippets (what you should see in each job's log):

* Greet job:

```bash theme={null}
Run echo 'Hello, World!'
Hello, World!
```

* Build job:

```bash theme={null}
Run echo 'Pretending to build...'
Pretending to build...
