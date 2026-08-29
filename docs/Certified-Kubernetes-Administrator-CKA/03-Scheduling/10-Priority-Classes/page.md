# Priority Classes

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Scheduling/Priority-Classes/page

Understanding priority classes is essential for managing workload scheduling in Kubernetes by assigning numerical values to Pods based on their importance.

Understanding priority classes is essential for managing workload scheduling in Kubernetes. Kubernetes runs various applications as Pods with different levels of importance. For instance, control plane components run within the cluster as Pods and are vital for its operation. Similarly, production databases and critical applications are high-priority while background jobs generally have lower priority. To ensure that more important workloads are scheduled before less critical ones, Kubernetes uses priority classes.

Priority classes allow you to assign a numerical value to Pods, where a higher number indicates higher priority. For user-deployed applications, the value can range from approximately -2 billion to +1 billion. Additionally, there is a reserved range for internal system-critical Pods (like the Kubernetes control plane) which can have values up to 2 billion.

![The image is a diagram illustrating priorities for Kubernetes components, databases, critical apps, and jobs, with a focus on system and app allocation, and numerical values indicating priority levels.](https://kodekloud.com/kk-media/image/upload/v1752869897/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Priority-Classes/kubernetes-priorities-diagram.jpg)

:::note Note
To check the current priority classes in your cluster, run the following command:
:::

```bash theme={null}
kubectl get priorityclass
```

The output may appear as follows:

```bash theme={null}
NAME                      VALUE          GLOBAL-DEFAULT   AGE     PREEMPTIONPOLICY
system-cluster-critical   2000000000     false            7m33s   PreemptLowerPriority
system-node-critical      2000010000     false            7m33s   PreemptLowerPriority
```

## Creating a New Priority Class

To create a new priority class, define an object with the API version `scheduling.k8s.io/v1`, set the kind to `PriorityClass`, and include metadata with a name, numerical value, and an optional description. For example:

```yaml theme={null}
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Priority class for mission critical pods"
```

After creating the priority class, you can assign it to a Pod by specifying the `priorityClassName` field in your Pod's specification. If you do not specify a priority class, the Pod is assigned a default priority value of zero. To change the default priority for Pods, create a priority class with the `globalDefault` property set to `true`. Note that only one priority class can be marked as the global default.

Below is an example that demonstrates both the creation of a priority class and how to use it in a Pod definition:

```yaml theme={null}
