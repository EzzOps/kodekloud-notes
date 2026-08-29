# you should see the example files listed earlier
sudo vi demo.html
```

2. Use the standard fragments for header and footer. These provide the required CSS/JS and layout:

```html theme={null}
{{ template "head" . }}
{{ template "prom_content_head" . }}
{{ template "prom_content_tail" . }}
{{ template "tail" }}
```

3. Replace the middle area with your page content. Save the following as `/etc/prometheus/consoles/demo.html`. This example:
   * Renders a page header,
   * Inserts the current value of `node_memory_Active_bytes` as a clickable drilldown,
   * Adds a chart that visualizes the same metric.

```html theme={null}
{{ template "head" . }}
{{ template "prom_content_head" . }}

<h1>Memory details</h1>

<p>
  Active memory:
  {{ template "prom_query_drilldown" (args "node_memory_Active_bytes") }}
</p>

<div id="graph"></div>

<script>
  // Create a graph inside the div with id="graph".
  // PromConsole.Graph is provided by Prometheus console JS libraries.
  new PromConsole.Graph({
    node: document.querySelector("#graph"),
    // The expr can be any PromQL expression. Adjust it to your needs.
    expr: "node_memory_Active_bytes"
  });
</script>

{{ template "prom_content_tail" . }}
{{ template "tail" }}
```

4. Open your new console page in a browser:

`http://<prometheus-host>:9090/consoles/demo.html`

You should see:

* The header/footer and CSS from the included fragments,
* An H1 "Memory details",
* A rendered metric value for `node_memory_Active_bytes` as a clickable link showing label details and the PromQL expression,
* A chart rendered inside `#graph` showing the metric over time.

Example metric text shown by the drilldown widget:

```text theme={null}
node_memory_Active_bytes{instance="192.168.1.168:9100", job="node"} 9160494976
```

Tips and recommended usage

* Use `{{ template "prom_query_drilldown" (args "<metric_name>") }}` to create clickable metric values that show expression details.
* Use `new PromConsole.Graph({...})` to render interactive charts using the console JS library.
* Reuse fragments such as `head`, `prom_content_head`, `prom_content_tail`, and `tail` to keep consistent layout and load required JS/CSS.
* Combine multiple graphs, tables, and fragments to build richer dashboards or drill-down pages.

Links and References

