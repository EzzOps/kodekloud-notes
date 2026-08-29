# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
    component: frontend
spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports:
        - containerPort: 80
```

2. **Define the NodePort Service**, matching the Pod labels:

```yaml theme={null}
# service-definition.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: NodePort
  selector:
    app: myapp
    component: frontend
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30008
```

3. **Deploy and Verify**:

```bash theme={null}
kubectl apply -f pod-definition.yaml
kubectl apply -f service-definition.yaml
kubectl get svc
```

Expected output:

```text theme={null}
NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes       ClusterIP   10.96.0.1        <none>        443/TCP          16d
myapp-service    NodePort    10.106.127.123   <none>        80:30008/TCP     5m
```

Access the application:

```bash theme={null}
curl http://192.168.1.2:30008
<html>
  <head><title>Welcome to nginx!</title></head>
  <body><h1>Welcome to nginx!</h1></body>
</html>
```

> **triangle-alert** Exposing high ports on Nodes can pose security risks. Ensure proper firewall rules and network policies are in place.

## Scaling with Multiple Pods and Nodes

In production, you’ll run multiple Pod replicas for high availability. A NodePort Service automatically load-balances incoming traffic across all Pods that match its selector, even when spread across multiple Nodes.

![The image illustrates a Kubernetes NodePort service setup, showing how a user connects to a service that routes traffic to different pods across multiple nodes.](https://kodekloud.com/kk-media/image/upload/v1752874035/notes-assets/images/Docker-Certified-Associate-Exam-Course-Services-NodePort/kubernetes-nodeport-service-setup-2.jpg)

Simply scale your Deployment or Pod replicas:

```bash theme={null}
kubectl scale deployment myapp-deployment --replicas=3
```

Now, requests to any Node at `NodeIP:30008` are distributed across all 3 Pods.

## Summary

* **NodePort Services** expose Pod ports on each Node for external access.
* Key fields: `type: NodePort`, `port`, `targetPort`, and `nodePort`.
* Match Services to Pods via label `selector`.
* Kubernetes handles load balancing across Pods and Nodes automatically.

Next, explore the demo to see NodePort Services in action!

## Links and References

* [Kubernetes Services Documentation](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Exposing Services in Kubernetes](https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/)
* [Kubernetes API Reference: Service](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#service-v1-core)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/9132fc61-317f-41b7-854e-1c33494a9112)


# Storage Classes

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Storage-Classes/page

This article explores how StorageClasses enable dynamic volume provisioning in Kubernetes, automating workflows previously managed through static provisioning.

In this lesson, we’ll explore how **StorageClasses** enable dynamic volume provisioning in Kubernetes. If you’re familiar with static provisioning—where you manually create cloud disks and bind them via PersistentVolumes (PVs) and PersistentVolumeClaims (PVCs)—you’ll see how StorageClasses automate this workflow.

***

## Table of Contents

* [Static Provisioning Recap](#static-provisioning-recap)
* [Dynamic Provisioning with StorageClass](#dynamic-provisioning-with-storageclass)
* [StorageClass Definition](#storageclass-definition)
* [Using a Dynamic PVC and Pod](#using-a-dynamic-pvc-and-pod)
* [Comparing Provisioning Methods](#comparing-provisioning-methods)
* [Customizing StorageClass Parameters](#customizing-storageclass-parameters)
* [Defining Service Tiers](#defining-service-tiers)
* [Links and References](#links-and-references)

***

## Static Provisioning Recap

With **static provisioning**, you manually create the underlying cloud disk before you define a PV:

```bash theme={null}
gcloud beta compute disks create \
  --size=1GB \
  --region=us-east1 \
  pd-disk
```

Then you define:

```yaml theme={null}
