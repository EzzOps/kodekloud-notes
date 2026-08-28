# Output: bXlzcWw=
echo -n 'root' | base64
# Output: cm9vdA==
echo -n 'paswrd' | base64
# Output: cGFzd3Jk
```

## Viewing and Decoding Secrets

To list all Secrets in your cluster, run:

```bash theme={null}
kubectl get secrets
```

Example output:

```plaintext theme={null}
NAME          TYPE     DATA   AGE
app-secret    Opaque   3      10m
```

For detailed information about a specific Secret, use:

```bash theme={null}
kubectl describe secrets
```

This command displays the Secret's attributes without revealing the actual sensitive data. To inspect the encoded values, execute:

```bash theme={null}
kubectl get secret app-secret -o yaml
```

To decode an encoded value, for example:

```bash theme={null}
echo -n 'bXlzcWw=' | base64 --decode
echo -n 'cm9vdA==' | base64 --decode
# Output: root
```

## Injecting Secrets into Pods

Once you have created your Secret, you can inject its data into a Pod. There are two common methods for this: as environment variables or by mounting them as files in a volume.

### As Environment Variables

Below is an example of a pod definition that imports the Secret as environment variables:

```yaml theme={null}
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

And here is the corresponding Secret definition with properly encoded data:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  DB_Host: bXlzcWw=
  DB_User: cm9vdA==
  DB_Password: cGFzd3Jk
```

When the pod is created, the Secret's data will be available to the container as environment variables.

### As Mounted Volumes

Another approach involves mounting Secrets as files within a Pod. When mounted, each key in the Secret becomes a file, and its content is the corresponding decoded value. For example:

```yaml theme={null}
volumes:
  - name: app-secret-volume
    secret:
      secretName: app-secret
```

Listing the mounted volume may reveal files like:

```bash theme={null}
ls /opt/app-secret-volumes
# Output: DB_Host  DB_Password  DB_User
```

And to view the database password:

```bash theme={null}
cat /opt/app-secret-volumes/DB_Password
# Output: paswrd
```

## Important Considerations When Working with Secrets

1. Secrets are encoded in base64, not encrypted. Anyone with access to the Secret object can decode the sensitive data.
2. Avoid version controlling your secret definition files to prevent accidental exposure.
3. By default, Secrets stored in etcd are not encrypted. Consider enabling encryption at rest in your Kubernetes cluster.

<Callout icon="triangle-alert">
  Ensure that secrets in etcd are properly encrypted and that access is restricted using Role-Based Access Control (RBAC). Do not expose your secret files in public repositories.
</Callout>

For example, here is an encryption configuration file that secures Secrets along with other resources:

```yaml theme={null}
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - identity: {}
      - aesgcm:
          keys:
            - name: key1
              secret: C2VjcmVjT0glZzIHNLY3VyZQ==
            - name: key2
              secret: dGhpcpyBcyBwYXNzd29yZA==
      - aescbc:
          keys:
            - name: key1
              secret: C2VjcmVjT0glZzIHNLY3VyZQ==
            - name: key2
              secret: dGhpcpyBcyBwYXNzd29yZA==
      - secretbox:
          keys:
            - name: key1
              secret: [SECRET_REDACTED]=
```

You must pass this file to the Kubernetes API server. Here is an example of modifying the kube-apiserver pod configuration to make use of the encryption configuration:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubeddm.kubernetes.io/kube-apiserver.advertise-address.endpoint: 10.10.30.4:6443
  creationTimestamp: null
  labels:
    component: kube-apiserver
    tier: control-plane
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
    - command:
        - kube-apiserver
        # ...
        - --encryption-provider-config=/etc/kubernetes/enc/enc.yaml # <--- add this line
  volumeMounts:
    # ...
    - name: enc
      mountPath: /etc/kubernetes/enc
      readOnly: true # <--- add this line
  volumes:
    # ...
    - name: enc
      hostPath:
        path: /etc/kubernetes/enc
        type: DirectoryOrCreate # <--- add this line
```

This setup ensures that Secrets stored in etcd are encrypted. Note that only users with the correct permissions can create pods or deployments that have access to these Secrets. It is important to enforce proper RBAC policies.

Additionally, consider leveraging third-party secret management providers such as AWS, Azure, GCP, or HashiCorp Vault. These external providers help in storing secrets securely outside of etcd and enforce robust security measures.

<Frame>
  ![The image provides guidelines on handling secrets, emphasizing encryption, access control, and considering third-party providers for secure storage.](https://kodekloud.com/kk-media/image/upload/v1752871147/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Secrets/frame_470.jpg)
</Frame>

For further details on advanced secret management and external providers, check out the [Certified Kubernetes Security Specialist (CKS)](https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks) course.

That concludes our guide on Kubernetes Secrets. Now, head over to the labs and practice managing Secrets to enhance your security skills in a Kubernetes environment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/aee75c02-d33f-4f31-a601-c5c2045b61a4" />
</CardGroup>


# Security Contexts

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Configuration/Security-Contexts/page

This lesson covers how Kubernetes manages security contexts, allowing configuration of user IDs and Linux capabilities for containers within Pods.

Hello and welcome to this lesson on security contexts in Kubernetes.

My name is Mumshad Mannambeth, and in this guide, I'll walk you through how Kubernetes manages security contexts. Previously, we explored Docker container security, where you can define user IDs and modify Linux capabilities for your containers. Kubernetes extends this capability, allowing you to configure similar security settings.

## Docker vs. Kubernetes Security Context

In Docker, you may run containers with security options like these:

```bash theme={null}
docker run --user=1001 ubuntu sleep 3600
docker run --cap-add MAC_ADMIN ubuntu
```

In Kubernetes, containers run within Pods. You have the flexibility to set security contexts either at the container level or at the Pod level. Settings defined at the Pod level affect all containers in that Pod. However, if the same security context options are specified for both the Pod and individual containers, the container-level settings override those at the Pod level.

<Callout icon="lightbulb">
  Security settings specified at the container level have a higher precedence than those set at the Pod level. Always verify your configuration to ensure the intended security policies are applied.
</Callout>

## Example Pod Definition

Consider the following example of a Pod definition file. In this configuration, an Ubuntu container is started with the `sleep` command. The security context is defined within the container specification using the `securityContext` field. Here, the `runAsUser` parameter sets the user ID for the container, and the `capabilities` option adds specific Linux capabilities:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
      securityContext:
        runAsUser: 1000
        capabilities:
          add: ["MAC_ADMIN"]
```

This example illustrates how to configure user permissions and capabilities in Kubernetes. Take some time to practice viewing, configuring, and troubleshooting security context issues using this configuration.

<Callout icon="lightbulb">
  After you experiment with this configuration, explore how to integrate more advanced security policies across multiple Pods and clusters. Delving deeper into Kubernetes security will strengthen your operational best practices.
</Callout>

That's it for now—I look forward to seeing you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/04ba9675-066e-4ea2-bd32-fc95f1f91a21" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/3aaded14-eaf2-4e11-b76b-9e5601f3dbf6" />
</CardGroup>
