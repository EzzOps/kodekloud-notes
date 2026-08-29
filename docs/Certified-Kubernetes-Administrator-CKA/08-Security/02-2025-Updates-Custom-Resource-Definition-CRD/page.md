# 2025 Updates Custom Resource Definition CRD

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Security/2025-Updates-Custom-Resource-Definition-CRD/page

This guide explores Custom Resource Definitions in Kubernetes, detailing standard resources, custom resources like FlightTicket, and the need for custom controllers.

In this guide, we dive into Custom Resource Definitions (CRDs) in Kubernetes, beginning with an overview of standard Kubernetes resources and controllers before extending these principles to custom resources like our FlightTicket example.

***

## Understanding Standard Kubernetes Resources and Controllers

Kubernetes relies on built-in controllers to manage standard resources. For instance, when you create a Deployment, Kubernetes stores the desired state in its etcd data store and automatically manages related ReplicaSets and Pods. The deployment controller continuously monitors the Deployment and ensures that the cluster state matches the desired configuration. Creating a Deployment with three replicas will result in three Pods being deployed.

Below is an example YAML file defining a Deployment:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      type: front-end
  template:
    metadata:
      name: myapp-pod
      labels:
        type: front-end
    spec:
      containers:
        - image: nginx
```

After saving the above content as `deployment.yml`, run the following commands to create, view, and delete the Deployment:

```bash theme={null}
kubectl create -f deployment.yml
