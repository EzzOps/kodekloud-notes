# deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      type: front-end
  template:
    metadata:
      name: myapp-pod
      labels:
        type: front-end
    spec:
      containers:
      - image: nginx
```

Using the file above, you can create, query, and delete the deployment with the following commands:

```bash theme={null}
kubectl create -f deployment.yml
# Output:
kubectl get deployments
# Output:
# NAME              DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kubectl delete -f deployment.yml
# Output:
# deployment "myapp-deployment" deleted
```

The deployment controller automatically creates a ReplicaSet, which manages the specified number of pods. This automation lies at the heart of Kubernetes resource management.

***

## Custom Resource: FlightTicket

Imagine you want to manage something entirely new on your cluster—such as booking a flight ticket. In this example, we define a custom resource called FlightTicket that represents a flight ticket booking. The resource encapsulates details such as the departure and destination airports and the number of tickets required.

Below is an example of a FlightTicket resource file:

```yaml theme={null}
# flightticket.yml
apiVersion: flights.com/v1
kind: FlightTicket
metadata:
  name: my-flight-ticket
spec:
  from: Mumbai
  to: London
  number: 2
```

When you create this custom resource, you expect that:

* It is stored in etcd.
* A custom controller (which you will build) watches for create, update, or delete events.
* The controller automatically makes the necessary API calls (for example, to an external flight booking API) to either book or cancel the ticket.

<Callout icon="triangle-alert">
  Attempting to create the FlightTicket resource without first informing Kubernetes of its existence will result in an error:

  ```bash theme={null}
  kubectl create -f flightticket.yml
  # Output:
  # no matches for kind "FlightTicket" in version "flights.com/v1"
  ```

  This error means that Kubernetes does not yet recognize the FlightTicket type.
</Callout>

***

## Defining a Custom Resource Definition (CRD)

To allow the Kubernetes API to accept FlightTicket objects, you must create a CRD that informs the API server about this new resource type. The CRD includes details such as API version, kind, metadata, spec, and schema information (including supported fields, types, and validation rules).

Here’s an example of a CRD for the FlightTicket resource:

```yaml theme={null}
# flightticket-custom-definition.yml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: flighttickets.flights.com
spec:
  group: flights.com
  scope: Namespaced
  names:
    plural: flighttickets
    singular: flightticket
    kind: FlightTicket
    shortNames:
      - ft
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                from:
                  type: string
                to:
                  type: string
                number:
                  type: integer
                  minimum: 1
```

Key points in the CRD:

* The API group is `flights.com`.
* The resource scope is namespace-scoped.
* Both singular and plural names are defined along with a short name (`ft`).
* Only one version (`v1`) is served and defined as the storage version.
* An OpenAPI v3 schema enforces that the `spec` includes `from` and `to` as strings, and `number` as an integer with a minimum value of 1.

After creating the CRD, you can create, retrieve, and delete FlightTicket resources using these commands:

```bash theme={null}
kubectl create -f flightticket-custom-definition.yml
# Output:
kubectl create -f flightticket.yml
# Output:
kubectl get flightticket
# Output:
# NAME             STATUS
kubectl delete -f flightticket.yml
# Output:
# flightticket "my-flight-ticket" deleted
```

To verify that your new resource is recognized by Kubernetes, run:

```bash theme={null}
kubectl api-resources
# Output snippet:
# NAME            SHORTNAMES   APIGROUP     NAMESPACED   KIND
# flighttickets   ft           flights.com  true         FlightTicket
```

***

## The Role of a Custom Controller

While defining a CRD enables Kubernetes to store and retrieve FlightTicket objects in etcd, these objects remain inactive without a controller. A custom controller, often implemented in Go, observes events related to FlightTicket resources and executes business logic (such as calling external APIs to book or cancel flights).

Below is a simplified snippet of what such a controller might look like:

```go theme={null}
package flightticket

var controllerKind = apps.SchemeGroupVersion.WithKind("FlightTicket")

// Run begins watching and syncing FlightTicket resources.
func (dc *FlightTicketController) Run(workers int, stopCh <-chan struct{}) {
    // Controller logic goes here
}

