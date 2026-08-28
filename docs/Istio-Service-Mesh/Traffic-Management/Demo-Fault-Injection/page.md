# Reviews service
apiVersion: v1
kind: Service
metadata:
  name: reviews
  labels:
    app: reviews
    service: reviews
    test: beta
spec:
  ports:
    - port: 9080
      name: http
  selector:
    app: reviews
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: bookinfo-reviews
  labels:
    app: reviews
    account: reviews
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reviews-v1
  labels:
    app: reviews
    version: v1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: reviews
```

After updating the reviews service, add the same label to the Version V2 and Version V3 deployments. For instance, the deployment for Version V3 with the updated label is as follows:

```yaml theme={null}
selector:
  matchLabels:
    app: reviews
    version: v3
    test: beta
template:
  metadata:
    labels:
      app: reviews
      version: v3
      test: beta
  spec:
    serviceAccountName: bookinfo-reviews
    containers:
      - name: reviews
        image: docker.io/istio/examples-bookinfo-reviews-v3:1.16.2
        imagePullPolicy: IfNotPresent
        env:
          - name: LOG_DIR
            value: "/tmp/logs"
        ports:
          - containerPort: 9080
        volumeMounts:
          - name: tmp
            mountPath: /tmp
          - name: wlp-output
            mountPath: /opt/ibm/wlp/output
        securityContext:
          runAsUser: 1000
    volumes:
      - name: wlp-output
        emptyDir: {}
      - name: tmp
        emptyDir: {}
```

### Step 3: Apply Changes

After modifying the YAML file, delete the existing configuration and reapply the updated changes:

```bash theme={null}
istiotraining@local istio-1.10.3 $ vi reviews.yaml
istiotraining@local istio-1.10.3 $ kubectl delete -f reviews.yaml
service "reviews" deleted
serviceaccount "bookinfo-reviews" deleted
deployment.apps "reviews-v1" deleted
deployment.apps "reviews-v2" deleted
deployment.apps "reviews-v3" deleted
istiotraining@local istio-1.10.3 $ kube
```

<Frame>
  ![The image shows a Kiali Console interface displaying a list of workloads in the "default" namespace, each labeled with its name, type, and version. The sidebar includes options like Overview, Graph, Applications, Workloads, Services, and Istio Config.](https://kodekloud.com/kk-media/image/upload/v1752879387/notes-assets/images/Istio-Service-Mesh-Demo-Destination-Rules/kiali-console-workloads-default-namespace.jpg)
</Frame>

Notice that the new `test: beta` label appears only in Version V2 and Version V3, while Version V1 remains unchanged. In the Applications page, you can now observe the service reflecting the new label.

## Modifying the Istio Configuration

To leverage the new grouping label, update the Istio configuration by modifying both the Destination Rule and the Virtual Service.

### Updating the Destination Rule

The original Destination Rule for the reviews service defines subsets for V1, V2, and V3. Here is the original configuration:

```yaml theme={null}
kind: DestinationRule
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: reviews
  namespace: default
  uid: 7a20a15c-416b-4948-a331-1ac49c64fc4
  resourceVersion: '26753'
  generation: 7
  creationTimestamp: '2021-08-15T22:17:54Z'
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"networking.istio.io/v1alpha3","kind":"DestinationRule","metadata":{"annotations":{},"name":"reviews"},"spec":{"host":"reviews","subsets":[{"labels":{"version":"v1"},"name":"v1"},{"labels":{"version":"v2"},"name":"v2"},{"labels":{"version":"v3"},"name":"v3"}]}}
spec:
  host: reviews
  subsets:
    - labels:
        version: v1
      name: v1
    - labels:
        version: v2
      name: v2
```

Update the configuration to incorporate the new grouping label by preserving the V1 subset and adding a new subset for `test: beta`:

```yaml theme={null}
kind: DestinationRule
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: reviews
  namespace: default
  uid: 7a2031c5-416b-4948-a331-1cda49c64fc4
  resourceVersion: '26753'
  generation: 7
  creationTimestamp: '2021-08-15T22:17:54Z'
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"networking.istio.io/v1alpha3","kind":"DestinationRule","metadata":{"annotations":{},"name":"reviews","namespace":"default"},"spec":{"host":"reviews","subsets":[{"labels":{"version":"v1"},"name":"v1"},{"labels":{"version":"v2"},"name":"v2"},{"labels":{"version":"v3"},"name":"v3"}}]}}
spec:
  host: reviews
  subsets:
    - labels:
        version: v1
      name: v1
    - labels:
        test: beta
      name: v2
