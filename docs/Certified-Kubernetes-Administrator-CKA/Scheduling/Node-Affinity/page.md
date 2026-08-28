# my-scheduler-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: my-scheduler
```

```yaml theme={null}
# scheduler-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: default-scheduler
```

***

## Deploying an Additional Scheduler

You can deploy an additional scheduler using the existing kube-scheduler binary, tailoring its configuration through specific service files.

### Step 1: Download the kube-scheduler Binary

Begin by downloading the kube-scheduler binary:

```bash theme={null}
wget https://storage.googleapis.com/kubernetes-release/release/v1.12.0/bin/linux/amd64/kube-scheduler
```

### Step 2: Create Service Files

Create separate service files for each scheduler. For example, consider the following definitions:

```bash theme={null}
# kube-scheduler.service
ExecStart=/usr/local/bin/kube-scheduler --config=/etc/kubernetes/config/kube-scheduler.yaml
```

```bash theme={null}
# my-scheduler-2.service
ExecStart=/usr/local/bin/kube-scheduler --config=/etc/kubernetes/config/my-scheduler-2-config.yaml
```

### Step 3: Define Scheduler Configuration Files

Reference the scheduler names in the associated configuration files:

```yaml theme={null}
# my-scheduler-2-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: my-scheduler-2
```

```yaml theme={null}
# my-scheduler-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: my-scheduler
```

<Callout icon="lightbulb">
  Several code blocks might look similar or repeated. The examples above represent a consolidated view for clarity.
</Callout>

***

## Deploying the Custom Scheduler as a Pod

In addition to running the scheduler as a service, you can deploy it as a pod inside the Kubernetes cluster. This method involves creating a pod definition that references the scheduler’s configuration file.

### Example Pod Definition

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: my-custom-scheduler
  namespace: kube-system
spec:
  containers:
    - name: kube-scheduler
      image: k8s.gcr.io/kube-scheduler-amd64:v1.11.3
      command:
        - kube-scheduler
        - --address=127.0.0.1
        - --kubeconfig=/etc/kubernetes/scheduler.conf
        - --config=/etc/kubernetes/my-scheduler-config.yaml
```

The corresponding custom scheduler configuration file might look like:

```yaml theme={null}
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: my-scheduler
```

<Callout icon="lightbulb">
  Leader election is an important configuration for high-availability environments. It ensures that while multiple scheduler instances are running, only one actively schedules the pods.
</Callout>

***

## Deploying the Custom Scheduler as a Deployment

In many modern Kubernetes setups—especially those using kubeadm—control plane components run as pods or deployments. Below is an example of deploying a custom scheduler as a Deployment.

### Step 1: Build and Push a Custom Scheduler Image

Create a Dockerfile for your custom scheduler:

```dockerfile theme={null}
FROM busybox
ADD ./.output/local/bin/linux/amd64/kube-scheduler /usr/local/bin/kube-scheduler
```

Build and push the Docker image:

```bash theme={null}
docker build -t gcr.io/my-gcp-project/my-kube-scheduler:1.0 .
gcloud docker -- push gcr.io/my-gcp-project/my-kube-scheduler:1.0
```

### Step 2: Create ServiceAccount and RBAC Configurations

Prepare the following YAML to create a service account and set appropriate RBAC permissions:

```yaml theme={null}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-scheduler
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: my-scheduler-as-kube-scheduler
subjects:
  - kind: ServiceAccount
    name: my-scheduler
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: system:kube-scheduler
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: my-scheduler-as-volume-scheduler
subjects:
  - kind: ServiceAccount
    name: my-scheduler
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: system:volume-scheduler
  apiGroup: rbac.authorization.k8s.io
```

### Step 3: Create a ConfigMap for Scheduler Configuration

Define a ConfigMap that includes your custom scheduler configuration:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-scheduler-config
  namespace: kube-system
data:
  my-scheduler-config.yaml: |
    apiVersion: kubescheduler.config.k8s.io/v1beta2
    kind: KubeSchedulerConfiguration
    profiles:
      - schedulerName: my-scheduler
        leaderElection:
          leaderElect: false
