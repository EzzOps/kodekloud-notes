# create a service account
kubectl create serviceaccount sa1

# list service accounts in the current namespace
kubectl get serviceaccounts
```

All incoming API requests (from kubectl, dashboard, controllers, or direct API calls) are received by kube-apiserver, which authenticates each request before applying authorization rules.

Below are the common authentication mechanisms you can configure on kube-apiserver.

<Frame>
  <img alt="A slide titled &#x22;Auth Mechanisms&#x22; showing a &#x22;kube-apiserver&#x22; box above three authentication options: Static Token File, Certificates, and Identity Services, each represented by a simple icon. The layout is on a dark background and appears to be a presentation graphic." />
</Frame>

Common authentication options

* Static basic-auth (password) files — legacy.
* Static token files — legacy.
* TLS client certificates — recommended for many production setups.
* External identity providers (OIDC, LDAP, Kerberos) — recommended for large or multi-tenant clusters.

Table: Authentication mechanisms at a glance

|                                Mechanism | Use case                                       | Example / Notes                                                                     |
| ---------------------------------------: | ---------------------------------------------- | ----------------------------------------------------------------------------------- |
|                   Static basic-auth file | Small experiments, local demos                 | CSV of username/password (plaintext); configured via --basic-auth-file (deprecated) |
|                        Static token file | Simple automation, throwaway clusters          | CSV mapping bearer tokens to users; configured via --token-auth-file (deprecated)   |
|                  TLS client certificates | Secure machine access, admin/user certificates | Use CA-signed client certs; verified by kube-apiserver                              |
| External identity providers (OIDC, LDAP) | Enterprise SSO, centralized user management    | Integrate kube-apiserver with OIDC/LDAP for federated auth                          |

Legacy mechanisms: static basic-auth and token files
We’ll briefly cover these two legacy mechanisms so you understand the underlying concepts. Both are simple CSV-based approaches and should not be used in production.

Static basic-auth file

* A basic-auth file is a CSV containing password, username, uid, and groups.
* kube-apiserver reads it when started with the --basic-auth-file flag.
* Credentials are stored in clear text — insecure and deprecated.

Example basic-auth CSV (legacy format):

```csv theme={null}
# password,username,uid,groups
KpjCVbI7rCFAHYPkByTIzRb7gu1cUc4B,user10,u0010,group1
rJjncHmvtXHc6MlWQddhtvNyvhgTdxSC,user11,u0011,group1
mjp0FIEiFOKL9toikaRNtt59ePtczZSq,user12,u0012,group2
PG41IXhs7QjqwWkmBkvgGT9g10yUqZij,user13,u0013,group2
```

Enable this mechanism on kube-apiserver (not recommended):

```bash theme={null}
--basic-auth-file=/path/to/basic-auth.csv
```

Authenticate with HTTP Basic (example using curl):

```bash theme={null}
curl -k -u user10:KpjCVbI7rCFAHYPkByTIzRb7gu1cUc4B https://master-node-ip:6443/api
```

Static token file

* A token file is a CSV mapping bearer tokens to user identities and groups.
* kube-apiserver reads it via the --token-auth-file flag.
* Like the basic file, it stores tokens in plaintext — insecure and deprecated.

Example token CSV (legacy format):

```csv theme={null}
# token,username,uid,groups
c29tZXRva2VuMTIz,user21,u0021,group1
aW5vdGhlcnRva2Vu,user22,u0022,group2
```

Enable on kube-apiserver (not recommended):

```bash theme={null}
--token-auth-file=/path/to/token-auth.csv
```

Authenticate with a bearer token (curl example):

```bash theme={null}
curl -k -H "Authorization: Bearer c29tZXRva2VuMTIz" https://master-node-ip:6443/api
```

Important operational notes

* kubeadm-managed clusters: kube-apiserver runs as a static pod. To add flags such as --basic-auth-file or --token-auth-file you must edit the kube-apiserver manifest (commonly /etc/kubernetes/manifests/kube-apiserver.yaml) and add hostPath/volume mounts so the files are accessible to the pod. The kubelet will detect the manifest change and restart kube-apiserver automatically.
* When you modify kube-apiserver flags or change its static pod manifest, the kube-apiserver process will restart under kubeadm-managed setups; plan for a short control-plane interruption.
* Always combine authentication with proper authorization (RBAC) to control what an authenticated identity can do.

<Callout icon="lightbulb">
  Static basic-auth and token files store credentials in clear text and are considered legacy and unsafe. They are deprecated in modern Kubernetes releases. Prefer certificate-based authentication or external identity providers (OIDC, LDAP, etc.), and always enforce RBAC for authorization.
</Callout>

<Frame>
  <img alt="A dark-blue slide titled &#x22;Notes&#x22; with three rounded boxes listing Kubernetes-related advice: &#x22;This is not a recommended authentication mechanism&#x22;, &#x22;Consider volume mount while providing the auth file in a kubeadm setup&#x22;, and &#x22;Set up Role-Based Authorization for new users.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the lower-left corner." />
</Frame>

Summary and recommendations

* kube-apiserver is the central authentication gateway for Kubernetes; every request to the API is authenticated by it.
* Kubernetes does not create or manage regular user accounts itself — integrate with external identity providers or use client certificates. Service accounts are native Kubernetes objects for in-cluster processes.
* Static basic-auth and token files are easy to understand but insecure and deprecated. Use them only for quick tests or isolated labs.
* For production, prefer TLS client certificates or integrate kube-apiserver with a robust external identity provider (OIDC, LDAP). Always pair authentication with RBAC authorization.

Further reading and references

* [Kubernetes Authentication Overview](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)
* [kube-apiserver command line reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)
* [Using OpenID Connect (OIDC) with Kubernetes](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#openid-connect-tokens)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/77826599-d456-4cb5-8cbc-b713cc077b45/lesson/011ca8e1-16dc-443b-9501-a2b68d92501e" />
</CardGroup>


# Authorization

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Security/Authorization/page

This article explores authentication and authorization in Kubernetes, detailing user access, permissions, and various authorization mechanisms like RBAC and external tools.

In this lesson, we explore how authentication allows individuals or machines to gain access to a cluster and how authorization subsequently defines what actions they can perform within that cluster. Once a user gains access, authorization ensures they only have the appropriate permissions for their role. For example, a cluster administrator can view various objects such as Pods, Nodes, and Deployments:

```bash theme={null}
kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          53s