```

This change allows you to test different versions of the application. You can even enable customers to choose their preferred version.

### Updating the Virtual Service

When you update the Virtual Service, the subset references must match the updated Destination Rule. The original Virtual Service configuration is as follows:

```yaml theme={null}
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: reviews
  namespace: default
  uid: 7bc87fe-169a-45a2-ad2d-8bae6f02009e
  resourceVersion: '27541'
  generation: 9
  creationTimestamp: '2021-08-15T22:18:03Z'
annotations: {}
spec:
  hosts:
    - reviews
  http:
    - match:
        - headers:
            end-user:
              exact: kodekloud
      route:
        - destination:
            host: reviews
            subset: v2
    - match:
        - headers:
            end-user:
              exact: versionest
      route:
        - destination:
            host: reviews
            subset: v3
```

To eliminate warnings on Kiali regarding mismatched subsets, update the Virtual Service to use only the V1 subset along with the new test-beta subset:

```yaml theme={null}
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: reviews
  namespace: default
  uid: 7bc87de-169a-4f32-a2ad-8bae6f02090e
  resourceVersion: '27541'
  generation: 9
  creationTimestamp: '2021-08-15T22:18:03Z'
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >-
      {"apiVersion":"networking.istio.io/v1alpha3","kind":"VirtualService","metadata":{"annotations":{},"name":"reviews","namespace":"default"},"spec":{"hosts":["reviews"],"http":[{"match":[{"headers":{"end-user":{"exact":"kodekloud"}}}],"route":[{"destination":{"host":"reviews","subset":"v2"}}]},{"match":[{"headers":{"end-user":{"exact":"kodekloud"}}}],"route":[{"destination":{"host":"reviews","subset":"v3"}}]},{"route":[{"destination":{"host":"reviews","subset":"beta"}}]}]}}
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
            subset: v1
        - destination:
            host: reviews
            subset: beta
```

## Managing Traffic Distribution

Now that the configurations have been updated, you can control the percentage of traffic routed to each subset. For a scenario where the new subset receives only 10% of the traffic, use this configuration:

```yaml theme={null}
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: reviews
  namespace: default
  uid: 7bc87de-169a-4f32-a2ad-8bae6f02009e
  resourceVersion: '27341'
  generation: 9
  creationTimestamp: '2021-08-15T22:18:03Z'
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"networking.istio.io/v1alpha3","kind":"VirtualService","metadata":{"annotations":{},"name":"reviews","namespace":"default"},"spec":{"hosts":["reviews"],"http":[{"match":[{"headers":{"end-user":{"exact":"kodekloud"}}}],"route":[{"destination":{"host":"reviews","subset":"v2"}}]},{"match":[{"headers":{"end-user":{"exact":"kodekloud"}}}],"route":[{"destination":{"host":"reviews","subset":"v3"}}]},{"route":[{"destination":{"host":"reviews","subset":"beta"}}]}]}}
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
            subset: v1
        - destination:
            host: reviews
            subset: beta
          weight: 10
```

After testing, you might observe that Reviews V1 handles most of the traffic while the new subset appears less frequently. To experiment with dynamic traffic distribution, adjust the weights—for example, giving V1 and the `test` subset equal distribution:

```yaml theme={null}
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: reviews
  namespace: default
  uid: 7bc87fe-169a-4f32-a2ad-8baeef02009e
  resourceVersion: '28322'
  generation: 11
  creationTimestamp: '2021-08-01T22:18:03Z'
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"networking.istio.io/v1alpha3","kind":"VirtualService","metadata":{"annotations":{},"name":"reviews"},"namespace":"default","spec":{"hosts":["reviews"],"http":[{"match":[{"headers":{"end-user":{"exact":"kodekloud"}}}],"route":[{"destination":{"host":"reviews","subset":"v2"}}]},{"match":[{"headers":{"end-user":{"exact":"kodekloud"}}}],"route":[{"destination":{"host":"reviews","subset":"v3"}}]}]}}
managedFields:
  - apiVersion: networking.istio.io/v1alpha3
    kind: VirtualService
    metadata:{"annotations":{},"name":"reviews"}
    namespace: default
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
            subset: v1
          weight: 10
        - destination:
            host: reviews
            subset: test
          weight: 10
