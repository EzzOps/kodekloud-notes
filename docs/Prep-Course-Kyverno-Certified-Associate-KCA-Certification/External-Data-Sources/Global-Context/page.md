# List namespaces
kubectl get namespaces
NAME               STATUS   AGE
default            Active   75s
kube-flannel       Active   75s
kube-node-lease    Active   86s
kube-public        Active   87s
kube-system        Active   87s
kyverno            Active   57s

# Check Kyverno pods
kubectl get pods -n kyverno
NAME                                           READY   STATUS            RESTARTS   AGE
kyverno-admission-controller-5b789b5b-rq2f     0/1     PodInitializing   0          51s
kyverno-background-controller-5f89f696c9c9-5rf9 1/1     Running           0          51s
kyverno-cleanup-controller-84d58454-pbhsf      1/1     Running           0          51s
kyverno-reports-controller-87458444-qvhzf1     1/1     Running           0          51s
```

Quick policy example: enforce Pod Security baseline via a ClusterPolicy

```yaml theme={null}
# policy.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: podsecurity-subrule-baseline
spec:
  validationFailureAction: Enforce
  rules:
    - name: baseline
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        podSecurity:
          level: baseline
          version: latest
```

```bash theme={null}
# Apply and check policy
kubectl apply -f policy.yaml
clusterpolicy.kyverno.io/podsecurity-subrule-baseline created

kubectl get cpol
NAME                          ADMISSION   BACKGROUND   READY   AGE   MESSAGE
podsecurity-subrule-baseline  true        true         True    9s    Ready
```

To help you prepare for the KCA exam, this course includes mock exams modeled on the real test so you can measure readiness and build confidence.

By earning the KCA certification, you demonstrate knowledge of Kyverno’s architecture, the policy lifecycle, and advanced capabilities—skills that make you a valuable asset in modern Kubernetes environments.

Course roadmap overview

| Module                      | What you'll learn                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Introduction to Kyverno     | What Kyverno is, how it works, installation options, and policy structure.                                                     |
| Resource filtering          | Target resources precisely using `match`, `any`/`all`, `exclude`, and preconditions.                                           |
| Validation rules            | Build powerful `validate` policies with `patterns`, `deny` conditions, `forEach`, CEL expressions, and Pod Security sub-rules. |
| Mutation rules              | Modify resources using JSONPatch, strategic merge patches, and conditional anchors.                                            |
| Generate rules              | Automate resource creation (ConfigMap, NetworkPolicy, etc.) and keep resources synchronized.                                   |
| ImageVerify rules           | Verify container image signatures and attestations to secure the supply chain.                                                 |
| Policy exceptions & cleanup | Create PolicyException resources, cleanup unused resources, reporting, and Kyverno CLI usage.                                  |

Resource filtering example — target resources with `match` and `any`

```yaml theme={null}
match:
  any: # Match if Block 1 OR Block 2 is true
    - resources: # Block 1: Critical Deployments
        kinds:
          - Deployment
      selector:
        matchLabels:
          app: critical
    - resources: # Block 2: All StatefulSets
        kinds:
          - StatefulSet
```

Validate rules example — deny a container running as root using `securityContext`

```yaml theme={null}
spec:
  securityContext:
    runAsNonRoot: true
  containers:
    - name: bad-container
      securityContext:
        runAsNonRoot: false
```

Mutation and generate rules let you modify or create resources automatically. For example, a `generate` rule can create a NetworkPolicy or ConfigMap and keep it synchronized with a source resource:

```yaml theme={null}
spec:
  rules:
    - name: deny-all-traffic
      match:
        ...
      generate:
        synchronize: true
        ...
```

ImageVerify rules teach you how to verify container image signatures and attestations to strengthen your supply chain security—an increasingly important control in enterprise deployments.

<Frame>
  <img alt="The image shows a person speaking into a microphone with a list of topics under &#x22;Kyverno Certified Associate Curriculum&#x22; on the left. The topics include introductions, filters, rules validation, mutation, generation, ImageVerify Rules, and management." />
</Frame>

You will also learn to:

* Create PolicyException resources to exempt resources from specific policy rules.
* Use cleanup policies to remove orphaned or unused resources.
* Track compliance and generate reports using Kyverno reporting features.
* Use the Kyverno CLI to build, validate, and test policies locally before applying them to a cluster.

PolicyException example (exempt resources from specific policy rules)

```yaml theme={null}
apiVersion: kyverno.io/v2
kind: PolicyException
metadata:
  name: `exception-name`
  namespace: `exception-namespace`
