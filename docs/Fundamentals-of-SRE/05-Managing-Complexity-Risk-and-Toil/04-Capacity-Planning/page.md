# Capacity Planning

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Managing-Complexity-Risk-and-Toil/Capacity-Planning/page

Capacity planning practices for forecasting, monitoring, and adjusting compute storage and network resources to prevent outages reduce costs and ensure reliable performance as demand grows.

Capacity planning is the practice of forecasting, provisioning, and monitoring the compute, storage, and network resources your services need so users stay happy as demand grows. Good capacity planning prevents outages, reduces latency, and avoids unnecessary cloud spend.

Imagine Black Friday: if you only react after alerts fire, it's already too late. Capacity planning answers one critical question: do you have enough resources now and in the future to serve users reliably? If not, you either overspend or fail under load.

<Frame>
  <img alt="A presentation slide titled &#x22;The Importance of Capacity Planning&#x22; showing resources flowing to a system with the caption &#x22;Capacity planning forecasts resources for reliable workload handling.&#x22; Below are three icons listing consequences: experience outages, degraded performance, and excessive costs." />
</Frame>

## Main components

Capacity planning is built from a few repeatable activities:

* Resource measurement — track CPU, memory, disk, network, and application-level metrics.
* Workload characterization — map request patterns, peaks, and steady-state behavior.
* Growth forecasting — predict future demand from historical trends and business drivers.
* Threshold management — define warnings and critical limits and the actions they trigger.
* Capacity adjustment — automate scaling and schedule planned provisioning.

<Frame>
  <img alt="A presentation slide titled &#x22;The Importance of Capacity Planning&#x22; showing a circular diagram with five key components — Resource Measurement, Workload Characterization, Growth Forecasting, Threshold Management, and Capacity Adjustment — around a central gear-and-person icon. Each component has a short description about tracking resources, understanding demand patterns, predicting growth, setting limits, and adjusting capacity." />
</Frame>

When implemented, these activities lead to fewer outages from resource exhaustion, lower cloud bills through right-sizing, improved support for business growth, better user experience, and more predictable budgeting.

<Frame>
  <img alt="A presentation slide titled &#x22;The Importance of Capacity Planning&#x22; that lists five benefits of effective capacity planning with simple circular-arrow icons and captions. The benefits shown include preventing outages, reducing costs, supporting business growth, improving user experience, and enabling predictable budgeting (© KodeKloud)." />
</Frame>

## Resource types and metrics

Track the resources that directly affect reliability and performance. Use the table below to decide what to collect, visualize, and alert on.

| Resource Type     | Key Metrics                                       | Typical Signals to Monitor                  |
| ----------------- | ------------------------------------------------- | ------------------------------------------- |
| Compute (CPU)     | Utilization %, load, runnable queue               | High sustained CPU -> scale, increase cores |
| Memory (RAM)      | Used %, page faults, swap                         | Rising usage -> OOM risk, memory leaks      |
| Storage (Disk)    | Used space %, IOPS, latency, throughput           | Fast growth -> add storage, tune retention  |
| Network           | Bandwidth, packets/sec, packet loss               | Saturation -> rate-limit, add capacity      |
| Database          | Query throughput, latency, connections            | Long queries/connection spikes -> scale DB  |
| API / Rate limits | Requests/sec, 4xx/5xx error rate, p95/p99 latency | Traffic bursts -> throttling or scaling     |

Collect these metrics consistently so forecasting, alerting, and scaling decisions can be data-driven.

<Frame>
  <img alt="A slide titled &#x22;Resource Measurement&#x22; showing a three-column table of resource types, descriptions, and key metrics. It lists rows for Compute (CPU), Memory, Storage, Network, Database, and API Rate Limits with brief descriptions and example metrics like utilization, IOPS, bandwidth, query throughput, and requests/sec." />
</Frame>

## Example metric signals

Real-world signals tell you when to act:

