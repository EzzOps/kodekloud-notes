# Output: cGFzd3Jk
```

## Viewing and Decoding Secrets

After creating a Secret, you can list and inspect it with the following commands:

* **List Secrets:**

  ```bash theme={null}
  kubectl get secrets
  ```

  Expected output:

  ```plaintext theme={null}
  NAME          TYPE    DATA   AGE
  app-secret    Opaque    3    10m
  ```

* **Describe a Secret (without showing sensitive data):**

  ```bash theme={null}
  kubectl describe secret app-secret
  ```

* **View the encoded data in YAML format:**

  ```bash theme={null}
  kubectl get secret app-secret -o yaml
  ```

If you need to decode an encoded value, use the `base64 --decode` command:

```bash theme={null}
echo -n 'bXlzcWw=' | base64 --decode
echo -n 'cm9vdA==' | base64 --decode
echo -n 'cGFzd3Jk' | base64 --decode
# Output: paswrd
```

## Injecting Secrets into a Pod

Once the Secret is created, you can inject it into a Pod using environment variables or by mounting them as files in a volume.

### Injecting as Environment Variables

Below is an example Pod definition that injects the Secret as environment variables:

```yaml theme={null}
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
  labels:
    name: simple-webapp-color
spec:
  containers:
  - name: simple-webapp-color
    image: simple-webapp-color
    ports:
    - containerPort: 8080
    envFrom:
    - secretRef:
        name: app-secret
```

### Mounting Secrets as Files

Alternatively, mount the Secret as files within a volume. Each key in the Secret becomes a separate file:

```yaml theme={null}
volumes:
- name: app-secret-volume
  secret:
    secretName: app-secret
```

After mounting, listing the directory contents should display each key as a file:

```bash theme={null}
ls /opt/app-secret-volumes
# Output: DB_Host  DB_Password  DB_User
```

To view the content of a specific file, such as the DB password:

```bash theme={null}
cat /opt/app-secret-volumes/DB_Password
# Output: paswrd
```

## Important Considerations When Using Secrets

> **triangle-alert** Remember that Kubernetes Secrets are only encoded in Base64, not encrypted by default. Anyone with sufficient access can decode the data. Always handle secret definition files with care and avoid storing them in public repositories.

Here are some key considerations:

* Secrets offer only Base64 encoding. For enhanced security, consider enabling encryption at rest for etcd.
* Limit access to Secrets using Role-Based Access Control (RBAC). Restrict permissions to only those who require it.
* Avoid storing sensitive secret definition files in source control systems that are publicly accessible.
* For even greater security, explore third-party secret management solutions such as AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, or Vault.

## External Secret Providers

External secret providers decouple secret management from etcd and offer advanced encryption, granular access control, and comprehensive auditing capabilities. For further details and best practices, consider exploring courses like the [Certified Kubernetes Security Specialist (CKS)](https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks).

![The image provides guidelines on handling secrets, emphasizing encryption, access control, and considering third-party providers for secure storage.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869672/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Secrets/frame_470.jpg)

## Conclusion

Managing Kubernetes Secrets effectively is crucial for maintaining the security of your applications. By following the best practices outlined above, including using Secrets to handle sensitive data and applying strict RBAC policies, you can mitigate potential security risks associated with managing sensitive configuration data.

Practice these approaches using hands-on labs and ensure your Kubernetes clusters are secure.

For additional resources, consider the following links:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/2ddcf79b-abb0-4aeb-ad0c-3d54c7b4fc64/lesson/59dd4ea9-d571-4db0-9bfb-12006d31d3a9)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/2ddcf79b-abb0-4aeb-ad0c-3d54c7b4fc64/lesson/9b081c0a-d604-427b-b603-a5716262199b)


# Vertical Pod Autoscaling VPA 2025 Updates

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Application-Lifecycle-Management/Vertical-Pod-Autoscaling-VPA-2025-Updates/page

This article explores optimizing Kubernetes workloads by using the Vertical Pod Autoscaler to automatically adjust resource allocations for applications.

In this article, we explore how to optimize Kubernetes workloads by scaling them vertically using the Vertical Pod Autoscaler (VPA). As a Kubernetes administrator, your goal is to ensure that applications always receive optimal resource allocations, such as CPU and memory. Let’s start by examining a typical deployment configuration for a pod that specifies a CPU request of 250 millicores and a limit of 500 millicores:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: nginx
          resources:
            requests:
              cpu: "250m"
            limits:
              cpu: "500m"
```

In this setup, the pod cannot use more than 500 millicores of CPU. To monitor its resource consumption, execute the following command (ensure that the metrics server is installed in your cluster):

```bash theme={null}
$ kubectl top pod my-app-pod
NAME        CPU(cores)   MEMORY(bytes)
my-app-pod  450m         350Mi
```

If the pod's CPU consumption reaches a predefined threshold, you might need to update its resource specifications manually. For example, you can increase the CPU request to "1" while keeping the limit unchanged:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nginx
        resources:
          requests:
            cpu: "1"
          limits:
            cpu: "500m"
