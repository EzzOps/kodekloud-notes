# This item has no matching transformer
#  - sleep:
#      _key: time
#      value:
#        isLiteral: true
#        value: 20
  - name: Sleep for 5 seconds
    run: sleep 5s
  - name: echo message
    run: echo Second stage completed.
```

We need a transformer that reads the `time` argument from the Jenkins representation and dynamically generates the proper `run: sleep <Ns>` step.

## How the Jenkins step appears in the importer JSON

The importer receives each pipeline step as a JSON item. For `sleep`, the JSON looks like:

```json theme={null}
{
  "name": "sleep",
  "arguments": [
    {
      "key": "time",
      "value": {
        "isLiteral": true,
        "value": 20
      }
    }
  ]
}
```

The numeric sleep value is available at `arguments[0].value.value` (for example, `5` or `20`). Extract that value in your transformer and use it to build the GitHub Actions step.

## Transformer basics

* Transformers are Ruby `.rb` files that define one or more `transform` blocks (DSL entries).
* Each `transform` block should return a Ruby `Hash` that maps to the GitHub Actions YAML for a step.
* Provide transformer files to the CLI with `--custom-transformers` for `audit`, `dry-run`, or `migrate`.

Example CLI usage:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/folder-1/job/folder-2/job/pipeline-project-2 \
  --output-dir tmp/dry-run \
  --custom-transformers helper-transformer.rb
```

> **lightbulb** Use `dry-run` to validate your transformer output before running a full migration. This prevents creating PRs with incorrect workflows.

## Step 1 — Helper transformer to inspect `sleep` items

Start by creating a small helper transformer that prints each `sleep` item so you can confirm the JSON structure and the path to the time value.

Save as `helper-transformer.rb`:

```ruby theme={null}
# helper-transformer.rb
transform "sleep" do |item|
  puts "JSON for sleep identifier: #{item}"
end
```

Run the importer with:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/folder-1/job/folder-2/job/pipeline-project-2 \
  --output-dir tmp/dry-run \
  --custom-transformers helper-transformer.rb
```

You should see output like:

```text theme={null}
JSON for sleep identifier: {"name"=>"sleep", "arguments"=>[{"key"=>"time", "value"=>{"isLiteral"=>true, "value"=>5}}]}
JSON for sleep identifier: {"name"=>"sleep", "arguments"=>[{"key"=>"time", "value"=>{"isLiteral"=>true, "value"=>20}}]}
```

This confirms where the `time` value is located in each `sleep` item.

## Step 2 — Final `sleep` transformer

Now implement the transformer that extracts the time value and returns a hash representing the corresponding GitHub Actions step. Save it as `sleep-transformer.rb`:

```ruby theme={null}
# sleep-transformer.rb
transform 'sleep' do |item|
  # Extract the sleep duration from the step's arguments
  sleep_time = item["arguments"][0]["value"]["value"]

  # Return a Hash representing the GitHub Actions step
  {
    "name" => "Sleep for #{sleep_time} seconds",
    "run"  => "sleep #{sleep_time}s"
  }
end
```

Notes:

* Access the time via `item["arguments"][0]["value"]["value"]`.
* Return a Ruby `Hash` with string keys; the importer converts it into YAML for the workflow.

Run a `dry-run` using this transformer:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/folder-1/job/folder-2/job/pipeline-project-2 \
  --output-dir tmp/dry-run \
  --custom-transformers sleep-transformer.rb
```

If successful, the generated workflow will include transformed `sleep` steps.

### Example generated YAML after transformation

```yaml theme={null}
name: folder-1/folder-2/pipeline-project-2
on:
  workflow_dispatch:
jobs:
  First_Stage:
    name: First Stage
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0
      - name: echo message
        run: echo Starting the first stage...
      - name: Sleep for 5 seconds
        run: sleep 5s
      - name: echo message
        run: echo First stage completed.
  Second_Stage:
    name: Second Stage
    runs-on: ubuntu-latest
    needs: First_Stage
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0
      - name: echo message
        run: echo Starting the second stage...
      - name: Sleep for 20 seconds
        run: sleep 20s
      - name: echo message
        run: echo Second stage completed.
```

## Migrating with the transformer

You can supply the transformer to the `migrate` command. Example:

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/jenkins-demo-org/demo-repo \
  --output-dir tmp/migrate \
  --source-url http://139.84.149.83:8080/job/folder-1/job/folder-2/job/pipeline-project-2 \
  --custom-transformers sleep-transformer.rb
```

If the migration succeeds, the importer creates a pull request in the target repository (for example: `https://github.com/jenkins-demo-org/demo-repo/pull/3`) that contains the converted workflow including the dynamically generated `sleep` steps. You can review and merge that PR on GitHub.

