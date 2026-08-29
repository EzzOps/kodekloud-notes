# Launching Telepresence User Daemon
# Connected to context arn:aws:eks:us-east-1:195725640053:cluster/telepresence, namespace default (...)
```

<Callout icon="lightbulb">
  Make sure your Kubernetes context and namespace are correctly configured before running `telepresence connect --docker`.
</Callout>

### Verify Telepresence Status

```bash theme={null}
telepresence status
# OSS Daemon in container arn:aws:eks:us-east-1:195725640053:cluster_telepresence-default-cn: Running
# Version            : 2.20.0
# Status             : Connected
# Kubernetes context : arn:aws:eks:us-east-1:195725640053:cluster/telepresence
# ... (additional info) ...
```

### Confirm the Daemon Container

```bash theme={null}
docker ps
# CONTAINER ID   IMAGE                                        COMMAND                  CREATED         STATUS         PORTS
# 469b3f77cdcb   ghcr.io/telepresenceio/telepresence:2.20.0   "telepresence connec…"   18 seconds ago  Up 17 seconds  127.0.0.1:42715->42715/tcp   tp-arn_aws_eks_us-east-1_195725640053_cluster_telepresence-default-cn
```

***

## 2. Intercepting the Auth Service

### 2.1 Inspect Cluster Services

```bash theme={null}
kubectl get svc
# NAME               TYPE           CLUSTER-IP      PORT(S)          AGE
# auth-service       ClusterIP      10.100.10.52    3000/TCP         4h57m
# inventory-service  ClusterIP      10.100.246.69   3000/TCP         5h34m
curl http://auth-service:3000
# {"message":"this is the auth service"}
```

### 2.2 Update Local Auth Service

In your `auth/index.js`:

```javascript theme={null}
const express = require("express");
const app = express();
const port = 8000;

