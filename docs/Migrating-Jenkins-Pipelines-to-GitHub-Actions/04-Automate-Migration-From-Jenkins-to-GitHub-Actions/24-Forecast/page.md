# This item has no matching transformer
# - sleep:
#   - key: time
#     value:
#       isLiteral: true
#       value: 80
      - name: echo message
        run: echo "DISABLE_AUTH is ${{ env.DISABLE_AUTH }}"

  test:
    runs-on:
      - self-hosted
      - TeamARunner
    needs: build
    steps:
      - name: checkout
        uses: actions/checkout@v2
      - name: Publish test results
        uses: EnricoMi/publish-unit-test-result-action@v1.7
        if: always()
        with:
          files: "**/target/*.xml"
```

## Common mappings

The importer converts many Jenkins constructs to GitHub Actions equivalents. The table below summarizes typical mappings and examples.

| Jenkins construct  |    GitHub Actions equivalent | Example                                                                           |
| ------------------ | ---------------------------: | --------------------------------------------------------------------------------- |
| `agent` (label)    |                    `runs-on` | `label 'TeamARunner'` → `runs-on: ['self-hosted', 'TeamARunner']`                 |
| `environment`      |                        `env` | `DISABLE_AUTH = 'true'` → `env: DISABLE_AUTH: 'true'`                             |
| `stages` / `steps` |             `jobs` / `steps` | `stage('build') { steps { ... } }` → `jobs.build.steps: [...]`                    |
| Test publishing    | Actions or community actions | `junit '**/target/*.xml'` → `uses: EnricoMi/publish-unit-test-result-action@v1.7` |

## Notes on partial conversions

* Many Jenkins constructs map directly to GitHub Actions concepts (agents -> `runs-on`, `environment` -> `env`, stages/steps -> jobs/steps).
* When a Jenkins construct has no matching transformer (for example, `sleep 80`), the importer leaves a commented representation in the generated YAML so you can review and implement the desired behavior manually.
* Commented placeholders in the YAML make it clear where custom handling is required and where to add your own steps or actions.
* The generated workflow includes best-effort substitutions (for example, `self-hosted` + label for custom runners) but you should review `runs-on` and runner labels to ensure they match your GitHub-hosted or self-hosted runner setup.

## Next steps

* Review the generated files in the `--output-dir` and confirm the mappings for `env`, `runs-on`, job dependencies (`needs`), and test publishing.
* Create custom transformers for Jenkins constructs that need automatic translation (for example, converting `sleep` into an equivalent step using `timeout` or a small script).
* When satisfied with the dry-run output, run the importer without `dry-run` to generate real workflow files and open a pull request.

Links and references

* [GitHub Actions documentation](https://docs.github.com/actions)
* [Jenkins documentation](https://www.jenkins.io/doc/)
* [GitHub Actions Importer (gh actions-importer)](https://github.com/github/gh-actions-importer)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/8c88e5f7-609c-431e-9d7b-013ae5380f32" />
</CardGroup>


# Forecast

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Forecast/page

Explains the forecast command that analyzes Jenkins historical runs to predict GitHub Actions runner minutes, peak concurrency, queue behavior, and costs to plan pipeline migration.

This lesson covers the `forecast` command from GitHub Actions Importer. The forecast step estimates the effort, resource usage, and feasibility of migrating Jenkins CI/CD pipelines to GitHub Actions before you convert them. By analyzing historical Jenkins run data, it predicts runner minutes, concurrency needs, and queue behavior so you can plan capacity and cost for GitHub-hosted or self-hosted runners.

<Frame>
  <img alt="A presentation slide titled &#x22;Purpose&#x22; that says &#x22;Estimate the effort and feasibility of migrating pipelines before conversion.&#x22; It shows two cards: &#x22;Estimating GitHub Actions Usage&#x22; and &#x22;Analyzing Historical Data&#x22; with bullets about predicting resource use, cost planning, and evaluating past and future pipeline workloads." />
</Frame>

How the forecast command works — a high-level overview:

* Data collection: extracts Jenkins metrics such as build durations, frequencies, job metadata, and queue labels.
* Usage prediction: analyzes the collected metrics to estimate GitHub Actions runner minutes, peak concurrency, and expected queue times.
* Reporting: produces logs, datasets of completed jobs, and human-readable forecast reports.
* Planning aid: provides actionable numbers to size runner pools, choose runner types, and estimate billing costs.

<Frame>
  <img alt="A presentation slide titled &#x22;Functionalities&#x22; showing four feature tiles: Data Collection (highlighted), Usage Prediction, Reporting, and Planning Aid. The Data Collection tile notes it &#x22;Collects Jenkins metrics like build duration and frequency.&#x22;" />
</Frame>

## Usage

Run the forecast against your Jenkins instance. The command writes logs and the forecast report to the output directory you specify:

```bash theme={null}
gh actions-importer forecast jenkins --output-dir tmp/forecast
```

After the command completes, the output directory (for example `tmp/forecast`) contains:

* Logs of the forecast process
* A dataset of completed Jenkins jobs used for analysis
* One or more forecast reports summarizing resource and concurrency predictions

## Key metrics included in the forecast report

The forecast report focuses on a concise set of metrics that drive migration planning. Use the table below to quickly understand each metric and why it matters.

| Metric            | What it measures                                             | Why it matters                                                        |
| ----------------- | ------------------------------------------------------------ | --------------------------------------------------------------------- |
| Job count         | Total number of completed jobs analyzed                      | Helps validate dataset size and representativeness                    |
| Pipeline count    | Number of unique pipelines (jobs) observed                   | Identifies breadth of workflows to migrate                            |
| Execution time    | Time a runner spent executing a job (per-job and aggregated) | Direct input for calculating total runner minutes and cost            |
| Queue time        | Time jobs waited for a runner                                | Reveals need for higher concurrency or autoscaling                    |
| Concurrent jobs   | Jobs running simultaneously over time                        | Determines peak runner count required                                 |
| Per-queue metrics | Metrics broken down by Jenkins queue/label/node type         | Useful when different queue types have different capacity or hardware |

Example summary from a forecast report:

```text theme={null}
- Job count: 73
- Pipeline count: 6

