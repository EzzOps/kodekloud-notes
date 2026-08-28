# ...other variables
```

<Callout icon="lightbulb">
  You can choose any filename for the environment file (e.g., `dev.env` or `products.env`). Just update your intercept command accordingly.
</Callout>

## 4. Load the `.env` File in Your Local Process

Most development tools support dotenv files out of the box. For example, with a Node.js application you can:

```bash theme={null}
npm install dotenv
```

```js theme={null}
// index.js
require('dotenv').config();
console.log('API URL:', process.env.API_URL);
```

Or, if you prefer a one-liner in Bash:

```bash theme={null}
export $(grep -v '^#' .env | xargs) && npm start
```

<Callout icon="triangle-alert">
  Avoid committing your `.env` file to version control if it contains sensitive data. Add it to your `.gitignore` instead.
</Callout>

## 5. Summary of Key Flags

| Flag         | Description                                  | Example            |
| ------------ | -------------------------------------------- | ------------------ |
| `--port`     | Forward remote port to local                 | `--port 8000:3000` |
| `--env-file` | Dump container environment variables to file | `--env-file .env`  |

## Links and References

* [Telepresence Documentation](https://www.telepresence.io/docs/)
* [GitHub: telepresence-command-reference](https://github.com/telepresenceio/telepresence)
* [dotenv npm package](https://www.npmjs.com/package/dotenv)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/telepresence-for-kubernetes/module/0eb5dcb6-2e2a-40d9-9caa-bd3149741aeb/lesson/d6bda8d0-e3f3-4f40-a5ad-3d63a3fe86b2" />
</CardGroup>


# How does Telepresence Work

Source: https://notes.kodekloud.com/docs/Telepresence-For-Kubernetes/Telepresence-For-Kubernetes/How-does-Telepresence-Work/page

Telepresence enables local development and debugging by creating a seamless connection to a remote Kubernetes cluster through a bi-directional network tunnel.

Telepresence lets you develop and debug services locally while connecting seamlessly to a remote Kubernetes cluster. By creating a bi-directional network tunnel, it feels as if your workstation is inside the cluster—eliminating the need to build container images or exec into pods for iterative development.

## Architecture Overview

| Component           | Location           | Responsibility                                                                     |
| ------------------- | ------------------ | ---------------------------------------------------------------------------------- |
| Telepresence CLI    | Local machine      | Provides commands to connect, intercept services, and manage the Traffic Manager.  |
| Traffic Manager     | Kubernetes cluster | Coordinates traffic routing between the cluster and your workstation.              |
| Telepresence Daemon | Local machine      | Maintains a persistent tunnel and reroutes intercepted traffic to local processes. |

When you issue an intercept, the Traffic Manager injects a **Traffic Agent** sidecar into the target pod. Incoming requests for that pod are proxied through the agent over the tunnel to your local service.

<Frame>
  ![The image illustrates the Telepresence architecture, showing a laptop connected via a tunnel to a backend pod with a traffic manager, traffic agent, and frontend components.](https://kodekloud.com/kk-media/image/upload/v1752884090/notes-assets/images/Telepresence-For-Kubernetes-How-does-Telepresence-Work/telepresence-architecture-laptop-pod.jpg)
</Frame>

## Prerequisites

<Callout icon="lightbulb">
  Before you begin, confirm you have:

  * Network access to your Kubernetes cluster
  * `kubectl` configured with the correct context
  * Permissions to install or upgrade cluster components (or a colleague who can)
</Callout>

<Frame>
  ![The image lists three requirements: network connection, kubectl access to a cluster, and permissions to deploy a traffic manager to the cluster.](https://kodekloud.com/kk-media/image/upload/v1752884091/notes-assets/images/Telepresence-For-Kubernetes-How-does-Telepresence-Work/traffic-manager-deployment-requirements.jpg)
</Frame>

## Installation

### 1. Install the Telepresence CLI

Download the latest Telepresence binary and make it executable:

```bash theme={null}
sudo curl -FL \
  https://app.getambassador.io/download/tel2oss/releases/download/v2.20.0/telepresence-linux-amd64 \
  -o /usr/local/bin/telepresence
sudo chmod a+x /usr/local/bin/telepresence
```

### 2. Deploy the Traffic Manager

Use the built-in Helm support to install:

```bash theme={null}
telepresence helm install
```

This command provisions the Traffic Manager and necessary RBAC resources in your cluster.

## Establishing the Connection

Run the following to start the daemon and open the tunnel:

```bash theme={null}
telepresence connect
```

This will:

* Launch the local Telepresence daemon
* Connect to the Traffic Manager in your cluster
* Configure routing so cluster pod and service IPs resolve locally

<Frame>
  ![The image illustrates a "Telepresence connect" setup, showing a laptop connected via a tunnel to a Kubernetes cluster with pods and services, including Kube-DNS.](https://kodekloud.com/kk-media/image/upload/v1752884093/notes-assets/images/Telepresence-For-Kubernetes-How-does-Telepresence-Work/telepresence-connect-kubernetes-setup.jpg)
</Frame>

## Common Telepresence Commands

| Command                     | Description                                                      |
| --------------------------- | ---------------------------------------------------------------- |
| telepresence connect        | Establishes the network tunnel                                   |
| telepresence status         | Displays current connection and routing status                   |
| telepresence intercept NAME | Redirects traffic for a Kubernetes service to your local process |

## Verifying Your Connection

Check connection health and routing:

```bash theme={null}
telepresence status
```

Example output:

```plaintext theme={null}
OSS User Daemon: Running
Version              : 2.20.0
Status               : Connected
Subnets (2)          : 10.100.0.0/16, 192.168.0.0/18
...
OSS Traffic Manager: Connected
```

Ensure **Status: Connected** and the **Subnets** match your cluster’s pod CIDR and service network.

## Local Routing

Telepresence adds local routes for cluster IP ranges. View them with:

```bash theme={null}
ip route
```

Sample:

```plaintext theme={null}
10.100.0.0/16 dev tel1 scope link
192.168.0.0/18 dev tel1 scope link
```

Traffic on these subnets is directed through the `tel1` tunnel interface.

## Using Cluster Services Locally

With the tunnel in place, resolve and call internal services as if you were in the cluster:

```bash theme={null}
nslookup service-a
curl http://service-a:3000
curl http://172.16.0.1
```

This approach removes the overhead of building images or managing port-forwards during development.

## Links and References

* [Telepresence Documentation](https://www.telepresence.io/docs/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Helm Charts Overview](https://helm.sh/docs/topics/charts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/telepresence-for-kubernetes/module/0eb5dcb6-2e2a-40d9-9caa-bd3149741aeb/lesson/46e22602-bab3-4c01-892a-0eabe2aab70e" />
</CardGroup>
