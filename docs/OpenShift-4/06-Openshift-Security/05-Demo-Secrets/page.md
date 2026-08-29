# Demo Secrets

Source: https://notes.kodekloud.com/docs/OpenShift-4/Openshift-Security/Demo-Secrets/page

This guide demonstrates methods for creating and managing Kubernetes secrets using YAML manifests and the OpenShift web console.

This guide demonstrates multiple methods for creating and managing Kubernetes secrets, including using YAML manifests and the OpenShift web console. By following these instructions, you can securely store and reference sensitive information in your deployments.

## Creating a Secret Using a YAML Manifest

Traditionally, in Kubernetes (and, by extension, OpenShift, which runs on Kubernetes), secrets are defined using a YAML manifest. Below is an example of a secret definition:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  namespace: default
  name: dbpassword
type: Opaque
data:
  MONGODB_PASSWORD: password
```

<Callout icon="lightbulb">
  In this manifest:

  * The **apiVersion** and **kind** specify that this is a Kubernetes Secret.
  * The **metadata** section includes the namespace (`default`) and the secret's name (`dbpassword`).
  * The **type** `Opaque` means the secret is intended for storing arbitrary user-defined data.
  * The **data** section holds key/value pairs; in this example, `MONGODB_PASSWORD` is paired with its secret value.
</Callout>

This structure is similar to a ConfigMap, but Secrets are designed for sensitive information.

To create this secret via the OpenShift client, save the above content into a file (e.g., `secret.yaml`) and run:

```bash theme={null}
oc apply -f secret.yaml
```

You should see a confirmation message such as:

```bash theme={null}
secret/dbpassword created
```

If you ever need to remove the secret, execute:

```bash theme={null}
oc delete -f secret.yaml
```

## Creating a Secret via the OpenShift Web Console

You can also create a secret using the OpenShift web console. Follow these steps:

1. Navigate to the Dashboard.
2. In the **Workloads** section, select **Secrets**.
3. Click on **Create Secret** and choose the key/value secret option.
4. Provide the following details:
   * **Secret Name:** For example, `dbpassword`
   * **Key:** For example, `MONGODB_PASSWORD`
   * **Value:** For example, `password`

The resulting YAML configuration remains consistent with the earlier example:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  namespace: default
  name: dbpassword
type: Opaque
data:
  MONGODB_PASSWORD: password
```

<Frame>
  ![The image shows the "Secrets" section of the Red Hat OpenShift web console, displaying a list of Kubernetes secrets with options to create new ones.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882725/notes-assets/images/OpenShift-4-Demo-Secrets/openshift-secrets-kubernetes-console.jpg)
</Frame>

After creating the secret, you can view its details—including the YAML configuration—to ensure that it has been set up correctly.

<Frame>
  ![The image shows a Red Hat OpenShift interface displaying details of a secret named "dbpassword" in the default namespace. It includes options to add the secret to a workload and edit labels and annotations.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882727/notes-assets/images/OpenShift-4-Demo-Secrets/openshift-secret-dbpassword-interface.jpg)
</Frame>

## Referencing Secrets in Deployment Configurations

Once your secret is ready, you can reference it in your application’s deployment configuration. For instance, consider the following deployment YAML for a MongoDB instance used in the CartsDB application:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: carts-db
  namespace: default
  labels:
    name: carts-db
spec:
  replicas: 1
  selector:
    matchLabels:
      name: carts-db
  template:
    metadata:
      labels:
        name: carts-db
    spec:
      containers:
      - name: carts-db
        image: centos/mongodb-34-centos7
        resources:
          requests:
            memory: "100Mi"
        ports:
          - name: mongo
            containerPort: 27017
        env:
          - name: MONGODB_USER
            value: sock-user
          - name: MONGODB_PASSWORD
            valueFrom:
              secretKeyRef:
                name: dbpassword
                key: MONGODB_PASSWORD
          - name: MONGODB_DATABASE
            value: data
          - name: MONGODB_ADMIN_PASSWORD
            value: admin
        volumeMounts:
          - mountPath: /tmp
            name: tmp-volume
```

In this deployment:

* The environment variable `MONGODB_PASSWORD` utilizes `valueFrom` with a `secretKeyRef` to securely fetch the password from the `dbpassword` secret.
* This method avoids embedding sensitive data directly in the deployment manifest, ensuring a cleaner and more secure configuration.

Deploy the application with the following command:

```bash theme={null}
oc apply -f deployment.yaml
```

After deployment, review the OpenShift console under **Deployments** and **Pods** to verify that the CartsDB pod is running as expected.

<Frame>
  ![The image shows a Red Hat OpenShift console displaying details of a deployment named "carts-db," with one running pod listed under the "Pods" tab.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882728/notes-assets/images/OpenShift-4-Demo-Secrets/openshift-console-carts-db-deployment.jpg)
</Frame>

If you inspect the running pod's YAML, you'll confirm that the `MONGODB_PASSWORD` variable is correctly referencing the secret around the indicated line in the detailed view.

## Conclusion

Whether you define your secrets via YAML manifests or through the OpenShift web console, securely managing sensitive data is crucial to protecting your applications. Kubernetes secrets enable you to keep secret data separate from application code, ensuring that deployment configurations remain secure and maintainable.

For more detailed information on managing secrets in Kubernetes and OpenShift, review the [Kubernetes Documentation](https://kubernetes.io/docs/) and [OpenShift Documentation](https://docs.openshift.com/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/openshift-4/module/413252bb-7455-41fa-86eb-e3e9370c8f08/lesson/24f32436-cd2d-4f30-837a-366c1251e60a" />
</CardGroup>
