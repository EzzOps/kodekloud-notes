# Deploy a simple BusyBox pod with a single replica
kubectl run hello-minikube --image=busybox --replicas=1

# Verify nodes and cluster
kubectl get nodes
kubectl cluster-info

# Scale up your application
kubectl scale deployment hello-minikube --replicas=3

# Perform a rolling update
kubectl set image deployment/hello-minikube hello-minikube=busybox:1.1 --record

# Roll back if needed
kubectl rollout undo deployment/hello-minikube
```

<Callout icon="lightbulb">
  You can also configure **Horizontal Pod Autoscaler** to automatically adjust replica counts based on CPU or custom metrics. See [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) for details.
</Callout>

***

Ready to dive deeper? Explore our in-depth Kubernetes courses to master topics like Networking, Storage, Security, and become a certified Kubernetes Administrator (CKA).

## Links and References

* [Kubernetes Official Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/c7a6816c-f8f7-4a9d-9764-a29c20ae9094" />
</CardGroup>


# Liveness Probes

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Liveness-Probes/page

Liveness probes in Kubernetes check container health, automatically restarting unresponsive applications to maintain availability without manual intervention.

In Kubernetes, **liveness probes** periodically check whether a container is still running correctly. If a probe fails, Kubernetes kills and restarts the container, restoring application availability without manual intervention.

## Basic Docker Behavior

When you run an application in Docker, any crash stops the container until you restart it manually:

```bash theme={null}
docker run nginx
```

If the `nginx` process crashes:

```bash theme={null}
docker ps -a
```

```text theme={null}
CONTAINER ID        IMAGE    CREATED         STATUS                     PORTS
45aacca36850        nginx    43 seconds ago  Exited (1) 41 seconds ago
```

## Kubernetes Automatic Restarts

Kubernetes continuously monitors container exit codes and restarts crashed containers automatically:

```bash theme={null}
kubectl run nginx --image=nginx
kubectl get pods
```

```text theme={null}
NAME        READY   STATUS      RESTARTS   AGE
nginx-pod   0/1     Completed   1          1d
```

Each time the container exits unexpectedly, the **RESTARTS** count increments. However, if an application stays running but becomes unresponsive (for example, trapped in an infinite loop), Kubernetes still considers it healthy—until you explicitly tell it how to check deeper.

<Callout icon="triangle-alert">
  Without a liveness probe, Kubernetes **cannot** detect hung or unresponsive applications that have not exited.
</Callout>

## Introducing Liveness Probes

A **liveness probe** defines how Kubernetes determines container health. You choose one of three probe types:

| Probe Type | Use Case               | Configuration Snippet            |
| ---------- | ---------------------- | -------------------------------- |
| HTTP GET   | Web services           | `httpGet` with `path` and `port` |
| TCP Socket | TCP-based protocols    | `tcpSocket` with `port`          |
| Exec       | Custom commands/checks | `exec` with a `command` array    |

When a container fails its liveness probe, Kubernetes restarts it automatically.

### HTTP Liveness Probe Example

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
spec:
  containers:
    - name: simple-webapp
      image: simple-webapp
      ports:
        - containerPort: 8080
      livenessProbe:
        httpGet:
          path: /api/healthy
          port: 8080
        initialDelaySeconds: 15
        periodSeconds: 10
        failureThreshold: 3
```

Explanation:

1. `initialDelaySeconds: 15`\
   Waits 15 seconds before the first health check.
2. `periodSeconds: 10`\
   Probes every 10 seconds.
3. `failureThreshold: 3`\
   Restarts the container after three consecutive failures.

## Additional Probe Examples

Below are more probe configurations—applicable to both **liveness** and **readiness** probes:

```yaml theme={null}
readinessProbe:
  httpGet:
    path: /api/ready
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 8
---
readinessProbe:
  tcpSocket:
    port: 3306
---
readinessProbe:
  exec:
    command:
      - cat
      - /app/is_ready
```

By leveraging these probe types, you ensure Kubernetes can detect both crashed and unresponsive containers, automatically restoring service availability.

## Links and References

* [Kubernetes Probes Documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
* [Pods in Kubernetes Basics](https://kubernetes.io/docs/concepts/workloads/pods/pod/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/df5f3cd3-fd5d-4240-aea3-86e5ca1914de" />
</CardGroup>
