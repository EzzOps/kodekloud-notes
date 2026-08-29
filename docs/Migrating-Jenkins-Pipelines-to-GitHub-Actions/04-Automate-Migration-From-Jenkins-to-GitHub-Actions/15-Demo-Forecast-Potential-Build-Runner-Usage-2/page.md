# Logfile created on 2025-05-22 09:33:36 +0000 by logger.rb/v1.6.0
I, [2025-05-22T09:33:36.761835 #1]  INFO -- : Using GitHub Features: Defaults
I, [2025-05-22T09:33:36.761882 #1]  INFO -- : Forecasting 'http://139.84.149.83:8080/'
I, [2025-05-22T09:33:36.844907 #1]  INFO -- : request: GET http://139.84.149.83:8080/pluginManager/api/json?depth=1&tree=plugins%5BshortName%5D
I, [2025-05-22T09:33:37.046147 #1]  INFO -- : response: Status 200
E, [2025-05-22T09:33:37.048371 #1] ERROR -- : The 'Paginated Builds' plugin (https://plugins.jenkins.io/paginated-builds) must be installed on
/usr/local/bundle/gems/actions_importer-1.3.22397/lib/valet/services/jenkins/extract_jobs.rb:12:in `call'
... (stack trace truncated) ...
```

## Install the Paginated Builds plugin in Jenkins

1. Open Jenkins → Manage Jenkins → Manage Plugins.
2. Search for "Paginated Builds" in the Available plugins tab.
3. Install the plugin and restart Jenkins when prompted.

<Frame>
  <img alt="Screenshot of the Jenkins &#x22;Available plugins&#x22; page in dark mode showing the search for &#x22;paginate&#x22; and the &#x22;Paginated Builds&#x22; plugin selected. A blue &#x22;Install&#x22; button is visible at the top-right." />
</Frame>

The installer shows download and installation progress.

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Download progress&#x22; page showing preparation steps and green success indicators for Paginated Builds and loading plugin extensions. The left sidebar shows the Plugins menu (Updates, Available plugins, Installed plugins, etc.)." />
</Frame>

After restarting Jenkins, confirm the plugin is enabled in Installed plugins.

<Frame>
  <img alt="A screenshot of the Jenkins Plugins management page (dark theme) showing the &#x22;Paginated Builds&#x22; plugin listed. The plugin is enabled with a blue toggle and the sidebar shows Installed plugins and other settings." />
</Frame>

## Rerun the forecast — handle HTTP caching issues

Even after installing the plugin, you may still see the same error if the importer is using previously cached HTTP responses that predate the plugin installation. To force fresh requests, re-run the forecast with the `--no-http-cache` flag.

You can check the forecast command options:

```bash theme={null}
root@jenkins in /home
❯ gh actions-importer forecast --help
Description:
  Forecast GitHub Actions usage from historical pipeline utilization.

Options:
  --source-file-path <source-file-path> (REQUIRED)  The file path(s) to existing jobs data.
  -o, --output-dir <output-dir> (REQUIRED)          The location for any output files.
  --start-date <start-date>                         The start date of the forecast analysis in YYYY-MM-DD format.
  --time-slice <time-slice>                         The time slice in seconds to use for computing concurrency metrics. [default: 60]
  --credentials-file <credentials-file>             The file containing the credentials to use.
  --no-telemetry                                    Boolean value to disallow telemetry.
  --no-ssl-verify                                   Disable SSL certificate verification.
  --no-http-cache                                   Disable caching of HTTP responses.
  --prerelease                                      Use prerelease image for GitHub Actions Importer.
  --no-host-network                                 Use docker's default bridge network instead of the host machine's network.
  -?, -h, --help                                    Show help and usage information

Commands:
  azure-devops  Forecasts GitHub Actions usage from historical Azure DevOps pipeline utilization.
  jenkins       Forecasts GitHub Actions usage from historical Jenkins pipeline utilization.
  gitlab        Forecasts GitHub Actions usage from historical GitLab pipeline utilization.
  circle-ci     Forecasts GitHub Actions usage from historical CircleCI pipeline utilization.
  travis-ci     Forecasts GitHub Actions usage from historical Travis CI pipeline utilization.
  github        Forecasts GitHub Actions usage from historical Github pipeline utilization.
  bamboo        Forecasts GitHub Actions usage from historical Bamboo pipeline utilization.
  bitbucket     Forecasts GitHub Actions usage from historical Bitbucket pipeline utilization.
```

<Callout icon="warning">
  If you still see the plugin-related error after installing Paginated Builds, add `--no-http-cache` to the forecast command to ensure the importer queries Jenkins live instead of using cached plugin lists.
</Callout>

Example successful run using `--no-http-cache`:

```bash theme={null}
root@jenkins in /home
❯ gh actions-importer forecast jenkins --output-dir tmp/forecast --no-http-cache
[2025-05-22 09:40:18] Logs: 'tmp/forecast/log/valet-20250522-094018.log'
[2025-05-22 09:40:18] Forecasting 'http://139.84.149.83:8080/'
[2025-05-22 09:40:21] Output file(s):
    tmp/forecast/jobs/05-22-2025-09-40_jobs_0.json
    tmp/forecast/forecast_report.md

root@jenkins in /home took 23s
```

## Output artifacts

The forecast run produces two primary outputs:

| Artifact                   | Purpose                                                                               | Example path                                     |
| -------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Jobs JSON                  | Raw list of extracted builds; one object per build with timestamps and result details | `tmp/forecast/jobs/05-22-2025-09-40_jobs_0.json` |
| Forecast report (Markdown) | Human-readable summary of totals, execution-time stats, queue times, and concurrency  | `tmp/forecast/forecast_report.md`                |

## Example: jobs JSON snippet

The jobs JSON file contains one object per build record. Each object includes fields such as `id`, `result`, `queue_time`, `start_time`, `finish_time`, and `definition_id`.

```json theme={null}
[
  {
    "id": "28",
    "build_number": null,
    "result": "ABORTED",
    "runner_group": "",
    "queue_time": "2025-05-22T00:00:11+00:00",
    "start_time": "2025-05-22T00:00:11+00:00",
    "finish_time": "2025-05-22T09:20:42+00:00",
    "definition_id": "ci-pipeline-poll-scm",
    "runner_name": "",
    "os_description": null
  },
  {
    "id": "27",
    "build_number": null,
    "result": "SUCCESS",
    "runner_group": "",
    "queue_time": "2025-05-21T07:48:59+00:00",
    "start_time": "2025-05-21T07:48:59+00:00",
    "finish_time": "2025-05-21T07:50:53+00:00",
    "definition_id": "ci-pipeline-poll-scm",
    "runner_name": "",
    "os_description": null
  }
  /* ... additional build objects ... */
]
```

## Example: forecast\_report.md (trimmed)

The generated `forecast_report.md` summarizes totals and statistical metrics that aid capacity planning — such as total execution minutes, median and percentile values, and concurrency distributions.

```markdown theme={null}
- GitHub Actions Importer version: **1.3.22397([AWS_SECRET_ACCESS_KEY])**
- Performed at: **5/22/25 at 09:40**
- Date range: **5/15/25 - 5/22/25**

## Total

- Job count: **32**
- Pipeline count: **5**

- Execution time
  - Total: **9,455 minutes**
  - Median: **1 minute**
  - P90: **1,589 minutes**
  - Min: **0 minutes**
  - Max: **3,499 minutes**

- Queue time
  - Median: **0 minutes**
  - P90: **0 minutes**
  - Min: **0 minutes**
  - Max: **0 minutes**

- Concurrent jobs
  - Median: **1**
```

These metrics are useful for estimating:

* GitHub-hosted runner minute consumption.
* The number of concurrent self-hosted runners required to achieve desired throughput.
* Cost planning and migration strategy when moving pipelines to GitHub Actions.

## Recap and troubleshooting checklist

* Purpose: `gh actions-importer forecast jenkins` computes GitHub Actions usage estimates from historical Jenkins builds.
* Precondition: Install the Jenkins Paginated Builds plugin and restart Jenkins.
* If you see the plugin error after installation:
  * Re-run the command with `--no-http-cache` to bypass stale HTTP responses.
* Outputs:
  * Jobs JSON file (raw build records).
  * `forecast_report.md` (human-readable usage summary).

If you need to review the installer or plugin details, refer to the Jenkins plugin page ([https://plugins.jenkins.io/paginated-builds](https://plugins.jenkins.io/paginated-builds)) and the importer docs ([https://github.com/actions-importer/preview/tree/main/jenkins#paginated-builds-plugin](https://github.com/actions-importer/preview/tree/main/jenkins#paginated-builds-plugin)).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/40334466-4224-4ef0-b0e2-3bea5b363a71" />
</CardGroup>


# Demo Forecast Potential Build Runner Usage 2

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Forecast-Potential-Build-Runner-Usage-2/page

Demonstrates running a folder-scoped Jenkins audit and forecast using gh actions-importer to analyze job execution, queueing, and concurrency for targeted capacity planning and migration

Earlier we audited and forecasted the entire Jenkins server. This lesson shows how to limit that audit/forecast to a single folder inside Jenkins — useful when you only need metrics for a subset of jobs (for focused capacity planning, migration assessments, or targeted troubleshooting).

<Frame>
  <img alt="A screenshot of a Jenkins dashboard showing a list of jobs and pipelines, with a folder item named &#x22;folder-1&#x22; outlined in red. The left sidebar displays Jenkins menu options (New Item, Build History, Manage Jenkins, etc.) and build queue/status." />
</Frame>

What you’ll see in this example:

* A folder named `folder-1`.
* Inside `folder-1`:
  * `project1` — a Freestyle job that runs a simple `sleep` command (30 seconds).
  * A nested `folder-2` that contains additional jobs (including a Pipeline).

To illustrate the effect of concurrent executors, I triggered the Freestyle job several times. Because the Jenkins master in this demo has two executors, two builds run concurrently; subsequent builds queue until an executor is free.

Quick summary of jobs in `folder-1`:

| Job / Folder         | Type                 | Behavior                                           |
| -------------------- | -------------------- | -------------------------------------------------- |
| `project1`           | Freestyle            | Runs `sleep 30` (multiple triggered runs observed) |
| `folder-2`           | Folder               | Contains pipeline jobs (see below)                 |
| `pipeline-project-2` | Declarative Pipeline | Two stages with `echo` / `sleep` steps             |

Next, open `folder-2` to inspect the Pipeline job.

<Frame>
  <img alt="A dark‑theme Jenkins web interface showing a folder titled &#x22;folder-2&#x22; with a listed pipeline job (pipeline-project-2) and columns for last success, last failure and duration. The left sidebar displays folder actions (Configure, New Item, Delete Folder, etc.) and a small build queue panel is visible." />
</Frame>

The pipeline is a minimal Declarative example; it contains two stages that echo a message and sleep for a few seconds:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('First Stage') {
      steps {
        echo 'Starting the first stage...'
        sleep time: 5, unit: 'SECONDS'
        echo 'First stage completed.'
      }
    }

    stage('Second Stage') {
      steps {
        echo 'Starting the second stage...'
        sleep time: 10, unit: 'SECONDS'
        echo 'Second stage completed.'
      }
    }
  }
}
```

I triggered this pipeline multiple times as well. Actual start times vary depending on executor availability and queued tasks.

<Frame>
  <img alt="A screenshot of a Jenkins pipeline project page (pipeline-project-2) showing the left action menu (Build Now, Configure, Open Blue Ocean, etc.), a central &#x22;Permalinks&#x22; list of recent builds, and a Builds panel with recent build statuses. The UI is in dark mode and shows the Jenkins version 2.504.1 in the corner." />
</Frame>

Restrict the audit/forecast to a folder

* Use the `-f` (or `--folder`) argument to limit the scope to a single folder inside Jenkins. The folder name should match the name shown in the Jenkins UI.

<Callout icon="lightbulb">
  Use `-f <folder-name>` to restrict the audit/forecast to a single folder (e.g., `folder-1`). The folder name should match the name visible in Jenkins.
</Callout>

Example command that targets only `folder-1`:

```bash theme={null}
gh actions-importer forecast jenkins --output-dir tmp/forecast --no-http-cache -f folder-1
```

Abbreviated sample output from the run:

```bash theme={null}
[2025-05-22 09:55:20] Logs: 'tmp/forecast/log/valet-20250522-095520.log'
[2025-05-22 09:55:20] Forecasting 'http://139.84.149.83:8080/'
[2025-05-22 09:55:21] Output file(s):
[2025-05-22 09:55:21]   tmp/forecast/jobs/05-22-2025-09-55_jobs_0.json
[2025-05-22 09:55:21]   tmp/forecast/forecast_report.md
```

Interpreting the folder-scoped forecast

* The generated report and job JSON files contain only the jobs present inside the specified folder (`folder-1` in this example).
* In this run the forecast report summarized:
  * 2 pipeline projects
  * 9 total job runs (4 runs of the Freestyle `project1` and 5 runs of the Pipeline)
  * Metrics limited to those jobs: execution time, queue time, concurrency, and per-job run statistics

Why use folder-scoped forecasts?

* Focused capacity planning: measure executor needs for a subset of jobs (e.g., a team folder).
* Migration assessments: analyze only the jobs you plan to migrate.
* Faster runs: smaller scope reduces runtime and output size compared to full-server audits.

References and further reading

* Jenkins: [What is Jenkins?](https://www.jenkins.io/doc/)
* Jenkins Pipelines: [Pipeline as Code](https://www.jenkins.io/doc/book/pipeline/)
* GitHub CLI & actions-importer (example usage): refer to your project or extension documentation for `gh actions-importer` usage and flags

If you want, I can provide a step-by-step checklist to run the folder-scoped forecast in your environment or show how to parse the generated `jobs_*.json` for custom metrics.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/de5c4025-9e6f-4cef-a456-40de2a9ae52a" />
</CardGroup>
