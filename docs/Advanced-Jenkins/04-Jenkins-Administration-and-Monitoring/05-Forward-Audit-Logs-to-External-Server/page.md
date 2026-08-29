# Check Jenkins service status (Debian/Ubuntu)
root@jenkins-server ~ ➜ service jenkins status
* jenkins is running

root@jenkins-server ~ ➜
```

> **lightbulb** On modern Linux distributions using systemd, prefer `systemctl status jenkins` to view the service unit status and logs.

Course preview: what you will master

* Shared Libraries — refactor and reuse pipeline logic across many repositories.
* Advanced agents and node management — build custom Docker agents and run Jenkins agents as Kubernetes Pod templates for isolation and scalability.
* Pipeline optimization and caching — reduce build times with caching strategies and effective pipeline structuring.
* Scripted vs Declarative pipelines — decide which style fits your use case and compose maintainable pipelines.
* Jenkins administration & monitoring — instrument Jenkins with metrics, alerts, and secure audit trails.
* Backup and configuration management — use Jenkins Configuration as Code and backup strategies to achieve reproducible environments.

Shared Libraries and reducing duplication
Basic Jenkinsfiles work for single projects, but Shared Libraries let you centralize logic, reduce duplication, and enforce consistency.

<Frame>
  <img alt="A presentation slide titled &#x22;Why use Shared Library&#x22; with three colorful icons labeled &#x22;Duplication,&#x22; &#x22;Inconsistency,&#x22; and &#x22;Complexity.&#x22; A small circular video feed of a person is visible in the bottom-right corner." />
</Frame>

Agents, node management, and containerized builds
You will learn to author Docker images for Jenkins agents and define Kubernetes Pod templates. These approaches give you:

* Better resource isolation
* Reproducible build environments
* Improved scalability for CI workloads

Pipeline structure: Scripted vs Declarative
We compare the two pipeline styles and explain trade-offs so you can select the right approach for maintainability vs flexibility.

<Frame>
  <img alt="A presentation slide titled &#x22;Types of Pipeline Projects&#x22; comparing Scripted Pipeline (code-centric, flexible, steeper learning curve) and Declarative Pipeline (human-readable, easier to learn, limited complexity). A small circular video of a presenter appears in the lower-right corner." />
</Frame>

Pipeline enhancement and caching
Learn techniques to:

* Cache dependencies between runs
* Use layered Docker images to minimize rebuilds
* Organize complex workflows for reliability and speed

Administration, monitoring, and observability
Discover how to instrument Jenkins, collect metrics, and visualize performance to keep your CI system healthy. We cover common tooling integrations and practical monitoring dashboards.

<Frame>
  <img alt="A dark-themed monitoring dashboard (labeled &#x22;Advanced Jenkins&#x22;) showing various Jenkins performance metrics like processing speed, queued rate, memory usage and many &#x22;None&#x22; or &#x22;N/A&#x22; values. A small circular video overlay with a person speaking appears in the bottom-right corner." />
</Frame>

Backup, configuration as code, and integrations
We’ll cover:

* Jenkins Configuration as Code to declare and version control your Jenkins setup
* Backup and restore best practices
* When and how to integrate with other CI platforms like GitHub Actions

<Frame>
  <img alt="A bearded man in a black T-shirt gestures while speaking on camera. To his left is a presentation slide titled &#x22;Advanced Jenkins Curriculum&#x22; listing topics like Shared Libraries, Advanced Agents and Node Management, and Backup and Configuration Management." />
</Frame>

Course modules at a glance

| Module                | Focus                                   | Outcome                                    |
| --------------------- | --------------------------------------- | ------------------------------------------ |
| Shared Libraries      | Reusable pipeline code and utilities    | Centralized pipeline logic for many repos  |
| Advanced Agents       | Docker agents, Kubernetes Pod templates | Scalable, isolated build environments      |
| Pipeline Optimization | Caching, layering, parallelization      | Faster, more reliable builds               |
| Pipeline Styles       | Scripted vs Declarative                 | Choose maintainability or flexibility      |
| Admin & Monitoring    | Prometheus/Grafana metrics, auditing    | Observable and secure Jenkins instances    |
| Config & Backup       | Jenkins Configuration as Code, backups  | Reproducible and restorable infrastructure |

Community and continued learning
At KodeKloud we encourage community interaction. Join the forum to ask questions, share solutions, and learn from other practitioners.

References and further reading

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Jenkins Configuration as Code Plugin](https://plugins.jenkins.io/configuration-as-code/)
* [Learn By Doing: AIOps Foundations - Intelligent Monitoring With Prometheus & Grafana](https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana)
* [GitHub Actions course on KodeKloud](https://learn.kodekloud.com/user/courses/github-actions)

> **warning** When applying changes to production Jenkins, use a staging environment and version-controlled configuration (JCasC). Always validate backups and restore procedures before relying on them in emergencies.

If you're ready to bridge the gap between basic Jenkins knowledge and production-ready CI/CD practices, let’s get started.

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/60bfe853-6ad7-4041-bad5-cf4419fe5f07/lesson/89fb6a70-439e-404e-806a-3d9457996417)


# Forward Audit Logs to External Server

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Jenkins-Administration-and-Monitoring/Forward-Audit-Logs-to-External-Server/page

How to forward Jenkins Audit Trail log files from a controller to Elastic Cloud using Elastic Agent, configure elastic-agent.yml, restart agent, and verify logs in Kibana

This guide shows how to forward Jenkins Audit Trail logs (already written to a file on the Jenkins controller) to Elastic Cloud (hosted Elasticsearch) using the Elastic Agent. The high-level flow:

1. Use Elastic Cloud Observability onboarding to get the Elastic Agent installation command and API key.
2. Install the Elastic Agent on the Jenkins controller.
3. Update the Elastic Agent configuration at `/opt/Elastic/Agent/elastic-agent.yml` to stream the Audit Trail files.
4. Verify logs in Kibana / Elastic Cloud Observability.

Recommended reading:

* [Elastic Cloud](https://www.elastic.co/cloud/)
* [Kibana](https://www.elastic.co/kibana/)

## 1. Create an Elastic Cloud trial and get onboarding details

In Elastic Cloud, open the Observability tab → Collect and analyze logs → choose the resource type to monitor (for a Jenkins controller, choose host system logs or stream log files). Elastic Cloud will produce an onboarding one-liner that downloads and installs the Elastic Agent and enrolls it with your cluster.

<Frame>
  <img alt="A screenshot of the Elastic/Kibana observability onboarding page showing tiles for selecting resource types to monitor — e.g., Stream host system logs, Stream log files, OpenTelemetry, and cloud providers (Azure, AWS, Google Cloud). A search bar and a &#x22;Setup guides&#x22; button are visible in the top navigation." />
</Frame>

Example onboarding command (replace the API key and onboarding URL with the values provided):

```bash theme={null}
curl https://artifacts.elastic.co/downloads/beats/elastic-agent/standalone_agent_setup.sh -o standalone_agent_setup.sh \
  && sudo bash standalone_agent_setup.sh '<API_KEY>' 'https://<YOUR_ONBOARDING_ENDPOINT>' 8.15.3 '<ONBOARDING_ID>'
