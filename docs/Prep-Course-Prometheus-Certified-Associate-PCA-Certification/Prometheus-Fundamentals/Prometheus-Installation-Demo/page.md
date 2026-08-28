# my global config
global:
  scrape_interval: 1m
  scrape_timeout: 10s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
```

Overview of important sections

* `global`: Default parameters that apply to all scrape jobs. Individual `scrape_configs` can override these defaults.
* `scrape_configs`: Defines jobs (logical groups of targets) and how Prometheus should scrape them. Each job may define its own `scrape_interval`, `scrape_timeout`, `metrics_path`, `scheme`, authentication, discovery mechanism, and static targets.

A more detailed example showing per-job overrides and a node metrics job:

> Note: the example below demonstrates overriding defaults for a job; `scheme` and `metrics_path` are illustrative. Most exporters use `http` and the default `metrics_path` (`/metrics`).

```yaml theme={null}
global:
  scrape_interval: 1m       # default scrape interval for jobs that don't override it
  scrape_timeout: 10s       # default scrape timeout

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "nodes"
    scrape_interval: 15s     # overrides global scrape_interval for this job
    scrape_timeout: 5s       # per-job scrape timeout
    scheme: https            # defaults to http if not set
    metrics_path: /stats/metrics
    static_configs:
      - targets: ["192.168.1.168:9100"]
```

Common fields and what they do

* `job_name`: Logical name for the job — added as a `job` label to all scraped metrics.
* `scrape_interval`: How often Prometheus pulls metrics from targets in this job.
* `scrape_timeout`: How long Prometheus will wait for a scrape before it times out.
* `metrics_path`: HTTP path where metrics are exposed (defaults to `/metrics`).
* `scheme`: `http` or `https` (defaults to `http`).
* `static_configs.targets`: List of `host:port` targets to scrape (Node Exporter commonly uses port `9100`).
* `basic_auth`: If targets require basic auth, set `username` and either `password` or `password_file` (mutually exclusive).

Table: Common scrape config fields

| Field                    | Purpose                                                  | Example                                                                |
| ------------------------ | -------------------------------------------------------- | ---------------------------------------------------------------------- |
| `job_name`               | Logical name added to scraped metrics as the `job` label | `job_name: "node"`                                                     |
| `scrape_interval`        | How frequently to scrape targets                         | `scrape_interval: 15s`                                                 |
| `scrape_timeout`         | Per-scrape timeout                                       | `scrape_timeout: 5s`                                                   |
| `metrics_path`           | Path where metrics are exposed                           | `metrics_path: /metrics`                                               |
| `scheme`                 | Protocol used for scrapes                                | `scheme: https`                                                        |
| `static_configs.targets` | Explicit list of `host:port` targets                     | `- targets: ["192.168.1.168:9100"]`                                    |
| `basic_auth`             | Basic authentication for scrapes                         | `basic_auth: { username: "user", password_file: "/etc/secrets/pass" }` |

Reference-style documented options:

```yaml theme={null}
scrape_configs:
  # How frequently to scrape targets from this job.
  # [ scrape_interval: <duration> | default = <global.scrape_interval> ]

  # Per-scrape timeout when scraping this job.
  # [ scrape_timeout: <duration> | default = <global.scrape_timeout> ]

  # The HTTP resource path on which to fetch metrics from targets.
  # [ metrics_path: <path> | default = /metrics ]

  # Configures the protocol scheme used for requests.
  # [ scheme: <scheme> | default = http ]

  # Sets the ‘Authorization’ header on every scrape request with the configured username and password.
  # password and password_file are mutually exclusive.
  basic_auth:
    # [ username: <string> ]
    # [ password: <secret> ]
    # [ password_file: <string> ]