```

### Step 4: Define the Deployment

Deploy the custom scheduler as a Deployment with the following YAML:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-scheduler
  namespace: kube-system
  labels:
    component: scheduler
    tier: control-plane
spec:
  replicas: 1
  selector:
    matchLabels:
      component: scheduler
      tier: control-plane
  template:
    metadata:
      labels:
        component: scheduler
        tier: control-plane
        version: second
    spec:
      serviceAccountName: my-scheduler
      containers:
        - name: kube-second-scheduler
          image: gcr.io/my-gcp-project/my-kube-scheduler:1.0
          command:
            - /usr/local/bin/kube-scheduler
            - --config=/etc/kubernetes/my-scheduler/my-scheduler-config.yaml
          livenessProbe:
            httpGet:
              path: /healthz
              port: 10259
              scheme: HTTPS
            initialDelaySeconds: 15
          readinessProbe:
            httpGet:
              path: /healthz
              port: 10259
              scheme: HTTPS
          volumeMounts:
            - name: config-volume
              mountPath: /etc/kubernetes/my-scheduler
      volumes:
        - name: config-volume
          configMap:
            name: my-scheduler-config
```

Also, ensure a proper ClusterRole exists for the scheduler. For example:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:kube-scheduler
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
rules:
  - apiGroups:
      - coordination.k8s.io
    resources:
      - leases
    verbs:
      - create
  - apiGroups:
      - coordination.k8s.io
    resourceNames:
      - kube-scheduler
      - my-scheduler
    resources:
      - leases
    verbs:
      - get
      - list
      - watch
```

***

## Configuring Workloads to Use the Custom Scheduler

To have specific pods or deployments use your custom scheduler, add the "schedulerName" field in the pod's specification. For example:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx
  schedulerName: my-custom-scheduler
```

Deploy this pod with:

```bash theme={null}
kubectl create -f pod-definition.yaml
```

If the custom scheduler configuration is incorrect, the pod may remain in the Pending state. Conversely, a properly scheduled pod will transition to the Running state.

***

## Verifying Scheduler Operation

To confirm which scheduler assigned a pod, review the events in your namespace:

```bash theme={null}
kubectl get events -o wide
```

A sample output might appear as follows:

```text theme={null}
LAST SEEN   COUNT   NAME        KIND   TYPE    REASON      SOURCE                  MESSAGE
9s          1       nginx.15    Pod    Normal  Scheduled   my-custom-scheduler     Successfully assigned default/nginx to node01
8s          1       nginx.15    Pod    Normal  Pulling     kubelet, node01         pulling image "nginx"
2s          1       nginx.15    Pod    Normal  Pulled      kubelet, node01         Successfully pulled image "nginx"
2s          1       nginx.15    Pod    Normal  Created     kubelet, node01         Created container
2s          1       nginx.15    Pod    Normal  Started     kubelet, node01         Started container
```

Notice that the event source is "my-custom-scheduler," confirming that the pod was scheduled by your custom scheduler.

If you encounter issues, view the scheduler logs with:

```bash theme={null}
kubectl logs my-custom-scheduler --namespace=kube-system
```

A sample log output might include messages like:

```text theme={null}
I0204 09:42:25.819338   1 server.go:126] Version: v1.11.3
W0204 09:42:25.822720   1 authorization.go:47] Authorization is disabled
W0204 09:42:25.822745   1 authentication.go:55] Authentication is disabled
I0204 09:42:25.822801   1 insecure_serving.go:47] Serving healthz insecurely on 127.0.0.1:10251
I0204 09:45:14.725407   1 controller_utils.go:1025] Waiting for caches to sync for scheduler controller
I0204 09:45:14.825634   1 controller_utils.go:1032] Caches are synced for scheduler controller
I0204 09:45:14.825814   1 leaderelection.go:185] attempting to acquire leader lease kube-system/my-custom-scheduler...
I0204 09:45:14.834953   1 leaderelection.go:194] successfully acquired lease kube-system/my-custom-scheduler
```

This confirms that the custom scheduler is up and functioning as expected.

***

## Conclusion

By following these techniques, you can run both the default Kubernetes scheduler and one or more custom schedulers concurrently. This flexibility allows you to assign specific workloads to the most appropriate scheduler based on your cluster’s requirements.

Happy scheduling!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/a1359d88-99be-4049-905c-32c0226da353" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/e237ec9f-3c5a-4ed4-ada8-ab3769579775" />
</CardGroup>


