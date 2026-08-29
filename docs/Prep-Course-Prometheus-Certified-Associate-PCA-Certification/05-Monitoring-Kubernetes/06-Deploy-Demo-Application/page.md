# Using a pod (replace <prom-pod> with the actual pod name)
kubectl port-forward <prom-pod> 9090:9090

# Or directly from the service
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
```

3. Open your browser at: [http://localhost:9090](http://localhost:9090)

You should see the Prometheus web UI where you can run queries and explore time series data.

<Frame>
  <img alt="The image shows a Prometheus web interface for querying time series data, with options for enabling features like autocomplete and highlighting. It includes fields for expressions and no data has been queried yet." />
</Frame>

This local port-forward is ideal for quick checks and demos. For persistent or multi-user access, choose NodePort, LoadBalancer, or an Ingress-based approach and secure it appropriately.

## Example: change service type to NodePort (quick patch)

If you decide to expose Prometheus via NodePort briefly, you can patch the service:

```bash theme={null}
kubectl patch svc prometheus-kube-prometheus-prometheus -p '{"spec": {"type": "NodePort"}}'
```

After patching, run `kubectl get svc prometheus-kube-prometheus-prometheus -o wide` to see the assigned `NODE-PORT`. Then you can access Prometheus at `http://<node-ip>:<node-port>` (ensure firewall / security groups allow the port).

For production setups, prefer Ingress with TLS and authentication, or use a cloud LoadBalancer combined with proper access controls.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/b88c394c-edce-4eb5-8fc4-c65759ecbf20" />
</CardGroup>


# Deploy Demo Application

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Deploy-Demo-Application/page

Guide to containerizing and deploying a Node.js app instrumented with swagger-stats, creating Kubernetes manifests, and configuring Prometheus Operator scraping for metrics

We've already installed and configured a Prometheus server to monitor our Kubernetes infrastructure. Next, we'll demonstrate how to configure Prometheus (installed via the Prometheus Operator) to monitor a simple Node.js application running inside Kubernetes.

This walkthrough covers:

* A minimal Node.js app instrumented with `swagger-stats` for Prometheus metrics
* Containerizing and publishing the image to Docker Hub
* Kubernetes manifests (Deployment + Service) to run the app
* Verifying the deployment and exposing the metrics endpoint for Prometheus scraping

Relevant links:

* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Prometheus Operator: [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
* Kubernetes: [https://kubernetes.io/](https://kubernetes.io/)
* Node.js: [https://nodejs.org/](https://nodejs.org/)
* Express: [https://expressjs.com/](https://expressjs.com/)
* swagger-stats: [https://github.com/sladkovm/swagger-stats](https://github.com/sladkovm/swagger-stats)
* Docker Hub: [https://hub.docker.com/](https://hub.docker.com/)
* Dockerfile reference: [https://docs.docker.com/engine/reference/builder/](https://docs.docker.com/engine/reference/builder/)

## 1) Example Node.js application (index.js)

This minimal Express app exposes a few endpoints and uses `swagger-stats` to provide a Prometheus-compatible metrics endpoint at `/swagger-stats/metrics`.

```javascript theme={null}
// index.js
const express = require("express");
const swStats = require("swagger-stats");
const app = express();

// Exposes metrics at /swagger-stats/metrics
app.use(swStats.getMiddleware());

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.get("/comments", (req, res) => {
  res.send("Comments");
});

app.get("/threads", (req, res) => {
  res.send("Threads");
});

app.get("/replies", (req, res) => {
  res.send("Replies");
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API listening on port ${PORT}`));
```

<Callout icon="lightbulb">
  Ensure your application listens on the same port you expose in the container and in the Kubernetes Service (below). This example uses port 3000 and exposes metrics at `/swagger-stats/metrics`.
</Callout>

## 2) Dockerfile

A lightweight Dockerfile to build the image for this app:

```dockerfile theme={null}
FROM node:16
