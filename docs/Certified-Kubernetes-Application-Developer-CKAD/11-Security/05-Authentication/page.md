# Authentication

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Security/Authentication/page

This article covers authentication mechanisms in Kubernetes clusters, focusing on securing access for users and service accounts through various methods.

Welcome to this comprehensive lesson on authentication within a Kubernetes cluster. In a typical Kubernetes environment, the cluster consists of multiple nodes—whether physical or virtual—and a range of components that work together seamlessly. The cluster is accessed by various users, including administrators managing cluster operations, developers deploying applications, end users interacting with those applications, and even third-party applications for integrations. In this lesson, we focus on securing the cluster by ensuring secure communication between internal components and by managing administrative access with robust authentication and authorization mechanisms.

<Frame>
  ![The image illustrates a network diagram showing interactions between admins, developers, end users, and bots, connected through a series of nodes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752871279/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Authentication/frame_30.jpg)
</Frame>

Our primary focus is on authentication mechanisms that secure access for users (such as administrators and developers) and service accounts (robots or processes with cluster access). Note that while end user authentication for applications is generally managed by the application itself, Kubernetes relies on external sources for handling human user accounts.

Kubernetes itself does not manage user accounts natively. Instead, it integrates with external sources like CSV files, certificate authorities, or third-party identity services (e.g., LDAP). Although service accounts can be created and managed via the Kubernetes API, user management for non-service accounts must be handled externally. Every request—whether it comes via the kubectl tool or the API—is first authenticated by the kube-apiserver.

There are several authentication mechanisms available in Kubernetes:

* Using a static password file (a CSV file containing usernames and passwords)
* Using a static token file for token-based authentication
* Using certificates for user authentication
* Integrating with third-party authentication protocols such as LDAP or Kerberos

Below is another visual representation that categorizes accounts into "User" (Admins, Developers) and "Service Accounts" (Bots).

<Frame>
  ![The image categorizes accounts into "User" (Admins, Developers) and "Service Accounts" (Bots) with corresponding icons.](../../../../images/kodekloud.com/kk-media/image/upload/v1752871281/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Authentication/frame_90.jpg)
</Frame>

All authentication methods funnel through the kube-apiserver which validates each request before further processing.

<Frame>
  ![The image outlines Kubernetes authentication mechanisms, including static password files, static token files, certificates, and identity services, related to the kube-apiserver.](../../../../images/kodekloud.com/kk-media/image/upload/v1752871282/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Authentication/frame_180.jpg)
</Frame>

## Static Password File Authentication

The simplest authentication method uses a CSV file that lists users along with their passwords, usernames, and user IDs. Optionally, a fourth column can indicate group memberships. This file is made available to the kube-apiserver using the `--basic-auth-file` flag. Consider this example CSV file that stores user details:

```csv theme={null}
password123,user1,u0001
password123,user2,u0002
password123,user3,u0003
password123,user4,u0004
password123,user5,u0005
```

To configure the kube-apiserver to use this file, update its service configuration. For clusters set up with tools like kubeadm, modify the kube-apiserver manifest (typically located at `/etc/kubernetes/manifests/kube-apiserver.yaml`) as shown below:

```bash theme={null}
kube-apiserver.service
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
    --basic-auth-file=user-details.csv
```

Below is an excerpt from a modified kube-apiserver pod manifest for a kubeadm-based cluster:

```yaml theme={null}
/etc/kubernetes/manifests/kube-apiserver.yaml
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - name: kube-apiserver
    image: k8s.gcr.io/kube-apiserver-amd64:v1.11.3
    command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
    - --advertise-address=172.17.0.107
    - --allow-privileged=true
    - --enable-admission-plugins=NodeRestriction
    - --enable-bootstrap-token-auth=true
```

After updating the manifest, the kube-apiserver will restart automatically (in a kubeadm environment) to apply the new authentication configuration.

## Static Token File Authentication

For token-based authentication, you can create a CSV file similar to the static password file, but with a token replacing the password. This file is provided to the kube-apiserver using the `--token-auth-file` flag. Here’s an example CSV file with tokens and group memberships:

```csv theme={null}
KpjCvB7rcFAHYPKByTIZRb7gulcUc4B,user10,u0010,group1
rJJncHmvtxHc6M1WQddhtvNyhgTdxSC,user11,u0011,group1
mjpOFTEiFOKL9toikaRNTt59ePtczZSq,user12,u0012,group2
PG411Xhs7QjqWKmBkvgGT9glOyUqZij,user13,u0013,group2
```

When starting the kube-apiserver, include the token file as follows:

```bash theme={null}
--token-auth-file=user-token-details.csv
```

To authenticate a request with a token, pass the token as an authorization bearer token. For example:

```bash theme={null}
curl -v -k https://master-node-ip:6443/api/v1/pods --header "Authorization: Bearer KpjCvB7rcFAHYPKByTIZRb7gulcUc4B"
```

## Important Considerations

<Callout icon="triangle-alert">
  Using static password or token files is not recommended for production environments since they store sensitive information (usernames, passwords, tokens) in clear text. Consider using more secure methods such as client certificates or integrative external identity providers.
</Callout>

If you are testing these authentication methods in a kubeadm cluster, ensure that you configure volume mounts appropriately to pass the authentication file into the kube-apiserver pod. Additionally, configure robust authorization mechanisms for the new users. We will explore authorization strategies later in this course.

This concludes our detailed examination of Kubernetes authentication mechanisms. For further details and best practices, consult the [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/9b6bf541-dfbb-465f-8cd3-2488d2fc044b" />
</CardGroup>