```

> **warning** Keep your onboarding API key secret. Do not check it into source control or share it publicly. Use the exact API key and onboarding endpoint provided by your Elastic Cloud Observability onboarding page.

When you run the script it will download and install the Elastic Agent, enroll it with your Elastic Cloud instance, and write a base configuration file to `/opt/Elastic/Agent/elastic-agent.yml`.

Typical condensed output:

```text theme={null}
Downloading Elastic Agent archive...
Elastic Agent successfully installed, starting enrollment.
Checking Elastic Agent status
Elastic Agent running (id: 45023cea-1f89-4b06-b5e6-32a749038edd)
Download and save configuration to /opt/Elastic/Agent/elastic-agent.yml
Done with standalone Elastic Agent setup. Make sure to add your configuration to /opt/Elastic/Agent/elastic-agent.yml, then look for streaming logs to arrive in Kibana
```

## 2. Confirm Jenkins Audit Trail files exist

Before configuring the agent, confirm the Audit Trail plugin writes logs somewhere accessible to the agent. Common location:

```bash theme={null}
ls -l /var/log/jenkins
```

Example output:

```text theme={null}
total 12
drwxr-xr-x  2 jenkins jenkins 4096 Nov 10 14:30 ./
drwxrwxr-x 10 root     syslog 4096 Nov 10 00:00 ../
-rw-r--r--  1 jenkins jenkins  526 Nov 10 14:30 custom-audit-0.log-2024-11-10
-rw-r--r--  1 jenkins jenkins    0 Nov 10 14:30 custom-audit-0.log-2024-11-10.lck
```

Sample audit log lines:

```text theme={null}
Nov 10, 2024 2:29:30,662 PM/job/monitor-jenkins/configSubmit by siddharth from 124.123.186.17
Nov 10, 2024 2:29:34,672 PM job/monitor-jenkins/#29 Started by user siddharth, Parameters:[]
Nov 10, 2024 2:29:39,049 PM monitor-jenkins #29 Started by user siddharth, Parameters:[] on node #unknown# started at 2024-11-10T14:29:34Z completed in 4361ms completed: SUCCESS
Nov 10, 2024 2:30:45,042 PM /manage/configSubmit by siddharth from 124.123.186.17
```

## 3. Review the onboarding configuration

The onboarding script writes a base `elastic-agent.yml`. Important sections:

* `outputs` — where the agent sends data (Elasticsearch cluster and API key).
* `inputs` — what log files to collect.

Representative snippet (from onboarding):

```yaml theme={null}
outputs:
  default:
    type: elasticsearch
    hosts:
      - 'https://your-cluster.us-central1.gcp.cloud.es.io:443'
    api_key: 'REPLACE_WITH_YOUR_API_KEY'

