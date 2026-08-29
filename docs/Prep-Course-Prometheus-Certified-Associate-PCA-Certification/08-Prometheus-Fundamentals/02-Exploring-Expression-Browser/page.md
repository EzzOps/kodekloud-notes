# /etc/node_exporter/config.yml
tls_server_config:
  cert_file: node_exporter.crt
  key_file: node_exporter.key
```

Later you can add `basic_auth_users:` to this file for username/password protection (bcrypt hashes).

## 3) Run Node Exporter with the web config file

Update the Node Exporter systemd unit (or the service file you use) so Node Exporter is started with `--web.config.file`:

```ini theme={null}
# /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter --web.config.file=/etc/node_exporter/config.yml

[Install]
WantedBy=multi-user.target
```

Reload systemd and restart:

```bash theme={null}
sudo systemctl daemon-reload
sudo systemctl restart node_exporter
```

Testing note: with a self-signed cert a client like curl will reject the connection by default. To test locally, use:

```bash theme={null}
curl -k https://localhost:9100/metrics
```

If you use a CA-trusted certificate, `-k` is not necessary.

## 4) Move cert/config into a canonical location and set permissions

Best practice: store config and keys under `/etc/node_exporter` and set appropriate ownership/permissions:

```bash theme={null}
sudo mkdir -p /etc/node_exporter
sudo mv node_exporter.crt node_exporter.key config.yml /etc/node_exporter/
sudo chown -R node_exporter:node_exporter /etc/node_exporter
sudo chmod 640 /etc/node_exporter/*.key
sudo chmod 644 /etc/node_exporter/*.crt
sudo systemctl restart node_exporter
```

## 5) Configure Prometheus to validate TLS when scraping the target

Copy the Node Exporter certificate or the CA cert to the Prometheus server so Prometheus can validate the target:

```bash theme={null}
# On Prometheus server, copy the cert from the target host
scp user@node:/etc/node_exporter/node_exporter.crt /etc/prometheus/node_exporter.crt
sudo chown prometheus:prometheus /etc/prometheus/node_exporter.crt
sudo chmod 644 /etc/prometheus/node_exporter.crt
```

Update the Prometheus scrape job to use HTTPS and a `tls_config` that points to the CA file you copied. This ensures proper verification. For quick testing only, you can set `insecure_skip_verify: true` (not recommended for production).

Example scrape job that validates the target certificate:

```yaml theme={null}
- job_name: "node"
  scheme: https
  static_configs:
    - targets: ['node:9100']
  tls_config:
    ca_file: /etc/prometheus/node_exporter.crt
    insecure_skip_verify: false
```

<Callout icon="warning">
  Setting `insecure_skip_verify: true` disables certificate validation and makes TLS vulnerable to man-in-the-middle attacks. Only use this for testing with self-signed certificates. In production, use a CA-signed certificate and keep `insecure_skip_verify: false`.
</Callout>

After editing `prometheus.yml`, restart Prometheus:

```bash theme={null}
sudo systemctl restart prometheus
```

## 6) Enable basic authentication on Node Exporter

To require basic auth for scraping, add a `basic_auth_users` map to the Node Exporter web config. Node Exporter expects bcrypt password hashes.

Install `apache2-utils` (provides `htpasswd`) on the Node Exporter host:

```bash theme={null}
sudo apt update
sudo apt install -y apache2-utils
```

Generate a bcrypt hash for the password (this prompts for the password):

```bash theme={null}
htpasswd -nBC 12 "" | tr -d ':\n'
```

Example bcrypt output (single line):

```text theme={null}
$2y$12$gfAopKVO008KK063rJe0Z9efGRx30qJEZ9vC8IxBP9.cXkurgucc6
```

Add `basic_auth_users` to `/etc/node_exporter/config.yml` and include the hash (quote the string to preserve characters):

```yaml theme={null}
tls_server_config:
  cert_file: node_exporter.crt
  key_file: node_exporter.key

basic_auth_users:
  prometheus: "$2y$12$gfAopKVO008KK063rJe0Z9efGRx30qJEZ9vC8IxBP9.cXkurgucc6"
```

Restart Node Exporter:

```bash theme={null}
sudo systemctl restart node_exporter
```

At this point, Prometheus will likely show the target as DOWN and the target page will return HTTP 401 Unauthorized because Prometheus is not yet sending credentials.

<Frame>
  <img alt="The image shows a Prometheus monitoring interface indicating an endpoint is down, with a 401 Unauthorized error. It also mentions that the Prometheus Server will now show as Unauthorized." />
</Frame>

## 7) Configure Prometheus to use basic auth when scraping

Update the Prometheus job in `prometheus.yml` to include `basic_auth`. Prometheus will send the password over the TLS connection configured earlier.

```yaml theme={null}
- job_name: "node"
  scheme: https
  static_configs:
    - targets: ['node:9100']
  basic_auth:
    username: prometheus
    password: "your_plaintext_password_here"
  tls_config:
    ca_file: /etc/prometheus/node_exporter.crt
    insecure_skip_verify: false
```

Replace `"your_plaintext_password_here"` with the actual password used to create the bcrypt hash earlier (Prometheus requires the plaintext in its config to authenticate when scraping).

Restart Prometheus:

```bash theme={null}
sudo systemctl restart prometheus
```

After Prometheus restarts, verify on the Targets page in the Prometheus web UI that the target shows as UP. This confirms successful HTTPS connection and basic authentication.

## Summary checklist

| Step | Action                              | Example / Notes                                                                              |
| ---- | ----------------------------------- | -------------------------------------------------------------------------------------------- |
| 1    | Generate cert/key for Node Exporter | Use OpenSSL or CA; ensure CN/SAN match the hostname Prometheus uses                          |
| 2    | Create Node Exporter web config     | Add `tls_server_config` and optionally `basic_auth_users` in `/etc/node_exporter/config.yml` |
| 3    | Start Node Exporter with web config | `--web.config.file=/etc/node_exporter/config.yml`                                            |
| 4    | Set canonical paths & permissions   | Store files under `/etc/node_exporter`, `chmod 640` for keys                                 |
| 5    | Configure Prometheus TLS            | Copy cert/CA to Prometheus and set `tls_config.ca_file`                                      |
| 6    | Enable basic auth on Node Exporter  | Add `basic_auth_users: username: "bcrypt_hash"`                                              |
| 7    | Configure Prometheus basic auth     | Add `basic_auth` (plaintext password) to `prometheus.yml`                                    |

## Links and references

* OpenSSL: [https://www.openssl.org/](https://www.openssl.org/)
* curl: [https://curl.se/](https://curl.se/)
* apache2-utils / htpasswd docs: [https://httpd.apache.org/docs/current/programs/htpasswd.html](https://httpd.apache.org/docs/current/programs/htpasswd.html)
* Let's Encrypt: [https://letsencrypt.org/](https://letsencrypt.org/)
* Prometheus documentation (configuration / TLS): [https://prometheus.io/docs/](https://prometheus.io/docs/)

Follow these steps to secure Prometheus scrapes with TLS and basic authentication. For production, prioritize CA-signed certificates and avoid `insecure_skip_verify: true`.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/4c880f39-26ed-48a2-b0ef-5a3e0569c623" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/fe5a2181-a076-4bf9-bd93-8ea791633cb0" />
</CardGroup>


# Exploring Expression Browser

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Exploring-Expression-Browser/page

Guide to using the Prometheus expression browser to run PromQL queries, inspect and graph time series, explore status pages, and troubleshoot metrics and configuration.

In this lesson we'll walk through the Prometheus expression browser — the built-in web UI for running PromQL queries directly against your Prometheus server. You'll learn how to run ad-hoc queries, inspect raw time series, visualize results, and explore useful server pages for configuration, targets, rules, and alerts.

To open the expression browser, point your web browser to the IP or hostname of your Prometheus server and the Prometheus port (default: `9090`). For a local install, use:

`http://localhost:9090`

Key UI elements:

* Expression input: type PromQL queries here.
* Execute button: run the query at the chosen evaluation time.
* Graph / Console tabs: visualize results or view raw series.
* Autocomplete / Highlighting / History: help craft and re-run queries.

Below is the expression browser with metric autocomplete suggesting metrics related to "up".

<Frame>
  <img alt="The image shows the Prometheus time series database interface on a web browser, with a search bar suggesting metric names related to &#x22;up&#x22;." />
</Frame>

Basic queries

Start with a simple built-in metric, `up`, which returns one time series per monitored target with labels that identify that target. Example Console output:

```promql theme={null}
up{instance="192.168.1.168:9100", job="node"}
up{instance="192.168.21.43:80", job="ec2"}
up{instance="192.168.40.248:80", job="ec2"}
up{instance="localhost:9090", job="prometheus"}
```

* In Prometheus, a value of `1` means the target is reachable (UP).
* A value of `0` means the target is unreachable (DOWN).
* Press Execute and switch to the Console tab to see the raw series and their current values.

Drilling into metrics

More detailed metrics produce many series — for example, CPU metrics are split by CPU/core, mode, instance, and job. Example:

```promql theme={null}
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="idle"} 1434.34
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="iowait"} 7.67
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="irq"} 0
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="nice"} 24.7
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="softirq"} 0.51
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="steal"} 0
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="system"} 21.6
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="user"} 60.38
```

Time-travel evaluation

The expression browser supports historical evaluation. Use the calendar/time selector to set a past evaluation time and re-run the query to see values at that timestamp.

<Frame>
  <img alt="The image shows a Prometheus web interface on Firefox running on Ubuntu, displaying a data query with a calendar and time selection tool. The interface includes options like &#x22;Enable autocomplete&#x22; and displays CPU seconds for different nodes." />
</Frame>

Graphing queries

Switch to the Graph tab to visualize query results over a time range. You can:

* Adjust the time window (e.g., 1h, 30m, custom range).
* Choose chart styles and display options.
* Filter or aggregate series if a metric returns many lines (otherwise all series will be plotted).

<Frame>
  <img alt="The image shows a Prometheus graph displaying CPU usage metrics over time with various data series, while running on a Linux operating system within a Firefox web browser." />
</Frame>

Query authoring helpers

The expression input includes autocomplete, syntax highlighting, and a query history — toggle these features via the checkboxes in the UI. Use autocomplete to discover metric names and label keys quickly.

Useful server pages

The expression browser exposes several server pages under the Status and main navigation menus. These pages are essential for debugging Prometheus itself.

| Page                     | Purpose                              | What you’ll find                                                                                 |
| ------------------------ | ------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `Status > Configuration` | Inspect the active Prometheus config | The YAML file Prometheus loaded at startup (scrape intervals, scrape configs, alerting settings) |
| `Status > Targets`       | Troubleshoot scraping issues         | All scrape targets, their UP/DOWN status, last scrape time, and scrape errors                    |
| `Status > Rules`         | View recording & alerting rules      | Loaded recording rules and alerting rules with evaluation state                                  |
| `Alerts`                 | Review alerts                        | Active and pending alerts generated from alerting rules                                          |

Example (truncated) of a running `prometheus.yml` shown on the Configuration page:

```yaml theme={null}
global:
  scrape_interval: 15s
  evaluation_interval: 15s
alerting:
  alertmanagers:
  - follow_redirects: true
    enable_http2: true
    scheme: http
    timeout: 10s
    api_version: v2
    static_configs:
    - targets: []
scrape_configs:
- job_name: prometheus
  honor_timestamps: true
  scrape_interval: 15s
  scrape_timeout: 10s
  metrics_path: /metrics
  scheme: http
  follow_redirects: true
  enable_http2: true
  static_configs:
  - targets:
    - localhost:9090
- job_name: node
  honor_timestamps: true
  scrape_interval: 15s
  scrape_timeout: 10s
  metrics_path: /metrics
  scheme: http
  follow_redirects: true
  enable_http2: true
  static_configs:
  - targets:
    - 192.168.1.168:9100
- job_name: ec2
  honor_timestamps: true
  scrape_interval: 15s
  scrape_timeout: 10s
  metrics_path: /metrics
  scheme: http
  follow_redirects: true
  enable_http2: true
  static_configs:
  - targets: []
```

The Targets page helps you spot unreachable endpoints and scrape errors. The example below shows some endpoints marked DOWN with scrape errors and others UP:

<Frame>
  <img alt="The image shows a Prometheus web interface displaying the status of various endpoints, with some marked as &#x22;DOWN&#x22; and others as &#x22;UP&#x22;. It highlights scrape errors for two &#x22;ec2&#x22; endpoints and a proper connection for &#x22;node&#x22; and &#x22;prometheus&#x22;." />
</Frame>

Best practices and next steps

<Callout icon="lightbulb">
  Use the expression browser for exploratory, ad-hoc queries and troubleshooting. For long-term dashboards and richer visualizations, connect Prometheus to [Grafana](https://grafana.com/) and build persistent dashboards there.
</Callout>

<Callout icon="warning">
  Do not expose the Prometheus expression browser directly to the public internet. Use network controls, authentication proxies, or restricted access to avoid leaking metrics and configuration.
</Callout>

Links and references

* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* PromQL basics: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* Grafana: [https://grafana.com/](https://grafana.com/)

Summary

This covers the core usage of the Prometheus expression browser:

* Run PromQL queries and use autocomplete to author queries faster.
* View raw time series in the Console and plot metrics in the Graph tab.
* Use time-travel evaluation to inspect historical metric values.
* Inspect Prometheus configuration, targets, rules, and alerts via the server pages for effective troubleshooting and monitoring.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/db6382d4-909e-4c31-b246-2e085817c553" />
</CardGroup>
