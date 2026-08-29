# Span Links

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Links/page

Explains span links in distributed tracing and OpenTelemetry, showing how to associate independent asynchronous or parallel spans for correlated tracing and practical use cases.

In distributed tracing, span links let you express relationships between spans that are related but not in a direct parent-child hierarchy. This lesson explains what span links are, how they differ from parent-child spans, when to use them, and how to create them with OpenTelemetry.

What you will learn:

* Definition and motivation for span links
* Common async and parallel scenarios where links matter
* Key differences vs. parent-child spans
* OpenTelemetry Link usage with a code example
* Practical use cases and best practices

Span links connect independent spans that share context or relevance, even when those spans start separately, run asynchronously, or execute in parallel. This is critical for tracing real-world, message-driven, or batch-oriented systems.

<Frame>
  <img alt="The image explains &#x22;Span Links,&#x22; showing a connection between &#x22;Span A&#x22; and &#x22;Span B&#x22; to illustrate links between related but separate activities." />
</Frame>

## Why span links matter

Traditional tracing models a strict parent → child call hierarchy. But modern systems frequently:

* Execute work asynchronously (e.g., tasks enqueued and processed later)
* Run parallel workers for a single logical job
* Use message brokers where producer and consumer are independent processes

Span links capture associations between those independent activities so you can query, visualize, and analyze work that shares a trigger or context without requiring a synchronous parent-child relationship.

<Frame>
  <img alt="The image titled &#x22;Why Span Links Matter&#x22; explains that activities can run parallelly or asynchronously, and includes relevant icons for each concept." />
</Frame>

## Example scenario

* A user places an order on an e-commerce site. The front-end service creates an `order-confirmation` span for the incoming request.
* The order processing service publishes messages to a queue for downstream consumers.
* Separate consumers independently process those messages: one sends the confirmation email, another updates inventory.
* The email and inventory spans are not children of the original order-confirmation span (they run in different processes), but they are logically tied to the same order.

Span links let each consumer span reference the originating order span so traces can be correlated even when spans are created independently.

<Frame>
  <img alt="The image illustrates a process flow involving &#x22;Span Links in Action,&#x22; where an order confirmation service sends an email and updates inventory, demonstrated with a simple diagram." />
</Frame>

## Batch, asynchronous, and parallel processing

Common patterns that benefit from links:

* Batch jobs / Map-Reduce: multiple worker spans handle partitions of a job; links relate each worker to the initiating job span.
* Message aggregation: combine results from several messages into a single aggregate result; link each message-processing span to the aggregator span.
* Transactional messaging & event sourcing: relate event-processing spans and participating messages back to a transaction or final entity state.

These patterns often produce spans that cannot be modeled as synchronous parent/child, but still require a way to associate related work.

<Frame>
  <img alt="The image compares &#x22;Parent-Child&#x22; and &#x22;Span Links&#x22; models, highlighting their characteristics and providing diagrams to illustrate both relationships in processes." />
</Frame>

## Key differences

* Parent-child spans:
  * Represent a strict hierarchy and direct cause/effect.
  * Child spans typically inherit context from the parent.
  * Useful for synchronous request/response call chains.

* Span links:
  * Represent loose contextual associations between independently started spans.
  * Spans may be created in different processes, at different times, or in parallel.
  * Useful for async processing, queues, event-driven flows, and batch work.

Use span links when you need to associate work that shares context or a common trigger but cannot (or should not) use a direct parent-child relationship.

<Frame>
  <img alt="The image describes &#x22;Span Links in Complex Systems,&#x22; outlining three aspects: Asynchronous Workflows, Microservice Communication, and Batch Processing, each with a brief explanation of their function." />
</Frame>

## OpenTelemetry: the Link concept

OpenTelemetry exposes a Link construct to attach a span context (and optional attributes) to a newly created span. A Link typically contains the target span context and metadata such as an `order.id` or `message.id`. Links are recorded on the new span and allow backends to correlate traces and perform richer analysis.

Example (Python, OpenTelemetry):

```python theme={null}
from opentelemetry import trace
from opentelemetry.trace import Link, SpanContext, TraceFlags, TraceState

tracer = trace.get_tracer(__name__)