spec:
  # 1. WHICH policy and rule(s) to bypass?
  exceptions:
    - policyName: `name-of-policy-to-exempt`
      ruleNames:
        - `name-of-rule-to-exempt`
  # 2. WHICH resource(s) get the exception?
  match:
    any:
      ...
  # 3. (Optional) Under WHAT extra conditions?
  conditions:
    any:
      ...
```

At KodeKloud, we foster an active learning community where you can ask questions, share insights, and collaborate with fellow learners—enhancing your hands-on experience.

<Callout icon="lightbulb">
  This course is hands-on: expect labs, real cluster exercises, and mock exams. Apply policies in a live environment to cement your understanding.
</Callout>

Are you ready to master Kyverno and become a Kubernetes Policy Expert?

Links and references

* Kyverno Documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kubernetes Documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* KCA Exam Overview: [https://kyverno.io/certification/](https://kyverno.io/certification/) (refer to the official Kyverno site for the latest exam details)
* KodeKloud courses and community: [https://www.kodekloud.com/](https://www.kodekloud.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/fbb5f757-2fb5-45db-89d9-93dca14f77b7/lesson/c7c73ceb-38b3-4300-94f0-b1e9331a8d18" />
</CardGroup>


# Global Context

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/External-Data-Sources/Global-Context/page

Explains Kyverno GlobalContextEntry caching to reduce API server load by caching Kubernetes resources or external API data for efficient policy evaluations.

Earlier, we learned how to fetch live data from ConfigMaps and directly from the Kubernetes API server. Those direct API call patterns are powerful, but they have a hidden cost: every time Kyverno evaluates a policy that performs a live API request, Kyverno makes a real-time call to the Kubernetes API server. In a busy cluster, a popular policy that fires on every Pod or Service change can generate hundreds or thousands of API requests and cause unnecessary load.

In this lesson we solve that performance problem using Kyverno's GlobalContextEntry resource: a configurable, cluster-scoped cache that lets you fetch data periodically or keep it updated in real time and then reference that cached data from many policies with near-zero evaluation cost.

Let's check back in with Alex.

Alex previously wrote a policy that lists Services to make a validation decision. It worked, but the policy became chatty: every Service create or update triggered an API call that listed all Services in the namespace. In a busy cluster this resulted in a huge spike in API server requests and noisy-neighbor behavior.

<Frame>
  <img alt="The image illustrates a flowchart titled &#x22;Alex's New Challenge,&#x22; depicting a situation where Alex and a Cloud Administrator are experiencing a huge spike in API server requests due to the &#x22;limit-lb-svc&#x22; policy, which makes an API call on every service creation or update in any namespace." />
</Frame>

Alex recognized that the data he needs—for example, the list of load-balancer Services—doesn't change every millisecond. The set of relevant Services is relatively stable. That suggests a better approach: fetch the data on a schedule (for example, once a minute), store it in a shared cache, and have policies read from that cache instead of making live API calls on every evaluation.

This is exactly what GlobalContextEntry is designed to solve.

Overview: how GlobalContextEntry works

* Create one or more GlobalContextEntry resources to declare the data Kyverno should cache and how to keep it updated.
* Reference the cache in policy rules using a `globalReference` inside the policy `context` block. Policies then read from Kyverno's in-memory cache instead of calling the API server on every evaluation.

This define-once, reference-many pattern dramatically reduces API traffic and improves policy evaluation performance.

There are two GlobalContextEntry types; choose based on your use case:

* kubernetesResource — informer-based, real-time caching of all resources of a single kind.
* apiCall — polling-based caching for filtered Kubernetes API queries or external services.

<Frame>
  <img alt="The image explains two types of GlobalContextEntry: &#x22;kubernetesResource&#x22; for caching Kubernetes resources, and &#x22;apiCall&#x22; for caching API call results." />
</Frame>

## kubernetesResource: informer-based, near-real-time cache

Use the `kubernetesResource` type when you need a complete, up-to-date cache of all objects of a single resource kind. Kyverno uses Kubernetes informers (the same mechanism used by controllers) so the cache is updated instantly on create, update, or delete. There is no polling interval and no staleness window.

Example — cache all Deployments in the `fitness` namespace:

```yaml theme={null}
apiVersion: kyverno.io/v2alpha1
kind: GlobalContextEntry
metadata:
  name: deployments
spec:
  kubernetesResource:
    group: apps
    version: v1
    resource: deployments
    namespace: fitness
