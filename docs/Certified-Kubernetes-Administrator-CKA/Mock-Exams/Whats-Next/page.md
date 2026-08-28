# sysctl params required by setup, params persist across reboots
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.ipv4.ip.forward = 1
EOF

# Apply sysctl params without reboot
sudo sysctl --system
```

<Callout icon="lightbulb">
  Always copy the exact command names from the exam instructions to avoid errors.
</Callout>

This completes Question 1.

***

## Question 2 – Creating a Service Account and Granting PVC Listing Permissions

In this question you will:

1. Create a service account named **pvviewer**.
2. Create a cluster role (**pvviewer-role**) that grants permission to list persistent volumes.
3. Bind the role to the service account with a cluster role binding (**pvviewer-role-binding**).
4. Launch a pod (**pvviewer**) using the Redis image in the default namespace.

### Step 1: Create the Service Account

```bash theme={null}
kubectl create serviceaccount pvviewer
kubectl get sa
```

*Expected output:*

```plaintext theme={null}
NAME      SECRETS   AGE
default   0         6m55s
pvviewer  0         5s
```

### Step 2: Create the Cluster Role

Create the role with the required permission:

```bash theme={null}
kubectl create clusterrole pvviewer-role --resource=persistentvolumes --verb=list
```

Verify with:

```bash theme={null}
kubectl describe clusterrole pvviewer-role
```

*Expected output snippet:*

```plaintext theme={null}
Name:         pvviewer-role
Labels:       <none>
Annotations:  <none>
PolicyRules:
  Resource            Non-Resource URLs  Resource Names  Verbs
  ------------------  -----------------  --------------  -----
  persistentvolumes   []                 []              [list]
```

### Step 3: Bind the Role to the Service Account

```bash theme={null}
kubectl create clusterrolebinding pvviewer-role-binding --clusterrole=pvviewer-role --serviceaccount=default:pvviewer
```

### Step 4: Launch the Pod

Create a pod manifest (e.g., `question2.yaml`):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: pvviewer
spec:
  serviceAccountName: pvviewer
  containers:
    - name: pvviewer
      image: redis
```

Apply the manifest:

```bash theme={null}
kubectl apply -f question2.yaml
```

Verify the pod and its service account:

```bash theme={null}
kubectl get pod
kubectl describe pod pvviewer
```

This completes Question 2.

