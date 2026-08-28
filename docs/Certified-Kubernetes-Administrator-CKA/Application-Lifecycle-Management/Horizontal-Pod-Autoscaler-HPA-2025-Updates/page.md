# Create a secret from all files within a directory:
kubectl create secret generic my-secret --from-file=path/to/bar

# Create a secret using specified keys from files:
kubectl create secret generic my-secret --from-file=ssh-privatekey=path/to/id_rsa --from-file=ssh-publickey=path/to/id_rsa.pub

# Create a secret from literal key-value pairs:
kubectl create secret generic my-secret --from-literal=key1=supersecret --from-literal=key2=topsecret

# Create a secret combining a file and a literal:
kubectl create secret generic my-secret --from-file=ssh-privatekey=path/to/id_rsa --from-literal=passphrase=topsecret

# Create a secret from environment files:
kubectl create secret generic my-secret --from-env-file=path/to/foo.env --from-env-file=path/to/bar.env
```

Additional options like `--allow-missing-template-keys`, `--append-hash`, and `--dry-run` can further refine your secret creation process.

After the command executes, verify the secret:

```bash theme={null}
kubectl create secret generic my-secret --from-literal=key1=supersecret
kubectl get secret my-secret
```

Using the `describe` command provides detailed metadata, including the base64-encoded data:

```bash theme={null}
kubectl describe secret my-secret
```

<Callout icon="lightbulb">
  Secret values are base64-encoded by default; they are not encrypted. Avoid pushing secret configuration files containing base64 values to public repositories.
</Callout>

***

## Viewing the Encoded Secret

Kubernetes stores secret values in base64‑encoded format. Retrieve the secret as YAML to inspect its contents:

```bash theme={null}
kubectl get secret my-secret -o yaml
```

The output might look like:

```yaml theme={null}
apiVersion: v1
data:
  key1: c3VwZXJzWmNyZVQ=
kind: Secret
metadata:
  creationTimestamp: "2022-10-24T05:34:13Z"
  name: my-secret
  namespace: default
  resourceVersion: "2111"
  uid: dfe97c62-5aa1-46a8-b71c-ffa0cd4c08ec
type: Opaque
```

To decode the secret value:

```bash theme={null}
echo "c3VwZXJzWmNyZVQ=" | base64 --decode
```

This reveals that the stored secret is only encoded, not encrypted, making it potentially accessible to anyone with access to the YAML output or an etcd dump.

***

## Inspecting Secret Data in etcd

etcd is the key-value store where Kubernetes persists cluster data. Without encryption at rest, secret values remain only base64-encoded, allowing anyone with access to etcd to decode them. Use the `etcdctl` client (API version 3) to query etcd:

```bash theme={null}
ETCDCTL_API=3 etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret | hexdump -C
```

Before running the above command, ensure that the `etcdctl` client is installed. On Ubuntu, install it using:

```bash theme={null}
apt-get install etcd-client
```

Verify the installation:

```bash theme={null}
etcdctl
```

Also, check that your control plane node can access the necessary certificate files:

```bash theme={null}
ls /etc/kubernetes/pki/etcd/ca.crt
```

The hexdump output will display the raw data, illustrating that without encryption, the secret’s value is visible within etcd.

***

## Enabling Encryption at Rest

To protect sensitive data stored in etcd, Kubernetes offers an encryption at rest mechanism using an encryption provider configuration. First, verify if encryption is enabled by checking the kube-apiserver process:

```bash theme={null}
ps -aux | grep kube-api | grep "encryption-provider-config"
```

If no configuration is found, follow these steps:

### 1. Create an Encryption Configuration File

Generate a random 32-byte key (base64-encoded) with:

```bash theme={null}
head -c 32 /dev/urandom | base64
```

Next, create a YAML file (e.g., `enc.yaml`) with the following content (replace the sample key with your generated key):

```yaml theme={null}
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
  providers:
    - aescbc:
        keys:
          - name: key1
            secret: [SECRET_REDACTED]=  # Replace with your generated key
    - identity: {}
