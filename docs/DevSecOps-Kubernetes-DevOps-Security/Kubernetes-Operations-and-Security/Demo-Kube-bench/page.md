# No resources found
```

## 2. Inspect the `prod` Namespace

List pods and services running in `prod`:

```bash theme={null}
kubectl -n prod get pods,svc
```

Pods:

```bash theme={null}
NAME                              READY   STATUS    RESTARTS   AGE
pod/devsecops-769f696c95f7jq      2/2     Running   0          2m17s
pod/devsecops-769f696c9f9f        2/2     Running   0          2m17s
pod/node-app-597464649c-5x75q     2/2     Running   0          4d4h
```

Services:

```bash theme={null}
NAME                   TYPE        CLUSTER-IP       PORT(S)     AGE
service/devsecops-svc  ClusterIP   10.101.121.127   8080/TCP    4d2h
service/node-service   ClusterIP   10.101.46.231    5000/TCP    4d4h
```

## 3. Observe Traffic

Generate continuous requests to the `devsecops-svc` service:

```bash theme={null}
while true; do
  curl -s 10.101.121.127:8080/increment/99
  sleep 1
done
```

## 4. Visualize in Kiali

Open Kiali’s Graph view for the `prod` namespace. By default, Istio uses **PERMISSIVE** mTLS, so you’ll see both plaintext and encrypted traffic between `devsecops-svc` and `node-service`.

<Frame>
  ![The image shows a Kiali dashboard displaying a service mesh graph for a Kubernetes environment, illustrating the connections and response times between different services.](https://kodekloud.com/kk-media/image/upload/v1752873753/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Istio-mTLS/kiali-dashboard-service-mesh-graph.jpg)
</Frame>

Click the lock icon to confirm which connections are encrypted.

## 5. Disable mTLS Globally

<Callout icon="triangle-alert">
  Disabling mTLS will route all service-to-service traffic over plaintext HTTP, exposing your data in transit.
</Callout>

Create a `PeerAuthentication` in the `istio-system` namespace:

```yaml theme={null}
# peerauth-disable.yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: DISABLE
```

Apply it:

```bash theme={null}
kubectl apply -f peerauth-disable.yaml
```

Wait \~15 seconds and refresh Kiali. You’ll first see mixed traffic, then all connections drop the lock icon.

## 6. Switch to Permissive Mode

<Callout icon="lightbulb">
  Permissive mode allows both mTLS and plaintext connections simultaneously—ideal for gradual rollout.
</Callout>

Edit the default PeerAuthentication:

```bash theme={null}
kubectl edit peerauthentication default -n istio-system
```

Update the spec:

```yaml theme={null}
spec:
  mtls:
    mode: PERMISSIVE
```

Save and exit, then verify:

```bash theme={null}
kubectl get peerauthentication default -n istio-system
# NAME      MODE        AGE
# default   PERMISSIVE  2m36s
```

Refresh Kiali to observe a mix of encrypted and unencrypted traffic.

## 7. Enforce Strict mTLS Mode

To require mTLS for all workloads:

```bash theme={null}
kubectl edit peerauthentication default -n istio-system
```

Change to:

```yaml theme={null}
spec:
  mtls:
    mode: STRICT
```

Save. The `curl` loop will now fail, as plaintext requests are blocked. Kiali will show a fully locked mesh:

<Frame>
  ![The image shows a Kiali dashboard displaying a service mesh graph for a Kubernetes environment, illustrating the connections and response times between different services.](https://kodekloud.com/kk-media/image/upload/v1752873755/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Istio-mTLS/kiali-dashboard-service-mesh-graph-2.jpg)
</Frame>

Hover over the lock icon to see “Mesh-wide mTLS is enabled.”

## 8. Verify with Packet Capture

Install the `ksniff` plugin and capture traffic to confirm encryption:

```bash theme={null}
# Install ksniff
kubectl krew install ksniff

# Capture TCP traffic from a pod
kubectl sniff <pod-name> -n prod --protocol tcp
```

Open the resulting PCAP in [Wireshark](https://www.wireshark.org/) and inspect TLS records on port `15001`.

***

In this lesson, you learned how to manage mTLS modes with Istio’s [PeerAuthentication API](https://istio.[AWS_SECRET_ACCESS_KEY]/peer_authentication/) and verify traffic encryption. Next, explore securing ingress traffic using the [Istio ingress gateway](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/).

## Links and References

* [Istio PeerAuthentication API](https://istio.[AWS_SECRET_ACCESS_KEY]/peer_authentication/)
* [Kiali Documentation](https://www.kiali.io/documentation/)
* [Wireshark](https://www.wireshark.org/)
* [ksniff Plugin](https://krew.sigs.k8s.io/plugins/ksniff)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/48076de3-407c-435c-95af-1b1a07bb0a2a" />
</CardGroup>


# Demo Kube bench

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Demo-Kube-bench/page

This article explains how to use kube-bench to run CIS Kubernetes Benchmark tests on a cluster, covering installation, execution, and CI/CD integration.

In this lesson, we’ll use **kube-bench** to run the [CIS Kubernetes Benchmark] tests against your cluster. We’ll cover:

* Overview of the CIS Benchmark PDF
* Manual Kubelet anonymous-auth check
* Installing and running kube-bench
* Parsing JSON output with `jq`
* CI/CD integration with Jenkins

## CIS Kubernetes Benchmark PDF

Download the official CIS Kubernetes Benchmark from the CIS website:\
[CIS Kubernetes Benchmark] requires an email to access the PDF.

<Callout icon="lightbulb">
  The PDF contains \~270 pages of guidelines, organized by test IDs per component. For instance, **4.2.1** in *Worker Node Security Configuration* verifies `--anonymous-auth=false`.
</Callout>

<Frame>
  ![The image shows a webpage for CIS Benchmarks focused on securing Kubernetes, offering a download link for the latest security guidelines. It includes a brief description and links to additional resources and community information.](https://kodekloud.com/kk-media/image/upload/v1752873756/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Kube-bench/cis-benchmarks-kubernetes-security-guidelines.jpg)
</Frame>

After downloading, open the PDF to review sections such as Terms of Use, Overview, and Recommendations.

<Frame>
  ![The image shows a computer screen displaying a PDF document titled "CIS Kubernetes Benchmark v1.6.0" with a table of contents visible. The document appears to be open in a PDF viewer, and the table of contents lists sections such as Terms of Use, Overview, and Recommendations.](https://kodekloud.com/kk-media/image/upload/v1752873757/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Kube-bench/cis-kubernetes-benchmark-pdf-viewer.jpg)
</Frame>

## Manual Check: Kubelet Anonymous Auth

On a kubeadm-provisioned node, verify the running Kubelet process and its config file:

```bash theme={null}
