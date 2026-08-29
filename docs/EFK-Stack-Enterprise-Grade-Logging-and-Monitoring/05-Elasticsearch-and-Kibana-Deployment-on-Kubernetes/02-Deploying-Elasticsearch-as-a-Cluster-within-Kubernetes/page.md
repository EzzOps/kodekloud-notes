# Context "kubernetes-admin@kubernetes" modified.
git clone https://github.com/kodekloudhub/efk-stack.git
# Cloning into 'efk-stack'...
cd /root/efk-stack/elasticsearch-kibana
```

## Exploring the Repository Files

After navigating to the proper directory, list the available files to understand the repository structure. There are five configuration files present. The three critical files for Elasticsearch are:

* es-statefulset.yaml (defines the StatefulSet)
* es-service.yaml (defines the Service)
* es-pvolume.yaml (defines the Persistent Volume)

```bash theme={null}
ls -lrt
# total 4
cd efk-stack/
cd /root/efk-stack/elasticsearch-kibana

ls -lrt
# total 20
# -rw-r--r-- 1 root  root   184 Aug  6 14:18 kibana-service.yaml
# -rw-r--r-- 1 root  root   354 Aug  6 14:18 kibana-deployment.yaml
# -rw-r--r-- 1 root  root  1195 Aug  6 14:18 es-statefulset.yaml
# -rw-r--r-- 1 root  root   299 Aug  6 14:18 es-service.yaml
# -rw-r--r-- 1 root  root   185 Aug  6 14:18 es-pvolume.yaml
```

## Inspecting the Elasticsearch StatefulSet

The es-statefulset.yaml file contains the configuration for the Elasticsearch StatefulSet. This file includes metadata, pod specifications, and the Docker image version (8.13.0). It exposes ports 9200 and 9300 and sets essential environment variables, such as running in single-node mode and disabling x-pack security for demonstration purposes.

```yaml theme={null}
selector:
  matchLabels:
    app: elasticsearch
template:
  metadata:
    labels:
      app: elasticsearch
  spec:
    containers:
    - name: elasticsearch
      image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
      ports:
      - containerPort: 9200
        name: port1
      - containerPort: 9300
        name: port2
      env:
      - name: discovery.type
        value: single-node
      - name: xpack.security.enabled
        value: "false"
      volumeMounts:
      - name: es-data
        mountPath: /usr/share/elasticsearch/data
    initContainers:
    - name: fix-permissions
      image: busybox
      command: ["sh", "-c", "chown -R 1000:1000 /usr/share/elasticsearch/data"]
      securityContext:
        privileged: true
      volumeMounts:
      - name: es-data
        mountPath: /usr/share/elasticsearch/data
    volumeClaimTemplates:
    - metadata:
        name: es-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
```

Later in the same file, the persistent storage size is updated along with similar configurations. Note that the x-pack security is disabled, and the volume mount ensures persistent data storage across pod restarts.

```yaml theme={null}
metadata:
  labels:
    app: elasticsearch
spec:
  containers:
    - name: elasticsearch
      image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
      ports:
        - containerPort: 9200
          name: port1
        - containerPort: 9300
          name: port2
      env:
        - name: discovery.type
          value: single-node
        - name: xpack.security.enabled
          value: "false"
      volumeMounts:
        - name: es-data
          mountPath: /usr/share/elasticsearch/data
  initContainers:
    - name: fix-permissions
      image: busybox
      command: ["sh", "-c", "chown -R 1000:1000 /usr/share/elasticsearch/data"]
      securityContext:
        privileged: true
      volumeMounts:
        - name: es-data
          mountPath: /usr/share/elasticsearch/data
  volumeClaimTemplates:
    - metadata:
        name: es-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 5Gi
```

<Callout icon="lightbulb">
  For enhanced security in production environments, explore additional configuration options to enable robust authentication and secure data communication.
</Callout>

## Volume Mount and Persistent Storage

The StatefulSet configures an "es-data" volume mount where Elasticsearch stores its data. This mount is defined via a Persistent Volume Claim, ensuring that data persists even if the pod is restarted or recreated.

```yaml theme={null}
metadata:
  labels:
    app: elasticsearch
spec:
  containers:
    - name: elasticsearch
      image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
      ports:
        - containerPort: 9200
          name: port1
        - containerPort: 9300
          name: port2
      env:
        - name: discovery.type
          value: single-node
        - name: xpack.security.enabled
          value: "false"
      volumeMounts:
        - name: es-data
          mountPath: /usr/share/elasticsearch/data
  initContainers:
    - name: fix-permissions
      image: busybox
      command: ["sh", "-c", "chown -R 1000:1000 /usr/share/elasticsearch/data"]
      securityContext:
        privileged: true
      volumeMounts:
        - name: es-data
          mountPath: /usr/share/elasticsearch/data
  volumeClaimTemplates:
    - metadata:
        name: es-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 5Gi
```

The Persistent Volume (defined in es-pvolume.yaml) is configured to use a hostPath at "/data/elasticsearch" with a storage capacity of 5Gi and access mode "ReadWriteOnce".

```yaml theme={null}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-elasticsearch
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/elasticsearch
```

## Defining the Elasticsearch Service

The es-service.yaml file defines the Elasticsearch Service, which exposes ports 9200 and 9300. It leverages NodePort and ensures consistent metadata with the StatefulSet for proper traffic routing.

```yaml theme={null}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-elasticsearch
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/elasticsearch
---
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch
  namespace: efk
spec:
  selector:
    app: elasticsearch
  ports:
  - port: 9200
    targetPort: 9200
    protocol: TCP
    name: http
  - port: 9300
    targetPort: 9300
    protocol: TCP
    name: nodePort
