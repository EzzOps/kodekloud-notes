# Demo Network Policies

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Container-Network-InterfaceCNI/Demo-Network-Policies/page

This walkthrough explores securing Pod-to-Pod and Pod-to-External traffic in Kubernetes using NetworkPolicies.

In this walkthrough, we’ll explore how to secure Pod-to-Pod and Pod-to-External traffic in Kubernetes using NetworkPolicies. You will learn to:

1. Verify the **default** connectivity behavior
2. Apply **default-deny** rules for egress and ingress
3. Permit **specific** egress/ingress to selected Pods
4. Validate the resulting network restrictions

***

## 1. Verify Default Connectivity

By default, Kubernetes allows all egress and ingress traffic between Pods (even across namespaces) and to the Internet.

### 1.1 Test External Connectivity

Exec into **pod1** (in the `default` namespace) and ping an external endpoint:

```bash theme={null}
kubectl exec -it pod1 --container container1 -- ping -c 4 www.google.com
```

You should see successful responses:

```text theme={null}
64 bytes from 142.250.125.103: icmp_seq=1 ttl=111 time=2.05 ms
...
4 packets transmitted, 4 received, 0% packet loss
```

### 1.2 Test Cross-Namespace Connectivity

List Pod IPs in `kube-system` and pick one (e.g. `192.168.121.187`):

```bash theme={null}
kubectl get pods -n kube-system -o jsonpath='{range .items[*]}{.status.podIP}{"\n"}{end}'
```

From **pod1**, ping that IP:

```bash theme={null}
kubectl exec -it pod1 --container container1 -- ping -c 3 192.168.121.187
```

You should receive replies, confirming open egress/ingress.

> **lightbulb** By default, no NetworkPolicy is enforced, so all traffic flows freely.

***

## 2. Apply Default-Deny Egress

To block all outbound traffic from Pods in the `default` namespace, create a **default-deny egress** policy.

```yaml theme={null}