```

Review the file to ensure accuracy:

```bash theme={null}
cat enc.yaml
```

### 2. Mount the Encryption Configuration File into the API Server

Next, incorporate the configuration into the kube-apiserver by performing these steps:

1. Move the encryption configuration file to a secure directory:

   ```bash theme={null}
   mkdir -p /etc/kubernetes/enc
   mv enc.yaml /etc/kubernetes/enc/
   ```

2. Modify the kube-apiserver manifest (found at `/etc/kubernetes/manifests/kube-apiserver.yaml`) by adding the `--encryption-provider-config` flag. Include a new volume and volume mount for the `/etc/kubernetes/enc` directory. For example:

   ```yaml theme={null}
   spec:
     containers:
     - command:
       - kube-apiserver
       # ... other flags ...
       - --encryption-provider-config=/etc/kubernetes/enc/enc.yaml
       volumeMounts:
         # ... other volume mounts ...
         - name: enc
           mountPath: /etc/kubernetes/enc
           readOnly: true
     volumes:
       # ... other volumes ...
       - name: enc
         hostPath:
           path: /etc/kubernetes/enc
           type: DirectoryOrCreate
   ```

After saving the changes, the kube-apiserver will restart and begin using the new encryption configuration.

***

## Verifying Encryption

Once encryption is activated, any new secret you create will be encrypted at rest. Create a new secret:

```bash theme={null}
kubectl create secret generic my-secret-2 --from-literal=key2=topsecret
```

Verify the secret's creation:

```bash theme={null}
kubectl get secret
```

Then inspect etcd to ensure the secret’s value is encrypted:

```bash theme={null}
ETCDCTL_API=3 etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret-2 | hexdump -C
```

You should observe that the secret’s data no longer appears in plain text. Remember, secrets created before enabling encryption remain unencrypted until updated. To re-encrypt existing secrets, use:

```bash theme={null}
kubectl get secret --all-namespaces -o json | kubectl replace -f -
```

Then confirm that the secrets in etcd are now encrypted.

<Callout icon="lightbulb">
  Always update your existing secrets after enabling encryption at rest to ensure full protection of sensitive data.
</Callout>

***

## Conclusion

This guide demonstrated how Kubernetes handles secret data by showing that, by default, secrets are only base64-encoded—not encrypted—in etcd. We then detailed the process for enabling encryption at rest: creating an encryption configuration file, mounting it into the API server, and verifying that new secrets store their data securely. By following these steps, you can significantly enhance the security posture of your Kubernetes cluster.

Happy encrypting!

***

## Additional Resources

| Resource              | Description                                 | Example Command / Link                                                                                   |
| --------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Kubernetes Secrets    | Official documentation on secrets           | [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)                          |
| etcd Documentation    | Information on etcd and its usage           | [etcd Documentation](https://etcd.io/docs/)                                                              |
| Kubernetes API Server | Details on configuring kube-apiserver flags | [Kube-apiserver Docs](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/) |

For further reading on securing your Kubernetes environment, consider consulting the [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/2ddcf79b-abb0-4aeb-ad0c-3d54c7b4fc64/lesson/4abaab5a-b18a-45a4-b969-2f2251a54375" />
</CardGroup>


# Horizontal Pod Autoscaler HPA 2025 Updates

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Application-Lifecycle-Management/Horizontal-Pod-Autoscaler-HPA-2025-Updates/page

This article explores the Horizontal Pod Autoscaler in Kubernetes and how it automates workload scaling, improving efficiency over manual scaling methods.

In this article, we explore the Horizontal Pod Autoscaler (HPA) feature in Kubernetes and explain how it automates the scaling of workloads. We'll begin by examining the manual approach to scaling an application and then show how HPA streamlines this process.

## Manual Horizontal Scaling

As a Kubernetes administrator, you might manually scale your application to ensure it has enough resources during traffic spikes. Consider the following deployment configuration:

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

In this configuration, each pod requests 250 millicores (mCPU) and is limited to 500 mCPU. To monitor the resource usage of a pod, you might run:

```bash theme={null}
$ kubectl top pod my-app-pod
```

The output would be similar to:

```bash theme={null}
NAME         CPU(cores)   MEMORY(bytes)
my-app-pod   450m         350Mi
```

Once you observe the pod’s CPU usage nearing the threshold (for example, at 450 mCPU), you would manually execute a scale command to add more pods:

```bash theme={null}
$ kubectl scale deployment my-app --replicas=3
```

<Callout icon="lightbulb">
  Manual scaling requires continuous monitoring and timely intervention, which may not be ideal during unexpected surges in traffic.
</Callout>

## Introducing the Horizontal Pod Autoscaler (HPA)

To address the shortcomings of manual scaling, Kubernetes offers the Horizontal Pod Autoscaler (HPA). HPA continuously monitors pod metrics—such as CPU, memory, or custom metrics—using the metrics-server. Based on these metrics, HPA automatically adjusts the number of pod replicas in a deployment, stateful set, or replica set. When resource usage exceeds a preset threshold, HPA increases the pod count; when usage declines, it scales down to conserve resources.

<Frame>
  ![The image is a diagram explaining the functions of a Horizontal Pod Autoscaler (HPA), highlighting its roles in observing metrics, adding pods, balancing thresholds, and tracking multiple metrics.](https://kodekloud.com/kk-media/image/upload/v1752869662/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Horizontal-Pod-Autoscaler-HPA-2025-Updates/horizontal-pod-autoscaler-diagram.jpg)
</Frame>

For example, with the nginx deployment above, you can create an HPA by running the command below. This command configures the "my-app" deployment to maintain 50% CPU utilization, scaling the number of pods between 1 and 10:

```bash theme={null}
$ kubectl autoscale deployment my-app --cpu-percent=50 --min=1 --max=10
```

Kubernetes will then create an HPA that monitors the CPU metrics (using the pod's 500 mCPU limit) via the metrics-server. If the average CPU utilization exceeds 50%, HPA adjusts the replica count to meet demand without manual input.

To review the status of your HPA, use:

```bash theme={null}
$ kubectl get hpa
```

This command shows the current CPU usage, threshold set, and the number of replicas—ensuring that pod counts remain within the defined limits. When the HPA is no longer needed, you can remove it with:

```bash theme={null}
$ kubectl delete hpa my-app
```

## Declarative Configuration for HPA

Beyond the imperative approach, you can declare the HPA configuration with a YAML file. Here's an example using the `autoscaling/v2` API:

```yaml theme={null}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

