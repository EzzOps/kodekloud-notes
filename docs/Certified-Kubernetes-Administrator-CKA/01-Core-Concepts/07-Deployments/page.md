# Output:
# pod/nginx created
```

To check the status of your Pod, run:

```bash theme={null}
kubectl get pods
```

Initially, you might see an output similar to this:

```bash theme={null}
NAME    READY   STATUS              RESTARTS   AGE
nginx   0/1     ContainerCreating   0          7s
```

After a short while, re-running the command should show the Pod in a running state:

```bash theme={null}
kubectl get pods
```

Example output:

```bash theme={null}
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          9s
```

## Step 4: Inspecting the Pod Details

For a detailed overview of your Pod, use the `kubectl describe` command:

```bash theme={null}
kubectl describe pod nginx
```

This command provides comprehensive details about the Pod, including container statuses, event logs, volumes, and node assignments. Below is an example of typical output:

```bash theme={null}
Initialized              True
Ready                    True
ContainersReady          True
PodScheduled             True
Volumes:
  default-token-f5ntk:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-f5ntk
    Optional:    false
QoS Class:   BestEffort
Node-Selectors: <none>
Tolerations: node.kubernetes.io/not-ready:NoExecute for 300s
             node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason        Age   From                Message
  ----     ------        ----  ----                -------
  Normal   Scheduled     21s   default-scheduler   Successfully assigned default/nginx to minikube
  Normal   Pulling       20s   kubelet, minikube   Pulling image "nginx"
  Normal   Pulled        14s   kubelet, minikube   Successfully pulled image "nginx"
  Normal   Created       14s   kubelet, minikube   Created container nginx
  Normal   Started       14s   kubelet, minikube   Started container nginx
```

## Conclusion

This demonstration has guided you through creating a Kubernetes Pod using a YAML configuration file. This approach not only reinforces good configuration practices but also provides enhanced flexibility compared to command-based object creation. In our next lesson, we will cover advanced IDEs and tools to further ease YAML file management.

For additional reading and resources, check out:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/c6d2ac7d-8192-4cff-aa54-e36d888c5bd9/lesson/94035645-87a0-4b78-a5f8-e66a3f3c228c" />
</CardGroup>


# Deployments

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Core-Concepts/Deployments/page

This guide explores Kubernetes deployments, simplifying application management with features like rolling updates, rollbacks, and high availability.

Hello and welcome! My name is Mumshad Mannambeth. In this guide, we dive into Kubernetes deployments—an abstraction that simplifies managing your applications in a production environment. Rather than interacting directly with pods and ReplicaSets, deployments offer advanced features that enable you to:

* Deploy multiple instances of your application (like a web server) to ensure high availability and load balancing.
* Seamlessly perform rolling updates for Docker images so that instances update gradually, reducing downtime.
* Quickly roll back to a previous version if an upgrade fails unexpectedly.
* Pause and resume deployments, allowing you to implement coordinated changes such as scaling, version updates, or resource modifications.

Previously, we discussed how individual pods encapsulate containers and how ReplicaSets maintain multiple pod copies. A deployment, however, sits at a higher level, automatically managing ReplicaSets and pods while providing enhanced features like rolling updates and rollbacks.

## Creating a Deployment

To create a deployment, start by writing a deployment definition file. This file is similar to a ReplicaSet definition, with the key difference being that the kind is set to Deployment instead of ReplicaSet. Below is an example of a correct deployment definition file:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    app: myapp
    type: front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      type: front-end
  template:
    metadata:
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
        - name: nginx-container
          image: nginx
```

Once your deployment definition file (for example, named deployment-definition.yml) is ready, create the deployment with the following command:

```bash theme={null}
kubectl create -f deployment-definition.yml
```

The command output should confirm that the deployment has been created:

```console theme={null}
deployment "myapp-deployment" created
```

To verify the deployment, run:

```bash theme={null}
kubectl get deployments
```

The output will look similar to this:

```console theme={null}
NAME                DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
myapp-deployment    3         3         3            3           21s
```

## Behind the Scenes: How Deployments Work

When you create a deployment, Kubernetes automatically creates an associated ReplicaSet. To see this in action, run:

```bash theme={null}
kubectl get replicasets
```

You'll notice a new ReplicaSet with a name derived from your deployment. This ReplicaSet oversees the creation and management of pods. To view the pods managed by the ReplicaSet, run:

```bash theme={null}
kubectl get pods
```

While deployments and ReplicaSets work together seamlessly, deployments provide additional functionalities such as rolling updates, rollbacks, and the ability to pause/resume changes.

<Callout icon="lightbulb">
  To view all the created Kubernetes objects—deployments, ReplicaSets, pods, and more—use the following command:

  ```bash theme={null}
  kubectl get all
  ```

  This gives you a comprehensive overview of your deployment's components.
</Callout>

A sample output of the "kubectl get all" command might be:

```console theme={null}
NAME                            DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deploy/myapp-deployment         3         3         3            3           9h

NAME                                        DESIRED   CURRENT   READY   AGE
rs/myapp-deployment-6795844b58              3         3         3       9h

NAME                                      READY   STATUS    RESTARTS   AGE
po/myapp-deployment-6795844b58-5rbjl        1/1     Running   0          9h
po/myapp-deployment-6795844b58-h4w55         1/1     Running   0          9h
po/myapp-deployment-6795844b58-1fjhv         1/1     Running   0          9h
```

In this output, you can clearly see the deployment, its associated ReplicaSet, and the managed pods.

## Conclusion

This article has covered the fundamentals of creating a deployment in Kubernetes. By leveraging deployments, you gain powerful capabilities like rolling updates and rollbacks that make managing application updates and maintenance in production more efficient. Whether you are scaling your application or rolling out new features, Kubernetes deployments provide a robust solution for modern application management.

Happy deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/c6d2ac7d-8192-4cff-aa54-e36d888c5bd9/lesson/5f6448e3-51e0-41c1-8abb-865cbdbc611d" />
</CardGroup>
