# kind.config
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: my-cluster
networking:
  ipFamily: dual
  disableDefaultCNI: true
nodes:
- role: control-plane
- role: worker
- role: worker
```

Create the cluster:

```bash theme={null}
kind create cluster --config kind.config
```

After creation, check node status (nodes will be `NotReady` until a CNI is installed):

```bash theme={null}
kubectl get nodes
```

Example output:

```console theme={null}
NAME                         STATUS     ROLES          AGE   VERSION
my-cluster-control-plane     NotReady   control-plane  77s   v1.32.2
my-cluster-worker            NotReady   <none>         66s   v1.32.2
my-cluster-worker2           NotReady   <none>         66s   v1.32.2
```

Verify kube-system pods — kube-proxy is present by default (one pod per node):

```bash theme={null}
kubectl get pod -n kube-system
```

Example output highlighting kube-proxy:

```console theme={null}
NAME                                                   READY   STATUS    RESTARTS   AGE
coredns-668d6bf9bc-5j6sz                               0/1     Pending   0          80s
coredns-668d6bf9bc-mhq8g                               0/1     Pending   0          80s
etcd-my-cluster-control-plane                          1/1     Running   0          87s
kube-apiserver-my-cluster-control-plane                1/1     Running   0          85s
kube-controller-manager-my-cluster-control-plane       1/1     Running   0          85s
kube-proxy-ckwhs                                       1/1     Running   0          77s
kube-proxy-d7bhz                                       1/1     Running   0          80s
kube-proxy-kd267                                       1/1     Running   0          77s
kube-scheduler-my-cluster-control-plane                1/1     Running   0          85s
```

***

## Install Cilium (run alongside kube-proxy)

Install Cilium via the official Helm chart. By default, Cilium's Helm chart sets kubeProxyReplacement to "false", which means Cilium runs alongside kube-proxy and does not change service handling.

Snippet example from `values.yaml`:

```yaml theme={null}
readinessProbe:
  # failure threshold of readiness probe
  failureThreshold: 3
  # interval between checks of the readiness probe
  periodSeconds: 30

# Configure the kube-proxy replacement in Cilium BPF datapath
# Valid options: "false" or "true" (check your chart's values; some Cilium versions/methods also expose modes like "partial"/"strict")
# ref: https://docs.cilium.io/en/stable/network/kubernetes/kubeproxy-free/
kubeProxyReplacement: "false"
```

Install Cilium with Helm (adjust file paths as needed):

```bash theme={null}
helm repo add cilium https://helm.cilium.io/
helm repo update
helm install cilium cilium/cilium -n kube-system -f values.yaml
```

Verify Cilium pods are running:

```bash theme={null}
kubectl get pod -n kube-system | grep -i cilium
```

Example output:

```console theme={null}
cilium-envoy-5s5hl               1/1     Running   0    3m1s
cilium-envoy-k26kd               1/1     Running   0    3m1s
cilium-envoy-m99v9               1/1     Running   0    3m1s
cilium-gb5nk                     1/1     Running   0    3m1s
cilium-glbl6                     1/1     Running   0    3m1s
cilium-nbqld                     1/1     Running   0    3m1s
cilium-operator-59944f4b8f-bmr98 1/1     Running   0    3m1s
cilium-operator-59944f4b8f-mhq7s 1/1     Running   0    3m1s
```

Verify the kube-proxy replacement setting from inside a Cilium agent pod using the Cilium debug tool:

Get a Cilium agent pod name:

```bash theme={null}
kubectl -n kube-system get pods -l k8s-app=cilium
```

Exec into a Cilium agent pod and check status:

```bash theme={null}
kubectl -n kube-system exec -it <cilium-pod> -- cilium-dbg status | grep -i kubeproxyreplacement
```

Expected output when running alongside kube-proxy:

```console theme={null}
Defaulted container "cilium-agent" out of: cilium-agent, config (init), mount-cgroup (init), apply-sysctl-overwrites (init), mount-bpf-fs (init), clean-cilium-state (init), install-cni-binaries (init)
KubeProxyReplacement:  False
```

This confirms Cilium is not replacing kube-proxy and leaves kube-proxy active.

***

## Switching Cilium to replace kube-proxy

Cilium's kube-proxy replacement (kubeProxyReplacement: "true") hands over Kubernetes service handling from kube-proxy (iptables/ipvs) to Cilium's eBPF-based datapath. High-level steps:

1. Remove kube-proxy components (daemonset and configmap).
2. Clean up kube-proxy-created iptables chains (environment-dependent).
3. Update Cilium configuration to enable kube-proxy replacement and configure direct API server connectivity (k8sServiceHost/k8sServicePort).
4. Upgrade the Cilium Helm release with new values.
5. Verify replacement is active and confirm service connectivity.

<Callout icon="warning">
  Deleting kube-proxy and flushing iptables can disrupt cluster networking. Ensure you have console access to nodes and a recovery plan before making these changes on production clusters.
</Callout>

Important notes:

* On kind clusters (Docker-in-Docker), iptables changes from inside containers may not affect the host. Proceed with caution and skip iptables cleanup on kind unless you understand the host context.
* Ensure Cilium agents can reach the API server directly when kube-proxy is removed (set k8sServiceHost and k8sServicePort appropriately).

### Remove kube-proxy daemonset and configmap

Delete the kube-proxy daemonset:

```bash theme={null}
kubectl -n kube-system delete ds kube-proxy
```

Delete the kube-proxy configmap:

```bash theme={null}
kubectl -n kube-system delete cm kube-proxy
```

You should see confirmation that resources were deleted.

### iptables cleanup (environment-dependent)

kube-proxy typically creates Kubernetes-specific iptables chains. In production you would remove those so that Cilium's eBPF datapath becomes authoritative for services. Do not run these commands on kind unless you know the correct host context.

Example inspection and (cautious) commands:

```bash theme={null}
# Inspect kube-proxy chains (example)
sudo iptables -t nat -S | grep KUBE-

