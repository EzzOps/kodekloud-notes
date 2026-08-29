# Demo AnalysisTemplate

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Demo-AnalysisTemplate/page

Guide to creating and using Argo Rollouts AnalysisTemplate for runtime analysis during progressive delivery, defining metrics, providers, arguments, conditions, and example manifests.

This lesson shows how to create an Argo Rollouts AnalysisTemplate — the reusable resource that defines how to perform runtime analysis during progressive delivery. AnalysisTemplates specify which metrics to collect, how often to collect them, how many samples to take, and what constitutes success or failure. They can accept runtime arguments (including secrets) so Rollouts can pass contextual values into the template.

Below is a minimal AnalysisTemplate manifest showing the resource kind and metadata:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: http-health-check
  namespace: argo-analysis-lab
spec: {}
```

AnalysisTemplates can be namespaced (as shown above) or cluster-scoped. Cluster-level templates use the same API but are available to Rollouts across the cluster.

## Template arguments (args)

AnalysisTemplates accept args (input parameters) that Rollouts supply at runtime. An arg can be required (no default) or optional (with a default value). Args can also be populated from Kubernetes Secrets using `valueFrom.secretKeyRef`.

Example of args and metrics declared in an AnalysisTemplate:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: args-example
spec:
  args:
    # required in Rollout due to no default value
    - name: service-name
    - name: stable-hash
    - name: latest-hash
    # optional in Rollout given the default value
    - name: api-url
      value: http://example/measure
    # from secret
    - name: api-token
      valueFrom:
        secretKeyRef:
          name: token-secret
          key: apiToken

  metrics:
    - name: webmetric
      successCondition: result == 'true'
      provider:
        # provider config here
```

To reference an argument inside the template use the `args` namespace, for example `{{ args.service-name }}`.

> **lightbulb** Arguments are substituted at runtime using the template expression `{{ args.<name> }}`. Ensure the argument names in your Rollout match exactly those declared in the AnalysisTemplate.

## Metrics, providers, and conditions

The core of an AnalysisTemplate is the `metrics` list. Each metric declares:

* A name
* A sampling cadence (`interval`)
* How many samples (`count`) or an allowed number of failures (`failureLimit`)
* A `successCondition` and optional `failureCondition` to evaluate the provider result
* A provider (Prometheus, Datadog, New Relic, Job, Web/HTTP, CloudWatch, etc.)

The provider block defines how the metric is measured (query, HTTP call, job execution, etc.). The `successCondition` and `failureCondition` receive a `result` object whose structure depends on the provider (for web, `result.code` is HTTP status; for Prometheus, `result` is typically a vector/array).

Common providers at a glance:

| Provider                         | Use Case                                            | Key result field                                             |
| -------------------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| Prometheus                       | Query metrics and SLI-style checks                  | `result` (array/vector, often indexed like `result[0]`)      |
| Web (HTTP)                       | Call HTTP endpoints (health, readiness, custom API) | `result.code`, `result.body`, JSON extraction via `jsonPath` |
| Job                              | Run a Kubernetes Job to compute or validate results | Job exit code / logs                                         |
| Datadog / New Relic / CloudWatch | Provider-specific metric queries                    | Provider-specific `result` fields                            |

### Prometheus provider example

Prometheus query results are returned in vector form, so you typically index into `result` (for example `result[0]`) when writing `successCondition`.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 5m
      # NOTE: prometheus queries return results in vector form.
      # So it is common to access index 0 of the returned array to obtain the scalar.
      successCondition: result[0] >= 0.95
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.example.com:9090
          # timeout is expressed in seconds
          timeout: 40
          headers:
            - key: X-Scope-OrgID
              value: tenant_a
          query: |
            sum(irate(
              istio_requests_total{reporter="source",destination_service=~"{{ args.service-name }}",response_code=~"2.."}[5m]
            )) /
            sum(irate(
              istio_requests_total{reporter="source",destination_service=~"{{ args.service-name }}"}[5m]
            ))
```

Hints:

* Use `failureLimit` to allow a small number of failing samples before the analysis fails.
* Choose `interval` to balance responsiveness with query load.

### Web (HTTP) provider example

The web provider performs HTTP requests to gather a measurement. You can configure the URL, HTTP method, headers, timeout, and optional JSON path to extract values from the response body.

```yaml theme={null}
metrics:
  - name: webmetric
    successCondition: result == 'true'
    provider:
      web:
        url: "http://my-server.com/api/v1/measurement?service={{ args.service-name }}"
        timeoutSeconds: 20 # defaults to 10 seconds
        headers:
          - key: Authorization
            value: "Bearer {{ args.api-token }}"
        jsonPath: "{$.data.ok}"
```

Notes:

* Use `jsonPath` to extract a specific value from JSON responses; the extracted value becomes `result`.
* `timeoutSeconds` defaults to 10s unless overridden.

## Example: HTTP health-check AnalysisTemplate

This complete AnalysisTemplate uses the web provider to call a service `/health` endpoint. It runs 3 probes at 5-second intervals and treats any 2xx HTTP status as success.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: http-health-check
  namespace: argo-analysis-lab
spec:
  args:
    - name: service-name
  metrics:
    - name: health-check
      interval: 5s
      count: 3
      provider:
        web:
          method: GET
          url: http://{{ args.service-name }}.argo-analysis-lab.svc.cluster.local/health
      successCondition: result.code >= 200 && result.code < 300
```

Key details:

* `count: 3` — the probe will be executed three times.
* `interval: 5s` — delay between successive probes.
* `successCondition` — for the web provider, `result.code` contains the HTTP response status code.

> **lightbulb** Use `count` and `interval` to control sample size and cadence. Collecting multiple samples helps smooth out transient failures and reduces flakiness in progressive rollouts.

## Create the AnalysisTemplate

Apply the manifest to create the AnalysisTemplate in the target namespace:

```bash theme={null}
kubectl -n argo-analysis-lab apply -f https://gist.githubusercontent.com/sidd-harth/07d93e0a96d0dc1e1601def53d0aa42b/raw/6f9acdf21b0297ea3b5110e37dc32a1e8a3988c0/health-check-analysis-template.yml
```

Expected response:

```bash theme={null}
analysistemplate.argoproj.io/http-health-check created
```

Verify the template exists:

```bash theme={null}
kubectl -n argo-analysis-lab get analysistemplate
```

Example output:

```bash theme={null}
NAME               AGE
http-health-check  11s
```

Describe the template to inspect args and metrics:

```bash theme={null}
kubectl -n argo-analysis-lab describe analysistemplate http-health-check
```

Relevant fields in the describe output (formatted for clarity):

```text theme={null}
Name:         http-health-check
Namespace:    argo-analysis-lab
API Version:  argoproj.io/v1alpha1
Kind:         AnalysisTemplate
Spec:
  Args:
    Name: service-name
  Metrics:
    Name:     health-check
    Interval: 5s
    Count:    3
    Provider:
      Web:
        Method: GET
        URL: http://{{ args.service-name }}.argo-analysis-lab.svc.cluster.local/health
    Success Condition: result.code >= 200 && result.code < 300
```

Now the AnalysisTemplate exists and is ready to be referenced by a Rollout in this namespace. Wire the template into a Rollout's analysis section to execute these checks as part of a progressive delivery strategy.

## Links and references

* [Argo Rollouts Documentation](https://argoproj.github.io/argo-rollouts/)
* [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
* [Kubernetes API Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

For additional examples and provider details, consult the Argo Rollouts AnalysisTemplates guide in the official documentation.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/621a0306-7c3c-42d3-aad2-5431d3a97848)
