# Replace <your_token> in config file
sed -i 's/<your_token>/YOUR_TOKEN/' gitlab-ci-pipelines-exporter.yml

docker-compose up -d
```

Once running, access the stack at:

| Service          | URL                                                            |
| ---------------- | -------------------------------------------------------------- |
| Exporter Metrics | [http://localhost:8080/metrics](http://localhost:8080/metrics) |
| Prometheus UI    | [http://localhost:9090](http://localhost:9090)                 |
| Grafana UI       | [http://localhost:3000](http://localhost:3000) (admin/admin)   |

### 3.3 Docker Compose Overview

```yaml theme={null}
version: '3'
services:
  gitlab-ci-pipelines-exporter:
    image: quay.io/mvisonneau/gitlab-ci-pipelines-exporter:latest
    ports:
      - '8080:8080'
    environment:
      GCPE_GITLAB_TOKEN: ${GCPE_GITLAB_TOKEN}
      GCPE_CONFIG: /etc/gitlab-ci-pipelines-exporter.yml
    volumes:
      - ./gitlab-ci-pipelines-exporter.yml:/etc/gitlab-ci-pipelines-exporter.yml

  prometheus:
    image: prom/prometheus:v2.44.0
    ports:
      - '9090:9090'
    volumes:
      - ./prometheus/config.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:9.5.2
    ports:
      - '3000:3000'
    environment:
      GF_AUTH_ANONYMOUS_ENABLED: 'true'
      GF_INSTALL_PLUGINS: grafana-polystat-panel,yesoreyeram-boomtable-panel
    volumes:
      - ./grafana/dashboards.yml:/etc/grafana/provisioning/dashboards/default.yml
      - ./grafana/datasources.yml:/etc/grafana/provisioning/datasources/default.yml
```

### 3.4 Prometheus Scraping Config

Configure Prometheus to scrape the exporter:

```yaml theme={null}
# prometheus/config.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'gitlab-ci-pipelines-exporter'
    scrape_interval: 10s
    static_configs:
      - targets: ['gitlab-ci-pipelines-exporter:8080']
```

### 3.5 Exporter Configuration

A minimal `gitlab-ci-pipelines-exporter.yml`:

```yaml theme={null}
---
log:
  level: debug

gitlab:
  url: https://gitlab.com
  token: <your_token>

project_defaults:
  pull:
    pipeline:
      jobs:
        enabled: true

projects:
  - name: gitlab-org/gitlab-runner
    pull:
      environments:
        enabled: true
        name_regexp: '^stable.*'
  - name: gitlab-org/charts/auto-deploy-app
