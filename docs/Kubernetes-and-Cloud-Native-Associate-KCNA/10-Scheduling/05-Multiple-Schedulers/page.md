# Output:
# NAME     READY   STATUS    RESTARTS   AGE
# nginx    0/1     Pending   0          3s
```

## Approaches to Manual Pod Scheduling

There are two primary methods for manually scheduling a pod:

### 1. Specify `nodeName` During Pod Creation

The simplest approach is to set the `nodeName` in the pod's specification. When this field is explicitly defined, Kubernetes assigns the pod immediately to the designated node. See the updated manifest example below:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    name: nginx
spec:
  containers:
    - name: nginx
      image: nginx
      ports:
        - containerPort: 8080
  nodeName: node02
```

### 2. Scheduling an Existing Pod Using a Binding Object

If the pod is already created and its `nodeName` cannot be modified, you need to simulate the scheduler's behavior by creating a Binding object. This involves the following two steps:

1. **Create the Binding Object**\
   Define a binding object that specifies the target node:

   ```yaml theme={null}
   apiVersion: v1
   kind: Binding
   metadata:
     name: nginx
   target:
     apiVersion: v1
     kind: Node
     name: node02
   ```

2. **Send the Binding Object via a POST Request**\
   Convert the YAML definition into JSON and use a `curl` command to send a POST request to the pod's binding API:

   ```bash theme={null}
   curl --header "Content-Type: application/json" \
        --request POST \
        --data '{"apiVersion":"v1", "kind": "Binding", "metadata": {"name": "nginx"}, "target": {"apiVersion": "v1", "kind": "Node", "name": "node02"}}' \
        http://$SERVER/api/v1/namespaces/default/pods/$PODNAME/binding/
   ```

> **lightbulb** Ensure that you replace `$SERVER` and `$PODNAME` with your actual server address and pod name.

## Summary

In summary, you have two options for manually scheduling a pod in Kubernetes:

* **During Pod Creation:** Set the `nodeName` field in your pod's manifest to assign it directly to a node.
* **For Existing Pods:** Create a Binding object and use a POST request to assign the pod to your desired node.

This approach provides flexibility in environments where automated scheduling may not fit specific use cases. For more detailed information on Kubernetes pod management, visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

Happy scheduling!

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/4fab542c-3091-4f8e-ad7c-91d96d54b049/lesson/8268701e-0523-4d87-ae9d-35407df68073)


# Multiple Schedulers

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Scheduling/Multiple-Schedulers/page

This article covers deploying multiple schedulers in Kubernetes to enable custom placement logic for specific applications while using the default scheduler for most workloads.

Welcome to this article on deploying multiple schedulers in a Kubernetes cluster. In this guide, we will walk through configuring and deploying additional schedulers—enabling you to use custom placement logic for specific applications while still relying on the default scheduler for most workloads.

Kubernetes distributes pods evenly across nodes and considers factors such as taints, tolerations, and node affinity when using its default scheduler. However, if your application requires custom scheduling behavior, Kubernetes allows you to implement and deploy a custom scheduler alongside the default one. When running multiple schedulers, each must have a unique name so Kubernetes can easily differentiate between them. The default scheduler is typically named "default-scheduler".

> **lightbulb** Even though you do not need an explicit configuration file for the default scheduler, creating one can help you document and customize the scheduling behavior if needed.

## Default Scheduler Configuration

A configuration file for the default scheduler might look like this:

```yaml theme={null}
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: default-scheduler
```

## Creating a Custom Scheduler

To create a custom scheduler, prepare a separate configuration file that specifies a unique scheduler name. For example:

```yaml theme={null}
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: my-scheduler
```

## Deploying an Additional Scheduler as a Service

When deploying an extra scheduler as a service, you typically use the same kube-scheduler binary or a modified version with a unique configuration file. Below are two examples—one for the default scheduler and another for a custom scheduler.

### Default Scheduler Service

```bash theme={null}
wget https://storage.googleapis.com/kubernetes-release/release/v1.12.0/bin/linux/amd64/kube-scheduler

ExecStart=/usr/local/bin/kube-scheduler \
--config=/etc/kubernetes/config/kube-scheduler.yaml
```

### Custom Scheduler Service

Create a service file for your custom scheduler, for example, `my-scheduler-2.service`:

```bash theme={null}
