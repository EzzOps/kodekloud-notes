# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.665721119292e+09
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 7.3271296e+08
# HELP process_virtual_memory_max_bytes Maximum amount of virtual memory available in bytes.
# TYPE process_virtual_memory_max_bytes gauge
process_virtual_memory_max_bytes 1.8446744073709552e+19
# HELP pushgateway_build_info A metric with a constant '1' value labeled by version, revision, branch, and goversion from which pushgateway was built.
# TYPE pushgateway_build_info gauge
pushgateway_build_info{branch="HEAD",goversion="go1.18.2",revision="f9dc1c8664050edbc75916c3664be1df595a1958",version="1.4.3"} 1
```

## 3) Install as a systemd service (recommended for production)

Run Pushgateway under systemd to ensure it starts on boot and is managed consistently.

Create a dedicated system user and install the binary:

```bash theme={null}
sudo useradd --no-create-home --shell /bin/false pushgateway
sudo cp pushgateway /usr/local/bin/
sudo chown pushgateway:pushgateway /usr/local/bin/pushgateway
sudo chmod 0755 /usr/local/bin/pushgateway
```

Create the systemd unit file at `/etc/systemd/system/pushgateway.service` with the following content:

```ini theme={null}
[Unit]
Description=Prometheus Pushgateway
Wants=network-online.target
After=network-online.target

[Service]
User=pushgateway
Group=pushgateway
Type=simple
ExecStart=/usr/local/bin/pushgateway

[Install]
WantedBy=multi-user.target
```

Reload systemd, start and enable the service:

```bash theme={null}
sudo systemctl daemon-reload
sudo systemctl start pushgateway
sudo systemctl enable pushgateway
sudo systemctl status pushgateway
```

## Quick reference: common commands and locations

| Purpose                | Command / Path                            |
| ---------------------- | ----------------------------------------- |
| Run binary for testing | `./pushgateway`                           |
| Systemd unit file      | `/etc/systemd/system/pushgateway.service` |
| Installed binary       | `/usr/local/bin/pushgateway`              |
| Service user           | `pushgateway`                             |
| Default listen port    | `9091`                                    |

<Callout icon="warning">
  If your server has a firewall (for example `ufw` or `firewalld`), ensure port `9091` is open for Prometheus scrapes or only allow access from Prometheus servers. Running services as root is not recommended — the example above uses a dedicated unprivileged `pushgateway` user.
</Callout>

## 4) Configure Prometheus to scrape Pushgateway

Add Pushgateway as a scrape target in your `prometheus.yml`. In many setups you should enable `honor_labels: true` so label values pushed by clients (for example `job` and `instance`) are preserved in Prometheus instead of being replaced by the Pushgateway scrape labels.

Example `prometheus.yml` snippet:

```yaml theme={null}
scrape_configs:
  - job_name: pushgateway
    honor_labels: true
    static_configs:
      - targets: ["192.168.1.168:9091"]
```

<Callout icon="lightbulb">
  Use `honor_labels: true` when multiple jobs push metrics to Pushgateway and you want the original `job` and `instance` labels from the pushing clients to be preserved in Prometheus. Without this, Prometheus will overwrite those labels with the Pushgateway's own scrape labels.
</Callout>

## 5) Verify end-to-end

1. Push a sample metric from a client (example using curl):

```bash theme={null}
echo "my_job_metric 42" | curl --data-binary @- http://<PUSHGATEWAY_HOST>:9091/metrics/job/my_job/instance/one
```

2. Confirm metrics are visible on Pushgateway:

```bash theme={null}
curl http://<PUSHGATEWAY_HOST>:9091/metrics
```

3. Confirm Prometheus scrapes the Pushgateway and the metric appears in Prometheus targets and in PromQL queries (use the Prometheus UI at `/targets` and `/graph`).

## Troubleshooting tips

* If metrics don’t appear in Prometheus:
  * Verify `prometheus.yml` has the correct address and that Prometheus has reloaded.
  * Check `honor_labels` behavior — it may affect label attribution.
  * Confirm network/firewall rules allow Prometheus to reach port `9091`.
* Check logs:
  * Pushgateway logs: `journalctl -u pushgateway`
  * Prometheus logs: `journalctl -u prometheus` or view Prometheus UI logs.

## Links and references

* Prometheus Pushgateway Releases: [https://github.com/prometheus/pushgateway/releases](https://github.com/prometheus/pushgateway/releases)
* Prometheus documentation: [https://prometheus.io/docs/](https://prometheus.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/18b41166-411a-42a8-91c2-18a5b49bc189/lesson/cb8d5619-8e53-43e4-9e06-ecb93580e52c" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Push-Gateway/Introduction/page

Explains Prometheus Pushgateway for capturing and exposing metrics from short lived batch jobs, including usage, endpoints, examples, and best practices.

In this lesson, we explain Prometheus Pushgateway and how it helps capture metrics from short-lived, ephemeral batch jobs that exit before Prometheus can scrape them.

Batch jobs that run briefly and then terminate are difficult for Prometheus to scrape because the process might have already exited when a scrape occurs. In that case, there is nothing for Prometheus to contact, and the job's metrics are effectively lost from the Prometheus scraping perspective.

The Pushgateway solves this by acting as an intermediary between ephemeral jobs and the Prometheus server. A batch job pushes its metrics to the Pushgateway before it exits. The Pushgateway stores those metrics and exposes them on an HTTP endpoint so Prometheus can scrape them like any other target.

<Frame>
  <img alt="The image illustrates the Push Gateway's role as an intermediary between batch jobs and the Prometheus server, with metrics being scraped at regular intervals." />
</Frame>

Prometheus treats the Pushgateway like any other scrape target: it scrapes the Pushgateway's `/metrics` endpoint on the configured schedule. Prometheus does not need to know that the metrics were pushed; it only consumes the metrics that the Pushgateway exposes.

Typical push flow:

* The job collects metrics while running.
* Before exiting, the job pushes those metrics to the Pushgateway.
* The Pushgateway stores and serves those metrics at `/metrics`.
* Prometheus scrapes the Pushgateway at its regular scrape interval.

Why use Pushgateway?

* Capture metrics from non-long-lived processes (batch jobs, one-off tasks).
* Decouple metric lifetime from job lifetime so Prometheus can scrape them at its schedule.
* Add grouping labels to distinguish pushes from multiple instances.

For more background, see the Prometheus documentation: [Pushgateway](https://prometheus.io/docs/practices/pushing/).

HTTP endpoints and common actions

| Action                    | URL path (example)                            | Description                                                                           |
| ------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------- |
| Push metrics for a job    | `/metrics/job/<job_name>`                     | Push metrics for a job name. Use `POST`/`PUT` or `--data-binary` with `curl`.         |
| Push with grouping labels | `/metrics/job/<job_name>/instance/<instance>` | Add grouping labels (e.g., `instance`, `id`) in the URL path to differentiate pushes. |
| Retrieve stored metrics   | `/metrics`                                    | Prometheus scrapes this endpoint to collect all stored metrics.                       |
| Delete metrics for a job  | `/metrics/job/<job_name>` (HTTP `DELETE`)     | Remove stored metrics to avoid stale data.                                            |

Example: push a local metrics file to the Pushgateway

```bash theme={null}
