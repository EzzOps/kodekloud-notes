# Inside the shell:
printenv | grep MESSAGE
```

If you see:

```bash theme={null}
MESSAGE=Hello, World
```

then your application is using the expected configuration.

## Adding the Reloader Annotation

To enable Reloader for your application, update your deployment definition with the Reloader annotation. Below is an example of a Deployment configuration with the necessary annotation:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  annotations:
    reloader.stakater.com/auto: "true"
    deployment.kubernetes.io/revision: "1"
  labels:
    app: ""
spec:
  replicas: 1
  selector:
    matchLabels:
      app: node-env-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
  template:
    metadata:
      labels:
        app: node-env-app
    spec:
      containers:
      - name: web-app
        image: rakshithraka/node-env-app
        ports:
        - containerPort: 3000
        envFrom:
        - configMapRef:
            name: web-message
```

After applying this update, Reloader will automatically initiate a restart of the deployment whenever there's a change to any associated ConfigMaps or Secrets. Apply the updated configuration by running:

```bash theme={null}
kubectl apply -f https://raw.githubusercontent.[AWS_SECRET_ACCESS_KEY]/kubernetes/reloader.yaml
```

Then, inspect your production pods:

```bash theme={null}
kubectl get pods -n production
```

You can also review your deployment details with:

```bash theme={null}
kubectl edit deployments.apps -n production web-app
```

## Updating a ConfigMap and Observing Reloader in Action

To demonstrate Reloader's functionality, update the ConfigMap to change the greeting message. Use the following updated ConfigMap configuration:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-message
  namespace: production
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"MESSAGE":"Hello, World"},"kind":"ConfigMap","metadata":{"name":"web-message","namespace":"production"}}
data:
  MESSAGE: Hello Reloader
```

After applying the updated ConfigMap, observe that the Deployment is immediately restarted—the old pods are terminated and new ones are created. Confirm the current state with:

```bash theme={null}
kubectl get pods -n production
```

Then, connect to one of the new pods and check the environment variable:

```bash theme={null}
kubectl exec -n production -it web-app-68547b8c9d-8vhtl -- /bin/sh
# Inside the shell:
printenv | grep MESSAGE
```

A successful update should display:

```bash theme={null}
MESSAGE=Hello Reloader
```

<Callout icon="lightbulb">
  This demonstration highlights how Reloader minimizes manual interventions, saving time and ensuring your application configuration changes are applied efficiently.
</Callout>

## Conclusion

Reloader streamlines the process of handling ConfigMap and Secret updates by automating the restart of Kubernetes resources. This automation not only simplifies troubleshooting but also reduces potential downtime in your applications. Use Reloader to enhance your Kubernetes deployment workflows and ensure smooth and continuous integration of configuration changes.

Happy deploying, and enjoy the benefits of automated rolling upgrades!

***

## Further Reading and Resources

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [GitHub Repository: stakater/Reloader](https://github.com/stakater/Reloader)
* [Kubernetes Rolling Upgrades](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)

For more information on Kubernetes best practices and troubleshooting, check out additional guides on [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-troubleshooting-for-application-developers/module/143d3913-caef-4dab-bde6-b77e96dbb161/lesson/a3b0b3d3-a997-496b-9b61-e30dcbc1b224" />
</CardGroup>


# Schrodingers Deployment

Source: https://notes.kodekloud.com/docs/Kubernetes-Troubleshooting-for-Application-Developers/Troubleshooting-Scenarios/Schrodingers-Deployment/page

This lesson explores troubleshooting mixed responses in Kubernetes deployments caused by overlapping service selectors.

Welcome to this lesson on troubleshooting a peculiar behavior in Kubernetes deployments. In this guide, we will explore why our blue service sometimes returns responses from the green application. Let’s dive in.

***

## Observing the Problem

When inspecting the cluster, both the blue and green deployments are running as expected. The following command output confirms this:

```bash theme={null}
controlplane ~ ➜ k get all
NAME                                       READY   STATUS      RESTARTS   AGE
pod/blue-6c7b7b965f-8vxwp                   1/1     Running     0          21m
pod/blue-6c7b7b965f-zddzq                   1/1     Running     0          24m
pod/green-864c4d957c-tnq9r                  1/1     Running     0          24m
pod/green-864c4d957c-w7ktb                  1/1     Running     0          93s

NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/blue-service       NodePort    10.98.48.50     <none>       8080:30102/TCP   24m
service/green-service      NodePort    10.107.193.230  <none>       8080:30101/TCP   24m
service/kubernetes         ClusterIP   10.96.0.1       <none>       443/TCP         46m

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/blue      2/2     2            2           24m
deployment.apps/green     2/2     2            2           24m

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/blue-6c7b7b965f                   2         2         2       24m
replicaset.apps/green-864c4d957c                   2         2         2       24m
controlplane ~ ➜
```

The blue service is expected to serve a blue screen, while the green service serves a green screen using a basic web server. When accessing the green service in your browser, each refresh may hit a different replica due to load balancing across multiple pods.

However, upon accessing the blue service endpoint repeatedly, you may notice an unexpected mix of responses that sometimes include a green background.

***

## Investigating Service Definitions

To diagnose the issue, let's review the service definitions.

### Current Cluster State

The initial output of our cluster services is as follows:

```bash theme={null}
controlplane ~ ➜ k get all
NAME                                                      READY   STATUS    RESTARTS   AGE
pod/blue-6c7b7b965f-8vxwp                                 1/1     Running   0          21m
pod/blue-6c7b7b965f-zddzq                                 1/1     Running   0          24m
pod/green-864c4d957c-tnq7r                                1/1     Running   0          24m
pod/green-864c4d957c-w7ktb                                1/1     Running   0          93s

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
service/blue-service    NodePort    10.98.48.50     <none>       8080:30102/TCP     24m
service/green-service   NodePort    10.107.193.230  <none>       8080:30101/TCP     24m
service/kubernetes      ClusterIP   10.96.0.1       <none>       443/TCP            46m

