# Implementing SLIs

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Service-Level-Objectives-and-Measurements/Implementing-SLIs/page

Guide to selecting, defining, and collecting service level indicators—availability, latency, errors, throughput, saturation—with Prometheus examples, instrumentation, and synthetic tests for user-focused reliability.

Service Level Indicators (SLIs) are the vital signs of your system — measurable signals that tell you whether users are getting the experience you promise. Choosing the right SLIs helps you detect problems quickly, prioritize fixes, and set meaningful reliability targets.

Think of picking SLIs like being a detective. Monitoring is your network of cameras and alarms that alert you when a specific condition happens. Observability is the forensic toolkit that lets you reconstruct what happened from traces, logs, and metrics.

<Frame>
  <img alt="A presentation slide titled &#x22;Choosing the Right SLI Tools for the Job&#x22; showing a house with a burglar, a security camera and a green &#x22;Observability&#x22; banner. To the right are icons and labels for &#x22;Footprints,&#x22; &#x22;Fingerprints,&#x22; and &#x22;Camera footage.&#x22;" />
</Frame>

Even if an incident unfolds in an unexpected way, good observability lets you recreate the story and act on it.

Not every service is measured the same way. There are five primary SLI categories to consider:

<Frame>
  <img alt="A presentation slide titled &#x22;Choosing the Right SLI Tools for the Job&#x22; that lists five numbered SLI categories: 01 Availability SLIs, 02 Latency SLIs, 03 Errors SLIs, 04 Throughput SLIs, and 05 Saturation SLIs." />
</Frame>

* Availability — percentage of requests successfully handled. Typical for APIs and web UIs.
* Latency — response time distribution; measure with percentiles, not averages.
* Errors — failure rate; be explicit about what counts as an error.
* Throughput — amount of work processed (requests/sec, items/min).
* Saturation — how close a resource is to its capacity (CPU, memory, queues).

<Callout icon="lightbulb">
  Select SLIs that map directly to user experience — if you measure the wrong thing, you’ll optimize in the wrong direction.
</Callout>

SLIs at a glance

| SLI Type     | What it measures                        | Common metric examples |
| ------------ | --------------------------------------- | ---------------------- |
| Availability | Fraction of valid requests that succeed | 2xx/total requests (%) |
| Latency      | Speed of responses (tail behavior)      | P95, P99 latency (s)   |
| Errors       | Fraction of failing requests            | 5xx rate (%)           |
| Throughput   | Work completed per time window          | requests/sec           |
| Saturation   | Resource usage relative to capacity     | CPU%, queue depth      |

Choosing the right SLI definition is critical. Small query mismatches (e.g., wrong label, wrong endpoint, or counting retries) can produce misleading SLIs and wrong decisions.

Prometheus / PromQL: common SLI query patterns

```promql theme={null}
