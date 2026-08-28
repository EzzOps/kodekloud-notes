# Updated pod configuration for nginx1401
spec:
  containers:
    - image: kodekloud/nginx
      imagePullPolicy: IfNotPresent
      name: nginx
      ports:
        - containerPort: 9080
          protocol: TCP
      readinessProbe:
        failureThreshold: 3
        httpGet:
          path: /
          port: 9080
          scheme: HTTP
        periodSeconds: 10
        successThreshold: 1
        timeoutSeconds: 1
      livenessProbe:
        exec:
          command:
            - ls
            - /var/www/html/file_check
        periodSeconds: 60
  resources: {}
  terminationMessagePath: /dev/termination-log
  terminationMessagePolicy: File
  volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-7b8v2
```

Apply the updated configuration by replacing the existing pod. Save the file (for example, as `nginx1401.yaml`) and then run:

```bash theme={null}
kubectl replace -f nginx1401.yaml --force
```

Finally, verify that the pod is now in a ready state:

```bash theme={null}
kubectl get pod nginx1401 -n dev1401 -o yaml > nginx1401.yaml
```

<Callout icon="lightbulb">
  Ensure your pod configuration settings (such as `containerPort`) match across all probe definitions to avoid inconsistencies.
</Callout>

***

## Task 2: Create a CronJob Named "dice"

The next task involves creating a CronJob called "dice" that runs every minute. This job leverages the `kodekloud/throw-dice` image, which randomly returns a number between one and six. A roll of six indicates success; any other result is a failure.

Additional requirements for the CronJob include:

* Running jobs non-parallel (in series).
* Completing the task only once (completions: 1).
* Using a backoff limit of 25.
* Terminating the job if it runs longer than 20 seconds (using `activeDeadlineSeconds: 20`).
* Setting the restart policy to `Never`.

Create the CronJob definition in a file called `dice-job.yaml`:

```yaml theme={null}
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dice
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      completions: 1
      backoffLimit: 25
      activeDeadlineSeconds: 20
      template:
        spec:
          containers:
          - name: dice
            image: kodekloud/throw-dice
            imagePullPolicy: IfNotPresent
            command:
            - /bin/sh
            - -c
            - "date; echo Hello from the Kubernetes cluster"
          restartPolicy: Never
```

Save and apply the CronJob configuration:

```bash theme={null}
kubectl apply -f dice-job.yaml
```

Verify the CronJob by running:

```bash theme={null}
kubectl get cj
```

You should see an output similar to:

```bash theme={null}
NAME   SCHEDULE       SUSPEND   ACTIVE   LAST SCHEDULE   AGE
dice   */1 * * * *    False     0        <none>          12S
```

***

## Task 3: Create a "my-busybox" Pod in a Specific Namespace

In this task, you will create a pod named "my-busybox" using the `busybox` image in the `dev2406` namespace. The pod requirements are as follows:

* The container inside the pod should be named `secret` and execute `sleep 3600`.
* Mount a read-only secret volume named `secret-volume` at `/etc/secret-volume`. (The secret `dotfile-secret` is pre-created.)
* Schedule the pod on the control plane by specifying `nodeName: controlplane`.

Start by generating a basic pod manifest using dry-run:

```bash theme={null}
kubectl run my-busybox --image=busybox --dry-run=client -o yaml > my-busybox.yaml
```

Edit the generated `my-busybox.yaml` file to include the required customizations:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: my-busybox
  namespace: dev2406
  labels:
    run: my-busybox
spec:
  nodeName: controlplane
  containers:
  - image: busybox
    name: secret
    command:
    - sleep
    - "3600"
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secret-volume
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: dotfile-secret
  restartPolicy: Always
```

Apply the configuration with:

```bash theme={null}
kubectl apply -f my-busybox.yaml
```

***

## Task 4: Create an Ingress Resource for Virtual Hosting Routing

This task involves creating a single Ingress resource named `ingress-vh-routing` to handle virtual hosting routing for HTTP traffic. The configuration will route traffic as follows:

* Requests to `watch.ecom-store.com` with the path `/video` will be directed to the `video-service` on port 8080.
* Requests to `apparels.ecom-store.com` with the path `/wear` will be directed to the `apparels-service` on port 8080.

Create a file named `ingress.yaml` with the following content:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-vh-routing
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx-example
  rules:
  - host: watch.ecom-store.com
    http:
      paths:
      - pathType: Prefix
        path: "/video"
        backend:
          service:
            name: video-service
            port:
              number: 8080
  - host: apparels.ecom-store.com
    http:
      paths:
      - pathType: Prefix
        path: "/wear"
        backend:
          service:
            name: apparels-service
            port:
              number: 8080