# Example flush (only if you know what you're doing):
# sudo iptables -t nat -F KUBE-SERVICES
# sudo iptables -t nat -F KUBE-NODEPORTS
# sudo iptables -t nat -F KUBE-EXTERNAL-SERVICES
```

<Callout icon="lightbulb">
  On kind clusters running inside Docker containers, modifying host iptables from the container may not have the intended effect. Skip iptables cleanup on kind unless you know the correct host context.
</Callout>

### Enable kube-proxy replacement in values.yaml

Edit your `values.yaml` to enable kube-proxy replacement and add API server connectivity settings. Example modifications:

```yaml theme={null}
readinessProbe:
  failureThreshold: 10
  periodSeconds: 30

# Enable Cilium's kube-proxy replacement
kubeProxyReplacement: "true"

# Kubernetes connection settings for kube-proxy replacement
kubeConfigPath: ""
k8sServiceHost: "my-cluster-control-plane"
k8sServicePort: "6443"
```

Notes:

* k8sServiceHost should be a hostname or IP reachable from worker nodes.
* k8sServicePort is typically 6443 (API server port).

Table — kubeProxyReplacement options:

| kubeProxyReplacement value | Meaning                                                                        |
| -------------------------- | ------------------------------------------------------------------------------ |
| "false"                    | Cilium runs alongside kube-proxy; kube-proxy handles services.                 |
| "true"                     | Cilium replaces kube-proxy; Cilium's eBPF datapath handles services.           |
| "partial"/"strict"         | Some Cilium versions/methods may expose additional modes; consult Cilium docs. |

Reference: [Cilium kube-proxy replacement docs](https://docs.cilium.io/en/stable/network/kubernetes/kubeproxy-free/)

### Push updated configuration with Helm

Upgrade the Cilium release with the modified values:

```bash theme={null}
helm upgrade cilium cilium/cilium -f values.yaml -n kube-system
```

After the upgrade, verify that Cilium reports kube-proxy replacement enabled.

Get a Cilium agent pod and inspect status:

```bash theme={null}
kubectl -n kube-system get pods -l k8s-app=cilium
kubectl -n kube-system exec -it <cilium-pod> -- cilium-dbg status --verbose | grep -A 20 "KubeProxyReplacement"
```

You should see a section similar to:

```console theme={null}
KubeProxyReplacement Details:
  Status:                   True
  Socket LB:                Enabled
  Socket LB Tracing:        Enabled
  Socket LB Coverage:       Full
  Devices:                  eth0  172.19.0.3 ...
  Mode:                     SNAT
  Session Affinity:         Enabled
  Graceful Termination:     Enabled
  ...
Services:
 - ClusterIP:               Enabled
 - NodePort:                Enabled (Range: 30000-32767)
 - LoadBalancer:            Enabled
 - externalIPs:             Enabled
 - HostPort:                Enabled