```

To apply this change, run:

```bash theme={null}
$ kubectl edit deployment my-app
```

After saving, Kubernetes will terminate the current pod and create a new one with the updated resource configuration.

> **lightbulb** Manually updating pods can be time-consuming and error-prone. Kubernetes provides the Vertical Pod Autoscaler (VPA) to automate this process.

Kubernetes distinguishes between scaling methods. While the Horizontal Pod Autoscaler (HPA) adds or removes pods based on demand, the VPA continuously monitors metrics and automatically adjusts the CPU and memory allocation of each pod. Since VPA is not enabled by default, you must install it manually. Start by applying the VPA definition file from the autoscaler GitHub repository:

```bash theme={null}
$ kubectl apply -f https://github.com/kubernetes/autoscaler/releases/latest/download/vertical-pod-autoscaler.yaml
```

Verify that the VPA components are running in the kube-system namespace:

```bash theme={null}
$ kubectl get pods -n kube-system | grep vpa
vpa-admission-controller-xxxx   Running
vpa-recommender-xxxx            Running
vpa-updater-xxxx                Running
```

The VPA deployment includes three key components:

1. **VPA Recommender:** Continuously monitors resource usage via the Kubernetes metrics API, analyzes historical and live data, and provides optimized recommendations for CPU and memory.
2. **VPA Updater:** Compares current pod resource settings against recommendations and evicts pods running with suboptimal resources. This eviction triggers the creation of new pods with updated configurations.
3. **VPA Admission Controller:** Intercepts pod creation requests and mutates the pod specification based on the recommender's suggestions, ensuring that new pods start with the ideal resource configuration.

Next, create a VPA resource with a YAML definition. Unlike HPA, the VPA isn’t set up through imperative commands. The example below shows a configuration that monitors the "my-app" deployment, enforces minimum and maximum CPU limits, and uses the "Auto" update mode:

```yaml theme={null}
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
      - containerName: "my-app"
        minAllowed:
          cpu: "250m"
        maxAllowed:
          cpu: "2"
        controlledResources: ["cpu"]
```

In "Auto" mode, the VPA updater behaves similarly to a "recreate" strategy by terminating pods that run with non-optimal resources, allowing new pods to be created with the recommended values. In the future, when Kubernetes supports in-place updates, VPA will update pods’ resources without needing a full restart.

To inspect the resource recommendations provided by VPA for your deployment, run:

```bash theme={null}
$ kubectl describe vpa my-app-vpa
```

You might see an output similar to this, which indicates a recommended CPU value of 1.5:

```text theme={null}
Recommendations:
  Target:
    Cpu: 1.5
```

## Comparing Vertical and Horizontal Pod Autoscaling

Understanding when to use VPA versus HPA is crucial for efficient resource management:

| Feature           | Vertical Pod Autoscaling (VPA)                                                                    | Horizontal Pod Autoscaling (HPA)                                                 |
| ----------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Scaling Method    | Adjusts CPU and memory settings of individual pods (may restart pods for changes).                | Increases or decreases the number of pods to distribute load.                    |
| Pod Behavior      | May cause temporary downtime during pod restarts.                                                 | Scales pods seamlessly without interrupting existing ones.                       |
| Traffic Handling  | Less effective for sudden spikes due to restart delays.                                           | Ideal for handling rapid traffic spikes by adding more pods instantly.           |
| Cost Optimization | Prevents over-provisioning by matching resource allocation with actual usage.                     | Reduces operational costs by avoiding underutilized pods.                        |
| Use Cases         | Stateful workloads, databases, JVM-based applications, and AI workloads requiring precise tuning. | Stateless applications, web services, and microservices requiring rapid scaling. |

![The image is a comparison chart highlighting the key differences between Vertical Pod Autoscaling (VPA) and Horizontal Pod Autoscaling (HPA) in Kubernetes, focusing on features like scaling method, pod behavior, traffic handling, cost optimization, and use cases.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869688/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Vertical-Pod-Autoscaling-VPA-2025-Updates/vpa-hpa-comparison-chart-kubernetes.jpg)

> **lightbulb** VPA focuses on optimizing resource allocation for individual pods, while HPA scales the number of pods to meet demand. The choice depends on your application’s workload characteristics and scaling requirements.

In summary, the Vertical Pod Autoscaler (VPA) enhances Kubernetes resource management by dynamically adjusting CPU and memory allocations based on real-time metrics. By applying these VPA techniques, you can ensure that your applications run efficiently without manual intervention.

Now, try deploying VPA in your Kubernetes environment to experience improved resource optimization and operational efficiency.

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/2ddcf79b-abb0-4aeb-ad0c-3d54c7b4fc64/lesson/4a2a1d89-253e-4511-aa13-968566ec5f66)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/2ddcf79b-abb0-4aeb-ad0c-3d54c7b4fc64/lesson/b4aa0137-fe1f-4470-9b74-865b45266131)
