# Choosing the Right Instrumentation Approach

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Choosing-the-Right-Instrumentation-Approach/page

Guide comparing auto, library, and manual OpenTelemetry instrumentation approaches and recommending a layered strategy to balance rapid visibility with deep business-context telemetry

There are multiple ways to instrument an application with OpenTelemetry. Choosing the right approach depends on your goals (speed to visibility, depth of business context, and engineering effort). This guide clarifies the common approaches, their trade-offs, and a recommended layered strategy for production-grade observability.

Start with zero-code (auto-)instrumentation. Language agents—such as the [Python](https://opentelemetry.io/docs/instrumentation/python/), [Java](https://opentelemetry.io/docs/instrumentation/java/), and [.NET](https://opentelemetry.io/docs/instrumentation/dotnet/) agents—can automatically capture spans from supported libraries without changing your source. This is the fastest, lowest-effort path to baseline telemetry because you typically don't need to modify application code.

<Frame>
  <img alt="The image outlines the benefits of zero-code auto-instrumentation, highlighting the use of language agents, quick data capture from libraries, and enhanced observability." />
</Frame>

Auto-instrumentation commonly captures HTTP requests, database calls, messaging interactions, and well-known web frameworks (for example, [Flask](https://flask.palletsprojects.com/) and [Spring](https://spring.io/projects/spring-framework)). It accelerates initial observability and helps you detect obvious performance issues and errors.

Where auto-instrumentation leaves gaps—such as business logic, complex asynchronous flows, or domain-specific operations—you should supplement it with manual, code-based instrumentation.

<Frame>
  <img alt="The image shows a titled presentation slide &#x22;Filling Gaps With Manual Instrumentation – Spans Added,&#x22; with three categories: Business logic, Async flows, and Domain-specific operations, each illustrated with icons." />
</Frame>

Manual instrumentation gives you precise control: create spans for business actions (for example, `validate insurance claim`, `calculate premium`), record meaningful attributes, log custom events, and build explicit span hierarchies that reflect your domain's control flow. This requires developer effort and access to the codebase, but it produces the richest, most actionable telemetry.

Another middle-ground option is library-based instrumentation. These are OpenTelemetry instrumentation packages that instrument specific third-party libraries for you (for example, `opentelemetry-instrumentation-flask`). They provide coverage for library-level interactions without requiring you to manually add spans around those calls.

<Frame>
  <img alt="The image explains three benefits of using library-based instrumentation: using OpenTelemetry (OTel) instrumentation libraries, easily getting spans from calls in libraries, and offloading the task of instrumenting popular libraries. An example provided is &#x22;opentelemetry-instrumentation-flask.&#x22;" />
</Frame>

Below is a concise comparison of the three approaches to help with decision-making.

| Method              | Code Changes Required                  | Typical Coverage                               | Visibility into Business Logic |   Setup Time | Best Use Cases                                                           |
| ------------------- | -------------------------------------- | ---------------------------------------------- | -----------------------------: | -----------: | ------------------------------------------------------------------------ |
| Zero-code (Auto)    | None (agent-based)                     | Broad (HTTP, DB, messaging, common frameworks) |                            Low |        Short | Rapid baseline telemetry, initial troubleshooting                        |
| Library-based       | Minimal (add instrumentation packages) | Focused on popular third-party libs            |                         Medium | Short–Medium | When a dependency needs better visibility without full manual spans      |
| Manual (Code-based) | Yes (developer effort)                 | Targeted, depends on implementation            |                           High |  Medium–Long | Business-critical flows, async control paths, domain-specific operations |

<Frame>
  <img alt="The image is a table comparing different instrumentation methods: Zero-Code, Library-Based, and Manual Code-Based, across various aspects such as code changes required, coverage, custom logic visibility, setup time, and suitability." />
</Frame>

Manual instrumentation requires engineering time and discipline (naming conventions, attribute standards, sampling considerations), but it provides essential context for domain-specific troubleshooting that auto-instrumentation cannot infer. Library-based instrumentation is a useful compromise: it offloads work for well-known libraries while still allowing targeted manual spans where needed.

In practice, the most effective strategy is layered:

* Enable zero-code auto-instrumentation first to get immediate, wide coverage and rapid feedback.
* Review traces to identify blind spots (missing business spans, confusing span hierarchies, or async gaps).
* Add targeted manual spans for business-critical logic and complex flows.
* Apply library-based instrumentation for third-party libraries that the agent doesn’t cover or where a library-specific implementation is preferable.

This layered approach balances ease of adoption against observability depth: auto-instrumentation gets you running quickly, library packages extend coverage for dependencies, and manual instrumentation provides the richest domain context.

<Frame>
  <img alt="The image depicts a balance scale illustrating the concept of &#x22;Balancing Ease vs. Depth,&#x22; with &#x22;Ease of Adoption&#x22; and &#x22;Observability Depth&#x22; on either side." />
</Frame>

<Callout icon="lightbulb">
  A practical cadence: enable auto-instrumentation, inspect traces to find coverage gaps, then add targeted manual or library-based instrumentation where business value or debugging needs justify the effort.
</Callout>

Further reading and references:

* [OpenTelemetry Instrumentation Overview](https://opentelemetry.io/docs/instrumentation/) — language-specific guides, agent docs, and library listings.
* Language docs (examples): [Python](https://opentelemetry.io/docs/instrumentation/python/), [Java](https://opentelemetry.io/docs/instrumentation/java/), [.NET](https://opentelemetry.io/docs/instrumentation/dotnet/).
* Instrumentation libraries (search for packages like `opentelemetry-instrumentation-*`) on the OpenTelemetry docs and package registries.

<Frame>
  <img alt="The image shows a list of references related to &#x22;Instrumentation Overview,&#x22; &#x22;Language-Specific Guides,&#x22; and &#x22;Instrumentation Libraries,&#x22; with links to various OpenTelemetry resources." />
</Frame>

That covers the core approaches to instrumentation and a practical way to combine them for fast, meaningful observability.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/c366a2e9-0dc6-4bfa-980d-1672fa6d6ad3" />
</CardGroup>