// callBookFlightAPI handles the API call to book a flight ticket.
func (dc *FlightTicketController) callBookFlightAPI(obj interface{}) {
    // API call implementation goes here
}
```

<Callout icon="lightbulb">
  Without a custom controller, any FlightTicket resource you create remains a passive data record in etcd without triggering any external actions.
</Callout>

***

## Conclusion

In this lesson, we learned how:

* Kubernetes resources like Deployments are managed by built-in controllers.
* A custom resource (FlightTicket) can be defined to represent a new domain object.
* A CRD must be created so that Kubernetes recognizes your custom resource.
* A custom controller is essential to actively process and respond to events related to these resources.

In upcoming lessons, we’ll dive deeper into developing custom controllers that monitor CRD events and execute automated tasks based on resource changes.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/8b7b28d2-6dfe-4a88-8b50-14bdac7c286d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/84040576-5913-4ea2-8f1c-1c3ceb8e93d3" />
</CardGroup>


# KubeConfig

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Security/KubeConfig/page

This guide explores kubeconfig files in Kubernetes, focusing on authentication and context management for kubectl to enhance workflow efficiency.

Welcome to this guide on kubeconfig files in Kubernetes. In this article, we will explore how kubeconfig files streamline authentication and context management for kubectl, enhancing your workflow by reducing repetitive command-line options.

So far, you learned how to generate a certificate for a user and how a client can use the certificate file and key to query the Kubernetes REST API. For example, assume your cluster is named "my kube playground." You can send a curl request to the Kubernetes API server with the client certificate, key, and CA certificate:

```bash theme={null}
curl https://my-kube-playground:6443/api/v1/pods \
  --key admin.key \
  --cert admin.crt \
  --cacert ca.crt
```

The API server validates the certificate and responds with output similar to:

```json theme={null}
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {
    "selfLink": "/api/v1/pods"
  },
  "items": []
}
```

When using kubectl, you normally pass the same connection information with the corresponding options:

```bash theme={null}
kubectl get pods \
  --server my-kube-playground:6443 \
  --client-key admin.key \
  --client-certificate admin.crt \
  --certificate-authority ca.crt
```

This command might return:

```text theme={null}
No resources found.
```

Typing these options every time can become tedious. To simplify your workflow, you can move the connection details into a configuration file known as a kubeconfig file. By default, kubectl looks for a file named `config` under the `.kube` directory in your home directory. If the kubeconfig file is in its default location, you don’t have to specify connection options for each command:

```bash theme={null}
kubectl get pods
```

<Callout icon="lightbulb">
  Using a kubeconfig file saves you time by automatically applying connection settings, which means you no longer have to repeatedly supply options like `--client-key` and `--certificate-authority`.
</Callout>

## Kubeconfig Structure

The kubeconfig file is organized into three primary sections:

* **Clusters**: Define the various Kubernetes clusters you need access to. You might have separate clusters for development, testing, production, or different cloud providers.
* **Users**: Define the user accounts holding credentials (such as client certificates and keys) needed to access these clusters.
* **Contexts**: Link clusters and users together. A context specifies which user credentials should be used to access a particular cluster. For example, you could have a context called “admin\@production,” which uses the admin user’s credentials for the production cluster.

These components work together to streamline connectivity and authentication in your Kubernetes environment.

<Frame>
  ![The image illustrates a KubeConfig file structure, showing clusters, contexts, and users, with examples like "Development," "Admin@Production," and "Dev User."](https://kodekloud.com/kk-media/image/upload/v1752871289/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-KubeConfig/frame_160.jpg)
</Frame>

In our example, the server address and CA certificate information belong in the clusters section, while the admin user’s keys and certificates go in the users section. A context then binds these settings together. Below is a sample kubeconfig file in YAML format:

```yaml theme={null}
apiVersion: v1
kind: Config
clusters:
- name: my-kube-playground  # values hidden for brevity
- name: development
- name: production
- name: google
contexts:
- name: my-kube-admin@my-kube-playground
- name: dev-user@google
- name: prod-user@production
users:
- name: my-kube-admin
- name: admin
- name: dev-user
- name: prod-user
```

Note that you do not create Kubernetes objects for these configurations. Instead, kubectl reads this file to obtain the necessary connection details.

kubectl selects a context from the kubeconfig based on the `current-context` field. For example, if you set:

```yaml theme={null}
current-context: my-kube-admin@my-kube-playground
```

kubectl will default to that context. Alternatively, you can specify a different kubeconfig file from the command line using the `--kubeconfig` flag:

```bash theme={null}
kubectl config view --kubeconfig=my-custom-config
```

### Default Kubeconfig Example

An example output of the default kubeconfig file might be:

```plaintext theme={null}
apiVersion: v1
kind: Config
current-context: kubernetes-admin@kubernetes
clusters:
- cluster:
    certificate-authority-data: REDACTED
    server: https://172.17.0.5:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
