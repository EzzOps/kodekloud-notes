# main.py
def hello_http(request):
    name = request.args.get('name') or request.get_json(silent=True).get('name', 'World')
    return f'Hello {name}!', 200
```

Deploy example (gcloud CLI, HTTP-triggered):

```bash theme={null}
gcloud functions deploy helloHttp \
  --runtime nodejs18 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point helloHttp
```

Use Pub/Sub or Storage triggers similarly by specifying `--trigger-topic` or `--trigger-bucket` during deployment.

## Quick exam-style question

Which billing model does Cloud Functions use?

1. Pay for servers running 24/7.
2. Pay per use only when your code executes.
3. Monthly subscription, regardless of usage.

Correct answer: option 2 — pay per use only when your Cloud Function executes. This billing model reduces cost by eliminating charges for idle compute.

## Summary

Cloud Functions offers lightweight, event-driven compute that scales automatically and removes the burden of server management. Use Cloud Functions for small, focused units of logic that respond to events; rely on external services for persistent state.

Topics to explore next:

* Performance characteristics and cold-start behavior
* Data-processing design patterns with Cloud Functions
* Rate limiting, batching, and retry strategies
* When to choose Cloud Functions vs. Cloud Run or Workflows

## Links and references

* [Cloud Functions documentation](https://cloud.google.com/functions/docs)
* [Cloud Functions runtime support](https://cloud.google.com/functions/docs/concepts/runtime-support)
* [Google Cloud Storage events](https://cloud.google.com/storage/docs/pubsub-notifications)
* [Pub/Sub documentation](https://cloud.google.com/pubsub/docs)

That is it for this lesson. Speak with you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/25c01a5c-5482-47e9-b2b3-da9cfbd0e1de" />
</CardGroup>


# Cloud Functions vs Cloud Workflows

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Orchestration-Options/Cloud-Functions-vs-Cloud-Workflows/page

Comparison of Google Cloud Functions and Cloud Workflows to help choose between short-lived event handlers and long-running, stateful orchestrations coordinating multiple services with retries and branching

Welcome back. This lesson compares Cloud Functions and Cloud Workflows so you can choose the right orchestration approach for event-driven applications on Google Cloud. We build on Cloud Functions best practices and optimization techniques and expand the perspective to multi-service coordination, long-running sequences, and stateful orchestrations.

Quick overview:

* Use Cloud Functions for single-purpose, short-lived event handlers.
* Use Cloud Workflows when you need to coordinate multiple steps, persist state across steps, or run long-running processes.

## Key differences: execution model, duration, and control flow

| Aspect                   | Cloud Functions                                                                                                    | Cloud Workflows                                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| Execution model          | Event-driven, stateless functions that react to a single trigger and finish                                        | Orchestrator that sequences multiple steps, passes data between steps, and coordinates services                 |
| Duration                 | Short-lived tasks (minutes). Newer runtimes may allow longer timeouts, but Functions are optimized for short tasks | Designed for long-running orchestrations; can wait, pause, or span hours/days                                   |
| Control flow             | Simple single-purpose logic; any branching or complex flow must be managed by the function code                    | Built-in branching, error handling, retries, and conditional logic defined in YAML or JSON workflow definitions |
| State management         | No built-in state — persist externally (Cloud Storage, Firestore, database)                                        | State passing between steps and execution history are built-in                                                  |
| Error handling & retries | Basic retry behavior via trigger configuration or custom retry logic in code                                       | Advanced retry policies, conditional error handling, and explicit fallback paths in workflow definitions        |
| Pricing model            | Billed for invocations, compute time, and resources used                                                           | Billed per state transition/step and for certain callouts; pricing units differ from Functions                  |
| Typical use cases        | Microservices, single-event responses (e.g., transform/store a file on upload)                                     | Orchestrations spanning multiple APIs/services, long-running flows, and processes requiring approvals           |

<Frame>
  <img alt="A slide titled &#x22;Service Comparison Matrix&#x22; showing a table that compares Cloud Functions and Cloud Workflows across aspects like execution model, duration, complexity, state management, error handling, pricing, and use cases. The matrix contrasts event-driven, short-lived, stateless functions with stateful, long-running, multi-step workflows." />
</Frame>

## Duration and state: when time and persistence matter

* Cloud Functions: best for tasks that complete quickly. For persistent data, rely on external stores (Cloud Storage, Firestore, Cloud SQL).
* Cloud Workflows: maintain execution context across steps; outputs flow into subsequent steps without needing an external store for intermediate state.

## Complexity and orchestration

* Cloud Functions: keep functions focused and stateless. Suitable for simple event handlers or small microservices.
* Cloud Workflows: model complex business processes (branching, parallel steps, waits for approvals, external API calls) declaratively in a workflow definition.

## Error handling and retries

* Cloud Functions: rely on trigger-level retries or custom retry logic inside the function.
* Cloud Workflows: define retry policies, backoff, and alternate paths in the workflow. Useful for resilient, multi-step integrations.

## Pricing considerations

Both are usage-based but charge on different metrics. Evaluate expected invocation counts, compute duration (Functions), and number of state transitions/callouts (Workflows) to estimate costs for your scenario. See [Cloud Functions pricing](https://cloud.google.com/functions/pricing) and [Cloud Workflows pricing](https://cloud.google.com/workflows/pricing) for current details.

## Typical use cases and examples

| Service         | Example use cases                                                                                                                                                                                                                                                                  |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cloud Functions | - Image or file processing upon upload to Cloud Storage<br />- Lightweight API backends or webhook handlers<br />- Event-driven microservices (single responsibility)                                                                                                              |
| Cloud Workflows | - Multi-step onboarding with document checks, ID verification, manual approvals, and external API calls<br />- Orchestrating a transaction across several services with retries and compensating actions<br />- Long-lived ETL pipelines that require coordination and checkpoints |

Example scenarios:

* Cloud Function: calculate an estimated fare and assign a nearby driver when a ride request arrives — one trigger, one responsibility, short execution.
* Cloud Workflow: a driver onboarding process that collects documents, verifies IDs, waits for human approval, and activates accounts — many steps, branching paths, and waits.

## Exam-style question

What would you choose for a long-running process involving multiple GCP APIs where state must be maintained?

Answer: Cloud Workflows — they are designed to orchestrate steps, persist execution state between steps, and provide rich error handling and retry strategies.

<Callout icon="lightbulb">
  Simple decision rule: ask yourself “Do I need just a single event response?” If yes, Cloud Functions are usually the right fit. If no — if you need orchestration, retries, multiple API calls, or long-running stateful sequences — choose Cloud Workflows.
</Callout>

## Decision guidance

* Choose Cloud Functions when: you need a fast, single-purpose event response, minimal orchestration, and stateless execution.
* Choose Cloud Workflows when: you need to coordinate multiple steps, preserve state across steps, implement complex branching or retry policies, or support long-running processes.

A consolidated visual decision flow can help guide the choice below.

<Frame>
  <img alt="A simple decision flowchart titled &#x22;Decision Flowchart – When to Use Which Service&#x22; showing a diamond labeled &#x22;Single Event Response?&#x22; With &#x22;Yes&#x22; it leads to a blue box &#x22;Cloud Functions — Event-driven,&#x22; and with &#x22;No&#x22; it leads to an orange box &#x22;Cloud Workflows — Orchestration.&#x22;" />
</Frame>

Further reading and references:

* [Cloud Functions documentation](https://cloud.google.com/functions/docs)
* [Cloud Workflows documentation](https://cloud.google.com/workflows/docs)
* [Choosing between serverless compute and orchestration patterns](https://cloud.google.com/architecture)

See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/534e3ba4-05aa-49f1-980a-4eb9cb15016d" />
</CardGroup>