app.get("/", (req, res) => {
  res.json({ message: "this is the auth service running on my machine" });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
```

### 2.3 Build the Auth Docker Image

```bash theme={null}
cd auth
docker build -t telepresence-auth:v2 .
# ... build output ...
```

### 2.4 Create the Telepresence Intercept

```bash theme={null}
telepresence intercept auth-depl \
  --port 8000 \
  --docker-run telepresence-auth:v2
# Using Deployment auth-depl
# Intercept name: auth-depl
# State: ACTIVE
# Workload kind: Deployment
# Destination: 127.0.0.1:8000
# Service Port Identifier: 3000/TCP
# Intercepting: all TCP connections
# Example app listening on port 8000
```

### 2.5 Verify the Auth Container

```bash theme={null}
docker ps
# CONTAINER ID   IMAGE                     NAMES   COMMAND   STATUS
# ...            telepresence-auth:v2      ...     ...       Up ...
```

***

## 3. Intercepting the Products Service

### 3.1 Modify the Products Endpoint

Edit `products/index.js` to confirm local behavior:

```javascript theme={null}
app.get("/", async (req, res) => {
  // ... fetch data ...
  res.json({ data: productsWithInventory, message: "running on container on local machine" });
});
```

### 3.2 Build and Intercept

```bash theme={null}
cd products
docker build -t my-test-image .
telepresence intercept products-depl \
  --port 8000 \
  --docker-run -- my-test-image
# Using Deployment products-depl
# Intercept name: products-depl
# ...
# Example app listening on port 8000
```

### 3.3 Test the Products Intercept

```bash theme={null}
kubectl get svc products-service
curl http://a2517fc7ee41999dd7c47eed9f866-376507947.us-east-1.elb.amazonaws.com:3000/?product_ids=1,2,3
# {"data":[...],"message":"running on container on local machine"}
```

***

## 4. Hot-Reload with Bind Mounts

Rebuilding images after each change can slow development. Instead, use a bind mount with Nodemon for hot-reload.

### 4.1 Dockerfile for Hot-Reload

```dockerfile theme={null}
FROM node:22
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY .
```

### 4.2 Update `package.json`

```json theme={null}
{
  "scripts": {
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "dotenv": "^16.4.5"
  }
}
```

### 4.3 Run with Bind Mount and Nodemon

```bash theme={null}
telepresence intercept products-depl \
  --port 8000 \
  --docker-run -- \
    -v $(pwd):/usr/src/app my-test-image npm run dev
# [nodemon] 3.1.7
# [nodemon] to restart at any time, enter `rs`
# [nodemon] starting `node index.js`
# Example app listening on port 8000
```

Any change in the `products` directory now triggers an auto-reload inside the container.

***

## 5. Automatic Image Build with `--docker-build`

Skip manual builds by letting Telepresence build your image during intercept:

```bash theme={null}
telepresence intercept products-depl \
  --port 8000 \
  --docker-build products \
  --docker-build-opt tag=my-debug-image \
  -- my-debug-image
# Using Deployment products-depl
# Intercept name: products-depl
# State: ACTIVE
# ...
# Example app listening on port 8000
```

This command:

* Builds the image from the `products/` directory
* Tags it as `my-debug-image`
* Starts the intercept in one step

***

## 6. References

* [Telepresence CLI Reference](https://www.telepresence.io/docs/latest/reference/cli/)
* [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Docker Engine CLI](https://docs.docker.com/engine/reference/commandline/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/telepresence-for-kubernetes/module/0eb5dcb6-2e2a-40d9-9caa-bd3149741aeb/lesson/409f313b-7c84-4815-b0ba-6973f5a1975f" />
</CardGroup>


# Demo Volumes

Source: https://notes.kodekloud.com/docs/Telepresence-For-Kubernetes/Telepresence-For-Kubernetes/Demo-Volumes/page

Intercept a Kubernetes pod using Telepresence, mount its ConfigMap volume locally, and access configuration data as if the service were running in-cluster.

Intercept a Kubernetes pod using Telepresence, mount its ConfigMap volume on your local machine, and access configuration data as if the service were running in-cluster.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Node.js Service Example](#nodejs-service-example)
* [Kubernetes Deployment with ConfigMap Volume](#kubernetes-deployment-with-configmap-volume)
* [ConfigMap Definition](#configmap-definition)
* [Intercepting with Telepresence and Mounting Volumes](#intercepting-with-telepresence-and-mounting-volumes)
* [Exploring the Mounted Volume](#exploring-the-mounted-volume)
* [Customizing the Local Mount Path](#customizing-the-local-mount-path)
* [References](#references)

## Prerequisites

* Kubernetes cluster access with `kubectl` configured
* Telepresence installed
* A local `.env` file for environment variables

<Callout icon="lightbulb">
  Ensure your `kubectl` context is pointing to the intended cluster before starting the intercept.
</Callout>

## Node.js Service Example

The **products** service is an Express.js app that reads `API_URL` from environment variables:

```javascript theme={null}
require('dotenv').config({ override: true });
const express = require("express");
const app = express();
const port = 8000;

const apiURL = process.env.API_URL;
console.log("API_URL:", apiURL);

const products = [
  {
    id: 1,
    name: "iPhone 14",
    price: 900,
    category: "electronics",
    onSale: false,
  },
];

app.get("/products", (req, res) => {
  res.json(products);
});

app.listen(port, () => {
  console.log(`Products service listening on port ${port}`);
});
```

## Kubernetes Deployment with ConfigMap Volume

Deploy the `products-depl` Deployment and mount a ConfigMap called `db-info` at `/tmp`:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: products-depl
spec:
  selector:
    matchLabels:
      app: products
  template:
    metadata:
      labels:
        app: products
    spec:
      volumes:
        - name: db-config
          configMap:
            name: db-info
      containers:
        - name: products
          image: sanjeevkt720/telepresence-products
          imagePullPolicy: Always
          ports:
            - containerPort: 8000
              name: web
          volumeMounts:
            - name: db-config
              mountPath: /tmp
          env:
            - name: API_URL
              value: "http://api.example.com"
```

## ConfigMap Definition

Define your database connection details in a ConfigMap:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-info
data:
  DB_HOST: "prod.db"
  DB_USERNAME: "myusername123"
  DB_PASSWORD: "mypassword123"
```

| Key          | Value         |
| ------------ | ------------- |
| DB\_HOST     | prod.db       |
| DB\_USERNAME | myusername123 |
| DB\_PASSWORD | mypassword123 |

## Intercepting with Telepresence and Mounting Volumes

1. Check for existing intercepts:
   ```bash theme={null}
   telepresence list
   ```
2. Create an intercept on port 8000, inject your `.env`, and mount the pod’s volumes:
   ```bash theme={null}
   telepresence intercept products-depl \
     --port 8000 \
     --env-file .env \
     --mount
   ```

<Callout icon="triangle-alert">
  Redirecting service traffic through your local machine may impact production workloads. Proceed with caution.
</Callout>

Example output (identifiers will vary):

```bash theme={null}
Using Deployment products-depl
  Intercept name          : products-depl
  State                   : ACTIVE
  Workload kind           : Deployment
  Destination             : 127.0.0.1:8000
  Service Port Identifier : 8000/TCP
  Volume Mount Point      : /tmp/telfs-2391723209
  Intercepting            : all TCP connections
```

## Exploring the Mounted Volume

In a new terminal:

```bash theme={null}
cd /tmp/telfs-2391723209/tmp
ls
cat DB_HOST
