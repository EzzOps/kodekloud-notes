# Push a metrics file to the Pushgateway under job name "batch_job"
curl --data-binary @metrics.txt http://pushgateway:9091/metrics/job/batch_job
```

Example: include grouping labels in the push URL

```bash theme={null}
# Push a single metric with job and instance grouping labels
curl --data-binary 'my_metric 42' http://pushgateway:9091/metrics/job/batch_job/instance/instance1
```

Example: remove metrics for a job to avoid stale entries

```bash theme={null}
# Delete metrics for the job "batch_job"
curl -X DELETE http://pushgateway:9091/metrics/job/batch_job
```

Best practices and caveats

<Callout icon="lightbulb">
  Use the Pushgateway primarily for short-lived, ephemeral jobs. The Pushgateway stores metrics until they are explicitly deleted or overwritten. If metrics are not removed or updated after a job completes, they can become stale and produce misleading results in Prometheus.
</Callout>

Additional tips:

* Prefer instrumenting long-lived services directly and let Prometheus scrape them.
* Use meaningful grouping labels in the URL path to avoid label collisions and to identify metric sources.
* Automate deletion of Pushgateway entries when jobs are complete, or implement a TTL/cleanup mechanism if appropriate.
* Monitor the Pushgateway itself as a scrape target to ensure it remains available for Prometheus to collect pushed metrics.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/18b41166-411a-42a8-91c2-18a5b49bc189/lesson/978542d0-0941-457f-b7be-fc82245031b9" />
</CardGroup>


# Pushing Metrics

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Push-Gateway/Pushing-Metrics/page

Guide to pushing Prometheus metrics to a Pushgateway via HTTP, covering URL grouping keys, curl examples, and POST PUT DELETE semantics for updating or deleting metric groups

This article explains how to push metrics to a Prometheus Pushgateway using the HTTP endpoint. You can push metrics in two ways:

* Send an HTTP request directly to the Pushgateway (covered here).
* Use a Prometheus client library to push metrics programmatically (not covered).

This guide covers URL structure, examples with `curl`, grouping behavior, and the different HTTP methods (POST, PUT, DELETE) and their semantics.

## HTTP push URL structure

The Pushgateway accepts metric pushes at an endpoint that encodes a grouping key in the URL path. The grouping key is derived from the `job` name and any additional label/value pairs encoded as path segments.

Pattern:

`http://<pushgateway_address>:<port>/metrics/job/<job_name>/<label1>/<value1>/<label2>/<value2>`

Key points:

* Labels encoded in the path are appended to every pushed metric and form part of the grouping key.
* The grouping key determines how metrics are grouped for updates and deletions.
* Always URL-encode label names and values that include special characters (slashes, spaces, etc.).

Reference:

* Prometheus Pushgateway documentation: [https://github.com/prometheus/pushgateway](https://github.com/prometheus/pushgateway)
* Prometheus text exposition format: [https://prometheus.io/docs/instrumenting/exposition\_formats/](https://prometheus.io/docs/instrumenting/exposition_formats/)

## Pushing a single metric with curl

Metric data must be sent in Prometheus' text exposition format. A common pattern is to pipe the metric text into `curl` with `--data-binary @-`, which reads the request body from stdin and sends a POST by default.

Example: push a simple metric named `example_metric` with value `4421` under `job="db_backup"`:

```bash theme={null}
echo "example_metric 4421" | curl --data-binary @- http://localhost:9091/metrics/job/db_backup
```

Explanation:

* `echo "example_metric 4421"` writes the metric in the text exposition format.
* `curl --data-binary @-` sends stdin as the request body (POST by default).
* The URL `http://localhost:9091/metrics/job/db_backup` sets the grouping key `job="db_backup"`.

Verify the metric is exposed by the Pushgateway:

```bash theme={null}
curl http://localhost:9091/metrics | grep example_metric
```

## Grouping behavior and label-based grouping keys

Metrics pushed to the same URL path—i.e., the same `job` and identical label/value path components—belong to the same group. Groups enable updating or deleting a set of metrics together.

Example: push two metrics into the same group (`job=archive`, `db=mysql`):

```bash theme={null}
cat <<EOF | curl --data-binary @- http://localhost:9091/metrics/job/archive/db/mysql
