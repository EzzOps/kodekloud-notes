# Summary

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Troubleshooting/Summary/page

Overview of Istio troubleshooting and exam strategies for ICA including sidecar injection, Service and VirtualService validation, istioctl and kubectl diagnostics, logs, and SSH exam procedures

This short but crucial lesson covers Istio troubleshooting best practices and exam tips for the Istio Certified Associate (ICA). Keep these high-level guidelines in mind when debugging Istio-enabled workloads or preparing for the exam:

* Istio features only work when the namespace is configured for sidecar injection. Confirm the namespace label and, when required, restart deployments so the Envoy sidecar is injected.
* Inspect annotations, Service definitions and ports, VirtualServices, and DestinationRules carefully — these are frequent sources of misconfiguration.
* Never assume a namespace is empty. Check for other controllers, CRDs, or resources that may affect traffic.
* Combine standard Kubernetes troubleshooting (logs, events, pod status) with Istio-specific checks (`istioctl analyze`, configuration inspection).
* For exam-style scenarios, SSH into each host referenced by the question, perform the required checks, then exit before moving on to the next question.

<Frame>
  <img alt="The image is a summary slide with three numbered points related to Istio and Kubernetes configurations and exam tips, set on a gradient blue background." />
</Frame>

## Key troubleshooting focus areas

1. Namespace configuration
   * Confirm the `istio-injection` label exists and is set to `enabled` for automatic sidecar injection, or verify manual injection where applicable.
   * If you change the label or the pod template, restart the deployment to force injection.

2. Workload networking
   * Verify Service ports and targetPorts match the application container ports.
   * Confirm VirtualService hosts and routes align with Service names and ports.
   * Check DestinationRule subsets and labels to ensure traffic is routed to actual pod labels.

3. Resource inspection
   * Review pod logs for both application containers and sidecars (`-c <container>`).
   * Look at `kubectl describe` output and events for scheduling, image pull, or readiness/liveness failures.
   * Validate Istio configuration objects in the same namespace as well as in the `istio-system` control plane namespace.

## Recommended commands and checks

Use the following commands to quickly identify common Istio and Kubernetes issues. Replace placeholders such as `my-namespace`, `my-deployment`, `my-pod`, and `my-container` with your actual values.

| Command                               |                                                                  Purpose | Example                                                                    |
| ------------------------------------- | -----------------------------------------------------------------------: | -------------------------------------------------------------------------- |
| `istioctl analyze -n <namespace>`     |       Analyze Istio configuration and highlight common misconfigurations | `istioctl analyze -n my-namespace`                                         |
| `kubectl get namespace -o yaml`       |                                    Show namespace labels and annotations | `kubectl get namespace my-namespace -o yaml`                               |
| `kubectl get namespace --show-labels` |                                           Quick view of namespace labels | `kubectl get namespace my-namespace --show-labels`                         |
| `kubectl label namespace`             |                                       Enable automatic sidecar injection | `kubectl label namespace my-namespace istio-injection=enabled --overwrite` |
| `kubectl rollout restart`             | Restart deployments to pick up sidecar injection or pod template changes | `kubectl rollout restart deployment my-deployment -n my-namespace`         |
| `kubectl get pods`                    |                                                         See pod statuses | `kubectl get pods -n my-namespace`                                         |
| `kubectl describe pod`                |                                      Detailed pod information and events | `kubectl describe pod my-pod -n my-namespace`                              |
| `kubectl logs`                        |                             View container logs (application or sidecar) | `kubectl logs my-pod -c my-container -n my-namespace`                      |
| `kubectl get events`                  |            Check for cluster events that affect scheduling or networking | `kubectl get events -n my-namespace`                                       |

> **lightbulb** Always SSH into any host referenced by an exam question, run the required checks from that host, then exit before moving to the next question. Also run `istioctl analyze -n <namespace>` early — it catches many common Istio issues quickly.

## Quick troubleshooting checklist

* Confirm the namespace has `istio-injection=enabled` (or verify manual injection).
* Restart deployments after changing labels or pod templates.
* Validate that Service ports match container ports (including `targetPort`).
* Confirm VirtualService hosts/hosts and DestinationRule subsets correspond to Service names and pod labels.
* Inspect both application and Envoy sidecar logs.
* Use `istioctl analyze` and check `kubectl get events` for additional hints.

## Final tips for the ICA exam

* Be methodical: check labels, annotations, Services, VirtualServices, DestinationRules, and pod templates in sequence.
* Small oversights like not restarting a deployment after enabling injection can cost time and points.
* Use a large monitor if possible so you can view multiple terminals and resources at once; it reduces context-switching and speeds up verification.
* Practice navigating between hosts via SSH, running diagnostics, and exiting cleanly — exam questions may require interacting with multiple nodes.

> **warning** Exam tip: If the question lists specific hosts, SSH into each listed host and complete the checks from there. Failing to SSH into the required hosts (or forgetting to exit) can cause exam errors.

## Links and references

* [Istio Documentation](https://istio.io/latest/docs/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [istioctl CLI reference](https://istio.io/latest/docs/reference/commands/istioctl/)
* [ICA Course — KodeKloud](https://learn.kodekloud.com/user/courses/istio-service-mesh)

Congratulations on completing this course — you should now be ready to attempt the mock exams and the real ICA exam. Good luck!

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/3b1a1d7c-b04a-4a3d-bf30-65da7d5460c3/lesson/5a08da93-ae0a-4a21-80ae-378873d45306)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/2d0c6545-943b-49e4-b231-9092b777e287/lesson/9ec8607c-4689-4281-8c2b-a791f16c2b18)