inputs:
  - id: system-logs-... 
    type: logfile
    data_stream:
      namespace: default
    streams:
      - id: logfile-system.auth-...
        data_stream:
          dataset: system.auth
          type: logs
        paths:
          - /var/log/auth.log*
          - /var/log/secure*
        exclude_files:
          - .gz$
        multiline:
          pattern: '^\\s'
          match: after
        tags:
          - system-auth
```

You will add a logfile input for the Jenkins Audit Trail files under the `inputs:` list.

## 4. Add a logfile input for Jenkins Audit Trail

Edit `/opt/Elastic/Agent/elastic-agent.yml` and add a logfile input that targets the Audit Trail files. Use wildcards to capture rotated files and include `multiline` only if entries span multiple lines.

Minimal example to add under `inputs:`:

```yaml theme={null}
- id: jenkins-audit-logs
  type: logfile
  data_stream:
    namespace: default
  streams:
    - id: logfile-jenkins-audit
      data_stream:
        dataset: jenkins.audit
        type: logs
      paths:
        - /var/log/jenkins/custom*.log*
      exclude_files:
        - .gz$
      multiline:
        # If your logs include continuation lines, match lines starting with whitespace as a continuation
        pattern: '^\\s'
        match: after
      tags:
        - jenkins-audit
```

Key considerations:

* Use `paths` with a wildcard (`custom*.log*`) to include rotated logs.
* Only enable `multiline` if log entries span multiple lines; the `pattern: '^\\s'` + `match: after` treats indented lines as continuations.
* Select a clear `dataset` (e.g., `jenkins.audit`) so logs are organized correctly in Elastic.

## 5. Restart the Elastic Agent

After saving `elastic-agent.yml`, restart the agent so it applies the new configuration:

```bash theme={null}
sudo systemctl restart elastic-agent
sudo systemctl status elastic-agent --no-pager
```

Or, if the CLI is available:

```bash theme={null}
sudo elastic-agent status
```

Give it a minute to start shipping logs.

## 6. Verify logs in Kibana / Elastic Cloud

Open Kibana → Observability → Logs (or Discover). Look for events with the dataset you configured (for example `jenkins.audit`) and inspect parsed fields.

If parsing or ingest issues occur, check:

* Agent logs on host: `/var/log/elastic-agent/` or `journalctl -u elastic-agent`.
* That the `paths:` you configured match actual files and permissions allow the agent to read them.
* The ingest pipeline used by Elastic for your dataset; default pipelines may expect a different timestamp/format.

## Troubleshooting

| Symptom                                               |                                            Likely cause | Action                                                                                             |
| ----------------------------------------------------- | ------------------------------------------------------: | -------------------------------------------------------------------------------------------------- |
| No logs appear in Kibana                              | Agent not reading the correct files or lacks permission | Check `paths` and file permissions; inspect agent logs (`/var/log/elastic-agent/` or `journalctl`) |
| Grok/ingest parsing errors                            |        Default ingest pipeline doesn't match log format | Adjust ingest pipeline in Elastic or add processors in `elastic-agent.yml` to pre-process lines    |
| Only current file is collected (rotated logs missing) |               `paths` did not include rotated filenames | Use wildcards like `custom*.log*` to include rotated files                                         |

Example parsing error you might see:

```text theme={null}
Provided Grok expressions do not match field value: [Nov 10, 2024 3:33:43,556 PM]job/monitor-jenkins/ #35 Started by user siddharth, Parameters:[]
```

This indicates the pipeline expects a different timestamp or layout. Either modify the ingest pipeline or add a `grok` processor in the agent configuration to normalize the fields.

> **lightbulb** Make sure to use the exact API key and onboarding endpoint provided by your Elastic Cloud Observability onboarding page. After editing `elastic-agent.yml`, always restart the Elastic Agent so it reloads the configuration.

## Summary checklist

| Step                     | Command / Path                                                          | Notes                                                         |
| ------------------------ | ----------------------------------------------------------------------- | ------------------------------------------------------------- |
| Get onboarding command   | N/A (Elastic Cloud UI)                                                  | Use the Observability → Collect and analyze logs flow         |
| Install agent            | `bash standalone_agent_setup.sh '<API_KEY>' 'https://<ONBOARDING>' ...` | Use the exact API key/onboarding URL from the UI              |
| Confirm audit logs exist | `ls -l /var/log/jenkins`                                                | Confirm file names and rotation pattern                       |
| Configure agent          | Edit `/opt/Elastic/Agent/elastic-agent.yml`                             | Add logfile input pointing to `/var/log/jenkins/custom*.log*` |
| Restart agent            | `sudo systemctl restart elastic-agent`                                  | Check status and agent logs                                   |
| Verify in Kibana         | Kibana → Observability → Logs                                           | Look for `dataset: jenkins.audit` or your chosen dataset      |

That’s it — once the agent is reading the audit files and sending events to your Elastic Cloud cluster, you can build Discover queries, dashboards, or alerts based on the `jenkins.audit` dataset.

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/fe8b8755-ab0a-429d-ac8c-a7763f723359/lesson/52395607-f81b-4c76-87a6-23f1db54ada7)
