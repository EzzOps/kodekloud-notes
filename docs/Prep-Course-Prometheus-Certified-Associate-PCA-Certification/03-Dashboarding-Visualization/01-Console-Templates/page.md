# => 7.0
```

You can also add multiple labels to capture more dimensions (for example, `path` and HTTP `method`):

```python theme={null}
from prometheus_client import Counter

REQUESTS = Counter(
    "http_requests_total",
    "Total number of requests",
    ["path", "method"]
)

@app.get("/cars")
def get_cars():
    REQUESTS.labels("/cars", "GET").inc()
    return ["toyota", "honda", "mazda", "lexus"]

@app.post("/cars")
def create_cars():
    REQUESTS.labels("/cars", "POST").inc()
    return "Create Car"

@app.get("/boats")
def get_boats():
    REQUESTS.labels("/boats", "GET").inc()
    return ["boat1", "boat2"]

@app.post("/boats")
def create_boat():
    REQUESTS.labels("/boats", "POST").inc()
    return "Create Boat"
```

Label order matters: the first label value corresponds to `path`, the second to `method`, as declared in the metric.

Query examples with multiple labels:

```bash theme={null}
$ http_requests_total{method="GET"}
http_requests_total{path="/cars",method="GET"} 5.0
http_requests_total{path="/boats",method="GET"} 2.0
```

And combining selectors still works:

```bash theme={null}
$ http_requests_total{path="/cars"}
http_requests_total{path="/cars",method="GET"} 5.0
http_requests_total{path="/cars",method="POST"} 1.0
```

Use labels to keep metrics organized and queryable, but be mindful of cardinality: labels that can take many unique values (like user IDs, session tokens, or request IDs) cause a large number of time series and can harm performance and storage.

| Approach                                    | Pros                                                    | Cons                                                                   | When to use                                                        |
| ------------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------ |
| One metric per path (multiple metric names) | Simple to implement                                     | Hard to aggregate, high maintenance, error-prone when adding endpoints | Very small projects with few endpoints and no need for aggregation |
| Single metric with labels (recommended)     | Easy aggregation, fewer metric names, flexible querying | Risk of high cardinality if labels are unbounded                       | Most web services; use for per-path, per-method, per-status counts |

<Callout icon="lightbulb">
  Use labels to keep metrics organized and queryable. However, be cautious about label cardinality: labels with high cardinality (for example, user IDs, session IDs, or other highly unique values) can produce a huge number of time series and cause performance and storage problems. Restrict labels to a small, well-defined set of values.
</Callout>

Links and references

* [Prometheus — Overview](https://prometheus.io/docs/introduction/overview/)
* [Prometheus — Querying basics (PromQL)](https://prometheus.[SECRET_REDACTED]/)
* [prometheus\_client (Python) documentation](https://github.com/prometheus/client_python)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/0c0155c7-00c8-4ca2-a061-e66baa1a3216/lesson/c0e01897-34ab-4c6f-a288-e25b645e8c5c" />
</CardGroup>


# Console Templates

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Dashboarding-Visualization/Console-Templates/page

Explains Prometheus console templates for creating custom HTML dashboards using Go templates, embedding PromQL metrics, reusable fragments, and built-in JS helpers to render charts and drilldowns.

Console templates are Prometheus' built-in way to create small, custom HTML pages using the Go templating language. They let you embed Prometheus metrics, PromQL queries, and interactive charts to build compact dashboards or drill-down views that live on your Prometheus server.

<Frame>
  <img alt="The image contains text explaining that console templates allow for custom HTML page creation using Go templating language, and Prometheus metrics can be embedded in the templates." />
</Frame>

Key points:

* Console templates are plain HTML files augmented with Go template expressions (`{{ ... }}`).
* Templates can call shared fragments (for consistent header/footer/styles).
* Built-in console JS helpers provide drilldowns and chart rendering.

Location
Typically the built-in console templates are stored in `/etc/prometheus/consoles`. Listing that folder shows several example pages.

|                   Filename | Description / Purpose                                        |
| -------------------------: | ------------------------------------------------------------ |
|       `index.html.example` | Example index that imports fragments and lists console pages |
|            `node-cpu.html` | Node CPU charts and queries                                  |
|           `node-disk.html` | Disk-related views                                           |
|                `node.html` | Node-specific metrics overview                               |
|       `node-overview.html` | Comprehensive node overview with multiple charts             |
|          `prometheus.html` | Prometheus server metrics                                    |
| `prometheus-overview.html` | Prometheus overview dashboard                                |

You can also inspect the raw directory contents:

```bash theme={null}
$ ls -l /etc/prometheus/consoles
total 40
-rw-r--r--  1 prometheus prometheus   616 Nov 12 23:20 index.html.example
-rw-r--r--  1 prometheus prometheus  2675 Nov 12 23:20 node-cpu.html
-rw-r--r--  1 prometheus prometheus  3522 Nov 12 23:20 node-disk.html
-rw-r--r--  1 prometheus prometheus  1453 Nov 12 23:20 node.html
-rw-r--r--  1 prometheus prometheus  5783 Nov 12 23:20 node-overview.html
-rw-r--r--  1 prometheus prometheus  1334 Nov 12 23:20 prometheus.html
-rw-r--r--  1 prometheus prometheus  4103 Nov 12 23:20 prometheus-overview.html
```

The pages are standard HTML mixed with Go template directives. For example, `index.html.example` uses fragments like `head`, `tail`, and `prom_content_tail` to assemble the page layout:

```html theme={null}
{{ template "head" . }}
{{ template "prom_right_table_head" }}
{{ template "prom_right_table_tail" }}
{{ template "prom_content_head" . }}

<h1>Overview</h1>
<p>These are example consoles for Prometheus.</p>
<p>These consoles expect exporters to have the following job labels:</p>

<table class="table table-sm table-striped table-bordered" style="width: 0%">
  <tr>
    <th>Exporter</th>
    <th>Job label</th>
  </tr>
  <tr>
    <td>Node Exporter</td>
    <td><code>node</code></td>
  </tr>
  <tr>
    <td>Prometheus</td>
    <td><code>prometheus</code></td>
  </tr>
</table>

{{ template "prom_content_tail" . }}
{{ template "tail" }}
```

Open these pages in your browser by pointing to the Prometheus server under the `/consoles` path, for example:

`http://<prometheus-host>:9090/consoles/index.html.example`

The example pages include job/instance lists, useful charts (CPU, memory, disk, network), and drill-down links for inspecting query expressions.

<Frame>
  <img alt="The image displays a Prometheus dashboard showing the node overview for IP 192.168.1.168:9100, with graphs for CPU usage, Disk I/O utilization, and Memory usage. Various metrics such as user CPU, system CPU, memory details, network data, and disk utilization are listed on the right." />
</Frame>

Built-in consoles are utilitarian but easy to modify. Below are concise steps to create a simple console page, embed a metric drilldown, and render a chart using the console JS helpers.

<Callout icon="lightbulb">
  Console templates are regular HTML files using Go templates. Reuse provided fragments like `head`, `prom_content_head`, and `tail` for consistent styling and JS helpers. You can embed PromQL expressions and use built-in widgets for drilldowns and graphs.
</Callout>

## Create a simple console (demo.html)

Follow these steps to create a minimal custom console that displays a metric value and a chart.

1. Create the file in the consoles directory:

```bash theme={null}
cd /etc/prometheus/consoles
ls