```

Editing the configuration and reloading Prometheus

1. Edit the config file (example path):

```bash theme={null}
sudo vi /etc/prometheus/prometheus.yml
```

2. After saving changes, Prometheus does not automatically pick them up. You have several options to apply the new config:

* If you started Prometheus manually (for example with `./prometheus --config.file=/etc/prometheus/prometheus.yml`), stop it with Ctrl+C and start it again the same way.
* Send a SIGHUP to the Prometheus process to request a config reload:

```bash theme={null}
# find the pid (example)
pidof prometheus
# then:
kill -HUP <pid>
```

* If Prometheus is managed via systemd, restart it:

```bash theme={null}
sudo systemctl restart prometheus
```

<Callout icon="lightbulb">
  After updating `prometheus.yml`, restart Prometheus, send a SIGHUP, or use the `/-/reload` HTTP endpoint (if available) so new scrape jobs take effect.
</Callout>

Verifying targets in the Prometheus UI

* Open the Prometheus UI at `http://<prometheus-host>:9090/`.
* Navigate to Status -> Targets to view all configured targets and their scrape status. A green "UP" indicates a successful scrape.

Example output showing two targets appears in the Prometheus Targets view:

<Frame>
  <img alt="The image shows a Prometheus monitoring dashboard with two targets labeled &#x22;node&#x22; and &#x22;prometheus.&#x22; Both targets are in an &#x22;UP&#x22; state, indicating successful data scraping." />
</Frame>

You can also confirm target status by querying the `up` metric in the Prometheus expression browser:

```text theme={null}
up{instance="192.168.1.168:9100",job="node"}
up{instance="localhost:9090",job="prometheus"}
```

Putting it together — a common `/etc/prometheus/prometheus.yml` example

```yaml theme={null}
# my global config
global:
  scrape_interval: 15s         # scrape targets every 15s
  evaluation_interval: 15s     # evaluate rules every 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node"
    scrape_interval: 15s
    static_configs:
      - targets: ["192.168.1.168:9100"]
```

This minimal configuration allows Prometheus to scrape itself and a Node Exporter instance. From here you can extend jobs with service discovery, relabeling, authentication, TLS settings, alerting, and rule files as required.

Links and references

* Prometheus official docs: [https://prometheus.io/docs/](https://prometheus.io/docs/)
* Prometheus configuration reference: [https://prometheus.[AWS_SECRET_ACCESS_KEY]configuration/](https://prometheus.[AWS_SECRET_ACCESS_KEY]configuration/)
* Node Exporter: [https://github.com/prometheus/node\_exporter](https://github.com/prometheus/node_exporter)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/82d2fead-e942-4e95-966a-1e9fa3184311" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/09035c83-0db2-4a0a-af61-a5d94727ee06" />
</CardGroup>


# Prometheus Installation Demo

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Prometheus-Installation-Demo/page

Guide to install and run Prometheus on a systemd Linux host using a dedicated non-login user, standard directories, and a systemd service unit

This guide walks through installing Prometheus on a Linux system using a dedicated non-login system user and a systemd unit. The steps place Prometheus binaries, configuration, console files, and time-series data in conventional filesystem locations so the service runs securely and predictably.

Overview

1. Create a system user for Prometheus.
2. Create directories for configuration and storage.
3. Download and install Prometheus binaries.
4. Install console files and the configuration file.
5. Create the systemd service unit.
6. Start, enable, and verify the Prometheus service.

Prerequisites

* A Linux host with systemd (most modern distributions).
* `sudo` or root privileges.
* A Prometheus release tarball from the official downloads page: [https://prometheus.io/download/](https://prometheus.io/download/)

Step 1 — Create a dedicated Prometheus user
Create a system user that cannot log in and does not create a home directory. Running Prometheus under its own user improves security and makes ownership straightforward.

```bash theme={null}
sudo useradd --no-create-home --system --shell /usr/sbin/nologin --home-dir /nonexistent prometheus
```

Step 2 — Create directories for configuration and storage
Create standard directories for Prometheus configuration and TSDB data, set secure permissions, and ensure ownership is assigned to the `prometheus` user:

```bash theme={null}
sudo mkdir -p /etc/prometheus
sudo mkdir -p /var/lib/prometheus
sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus
sudo chmod 0755 /etc/prometheus /var/lib/prometheus
```

Step 3 — Download and install Prometheus binaries
Download the appropriate Prometheus tarball from the official releases page and extract it. From the extracted `prometheus-<version>.linux-<arch>` directory, copy the `prometheus` and `promtool` binaries into a directory on the system `PATH` and make them executable:

```bash theme={null}