users:
- name: kubernetes-admin
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
```

And when using a custom config file:

```plaintext theme={null}
kubectl config view --kubeconfig=my-custom-config
apiVersion: v1
kind: Config
current-context: my-kube-admin@my-kube-playground
clusters:
- name: my-kube-playground
- name: development
- name: production
contexts:
- name: my-kube-admin@my-kube-playground
- name: prod-user@production
users:
- name: my-kube-admin
- name: prod-user
```

### Switching Contexts

To switch your current context—for example, changing from the my-kube-admin account on the playground cluster to the prod-user account on the production cluster—use the `kubectl config use-context` command:

```bash theme={null}
kubectl config use-context prod-user@production
```

After running this command, your `current-context` in the kubeconfig file updates to `prod-user@production`. You can verify the change by viewing the configuration:

```yaml theme={null}
apiVersion: v1
kind: Config
current-context: prod-user@production
clusters:
- name: my-kube-playground
- name: development
- name: production
contexts:
- name: my-kube-admin@my-kube-playground
- name: prod-user@production
users:
- name: my-kube-admin
- name: prod-user
```

Additional variations of the `kubectl config` command let you update or delete entries within the kubeconfig file as needed.

## Configuring Namespaces

Each Kubernetes cluster can span multiple namespaces. You can designate a default namespace within a context so that switching contexts automatically sets the working namespace. For example, here is a configuration for the production cluster that sets "finance" as the default namespace:

```yaml theme={null}
apiVersion: v1
kind: Config
clusters:
- name: production
  cluster:
    certificate-authority: ca.crt
    server: https://172.17.0.51:6443
contexts:
- name: admin@production
  context:
    cluster: production
    user: admin
    namespace: finance
users:
- name: admin
  user:
    client-certificate: admin.crt
    client-key: admin.key
```

When you switch to the `admin@production` context, kubectl will automatically use the `finance` namespace.

## Working with Certificates in Kubeconfig

The kubeconfig file typically references certificate file paths. For clarity and robustness, it is best practice to use the full path to each certificate. Alternatively, you can embed the certificate data directly into the file by base64-encoding the certificate. For instance, instead of defining:

```yaml theme={null}
apiVersion: v1
kind: Config
clusters:
- name: production
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
```

you can embed the certificate data:

```yaml theme={null}
apiVersion: v1
kind: Config
clusters:
- name: production
  cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJU...
```

If you encounter certificate data in base64 format and need to decode it, use the following command:

```bash theme={null}
echo "LS0t...bnJ" | base64 --decode
```

This command will output the certificate in its standard PEM format:

```text theme={null}
-----BEGIN CERTIFICATE-----
MIICDCCAuCAQAoA...AIBDwAw...-----END CERTIFICATE-----
```

<Callout icon="lightbulb">
  Always ensure that certificate and key files are stored securely and access to the kubeconfig file is restricted to trusted users.
</Callout>

## Summary

In this article, we covered how kubeconfig files simplify connection management for Kubernetes by consolidating user credentials, cluster details, and context settings into a single file. Use this knowledge to streamline your kubectl commands and manage multiple Kubernetes environments effectively.

Next, apply these concepts by creating and troubleshooting your kubeconfig files to enhance your Kubernetes workflow.

For further reading, check out the following resources:

| Resource Type            | Description                          | Link                                                                                  |
| ------------------------ | ------------------------------------ | ------------------------------------------------------------------------------------- |
| Kubernetes Concepts      | Overview of Kubernetes functionality | [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) |
| Kubernetes Documentation | Complete documentation and guides    | [Kubernetes Documentation](https://kubernetes.io/docs/)                               |
| Docker Hub               | Container images and registry        | [Docker Hub](https://hub.docker.com/)                                                 |
| Terraform Registry       | Infrastructure as Code modules       | [Terraform Registry](https://registry.terraform.io/)                                  |

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/44fe192b-ed18-4a98-bfe2-0c0c91498ce4" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/27c5f4ce-2619-478f-9ea9-cb08c28423ce" />
</CardGroup>
