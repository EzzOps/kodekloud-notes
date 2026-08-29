# Example output:
# NAME             READY   UP-TO-DATE   AVAILABLE   AGE
# auth-depl        1/1     1            1           4h55m
# inventory-depl   1/1     1            1           5h32m
# products-depl    1/1     1            1           4h47m
```

## 2. Create an Intercept

First, connect Telepresence to your cluster if you haven’t already:

```bash theme={null}
telepresence connect
```

Then run:

```bash theme={null}
telepresence intercept auth-depl -p 8000:3000
```

| Local Port | Container Port | Description               |
| ---------- | -------------- | ------------------------- |
| 8000       | 3000           | Auth service HTTP traffic |

Here’s the relevant snippet from the Kubernetes manifest:

```yaml theme={null}
# Deployment spec excerpt
spec:
  template:
    spec:
      containers:
      - name: auth
        image: sanjeevkt720/telepresence-auth
        ports:
        - containerPort: 3000
          name: web
---
apiVersion: v1
kind: Service
metadata:
  name: auth-service
spec:
  selector:
    app: auth
  ports:
    - port: 3000
      targetPort: 3000
```

You should see output similar to:

```bash theme={null}
Using Deployment auth-depl
  Intercept name          : auth-depl
  State                   : ACTIVE
  Workload kind           : Deployment
  Destination             : 127.0.0.1:8000
  Service Port Identifier : 3000/TCP
  Volume Mount Point      : /tmp/telfs-1680244885
  Intercepting            : all TCP connections
```

## 3. Run the Service Locally

Switch to your local service directory and start the server on port 8000:

```bash theme={null}
cd ~/telepresence/auth
npm install
npm run dev
```

Ensure your Express app listens on port 8000:

```javascript theme={null}
// index.js
const express = require("express");
const app = express();
const port = 8000;

app.get("/", (req, res) => {
  res.json({ message: "auth service running locally via Telepresence" });
});

app.listen(port, () => {
  console.log(`Auth service listening on port ${port}`);
});
```

## 4. Verify the Intercept

Use `curl` to hit the Kubernetes service name. Telepresence will route this to your local process:

```bash theme={null}
curl http://auth-service:3000
```

Expected response:

```json theme={null}
{"message":"auth service running locally via Telepresence"}
```

## 5. Inspect the Pod

Observe both the original container and Telepresence’s traffic agent:

```bash theme={null}
POD_NAME=$(kubectl get pod -l app=auth -o jsonpath='{.items[0].metadata.name}')
kubectl describe pod $POD_NAME
```

Look for two containers:

* **auth** (port 3000/TCP)
* **traffic-agent** (port 9900/TCP)

## 6. Remove the Intercept

When you’re done debugging, clear the intercept:

```bash theme={null}
telepresence leave auth-depl
telepresence list
# Should report: No active intercepts
```

## 7. Switch to the Products Service

1. Stop your local auth service (`Ctrl+C`)

2. List deployments again:

   ```bash theme={null}
   kubectl get deployment
   ```

3. Intercept the products deployment:

   ```bash theme={null}
   telepresence intercept products-depl -p 8000:3000
   ```

4. Run the products service locally:

   ```bash theme={null}
   cd ~/telepresence/products
   npm install
   npm run dev
   ```

5. Verify with:

   ```bash theme={null}
   curl "http://products-service:3000/?product_ids=1,2,3"
   ```

## 8. Debugging an Error

If your request hangs and you see:

```plaintext theme={null}
TypeError: Failed to parse URL from undefined?product_ids=1,2,3
```

Inspect your route handler:

```javascript theme={null}
app.get("/", async (req, res) => {
  try {
    const productIds = req.query.product_ids;
    const idsArray = productIds.split(",").map(id => parseInt(id, 10));
    const response = await fetch(`${apiURL}?product_ids=${idsArray.join(",")}`);
    // ...
  } catch (error) {
    console.error(error);
  }
});
```

<Callout icon="triangle-alert">
  `apiURL` is undefined locally because the environment variable from the Pod isn’t set in your shell.
</Callout>

## 9. Import Environment Variables

To mirror the Pod’s settings, pull the env vars into your local shell:

```bash theme={null}
# Fetch one of the app pods
POD_NAME=$(kubectl get pod -l app=products -o jsonpath='{.items[0].metadata.name}')
# Export all environment variables from the container to your local session
kubectl exec $POD_NAME -- printenv | grep API_URL | sed 's/^/export /' > pod-env.sh
source pod-env.sh
```

Now restart your local service so it picks up `API_URL` and any other Pod-specific variables.

## Links and References

* [Telepresence Documentation](https://www.telepresence.io/docs/)
* [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Express.js Guide](https://expressjs.com/)
* [Docker Hub: sanjeevkt720/telepresence-auth](https://hub.docker.com/r/sanjeevkt720/telepresence-auth)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/telepresence-for-kubernetes/module/0eb5dcb6-2e2a-40d9-9caa-bd3149741aeb/lesson/93238627-79c8-49f3-b86d-cdff5e1a91b9" />
</CardGroup>


# Demo Telepresence with Docker

Source: https://notes.kodekloud.com/docs/Telepresence-For-Kubernetes/Telepresence-For-Kubernetes/Demo-Telepresence-with-Docker/page

Learn to run the Telepresence daemon in a Docker container without modifying the host’s network configuration or requiring admin privileges.

In this guide, you'll learn how to run the Telepresence daemon inside a Docker container. This method avoids modifications to the host’s network configuration and does not require admin privileges.

## Table of Contents

* [1. Run Telepresence in Docker](#1-run-telepresence-in-docker)
* [2. Intercepting the Auth Service](#2-intercepting-the-auth-service)
* [3. Intercepting the Products Service](#3-intercepting-the-products-service)
* [4. Hot-Reload with Bind Mounts](#4-hot-reload-with-bind-mounts)
* [5. Automatic Image Build with `--docker-build`](#5-automatic-image-build-with--docker-build)
* [6. References](#6-references)

***

## 1. Run Telepresence in Docker

First, ensure any existing Telepresence session is terminated, then start a new session with the daemon running inside a Docker container.

```bash theme={null}
telepresence quit
telepresence connect --docker
