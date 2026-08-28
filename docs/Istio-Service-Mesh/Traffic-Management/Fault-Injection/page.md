# Fault Injection

Source: https://notes.kodekloud.com/docs/Istio-Service-Mesh/Traffic-Management/Fault-Injection/page

This article explains fault injection as a testing strategy to simulate errors and validate error handling mechanisms in Virtual Services.

Fault injection is a testing strategy designed to simulate errors and validate the resilience of your error handling mechanisms. In this guide, we explain how to simulate faults in your Virtual Services to ensure that your application gracefully handles failures.

<Callout icon="lightbulb">
  Before proceeding, make sure you have successfully deployed your application, configured a Gateway, and set up the product page and reviews Virtual Services. All components should be functioning as expected.
</Callout>

Fault injection in Istio supports the simulation of two primary error types in Virtual Services:

* Delays
* Aborts

## Simulating Delay Faults

The following example demonstrates how to inject a delay fault into a Virtual Service. In this configuration, a delay of 5 seconds is applied to 10% of the requests routed to the service.

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
  - my-service
  http:
  - fault:
      delay:
        percentage:
          value: 0.1
        fixedDelay: 5s
    route:
    - destination:
        host: my-service
        subset: v1
```

In the above YAML, the delay fault for the Virtual Service named "my-service" causes a fixed delay of 5 seconds on 10% of the incoming requests. This helps you validate that your system's timeout and retry mechanisms are working correctly.

## Simulating Abort Faults

In addition to delay faults, you can configure abort faults to simulate scenarios where requests are rejected with specific error codes. Abort faults help test how your service behaves under error conditions, ensuring that fallback mechanisms and error handling policies are effective.

For detailed instructions and additional configuration options for abort faults, refer to the [Istio Fault Injection Documentation](https://istio.io/latest/docs/concepts/traffic-management/#fault-injection).

By incorporating both delay and abort fault injections, you can thoroughly assess the robustness of your application and ensure that it remains resilient even under adverse conditions.

For further reading, consider exploring these resources:

* [Istio Documentation](https://istio.io/latest/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Error Handling Best Practices](https://www.example.com/error-handling)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-service-mesh/module/fe135c6a-440a-4e97-b1b5-6a2b032689bd/lesson/6358d65b-15a3-4498-8e0b-61c2cae90233" />
</CardGroup>
