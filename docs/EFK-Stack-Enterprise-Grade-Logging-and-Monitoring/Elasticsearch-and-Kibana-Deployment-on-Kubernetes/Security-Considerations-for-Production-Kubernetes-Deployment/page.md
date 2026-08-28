# Cloning into 'efk-stack'...
# remote: Enumerating objects: 134, done.
# remote: Counting objects: 100% (134/134), done.
# remote: Compressing objects: 100% (114/114), done.
# remote: Total 134 (delta 60), reused 63 (delta 14), pack-reused 0
# Receiving objects: 100% (134/134), 62.75 KiB | 2.24 MiB/s, done.
kubectl taint node controlplane node-role.kubernetes.io/control-plane- untainted

kubectl create namespace efk
kubectl config set-context --current --namespace=efk
# Context "kubernetes-admin@kubernetes" modified.
```

Next, navigate into the repository and change your working directory to `elasticsearch-kibana/scaling-ek-stack`. This folder contains four essential files. You can list the contents using:

```bash theme={null}
ls -lrt
```

```plaintext theme={null}
total 16
-rw-r--r-- 1 root    697 Aug  8 14:06 pv.yml
-rw-r--r-- 1 root    791 Aug  8 14:06 kibana.yml
-rw-r--r-- 1 root   1619 Aug  8 14:06 es.yml
-rw-r--r-- 1 root    207 Aug  8 14:06 config-map.yml
```

## Configuring Persistent Volumes

In the following step, review the `pv.yml` file. This manifest creates three Persistent Volumes (PV), each associated with a different node in the cluster (e.g., controlplane, node01, and node02). In enterprise-scale environments, dedicating specific nodes entirely for Elasticsearch storage can optimize performance and scalability.

```yaml theme={null}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-elasticsearch-controlplane
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/elasticsearch-controlplane
  storageClassName: manual
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-elasticsearch-node01
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/elasticsearch-node01
  storageClassName: manual
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-elasticsearch-node02
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/elasticsearch-node02
  storageClassName: manual
```

<Callout icon="lightbulb">
  These persistent volumes ensure that each Elasticsearch pod has its dedicated storage, which is crucial for data persistence in a distributed database architecture.
</Callout>

## Deploying the Elasticsearch StatefulSet

The `es.yml` file is used to define a StatefulSet deployment for Elasticsearch. This configuration deploys three replicas of Elasticsearch across different nodes using node affinity rules:

```yaml theme={null}
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
  namespace: efk
spec:
  serviceName: "elasticsearch"
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      affinity:
        nodeAffinity:
          [SECRET_REDACTED]:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: kubernetes.io/hostname
                    operator: In
                    values:
                      - controlplane
                      - node01
                      - node02
      containers:
        - name: elasticsearch
          image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
          ports:
            - containerPort: 9200
              name: port1
            - containerPort: 9300
              name: port2
```

By configuring three replicas, you ensure that Elasticsearch pods are distributed across distinct nodes. The accompanying persistent volumes from the previous step guarantee data persistence for each replica. If you plan to scale out further, remember that each additional replica must be paired with its own persistent volume.

<Callout icon="triangle-alert">
  When scaling horizontally, ensure that your infrastructure can support the increased number of persistent volumes and consider adjusting resource limits to prevent issues such as out-of-memory errors.
</Callout>

The `kibana.yml` file in the same directory closely follows the configuration guidelines for Kibana, and the `config-map.yml` file is used to set up the necessary configuration map for the Elasticsearch cluster.

## Deploying and Monitoring the Stack

Deploy the complete stack by applying all the YAML manifests using the command below:

```bash theme={null}
kubectl apply -f .
```

Monitor the status of your pods with:

```bash theme={null}
kubectl get pods -w
```

A typical pod output may appear as follows:

```plaintext theme={null}
NAME                     READY   STATUS              RESTARTS   AGE
elasticsearch-0         0/1     Init:0/1            0          23s
kibana-77bc66b675-92tbq  0/1     ContainerCreating   0          0s
elasticsearch-0         1/1     Running             0          0s
elasticsearch-1         0/1     Pending             0          0s
elasticsearch-2         0/1     OOMKilled           0          56s
...
```

This output shows that during rollout, some Elasticsearch pods may initially fail due to reasons such as out-of-memory issues. However, each Elasticsearch pod is tied to its own persistent volume, ensuring data integrity even during restarts. The Kibana service is deployed as an independent pod.

After allowing time for all services to initialize, verify that each pod is running properly:

```bash theme={null}
kubectl get pods
```

A correctly deployed stack should return a result similar to:

```plaintext theme={null}
NAME                          READY   STATUS    RESTARTS   AGE
elasticsearch-0               1/1     Running   2          45s
elasticsearch-1               1/1     Running   2          44s
elasticsearch-2               1/1     Running   2          44s
kibana-77bc66b675-92tbq       1/1     Running   0          4m5s
```

## Scaling Considerations for Elasticsearch and Kibana

This demonstration emphasizes two critical aspects of scaling:

| Scaling Type       | Description                                                                                                                                                       | Consideration                                                 |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Horizontal Scaling | Increase or decrease the number of replicas in the Elasticsearch StatefulSet to add or remove nodes from the cluster.                                             | Each replica needs an associated persistent volume.           |
| Vertical Scaling   | Adjust resource allocations (CPU and memory) in the YAML manifests to meet different workload demands or address performance issues such as out-of-memory errors. | Make sure to update resource requests and limits accordingly. |

Utilizing these scaling strategies provides a robust framework for adapting Elasticsearch and Kibana deployments to meet growing data and query workloads.

That concludes our guide on scaling Elasticsearch and Kibana in Kubernetes. Happy deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/79ef74c6-138f-4dd8-b5fb-e8a8050b59a5/lesson/dba23802-7783-4920-a505-31631dffc0c6" />
</CardGroup>


# Security Considerations for Production Kubernetes Deployment

Source: https://notes.kodekloud.com/docs/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring/Elasticsearch-and-Kibana-Deployment-on-Kubernetes/Security-Considerations-for-Production-Kubernetes-Deployment/page

This guide highlights practical strategies to safeguard the Elastic Stack within your Kubernetes environment.

Welcome to this lesson on securing your Elasticsearch and Kibana deployments on Kubernetes. As your deployment grows, ensuring a robust security posture becomes essential. This guide highlights practical strategies to safeguard the Elastic Stack within your Kubernetes environment. We will cover the following critical aspects:

1. Securing your Kubernetes cluster
2. Enabling SSL/TLS encryption
3. Implementing Elastic Stack security features
4. Restricting Elasticsearch access

***

## 1. Securing Your Kubernetes Cluster

The first step in maintaining a secure Elastic Stack is to harden your Kubernetes cluster. Implementing network policies is a fundamental practice to control pod-to-pod communication. For example, you might configure a policy that permits only the necessary interactions between Kibana and Elasticsearch pods, significantly reducing the risk of internal breaches.

<Callout icon="lightbulb">
  This section introduces the key concepts behind network policies without the need for additional diagrams.
</Callout>

***

## 2. Enabling SSL/TLS Encryption

Protecting data in transit is paramount. SSL/TLS encryption ensures that communications between nodes remain confidential and tamper-proof. Configure your Elasticsearch and Kibana settings with the appropriate certificate and key paths. Below is an example of how you can enable SSL/TLS in Kibana:

```yaml theme={null}
