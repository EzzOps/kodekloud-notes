# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Create a namespace for Cert-Manager
kubectl create namespace cert-manager

# Install Cert-Manager and register its CRDs
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --set installCRDs=true
```

Wait until all pods in the `cert-manager` namespace are in the `Running` state:

```bash theme={null}
kubectl get pods -n cert-manager
```

> **lightbulb** Make sure your cluster meets the [Cert-Manager prerequisites](https://cert-manager.io/docs/installation/).

***

## 2. Review the Test App and Ingress

We have a simple “whoami” deployment in the `default` namespace, fronted by Traefik:

```bash theme={null}
kubectl get all -n default
```

Example output:

```text theme={null}
pod/whoami-8c9864b56-6pm4p   1/1 Running
service/whoami               ClusterIP   10.98.232.119    80/TCP
deployment.apps/whoami       1/1 Running
```

Check the existing Ingress:

```bash theme={null}
kubectl get ingress whoami-ingress -n default
```

```text theme={null}
NAME             CLASS    HOSTS   ADDRESS   PORTS   AGE
whoami-ingress   traefik  *       <none>    80      5m
```

Describe it:

```bash theme={null}
kubectl describe ingress whoami-ingress -n default
```

***

## 3. Create a Let’s Encrypt Staging Issuer

To prevent hitting rate limits, start with the staging environment. Save this as `staging-issuer.yaml`:

```yaml theme={null}
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email:  your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-staging
    solvers:
      - http01:
          ingress:
            name: whoami-ingress
```

Apply and inspect:

```bash theme={null}
kubectl apply -f staging-issuer.yaml
kubectl describe issuer letsencrypt-staging -n default
kubectl get secrets -n default
```

You should see `letsencrypt-staging` in the secret list.

***

## 4. Update the Ingress for TLS

Modify `whoami-ingress.yaml` to include the Cert-Manager annotation and a TLS block:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: whoami-ingress
  namespace: default
  annotations:
    cert-manager.io/issuer: letsencrypt-staging
spec:
  ingressClassName: traefik
  tls:
    - hosts:
        - test-example.com
      secretName: web-ssl
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: whoami
                port:
                  name: web
```

Apply the updated Ingress:

```bash theme={null}
kubectl apply -f whoami-ingress.yaml
```

> **triangle-alert** Ensure DNS for `test-example.com` points to your Traefik load balancer before requesting a certificate.

***

## 5. Verify the ACME Challenge and Certificate Issuance

Describe the Ingress again to confirm ACME resources:

```bash theme={null}
kubectl describe ingress whoami-ingress -n default
```

Look for:

* A `cm-acme-http-solver-…` backend under the ACME challenge path
* An event `CreateCertificate` indicating `web-ssl` was requested

```text theme={null}
Events:
  Type    Reason            Age   From                        Message
  ----    ------            ----  ----                        -------
  Normal  CreateCertificate  10s   cert-manager-ingress-shim  Successfully created Certificate "web-ssl"
```

***

## 6. Create a Let’s Encrypt Production Issuer

Once staging is validated, switch to the production environment. Create `prod-issuer.yaml`:

```yaml theme={null}
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-production
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email:  your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-production
    solvers:
      - http01:
          ingress:
            name: whoami-ingress
```

Apply and verify:

```bash theme={null}
kubectl apply -f prod-issuer.yaml
kubectl describe issuer letsencrypt-production -n default
```

***

## 7. Switch Ingress to Production Issuer

Update the Ingress annotation to use the production Issuer:

```bash theme={null}
kubectl annotate ingress whoami-ingress \
  cert-manager.io/issuer=letsencrypt-production \
  --overwrite -n default
```

Describe the Ingress to confirm renewal:

```bash theme={null}
kubectl describe ingress whoami-ingress -n default
```

In the events, you should see:

```text theme={null}
Normal  RenewCertificate  12s  cert-manager-ingress-shim  Successfully renewed Certificate "web-ssl"
```

Your Traefik Ingress is now secured with a Let’s Encrypt production certificate.

***

## Issuer Configuration Summary

