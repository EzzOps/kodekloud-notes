# Persistent Volumes

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Container-Orchestration-Storage/Persistent-Volumes/page

This article provides a comprehensive guide on persistent volumes in Kubernetes, focusing on centralized storage management for scalable environments.

Welcome to this comprehensive guide on persistent volumes in Kubernetes. In previous lessons, we introduced the concept of volumes. Now, we focus on persistent volumes and explore how they centralize storage management for a scalable, production-ready environment.

## Traditional Volume Configuration

Previously, storage details were embedded directly into the pod specification file. For example:

```yaml theme={null}
volumes:
- name: data-volume
  awsElasticBlockStore:
    volumeID: <volume-id>
    fsType: ext4
```

Although this approach works for simple deployments, it becomes cumbersome in large, multi-user environments. Each pod requires its own storage configuration, making global updates difficult and error-prone.

## Centralized Storage with Persistent Volumes

Persistent volumes solve these challenges by separating storage configuration from the pod definitions. Cluster administrators create a pool of storage resources, and users claim storage via Persistent Volume Claims (PVCs). This model simplifies management and reduces redundancy across the environment.

<Frame>
  ![The image illustrates the relationship between Persistent Volume Claims (PVC) and Persistent Volumes (PVs) in a Kubernetes environment.](https://kodekloud.com/kk-media/image/upload/v1752880632/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Persistent-Volumes/frame_90.jpg)
</Frame>

In summary:

* Administrators manage storage centrally.
* Users claim storage as needed without repetitive configuration.
* Global changes and updates become easier to implement.

## Creating a Persistent Volume

In this section, we create a persistent volume using a YAML template. Begin by updating the API version, setting the kind to PersistentVolume, and naming the volume (e.g., PV-01). Within the spec section, include:

* **Access Modes:** Determines how a volume can be mounted (e.g., ReadOnlyMany, ReadWriteOnce, ReadWriteMany).
* **Capacity:** Specifies the allocated storage size (1Gi in this example).
* **Volume Type:** Here, we use a host path to utilize local node storage.

<Callout icon="lightbulb">
  While using a hostPath is useful for demonstration purposes, it is not recommended for production environments. Always opt for a supported production-ready storage solution.
</Callout>

Below is an example of a persistent volume definition:

```yaml theme={null}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-voll
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 1Gi
  hostPath:
    path: /tmp/data
```

## Deploying the Persistent Volume

To create the persistent volume, run the following command in your terminal:

```bash theme={null}
kubectl create -f pv-definition.yaml
```

After deployment, verify that the persistent volume has been successfully created by executing:

```bash theme={null}
kubectl get persistentvolume
```

This command lists all available persistent volumes, including the one you just created.

## Conclusion

Persistent volumes in Kubernetes enable centralized storage management that streamlines deployments and simplifies ongoing maintenance. By externalizing storage configuration via PVCs, you ensure efficient resource utilization and easier scalability.

For further information, visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

Happy deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/fbd7b99a-b2c1-4eda-9ef9-f5e0d7a20fce/lesson/3b20ea5e-b33a-46f0-9a9a-1d5eecaa4eba" />
</CardGroup>
