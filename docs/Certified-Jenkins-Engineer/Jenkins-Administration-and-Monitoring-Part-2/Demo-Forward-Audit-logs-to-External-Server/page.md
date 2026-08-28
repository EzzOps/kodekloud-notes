# Demo Forward Audit logs to External Server

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-2/Demo-Forward-Audit-logs-to-External-Server/page

Learn to ship Jenkins audit logs to an Elasticsearch cluster on Elastic Cloud Observability.

In this guide, you’ll learn how to ship Jenkins audit trail logs from your controller to an external Elasticsearch cluster hosted on Elastic Cloud Observability. We’ll cover:

1. Setting up Elastic Cloud Observability
2. Installing the Elastic Agent on your Jenkins controller
3. Configuring the agent to read Jenkins audit logs
4. Verifying audit entries in Kibana

## 1. Set Up Elastic Cloud Observability

1. Sign up for an Elastic Cloud trial on [elastic.co](https://www.elastic.co/cloud).
2. In the Elastic Cloud console, go to **Observability → Logs** and click **Collect and analyze logs**.

<Frame>
  ![The image shows a webpage from Elastic's observability onboarding, offering options to collect and analyze logs, monitor application performance, and monitor infrastructure. There are multiple browser tabs open at the top.](https://kodekloud.com/kk-media/image/upload/v1752870680/notes-assets/images/Certified-Jenkins-Engineer-Demo-Forward-Audit-logs-to-External-Server/elastic-observability-onboarding-webpage.jpg)
</Frame>

3. Choose **Host system logs** as your resource type.

<Frame>
  ![The image shows a webpage from Elastic, asking "What type of resource are you monitoring?" with options for monitoring system logs, log files, OpenTelemetry, Azure, AWS, and Google Cloud Platform.](https://kodekloud.com/kk-media/image/upload/v1752870681/notes-assets/images/Certified-Jenkins-Engineer-Demo-Forward-Audit-logs-to-External-Server/elastic-monitoring-resource-options.jpg)
</Frame>

4. Follow the prompts to install the Elastic Agent and generate an API key for onboarding.

<Frame>
  ![The image shows a webpage from Elastic's Kibana interface, guiding users on how to add observability data by collecting system logs. It includes instructions for installing an Elastic Agent and mentions an API key creation.](https://kodekloud.com/kk-media/image/upload/v1752870682/notes-assets/images/Certified-Jenkins-Engineer-Demo-Forward-Audit-logs-to-External-Server/kibana-observability-data-setup.jpg)
</Frame>

<Callout icon="lightbulb">
  Your Elastic Cloud trial includes full access to Observability features. Save the API key securely, as you’ll need it for agent enrollment.
</Callout>

## 2. Install the Elastic Agent on the Jenkins Controller

On your Jenkins controller shell, download and run the provided installation script. Replace the placeholders with your API key and Cloud endpoint URL:

```bash theme={null}
curl \
  https://<your-cloud-endpoint>/plugins/observabilityOnboarding/assets/standalone_agent_setup.sh \
  -o standalone_agent_setup.sh && \
sudo bash standalone_agent_setup.sh \
  YOUR_API_KEY \
  https://<your-cloud-endpoint>/internal/observability_onboarding \
  8.15.3 \
  <ENROLLMENT_ID>
```

This script will:

* Download and unpack the Elastic Agent
* Enroll the agent using your API key and endpoint
* Place the main config at `/opt/Elastic/Agent/elastic-agent.yml`

## 3. Configure the Agent to Stream Audit Logs

Edit the agent configuration as root:

```bash theme={null}
sudo vi /opt/Elastic/Agent/elastic-agent.yml
```

### 3.1 Define the Elasticsearch Output

Locate (or add) the `outputs` section and update it with your Cloud URL and API key:

```yaml theme={null}
outputs:
  default:
    type: elasticsearch
    hosts: ['https://your-cluster-id.us-central1.gcp.cloud.es.io:443']
    api_key: 'YOUR_API_KEY'
```

### 3.2 Add Log File Inputs

Below `outputs:`, include inputs to capture Jenkins audit files from `/var/log/jenkins/custom*`:

```yaml theme={null}
inputs:
  - id: jenkins-audit-logs
    type: logfile
    data_stream:
      dataset: system.auth
      type: logs
    streams:
      - id: jenkins-audit-logs-stream
        type: logs
        data_stream:
          namespace: default
        paths:
          - /var/log/jenkins/custom*
        exclude_files:
          - '*.gz'
        multiline:
          pattern: '^'
          match: after
        tags: ['jenkins','audit']

  - id: system-messages
    type: logfile
    data_stream:
      dataset: system.syslog
      type: logs
    streams:
      - id: system-messages-stream
        type: logs
        data_stream:
          namespace: default
        paths:
          - /var/log/messages*
          - /var/log/syslog*
          - /var/log/system*
        exclude_files:
          - '*.gz'
        multiline:
          pattern: '^'
          match: after
```

<Callout icon="triangle-alert">
  Ensure indentation and quotation marks are correct in `elastic-agent.yml`. A YAML syntax error will prevent the agent from starting.
</Callout>

### 3.3 Restart the Agent

Apply your changes:

```bash theme={null}
sudo systemctl restart elastic-agent
```

## 4. Verify Logs in Kibana

1. In Kibana, open **Observability → Logs**.
2. Refresh the interface; you should see Jenkins audit events streaming in.

<Frame>
  ![The image shows a webpage from Elastic's Kibana interface indicating that logs are being shipped, with options for downloading a config file, troubleshooting, and exploring logs.](https://kodekloud.com/kk-media/image/upload/v1752870683/notes-assets/images/Certified-Jenkins-Engineer-Demo-Forward-Audit-logs-to-External-Server/kibana-logs-shipping-interface.jpg)
</Frame>

3. Click **Explore logs** to filter, search, and analyze your audit data.

<Frame>
  ![The image shows a screenshot of the Elastic Observability Logs Explorer interface, displaying log details and content breakdown for a specific time range. It includes fields like error messages, service infrastructure, and cloud provider information.](https://kodekloud.com/kk-media/image/upload/v1752870684/notes-assets/images/Certified-Jenkins-Engineer-Demo-Forward-Audit-logs-to-External-Server/elastic-observability-logs-explorer.jpg)
</Frame>

### Sample Audit Entries

```text theme={null}
pipeline logs-system.auth-1.62.1 failed with message: Provided Grok expressions do not match field value: [Nov 10, 2024 3:33:43,556 PM] job/monitor-jenkins/ #35 Started by user siddharth, Parameters:[]
```

Or on your controller:

```text theme={null}
Nov 10, 2024  3:30:09,212 PM job/monitor-jenkins/ #31 Started by user siddharth, Parameters:[]
Nov 10, 2024  3:33:44,394 PM monitor-jenkins #36 Started by user siddharth, Parameters:[] on node #unknown# started at 2024-11-10T15:33:43Z completed in 929ms completed: SUCCESS
```

Continue generating Jenkins audit events; they’ll flow automatically into your Elastic Cloud instance.

***

## Links and References

* [Elastic Cloud Observability](https://www.elastic.co/cloud/observability)
* [Elastic Agent Documentation](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html)
* [Kibana Logs UI](https://www.elastic.co/guide/en/kibana/current/logs.html)
* [Jenkins Audit Trail Plugin](https://plugins.jenkins.io/audit-trail/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/90da5b24-e8f2-455a-9756-9d69f4a7ce8e/lesson/d00342a9-0dd8-4001-b4c1-1a4633ee601f" />
</CardGroup>