| Issuer Name            | Environment | ACME Server URL                                                                                                  | Secret Name            |
| ---------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------- |
| letsencrypt-staging    | Staging     | [https://acme-staging-v02.api.letsencrypt.org/directory](https://acme-staging-v02.api.letsencrypt.org/directory) | letsencrypt-staging    |
| letsencrypt-production | Production  | [https://acme-v02.api.letsencrypt.org/directory](https://acme-v02.api.letsencrypt.org/directory)                 | letsencrypt-production |

***

## References

* [Cert-Manager Documentation](https://cert-manager.io/docs/)
* [Let’s Encrypt ACME v2 API](https://letsencrypt.org/docs/acme-protocol/)
* [Traefik Ingress Controller](https://doc.traefik.io/traefik/)
* [Kubernetes Ingress Basics](https://kubernetes.io/docs/concepts/services-networking/ingress/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-networking/module/5a70ab6c-2094-4bf2-9f49-e441919fc8c2/lesson/733b4868-57b0-497e-a4bb-47956f1cb24a)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-networking/module/5a70ab6c-2094-4bf2-9f49-e441919fc8c2/lesson/3cbd85fd-6665-41a7-b190-91a30b0c9a67)


# Demo Cilium Hubble

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Network-Security/Demo-Cilium-Hubble/page

This article provides a guide on setting up Cilium Hubble for metrics, monitoring, and visibility in a Kubernetes environment.

## Prerequisites

* A running Kubernetes cluster with Cilium installed (v1.15.3 or later).
* Prometheus and Grafana deployed in the `cilium-monitoring` namespace.

> **lightbulb** Hubble components (Relay, UI, metrics) are disabled by default. You must enable them via Helm to collect and visualize network flows.

## 1. Verify Cilium and Hubble Status

First, confirm Cilium is healthy and Hubble is not yet active:

```bash theme={null}
root@controlplane ~ ➜ cilium status
Cilium:               OK
Operator:             OK
Envoy DaemonSet:      disabled (using embedded mode)
Hubble Relay:         disabled
ClusterMesh:          disabled

Deployment          cilium-operator     Desired: 1, Ready: 1/1, Available: 1/1
DaemonSet           cilium              Desired: 2, Ready: 2/2, Available: 2/2
Containers:         cilium              Running: 2
                    cilium-operator     Running: 1

Cluster Pods:  5/5 managed by Cilium
Helm chart version:        v1.15.3
Image versions
  cilium            quay.io/cilium/cilium:v1.15.3
  cilium-operator   quay.io/cilium/operator-generic:v1.15.3
```

Verify that Grafana and Prometheus are up but not receiving Hubble metrics:

```bash theme={null}
root@controlplane ~ ➜ kubectl get all -n cilium-monitoring
NAME                           READY   STATUS    RESTARTS   AGE
pod/grafana-xxx                1/1     Running   0          10m
pod/prometheus-yyy             1/1     Running   0          10m

NAME                TYPE       CLUSTER-IP      PORT(S)
service/grafana     NodePort   10.98.81.88     3000:32000/TCP
service/prometheus  ClusterIP  10.99.242.121   9090/TCP
```

Check that the Cilium Helm repo is configured:

```bash theme={null}
root@controlplane ~ ➜ helm repo list
NAME    URL
cilium  https://helm.cilium.io/
```

## 2. Enable Hubble Components

Upgrade your Cilium installation to enable Hubble Relay, UI, and Prometheus metrics:

```bash theme={null}
root@controlplane ~ ➜ helm upgrade cilium cilium/cilium --version 1.15.4 \
  --namespace kube-system \
  --reuse-values \
  --set hubble.enabled=true \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true \
  --set hubble.metrics.enableOpenMetrics=true \
  --set prometheus.enabled=true \
  --set operator.prometheus.enabled=true \
  --set hubble.metrics.enabled="{dns,drop,tcp,flow,port_distribution,icmp,httpV2:exemplars=true;labelsContext=source_ip,source_namespace,destination_ip,destination_namespace,destination_workload,traffic_direction}"
```

> **lightbulb** | Metric Type        | Description                                   |
  | ------------------ | --------------------------------------------- |
  | dns                | DNS query and response details                |
  | drop               | Packets dropped by policy or misconfiguration |
  | tcp, icmp          | L4 protocol-specific flow statistics          |
  | port\_distribution | Top ports by traffic volume                   |
  | httpV2             | HTTP/2 requests and response summaries        |

After a minute, confirm that Hubble Relay and UI are healthy:

```bash theme={null}
root@controlplane ~ ➜ cilium status
...
Hubble Relay:    OK
Hubble UI:       OK
```

## 3. View Hubble Metrics in Grafana

Navigate to the Grafana dashboard in the `cilium-monitoring` namespace. You should see Hubble flow metrics such as flows per node, dropped vs forwarded traffic, and protocol distribution:

![The image shows a dashboard with various graphs displaying network flow metrics, such as "Flows processed Per Node," "Flow Types," and "Forwarded vs Dropped," over a time period.](https://kodekloud.com/kk-media/image/upload/v1752880402/notes-assets/images/Kubernetes-Networking-Deep-Dive-Demo-Cilium-Hubble/network-flow-metrics-dashboard-graphs.jpg)

## 4. Expose the Hubble UI as NodePort

By default, the Hubble UI service is `ClusterIP`. Edit it to use a NodePort for external access:

```bash theme={null}
root@controlplane ~ ➜ kubectl edit svc hubble-ui -n kube-system
```

Replace the spec with:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: hubble-ui
  namespace: kube-system
spec:
  type: NodePort
  ports:
    - name: http
      port: 80
      targetPort: 8081
      nodePort: 30000
  selector:
    k8s-app: hubble-ui
```

> **triangle-alert** Exposing services via NodePort can open your cluster to external traffic. Ensure proper firewall rules or security groups are in place.

Now you can access the Hubble UI at `<NodeIP>:30000`.

## 5. Test Network Flows with curl

We have a demo application offering two endpoints:

* `/api` – restricted to requests with header `X-API-KEY: abc123` from pods labeled `app=admin`.
* `/healthz` – open to all traffic.

Create a `CiliumNetworkPolicy` to enforce this:

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: demo-policy
  namespace: default
spec:
  endpointSelector:
    matchLabels:
      app: demo
  ingress:
  - fromEndpoints:
    - matchLabels: {app: admin}
    toPorts:
    - ports: [{port: "80", protocol: TCP}]
      rules:
        http:
        - method: GET
          path: /healthz
        - method: GET
          path: /api
          headers: {X-API-KEY: abc123}
```

Apply the policy and perform valid and invalid requests:

```bash theme={null}
root@controlplane ~ ➜ kubectl run --rm -i --tty admin --labels=app=admin \
  --image=curlimages/curl --restart=Never -- \
  curl -H "X-API-KEY: abc123" http://app-svc-80/api
{"message":"Have a great day!","method":"GET","url":"/api"}
```

Invalid request (missing API key) will time out:

```bash theme={null}
root@controlplane ~ ➜ kubectl run --rm -i --tty admin --image=curlimages/curl \
  --restart=Never -- curl http://app-svc-80/api --connect-timeout 2
curl: (28) Failed to connect to app-svc-80 port 80 after 2001 ms: Timeout was reached
```

### Observe Metrics for Forwarded vs Dropped Flows

Return to Grafana to see the changes in the “Forwarded vs Dropped” panel and other flow statistics:

![The image shows a network monitoring dashboard with various graphs displaying metrics such as forwarded vs. dropped packets, protocol usage, port distribution, and TCP statistics over time.](https://kodekloud.com/kk-media/image/upload/v1752880403/notes-assets/images/Kubernetes-Networking-Deep-Dive-Demo-Cilium-Hubble/network-monitoring-dashboard-graphs-metrics.jpg)

## 6. Visualize Live Flows in Hubble UI

Open the Hubble UI at `<NodeIP>:30000` to explore live network flows. Click on any flow to see detailed metadata and policy verdicts:

![The image shows a network flow diagram with nodes labeled "admin," "default," and "demo," indicating traffic flow to port 80 using TCP and HTTP. The flow details section indicates a dropped connection due to a policy denial.](https://kodekloud.com/kk-media/image/upload/v1752880404/notes-assets/images/Kubernetes-Networking-Deep-Dive-Demo-Cilium-Hubble/network-flow-diagram-admin-default-demo.jpg)

## 7. Using the Hubble CLI

You can also use the Hubble CLI for real-time troubleshooting. Exec into a Cilium agent pod:

```bash theme={null}
root@controlplane ~ ➜ kubectl exec -it -n kube-system cilium-xxxx -c cilium-agent -- /bin/bash
root@cilium:/home/cilium# hubble version
hubble 0.13.2 compiled with go1.21.8 on linux/amd64

root@cilium:/home/cilium# hubble status
Healthcheck (unix:///var/run/cilium/hubble.sock): Ok
Current/Max Flows: 4095/4095 (100.00%)
Flows/s: 4.77
```

Stream live flow logs:

```bash theme={null}
root@cilium:/home/cilium# hubble observe
Aug  1 00:52:09.273: 10.0.1.84:54976 <> kube-system/hubble-ui:8081 to-overlay FORWARDED (TCP SYN)
Aug  1 00:52:09.276: kube-system/hubble-ui:57128 -> kube-system/hubble-relay:4245 FORWARDED (TCP ACK, PSH)
```

Filter flows by namespace, pod, time range, or format:

```bash theme={null}
