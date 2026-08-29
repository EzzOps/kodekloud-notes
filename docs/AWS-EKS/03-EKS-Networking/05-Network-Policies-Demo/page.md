# Network Policies Demo

Source: https://notes.kodekloud.com/docs/AWS-EKS/EKS-Networking/Network-Policies-Demo/page

Learn to secure pod-to-pod communication in Kubernetes using NetworkPolicies through a hands-on guide with practical examples and configurations.

In this hands-on guide, you’ll learn how to secure pod-to-pod communication in Kubernetes using NetworkPolicies. We’ll start with a clean cluster—no workloads, services, or policies—and progressively:

1. Deploy two NGINX apps (`app1` & `app2`)
2. Verify default connectivity
3. Enforce a default-deny posture
4. Open selective ingress/egress rules
5. Test DNS resolution and direct IP connectivity

***

> **lightbulb** Ensure you have a running Kubernetes cluster (v1.8+) with a CNI plugin that supports NetworkPolicies (e.g., Calico, Cilium).

## 1. Deploying Two Sample Applications

We’ll create two deployments and expose each via a ClusterIP service.

### 1.1 app1 Deployment & Service (`app1.deploy.yaml`)

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: "1"
  template:
    metadata:
      labels:
        app: "1"
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app1
spec:
  type: ClusterIP
  selector:
    app: "1"
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```

### 1.2 app2 Deployment & Service (`app2.deploy.yaml`)

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: "2"
  template:
    metadata:
      labels:
        app: "2"
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app2
spec:
  type: ClusterIP
  selector:
    app: "2"
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```

Apply both manifests and confirm pods are running:

```bash theme={null}
kubectl apply -f app1.deploy.yaml -f app2.deploy.yaml
kubectl get pods
```

Expected output:

```text theme={null}
NAME                     READY   STATUS    RESTARTS   AGE
app1-xxxxxxxxxx-xxxxx    1/1     Running   0          ...
app2-xxxxxxxxxx-xxxxx    1/1     Running   0          ...
```

## 2. Verifying Basic Connectivity

By default, all pods can talk to each other. From inside `app1`, curl the `app2` service:

```bash theme={null}
kubectl exec -it \
  $(kubectl get pod -l app=1 -o jsonpath='{.items[0].metadata.name}') \
  -- curl http://app2
```

You should see the NGINX welcome page:

```html theme={null}
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
</html>
```

Repeat from `app2` to `app1` to confirm bi-directional access.

## 3. Applying a Default-Deny NetworkPolicy

Now enforce a zero-trust posture by blocking all ingress and egress in the `default` namespace.

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: default
spec:
  podSelector: {}                   # Selects all pods
  policyTypes:
  - Ingress
  - Egress
```

```bash theme={null}
kubectl apply -f default-deny.networkpolicy.yaml
kubectl get networkpolicies.networking.k8s.io
```

Output:

```text theme={null}
NAME           POD-SELECTOR   POLICY-TYPES      AGE
default-deny   <all pods>     Ingress,Egress    ...
```

> **triangle-alert** This policy blocks **all** traffic, including DNS queries. Pods will no longer resolve service names or reach cluster DNS.

Test connectivity failure:

```bash theme={null}
kubectl exec -it \
  $(kubectl get pod -l app=2 -o jsonpath='{.items[0].metadata.name}') \
  -- curl http://app1
