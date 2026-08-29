# Change `type: ClusterIP` to `type: NodePort` and save.
kubectl -n falco get service falco-falcosidekick-ui
```

***

## Accessing the Falco Sidekick UI

Open your browser at:

```text theme={null}
http://<node-ip>:<node-port>/ui
```

The UI launches with default alerts for privileged container launches.

![The image shows a Falcosidekick UI displaying events related to the launch of privileged containers, with detailed information about each event. The interface includes a search bar and various data fields such as user name, container ID, and event time.](https://kodekloud.com/kk-media/image/upload/v1752873742/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Falco-UI-HELM/falcosidekick-ui-privileged-containers-events.jpg)

The dashboard provides charts for event priorities and rule counts:

![The image shows a dashboard from the Falcosidekick UI, displaying a pie chart of event priorities and a bar chart of rules related to container security events.](https://kodekloud.com/kk-media/image/upload/v1752873743/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Falco-UI-HELM/falcosidekick-dashboard-pie-bar-chart.jpg)

On the **Events** tab, you can filter by severity and drill into individual alerts:

![The image shows a dashboard interface of the Falcosidekick UI displaying event logs with notices about container activities. It includes details like time, priority, and specific container information.](https://kodekloud.com/kk-media/image/upload/v1752873744/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Falco-UI-HELM/falcosidekick-ui-dashboard-event-logs.jpg)

***

## Triggering an Alert

Generate a new Falco event by executing a shell in any pod:

```bash theme={null}
kubectl exec -it n1 -n istio-system -- sh
# Run a command, then exit
exit
```

Refresh the UI to see the new alert.

***

## Next Steps

In the next article, we’ll configure Sidekick to send alerts to a Slack channel. Reinstall Falco with your Slack webhook:

```bash theme={null}
kubectl delete release falco -n falco
helm install falco falcosecurity/falco \
  --namespace falco \
  --set falcosidekick.enabled=true \
  --set falcosidekick.webui.enabled=true \
  --set falcosidekick.config.slack.webhookurl="https://hooks.slack.com/services/XXXX/YYYY/ZZZZ"
```

***

## Links and References

* [Falco Documentation](https://falco.org/docs/)
* [Falco Sidekick GitHub](https://github.com/falcosecurity/falco-sidekick)
* [Helm Charts for Falco](https://falcosecurity.github.io/charts)
* [Kubernetes Official Docs](https://kubernetes.io/docs/)
* [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/aa3c0077-5a2a-4c01-afd0-b1298995833b)


# Demo Integration Tests Prod

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Demo-Integration-Tests-Prod/page

This guide explains how to add integration testing to a Jenkins pipeline after deploying an application in production.

In this guide, we’ll walk through adding a lightweight integration testing stage to your Jenkins pipeline after deploying an application to the production namespace. This approach ensures your production release undergoes quick sanity checks before serving real traffic.

## Overview

Post-deployment testing often includes functional, smoke, black-box, and performance tests. Common tools include [JMeter](https://jmeter.apache.org/) for load testing. Here, we’ll implement a simple **Integration Tests – PROD** stage in Jenkins that mirrors our dev workflow.

| Test Type   | Purpose                              | Example Tool                         |
| ----------- | ------------------------------------ | ------------------------------------ |
| Smoke       | Basic health and response validation | `curl`, Postman                      |
| Functional  | Business logic verification          | Custom scripts                       |
| Black-box   | External interface testing           | `curl`, Selenium                     |
| Performance | Throughput and latency measurement   | [JMeter](https://jmeter.apache.org/) |

> **lightbulb** This integration step is a quick sanity check. For full end-to-end or load tests, consider extending with specialized tools or scripts.

## Jenkins Pipeline Changes

We insert a new **Integration Tests – PROD** stage immediately after the `K8S_Deployment - PROD` stage. If any test fails, the deployment rolls back to the previous version automatically.

```groovy theme={null}
stage('Integration Tests - PROD') {
    steps {
        script {
            try {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    sh "bash integration-test-PROD.sh"
                }
            } catch (e) {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    sh "kubectl -n prod rollout undo deploy ${deploymentName}"
                }
                error("Integration tests failed; rolled back deployment.")
            }
        }
    }
}
```

## Testing via Istio Ingress Gateway

In production, services typically use a **ClusterIP**. To access your app behind [Istio](https://istio.io/latest/docs/concepts/traffic-management/#gateways), retrieve the NodePort assigned to port 80 on the Istio Ingress Gateway:

```bash theme={null}
kubectl -n istio-system get svc istio-ingressgateway -o json \
  | jq '.spec.ports[] | select(.port == 80) | .nodePort'
```

> **triangle-alert** If the Ingress Gateway service does not expose port 80 as a NodePort, your tests will fail. Ensure your Gateway configuration allows external access.

## integration-test-PROD.sh

Below is the shell script executed in the **Integration Tests – PROD** stage. It:

1. Waits briefly for the deployment to settle.
2. Retrieves the Istio NodePort for port 80.
3. Constructs the application URL.
4. Checks a simple increment endpoint and HTTP status code.

```bash theme={null}
#!/bin/bash
set -euo pipefail
sleep 5s