<Frame>
  ![The image shows a Kubernetes task description on the left, instructing to create a service account and related roles, and a terminal on the right with a context menu open.](https://kodekloud.com/kk-media/image/upload/v1752869819/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Mock-Exam-3-Step-by-Step-Solutions/kubernetes-task-service-account-roles.jpg)
</Frame>

***

## Question 3 – Creating a Storage Class

Create a storage class called **rancher-sc** with these settings:

* Provisioner: `rancher.io/local-path`
* Allow volume expansion: `true`
* Volume binding mode: `WaitForFirstConsumer`

Example manifest (`question3.yaml`):

```yaml theme={null}
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rancher-sc
provisioner: rancher.io/local-path
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

Apply the storage class:

```bash theme={null}
kubectl apply -f question3.yaml
```

This completes Question 3.

<Frame>
  ![The image shows a search results page from the Kubernetes website, displaying results for the query "storageclass." It includes links to various Kubernetes documentation and articles related to storage classes.](https://kodekloud.com/kk-media/image/upload/v1752869820/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Mock-Exam-3-Step-by-Step-Solutions/kubernetes-storageclass-search-results.jpg)
</Frame>

***

## Question 4 – Configuring a ConfigMap and Updating a Deployment

In the **cm-namespace**, perform these tasks:

1. Create a ConfigMap **app-config** containing key-value pairs such as `ENV=production` and `LOG_LEVEL=info`.
2. Update the existing deployment **cm-web-app** to source environment variables from the ConfigMap.

### Step 1: Create the ConfigMap

```bash theme={null}
kubectl create configmap app-config -n cm-namespace --from-literal=ENV=production --from-literal=LOG_LEVEL=info
```

Verify with:

```bash theme={null}
kubectl describe cm app-config -n cm-namespace
```

### Step 2: Update the Deployment

Edit the deployment to include the ConfigMap:

```bash theme={null}
kubectl edit deployment cm-webapp -n cm-namespace
```

*Add the following under the container section:*

```yaml theme={null}
envFrom:
  - configMapRef:
      name: app-config
```

After saving, verify that new pods include the environment variables from **app-config**.

This completes Question 4.

<Frame>
  ![The image shows a Kubernetes task interface with instructions to create a ConfigMap and modify a Deployment, alongside a terminal displaying YAML configuration for a Kubernetes deployment.](https://kodekloud.com/kk-media/image/upload/v1752869821/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Mock-Exam-3-Step-by-Step-Solutions/kubernetes-configmap-deployment-yaml.jpg)
</Frame>

***

## Question 5 – Configuring Priority Classes and Pod Priority

For this task, you need to:

1. Create a PriorityClass **low-priority** with a value of 50,000.
2. Modify the existing pod **lp-pod** (in the **low-priority** namespace) to reference this PriorityClass.
3. Recreate the pod so that it picks up the new priority without manually setting a numeric value.

### Step 1: Create the PriorityClass

Create a manifest (e.g., `question5.yaml`):

```yaml theme={null}
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 50000
globalDefault: false
description: "This is a low priority class"
```

Apply it:

```bash theme={null}
kubectl apply -f question5.yaml
```

### Step 2: Update the Pod Manifest

Create or edit the pod manifest (e.g., `question5-pod.yaml`) to include only the PriorityClass name:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: lp-pod
  namespace: low-priority
  labels:
    run: lp-pod
spec:
  priorityClassName: low-priority
  containers:
    - name: lp-pod
      image: nginx
      imagePullPolicy: Always
      resources: {}
      terminationMessagePath: /dev/termination-log
      terminationMessagePolicy: File
  dnsPolicy: ClusterFirst
  restartPolicy: Always
```

*Do not include a numeric `priority` field.*

Replace the pod if needed:

```bash theme={null}
kubectl replace -f question5-pod.yaml --force
# If an error appears about a numeric priority, remove any "priority: 0" specification and apply again:
kubectl apply -f question5-pod.yaml
```

Finally, verify the pod:

```bash theme={null}
kubectl get pod -n low-priority
```

This completes Question 5.

***

## Question 6 – Fixing Incoming Connection Issues with a Network Policy

A pod (**np-test-1**) and its service (**np-test-service**) are not receiving incoming traffic on port 80. Create a NetworkPolicy named **test-network-policy** to allow TCP traffic on port 80.

First, confirm the pod’s labels:

```bash theme={null}
kubectl get pod --show-labels
```

Then, create a manifest (e.g., `question6.yaml`):

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: np-test-1
  policyTypes:
  - Ingress
  ingress:
  - ports:
    - protocol: TCP
      port: 80
```

Apply the policy:

```bash theme={null}
kubectl apply -f question6.yaml
```

This policy permits incoming TCP traffic on port 80 for pods labeled `run=np-test-1`.

***

## Question 7 – Tainting a Node and Creating Pods with Tolerations

In this question, you will:

1. Taint a worker node (**node01**) with `env_type=production:NoSchedule`.
2. Create a pod (**dev-redis**) without tolerations so it avoids node01.
3. Create another pod (**prod-redis**) with a toleration to allow scheduling on node01.

### Step 1: Taint the Node

```bash theme={null}
kubectl taint node node01 env_type=production:NoSchedule
```

Verify the taint:

```bash theme={null}
kubectl describe node node01 | grep -i taint
```

### Step 2: Create the Non-Tolerant Pod

Using an imperative command:

```bash theme={null}
kubectl run dev-redis --image=redis:alpine
```

### Step 3: Create the Tolerant Pod

Create a manifest (e.g., `question7.yaml`):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: prod-redis
spec:
  containers:
    - name: prod-redis
      image: redis:alpine
  tolerations:
    - key: "env_type"
      operator: "Equal"
      value: "production"
      effect: "NoSchedule"
```

Apply it:

```bash theme={null}
kubectl apply -f question7.yaml
```

Finally, check that **prod-redis** is scheduled on **node01** while **dev-redis** is not:

```bash theme={null}
kubectl get pod -o wide
```

***

## Question 8 – Binding a PVC to a PV by Matching Access Modes

A PersistentVolumeClaim (**app-pvc**) in the **storage-ns** namespace is not binding with the PersistentVolume (**app-pv**) because the PVC requests **ReadWriteMany** and the PV provides **ReadWriteOnce**. Update the PVC to request `["ReadWriteOnce"]` as the access mode.

After modifying the PVC manifest, remove the old PVC and apply the corrected file:

```bash theme={null}
kubectl delete pvc app-pvc -n storage-ns
kubectl apply -f <updated-pvc-manifest.yaml>
```

Verify the binding:

```bash theme={null}
kubectl get pvc -n storage-ns
```

The PVC should now be **Bound** to the PV.

***

## Question 9 – Troubleshooting a Faulty Kubeconfig File

The kubeconfig file **super.kubeconfig** (located at `/root/CKA/super.kubeconfig`) is returning a “connection refused” error. The issue is found in the cluster section where the server is set to:

```text theme={null}
https://controlplane:9999
```

Since the kube-apiserver listens on port **6443**, update the kubeconfig file as follows:

```yaml theme={null}
clusters:
- cluster:
    certificate-authority-data: <data>
    server: https://controlplane:6443
  name: kubernetes
```

After saving the changes, test the connection:

```bash theme={null}
kubectl get node --kubeconfig=/root/CKA/super.kubeconfig
```

The connection should now work without errors.

***

## Question 10 – Scaling a Deployment

The **nginx-deploy** deployment currently has 1 replica. To scale it to 3 replicas:

1. Check the current status:

   ```bash theme={null}
   kubectl get deployment nginx-deploy
   ```

2. Scale the deployment:

   ```bash theme={null}
   kubectl scale deployment nginx-deploy --replicas=3
   ```

3. Verify the change:

   ```bash theme={null}
   kubectl get deployment nginx-deploy
   ```

If the deployment still shows one available replica, review the deployment events:

```bash theme={null}
kubectl describe deployment nginx-deploy
```

Troubleshoot any issues such as ReplicaSet misconfigurations or control plane component errors (for example, verify the kube-controller-manager manifest at `/etc/kubernetes/manifests/kube-controller-manager.yaml`).

This completes Question 10.

***

## Question 11 – Creating a Horizontal Pod Autoscaler (HPA) with Custom Metric

For the **api-deployment** in the **api** namespace, create an HPA that scales based on a custom pod metric (`requests_per_second`), targeting an average value of 1000 with a range of 1 to 20 pods.

Create a manifest (e.g., `question11.yaml`):

```yaml theme={null}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 1
  maxReplicas: 20
  metrics:
    - type: Pods
      pods:
        metric:
          name: requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
```

Apply the HPA:

```bash theme={null}
kubectl apply -f question11.yaml
```

Verify its configuration:

```bash theme={null}
kubectl describe hpa -n api
```

This completes Question 11.

***

## Question 12 – Configuring an HTTPRoute to Split Traffic

To distribute incoming web traffic, configure an HTTP route to split between **web-service** (80%) and **web-service-v2** (20%). The associated web gateway and services already exist.

Create an HTTPRoute manifest (e.g., `question12.yaml`):

```yaml theme={null}
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-route
  namespace: default
spec:
  parentRefs:
    - name: web-gateway
      namespace: default
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: web-service
          port: 80
          weight: 80
        - name: web-service-v2
          port: 80
          weight: 20
```

Apply the route:

```bash theme={null}
kubectl apply -f question12.yaml
```

This successfully routes 80% of traffic to **web-service** and 20% to **web-service-v2**.

***

## Question 13 – Upgrading an Application Using Helm

You need to upgrade an application using a Helm chart from the directory `/root/new-version`. Follow these steps:

1. **Validate the Chart:**

   ```bash theme={null}
   helm lint /root/new-version
   ```

   *Expected message:*

   ```plaintext theme={null}
   ==> Linting /root/new-version
   [INFO] Chart.yaml: icon is recommended
   1 chart(s) linted, 0 chart(s) failed
   ```

2. **Install the Chart:**

   Use an auto-generated name:

   ```bash theme={null}
   helm install --generate-name /root/new-version
   ```

   List the releases:

   ```bash theme={null}
   helm list
   ```

3. **Uninstall the Old Version:**

   Replace `<old-release-name>` with the actual release name:

   ```bash theme={null}
   helm uninstall <old-release-name>
   ```

Verify the installation:

```bash theme={null}
helm list
```

This completes Question 13.

***

## Question 14 – Outputting the Pod CIDR Network

To determine the pod CIDR network of the cluster and save it to `/root/pod-cidr.txt`, extract the podCIDR from one of the nodes:

```bash theme={null}
kubectl get node -o jsonpath='{.items[0].spec.podCIDR}' > /root/pod-cidr.txt
```

Verify the file content:

```bash theme={null}
cat /root/pod-cidr.txt
```

*Expected output (example):*

```plaintext theme={null}
172.17.0.0/24
```

This completes Question 14 and wraps up the mock exam solutions.

***

End of Lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/d33baa6d-ccd3-410b-a20c-5d5b9c7a2114/lesson/37fcfdf5-d76d-4101-9315-4373086da5f7" />
</CardGroup>


# Whats Next

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Mock-Exams/Whats-Next/page

This course offers comprehensive mock exams for realistic CKA exam practice in a simulated environment.

Hello everyone, and welcome to the Ultimate CKA Mock Exam Series presented by Vijen Palazi from KodeKloud.

Before diving in, please ensure that you have completed all the prerequisite materials, including multiple mock exams and hands-on labs. If your CKA exam is approaching soon, it's essential to review all the background content first.

This course is designed as a series of comprehensive and challenging mock exams, offering you realistic, hands-on practice in a simulated exam environment. Unlike our regular labs, each mock exam uniquely mimics the actual test conditions.

The CKA exam assesses your practical knowledge in five key areas:

* Architecture, Installation, and Maintenance: 25%
* Workload Scheduling: 15%
* Service Networking: 20%
* Storage: 10%
* Troubleshooting: 30%

<Frame>
  ![A person is speaking with a pie chart labeled "Workloads & Scheduling 15%" displayed beside them.](https://kodekloud.com/kk-media/image/upload/v1752869831/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Whats-Next/frame_70.jpg)
</Frame>

<Frame>
  ![A person is speaking with a circular progress chart labeled "Troubleshooting 30%" displayed beside them.](https://kodekloud.com/kk-media/image/upload/v1752869832/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Whats-Next/frame_80.jpg)
</Frame>

Each mock exam respects the weight of these areas, ensuring you receive a realistic testing experience. The series uses four Kubernetes clusters, with some clusters dedicated to specific knowledge areas. By default, you will be logged into the student node, giving you access to all other clusters and allowing SSH access to individual nodes.

<Frame>
  ![A person is speaking next to a list titled "Exam Cluster," detailing four Kubernetes (K8s) clusters with varying node configurations.](https://kodekloud.com/kk-media/image/upload/v1752869834/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Whats-Next/frame_100.jpg)
</Frame>

This introduction marks the beginning of your journey through the Ultimate CKA Mock Exam Series.

<Frame>
  ![A KodeKloud mock exam interface shows a 95% score with completed questions, alongside a video of a person speaking.](https://kodekloud.com/kk-media/image/upload/v1752869835/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Whats-Next/frame_120.jpg)
</Frame>

Let’s dive into one of these tests.

## Starting the Mock Exam

Click on a lab corresponding to one of the mock exams (for example, "CKA Mock Exam One"). The lab should load within 30 seconds—often in just one to two minutes.

Once loaded, you will see that the exam consists of 20 questions. The first question is from the Architecture, Installation, and Maintenance category, representing 25% of the exam. This question requires you to set the context to cluster three.

Before proceeding, verify all the configured clusters. Switch to cluster three with the following command:

```bash theme={null}
kubectl config use-context cluster3
```

You are now logged into the student node. To view all configured clusters, run:

```bash theme={null}
kubectl config get-clusters
```

By default, without an explicitly set context, you connect to cluster one, which contains two worker nodes (node01 and node02). For this task, you must switch to cluster three. On the student node, execute:

```bash theme={null}
kubectl config use-context cluster3
kubectl config get-clusters
kubectl config get-contexts
kubectl get nodes
```

The student node serves as your client login node. If you open a new terminal session, it will also start in the student node. To access any specific control plane, use the SSH command.

When your context is correctly set to cluster three, executing:

```bash theme={null}
kubectl get nodes
```

will display a single-node cluster consisting of the control plane (e.g., "cluster3-controlplane") running Kubernetes version 1.24.1. It is highly recommended to set the appropriate context for each question so you interact with the correct cluster.

For example, verify the nodes in cluster three with:

```bash theme={null}
kubectl config use-context cluster3
kubectl get nodes
```

This command should return:

```bash theme={null}
NAME                     STATUS   ROLES                     AGE   VERSION
cluster3-controlplane    Ready    control-plane,master      18m   v1.24.1+k3s1
```

## Working Through a Question

Let's review a sample question. You may need to decode an existing secret, named "beta-sec-CK14-arc", which is created in a separate namespace. First, ensure the namespace exists by listing the secrets in that namespace:

```bash theme={null}
kubectl get secret -n beta-ns-cka14-arch
```

Then, retrieve the secret in YAML format to inspect the data:

```bash theme={null}
kubectl get secrets -n beta-ns-cka14-arch -o yaml
```

The secret data is stored under the "data" section. To decode the secret from a base64-encoded string, run:

```bash theme={null}
echo 'VGHpcpyB0aG9lUGc2VjcjmV0IQ=' | base64 -d
```

The decoded output should be: "This is the secret." You can redirect the decoded output directly into a file on the student node with:

```bash theme={null}
kubectl config use-context cluster3
kubectl get secrets -n beta-ns-cka14-arch -o yaml

echo 'VGHpcpyB0aG9lUGc2VjcjmV0IQ=' | base64 -d > /opt/beta-sec-cka14-arch
```

Scroll through the exam interface to view the remaining questions. The first question is worth eight points from the Architecture, Installation, and Maintenance section. The second question from the same section can be attempted with:

```bash theme={null}
kubectl config use-context cluster3
kubectl get secrets -n beta-ns-cka14-arch
kubectl get secrets -n beta-ns-cka14-arch -o yaml
echo 'VGhpcyBpc28sIHlvdSBhcmUgY29tbWl0dGVkIQ==' | base64 -d
echo 'VGhpcyBpc28sIHlvdSBhcmUgY29tbWl0dGVkIQ==' | base64 -d > /opt/beta-sec-cka14-arch
```

Remember, you must compile all solutions before the allotted time expires. If time runs out, the exam will automatically finish and be validated.

<Callout icon="lightbulb">
  Always double-check that you have switched the context appropriately using `kubectl config use-context <cluster-name>` before running commands that interact with cluster-specific resources.
</Callout>

You might also encounter additional commands to review logs and secrets, such as:

```bash theme={null}
kubectl config use-context cluster1
kubectl logs -f color-app-cka13-arch
kubectl get secrets -n beta-ns-cka14-arch
kubectl get secrets -n beta-ns-cka14-arch -o yaml
echo 'VhgpcyBpyB0aGluc2Jvc1QIQo=' | base64 -d > /opt/beta-sec-cka14-arch
```

At any time during the exam, you can click the "End Exam" button to check your score. In this demonstration, only the first question is attempted, with all other questions marked incorrect by default.

For example, reviewing the secret on the student node might show output like:

```bash theme={null}
student-node → kubectl get secrets -n beta-ns-cka14-arch
NAME                       TYPE     DATA   AGE
beta-sec-cka14-arch        Opaque   1      2m19s

student-node → kubectl get secrets -n beta-ns-cka14-arch -o yaml
apiVersion: v1
items:
- apiVersion: v1
  data:
    secret: VGhpcyBpc8yB0aGluZyBQcml0b3JpdHk=
  kind: Secret
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"v1","data":{"secret":"VGhpcyBpc8yB0aGluZyBQcml0b3JpdHk="},"kind":"Secret","metadata":{"name":"beta-sec-cka14-arch","namespace":"beta-ns-cka14-arch"},"type":"Opaque"}
    creationTimestamp: "2023-02-02T17:08:47Z"
    name: beta-sec-cka14-arch
    namespace: beta-ns-cka14-arch
    resourceVersion: "846"
    uid: ef9c5d98-aec0-4d4d-99be-1cbb989b5e0
  type: Opaque
kind: List
metadata:
  resourceVersion: ""
  selfLink: ""

student-node → echo VGhpcyBpc8yB0aGluZyBQcml0b3JpdHk= | base64 -d
This is the secret!
```

Additional exam commands might include:

```bash theme={null}
kubectl config use-context cluster1
kubectl get secrets -n beta-ns-cka14-arch -o yaml
curl http://cluster1-node01:30080
echo 'VGhpcyBpcyBhIHNlY3JldCE=' | base64 -d
echo 'VGhpcyBpcyB0aGUgc2VjcmV0IQ==' | base64 -d > /opt/beta-sec-cka14-arch
```

These steps ensure that you are working within the correct context and that your solutions are properly validated.

After completing your attempt, click the "End Exam" button to trigger automatic exam validation.

For reference, a sample terminal session may look like:

```bash theme={null}
student-node ~ ➜ kubectl --context cluster1 create
student-node ~ ➜ kubectl --context cluster1 create
student-node ~ ➜ kubectl --context cluster1 create
student-node ~ ➜ kubectl --context cluster1 auth
yes
```

<Callout icon="lightbulb">
  Always verify your solutions and ensure you are working on the correct cluster context to avoid misconfigurations.
</Callout>

I hope you find this article useful. Best of luck with your CKA preparation!

Thank you.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/d33baa6d-ccd3-410b-a20c-5d5b9c7a2114/lesson/dca9c12d-8a8b-4691-8d07-950c62a2043a" />
</CardGroup>
