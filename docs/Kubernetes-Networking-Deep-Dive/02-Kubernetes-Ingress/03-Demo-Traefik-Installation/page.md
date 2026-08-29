# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: whoami-ingress
  annotations:
    external-dns.alpha.kubernetes.io/hostname: whoami.kubernetkk.xyz
    external-dns.alpha.kubernetes.io/target: "192.168.121.243"
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: whoami
                port:
                  number: 80
```

Apply the Ingress:

```bash theme={null}
kubectl apply -f ingress.yaml
```

Watch ExternalDNS logs as it detects the new Ingress:

```bash theme={null}
kubectl logs -f deployment/external-dns -n default
```

Look for a log entry like:

```plaintext theme={null}
time="2024-07-18T23:21:05Z" level=info msg="GoDaddy: 3 changes will be done"
```

This confirms that ExternalDNS is creating the DNS record.

<Callout icon="lightbulb">
  If you use a cloud provider’s `LoadBalancer` service type, omit the `external-dns.alpha.kubernetes.io/target` annotation. ExternalDNS will automatically use the LoadBalancer’s IP.
</Callout>

***

## References

* [ExternalDNS GitHub](https://github.com/kubernetes-sigs/external-dns)
* [GoDaddy API Documentation](https://developer.godaddy.com/)
* [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
* [Helm Charts](https://helm.sh/docs/topics/charts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/19677663-2b7d-4c3d-92ee-06df9f5530eb/lesson/b562f81a-4ce6-404a-85de-01ed64dc8a03" />
</CardGroup>


# Demo Traefik Installation

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Kubernetes-Ingress/Demo-Traefik-Installation/page

This guide explains how to deploy Traefik as an Ingress controller on a Kubernetes cluster.

In this guide, you’ll learn how to deploy Traefik as an Ingress controller on your Kubernetes cluster. We cover:

1. Manual installation using Kubernetes manifests (Quick Start)
2. Installation with Helm and customizing the service type
3. Deploying a demo application behind Traefik
4. Enabling and viewing Traefik access logs

***

## Table of Contents

1. [Manual Installation (Quick Start)](#1-manual-installation-quick-start)
2. [Helm Installation](#2-helm-installation)
3. [Demo App Ingress Configuration](#3-demo-app-ingress-configuration)
4. [Viewing Traefik Logs](#4-viewing-traefik-logs)
5. [Links and References](#5-links-and-references)

***

## 1. Manual Installation (Quick Start)

This section walks you through deploying Traefik using static YAML manifests. We’ll configure RBAC, deploy Traefik, and expose it via LoadBalancer services.

### 1.1 Create RBAC Resources

Traefik needs permission to watch and update Kubernetes resources. First, define a `ClusterRole`:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: traefik-role
rules:
  - apiGroups: ["*"]
    resources:
      - services
      - secrets
      - endpoints
      - ingresses
      - configmaps
    verbs: ["get", "list", "watch"]
  - apiGroups: ["networking.k8s.io", "discovery.k8s.io"]
    resources: ["ingresses", "ingressclasses"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["networking.k8s.io"]
    resources: ["ingresses/status"]
    verbs: ["update"]
```

Bind this role to a ServiceAccount in the `kube-system` namespace:

```yaml theme={null}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: traefik-account
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: traefik-binding
subjects:
  - kind: ServiceAccount
    name: traefik-account
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: traefik-role
  apiGroup: rbac.authorization.k8s.io
```

<Callout icon="lightbulb">
  Ensure your cluster’s RBAC is enabled. If you run into `Forbidden` errors, verify that the ServiceAccount and ClusterRoleBinding are created correctly.
</Callout>

### 1.2 Deploy the Traefik Controller

Create a Deployment for Traefik, specifying the ServiceAccount:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: traefik
  namespace: kube-system
  labels:
    app: traefik
spec:
  replicas: 1
  selector:
    matchLabels:
      app: traefik
  template:
    metadata:
      labels:
        app: traefik
    spec:
      serviceAccountName: traefik-account
      containers:
        - name: traefik
          image: traefik:v3.1
          args:
            - --api.insecure=true
            - --providers.kubernetesingress=true
            - --entryPoints.web.address=:80
            - --entryPoints.websecure.address=:443
          ports:
            - name: web
              containerPort: 80
            - name: websecure
              containerPort: 443
            - name: dashboard
              containerPort: 8080
```

<Callout icon="triangle-alert">
  The `--api.insecure` flag enables an unsecured dashboard. Do **not** use this in production environments. For secure dashboards, configure TLS and authentication.
</Callout>

#### Expose Traefik with LoadBalancer Services

Create a Service manifest (`traefik-svc.yaml`):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: traefik-web
  namespace: kube-system
spec:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
      targetPort: 80
    - name: https
      port: 443
      targetPort: 443
  selector:
    app: traefik
---
apiVersion: v1
kind: Service
metadata:
  name: traefik-dashboard
  namespace: kube-system
spec:
  type: LoadBalancer
  ports:
    - name: dashboard
      port: 8080
      targetPort: 8080
  selector:
    app: traefik
```

Apply all resources:

```bash theme={null}
kubectl apply -f traefik-role.yaml \
  -f traefik-account.yaml \
  -f traefik-binding.yaml \
  -f traefik-deployment.yaml \
  -f traefik-svc.yaml
```

Check the LoadBalancer IPs:

```bash theme={null}
kubectl get svc -n kube-system
```

***

## 2. Helm Installation

Installing Traefik via Helm simplifies upgrades and customization.

### 2.1 Add the Traefik Helm Repository

```bash theme={null}
helm repo add traefik https://traefik.github.io/charts
helm repo update
kubectl create namespace traefik
```

### 2.2 Install with Default Values

```bash theme={null}
helm install traefik traefik/traefik \
  --namespace=traefik
```

Verify resources:

```bash theme={null}
kubectl get all -n traefik
```

### 2.3 Customizing the Service Type

On clusters without a LoadBalancer (e.g., bare-metal), switch to `NodePort`. Create `values.yaml`:

```yaml theme={null}
service:
  type: NodePort
  ports:
    web:
      nodePort: 32080
    websecure:
      nodePort: 32443

logs:
  access:
    enabled: true
```

Upgrade the release:

```bash theme={null}
helm upgrade traefik traefik/traefik \
  --namespace=traefik \
  --values=values.yaml
```

Confirm the NodePort assignment:

```bash theme={null}
kubectl get svc -n traefik
