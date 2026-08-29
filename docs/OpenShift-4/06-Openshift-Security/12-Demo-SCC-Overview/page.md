# Demo SCC Overview

Source: https://notes.kodekloud.com/docs/OpenShift-4/Openshift-Security/Demo-SCC-Overview/page

This article reviews the CartsDB deployment, focusing on enhancing security by configuring a non-privileged mode and a read-only root filesystem.

In this article, we review our trusted CartsDB deployment—a deployment favored for its frequent use in our environment. Initially, when inspecting the containers section of the deployment, you may notice that no security context is configured. This is expected for the initial setup.

Below is the original YAML snippet for the CartsDB container configuration:

```yaml theme={null}
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
```

## Enhancing Security

One potential issue with the current configuration is that the container could run with elevated privileges. In Kubernetes, running a container in privileged mode gives it enhanced access to system resources, which could expose your system to vulnerabilities. For enhanced security, containers that do not require root-level permissions should run in a non-privileged mode.

<Callout icon="lightbulb">
  The updated configuration below includes a security context that explicitly disables privileged access and sets the root filesystem as read-only. This additional safeguard minimizes the risk of unauthorized changes if the container is compromised.
</Callout>

To address these security concerns, update the deployment with the following enhanced YAML configuration:

```yaml theme={null}
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
    securityContext:
      privileged: false
      readOnlyRootFilesystem: true
  volumes:
  - name: tmp-volume
    emptyDir:
      medium: Memory
  nodeSelector:
    beta.kubernetes.io/os: linux
```

### Explanation of Changes

* **Security Context:**\
  The new `securityContext` ensures that the container does not run with elevated privileges by setting `privileged: false` and by enforcing a read-only root filesystem (`readOnlyRootFilesystem: true`). This reduces the risk of security breaches by limiting unnecessary access to the system.

* **Additional Environment Variables and Volume Mounts:**\
  An extra environment variable (`MONGODB_ADMIN_PASSWORD`) is added for administrative operations. Additionally, a volume mount is configured to use a temporary directory (`/tmp`) backed by an `emptyDir` volume stored in memory. This approach is useful for non-persistent storage needs and enhances the overall configuration flexibility.

## Applying the Configuration

After saving the updated configuration in your `deployment.yaml` file, you can apply the changes using the following command:

```plaintext theme={null}
PS C:\Users\mike\Desktop> oc apply -f .\deployment.yaml
```

Once applied, verify that the CartsDB deployment is running with the enhanced security context by checking the OpenShift UI under Workloads > Deployments.

By following these steps, you have successfully implemented a more secure deployment for CartsDB, ensuring that the containers run with non-privileged settings and a read-only root filesystem. For further reading on Kubernetes security best practices, consider visiting the [Kubernetes Documentation](https://kubernetes.io/docs/).

## Additional Resources

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [OpenShift Documentation](https://docs.openshift.com/)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/openshift-4/module/413252bb-7455-41fa-86eb-e3e9370c8f08/lesson/43e87026-14cb-4cb6-bc0c-d2ae77c53cbb" />
</CardGroup>
