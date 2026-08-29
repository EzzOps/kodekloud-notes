# Timeouts Retries Idempotency

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Failure-Protection-and-Operations/Timeouts-Retries-Idempotency/page

How to design distributed systems using timeouts, retries with backoff and idempotency to safely handle network failures and avoid duplicate side effects

You know the feeling: you tap Pay, the spinner keeps spinning, and you aren't sure whether the payment went through. Tap again and you risk paying twice. Or maybe the payment never happened at all.

This article shows how to design distributed systems so the Pay button (and similar user actions) are safe to press more than once. We cover the three core tools you should combine: timeouts, retries with backoff, and idempotency.

All components in this design communicate via API calls, and every call crosses a network. Networks are inherently unreliable: calls can be lost, delayed, duplicated, or reordered. Robust systems anticipate these worst-case scenarios rather than assuming responses always arrive.

<Frame>
  <img alt="This image is a network diagram illustrating a digital transaction process involving a mobile device, load balancer, app server with cache, service, and database, all connected via APIs. It highlights the flow of information and the elements of data management in an online purchase scenario." />
</Frame>

A common mistake is to write code that assumes a response will always arrive. In distributed systems, “no response” is normal. From the caller’s perspective, a slow service and a dead service look the same: no reply. Since you generally cannot reliably distinguish the two, set clear timeouts and design behavior for timeout events.

## Timeouts

When your application server calls another service, it cannot wait forever. If the downstream service is slow or down, blocking indefinitely ties up threads, sockets, and other resources and causes requests to pile up. That slows the server and can eventually crash it.

Best practices for timeouts:

* Set a sensible per-call timeout (e.g., 1–5 seconds for user-facing APIs). Tune based on observed latency.
* Prefer short timeouts for synchronous user flows; allow longer timeouts for internal background workflows.
* Fail fast: when a timeout triggers, return a clear error so caller logic can decide to retry or take an alternate path.
* Propagate deadline information where possible (for example, include an explicit deadline header) so downstream services can respect caller expectations.

Example: pseudo-code showing a client call with a timeout.

```javascript theme={null}
// Pseudo-code (Node/Fetch-like)
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 2000); // 2s timeout

try {
  const resp = await fetch(url, { signal: controller.signal });
  // handle response
} catch (err) {
  // timeout or network error
} finally {
  clearTimeout(timeout);
}
```

Important: a timeout only stops the caller from waiting. It does not tell you whether the remote service completed the work. The request may have failed before reaching the service, or the service may have completed the work but its response was lost. Treat timeouts as "unknown" outcomes until you have an application-level mechanism (like idempotency or a transaction trace) to determine final state.

## Retries and Backoff

Many errors are transient: a short network blip, a DNS hiccup, or a service restart. Retrying failed calls can often recover automatically. But retries must be performed carefully.

<Frame>
  <img alt="The image is a flowchart illustrating a network process involving a user purchasing headphones for $10.00, with components like a load balancer, app server, service, cache, and database, highlighting a &#x22;network blip&#x22; issue." />
</Frame>

The dangerous pattern is immediate, aggressive retries from many callers. If a database or service is struggling and every client retries at once, retries amplify load and can push the system into complete failure — the classic retry storm.

> **warning** Do not retry blindly. Immediate repeated retries across many clients can worsen outages (retry storms). Limit retries and add backoff and jitter.

<Frame>
  <img alt="The image is a diagram showing a flow of data from a user's phone through a load balancer, app server, and service to a struggling database. It illustrates retries in a network architecture." />
</Frame>

Recommended retry pattern:

* Try immediately once (fast-fail).
* On failure, retry with exponential backoff (e.g., wait 1s, then 2s, then 4s).
* Add jitter (randomized small variance) to avoid synchronized retries across clients.
* Cap the maximum wait and the number of attempts (for example, max 5 tries).
* Only retry on transient errors (network errors, 5xx server errors). Avoid retrying on client errors like 4xx unless you know they are safe to retry.

Example exponential backoff with jitter (pseudo-code):

```python theme={null}
