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

:::note Important
Ensure that the labels in the selector match those in the pod template. Consistent labeling is crucial for the proper functioning of your DaemonSet.
:::

Once your YAML file is ready, create the DaemonSet using the following command:

```bash theme={null}
kubectl create -f daemon-set-definition.yaml
```

Verify the DaemonSet's creation by running:

```bash theme={null}
kubectl get daemonsets
```

This command produces output similar to:

```console theme={null}
NAME               DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   AGE
monitoring-daemon  1         1         1       1            1           41
```

For more detailed information on your DaemonSet, use:

```bash theme={null}
kubectl describe daemonset monitoring-daemon
```

## How DaemonSets Schedule Pods

Prior to Kubernetes version 1.12, scheduling a pod on a specific node was often achieved by manually setting the `nodeName` property within the pod specification. However, since version 1.12, DaemonSets leverage the default scheduler in conjunction with node affinity rules. This improvement ensures that a pod is automatically scheduled on every node without manual intervention.

![The image explains Kubernetes node scheduling, showing default behavior till v1.12 and changes with NodeAffinity from v1.12, featuring nodes labeled node01 to node06.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869890/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-DaemonSets/frame_240.jpg)

:::note Tip
DaemonSets are an ideal solution for deploying services that must run on every node, such as monitoring agents and essential networking components. Leveraging node affinity simplifies management as your cluster scales.
:::

## Conclusion

DaemonSets provide an efficient mechanism to ensure that key services are uniformly deployed across your Kubernetes cluster. Whether you're running log collectors, monitoring agents, or essential network components like kube-proxy and weave-net, DaemonSets help maintain consistency and reliability in dynamic environments.

For further reading, explore these resources:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [DaemonSets Concept](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)

Happy clustering!

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/140b1ac2-fe89-494c-b64f-dfae87311d7f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/398221f8-e4b8-4e41-a0f8-1d130f510379)


# Labels and Selectors

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Scheduling/Labels-and-Selectors/page

This article explores labels, selectors, and annotations in Kubernetes for effective resource management and organization.

Welcome to this comprehensive guide on labels, selectors, and annotations in Kubernetes. In this article, we will explore how labels and selectors help group and filter items effectively, and we will also discuss how annotations are used to store additional metadata. By the end, you'll understand how these key concepts are applied to manage resources in a Kubernetes environment.

## Introduction to Labels and Selectors

Labels and selectors offer a systematic approach to categorizing items. Think of a scenario where you have various species of animals, and you need to filter them based on attributes such as class, kind, or color. For example, you might want to filter for all green animals or just the green birds. By attaching labels like class, kind, and color to each animal, you can later use selectors to efficiently filter and display the items that meet your criteria.

![The image shows animal icons with labels for class, kind, and color, illustrating selectors for categorization.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869891/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Labels-and-Selectors/frame_70.jpg)

In everyday applications, labels and selectors are ubiquitous. They function similarly to keywords in YouTube videos or blog posts, aiding users in finding relevant content. In online stores, labels empower customers to filter products based on various characteristics.

## Labels and Selectors in Kubernetes

In Kubernetes, labels and selectors are instrumental in managing an array of objects such as Pods, Services, ReplicaSets, and Deployments. As the number of objects in a cluster grows, these tools become essential for grouping and selecting objects by application, functionality, or type.

![The image illustrates the use of labels and selectors in Kubernetes, featuring various colored shapes representing different components or services.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869893/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Labels-and-Selectors/frame_140.jpg)

For instance, you might attach labels like "app" or "function" to your Kubernetes objects and later use selectors to filter objects based on specific conditions (e.g., app equals "App1").

![The image shows labeled shapes representing different apps and functions, including front-end, authentication, web servers, image processing, and databases.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869894/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Labels-and-Selectors/frame_160.jpg)

## Specifying Labels in Kubernetes

To apply labels to a Kubernetes object such as a Pod, include a `labels` section under the `metadata` field in its definition file. Consider the following Pod definition example:

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

After creating the Pod, you can retrieve it using the `kubectl get pods` command with a selector. For example:

```bash theme={null}
kubectl get pods --selector app=App1
NAME            READY   STATUS      RESTARTS   AGE
simple-webapp   0/1     Completed   0          1d
```

> **lightbulb** Using selectors with `kubectl` commands helps you filter and manage resources in large clusters with ease.

## Using Labels and Selectors with ReplicaSets

In Kubernetes, internal mechanisms utilize labels and selectors to connect different objects. When creating a ReplicaSet to manage three Pods, you first label the Pod definitions and then use a selector in the ReplicaSet definition to ensure the correct Pods are grouped together.

A ReplicaSet definition includes labels in two key areas:

1. Within the ReplicaSet's metadata (allowing other objects to reference the ReplicaSet).
2. Within the `template` of the ReplicaSet's specification (applying the labels to the Pods).

By setting the `selector` field in the ReplicaSet specification to match the labels defined on the Pods, you ensure that the ReplicaSet manages the intended Pods. Below is an example configuration:

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

> **lightbulb** If you require more granular control for selecting Pods, you can list multiple labels in the `matchLabels` section.

## Annotations

Annotations differ from labels and selectors in that they are used to store additional metadata that is not intended for selection. This metadata might include details such as tool versions, build information, or contact information. Below is an example of a ReplicaSet configuration that includes an annotation:

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

When the ReplicaSet is created, it matches the Pods based on labels, ensuring that only the intended Pods are managed. The same mechanism is used when creating Services, where the Service's selector matches the labels set on the Pods.

## Conclusion

This article has provided an in-depth look at labels, selectors, and annotations in Kubernetes. These concepts are essential for effectively managing and grouping objects within your clusters. For further hands-on practice, navigate to the coding exercises section and start working with labels and selectors today.

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/fc62111a-8765-45b8-918b-386843d446c7)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/9e7ffed0-765b-4f83-a5e8-40e83bd3a8fe)
