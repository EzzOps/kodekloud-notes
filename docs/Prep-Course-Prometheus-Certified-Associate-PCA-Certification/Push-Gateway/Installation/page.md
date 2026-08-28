# Create a registry to hold the metrics for this job/process
registry = CollectorRegistry()

# Define a Gauge and register it with the registry
test_metric = Gauge(
    'test_metric',                 # metric name
    'This is an example metric',   # help/description
    registry=registry
)

# Set the metric value
test_metric.set(10)

# Push the registry to the Pushgateway (pushadd = POST-like behavior)
pushadd_to_gateway('user2:9091', job='batch', registry=registry)
```

## Parameters explained

* The first argument to the push function is the Pushgateway address, e.g. `host:port` (`'pushgateway:9091'`).
* `job` is a required grouping label; metrics are organized by job and optional additional grouping labels in the Pushgateway.
* `registry` is the `CollectorRegistry` instance containing the metrics to push.

<Callout icon="lightbulb">
  When you want to replace all metrics for a job, use `push_to_gateway` (PUT semantics). Use `pushadd_to_gateway` to add/merge metrics (POST semantics). To remove metrics for a job or grouping, use `delete_from_gateway`.
</Callout>

## Additional imports and examples

If you need to perform replace or delete operations, import these functions:

```python theme={null}
from prometheus_client import push_to_gateway, delete_from_gateway
```

Example usages:

* Replace (PUT semantics):
  * `push_to_gateway('pushgateway:9091', job='batch', registry=registry')`  # replaces metrics for job
* Delete (DELETE semantics):
  * `delete_from_gateway('pushgateway:9091', job='batch')`  # deletes metrics for job

<Callout icon="warning">
  Ensure the Prometheus Pushgateway is reachable from your process. Choose `job` and any additional grouping labels carefully to avoid unintentionally overwriting or deleting other metrics.
</Callout>

## Links and references

* [Prometheus Pushgateway — pushing metrics](https://prometheus.io/docs/practices/pushing/)
* [prometheus\_client (Python) — GitHub](https://github.com/prometheus/client_python)
* [Prometheus documentation](https://prometheus.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/18b41166-411a-42a8-91c2-18a5b49bc189/lesson/bd98ee9b-5815-453b-a3b6-f261ae83377c" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/18b41166-411a-42a8-91c2-18a5b49bc189/lesson/1b35c5df-3f0d-46cb-b867-50af1283ff50" />
</CardGroup>


# Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Push-Gateway/Installation/page

Installing and running Prometheus Pushgateway, configuring systemd and Prometheus to scrape it, usage for short-lived or batch jobs, verification and troubleshooting

This lesson shows how to install Prometheus Pushgateway, run it for testing, and configure Prometheus to scrape it. Use Pushgateway when short-lived or batch jobs need to push metrics to Prometheus.

## 1) Download Pushgateway

Download the latest Pushgateway release from the official GitHub Releases page:

* [https://github.com/prometheus/pushgateway/releases](https://github.com/prometheus/pushgateway/releases)

<Frame>
  <img alt="The image shows a webpage for downloading the Prometheus Pushgateway with options for different operating systems and corresponding file details such as architecture, size, and SHA256 checksum." />
</Frame>

## 2) Extract and run (quick test)

After downloading the release tarball on your server, extract it and change into the extracted directory:

```bash theme={null}
wget https://github.com/prometheus/pushgateway/releases/download/v1.4.3/pushgateway-1.4.3.linux-amd64.tar.gz
tar xvzf pushgateway-1.4.3.linux-amd64.tar.gz
cd pushgateway-1.4.3.linux-amd64
```

For a quick test you can run the `pushgateway` binary directly; it listens on port `9091` by default:

```bash theme={null}
./pushgateway
```

Open another terminal and verify the metrics endpoint:

```bash theme={null}
curl localhost:9091/metrics