kubectl get nodes
NAME        STATUS   ROLES     AGE     VERSION
worker-1    Ready    <none>    5d21h   v1.13.0
worker-2    Ready    <none>    5d21h   v1.13.0

kubec
```

Administrators have full control, allowing them to create or delete objects like Pods or Nodes. As the cluster scales and more users—including administrators, developers, testers, or external applications like monitoring tools and [Jenkins](https://learn.kodekloud.com/user/courses/jenkins)—access the system, it is critical to provide only the access level necessary for each user’s role. For instance, developers might be limited to deploying applications without the ability to modify the overall cluster configuration.

Below is an example demonstrating operations executed with limited permissions:

```plaintext theme={null}
kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          53s

kubectl get nodes
NAME       STATUS   ROLES     AGE     VERSION
worker-1   Ready    <none>    5d21h   v1.13.0
worker-2   Ready    <none>    5d21h   v1.13.0

kubectl delete node worker-2
Node worker-2 Deleted!
```

In contrast, attempting similar operations without sufficient privileges results in the following responses:

```bash theme={null}
kubectl get pods
Error from server (Forbidden): pods is forbidden: User "Bot-1" cannot list "pods"

kubectl get nodes
Error from server (Forbidden): nodes is forbidden: User "Bot-1" cannot get "nodes"