```

For the full configuration schema, refer to the exporter’s docs:

<Frame>
  ![The image shows a GitHub repository page displaying a markdown file titled "GitLab CI Pipelines Exporter - Configuration syntax," with code snippets for log configuration and server settings.](https://kodekloud.com/kk-media/image/upload/v1752877373/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/github-repo-markdown-gitlab-ci.jpg)
</Frame>

## 4. Creating a Personal Access Token

Generate a token under **User Settings → Access Tokens** with at least `read_api` scope:

<Frame>
  ![The image shows a GitLab user interface for creating a personal access token, with fields for token name, expiration date, and scope selection. The sidebar includes various user settings options like Profile, Account, and Access Tokens.](https://kodekloud.com/kk-media/image/upload/v1752877374/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/gitlab-personal-access-token-ui.jpg)
</Frame>

<Callout icon="triangle-alert">
  Keep your personal access token secure. Do not commit it to public repositories or share it in logs.
</Callout>

Paste this token into `gitlab-ci-pipelines-exporter.yml` before launching the stack.

## 5. Verifying the Exporter

Ensure the exporter is up and exposing metrics:

```bash theme={null}
docker-compose ps
docker logs -f quickstart_gitlab-ci-pipelines-exporter_1
# Check metrics output:
curl -s http://localhost:8080/metrics | grep gcpe_
```

A sample output might include:

```text theme={null}
gcpe_projects_count 47
gcpe_gitlab_api_requests_remaining 1997
gcpe_metrics_count 0
...
```

## 6. Exploring in Prometheus

Visit **Status → Targets** in Prometheus ([http://localhost:9090](http://localhost:9090)) to confirm the exporter is up:

<Frame>
  ![The image shows a Prometheus monitoring dashboard displaying the status of a target called "gitlab-ci-pipelines-exporter," which is up and running with details about its endpoint, state, labels, last scrape time, and scrape duration.](https://kodekloud.com/kk-media/image/upload/v1752877374/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/prometheus-gitlab-ci-pipelines-dashboard.jpg)
</Frame>

Query your GitLab metrics:

<Frame>
  ![The image shows the Prometheus interface with a search query for GitLab metrics, displaying a list of available metrics related to GitLab CI/CD pipelines.](https://kodekloud.com/kk-media/image/upload/v1752877376/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/prometheus-gitlab-metrics-query.jpg)
</Frame>

Render a time series graph:

<Frame>
  ![The image shows a Prometheus dashboard displaying a stacked graph of GitLab CI pipeline coverage over time, with blue and green horizontal bands.](https://kodekloud.com/kk-media/image/upload/v1752877377/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/prometheus-dashboard-gitlab-ci-coverage.jpg)
</Frame>

Adjust time ranges and resolution to dig into historical data:

<Frame>
  ![The image shows a Prometheus dashboard with a stacked graph displaying data over time, likely related to GitLab CI pipeline coverage. The interface includes options for time range, resolution, and various settings.](https://kodekloud.com/kk-media/image/upload/v1752877377/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/prometheus-dashboard-gitlab-ci-graph.jpg)
</Frame>

## 7. Grafana Dashboards

Log in to Grafana ([http://localhost:3000](http://localhost:3000), admin/admin). The exporter provides three ready-to-use dashboards:

### Environments & Deployments

<Frame>
  ![The image shows a dashboard for GitLab CI environments and deployments, displaying various metrics such as availability, deployment status, and environment details in a graphical and tabular format.](https://kodekloud.com/kk-media/image/upload/v1752877379/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/gitlab-ci-dashboard-environments-metrics.jpg)
</Frame>

### Pipelines Overview

<Frame>
  ![The image shows a dashboard for GitLab CI pipelines, displaying metrics such as the number of pipelines, failed pipelines, and average pipeline duration, along with a visual representation of pipeline runs and their statuses.](https://kodekloud.com/kk-media/image/upload/v1752877380/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/gitlab-ci-pipelines-dashboard-metrics.jpg)
</Frame>

### Jobs Statistics

<Frame>
  ![The image shows a GitLab CI jobs dashboard with statistics on job runs, including average job duration and frequency, and lists of running, failed, and successfully completed jobs.](https://kodekloud.com/kk-media/image/upload/v1752877381/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/gitlab-ci-jobs-dashboard-statistics.jpg)
</Frame>

Dive into any metric and click through to GitLab for full context.

<Callout icon="lightbulb">
  For production environments, check out the [HA setup example][2] in the exporter repository.
</Callout>

***

## Links and References

* [GitLab CI Pipelines Exporter][1]
* [HA Setup Example][2]
* [Prometheus Documentation](https://prometheus.io/docs/)
* [Grafana Documentation](https://grafana.com/docs/)

[1]: https://github.com/mvisonneau/gitlab-ci-pipelines-exporter

[2]: https://github.com/mvisonneau/gitlab-ci-pipelines-exporter/tree/master/examples/ha

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/111d1517-3fea-4e1d-84dd-3a00d18cdc93" />
</CardGroup>


# Slack Channel Notifications

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Slack-Channel-Notifications/page

Integrating GitLab with Slack for receiving notifications and monitoring CI/CD pipelines within your messaging workspace.

Integrating GitLab with Slack lets you receive push notifications and monitor CI/CD pipelines without leaving your messaging workspace. This guide walks you through creating a Slack channel, installing the GitLab app, configuring triggers, and verifying notifications.

**Prerequisites**

* A Slack workspace with appropriate permissions
* A GitLab project with repository access

***

## 1. Create a Slack Channel

1. In Slack, click the **+** next to **Channels**.
2. Name it `gitlab-notifications` (or **GitLab Notifications**).
3. Optionally set it to **Private** to restrict access.
4. Skip adding members for this demo.

<Callout icon="lightbulb">
  Use a clear, descriptive name (like `gitlab-notifications`) so team members know exactly where to find CI/CD alerts.
</Callout>

Once the channel is ready, proceed to install the GitLab app in Slack.

***

## 2. Install GitLab for Slack

In your GitLab project:

1. Navigate to **Settings** → **Integrations**.
2. Scroll to **GitLab for Slack** and click **Install**.

<Frame>
  ![The image shows a GitLab interface for integrating with Slack, featuring a button to install the GitLab for Slack app. The left sidebar displays various project settings and options.](https://kodekloud.com/kk-media/image/upload/v1752877382/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Slack-Channel-Notifications/gitlab-slack-integration-interface.jpg)
</Frame>

You’ll be redirected to Slack to authorize GitLab’s access:

<Frame>
  ![The image shows a Slack authorization page where GitLab is requesting permission to access the "mcd-level2" Slack workspace, with options to allow or cancel.](https://kodekloud.com/kk-media/image/upload/v1752877383/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Slack-Channel-Notifications/gitlab-slack-authorization-mcd-level2.jpg)
</Frame>

<Callout icon="triangle-alert">
  Ensure you have admin privileges in Slack. Without proper scope, GitLab cannot post notifications.
</Callout>

***

## 3. Configure Notification Triggers

Back in GitLab’s integration settings:

1. Verify or edit the **Project alias** (e.g., `group/project@timestamp`).
2. Under **Triggers**, select **Push events**.
3. Enter your Slack channel name: `gitlab-notifications`.
4. In **Notifications**, deselect **Notify only for broken pipelines** if you want updates on all statuses.
5. Under **Branches**, choose **All branches** (or specify a subset).
6. Click **Test settings** to send a sample alert.
7. Finally, click **Save changes**.

| Trigger Event  | Description                                                   |
| -------------- | ------------------------------------------------------------- |
| Push events    | Notify on every repository push in the project.               |
| Merge requests | (Optional) Alerts when a merge request is created or updated. |
| Pipeline       | Stream pipeline status changes to Slack.                      |

<Frame>
  ![The image shows a GitLab integration settings page for the GitLab for Slack app, with various trigger options for events like repository pushes and issue updates.](https://kodekloud.com/kk-media/image/upload/v1752877384/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Slack-Channel-Notifications/gitlab-slack-integration-settings.jpg)
</Frame>

<Frame>
  ![The image shows a GitLab integration settings page for Slack notifications, where options for notifying only broken pipelines and specifying branches and labels for notifications are configured.](https://kodekloud.com/kk-media/image/upload/v1752877386/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Slack-Channel-Notifications/gitlab-slack-notifications-settings.jpg)
</Frame>

***

## 4. Commit Changes to Trigger Notifications

To test notifications, add or update your `.gitlab-ci.yml`:

```yaml theme={null}
variables:
  DOCKER_USERNAME: siddharth67
  IMAGE_VERSION: $CI_PIPELINE_ID
  K8S_IMAGE: $DOCKER_USERNAME/solar-system:$IMAGE_VERSION
  MONGO_URI: 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: $M_DB_PASSWORD
  SCAN_KUBERNETES_MANIFESTS: "true"

