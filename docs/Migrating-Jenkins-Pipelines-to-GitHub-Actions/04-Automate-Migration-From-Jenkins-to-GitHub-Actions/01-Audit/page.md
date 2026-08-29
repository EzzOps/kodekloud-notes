# .github/workflows/ci.yml (triggers)
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

## 2) Simplified YAML-based workflows

Workflows are stored with your code under `.github/workflows`, making them easy to review, track in pull requests, and version alongside application changes. Compared to Groovy-based Jenkinsfiles or GUI configuration, YAML workflows are typically more accessible to developers and reviewers.

A simple CI workflow example:

```yaml theme={null}
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm test
```

## 3) Cloud-native scalability

GitHub-hosted runners provide automatic scaling for CI workloads. You can run matrix builds and parallel jobs without provisioning or maintaining dedicated build servers or Jenkins agents. This eliminates the operational burden of capacity planning and agent lifecycle management.

## 4) Extensive Marketplace of pre-built Actions

The GitHub Actions Marketplace offers many community and vendor-maintained actions for tasks such as:

* Building and pushing container images
* Deploying to cloud providers (AWS, Azure, GCP)
* Notifying chat systems (Slack, Teams)
* Managing artifact storage and caching

Using marketplace actions reduces the amount of custom scripting and plugin management compared to Jenkins, where several plugins or bespoke scripts might be required for equivalent integrations.

## 5) Lower maintenance overhead

Jenkins requires ongoing server maintenance, plugin updates, and security patching—typically handled by platform or DevOps teams. GitHub Actions, as a managed service, shifts most of this operational work to GitHub and reduces platform overhead for teams.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Migrate from Jenkins to GitHub Actions?&#x22; highlighting &#x22;5. Lower Maintenance Overhead&#x22; with the note &#x22;No plugin updates or server maintenance needed.&#x22; Below it is a screenshot of the Jenkins Manage page showing available updates and security/warning messages." />
</Frame>

Overall, for teams already using GitHub, adopting GitHub Actions can reduce DevOps toil and simplify CI/CD through native integration, readable YAML workflows, scalable hosted runners, reusable marketplace components, and lower maintenance.