```

Apply the Ingress resource:

```bash theme={null}
kubectl apply -f ingress.yaml
```

Verify that the Ingress resource is successfully created with:

```bash theme={null}
kubectl get ingress
```

<Callout icon="lightbulb">
  For more details on configuring Ingress resources, visit [Ingress in Kubernetes](https://kubernetes.io/docs/concepts/services-networking/ingress/).
</Callout>

***

## Task 5: Inspect Pod Logs and Redirect Warnings

For the final task, inspect the logs of a pod in the `default` namespace that contains a container named `log-x`. Your goal is to redirect any warning messages to a file located at `/opt/warnings.log` on the control plane node.

First, list the pods to identify the target pod:

```bash theme={null}
kubectl get pod
```

Assuming the pod identified is `dev-pod-dind-878516`, execute the following command to filter and redirect warning messages:

```bash theme={null}
kubectl logs dev-pod-dind-878516 -c log-x | grep WARNING > /opt/warnings.log
```

To verify the log output, inspect the file:

```bash theme={null}
cat /opt/warnings.log
```

<Callout icon="triangle-alert">
  Make sure you have the necessary permissions to write to `/opt/` on the control plane node.
</Callout>

***

This concludes all tasks for Lightning Lab Two. Follow each step carefully to ensure proper configuration and successful task completion. Happy Kubernetes troubleshooting!

For more Kubernetes tips and documentation, check out the [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/82805f4b-784c-4364-82ab-dfc139d96dda/lesson/eb8693e4-9787-4419-8837-4f0a4f07c97e" />
</CardGroup>


# Mock Exam 1 Solution

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Mock-Exams/Mock-Exam-1-Solution/page

This guide provides solutions for Mock Exam 1 with commands and configurations for various Kubernetes tasks.

This guide provides comprehensive solutions for Mock Exam 1. Each section explains the commands and configurations for various Kubernetes tasks. All commands assume you are operating on a Kubernetes control plane. Follow the sections below for detailed instructions.

***

## Question 1: Deploy a Pod using the Nginx Alpine Image

Deploy a pod named "nginx-448839" using the Nginx Alpine image:

```bash theme={null}
kubectl run nginx-448839 --image=nginx:alpine
```

You should see output similar to:

```bash theme={null}
pod/nginx-448839 created
```

***

## Question 2: Create a Namespace

Create a namespace "apx-Z993845" by running:

```bash theme={null}
kubectl create ns apx-Z993845
```

Expected output:

```bash theme={null}
namespace/apx-Z993845 created
```

***

## Question 3: Create a Deployment with Replicas

Create a deployment named "httpd-frontend" using the `httpd:2.4-alpine` image and scale it to three replicas:

```bash theme={null}
kubectl create deployment httpd-frontend --image=httpd:2.4-alpine --replicas=3
```

This command sets up the deployment as specified.

***

## Question 4: Deploy a Messaging Pod with a Label

Deploy a messaging pod using the Redis Alpine image and assign the label `tier=MSG`:

```bash theme={null}
kubectl run messaging --image=redis:alpine -l tier=MSG
```

This command creates the pod with the appropriate image and label.

***

## Question 5: Fix the ReplicaSet with Invalid Image Name

A ReplicaSet named `rs-d33393` is not launching pods due to a typo in the image name. Follow these steps to fix the issue:

1. Check the ReplicaSet status:

   ```bash theme={null}
   kubectl get rs
   ```

2. Describe the ReplicaSet to diagnose the problem:

   ```bash theme={null}
   kubectl describe rs rs-d33393
   ```

<Callout icon="lightbulb">
  Look for the container image field to identify the typo (`busyboxXXXXXXXX` instead of `busybox`).
</Callout>

3. Edit the ReplicaSet to correct the image name:

   ```bash theme={null}
   kubectl edit rs rs-d33393
   ```

   In the YAML, change:

   ```yaml theme={null}
   image: busyboxXXXXXXXX
   ```

   to

   ```yaml theme={null}
   image: busybox
   ```

   Also, update the number of replicas to 4 by ensuring:

   ```yaml theme={null}
   spec:
     replicas: 4
   ```

4. Delete the misconfigured pods to allow the ReplicaSet to recreate them. First, list all pods:

   ```bash theme={null}
   kubectl get pod
   ```

   Then, delete pods with the label `name=busybox-pod`:

   ```bash theme={null}
   kubectl delete pod -l name=busybox-pod
   ```

5. Verify that the ReplicaSet now has 4 ready pods:

   ```bash theme={null}
   kubectl get rs
   ```

   Expected output:

   ```bash theme={null}
   NAME          DESIRED   CURRENT   READY   AGE
   rs-d33393     4         4         4       <age>
   ```

***

## Question 6: Expose the Redis Deployment via a Service

Expose the Redis deployment in the `marketing` namespace by creating a service called "messaging-service" on port 6379:

```bash theme={null}
kubectl expose deployment redis --port=6379 --name=messaging-service --namespace=marketing
```

This command sets up a ClusterIP service for the deployment.

***

## Question 7: Update the Environment Variable on a Pod

The pod `webapp-color` has an environment variable `APP_COLOR` set to `pink`. Update it to `green` by following these steps:

1. Export the pod configuration to a YAML file:

   ```bash theme={null}
   kubectl get pod webapp-color -o yaml > webapp-color.yaml
   ```

2. Open `webapp-color.yaml` in your preferred editor and locate the environment variable section. Replace:

   ```yaml theme={null}
   - name: APP_COLOR
     value: pink
   ```

   with

   ```yaml theme={null}
   - name: APP_COLOR
     value: green
   ```

3. Apply the updated configuration by replacing the pod:

   ```bash theme={null}
   kubectl replace -f webapp-color.yaml --force
   ```

The pod will be re-created with the updated environment variable.

***

## Question 8: Create a ConfigMap with Key-Value Pairs

Create a ConfigMap named "cm-3392845" with the following key-value pairs:

* DB\_NAME: SQL3322
* DB\_HOST: sql322.mycompany.com
* DB\_PORT: 3306

Execute the command:

```bash theme={null}
kubectl create configmap cm-3392845 --from-literal=DB_NAME=SQL3322 --from-literal=DB_HOST=sql322.mycompany.com --from-literal=DB_PORT=3306
```

Verify the ConfigMap contents:

```bash theme={null}
kubectl describe cm cm-3392845
```

***

## Question 9: Create a Secret with Given Data

Create a secret named "db-secret" with the specified key-value pairs:

```bash theme={null}
kubectl create secret generic db-secret --from-literal=DB_Host=sql01 --from-literal=DB_User=root --from-literal=DB_Password=password123
```

This command creates the secret with the provided configurations.

***

## Question 10: Update a Pod to Run as Root with SYS\_TIME Capability

For the pod `app-sec-kff3345`, update the security context to run as root and enable the `SYS_TIME` capability:

1. Export the pod configuration to a YAML file:

   ```bash theme={null}
   kubectl get pod app-sec-kff3345 -o yaml > app-sec.yaml
   ```

2. Edit `app-sec.yaml` with the following modifications:

   * Under `spec.securityContext`, set `runAsUser: 0`:

     ```yaml theme={null}
     securityContext:
       runAsUser: 0
     ```

   * Under the container section (e.g., container "ubuntu"), add a security context to include the `SYS_TIME` capability:

     ```yaml theme={null}
     securityContext:
       capabilities:
         add:
           - SYS_TIME
     ```

   A sample modified section appears as:

   ```yaml theme={null}
   spec:
     containers:
       - name: ubuntu
         image: ubuntu
         command:
           - sleep
           - "4800"
         securityContext:
           capabilities:
             add:
               - SYS_TIME
     securityContext:
       runAsUser: 0
   ```

3. Apply the updated configuration by replacing the pod:

   ```bash theme={null}
   kubectl replace -f app-sec.yaml --force
   ```

***

## Question 11: Export Pod Logs to a File

Export the logs of pod `e-com-1123` in the `e-commerce` namespace to a file:

```bash theme={null}
kubectl logs e-com-1123 -n e-commerce > /path/to/your/logfile.txt
```

This command redirects the pod logs to your specified destination.

***

## Question 12: Create a Persistent Volume

Create a Persistent Volume named "pv-analytics" with the specified details:

* Capacity: 100Mi
* Access mode: ReadWriteMany
* Host path: /PV/data-analytics

Create a file called `pv.yaml` with the following content:

```yaml theme={null}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-analytics
spec:
  capacity:
    storage: 100Mi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: Slow
  hostPath:
    path: /PV/data-analytics