kubectl delete node worker-2
Error from server (Forbidden): nodes "worker-2" is forbidden: User "developer" cannot delete resource "nodes"
```

When sharing a cluster across different organizations or teams using namespaces, authorization restricts users to their designated namespaces. Kubernetes supports multiple authorization mechanisms, including:

* Node Authorization
* Attribute-Based Authorization
* Role-Based Access Control (RBAC)
* Webhook Authorization

The Kubernetes API Server is the central component accessed by both management users and internal components, such as kubelets, which retrieve and report metadata about services, endpoints, nodes, and pods. The communication between a kubelet and the API server is illustrated in the diagram below:

<Frame>
  ![The image illustrates a Kubernetes node interaction, showing communication between a user, Kube API, and kubelet, with read/write operations on services, endpoints, nodes, and pods.](https://kodekloud.com/kk-media/image/upload/v1752869926/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Authorization/frame_150.jpg)
</Frame>

Requests from kubelets—typically using certificates with names prefixed by "system:node" as part of the system:nodes group—are authorized by a special component known as the node authorizer. The following diagram explains the authorization process for kubelet requests:

<Frame>
  ![The image illustrates the Node Authorizer process in Kubernetes, showing interactions between a user, Kube API, kubelet, and a certificate, with read/write permissions listed.](https://kodekloud.com/kk-media/image/upload/v1752869928/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Authorization/frame_180.jpg)
</Frame>

<Callout icon="lightbulb">
  Kubernetes supports several authorization strategies to meet diverse security requirements. Always select the most appropriate mechanism for your cluster’s needs.
</Callout>

## Attribute-Based Authorization

Attribute-based authorization associates specific users or groups with a defined set of permissions. For example, you can grant a user called "dev-user" permissions to view, create, and delete pods. This is achieved by creating a policy file in JSON format and passing it to the API server. Consider the following example policy file:

```json theme={null}
{"kind": "Policy", "spec": {"user": "dev-user", "namespace": "*", "resource": "pods", "apiGroup": "*"}}
{"kind": "Policy", "spec": {"user": "dev-user-2", "namespace": "*", "resource": "pods", "apiGroup": "*"}}
{"kind": "Policy", "spec": {"group": "dev-users", "namespace": "*", "resource": "pods", "apiGroup": "*"}}
{"kind": "Policy", "spec": {"user": "security-1", "namespace": "*", "resource": "csr", "apiGroup": "*"}}
```

Each time security requirements change, you must manually update this policy file and restart the Kube API Server. This manual process can be tedious and set the stage for more streamlined methods such as Role-Based Access Control (RBAC).

## Role-Based Access Control (RBAC)

RBAC simplifies user permission management by defining roles instead of directly associating permissions with individual users. For example, you can create a "developer" role that encompasses only the necessary permissions for application deployment. Developers are then associated with this role, and modifications in user access can be handled by updating the role, affecting all associated users immediately.

RBAC is considered the standard method for managing access within a Kubernetes cluster. The diagram below provides a visual representation of RBAC across different roles:

<Frame>
  ![The image illustrates RBAC roles, showing user permissions for developers and security, including actions like viewing, creating, and deleting PODs, and approving CSRs.](https://kodekloud.com/kk-media/image/upload/v1752869929/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Authorization/frame_290.jpg)
</Frame>

Further details on RBAC will be discussed in upcoming lessons.

## External Authorization Mechanisms

If you prefer managing authorization externally rather than with built-in Kubernetes mechanisms, third-party tools like [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) are an excellent choice. OPA can handle both admission control and authorization by processing user details and access requirements sent via API calls from Kubernetes. Based on OPA’s response, access is either granted or denied.

## AlwaysAllow and AlwaysDeny Modes

Kubernetes also supports two basic authorization modes:

* **AlwaysAllow:** Permits all requests without performing any authorization checks.
* **AlwaysDeny:** Denies all requests.

These modes are configured using the authorization-mode option on the Kube API Server and are crucial when determining which authorization mechanism is active. In cases where no mode is specified, AlwaysAllow is used by default.

Below is an example configuration using AlwaysAllow:

```bash theme={null}
ExecStart=/usr/local/bin/kube-apiserver \\
  --advertise-address=${INTERNAL_IP} \\
  --allow-privileged=true \\
  --apiserver-count=3 \\
  --authorization-mode=AlwaysAllow \\
  --bind-address=0.0.0.0 \\
  --enable-swagger-ui=true \\
  --etcd-cafile=/var/lib/kubernetes/ca.pem \\
  --etcd-certfile=/var/lib/kubernetes/apiserver-etcd-client.crt \\
  --etcd-keyfile=/var/lib/kubernetes/apiserver-etcd-client.key \\
  --etcd-servers=https://127.0.0.1:2379 \\
  --event-ttl=1h \\
  --kubelet-certificate-authority=/var/lib/kubernetes/ca.pem \\
  --kubelet-client-[SECRET_REDACTED]-etcd-client.crt \\
  --kubelet-client-key=/var/lib/kubernetes/apiserver-etcd-client.key \\
  --service-node-port-range=30000-32767 \\
  --client-ca-file=/var/lib/kubernetes/ca.pem \\
  --tls-cert-file=/var/lib/kubernetes/apiserver.crt \\
  --tls-private-key-file=/var/lib/kubernetes/apiserver.key \\
  -v=2
```

You can also specify a comma-separated list of multiple authorization modes. For example, to configure node authorization, RBAC, and webhook authorization, set the parameter as follows:

```bash theme={null}
ExecStart=/usr/local/bin/kube-apiserver \\
  --advertise-address=${INTERNAL_IP} \\
  --allow-privileged=true \\
  --apiserver-count=3 \\
  --authorization-mode=Node,RBAC,Webhook \\
  --bind-address=0.0.0.0 \\
  --enable-swagger-ui=true \\
  --etcd-cafile=/var/lib/kubernetes/ca.pem \\
  --etcd-certfile=/var/lib/kubernetes/apiserver-etcd-client.crt \\
  --etcd-keyfile=/var/lib/kubernetes/apiserver-etcd-client.key \\
  --etcd-servers=https://127.0.0.1:2379 \\
  --event-ttl=1h \\
  --kubelet-certificate-authority=/var/lib/kubernetes/ca.crt \\
  --tls-cert-file=/var/lib/kubernetes/apiserver.crt \\
  --tls-private-key-file=/var/lib/kubernetes/apiserver.key \\
  --v=2
```

When multiple modes are configured, each request is processed sequentially in the order specified. For example, a user’s request is first evaluated by the node authorizer. If the request does not pertain to node-specific actions and is consequently denied, it is then passed to the next module, such as RBAC. Once a module approves the request, further checks are bypassed and the user is granted access.

<Callout icon="lightbulb">
  This lesson provided an in-depth look at authorization in Kubernetes—from basic attribute-based policies to advanced RBAC and external mechanisms. Choosing the right authorization methods is essential for securing your cluster while ensuring users have only the permissions they need.
</Callout>

That concludes this lesson on authorization. Stay tuned for further exploration of role-based access controls and other advanced authorization mechanisms.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/77826599-d456-4cb5-8cbc-b713cc077b45/lesson/07ad19e2-0f1d-477b-8a15-ade674a14761" />
</CardGroup>
