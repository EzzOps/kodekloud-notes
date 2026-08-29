# Extensions healthcheck

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Extensions-healthcheck/page

Describes the OpenTelemetry Collector health_check extension that provides an HTTP health endpoint for monitoring, load balancer probes, and Kubernetes liveness and readiness checks

The health check extension provides a lightweight HTTP endpoint that confirms whether the OpenTelemetry Collector process is up and responding. When enabled, the endpoint returns a 200 OK and a small JSON payload with status, `upSince`, and `uptime` — making it ideal for monitoring, load balancer probes, and orchestration systems.

<Frame>
  <img alt="The image has a blue gradient background with the text &#x22;Collector Diagnostics&#x22; and &#x22;Extensions: healthcheck&#x22; in white, along with a copyright notice for KodeKloud." />
</Frame>

## Enable the health\_check extension

Add the `health_check` extension to your collector configuration and bind it to the default address and port (0.0.0.0:13133):

```yaml theme={null}
extensions:
  health_check:
    endpoint: "0.0.0.0:13133"  # GET / returns 200 OK when healthy
service:
  extensions: [health_check]  # ensure it is enabled under service
```

## Verify the endpoint with curl

A GET request to `/` returns HTTP 200 and a JSON body describing server availability:

```bash theme={null}
curl -i http://localhost:13133/
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 118

{
  "status": "Server available",
  "upSince": "2025-09-18T12:41:48.996342661Z",
  "uptime": "2m41.853715676s"
}
```

<Callout icon="lightbulb">
  The extension listens by default on port 13133. You can use this endpoint in health checks, load balancer probes, or external orchestration tools to decide rollout and restart behavior.
</Callout>

## Kubernetes: map to liveness and readiness probes

Use the health endpoint for Kubernetes liveness and readiness checks so the platform can detect and recover from unhealthy collector instances:

```yaml theme={null}
livenessProbe:
  httpGet:
    path: "/"
    port: 13133
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: "/"
    port: 13133
  initialDelaySeconds: 5
  periodSeconds: 5
```

Probes summary:

| Probe type | Purpose                                                           | Example                     |
| ---------- | ----------------------------------------------------------------- | --------------------------- |
| Liveness   | Restart container when collector is unresponsive                  | `livenessProbe` YAML above  |
| Readiness  | Exclude pod from service load balancer while starting/rehydrating | `readinessProbe` YAML above |

## Docker / Docker Compose

For Docker or Docker Compose deployments, expose the collector port so external systems (host, orchestrator, CI) can poll the endpoint:

```yaml theme={null}
services:
  otelcol:
    image: otel/opentelemetry-collector:latest
    ports:
      - "13133:13133"
```

External systems can poll `http://<host>:13133/` for a quick health signal and use the 200 OK response for rollout, restart, or monitoring decisions.

## When to use the healthcheck extension

* Integrate with Kubernetes probes (liveness & readiness).
* Configure load balancer health checks to avoid routing traffic to an unavailable collector.
* Use in CI/CD pipelines or deployment scripts to gate rollouts on collector availability.
* Provide a simple browser-accessible endpoint for quick diagnostic checks.

## Links and references

* [OpenTelemetry Collector — Extensions](https://opentelemetry.io/docs/collector/architecture/#extensions)
* [Kubernetes Probes — Liveness and Readiness](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
* [Docker Compose — Expose ports](https://docs.docker.com/compose/compose-file/compose-file-v3/#ports)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/c28a78c1-76d1-405d-af1a-6c458dbda94b" />
</CardGroup>