```

Apply the configuration:

```bash theme={null}
kubectl apply -f pv.yaml
```

***

## Question 13: Create a Redis Deployment and Expose It

1. Create a deployment named "redis" using the `redis:alpine` image with one replica:

   ```bash theme={null}
   kubectl create deployment redis --image=redis:alpine --replicas=1
   ```

2. Expose the deployment with a ClusterIP service on port 6379:

   ```bash theme={null}
   kubectl expose deployment redis --name=redis --port=6379 --target-port=6379
   ```

***

## Question 14: Create a Network Policy for Redis Access

Allow traffic to Redis only from pods with the label `access=redis` by creating a network policy. Create a file named `networkpolicy.yaml` with the following content:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: redis-access
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: redis
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: redis
    ports:
    - protocol: TCP
      port: 6379
```

Apply the network policy:

```bash theme={null}
kubectl apply -f networkpolicy.yaml
```

***

## Question 15: Create a Pod with Two Containers

Create a pod named "sega" that includes two containers:

* Container "tails": uses the `busybox` image and runs a sleep command for 3600 seconds.
* Container "sonic": uses the `nginx` image and sets the environment variable `NGINX_PORT` to "8080".

Create a file called `sega.yaml` with the following content:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: sega
spec:
  containers:
    - name: tails
      image: busybox
      command:
        - sleep
        - "3600"
    - name: sonic
      image: nginx
      env:
        - name: NGINX_PORT
          value: "8080"
```

Apply the pod configuration:

```bash theme={null}
kubectl apply -f sega.yaml
```

If an update is required later, replace the pod with:

```bash theme={null}
kubectl replace -f sega.yaml --force
```

***

That concludes the steps for Mock Exam 1. Each section documents the command or configuration change required. Happy deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/36d5003c-cbf5-4311-9e52-78a17776f919/lesson/2d24748c-3f4c-4ecc-b9fa-a1ef91b240d5" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/36d5003c-cbf5-4311-9e52-78a17776f919/lesson/3253aaee-d6ce-4d4c-aadf-b855ebebcc70" />
</CardGroup>
