# service-definition.yml
apiVersion: v1
kind: Service
metadata:
  name: back-end
spec:
  selector:
    app: myapp
    tier: back-end
  ports:
    - port: 80        # Service port exposed inside the cluster
      targetPort: 80  # Port on the container
      protocol: TCP
```

> **lightbulb** By default, `spec.type` is `ClusterIP`. If you omit it, Kubernetes will still create a ClusterIP Service unless you specify another type.

### Key Fields

| Field           | Description                                     |
| --------------- | ----------------------------------------------- |
| `metadata.name` | Name of the Service (DNS name within cluster)   |
| `spec.selector` | Labels used to identify the target Pods         |
| `spec.ports`    | List of ports the Service exposes and routes to |

## Pod Definition with Matching Labels

Ensure your Pods carry labels that match the Service’s selector:

```yaml theme={null}
# pod-definition.yml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-backend-pod
  labels:
    app: myapp
    tier: back-end
spec:
  containers:
    - name: nginx-container
      image: nginx
      ports:
        - containerPort: 80
```

## Deploying and Verifying

Apply the Service and check its status:

```bash theme={null}
kubectl apply -f service-definition.yml
kubectl get services
```

Example output:

```plain theme={null}
NAME       TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
back-end   ClusterIP   10.96.123.45   <none>        80/TCP    30s
```

Now, any Pod in the cluster can reach the back-end tier by calling:

```text theme={null}
http://back-end:80
```

Kubernetes will automatically load-balance requests across all matching Pods.

## Links and References

* [Kubernetes Services Overview](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Redis Official Site](https://redis.io/)
* [MySQL Official Site](https://www.mysql.com/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)

> **triangle-alert** Avoid mapping Service ports directly to host ports in production; use `ClusterIP` for secure, in-cluster traffic and consider `Ingress` or `LoadBalancer` types for external access.

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/ec963a0c-97e2-4614-be8f-5f141fc2d0a6)


# Services LoadBalancer

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Services-LoadBalancer/page

This article explores the Kubernetes Service type LoadBalancer, comparing it with NodePort and demonstrating cloud load balancer provisioning.

In this lesson, we’ll explore the Kubernetes Service type `LoadBalancer`. We begin with a quick recap of **NodePort**, then introduce **LoadBalancer** and demonstrate how to provision a cloud load balancer automatically.

## 1. Recap: Kubernetes NodePort Service

A **NodePort** exposes a Service on a static port (the *NodePort*) on every node in your cluster. For example, if you expose the voting app on port `31000` and the result app on port `32000`, external users can reach them via:

* http\://\<node-ip>:31000
* http\://\<node-ip>:32000

Even if your Pods run only on nodes with IPs 10.0.0.70 and 10.0.0.71, they remain accessible on the same port across all nodes in the cluster.

## 2. Limitations of NodePort

While NodePort is straightforward, it has some drawbacks:

* No single friendly URL for end users
* Manual management of external load balancer infrastructure
* Exposure of high-range ports (30000–32767)

> **triangle-alert** Managing separate load balancer VMs (HAProxy, NGINX, etc.) increases operational overhead.

## 3. Introducing the LoadBalancer Service

On supported cloud platforms (GCP, AWS, Azure), setting `type: LoadBalancer` in your Service manifest will:

1. Provision a native cloud load balancer
2. Configure forwarding rules to cluster nodes
3. Distribute traffic across Service endpoints

Here’s a sample `voting-service.yaml`:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: voting-app
spec:
  type: LoadBalancer
  selector:
    app: voting
  ports:
    - port: 80
      targetPort: 80
```

Apply it with:

```bash theme={null}
kubectl apply -f voting-service.yaml
kubectl get svc voting-app