# Node Affinity

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Scheduling/Node-Affinity/page

This article explains node affinity in Kubernetes, detailing advanced scheduling rules for pod placement based on node labels.

Welcome to this comprehensive lesson on node affinity in Kubernetes. In this guide, you'll learn how node affinity extends the capabilities of basic node selectors by allowing advanced expressions like In, NotIn, and Exists. This feature enables you to specify detailed rules for pod placement based on node labels.

Previously, you might have used node selectors for basic scheduling. For example, to ensure that a large data processing pod runs on a large node, you could use a configuration like this:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
    - name: data-processor
      image: data-processor
  nodeSelector:
    size: Large
```

While node selectors are simple and intuitive, they lack support for advanced matching operators. Node affinity overcomes these limitations by allowing more expressive rules. The example below demonstrates how to schedule a pod on a node labeled as large using node affinity:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
    - name: data-processor
      image: data-processor
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: size
                operator: In
                values:
                  - Large
```

<Callout icon="lightbulb">
  • The `affinity` key under `spec` introduces the `nodeAffinity` configuration.\
  • The field `requiredDuringSchedulingIgnoredDuringExecution` indicates that the scheduler must place the pod on a node meeting the criteria. Once the pod is running, any changes to node labels are ignored.\
  • The `nodeSelectorTerms` array contains one or more `matchExpressions`. Each expression specifies a label key, an operator, and a list of values. Here, the `In` operator ensures that the pod is scheduled only on nodes where the label `size` includes ‘Large’.
</Callout>

To allow for more flexible scheduling, such as permitting a pod to run on either large or medium nodes, simply add additional values to the list. Alternatively, you can use the `NotIn` operator to explicitly avoid placing a pod on nodes with specific labels. For example, to avoid nodes labeled as small:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
    - name: data-processor
      image: data-processor
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: size
                operator: NotIn
                values:
                  - Small
```

In cases where you only need to verify the presence of a label without checking for specific values, the `Exists` operator is useful. When using `Exists`, you do not provide a list of values:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: data-processor
    image: data-processor
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: size
            operator: Exists
```

<Callout icon="lightbulb">
  Once a pod is scheduled using node affinity rules, these rules are only evaluated during scheduling. Changes to node labels after scheduling will not affect a running pod due to the "ignored during execution" behavior.
</Callout>

There are two primary scheduling behaviors for node affinity:

1. **Required During Scheduling, Ignored During Execution**
   * The pod is scheduled only on nodes that fully satisfy the affinity rules.
   * Once running, changes to node labels do not impact the pod.

2. **Preferred During Scheduling, Ignored During Execution**
   * The scheduler prefers nodes that meet the affinity rules but will place the pod on another node if no matching nodes are available.

<Frame>
  ![The image explains node affinity types, showing "requiredDuringSchedulingIgnoredDuringExecution" and "preferredDuringSchedulingIgnoredDuringExecution" with a table detailing scheduling and execution requirements.](https://kodekloud.com/kk-media/image/upload/v1752869895/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Node-Affinity/frame_340.jpg)
</Frame>

Future enhancements may introduce additional affinity types, such as **Required During Execution**. In this model, if a node's labels change after a pod is running and no longer meet the affinity criteria, the pod would be evicted.

<Frame>
  ![The image shows a table explaining node affinity types, detailing scheduling and execution requirements for four types, with planned features listed above.](https://kodekloud.com/kk-media/image/upload/v1752869896/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Node-Affinity/frame_410.jpg)
</Frame>

## Summary

Node affinity empowers you to define sophisticated scheduling rules for pod placement based on node labels. Key takeaways include:

* Using `nodeSelectorTerms` with `matchExpressions` to specify rules.
* Leveraging operators such as `In`, `NotIn`, and `Exists` for flexible matching.
* Understanding the scheduling phases: during scheduling and after deployment (execution), and how they interact.

This concludes our lesson on node affinity. Practice the provided configurations and explore further by comparing node affinity with taints and tolerations. Happy learning and coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/19826c73-c55c-4eba-b5b2-81df0f2850b7" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/7231d50c-f8fb-44c4-9935-fb84ffb4c347" />
</CardGroup>
