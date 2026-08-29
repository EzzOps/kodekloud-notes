# Installing HashiCorp Consul Service Mesh

Source: https://notes.kodekloud.com/docs/Linode-Kubernetes-Engine/Working-with-Linode/Installing-HashiCorp-Consul-Service-Mesh/page

This guide covers the installation of HashiCorp Consul service mesh on Kubernetes, enabling secure communication and service management.

HashiCorp Consul is a powerful service mesh solution that integrates seamlessly with Terraform and Kubernetes. In this guide, you’ll walk through installing Consul on your Kubernetes cluster to enable:

* mTLS-encrypted pod-to-pod communication
* Detailed visibility and troubleshooting for east–west traffic
* Fine-grained access control between services

Consul’s official Helm chart simplifies installation and upgrades, making it an ideal choice for modern infrastructure.

***

## Prerequisites

Ensure you have the following in place:

| Tool / Resource                          | Purpose                                 |
| ---------------------------------------- | --------------------------------------- |
| Kubernetes cluster (LKE, EKS, GKE, etc.) | Host your Consul service mesh           |
| Helm (v3+)                               | Manage and deploy the Consul Helm chart |
| `kubectl`                                | Interact with your cluster              |

***

## 1. Add the HashiCorp Helm Repository

Register the official HashiCorp charts, search for the Consul chart, and update your local index:

```bash theme={null}
helm repo add hashicorp https://helm.releases.hashicorp.com
helm search repo hashicorp/consul
helm repo update
```

Sample output:

```plaintext theme={null}
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "hashicorp" chart repository
Update Complete. *Happy Helming!*
```

***

## 2. Define Your Consul Configuration

Create a file named `consul.yaml` to customize your deployment. This example enables the UI, sidecar injection, and sets up two server replicas:

```yaml theme={null}
global:
  name: consul
  datacenter: njtest

server:
  replicas: 2
  securityContext:
    runAsNonRoot: false
    runAsUser: 0

ui:
  enabled: true

connectInject:
  enabled: true
  default: true

controller:
  enabled: true
```

| Configuration Key    | Description                                       |
| -------------------- | ------------------------------------------------- |
| `global.name`        | Unique release name for your Consul deployment    |
| `global.datacenter`  | Logical datacenter identifier                     |
| `server.replicas`    | Number of Consul server pods                      |
| `ui.enabled`         | Toggle the Consul web UI                          |
| `connectInject`      | Enable sidecar proxy injection by default         |
| `controller.enabled` | Deploys the Consul Kubernetes controller and CRDs |

***

## 3. (Optional) Review Your Directory Structure

If you keep your configurations and helper scripts together, you might have:

```bash theme={null}
cd Linode/Consul
ls
```

```plaintext theme={null}
consul.yaml
consulservicemesh.sh
```

> **lightbulb** In this lesson, we’ll run Helm commands manually rather than via the helper script.

***

## 4. Install Consul with Helm

Deploy Consul into your cluster using your custom `consul.yaml`:

```bash theme={null}
helm install consul hashicorp/consul \
  --set global.name=consul \
  -f consul.yaml
```

Sample Helm output:

```plaintext theme={null}
NAME: consul
LAST DEPLOYED: Mon Aug 14 12:34:56 2023
STATUS: deployed
NOTES:
Thank you for installing HashiCorp Consul!
To learn more:
  $ helm status consul
  $ helm get all consul
```

***

## 5. Verify the Deployment

Wait a minute for pods to initialize, then confirm they’re running:

```bash theme={null}
kubectl get pods
```

```plaintext theme={null}
NAME                                    READY   STATUS    AGE
consul-server-0                         1/1     Running   2m
consul-server-1                         1/1     Running   2m
consul-client-74426                     1/1     Running   1m
consul-connect-injector-...             1/1     Running   1m
consul-controller-...                   1/1     Running   1m
consul-webhook-cert-manager-...         1/1     Running   1m
```

List the services to find the `consul-ui` ClusterIP:

```bash theme={null}
kubectl get svc
```

***

## 6. Access the Consul Web UI

Forward the UI port to your local machine:

```bash theme={null}
kubectl port-forward service/consul-ui 18500:80 --address 0.0.0.0
```

```plaintext theme={null}
Forwarding from 0.0.0.0:18500 -> 8500
```

Open your browser and navigate to:

```text theme={null}
http://localhost:18500
```

You should now see the Consul web interface, confirming your service mesh is up and running.

> **triangle-alert** Avoid exposing the Consul UI to the public internet. Use secure tunnels or VPNs for production environments.

***

Congratulations! You’ve successfully installed and accessed HashiCorp Consul as a service mesh on Kubernetes.

***

## Links and References

* [Consul Overview](https://www.consul.io/docs)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Helm Documentation](https://helm.sh/docs/)
* [Terraform Registry: Consul Provider](https://registry.terraform.io/providers/hashicorp/consul/latest)

- [Watch Video](https://learn.kodekloud.com/user/courses/linode-kubernetes-engine/module/9702fbe2-4321-41c5-87e8-8ea364da097d/lesson/6f6f2609-58c8-43f5-bd06-eb27a36da8d5)