```

This confirms Cilium is now handling kube-proxy responsibilities.

***

## Test service connectivity (NodePort example)

Create a simple nginx deployment and a NodePort service to verify service handling through Cilium's replacement.

deployment.yaml:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:stable
        ports:
        - containerPort: 80
```

service.yaml:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30007
```

Apply the manifests:

```bash theme={null}
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Confirm the service:

```bash theme={null}
kubectl get svc
```

Example output:

```console theme={null}
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP        19m
my-service   NodePort    10.96.101.131   <none>        80:30007/TCP   4s
```

Find node internal IPs:

```bash theme={null}
kubectl get node -o wide
```

Example excerpt:

```console theme={null}
NAME                       STATUS   ROLES          AGE   VERSION    INTERNAL-IP
my-cluster-control-plane   Ready    control-plane  20m   v1.32.2    172.19.0.4
my-cluster-worker          Ready    <none>         20m   v1.32.2    172.19.0.3
my-cluster-worker2         Ready    <none>         20m   v1.32.2    172.19.0.2
```

From a host that can reach the node IP (here using worker node IP and nodePort 30007), confirm HTTP response:

```bash theme={null}
curl 172.19.0.3:30007
```

Expected nginx response (truncated):

```html theme={null}
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and working.</p>
...
</html>
```

If you receive the nginx page, Cilium's kube-proxy replacement is successfully servicing NodePort traffic via the eBPF datapath.

***

## Summary

* By default Cilium runs alongside kube-proxy (kubeProxyReplacement: "false").
* To let Cilium replace kube-proxy:
  * Remove kube-proxy components.
  * Clean iptables chains where required (environment-dependent).
  * Set kubeProxyReplacement: "true" and configure k8sServiceHost/k8sServicePort.
  * Upgrade the Cilium Helm release and verify with `cilium-dbg status`.
  * Validate service traffic with a test Deployment + Service.
* Always test carefully and have recovery access when changing core networking components.

Links and references

* [Cilium Documentation — kube-proxy replacement](https://docs.cilium.io/en/stable/network/kubernetes/kubeproxy-free/)
* [kind — Kubernetes in Docker](https://kind.sigs.k8s.io/)
* [Helm](https://helm.sh/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/0807e400-fd1b-4f25-bba5-d0fdb0f4e3f2/lesson/c0703837-90ea-450f-ae27-5d5042322d32" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/0807e400-fd1b-4f25-bba5-d0fdb0f4e3f2/lesson/44205deb-7dd9-407d-a4f0-15b79934684d" />
</CardGroup>


# Demo Routing Modes

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Exploring-Cilium/Demo-Routing-Modes/page

Demonstrates Cilium tunnel versus native routing modes, inspects packet flows, and shows required physical network changes to enable native pod subnet routing with static routes or BGP.

This lesson demonstrates Cilium's two routing modes — tunnel (encapsulation) and native routing — by inspecting packet flows for each mode and showing what changes are required on your physical network to enable native routing.

We use a small 3-node cluster (1 control-plane, 2 workers) where each node sits on a different physical network and all networks connect via a central router. The pod CIDRs are allocated by Cilium/Cluster IPAM from 10.0.0.0/8 and are split per node (for example, 10.0.1.0/24 for worker1 and 10.0.2.0/24 for worker2).

We will observe traffic from a pod on worker1 to a pod on worker2 using four terminals: control-plane, worker1, worker2, and router.

<Callout icon="lightbulb">
  By default Cilium uses tunnel mode (VXLAN) to encapsulate pod traffic between nodes, so no changes are required on the physical network for basic pod-to-pod connectivity.
</Callout>

***

## Environment details

* Cluster: 3 nodes — 1 control-plane, 2 workers
* Node physical network interfaces and IPs:
  * control-plane: 192.168.146.130 (router .129)
  * worker1: 192.168.211.128 (router .129)
  * worker2: 192.168.44.128 (router .129)
* Pod CIDR ranges: 10.0.0.0/8 split per node (e.g., 10.0.1.0/24, 10.0.2.0/24)
* Tools used: kubectl, helm, tcpdump, Wireshark

***

## 1) Install Cilium (default: tunnel/encapsulation mode)

Install Cilium using the upstream Helm chart and a default values.yaml (no routing changes). The default uses VXLAN encapsulation.

Install:

```bash theme={null}
helm install cilium cilium/cilium -n kube-system -f values.yaml
```

Verify nodes:

```bash theme={null}
kubectl get node
