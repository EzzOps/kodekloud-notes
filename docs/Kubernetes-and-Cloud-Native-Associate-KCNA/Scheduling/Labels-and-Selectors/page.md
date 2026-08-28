# daemon-set-definition.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: monitoring-daemon
spec:
  selector:
    matchLabels:
      app: monitoring-agent
  template:
    metadata:
      labels:
        app: monitoring-agent
    spec:
      containers:
      - name: monitoring-agent
        image: monitoring-agent
```

For reference, here’s a similar ReplicaSet definition that deploys the same monitoring agent. Notice that the structure is nearly identical except for the value of `kind`:

```yaml theme={null}
# replicaset-definition.yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: monitoring-daemon
spec:
  selector:
    matchLabels:
      app: monitoring-agent
  template:
    metadata:
      labels:
        app: monitoring-agent
    spec:
      containers:
      - name: monitoring-agent
        image: monitoring-agent
```

Ensure that the labels in the `selector` match those in the Pod template to guarantee proper functioning. Once your DaemonSet definition is ready, create it using the following kubectl command:

```bash theme={null}
kubectl apply -f daemon-set-definition.yaml
```

After applying the YAML file, verify your DaemonSet with:

```bash theme={null}
kubectl get daemonsets
```

The console output might look similar to this:

```bash theme={null}
NAME                DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   AGE
monitoring-daemon   1         1         1       1            1           41
```

## How DaemonSets Work

DaemonSets automatically schedule Pods on every node in your cluster. In earlier Kubernetes versions, the `nodeName` property was used to assign Pods directly to nodes, bypassing the scheduler. However, since version 1.12, DaemonSets leverage the default scheduler and node affinity rules to manage Pod placement.

<Frame>
  ![The image illustrates a network diagram with nodes labeled node01 to node06, connected to six devices, under the title "How does it work?".](https://kodekloud.com/kk-media/image/upload/v1752880693/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-DaemonSets/frame_220.jpg)
</Frame>

To summarize, a DaemonSet ensures that a specific Pod is running on all nodes in your cluster—making it ideal for running services such as:

* Monitoring
* Logging
* Networking

Happy clustering!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/4fab542c-3091-4f8e-ad7c-91d96d54b049/lesson/f6d944ea-aea7-46f2-a97c-99318338b06b" />
</CardGroup>


# Labels and Selectors

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Scheduling/Labels-and-Selectors/page

Labels and selectors provide a method to group and filter items based on criteria, essential for managing Kubernetes objects like Pods and Services.

Labels and selectors provide a standard method to group and filter items based on various criteria. Think of it like sorting species by attributes such as class (mammal, bird, etc.), domestication status, or color. Whether you want to list all green animals or specifically all green birds, labels let you attach key-value pairs to each item, while selectors help retrieve items that meet your criteria.

This concept is applied widely—from tagging YouTube videos or blog posts, to using filters that sort products in an online store.

In Kubernetes, labels and selectors are essential for managing a cluster filled with objects such as Pods, Services, ReplicaSets, and Deployments. Labels help organize these resources by applying characteristics like application type or functionality, allowing you to filter and group them even when dealing with hundreds or thousands of objects. Selectors then query these objects based on the criteria specified by the labels.

<Frame>
  ![The image illustrates "Labels & Selectors in Kubernetes," showing various labeled components like Front-End, Web-Servers, and DB, represented by different colored shapes.](https://kodekloud.com/kk-media/image/upload/v1752880693/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Labels-and-Selectors/frame_140.jpg)
</Frame>

For every Kubernetes object, you attach labels as needed (for example, app or function) and then use selectors to filter the objects. For instance, if you want to filter objects where the label app equals App1, your selector would look like this:

```text theme={null}
app = App1
```

## Specifying Labels in a Pod Definition

In a Pod definition file, labels are defined under the metadata section. Below is an example of how to add labels in a key-value format:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
  labels:
    app: App1
    function: Front-end
spec:
  containers:
    - name: simple-webapp
      image: simple-webapp
      ports:
        - containerPort: 8080
```

After creating the Pod, you can run the following command with a selector to filter for Pods with a specific label, such as `app=App1`:

```bash theme={null}
kubectl get pods --selector app=App1
```

Console output:

```plaintext theme={null}
NAME             READY   STATUS      RESTARTS   AGE
simple-webapp    0/1     Completed   0          1d
```

## Using Labels and Selectors with ReplicaSets

When working with ReplicaSets to manage multiple Pods, you label the Pod definition and then specify a selector in the ReplicaSet to group the desired Pods. It’s crucial that the selector in the ReplicaSet specification matches the labels on the Pods exactly.

<Callout icon="lightbulb">
  Only the labels on the Pod template are used for selection; labels on the ReplicaSet itself are not considered.
</Callout>

Below is a correct ReplicaSet definition that connects the ReplicaSet to its Pods by matching labels:

```yaml theme={null}
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: simple-webapp
  labels:
    app: App1
    function: Front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      app: App1
  template:
    metadata:
      labels:
        app: App1
        function: Front-end
    spec:
      containers:
      - name: simple-webapp
        image: simple-webapp
```

A single matching label is sufficient. However, if there is a chance that other Pods might share a common label, you should include additional labels in the selector to guarantee that only the intended Pods are selected.

This principle also applies to other Kubernetes objects like Services. When a Service is created, its selector—defined in the Service specification—matches the labels on the Pods (or ReplicaSets) that it targets.

## Annotations in Kubernetes

While labels and selectors are used for grouping and filtering, annotations offer a way to attach non-identifying metadata to objects for informational purposes. Annotations might include details about the build version, contact information, or other integration data.

For example, consider the following ReplicaSet definition that includes an annotation:

```yaml theme={null}
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: simple-webapp
  labels:
    app: App1
    function: Front-end
  annotations:
    buildversion: "1.34"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: App1
  template:
    metadata:
      labels:
        app: App1
        function: Front-end
    spec:
      containers:
      - name: simple-webapp
        image: simple-webapp
```

Annotations are ideal for adding tool details, version information, or contact data without impacting how the system groups or selects objects.

## Summary

Through the careful use of labels, selectors, and annotations, Kubernetes offers a powerful framework to manage and organize vast numbers of objects effectively. This flexible mechanism improves resource management and simplifies querying, ensuring smooth operations in complex environments.

For more detailed information, consider exploring:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<Callout icon="lightbulb">
  Using specific labels and selectors efficiently can significantly streamline your Kubernetes resource management. Experiment with various configurations to understand the best practices for your deployment needs.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/4fab542c-3091-4f8e-ad7c-91d96d54b049/lesson/52340979-76f2-456c-9f91-0da38a75750c" />
</CardGroup>