```

## Updating the Destination Rule's Traffic Policy

Next, update the Destination Rule to include a traffic policy for the new test subset. Specify the label for the test group and apply a random load balancing strategy:

```yaml theme={null}
kind: DestinationRule
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: reviews
  namespace: default
  uid: 7da03f52-416b-4948-a331-14ca49c64fc4
  resourceVersion: '28120'
  generation: 8
  creationTimestamp: '2021-08-15T22:17:54Z'
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"networking.istio.io/v1alpha3","kind":"DestinationRule","metadata":{"annotations":{},"name":"reviews","namespace":"default"},"spec":{"host":"reviews","subsets":[{"labels":{"version":"v1"},"name":"v1"},{"labels":{"version":"v2"},"name":"v2"},{"labels":{"version":"v3"},"name":"v3"}]}}
managedFields:
  ...
spec:
  host: reviews
  subsets:
    - labels:
        version: v1
      name: v1
    - labels:
        test: beta
      name: test
  trafficPolicy:
    loadBalancer:
      simple: RANDOM
```

With this configuration, Reviews V2 and V3 are randomly selected based on the load balancing strategy.

## Reverting to Round-Robin Load Balancing

If you need to revert to a round-robin load balancing policy, remove the subsets from the Virtual Service and update the Destination Rule accordingly:

### Destination Rule Update

```yaml theme={null}
kind: DestinationRule
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: reviews
  namespace: default
  uid: 7a20a15c-416b-4948-a331-14c49c64fc4
  resourceVersion: '28566'
  generation: 10
  creationTimestamp: '2021-08-15T22:17:54Z'
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"networking.istio.io/v1alpha3","kind":"DestinationRule","metadata":{"annotations":{},"name":"reviews","namespace":"default"},"spec":{"host":"reviews","subsets":[{"labels":{"version":"v1"}},{"labels":{"version":"v2"}},{"labels":{"version":"v3"}},{"name":"v3"}]}}
managedFields: []
spec:
  host: reviews
  trafficPolicy:
    loadBalancer:
      simple: ROUND
```

### Virtual Service Update

```yaml theme={null}
kind: VirtualService
apiVersion: networking.istio.io/v1alpha3
metadata:
  name: reviews
  namespace: default
  uid: 7bc87fe-169a-4f32-a2ad-8bae6f02090e
  resourceVersion: '28616'
  generation: 13
  creationTimestamp: '2021-08-15T22:18:03Z'
annotations:
  kubectl.kubernetes.io/last-applied-configuration: >
    {"apiVersion":"networking.istio.io/v1alpha3","kind":"VirtualService","metadata":{"annotations":{},"name":"reviews","namespace":"default"},"spec":{"hosts":["reviews"],"http":[{"match":[{"headers":{"end-user":{"exact":"kodekloud"}}}],"route":[{"destination":{"host":"reviews","subset":"v2"}}]},{"match":[{"headers":{"end-user":{"exact":"kodekloud"}}}],"route":[{"destination":{"host":"reviews","subset":"v3"}}]}]}}