NAME                                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/blue                        2/2     2            2           24m
deployment.apps/green                       2/2     2            2           24m

NAME                                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/blue-6c7b7b965f                        2         2         2       24m
replicaset.apps/green-864c4d957c                        2         2         2       24m
controlplane ~ ➜
```

### Listing Service Definition Files

The two service configuration files in the directory are:

```bash theme={null}
controlplane ~ ➜ ls
blue-svc.yaml  green-svc.yaml
```

#### blue-svc.yaml

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: blue-service
spec:
  type: NodePort
  selector:
    version: v1
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30102
```

#### green-svc.yaml

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: green-service
spec:
  type: NodePort
  selector:
    version: v1
    app: green
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30101
```

The green service’s selector uses both `version: v1` and `app: green`, isolating the green pods properly. The blue service, however, only uses `version: v1` as its selector. Since both blue and green pods share the `version: v1` label, the blue service unintentionally selects green pods too, leading to mixed responses.

***

## Understanding Label Selectors and Endpoints

Kubernetes services route traffic to all pods matching their label selectors. To verify the selected pods for label `version=v1`, run:

```bash theme={null}
controlplane ~ ➜ k get pods -l version=v1
NAME                     READY   STATUS    RESTARTS   AGE
blue-6c7b7b965f-8xwp     1/1     Running   0          30m
blue-6c7b7b965f-zddzq     1/1     Running   0          33m
green-864c4d957c-tnq9r    1/1     Running   0          33m
green-864c4d957c-w7ktb    1/1     Running   0          10m
```

Checking the endpoints for each service further clarifies the issue:

```bash theme={null}
controlplane ~ ➜ k get endpoints
NAME            ENDPOINTS                                               AGE
blue-service    10.244.1.2:8080,10.244.1.3:8080,10.244.1.4:8080 + 1 more...   34m
green-service   10.244.1.2:8080                                   34m
kubernetes      192.147.9.6:6443                                  56m
```

Notice that the blue service includes endpoints for both blue and green pods, whereas the green service correctly targets only green pods.

<Callout icon="lightbulb">
  Use the command "k edit svc blue-service" to inspect and modify the blue service configuration in real time.
</Callout>

***

## Fixing the Issue

To ensure that the blue service routes traffic only to blue pods, update the blue service selector by adding a unique label. Modify the selector to include both `version: v1` and `app: blue`. After making this change, the blue service will exclusively target blue pods.

Once updated, verify the endpoints again:

```bash theme={null}
controlplane ~ ➜ k get endpoints
NAME            ENDPOINTS                                          AGE
blue-service    10.244.1.2:8080,10.244.1.4:8080                   35m
green-service   10.244.1.3:8080                                   35m
kubernetes      192.147.9.6:6443                                  57m
```

This confirmation shows that the blue service now exclusively routes requests to the correct blue pods, resolving the intermittent misrouting issue.

***

## Final Thoughts

This troubleshooting exercise highlights the critical importance of using unique labels in Kubernetes deployments. Overlapping selectors can cause unexpected behavior and intermittent failures that are challenging to diagnose in large-scale environments.

Understanding how label selectors, service endpoints, and load balancing interact is vital for maintaining reliable application deployments in Kubernetes.

<Frame>
  ![The image illustrates a Kubernetes deployment setup called "Schrödinger’s Deployment," featuring two services with version selectors, a load balancer, and multiple pods. It also indicates a 90% success rate for responses.](https://kodekloud.com/kk-media/image/upload/v1752880441/notes-assets/images/Kubernetes-Troubleshooting-for-Application-Developers-Schrodingers-Deployment/schrodingers-deployment-kubernetes-setup.jpg)
</Frame>

Even if the application appears to work correctly most of the time, such misconfigurations can lead to intermittent issues that are hard to catch during routine monitoring.

<Frame>
  ![The image is a graphic about "Troubleshooting Configuration," featuring an icon of a document with a gear and code symbol, and a note about label issues being overlooked during monitoring.](https://kodekloud.com/kk-media/image/upload/v1752880442/notes-assets/images/Kubernetes-Troubleshooting-for-Application-Developers-Schrodingers-Deployment/troubleshooting-configuration-graphic.jpg)
</Frame>

Having a robust troubleshooting process, including verifying service endpoints and label selectors, is essential for diagnosing and resolving configuration issues in Kubernetes.

<Frame>
  ![The image lists three key considerations: Endpoints Application, Service Load Balancing, and Label Selector Matching, each represented by a distinct icon.](https://kodekloud.com/kk-media/image/upload/v1752880443/notes-assets/images/Kubernetes-Troubleshooting-for-Application-Developers-Schrodingers-Deployment/endpoints-service-load-balancing-icons.jpg)
</Frame>

Happy troubleshooting, and see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-troubleshooting-for-application-developers/module/143d3913-caef-4dab-bde6-b77e96dbb161/lesson/9d709e5f-c68b-4274-a889-393d82b46d62" />
</CardGroup>
