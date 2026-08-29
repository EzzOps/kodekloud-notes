# Example usage:
sentences = [
    "First sentence.", "Second sentence.", "Third sentence.",
    "Fourth sentence.", "Fifth sentence."
]
chunks = chunk_sentences(sentences, chunk_size=2, overlap=1)
# chunks -> [
#  "First sentence. Second sentence.",
#  "Second sentence. Third sentence.",
#  "Third sentence. Fourth sentence.",
#  "Fourth sentence. Fifth sentence."
# ]
```

## When to consider alternatives

* Very short documents: Semantic chunking still applies; overlap may be unnecessary.
* Extremely long documents: Use hierarchical chunking—first split into sections, then paragraphs with overlap—to preserve high-level structure.
* Real-time or streaming ingestion: Use sliding windows or rolling buffers. Aim to respect semantic boundaries (e.g., sentence/paragraph fences) when possible to retain coherence.

## Validation and tuning

* Measure token counts with the embedding tokenizer to ensure chunks fit model limits.
* Sample retrieval results and run relevance/recall evaluations to confirm that chosen chunk size and overlap improve retrieval quality.
* Iterate: different corpora (legal text, scientific papers, code) will require different heuristics.

<Callout icon="lightbulb">
  When implementing chunking, always validate the chunks by checking token counts with the embedding model’s tokenizer and by sampling search results to ensure retrieval quality improves with your chosen chunk size and overlap.
</Callout>

## References and further reading

* tiktoken tokenizer: [https://github.com/openai/tiktoken](https://github.com/openai/tiktoken)
* Retrieval-Augmented Generation concepts: search for RAG architectures and embedding-based retrieval papers and blog posts for deeper guidance.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/6f4e345e-5e53-46cb-b940-10335c0a3355" />
</CardGroup>


# Ensuring Reliable Performance in Production LLM Deployments

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/Ensuring-Reliable-Performance-in-Production-LLM-Deployments/page

Guidance on achieving reliable, highly available production LLM deployments through comprehensive monitoring, alerting, observability, and incident response practices including metrics, tracing, logging, and canary testing.

Question 5.

Which component is most important for ensuring reliable performance when deploying an LLM in a production environment with high availability requirements?

* A monitoring system with automated alerts
* A detailed user manual
* Weekly backup schedules
* A feedback collection form

Answer: a monitoring system with automated alerts.

<Callout icon="lightbulb">
  A monitoring system with automated alerts is the single most important component for maintaining reliable performance and high availability in production LLM deployments. Observability gives real-time visibility into system health and enables proactive responses before end users are affected.
</Callout>

## Explanation

A robust monitoring and alerting platform provides immediate awareness of incidents and trends that affect availability, latency, and correctness. It should cover both the model-serving layer and the surrounding infrastructure.

Key observability capabilities to implement:

* Metrics collection: latency (p99/p95), throughput, error rates, and resource utilization (GPU/CPU/memory).
* Health checks: `liveness` and `readiness` probes for services so orchestrators can restart or reschedule unhealthy instances.
* Distributed tracing: track request flows to identify bottlenecks across microservices and external dependencies.
* Centralized logging: structured logs for diagnostics and root-cause analysis.
* Synthetic monitoring & canaries: run scripted checks and progressive rollouts to catch regressions before production impact.
* Automated alerting: severity levels, escalation paths, and integration with on-call tools (pager, SMS, Slack).
* Dashboards & SLOs: visualize trends, measure against service-level objectives (SLOs)/agreements (SLAs), and drive capacity planning.

### Quick comparison of the listed components

| Component            | Primary role for reliability                                                  | Why it is less critical than monitoring                                    |
| -------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Monitoring & alerts  | Detects incidents, trends; enables automated responses and on-call escalation | Essential for immediate detection and mitigation                           |
| Detailed user manual | Onboarding and human troubleshooting                                          | Helpful for humans, but not for real-time incident detection               |
| Weekly backups       | Data durability and disaster recovery                                         | Protects against data loss, but does not prevent outages or latency spikes |
| Feedback form        | Product improvement and user sentiment                                        | Asynchronous and reactive; not useful for immediate incident handling      |

## Why the other options don’t replace monitoring

* Detailed user manual: Important for support and handoffs, but cannot detect or resolve runtime failures.
* Weekly backups: Critical for recovery after catastrophic failure, but irrelevant to real-time availability or performance degradation.
* Feedback collection form: Valuable for product iteration, but feedback is delayed and cannot enable immediate remediation.

## Best practices for production LLM observability

* Combine monitoring with an incident response plan and concise runbooks so alerts trigger consistent, fast action.
* Instrument the entire stack: API gateway, model serving, feature stores, databases, and message queues.
* Implement auto-scaling and redundancy, and validate they operate correctly with metrics and alerts.
* Use canary deployments and synthetic checks to catch regressions early.
* Define SLOs and alert thresholds tied to business impact, not just raw metric thresholds.
* Automate common recovery actions (restarts, scale-outs, circuit breakers) where safe to reduce mean time to recovery (MTTR).

## Links and References

* [Prometheus monitoring](https://prometheus.io/) — metrics collection and alerting
* [Grafana](https://grafana.com/) — visualization and dashboards
* [OpenTelemetry](https://opentelemetry.io/) — tracing and telemetry instrumentation
* [SRE and SLO concepts](https://sre.google/sre-book/chapters/service-level-objectives/) — defining SLOs and alerting policies

<Callout icon="warning">
  Monitoring is necessary but not sufficient: it must be paired with clear on-call procedures, redundancy, automated recovery actions, and regular testing (canaries, chaos engineering) to truly achieve high availability.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/547b04cf-1e4b-45de-897e-3d5bd8c29e37" />
</CardGroup>
