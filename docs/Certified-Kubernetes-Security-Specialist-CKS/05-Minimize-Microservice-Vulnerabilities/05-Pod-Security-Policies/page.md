# Pod Security Policies

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Minimize-Microservice-Vulnerabilities/Pod-Security-Policies/page

This article explores pod security in Kubernetes, focusing on Pod Security Policies and their role in restricting insecure configurations.

In this lesson, we explore pod security in Kubernetes by examining a sample pod definition and discussing how Pod Security Policies (PSPs) were used to restrict insecure configurations. Although PSPs have been deprecated in favor of Pod Security Admission and Pod Security Standards (available since Kubernetes 1.25), understanding PSPs is still useful—especially when working with legacy clusters.

***

## Sample Pod Definition

Below is a sample pod definition that creates a pod running an Ubuntu container. The configuration includes permissive settings often unsuitable for production environments:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: sample-pod
spec:
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
      securityContext:
        privileged: True
        runAsUser: 0
        capabilities:
          add: ["CAP_SYS_BOOT"]
  volumes:
    - name: data-volume
      hostPath:
        path: /data
        type: Directory
```

In this pod:

* The `privileged` flag is set to `True`, granting container processes elevated privileges.
* The container runs as root (`runAsUser: 0`).
* It adds specific capabilities like `CAP_SYS_BOOT`.
* A HostPath volume is used, exposing part of the host’s filesystem.

These settings can introduce security vulnerabilities. To safeguard your cluster, it is important to enforce policies that restrict such configurations.

***

## The Role of Pod Security Policies

Pod Security Policies were designed to validate pod creation requests against a set of pre-configured security rules. When the PSP admission controller is enabled, it intercepts pod creation requests and rejects those that do not comply with the defined policies. For example, a pod configured with the `privileged` flag set to `True` can be denied by an appropriately configured PSP.

> **lightbulb** When a violation is detected, the system rejects the pod creation request and returns an error message, preventing insecure pods from running.

***

## Enabling PSP on the API Server

PSP functions as an Admission Controller. To enable it, add the `PodSecurityPolicy` plugin to the API server’s list of admission plugins. An example snippet from the API server’s startup command is shown below:

```text theme={null}
ExecStart=/usr/local/bin/kube-apiserver \
  --advertise-address=${INTERNAL_IP} \
  --allow-privileged=true \
  --apiserver-count=3 \
  --authorization-mode=Node,RBAC \
  --bind-address=0.0.0.0 \
  --enable-swagger-ui=true \
  --etcd-servers=https://127.0.0.1:2379 \
  --event-ttl=1h \
  --runtime-config=api/all \
  --service-cluster-ip-range=10.32.0.0/24 \
  --service-node-port-range=30000-32767 \
  --v=2 \
  --enable-admission-plugins=PodSecurityPolicy
```

Similarly, here’s an excerpt from the API server pod definition that confirms the admission plugin is enabled:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
    - command:
        - kube-apiserver
        - --authorization-mode=Node,RBAC
        - --advertise-address=172.17.0.107
        - --allow-privileged=true
        - --enable-bootstrap-token-auth=true
        - --enable-admission-plugins=PodSecurityPolicy
      image: k8s.gcr.io/kube-apiserver-amd64:v1.11.3
      name: kube-apiserver
```

Once the admission controller is activated, every pod creation request is validated against the PSP rules.

***

## Defining a Pod Security Policy

To enforce security, you can create a PSP that, for instance, disallows pods with the privileged flag enabled. Start by reviewing the original pod definition for context:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: sample-pod
spec:
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
      securityContext:
        privileged: True
        runAsUser: 0
        capabilities:
          add: ["CAP_SYS_BOOT"]
  volumes:
    - name: data-volume
      hostPath:
        path: /data
        type: Directory
```

Now, define a Pod Security Policy that disallows privileged containers:

```yaml theme={null}
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: example-psp
spec:
  privileged: false
```

This basic PSP will reject any pod creation request that tries to run a container with the `privileged` flag.

You can further customize the policy to enforce stricter measures. For instance, the following definition disallows running as root, mandates dropping the `CAP_SYS_BOOT` capability, adds a default capability, and only permits specific volume types:

```yaml theme={null}