- Execution time
  - Total: 27,057 minutes
  - Median: 2 minutes
  - P90: 19 minutes
  - Min: 0 minutes
  - Max: 15,625 minutes
```

Use those totals to estimate GitHub-hosted runner cost (runner minutes × price per minute for the chosen runner type). Refer to the GitHub Actions billing documentation to apply accurate pricing:

* [About billing for GitHub Actions](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)

## How to interpret the numbers

* Execution time (total and percentiles): gives you expected monthly or yearly runner minutes. Multiply these by the per-minute price for the runner image you plan to use to estimate cost.
* Peak concurrency: informs how many simultaneous runners you should provide (self-hosted or GitHub-hosted concurrency limits).
* High queue time: indicates either not enough runners or uneven scheduling; consider autoscaling or redistributing workloads.
* Per-queue differences: prioritize migrating queues with predictable usage first; complex or highly variable queues may need capacity buffer or dedicated self-hosted runners.

<Callout icon="lightbulb">
  Use the forecast results to size runner pools and estimate costs before migrating pipelines. Combine the forecasted runner minutes and peak concurrency with GitHub Actions pricing and your chosen runner types to prepare an accurate migration plan.
</Callout>

## Example planning steps after a forecast

1. Aggregate total runner minutes from the forecast for the migration window you care about (monthly, quarterly).
2. Choose runner types (GitHub-hosted images or self-hosted hardware), and apply cost per-minute or infrastructure cost estimates.
3. Evaluate peak concurrency to set a minimum runner pool or autoscaling policy.
4. For queues with large variance or long-running jobs, consider isolating those onto dedicated self-hosted runners or throttling parallelism.
5. Re-run forecasts periodically or after major pipeline changes to keep capacity planning accurate.

## Links and references

* [GitHub Actions billing documentation](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
* [GitHub Actions Importer (project README)](https://github.com/github-actions/importer) (reference for command usage and advanced options)

That’s all for now.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/3b575584-05ea-4df8-959c-9c5dbda8e0cd" />
</CardGroup>
