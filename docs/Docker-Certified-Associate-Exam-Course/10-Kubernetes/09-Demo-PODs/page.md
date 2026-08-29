# Demo PODs

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Demo-PODs/page

This tutorial covers deploying an NGINX Pod to a Minikube cluster using kubectl, including creation, status checking, and detailed inspection.

In this tutorial, we’ll deploy a Kubernetes Pod named `nginx` to a Minikube cluster using `kubectl`. You’ll learn how to create the Pod, inspect its status, view detailed descriptions, and retrieve extended information. Let’s get started!

## Prerequisites

* A running Minikube cluster (`minikube start`)
* `kubectl` configured to communicate with your Minikube context
* Internet access to pull the `nginx` image from [Docker Hub](https://hub.docker.com/)

## 1. Create a Pod with `kubectl run`

Execute the following command to launch a Pod named `nginx` using the official NGINX image:

```bash theme={null}
kubectl run nginx --image=nginx
```

Here:

* `nginx` is both the Pod name and the container image.
* You can append a tag (for example, `nginx:1.21`) or a custom registry URL if needed.

## 2. Check Pod Status

After a moment, confirm the Pod has been created:

```bash theme={null}
kubectl get pods
```

Example output:

```bash theme={null}
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          3s
```

| Column   | Description                                      |
| -------- | ------------------------------------------------ |
| NAME     | The Pod’s name (unique within its namespace).    |
| READY    | Number of containers ready vs. total containers. |
| STATUS   | Current phase (e.g., Pending, Running).          |
| RESTARTS | Count of container restarts.                     |
| AGE      | Time elapsed since the Pod was created.          |

## 3. Describe a Pod

To inspect detailed metadata, events, and container status:

```bash theme={null}
kubectl describe pod nginx
```

You’ll see sections like metadata, labels, node assignment, IP addresses, and container details:

```bash theme={null}
Name:         nginx
Namespace:    default
Node:         minikube/192.168.99.100
Start Time:   Sat, 11 Jul 2020 00:49:39 -0400
Labels:       run=nginx
Status:       Running
IP:           172.17.0.3
IPs:
  IP:           172.17.0.3
Containers:
  nginx:
    Container ID:   docker://987785b312ad2e38c77132300f8709b8a027566462c2d18634ff13b34de25479
    Image:          nginx
```

<Callout icon="lightbulb">
  Pod networking and IP addressing will be explored in detail in a later lesson.
</Callout>

### Events Log

Scrolling further down in the description reveals the event sequence:

```bash theme={null}
Events:
  Type     Reason      Age   From                    Message
  ----     ------      ----  ----                    -------
  Normal   Scheduled   46s   default-scheduler       Successfully assigned default/nginx to minikube
  Normal   Pulling     45s   kubelet, minikube       Pulling image "nginx"
  Normal   Pulled      44s   kubelet, minikube       Successfully pulled image "nginx"
  Normal   Created     44s   kubelet, minikube       Created container nginx
  Normal   Started     44s   kubelet, minikube       Started container nginx
```

## 4. Get Extended (“Wide”) Output

To include the node name and the Pod’s IP address in your listing:

```bash theme={null}
kubectl get pods -o wide
```

Sample output:

```bash theme={null}
NAME    READY   STATUS    RESTARTS   AGE     IP          NODE      NOMINATED NODE
nginx   1/1     Running   0          2m28s   172.17.0.3  minikube   <none>
```

Every Pod receives a unique internal IP within the cluster network.

***

In this lesson, you deployed an NGINX Pod on Minikube, inspected its state, and viewed detailed and wide outputs. Next, we’ll define Pods declaratively using YAML manifests.

## Links and References

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
* [Docker Hub: NGINX Image](https://hub.docker.com/_/nginx)
* [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/693f940b-bbe9-42e8-adfc-0150deb5a0b1" />
</CardGroup>