```

## Deploying the Elasticsearch Stack

After reviewing all configuration files, deploy the Elasticsearch stack by applying the Persistent Volume, StatefulSet, and Service configurations. First, confirm that all necessary files are present:

```bash theme={null}
# List the files to ensure they are present
ls -lrt
# total 20
# -rw-r--r--  1 root root  184 Aug  6 14:18 kibana-service.yaml
# -rw-r--r--  1 root root  354 Aug  6 14:18 kibana-deployment.yaml
# -rw-r--r--  1 root root 1195 Aug  6 14:18 es-statefulset.yaml
# -rw-r--r--  1 root root  209 Aug  6 14:18 es-service.yaml
# -rw-r--r--  1 root root  105 Aug  6 14:18 es-pvolume.yaml
```

Apply the configuration files with the following commands:

```bash theme={null}
kubectl apply -f es-pvolume.yaml
kubectl apply -f es-statefulset.yaml
kubectl apply -f es-service.yaml
# service/elasticsearch created
```

Next, monitor the status of the Elasticsearch pod:

```bash theme={null}
kubectl get pods
# NAME             READY   STATUS              RESTARTS   AGE
kubectl get pods -w
# NAME             READY   STATUS    RESTARTS   AGE
# elasticsearch-0  1/1     Running   0          52s
```

To further troubleshoot or verify logs, run:

```bash theme={null}
kubectl logs -f <pod-name>
```

An example snippet from the Elasticsearch pod logs might be:

```json theme={null}
{"elasticsearch.cluster.name":"docker-cluster"}
{"@timestamp":"2024-08-06T14:26:59.586Z","log.level":"INFO","message":"loaded module [wildcard]","ecs.version":"1.2.0","service.name":"ES_ECS","event.dataset":"elasticsearch.server"}
...
```

If no errors are reported, Elasticsearch is running correctly.

## Final Verification

Elasticsearch is now deployed in the "efk" namespace on Kubernetes. In the next lesson, we will deploy Kibana and demonstrate how to verify the Elasticsearch cluster status via the Kibana UI.

Thank you for following along. See you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/79ef74c6-138f-4dd8-b5fb-e8a8050b59a5/lesson/610d0d20-face-4029-89db-d65c83a2abab" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/79ef74c6-138f-4dd8-b5fb-e8a8050b59a5/lesson/4cbae816-6bbc-48d4-9a75-4acaac81cccf" />
</CardGroup>


# Deploying Elasticsearch as a Cluster within Kubernetes

Source: https://notes.kodekloud.com/docs/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring/Elasticsearch-and-Kibana-Deployment-on-Kubernetes/Deploying-Elasticsearch-as-a-Cluster-within-Kubernetes/page

This article provides a guide on deploying Elasticsearch and Kibana in a Kubernetes environment, focusing on setup, management, scaling, and security.

Welcome to this comprehensive guide on deploying Elasticsearch and Kibana in a Kubernetes environment. In this lesson, you'll learn how to set up, manage, and scale these powerful tools for search and visualization—whether you're establishing a new cluster or enhancing an existing one.

## Lab Session Overview

We'll kick things off with a hands-on demonstration that takes you step-by-step through the deployment process of Elasticsearch on Kubernetes. This interactive lab is designed to help you gain practical experience while ensuring that your cluster is configured for optimal performance and scalability.

<Frame>
  ![The image is a timeline of a training session with five steps: Hands-on Demonstration, Kibana Deployment, Resource Optimization, Security Consideration, and Scaling ElasticSearch. It includes details about deploying a Kibana instance within a Kubernetes cluster and practicing in a guided lab session.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874204/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Deploying-Elasticsearch-as-a-Cluster-within-Kubernetes/training-session-timeline-kibana.jpg)
</Frame>

<Callout icon="lightbulb">
  Follow along with the guided lab to deploy Elasticsearch and later integrate Kibana. This practical exercise reinforces best practices in managing and scaling your Kubernetes clusters.
</Callout>

## Deploying Kibana on Kubernetes

After successfully deploying Elasticsearch, the next step is to integrate Kibana within the same Kubernetes cluster. This segment also includes a guided lab session where you can apply your skills in configuring and deploying Kibana. The demonstration includes essential steps to ensure a smooth and secure deployment for visualization purposes.

## Optimizing Performance and Security

Deploying these applications is not only about making them operational but also about fine-tuning performance and security. In this lesson, we'll cover:

* **Resource Allocation:** Learn how to specify CPU and memory settings to ensure that your Elasticsearch and Kibana deployments run efficiently.
* **Security Considerations:** Understand the key security measures necessary to protect your data and infrastructure in production environments.

<Callout icon="triangle-alert">
  Ensure that all security configurations are reviewed and tested, especially in production environments, to prevent unauthorized access and potential breaches.
</Callout>

## Scaling Elasticsearch Nodes

As your demand grows, it's crucial to scale your Elasticsearch nodes effectively within Kubernetes. This session will demonstrate techniques to seamlessly grow your deployment, ensuring high availability and continuous performance improvement.

## Next Steps

In the upcoming section, we'll begin with the live demonstration of deploying Elasticsearch on Kubernetes, turning theory into practice. Get ready to enhance your cluster management skills with our detailed, interactive lab sessions.

For more in-depth Kubernetes resources, check out:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)
* [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/79ef74c6-138f-4dd8-b5fb-e8a8050b59a5/lesson/b195402b-c0a0-4bbb-8304-646dd7ad7cc0" />
</CardGroup>