```

If you omit the `namespace` field, Kyverno will cache deployments from all namespaces (cluster-wide).

When to use `kubernetesResource`:

* You need an always-up-to-date complete list of a resource kind.
* You prefer event-driven updates without polling.
* You want minimal staleness for policy decisions.

## apiCall: filtered Kubernetes queries or external APIs with refresh intervals

Use `apiCall` when you want to:

* Cache a filtered subset of Kubernetes resources (for example, only items with a certain label) to avoid storing thousands of irrelevant objects, or
* Cache data from an external service (HTTP/HTTPS) on a schedule.

Configure `apiCall` with either a `urlPath` (Kubernetes API query) or a `service` block (external URL), and set `refreshInterval` to control polling frequency.

Example — cache only Deployments in the `fitness` namespace with `app=blue`, refreshed every 10 seconds:

```yaml theme={null}
apiVersion: kyverno.io/v2alpha1
kind: GlobalContextEntry
metadata:
  name: blue-deployments
spec:
  apiCall:
    urlPath: "/[SECRET_REDACTED]?labelSelector=app=blue"
    refreshInterval: 10s
```

This entry polls the API every `refreshInterval`. The cached data can be up to that interval old — a trade-off that typically yields large performance gains when full real-time fidelity isn't required.

<Frame>
  <img alt="The image explains how to use the apiCall entry to filter Kubernetes resources before caching, highlighting its configuration, refresh scheduling, and optimal use cases." />
</Frame>

### External services and CA bundles

When the `service` block points to an internal HTTPS endpoint signed by a private Certificate Authority, include the CA certificate in the `caBundle` field so Kyverno can verify the service identity.

Example — call an internal HTTPS service every minute and include the CA bundle:

```yaml theme={null}
apiVersion: kyverno.io/v2alpha1
kind: GlobalContextEntry
metadata:
  name: redisdata
spec:
  apiCall:
    method: GET
    refreshInterval: 1m
    service:
      url: https://redis.myns.svc:6379
      caBundle: |-
        -----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----
```

<Callout icon="lightbulb">
  When using an internal HTTPS `service`, include the `caBundle` only if the service uses a private CA. Public CA-signed certificates do not require `caBundle`.
</Callout>

## Choosing the right type — quick comparison

|      Feature |              Use kubernetesResource              |                 Use apiCall                |
| -----------: | :----------------------------------------------: | :----------------------------------------: |
| Update model |              Informer (event-driven)             |         Polling (refresh interval)         |
|    Freshness |                  Near real-time                  |         Up to `refreshInterval` old        |
|        Scope | Full resource kind (optionally namespace-scoped) | Filtered queries or external API responses |
|     Best for |           Always-current resource lists          |    Filtered caches or external services    |

## Reference cached data in policies

After you create a GlobalContextEntry, reference it from a policy's `context` block using `globalReference`. The `name` must exactly match the GlobalContextEntry `metadata.name`. Use a [JMESPath](https://jmespath.org/) expression to extract or transform the cached data for your policy.

Example policy — deny Pod creation unless at least one Deployment exists in the `blue-deployments` cache:

```yaml theme={null}
rules:
- name: main-deployment-exists
  context:
  - name: deploymentCount
    globalReference:
      name: blue-deployments        # must match metadata.name of the GlobalContextEntry
      jmesPath: "length(@)"         # count items in the cached response
  match:
    any:
    - resources:
        kinds:
        - Pod
  validate:
    deny:
      conditions:
        any:
        - key: "{{ deploymentCount }}"
          operator: Equals
          value: 0
```

Notes on the example:

* The `deploymentCount` context variable receives the numeric result of the JMESPath `length(@)` expression.
* The `validate.deny` condition blocks Pod creation when `deploymentCount` equals `0`.

<Callout icon="lightbulb">
  The `name` under `globalReference` must exactly match the GlobalContextEntry `metadata.name`. Use JMESPath to shape the cached payload for your policy logic.
</Callout>

## Summary

Direct, synchronous API calls inside policy evaluations do not scale well. Kyverno's GlobalContextEntry provides a configurable, high-performance cache for both Kubernetes resources and external API data:

* Use `kubernetesResource` for informer-based, near-real-time caches of complete resource sets.
* Use `apiCall` for filtered Kubernetes queries or external service data on a poll schedule.

Define the cache once and reference it via `context.globalReference` in many policies for efficient, low-cost evaluations.

<Frame>
  <img alt="The image is a summary explaining two types of caches: &#x22;kubernetesResource&#x22; for real-time informer-based caching, and &#x22;apiCall&#x22; for periodically refreshed external data caches, along with usage instructions." />
</Frame>

That's it for this lesson.

Links and references

* Kyverno Global context and external data: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* JMESPath query language: [https://jmespath.org/](https://jmespath.org/)
* Kubernetes informers (controller pattern): [https://kubernetes.io/docs/reference/using-api/api-concepts/#watch-operations](https://kubernetes.io/docs/reference/using-api/api-concepts/#watch-operations)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/470bb961-febf-41b6-b75b-4c439def6eae/lesson/8f3ed83d-5b87-440c-88e6-c69509e7c582" />
</CardGroup>