<Callout icon="lightbulb">
  [Jenkins](https://learn.kodekloud.com/user/courses/jenkins) remains a powerful choice for advanced on‑premises use cases that require heavy customization, unique plugin ecosystems, or strict network isolation. Evaluate migration based on your specific requirements, compliance constraints, and plugin dependencies.
</Callout>

When to consider staying with Jenkins

* You depend on proprietary or niche plugins only available for Jenkins.
* Your build infrastructure must run in a strictly isolated network with no outbound access.
* You have complex, long-running pipeline orchestration tightly coupled to existing Jenkins jobs and components.

When GitHub Actions is a good fit

* Repositories are hosted on GitHub and you want event-driven workflows.
* You prefer configuration-as-code stored alongside the application.
* You want a managed CI solution with minimal server maintenance and easy scaling.

References and further reading

* [GitHub Actions documentation](https://docs.github.com/actions)
* [Jenkins documentation](https://www.jenkins.io/doc/)
* [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

To conclude: Jenkins is still a valid and capable CI/CD platform for specific, advanced scenarios. For many teams already on GitHub, GitHub Actions simplifies CI/CD with native integration, YAML workflows, automatic scaling, a large marketplace of actions, and reduced maintenance.

<Frame>
  <img alt="A slide titled &#x22;Why Migrate from Jenkins to GitHub Actions?&#x22; comparing Jenkins (left) and GitHub Actions (right). Jenkins is described as powerful for complex, on‑premises pipelines with heavy customization, while GitHub Actions is said to simplify CI/CD with native integration and reduced maintenance." />
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/c8922198-0dcd-4910-9545-21e08f8a847c/lesson/e805e71a-4e1e-4ac6-bb01-e348c027d912" />
</CardGroup>


# Audit

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Audit/page

Guide to auditing Jenkins pipelines, converting them into GitHub Actions workflows, and producing reports, artifacts, and migration tasks to plan and execute workflow migrations.

The `audit` command gives a complete overview of pipelines on a Jenkins server and produces artifacts you can use to plan and execute a migration to GitHub Actions. It performs three primary tasks:

* Enumerates all projects configured on the Jenkins instance.
* Attempts to transform each Jenkins pipeline into an equivalent GitHub Actions workflow.
* Generates a summary report describing feasibility, complexity, and any manual tasks required for migration.

<Frame>
  <img alt="A presentation slide titled &#x22;Perform an Audit&#x22; with a banner reading &#x22;Audit command provides an overview of all pipelines on a Jenkins server.&#x22; Below are three numbered panels listing steps: &#x22;Retrieves Jenkins projects,&#x22; &#x22;Transforms pipelines to GitHub Actions workflows,&#x22; and &#x22;Creates feasibility and complexity report,&#x22; each paired with a colorful icon." />
</Frame>

## Running an audit

By default the audit inspects the entire Jenkins instance. To limit the audit to a single folder, use the `-f` flag and specify the folder path. You must also set the output directory with `--output-dir` (or `-o`); the path must be located beneath the directory from which you run the GitHub Actions Importer commands.

<Callout icon="lightbulb">
  When you provide `--output-dir`, the tool writes all artifacts (converted workflows, logs, and metadata) into that directory. Ensure you have write permissions and sufficient disk space before starting the audit.
</Callout>

Example audit invocation and sample console output:

```bash theme={null}
> gh actions-importer audit jenkins --output-dir tmp/audit
[2024-02-29 19:47:20] Logs: 'tmp/audit/log/actions-importer-20240229-015817.log'
[2024-02-29 19:47:20] Auditing https://jenkins-url.com
[2024-02-29 19:47:20] Output file(s):===================================|
[2024-02-29 19:47:48]  tmp/audit/demo_pipeline/.github/workflows/nodejs_pipeline.yml
[2024-02-29 19:47:48]  tmp/audit/demo_pipeline/config.json
[2024-02-29 19:47:48]  tmp/audit/demo_pipeline/jenkinsfile
[2024-02-29 19:47:48]  tmp/audit/groovy_script/error.txt
[2024-02-29 19:47:48]  tmp/audit/groovy_script/config.json
```

All files listed in the output are written to the `--output-dir` you specified.

## Example audit output tree

Below is a representative `tree` of the audit output showing the types and structure of files the audit produces:

```bash theme={null}
$ tree tmp/audit/
tmp/audit/
├── audit_summary.md
├── ci-pipeline-poll-scm
│   ├── config.json
│   └── jenkinsfile
├── Generate_ASCII_Artwork
│   └── config.json
├── log
│   └── valet-20250521-181951.log
├── multi-branch-pipeline
│   ├── config.json
│   ├── main
│   │   └── config.json
│   └── uat
│       └── config.json
├── scripted-pipeline
│   ├── config.json
│   └── error.txt
├── solar-system-ci-pipeline
│   ├── config.json
│   └── jenkinsfile
└── workflow_usage.csv

13 directories, 19 files
```

## What the audit output contains

The audit directory will contain a mix of human-readable reports, original Jenkins content, converted workflows, metadata files, and logs:

|                           Artifact | Purpose                                                 | Example                                                         |
| ---------------------------------: | ------------------------------------------------------- | --------------------------------------------------------------- |
|                 `audit_summary.md` | Human-readable conversion metrics and findings          | `tmp/audit/audit_summary.md`                                    |
|   Jenkinsfiles & network responses | Originals used for conversion and troubleshooting       | `tmp/audit/demo_pipeline/jenkinsfile`                           |
| Converted GitHub Actions workflows | `.github/workflows/*` files you can validate and commit | `tmp/audit/demo_pipeline/.github/workflows/nodejs_pipeline.yml` |
|                      `config.json` | Conversion metadata for each pipeline                   | `tmp/audit/demo_pipeline/config.json`                           |
|                 Error stack traces | Failure diagnostics for problematic conversions         | `tmp/audit/groovy_script/error.txt`                             |
|               `workflow_usage.csv` | Manifest of actions, secrets, and runners per workflow  | `tmp/audit/workflow_usage.csv`                                  |

Open `audit_summary.md` first to get a quick overview of conversion success rates and items requiring manual attention.

## Pipeline Summary (example)

The Pipeline Summary in `audit_summary.md` reports high-level conversion statistics:

```markdown theme={null}
## Pipelines

Total: **7**

- Successful: **3 (42%)**
- Partially successful: **3 (42%)**
- Unsupported: **1 (14%)**
- Failed: **0 (0%)**

### Job types

Supported: **6 (85%)**

- flow-definition: **3**
- project: **2**
- org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject: **1**

Unsupported: **1 (14%)**

- scripted: **1**
```

Definitions used in the summary:

* Successful: converted automatically to equivalent GitHub Actions constructs.
* Partially successful: converted but requires manual adjustments for one or more items.
* Unsupported: pipeline types the importer cannot convert automatically (for example, some scripted pipelines).
* Failed: conversions that error out due to invalid Jenkins configurations, internal conversion errors, or inaccessible resources.

## Build steps summary (example)

The audit aggregates build steps across pipelines to show how Jenkins steps map to GitHub Actions and which steps need manual attention:

```markdown theme={null}
### Build steps

Total: **17**

Known: **13 (76%)**

- echo: **6**
- hudson.tasks.Shell: **3**
- junit: **2**
- archiveArtifacts: **1**
- sh: **1**

Unknown: **3 (17%)**

- sleep: **2**
- hudson.plugins.git.GitPublisher: **1**

Unsupported: **1 (5%)**

- hudson.tasks.Mailer: **1**

Actions: **22**

- run: **10**
- actions/checkout@v2: **9**
- EnricoMi/publish-unit-test-result-action@v1.7: **2**
- actions/upload-artifact@v2: **1**
```

Key terms:

* Known: automatically mapped to an equivalent Action or `run` step.
* Unknown: no direct mapping; requires manual replacement or a custom action.
* Unsupported: fundamentally incompatible with GitHub Actions as detected by the importer.

This breakdown is useful for security and compliance reviews (for example, creating an allow-list for actions on GitHub Enterprise Server).

## Manual tasks summary (example)

Items the importer could not configure automatically are shown under Manual Tasks. These require repository or organization-level configuration:

```markdown theme={null}
### Manual tasks

Total: **9**

Secrets: **2**

- `${{ secrets.SECRET_TEST_EXPRESSION_VAR }}`: **1**
- `${{ secrets.EXPRESSION_FIRST_VAR }}`: **1**

Self hosted runners: **7**

- `TeamARunner`: **6**
- `DemoRunner`: **1**
```

Manual tasks explained:

* Secrets: repository/organization secrets referenced by converted workflows. Create these manually in GitHub so workflows run correctly.
* Self-hosted runners: runner labels referenced by workflows. Provision and register these runners in GitHub if required.

<Callout icon="warning">
  Workflows that reference secrets or self-hosted runners will not run until those resources are created and configured. Plan to create required secrets and register self-hosted runners before enabling converted workflows in production.
</Callout>

## Manifest of conversion artifacts (example)

The final section of the audit report lists all files written to disk, grouped by Successful, Partially successful, and Failed conversions. These links and files help you inspect original and converted artifacts side-by-side.

```markdown theme={null}
### Successful

#### demo_pipeline
- [monas_dev_work/monas_freestyle/config.json](monas_dev_work/monas_freestyle/config.json)

#### test_multibranch_pipeline
- [test_multibranch_pipeline/config.json](test_multibranch_pipeline/config.json)

### Partially successful

#### test_freestyle_project
#### test_pipeline
- [test_pipeline/.github/workflows/test_pipeline.yml](test_pipeline/.github/workflows/test_pipeline.yml)
- [test_pipeline/config.json](test_pipeline/config.json)
- [test_pipeline/jenkinsfile](test_pipeline/jenkinsfile)

### Failed

#### groovy_script
- [groovy_script/error.txt](groovy_script/error.txt)
- [groovy_script/config.json](groovy_script/config.json)
```

<Frame>
  <img alt="A presentation slide titled &#x22;Review the Audit Summary&#x22; showing four colored rounded cards numbered 01–04 labeled &#x22;Original Jenkins Pipeline,&#x22; &#x22;Network Responses,&#x22; &#x22;Converted Workflow,&#x22; and &#x22;Stack Traces.&#x22; Each card contains a short descriptive line about that audit output." />
</Frame>

## workflow\_usage.csv

The audit produces `workflow_usage.csv`, which maps pipelines to Actions, Secrets, and Runner labels. This is especially valuable for:

* Security reviews (which actions must be allowed or mirrored to an enterprise appliance).
* Creating repository/organization secrets required by converted workflows.
* Identifying self-hosted runners you must provision.

Example CSV contents:

```csv theme={null}
Pipeline,Action,File path
demo_pipeline,actions/checkout@v2,tmp/audit/demo_pipeline/.github/workflows/demo_pipeline.yml
demo_pipeline,actions/upload-artifact@v2,tmp/audit/demo_pipeline/.github/workflows/demo_pipeline.yml

Pipeline,Secret,File path
test_freestyle_project,`${{ secrets.EXPRESSION_FIRST_VAR }}`,tmp/audit/test_freestyle_project/.github/workflows/test_freestyle_project.yml

Pipeline,Runner,File path
demo_pipeline,TeamARunner,tmp/audit/demo_pipeline/.github/workflows/demo_pipeline.yml
test_freestyle_project,DemoRunner,tmp/audit/test_freestyle_project/.github/workflows/test_freestyle_project.yml
```

## Recommended next steps

1. Review `audit_summary.md` to identify:
   * Pipelines that converted successfully and can be enabled quickly.
   * Partially converted pipelines that need manual edits.
   * Unsupported or failed conversions requiring investigation.
2. Use `workflow_usage.csv` to:
   * Create or approve external Actions.
   * Add required secrets in GitHub (repository or organization level).
   * Provision and register any self-hosted runners referenced by workflows.
3. Validate converted workflows by running them in a staging repository before enabling in production.
4. Use logs and `error.txt` stack traces to troubleshoot failed conversions.

## Links and references

* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [GitHub Actions Documentation](https://docs.github.com/actions)
* [GitHub Actions Importer (CLI)](https://docs.github.com/enterprise/importer)

That concludes the audit overview.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/5103f5c1-1448-4082-b951-24a1cc395056" />
</CardGroup>
