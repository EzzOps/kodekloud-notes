# Stateful Sets Introduction

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/State-Persistence/Stateful-Sets-Introduction/page

This article explores StatefulSets in Kubernetes, detailing their use cases, differences from Deployments, and management strategies.

In this lesson, we explore StatefulSets in Kubernetes and explain when to use them instead of Deployments. StatefulSets are ideal for applications that require:

* Ordered startup and shutdown
* Stable network identities
* Consistent storage provisioning

When your application instances need to start in a specific order or require persistent identities between restarts, opting for a StatefulSet is the right choice.

<Callout icon="lightbulb">
  A StatefulSet is similar to a Deployment in that you define it via a YAML file with a Pod template. The main differences are:

  * Change the kind from Deployment to StatefulSet (note the uppercase “S”).
  * Include the additional field 'serviceName' to specify a headless service.
</Callout>

## Converting a Deployment to a StatefulSet

Consider the following example of a MySQL Deployment:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql
```

To convert this Deployment into a StatefulSet, modify the YAML file by updating the kind and adding the `serviceName` field:

```yaml theme={null}
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  serviceName: mysql-h
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql
```

When you create a StatefulSet using this file, Kubernetes will:

* Deploy Pods one at a time in an ordered, graceful manner.
* Assign a stable, unique DNS record to each Pod, allowing other applications to refer to them reliably.
* Scale Pods sequentially, where each new Pod starts only after the previous one is ready.

This ordered behavior is particularly beneficial for applications like MySQL databases, where preserving state and order is critical.

## Creating and Managing a StatefulSet

You can use standard Kubernetes commands to create and scale your StatefulSet. For example:

```bash theme={null}
kubectl create -f statefulset-definition.yml
kubectl scale statefulset mysql --replicas=5