.prepare_nodejs_environment:
  image: node:17-alpine3.14
  services:
    - name: siddharth67/mongo-db:non-prod
      alias: mongo
      pull_policy: always
  variables:
    MONGO_URI: 'mongodb://mongo:27017/superData'
    MONGO_USERNAME: non-prod-user
    MONGO_PASSWORD: non-prod-password
```

Commit and push to your feature branch:

```bash theme={null}
git add .gitlab-ci.yml
git commit -m "Testing Slack notifications to feature branch"
git push origin feature-branch
```

***

## 5. Review the Slack Notification

In the `#gitlab-notifications` channel, you’ll see a message containing:

* Who pushed the changes
* Target branch
* Project alias (group/project)
* Commit ID and summary

This real-time overview keeps your team in sync without switching contexts.

***

## 6. Monitor the Pipeline in GitLab

While Slack delivers alerts, you can still manage your pipeline in GitLab. For example, a `docker_push` job might look like:

```yaml theme={null}
docker_push:
  stage: containerization
  needs:
    - docker_build
    - docker_test
  image: docker:24.0.5
  services:
    - docker:24.0.5-dind
  script:
    - docker load -i image/solar-system-image:$IMAGE_VERSION.tar
    - docker login --username=$DOCKER_USERNAME --password=$DOCKER_PASSWORD
    - docker push $DOCKER_USERNAME/solar-system:$IMAGE_VERSION
```

<Frame>
  ![The image shows a GitLab pipeline interface for a NodeJS project named "Solar System," with a unit testing job currently running.](https://kodekloud.com/kk-media/image/upload/v1752877387/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Slack-Channel-Notifications/gitlab-pipeline-nodejs-solar-system.jpg)
</Frame>

Once the pipeline finishes, you’ll see the success or failure status in GitLab:

<Frame>
  ![The image shows a GitLab CI/CD pipeline interface for a project named "Solar System NodeJS Pipeline," indicating a successful test job labeled "unit\_testing." The sidebar includes options like Pipelines, Jobs, and Merge requests.](https://kodekloud.com/kk-media/image/upload/v1752877391/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Slack-Channel-Notifications/gitlab-ci-cd-solar-system-pipeline.jpg)
</Frame>

***

## Next Steps

* Use [slash commands](https://docs.gitlab.com/ee/user/project/integrations/slack.html#using-slash-commands) in Slack to trigger pipelines and view statuses.
* Explore additional event triggers (merge requests, pipeline updates, issue events).

## Links and References

* [GitLab for Slack Integration](https://docs.gitlab.com/ee/user/project/integrations/slack.html)
* [Slack App Directory](https://slack.com/apps)
* [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/1573bc2e-563a-424a-a558-2081416601b3/lesson/fa62b816-c16a-4c5d-9caf-3d9d1d010cd7" />
</CardGroup>
