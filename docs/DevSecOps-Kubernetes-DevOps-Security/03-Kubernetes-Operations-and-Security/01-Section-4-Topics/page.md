# Wait for pods to start
sleep 60s

if ! kubectl -n prod rollout status deploy ${deploymentName} --timeout=5s | grep -q "successfully rolled out"; then
  echo "Deployment ${deploymentName} rollout has failed"
  kubectl -n prod undo deploy ${deploymentName}
  exit 1
else
  echo "Deployment ${deploymentName} rollout is successful"
fi
```

Make the script executable:

```bash theme={null}
chmod +x k8s-PROD-deployment-rollout-status.sh
```

***

## Triggering the Deployment

1. Commit and push both `Jenkinsfile` and YAML/script files to your Git repo.
2. Start the Jenkins build.
3. Approve the production deployment when prompted.

![The image shows a Jenkins pipeline with various stages of a deployment process, including tests and scans. It also includes a prompt asking for approval to deploy to the production environment.](https://kodekloud.com/kk-media/image/upload/v1752873818/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Promoting-App-to-Prod-and-Visualize-using-Kiali/jenkins-pipeline-deployment-process-approval.jpg)

***

## Verifying the Production Deployment

Validate pods in the `prod` namespace and confirm the Kiali service:

```bash theme={null}
# Check Kiali in istio-system
kubectl -n istio-system get svc kiali

# View prod pods
kubectl -n prod get po
```

Example output:

```text theme={null}
NAME                                 READY   STATUS    RESTARTS   AGE
devsecops-7699f69c9f-cq44c           2/2     Running   0          34s
devsecops-7699f69c9f-qnrrr           2/2     Running   0          34s
devsecops-7699f69c9f-m82p            2/2     Running   0          34s
node-app-597c464649-lgs82            2/2     Running   0          121m
```

> The extra container in each pod is the Istio sidecar proxy.

***

## Visualizing with Kiali

Kiali offers a comprehensive dashboard to monitor your service mesh. Below is a quick overview of key sections.

### Namespaces Overview

![The image shows a Kiali dashboard displaying an overview of namespaces with details about labels, Istio configuration, and applications. The screen also includes a browser with multiple tabs open.](https://kodekloud.com/kk-media/image/upload/v1752873819/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Promoting-App-to-Prod-and-Visualize-using-Kiali/kiali-dashboard-namespaces-istio-overview.jpg)

### Outbound & Inbound Metrics

**Outbound Metrics**

![The image shows a Kiali dashboard interface displaying outbound metrics for a specific application namespace. It includes options for viewing request volume, throughput, and other network metrics.](https://kodekloud.com/kk-media/image/upload/v1752873820/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Promoting-App-to-Prod-and-Visualize-using-Kiali/kiali-dashboard-outbound-metrics-namespace.jpg)

**Inbound Metrics**

![The image shows a Kiali dashboard displaying inbound metrics for a specific application, with graphs for request volume, request duration, and request throughput. The interface includes navigation options and metric settings.](https://kodekloud.com/kk-media/image/upload/v1752873822/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Promoting-App-to-Prod-and-Visualize-using-Kiali/kiali-dashboard-inbound-metrics-graphs.jpg)

#### Generating Traffic

Use a simple `curl` loop to generate load and see real-time metrics:

```bash theme={null}
# Get service endpoints
kubectl -n istio-system get svc kiali
kubectl -n prod get svc

# Loop requests
while true; do
  curl -s 10.101.121.127:8080/increment/99
  echo
  sleep 1
done
```

***

### Workload Health and Logs

![The image shows a Kiali dashboard displaying workload properties, a graph overview, and health status for a deployment named "devsecops." The dashboard indicates the overall health is "Healthy" with pod and traffic status details.](https://kodekloud.com/kk-media/image/upload/v1752873823/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Promoting-App-to-Prod-and-Visualize-using-Kiali/kiali-dashboard-devsecops-health-overview.jpg)

Access logs directly in Kiali:

```text theme={null}
2021-06-26 15:33:40.059 INFO 1 --- [nio-8080-exec-2] com.devsecops.NumericController       : Value Received in Request - 99
...
[2021-06-20T15:33:47.962Z] "GET /increment/99 HTTP/1.1" 200 0 3 ... inbound|8080|
```

***

### Service Mesh Graph

![The image shows a Kiali dashboard displaying a service mesh graph with nodes representing services and their interactions, including response times and traffic details.](https://kodekloud.com/kk-media/image/upload/v1752873824/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Promoting-App-to-Prod-and-Visualize-using-Kiali/kiali-dashboard-service-mesh-graph.jpg)

The lock icon indicates that mutual TLS (mTLS) is enforced between services.

***

## References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kiali Official Website](https://kiali.io/)
* [DNS Spoofing on Kubernetes Clusters](https://www.aquasec.com/blog/dns-spoofing-kubernetes-clusters/)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/78279c65-1ff1-42e7-9ecf-cca66cb9a51c)


# Section 4 Topics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Section-4-Topics/page

This article discusses enhancing a DevSecOps pipeline by integrating security, observability, and notification features into a CI/CD workflow.

In this section, we’ll build on our existing CI/CD workflow by integrating security, observability, and notification features. You will learn how to:

* Integrate a CIS benchmark scan into your Jenkins pipeline
* Deploy the application into a dedicated Kubernetes production namespace
* Enforce mutual TLS and policy-driven traffic using Istio
* Monitor runtime security and compliance with Falco and KubeScan
* Publish detailed, content-rich notifications to Slack

> **lightbulb** Ensure you have the following already set up before proceeding:

  * A Jenkins server with pipeline-as-code enabled
  * Access to a Kubernetes cluster (production namespace created)
  * `kubectl`, `helm`, and Istio CLI (`istioctl`) installed and configured
  * Slack App credentials with incoming-webhook permissions

| Step                      | Tool(s)                                                                               | Purpose                                               |
| ------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 1. CIS Benchmarking       | [cis-scanner](https://www.cisecurity.org/)                                            | Validate cluster configuration against CIS guidelines |
| 2. Kubernetes Deployment  | `kubectl`, Helm                                                                       | Deploy your app to the production namespace           |
| 3. Istio Traffic Security | [Istio](https://istio.io/)                                                            | Enable mTLS and policy enforcement                    |
| 4. Cluster Monitoring     | [Falco](https://falco.org/), [KubeScan](https://github.com/TetragonSecurity/kubescan) | Real-time security alerts and compliance checks       |
| 5. Slack Notifications    | Slack API                                                                             | Send structured pipeline updates and alerts           |

![The image is a slide titled "Section #4" from a presentation on Kubernetes, DevOps, and Security. It outlines topics such as Kubernetes Security, DevSecOps introduction, a simple DevOps pipeline, and a DevSecOps pipeline.](https://kodekloud.com/kk-media/image/upload/v1752873825/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Section-4-Topics/kubernetes-devops-security-section-4.jpg)

That's it for this overview. Let’s dive into Task 1: adding a CIS benchmarking stage to our Jenkins pipeline.

## Links and References

* [CIS Benchmarks (Official)](https://www.cisecurity.org/)
* [Istio Documentation](https://istio.io/latest/docs/)
* [Falco Project](https://falco.org/)
* [KubeScan on GitHub](https://github.com/TetragonSecurity/kubescan)
* [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/6044cf93-3d3d-4d6b-80df-85a919a630e2)
