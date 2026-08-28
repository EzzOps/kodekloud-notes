# Create app directory
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install
# For production builds consider:
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
```

Build and push steps (example). Replace `your-dockerhub-username/prometheus-demo` with your repository:

```bash theme={null}
# build
sudo docker build -t your-dockerhub-username/prometheus-demo:latest .

# push
sudo docker push your-dockerhub-username/prometheus-demo:latest
```

Example push output (truncated for brevity):

```bash theme={null}
Using default tag: latest
9f1d71d7577d: Pushed
083ec4401539: Mounted from sanjeevkt720/promexample
...
latest: digest: sha256:cd9b462d575ea589122c44e0a16a928b60eefdc9e29b2019159e35992c size: 2.40 kB
```

## 3) Kubernetes manifest (Deployment + Service)

Create a file called `api-deploy.yaml`. This single manifest contains:

* A Deployment (2 replicas) that runs the container image
* A ClusterIP Service that forwards traffic to port 3000 on the pods

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
  labels:
    app: api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: your-dockerhub-username/prometheus-demo:latest
          ports:
            - containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
  labels:
    job: node-api
    app: api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
    - name: web
      protocol: TCP
      port: 3000
      targetPort: 3000
```

Replace `your-dockerhub-username/prometheus-demo:latest` with the image you pushed to Docker Hub.

<Callout icon="warning">
  Using a `ClusterIP` service means the application is not exposed externally by default. If you need external access, consider `NodePort`, `LoadBalancer`, or an Ingress depending on your environment.
</Callout>

## 4) Apply and verify

Apply the manifest and verify deployments and services:

```bash theme={null}
kubectl apply -f api-deploy.yaml
```

Expected output:

```bash theme={null}
deployment.apps/api-deployment created
service/api-service created
```

Check services:

```bash theme={null}
kubectl get svc
```

Example output (truncated):

```bash theme={null}
NAME                            TYPE        CLUSTER-IP       EXTERNAL-IP  PORT(S)       AGE
api-service                     ClusterIP   10.100.40.38     <none>       3000/TCP      11s
prometheus-grafana              ClusterIP   10.100.235.247   <none>       80/TCP        13h
prometheus-kube-prometheus      ClusterIP   10.100.54.169    <none>       9090/TCP      13h
...
```

Check deployments:

```bash theme={null}
kubectl get deployment
```

Example output:

```bash theme={null}
NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
api-deployment                  2/2     2            2           2m
prometheus-grafana              1/1     1            1           13h
prometheus-kube-prometheus-operator 1/1 1            1           13h
```

If a replica shows `1/2` initially, wait a few seconds and re-run `kubectl get deployment` — the second pod often takes a moment to become ready.

## 5) Prometheus scrape configuration (Prometheus Operator)

When using the Prometheus Operator, you'll typically create a `ServiceMonitor` to tell Prometheus to scrape the application. The important parts are:

* `endpoints.path` should be `/swagger-stats/metrics`
* `endpoints.port` should match the service port name (`web` in the manifest above)
* `selector.matchLabels` should match the Service labels (e.g. `job: node-api` or `app: api`)

Example ServiceMonitor (illustrative):

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-servicemonitor
  labels:
    release: kube-prometheus
spec:
  selector:
    matchLabels:
      job: node-api
  endpoints:
    - port: web
      path: /swagger-stats/metrics
      interval: 15s
```

Note: Adjust `metadata.labels.release` or `selector` to match your Prometheus Operator setup.

## 6) Quick reference table

| Resource            | Purpose                                                 | Key fields / notes                                                                            |
| ------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Deployment          | Runs the Node.js app                                    | `replicas: 2`, `image: your-dockerhub-username/prometheus-demo:latest`, `containerPort: 3000` |
| Service (ClusterIP) | Internal access & Prometheus scraping                   | `port: 3000`, `targetPort: 3000`, label `job: node-api`                                       |
| ServiceMonitor      | Informs Prometheus what to scrape (Prometheus Operator) | `endpoints.path: /swagger-stats/metrics`, `endpoints.port: web`                               |

## 7) Next steps

* Apply a `ServiceMonitor` (or `PodMonitor`) so the Prometheus Operator discovers and scrapes `/swagger-stats/metrics`.
* Explore the metrics in Prometheus UI (typically `http://<prometheus-service>:9090`) and create Grafana dashboards.
* Consider securing the metrics endpoint (if needed) and tuning scrape intervals.

References and further reading:

* Prometheus documentation: [https://prometheus.io/docs/](https://prometheus.io/docs/)
* Prometheus Operator: [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
* Kubernetes Services: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)
* swagger-stats: [https://github.com/sladkovm/swagger-stats](https://github.com/sladkovm/swagger-stats)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/1edc5b8a-3b83-46f0-95d4-29351ed9cfe8" />
</CardGroup>


# Installing Helm Chart

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Installing-Helm-Chart/page

Guide to install Helm and deploy kube-prometheus-stack to provision Prometheus Alertmanager and observability components on a Kubernetes cluster, including installation, configuration, verification, and uninstallation.

In this lesson you'll install Helm and deploy the kube-prometheus-stack Helm chart to provision Prometheus, Alertmanager, and related observability components on a Kubernetes cluster. The guide walks through installing Helm, adding the Prometheus Community repo, inspecting and customizing chart values, installing the chart, verifying the deployment, and uninstalling the release.

## 1) Install Helm

Follow the official Helm documentation for platform-specific instructions: [https://helm.sh/docs/](https://helm.sh/docs/)

Typical Linux install (official script):

```bash theme={null}
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

Install via package managers:

```bash theme={null}