* Prometheus documentation: [https://prometheus.io/docs/](https://prometheus.io/docs/)
* Go templates (for `{{ ... }}` syntax): [https://pkg.go.dev/text/template](https://pkg.go.dev/text/template)
* Prometheus server web UI and consoles: [https://prometheus.io/docs/visualization/consoles/](https://prometheus.io/docs/visualization/consoles/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/d8fe7717-c2f8-4cfc-b3a7-c88d20fd5659/lesson/f48953a3-b698-460c-b2f1-e05596815346" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/d8fe7717-c2f8-4cfc-b3a7-c88d20fd5659/lesson/01eb9964-a4de-4275-81af-cf6770a2c596" />
</CardGroup>


# Expression Browser

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Dashboarding-Visualization/Expression-Browser/page

Prometheus Expression Browser web UI for ad hoc PromQL queries, quick graphs, metric discovery and troubleshooting, not for building persistent dashboards or production monitoring.

The Expression Browser is Prometheus' built‑in web UI for running PromQL queries and drawing quick, simple graphs. It is intended for ad‑hoc troubleshooting, quick data checks, and exploratory queries — not for building long‑term, custom dashboards or production monitoring views.

<Callout icon="lightbulb">
  Use the Expression Browser when you need fast, one‑off queries or to verify metric names/labels. For structured dashboards and alerts, use a dashboarding solution such as Grafana.
</Callout>

<Frame>
  <img alt="The image is a slide titled &#x22;Expression Browser&#x22; that outlines its purpose as a built-in web UI for executing queries and simple graphs, noting its limited functionality and lack of ability to build custom dashboards for day-to-day monitoring." />
</Frame>

## Accessing the Expression Browser

Open a browser and navigate to your Prometheus server IP and port (by default `:9090`). For a local instance, that is commonly:

`http://localhost:9090`

<Frame>
  <img alt="The image shows a Firefox web browser on a Linux desktop with a search for &#x22;localhost:9090&#x22;, suggesting access to a Prometheus time series collection and processing server." />
</Frame>

## Querying: autocomplete, instant vs range vectors

The query box accepts any valid PromQL expression. Autocomplete helps discover metric names and label keys/values as you type — enable or disable it with the checkbox on the page.

<Frame>
  <img alt="The image shows a web interface of Prometheus, a time-series database, in the Firefox browser. It displays a search function suggesting metrics, such as node_arp_entries and node_boot_time_seconds, to query." />
</Frame>

Example: an instant vector query returning the current value and labels for a node metric:

```Prometheus theme={null}
node_memory_Active_bytes{instance="192.168.1.168:9100", job="node"}
```

When you Execute, the Expression Browser returns the current sample(s) for that instant vector. You can change the evaluation timestamp (the "evaluation time") to inspect the value at any previous moment.

To request a range of samples for a given time window, use a range vector selector — for example, the last 5 minutes:

```PromQL theme={null}
node_memory_Active_bytes[5m]
```

Important distinction:

* Instant vectors (e.g., `metric{...}`) return values at a single timestamp.
* Range vectors (e.g., `metric[5m]`) return multiple samples across a window and are used as inputs to functions such as `rate()` and `increase()`.

<Frame>
  <img alt="The image shows a Prometheus web interface in a Firefox browser on Ubuntu, displaying a query result for node_memory_Active_bytes with data fetched from a specified instance." />
</Frame>

<Callout icon="warning">
  The Graph tab expects an instant vector to plot. Supplying a bare range vector will cause an error — wrap the range vector in an aggregation/function (for example `rate()`), or remove the range selector for plotting an instant vector.
</Callout>

## Graphing and panels

* Switch to the Graph tab to render the query output. If the query returns an instant vector, Prometheus will plot the single value at the selected evaluation time.
* To plot time series, use functions that accept range vectors (e.g., `rate()`), or use a metric that yields time series points directly.
* You can add multiple panels (queries) to the page to compare results side‑by‑side and remove panels as needed.
* Use the graph window controls to change the display range (e.g., 30m, 2h) or set a different evaluation time.

Common graphing examples:

* Rate of memory metric over the last 5 minutes:

```PromQL theme={null}
rate(node_memory_Active_bytes[5m])
```

* CPU usage rate (per CPU mode) over the last 2 minutes:

```PromQL theme={null}
rate(node_cpu_seconds_total[2m])
```

When graphing metrics with multiple label combinations (for example, different CPU modes), the legend populates automatically so you can identify each series.

## Quick examples and outputs

Example instant vector result (simplified):

```Prometheus theme={null}
node_memory_Active_bytes{instance="192.168.1.168:9100",job="node"} 903811072
```

Example of using a range vector inside a function to produce a plottable result:

```PromQL theme={null}
rate(node_cpu_seconds_total[2m])
```

## Comparison: Expression Browser vs Dashboard tools

| Feature        | Expression Browser              | Dashboard (Grafana)                 |
| -------------- | ------------------------------- | ----------------------------------- |
| Use case       | Ad‑hoc queries, debugging       | Persistent dashboards, templating   |
| Query language | PromQL                          | PromQL (via Prometheus datasource)  |
| Visualization  | Basic line plots and raw output | Rich panels, annotations, alerts    |
| Best for       | Quick exploration               | Day‑to‑day monitoring and reporting |

## Tips and best practices

* Prefer the Expression Browser for quick lookups, metric discovery, and validating PromQL expressions.
* For ongoing monitoring, alerting, and multi‑panel dashboards, integrate Prometheus with Grafana.
* When you get a graphing error, check whether your query returns an instant vector or a range vector and apply an appropriate function (e.g., `rate()` or `avg_over_time()`).

Further reading:

* Prometheus documentation: [https://prometheus.io/](https://prometheus.io/)
* PromQL basics: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/d8fe7717-c2f8-4cfc-b3a7-c88d20fd5659/lesson/2fed6a36-d435-46de-8728-e1a9fd5824e6" />
</CardGroup>