managedFields: []
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
```

With these modifications, the reviews service will now utilize a round-robin strategy, cycling through available endpoints.

## Conclusion

By leveraging Destination Rules and Virtual Services, Istio provides a powerful mechanism to manage and control traffic routing in your microservices architecture. This tutorial demonstrated how to add a new grouping label, update the relevant configurations, and control traffic distribution between different versions of the reviews service. With these techniques, you can enhance your service mesh architecture and experiment with advanced traffic management strategies.

For additional details on Istio and traffic management strategies, refer to the [Istio Documentation](https://istio.io/latest/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-service-mesh/module/fe135c6a-440a-4e97-b1b5-6a2b032689bd/lesson/4bedbf0b-5f51-4021-8161-4332380b8fcb" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/istio-service-mesh/module/fe135c6a-440a-4e97-b1b5-6a2b032689bd/lesson/09363f9a-0751-42b6-9238-a5c7401de8c1" />
</CardGroup>


# Demo Fault Injection

Source: https://notes.kodekloud.com/docs/Istio-Service-Mesh/Traffic-Management/Demo-Fault-Injection/page

This article demonstrates simulating service degradation using Istios fault injection to evaluate system responses to slow or failing services.

In this lesson, we demonstrate how to simulate service degradation by introducing a delay in the details service using Istio's fault injection capabilities. By doing so, you can evaluate how the overall product page responds to slow or failing services, helping you to plan coordinated responses to potential issues in your service mesh.

## Step 1: Create a Destination Rule

Before applying the fault injection rule, it is essential to configure a Destination Rule. This rule defines a subset (in this case, "v1") of the details service required for the fault injection configuration.

## Step 2: Set Up the Virtual Service

Begin by creating a Virtual Service named "details." Within the virtual service configuration, specify the affected service in the host section. Next, include a fault section under the HTTP protocol configuration. The following configuration delays 70% of the traffic destined for the "v1" subset of the details service by an extra 7 seconds:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: details
spec:
  hosts:
    - details
  http:
    - fault:
        delay:
          percentage:
            value: 70.0
          fixedDelay: 7s
      route:
        - destination:
            host: details
            subset: v1
```

<Callout icon="lightbulb">
  Save the above configuration to a file (for example, `virtual-service-fault.yaml`) and apply it using `kubectl` to implement the fault injection rule.
</Callout>

Apply the configuration with the following commands:

```bash theme={null}
istiotraining@local istio-1.10.3 $ vi virtual-service-fault.yaml
istiotraining@local istio-1.10.3 $ kubectl apply -f virtual-service-fault.yaml
virtualservice.networking.istio.io/details created
```

This rule instructs Istio to inject a 7-second delay to 70% of the requests reaching the details service.

## Step 3: Verify the Configuration in Kiali

After applying the configuration, verify that the Virtual Service and associated settings are active and error-free within your service mesh. Kiali provides a visual confirmation of the Istio configurations in use:

<Frame>
  ![The image shows the Kiali console interface displaying Istio configuration details for the "default" namespace, listing a VirtualService and a Gateway.](https://kodekloud.com/kk-media/image/upload/v1752879388/notes-assets/images/Istio-Service-Mesh-Demo-Fault-Injection/kiali-console-istio-configuration-default.jpg)
</Frame>

## Step 4: Observe the Impact on the Application

Navigate to the application to see the effect of the fault injection. In Kiali, you will observe that:

* The details service experiences performance degradation, as indicated by problematic connections from the product page.
* Some requests (approximately 30%) remain unaffected and continue to operate normally.

<Frame>
  ![The image shows a Kiali console interface displaying a service mesh graph with nodes representing different services and their interactions. It includes metrics on HTTP requests, success rates, and errors.](https://kodekloud.com/kk-media/image/upload/v1752879389/notes-assets/images/Istio-Service-Mesh-Demo-Fault-Injection/kiali-console-service-mesh-graph.jpg)
</Frame>

When you refresh the browser, you might notice that the details service occasionally fails to respond within the expected time frame due to the injected delay. Conversely, the healthy traffic (30%) may still provide timely responses.

<Callout icon="lightbulb">
  Fault injection is an effective technique to simulate real-world service degradations. It can help identify weaknesses in your service architecture and guide you in developing stronger, more resilient applications.
</Callout>

## Conclusion

This lesson has shown how to use Istio's fault injection to intentionally slow down a service, enabling you to examine the responses of the overall system under degraded conditions. Understanding these behaviors is key to improving the reliability and performance of your service mesh.

For more detailed information, consider exploring:

* [Istio Fault Injection Documentation](https://istio.io/latest/docs/tasks/traffic-management/fault-injection/)
* [Kiali Documentation](https://www.kiali.io/documentation/latest/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-service-mesh/module/fe135c6a-440a-4e97-b1b5-6a2b032689bd/lesson/b5053789-8d11-43ec-b03d-9d06c27a0fd6" />
</CardGroup>
