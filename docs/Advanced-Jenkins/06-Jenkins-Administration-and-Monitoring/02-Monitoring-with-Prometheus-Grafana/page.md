# Monitoring with Prometheus Grafana

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Jenkins-Administration-and-Monitoring/Monitoring-with-Prometheus-Grafana/page

Guides installing Jenkins Prometheus plugin, exposing /prometheus metrics, configuring Prometheus and Grafana via Docker Compose, importing dashboards and validating Jenkins monitoring and metrics visualization.

In this lesson you'll learn how to monitor Jenkins by exposing Prometheus-format metrics using the Jenkins "Prometheus metrics" plugin, scraping those metrics with Prometheus, and visualizing them in Grafana. This guide includes configuration examples, a Docker Compose stack for Prometheus + Grafana, Prometheus scrape config, example Prometheus queries, and steps to import a community Jenkins dashboard into Grafana.

What you'll cover:

* Install and configure the Jenkins Prometheus plugin
* Verify the `/prometheus` metrics endpoint
* Run Prometheus and Grafana (Docker Compose)
* Configure Prometheus to scrape Jenkins
* Add Prometheus as a Grafana data source and import a Jenkins dashboard
* Create test Jenkins activity and validate dashboards

Prerequisites

* A running Jenkins instance where you can install plugins and access Manage Jenkins → Configure System
* Docker & Docker Compose (for the Prometheus + Grafana stack example) or an existing Prometheus/Grafana installation
* Network connectivity between Prometheus and Jenkins (or adjust `prometheus.yml` accordingly)

Install the Jenkins Prometheus plugin

1. In Jenkins go to Manage Jenkins → Manage Plugins and install the "Prometheus metrics" plugin.
2. After installation open Manage Jenkins → Configure System to review plugin settings and enable the metric groups you need (JVM, build metrics, node status, disk usage, etc.).

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Prometheus metrics&#x22; plugin webpage, showing the plugin title, documentation tab, and an About/Metrics Exposed section. On the right are version details, install statistics, and links." />
</Frame>

Configure the Prometheus metrics plugin

* The plugin exposes metrics at `/prometheus` by default.
* Typical settings include the collection interval (often 10s) and checkboxes to enable/disable metric groups (e.g., build durations, JVM metrics).
* Some metrics (like disk usage) may require extra permissions or supplemental plugins.

<Frame>
  <img alt="A screenshot of a Jenkins &#x22;Manage Jenkins > System&#x22; settings page showing the Prometheus metrics plugin options, including a &#x22;Collecting metrics period in seconds&#x22; field and multiple checked checkboxes for counting build durations. The bottom shows job attribute name input and &#x22;Save&#x22; and &#x22;Apply&#x22; buttons." />
</Frame>

> **lightbulb** If the Prometheus plugin requests a Jenkins restart after changing settings, restart Jenkins so the `/prometheus` endpoint is served correctly. The endpoint will be available at `http://<jenkins-host>:<jenkins-port>/prometheus`.

Verify the metrics endpoint
When active, the `/prometheus` endpoint returns plain text in Prometheus exposition format. Example (truncated):

```text theme={null}