<Frame>
  <img alt="A screenshot of a GitHub pull request page titled &#x22;Convert folder-1/folder-2/pipeline-project-2 to GitHub Actions.&#x22; The page shows a comment saying the pipeline was migrated from Jenkins and the commit message / merge confirmation form." />
</Frame>

## Summary checklist

| Task                        | Why it matters                                           | Example / Command                                                                |
| --------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Create transformer file     | Transformers define how identifiers map to workflow YAML | `sleep-transformer.rb`                                                           |
| Inspect pipeline JSON       | Ensures you extract the correct value path               | Use `helper-transformer.rb` with `dry-run`                                       |
| Use `--custom-transformers` | Provide custom logic to the importer                     | `--custom-transformers sleep-transformer.rb`                                     |
| Test with `dry-run`         | Validate output before making changes to a repo          | `gh actions-importer dry-run jenkins --custom-transformers sleep-transformer.rb` |
| Migrate to create PR        | Apply transformer during migration to produce a PR       | `gh actions-importer migrate jenkins --custom-transformers sleep-transformer.rb` |

> **warning** Ensure you access literal values correctly (e.g., `item["arguments"][0]["value"]["value"]`). Returning an incorrect structure can cause the importer to leave the item untransformed.

## Final example transformer (recap)

```ruby theme={null}
transform 'sleep' do |item|
  sleep_time = item["arguments"][0]["value"]["value"]

  {
    "name" => "Sleep for #{sleep_time} seconds",
    "run"  => "sleep #{sleep_time}s"
  }
end
```

With this pattern you can implement custom transformers for other Jenkins identifiers (for example: `node`, environment variables, or custom build steps) that the importer does not convert automatically.

## Links and references

* [GitHub Actions importer docs](https://docs.github.com/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* gh CLI: `gh actions-importer` commands (use `--help` for details)

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/3978d097-99be-41b1-b148-e980d15ce31d)


# Demo Forecast Potential Build Runner Usage 1

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Forecast-Potential-Build-Runner-Usage-1/page

Guide for using gh actions-importer forecast to estimate GitHub Actions runner usage from Jenkins build history, requiring the Paginated Builds plugin and producing jobs JSON and a forecast report

This guide shows how to use the `gh actions-importer forecast` command to estimate potential GitHub Actions usage from historical CI pipeline runs (example uses Jenkins). The forecast analyzes historical builds and computes metrics — such as total execution minutes, queue times, and concurrency — useful for planning runner capacity or estimating GitHub-hosted runner costs.

The Jenkins server must have the Paginated Builds plugin installed so the importer can retrieve large volumes of build history without timing out.

Example command:

```bash theme={null}
gh actions-importer forecast jenkins --output-dir tmp/forecast
```

> **lightbulb** Install the Jenkins "Paginated Builds" plugin on the target Jenkins server before running `gh actions-importer forecast jenkins`. For Jenkins instances with a lot of historical builds, paginated access prevents request timeouts and ensures the importer can retrieve the full run history.

## What the forecast command does

* Extracts historical build records from your CI provider (Jenkins in this example).
* Computes execution-time statistics, queue-time summaries, and concurrent-job distributions.
* Produces:
  * A jobs JSON file containing one object per build (raw extracted records).
  * A human-readable `forecast_report.md` summarizing the computed metrics for capacity planning.

Useful links

* Jenkins Paginated Builds plugin: [https://plugins.jenkins.io/paginated-builds](https://plugins.jenkins.io/paginated-builds)
* Actions Importer Jenkins docs: [https://github.com/actions-importer/preview/tree/main/jenkins#paginated-builds-plugin](https://github.com/actions-importer/preview/tree/main/jenkins#paginated-builds-plugin)

## Initial run (example failure when plugin is missing)

If the Paginated Builds plugin is not installed, the forecast command will fail and log a message instructing you to install the plugin.

Example failing run and trimmed logs:

```bash theme={null}
root@jenkins in /home
❯ gh actions-importer forecast jenkins --output-dir tmp/forecast
[2025-05-22 09:33:36] Logs: 'tmp/forecast/log/valet-20250522-093336.log'
[2025-05-22 09:33:36] Forecasting 'http://139.84.149.83:8080/'
[2025-05-22 09:33:37] The 'Paginated Builds' plugin (https://plugins.jenkins.io/paginated-builds) must be installed on your Jenkins server prior to running the `forecast` command. Please view https://github.com/actions-importer/preview/tree/main/jenkins#paginated-builds-plugin for more details

Extracting jobs: |=--=--=--=------------=---------------------=|

root@jenkins in /home took 18s
❯
```

The detailed logfile shows the same error and includes a stack trace from the importer:

```text theme={null}