This configuration ensures that the HPA monitors the CPU utilization of the "my-app" deployment, automatically adjusting the replica count as needed. Note that HPA, integrated into Kubernetes since version 1.23, relies on the metrics-server to obtain resource utilization data.

## Metrics Sources and External Adapters

Kubernetes supports not only the internal metrics-server for collecting CPU or memory metrics but also custom metrics adapters. These adapters can retrieve metrics from other internal sources or external metrics providers like Datadog or Dynatrace through an external adapter. For further details on advanced configurations, please explore our [Kubernetes Autoscaling](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling) course.

<Frame>
  ![The image is a flowchart illustrating a metrics system architecture, showing the interaction between components like the Metrics Server, Custom Metrics Adapter, and External Adapter, with connections to Datadog and Dynatrace. It includes elements such as HPA (Horizontal Pod Autoscaler) and Workload (Deployment).](https://kodekloud.com/kk-media/image/upload/v1752869663/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Horizontal-Pod-Autoscaler-HPA-2025-Updates/metrics-system-architecture-flowchart.jpg)
</Frame>

## Conclusion

This article provided a comprehensive overview of the Horizontal Pod Autoscaler (HPA) in Kubernetes. We discussed the drawbacks of manual scaling and demonstrated how HPA automates scaling based on real-time resource usage. Whether through imperative commands or declarative YAML configurations, HPA ensures that your applications can adapt dynamically to fluctuating workloads.

For additional insights and hands-on experience, consider enrolling in our [Kubernetes Autoscaling](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling) course.

Happy scaling!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/2ddcf79b-abb0-4aeb-ad0c-3d54c7b4fc64/lesson/9fc22af6-82b3-4cda-9a57-dd94e24ecb1d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/2ddcf79b-abb0-4aeb-ad0c-3d54c7b4fc64/lesson/a84abc2e-7511-4685-8dcc-73e3f80045bf" />
</CardGroup>
