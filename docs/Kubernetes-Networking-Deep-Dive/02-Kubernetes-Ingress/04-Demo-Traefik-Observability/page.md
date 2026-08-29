# NAME      TYPE       CLUSTER-IP      PORT(S)
# traefik   NodePort   10.xx.xx.xx     80:32080/TCP,443:32443/TCP
```

<Callout icon="lightbulb">
  If you change ports in `values.yaml`, ensure your firewall or cloud provider permits traffic on the new NodePorts.
</Callout>

***

## 3. Demo App Ingress Configuration

Deploy a simple “whoami” service and expose it via Traefik.

### 3.1 Deploy the `whoami` Application

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: whoami
  labels:
    app: whoami
spec:
  replicas: 1
  selector:
    matchLabels:
      app: whoami
  template:
    metadata:
      labels:
        app: whoami
    spec:
      containers:
        - name: whoami
          image: traefik/whoami
          ports:
            - name: http
              containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: whoami
spec:
  type: ClusterIP
  selector:
    app: whoami
  ports:
    - name: http
      port: 80
      targetPort: 80
```

Apply:

```bash theme={null}
kubectl apply -f whoami-app.yaml
```

### 3.2 Configure an Ingress Resource

Create `whoami-ingress.yaml`:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: whoami-ingress
spec:
  ingressClassName: traefik
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

Apply and verify:

```bash theme={null}
kubectl apply -f whoami-ingress.yaml
kubectl describe ingress whoami-ingress
```

Access the demo app:

```text theme={null}
http://<LoadBalancer-IP>/
# or, on NodePort:
http://<NodeIP>:32080/
```

***

## 4. Viewing Traefik Logs

Tail the Traefik pod’s logs to inspect both general and access logs:

```bash theme={null}
kubectl logs -f deployment/traefik -n traefik
```

With `logs.access.enabled: true`, each HTTP request is recorded in the logs.

***

## 5. Links and References

* [Traefik Official Documentation](https://doc.traefik.io/traefik/)
* [Kubernetes Ingress Concepts](https://kubernetes.io/docs/concepts/services-networking/ingress/)
* [Helm Chart for Traefik](https://artifacthub.io/packages/helm/traefik/traefik)
* [Traefik “whoami” Docker Image](https://hub.docker.com/r/traefik/whoami)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/19677663-2b7d-4c3d-92ee-06df9f5530eb/lesson/7318bf47-e385-467b-9f22-4ada897c41b8" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/19677663-2b7d-4c3d-92ee-06df9f5530eb/lesson/143c0736-4ff1-4980-9c39-04c1d9977d78" />
</CardGroup>


# Demo Traefik Observability

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Kubernetes-Ingress/Demo-Traefik-Observability/page

This article explores the Traefik dashboard for observability, detailing its configuration, access, and features in a Kubernetes environment.

In this lesson, we’ll explore the Traefik dashboard—a powerful observability interface enabled by default in every Traefik installation. The dashboard provides real-time insights into routing rules, service health, and security settings. For production environments, avoid exposing this dashboard publicly. Use a private network or [kubectl port-forward](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application/) instead. In this lab, we will configure a NodePort (30000) for direct access.

## 1. Deploy the Traefik Dashboard Service

Create a Service of type `NodePort` to expose the Traefik API port:

```yaml theme={null}