* PostgreSQL disk usage: 72% used, growing at 5% monthly — schedule additional storage or reduce retention.
* FastAPI memory: peaks at 90% during sales — investigate leaks or increase pod memory and HPA targets.
* Celery task queue: 10× normal load during peak — add workers or throttle producers.
* Loki log storage: 70% used, growing at 8% monthly — change retention or add storage.

These signals should feed into dashboards and alerts so you can act before users see problems.

<Frame>
  <img alt="A presentation slide titled &#x22;Resource Measurement: Understanding Resource Types and Metrics&#x22; showing four 3D cylinder charts for different resources. The cylinders show PostgreSQL disk space 72%, FastAPI memory usage 90% (peak), Celery task queue 1000% (10x normal load), and Loki log storage 70%." />
</Frame>

## Example topology metrics

Below is an example snapshot of per-component metrics from a sample application. Use this structure to feed dashboards, alerts, and capacity models.

```text theme={null}
KodeKloud Records Store
├─ API Service (FastAPI)
│  ├─ CPU: 40-60% average, 85% peak during high traffic
│  ├─ Memory: 70% average, 90% peak during sales
│  ├─ Network: 500 Mbps average, 1.2 Gbps peak
│  ├─ Connections: 2000/sec average, 5000/sec peak
│  └─ Response Time: 150ms average, 350ms during peak
├─ Database Connection
│  └─ PostgreSQL Database
│     ├─ CPU: 50% average, 90% peak during checkout rush
│     ├─ Memory: 75% average, 95% peak during sales
│     ├─ Disk: 72% used, growing at 5% per month
│     ├─ Connections: 200 average, 500 peak
│     └─ IOPS: 1000 average, 5000 peak during sales
├─ Background Processing
│  ├─ Celery Worker
│  │  ├─ CPU: 30% average, 80% peak during order processing
│  │  ├─ Memory: 60% average, 85% peak
│  │  └─ Task Queue: 200 tasks/min average, 2000 tasks/min peak
│  └─ RabbitMQ Message Queue
│     ├─ CPU: 25% average, 70% peak
│     ├─ Memory: 45% average, 80% peak
│     ├─ Disk: 30% used
│     └─ Queue Size: 500 messages average, 10,000 peak
└─ Observability Stack
   ├─ Prometheus (Metrics)
   │  ├─ CPU: 20% average, 40% peak
   │  ├─ Memory: 60% average, 75% peak
   │  └─ Disk: 65% used, growing at 3% per month
   ├─ Loki (Logs)
   │  ├─ CPU: 15% average, 35% peak
   │  ├─ Memory: 50% average, 70% peak
   │  └─ Disk: 70% used, growing at 8% per month
   └─ Jaeger (Tracing)
      ├─ CPU: 10% average, 30% peak
      ├─ Memory: 40% average, 65% peak
      └─ Disk: 45% used, growing at 2% per month
```

## Monitoring and visibility

Metrics only help when collected, stored, and visualized. Build dashboards that show trends (not just current values), wire alerts into incident workflows, and enable automated responders where safe. Without observability, forecasting and right-sizing are guesswork.

## Capacity forecasting

Forecasting uses historical signals and business context to predict future demand. Choose models that match observed behavior:

* Linear growth — steady increase tied to predictable user growth.
* Exponential growth — viral adoption or new product launches.
* Seasonal patterns — daily/weekly/holiday cycles.
* Step functions — sudden jumps after marketing pushes or launches.
* Combination models — mixtures of the above patterns.

Match your model to actual patterns for accurate capacity plans.

<Frame>
  <img alt="A slide titled &#x22;Forecasting Models&#x22; showing common growth patterns—with &#x22;Seasonal Patterns&#x22; at the top and four illustrated types (Exponential Growth, Linear Growth, Step Functions, Combination Models) arranged below, each with a colored icon and short description of how resources change over time." />
</Frame>

Example: database growth over 12 months

```text theme={null}
