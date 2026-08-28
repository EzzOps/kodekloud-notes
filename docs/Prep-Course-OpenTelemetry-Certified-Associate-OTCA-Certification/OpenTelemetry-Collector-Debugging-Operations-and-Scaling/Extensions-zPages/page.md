# Open a local web UI for the profile
go tool pprof -http=:8080 cpu.pprof

# If you have the collector binary for symbolization, include it:
go tool pprof -http=:8080 /path/to/otelcol cpu.pprof
```

The pprof visualizer supports flame graphs, callgraphs, and textual reports. Flame graphs are particularly useful to quickly identify hot call paths—wider blocks represent functions that consume more CPU time.

<Frame>
  <img alt="The image shows a visualization of profiling results, likely from the pprof tool, with a colorful flame graph depicting function calls and execution paths. It includes various labeled sections like &#x22;runtime&#x22;, &#x22;net/http&#x22;, and &#x22;go.opentelemetry.io&#x22;." />
</Frame>

Interpreting flame graphs and call stacks

* Start from the wide blocks (hot functions) and trace downward to leaf functions to understand where time is spent.
* Look for heavy usage in components such as the batch processor, exporters, or custom receivers/processors.
* Use heap and allocs data to correlate CPU activity with memory growth; goroutine and mutex profiles often reveal synchronization bottlenecks or leaks.
* Prioritize optimization on code paths that are both high-cost and frequently executed.

<Callout icon="warning">
  pprof endpoints can expose detailed runtime and stack information. Do not expose them to untrusted networks—restrict access with network controls (firewalls, port binding), or secure access methods (SSH tunnels, VPNs).
</Callout>

Links and references

* Go pprof documentation: [https://pkg.go.dev/net/http/pprof](https://pkg.go.dev/net/http/pprof)
* go tool pprof: [https://github.com/google/pprof](https://github.com/google/pprof)
* OpenTelemetry Collector repo: [https://github.com/open-telemetry/opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-collector)

This covers enabling pprof in the OpenTelemetry Collector, collecting runtime profiles, and basic analysis workflows to find CPU, memory, and concurrency issues.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/6b3d6ddd-0cd7-4b94-8e52-fb70c8b38d94" />
</CardGroup>


# Extensions zPages

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Extensions-zPages/page

zPages extension for OpenTelemetry Collector offering in-process HTTP debug pages for service, pipeline, extension, feature gates, and trace diagnostics

zPages provides quick, built-in, in-process diagnostic visibility for the OpenTelemetry Collector. Originally developed for gRPC at Google, zPages moved into OpenCensus and later into OpenTelemetry. Its core value remains: lightweight diagnostics served from inside the Collector process with no external backend required. In the Collector, zPages runs as an extension and exposes a small HTTP server with several helpful debug pages.

Enabling the zPages extension adds a diagnostics endpoint that listens inside the Collector process. Add the extension under the `extensions` section of your Collector configuration:

```yaml theme={null}
extensions:
  zpages:
    endpoint: "0.0.0.0:55679"
```

<Callout icon="lightbulb">
  zPages exposes in-process diagnostic web pages (servicez, pipelinez, extensionz, featurez, tracez) for quick operational visibility. It is not a metrics scrape endpoint like Prometheus. See the OpenTelemetry Collector documentation for extension configuration and security recommendations.
</Callout>

Key zPages you’ll commonly use:

| Page       | Purpose                                                                             | Typical path        |
| ---------- | ----------------------------------------------------------------------------------- | ------------------- |
| servicez   | Snapshot of the running Collector: build, version, runtime, OS, architecture        | `/debug/servicez`   |
| pipelinez  | Effective pipelines assembled by the Collector (receivers → processors → exporters) | `/debug/pipelinez`  |
| extensionz | List of enabled extensions (health\_check, pprof, zpages, etc.)                     | `/debug/extensionz` |
| featurez   | Feature gates and their states (alpha/beta/stable)                                  | `/debug/featurez`   |
| tracez     | Live spans and latency bucket samples produced inside the Collector                 | `/debug/tracez`     |

Service snapshot (servicez)
The servicez page gives a concise snapshot of the Collector build and runtime — useful to confirm the exact binary and runtime environment you’re troubleshooting.

<Frame>
  <img alt="The image displays a summary of service details for &#x22;otelcol-contrib,&#x22; including build and runtime information such as command, description, version, OS, and architecture. Links to Pipelines, Extensions, and Features are also shown." />
</Frame>

Pipelines (pipelinez)
The pipelinez page shows how the Collector assembled each pipeline for traces, metrics, and logs. Instead of parsing the config file, you can inspect the effective pipeline order — receivers, processors (memory\_limiter, attributes, batch, etc.), and exporters — which is especially useful for troubleshooting ordering or missing components.

<Frame>
  <img alt="The image shows a screenshot of built pipelines labeled &#x22;Inspecting Built Pipelines,&#x22; detailing the setup of receivers, processors, and exporters for logs, metrics, and traces." />
</Frame>

Extensions (extensionz)
The extensionz page lists currently enabled extensions (for example: `health_check`, `pprof`, `zpages`). Use this to confirm which auxiliary endpoints and runtime capabilities are active on your Collector instance.

<Frame>
  <img alt="The image shows a webpage titled &#x22;Checking Active Extensions,&#x22; displaying a list of extensions: health_check, pprof, and zpages. The URL indicates it's from an OpenTelemetry collector debug page." />
</Frame>

Feature gates (featurez)
Feature gates allow toggling experimental, deprecated, or upcoming features at runtime. The featurez page shows each gate’s description, release stage (alpha/beta/stable), and current state — helpful when verifying whether an experimental feature is enabled in your running Collector.

<Frame>
  <img alt="The image is a table titled &#x22;Feature Gates,&#x22; listing various technologies or functionalities with columns including ID, Enabled status, Description, Stage, Version information, and Reference URL. It is used to explore and manage different feature gates in software, detailing whether they are active and providing additional context." />
</Frame>

Trace sampling and latency (tracez)
The tracez page groups spans generated inside the Collector by latency buckets so you can quickly spot slow components. Latency buckets (for example, >10s) highlight problematic spans, making it easier to find exporter delays, retry behavior, or upstream errors. Trace samples show when the Collector sent, retried, or waited — invaluable for debugging delivery or exporter issues.

<Frame>
  <img alt="The image shows a table of trace spans with latency and error samples, alongside detailed logs indicating HTTP request failures and retry intervals." />
</Frame>

<Callout icon="warning">
  Do not expose zPages to untrusted networks. zPages reveals internal diagnostics that could disclose configuration and runtime details. Run the extension on localhost or protect it with network policies and authentication if accessible from broader networks.
</Callout>

References and further reading

* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* zPages (OpenTelemetry): [https://opentelemetry.io/docs/reference/specification/zpages/](https://opentelemetry.io/docs/reference/specification/zpages/)
* OpenTelemetry Collector configuration: [https://opentelemetry.io/docs/collector/configuration/](https://opentelemetry.io/docs/collector/configuration/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/e754077d-2077-452f-8926-1653a5a3e5f7" />
</CardGroup>
