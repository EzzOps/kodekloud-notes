# Failure Handling Pattern for High Availability LLM Deployment Python

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/Failure-Handling-Pattern-for-High-Availability-LLM-Deployment-Python/page

Explains using the circuit breaker pattern in Python to protect LLM deployments, preventing cascading failures, enabling fallbacks, retries, and recovery with observability and configuration guidance.

This is question 12.

When implementing a Python script to deploy an LLM that must remain highly available, which pattern is most appropriate for handling potential failures?

* The circuit breaker pattern
* The decorator pattern
* The iterator pattern
* The builder pattern

Answer: the circuit breaker pattern

The circuit breaker pattern is the recommended approach for protecting the overall system from repeated failures of a single component (for example, an LLM inference endpoint). It monitors calls, trips when failures exceed a threshold, and prevents further calls until the service has a chance to recover. This prevents cascading failures, conserves resources, and enables graceful degradation.

<Frame>
  <img alt="The image shows a question about deploying an LLM with high availability, recommending the circuit breaker pattern for handling potential failures. It explains the pattern's function in managing system stability." />
</Frame>

## Why the circuit breaker is best for LLM deployments

* Prevents cascading failures by short-circuiting repeated failing calls (for example, when an LLM endpoint is rate-limited, overloaded, or returning errors).
* Conserves scarce resources (threads, sockets, GPU slots) that would otherwise be tied up retrying doomed requests.
* Enables graceful degradation: while the breaker is open you can return cached responses, fallback to a smaller model, or provide an informative error to the user.
* Supports recovery: after a timeout the breaker transitions to half-open to probe the backend; successful probes close the breaker again.

## Typical circuit breaker states

* Closed: Requests proceed normally; failures are counted.
* Open: Requests are blocked (fast-fail or fallback) once failures exceed thresholds.
* Half-open: A limited number of trial requests are allowed; successes close the breaker, failures re-open it.

## Recommended implementation considerations for LLM deployments

* Set failure thresholds and reset timeouts based on provider SLAs and observed latency/failure patterns.
* Combine circuit breakers with exponential backoff and limited retries for transient errors.
* Instrument the breaker with metrics and logs (failure counts, state transitions, latencies) and expose those metrics to your monitoring stack.
* Implement fallback strategies: cached responses, a degraded model, explicit user guidance, or a retry endpoint.
* Use health checks to detect and restore healthy model instances, and to drive intelligent routing decisions.

## Quick comparison: patterns and relevance

|         Pattern | Primary purpose                                           | Relevance to failure isolation in LLM deployments               |
| --------------: | --------------------------------------------------------- | --------------------------------------------------------------- |
| Circuit Breaker | Isolate failing components and prevent cascading failures | Highly relevant — provides trip semantics and recovery probing  |
|       Decorator | Add responsibilities to objects (logging, retries)        | Useful for augmenting behavior but not sufficient for isolation |
|        Iterator | Traverse collections                                      | Not applicable to availability or failure handling              |
|         Builder | Construct complex objects step-by-step                    | Not related to runtime failure handling                         |

## Example (using the pybreaker library)

The example below shows a simple circuit breaker around an LLM client call. It demonstrates tripping after a configurable number of failures, using a fallback when the breaker is open, and integrating a basic retry/backoff scheme for transient errors.

```python theme={null}
from pybreaker import CircuitBreaker, CircuitBreakerError
import time
import random
