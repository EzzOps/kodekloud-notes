# pv-definition.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-vol1
spec:
  capacity:
    storage: 500Mi
  accessModes:
    - ReadWriteOnce
  gcePersistentDisk:
    pdName: pd-disk
    fsType: ext4
```

```yaml theme={null}
# pvc-definition.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

```yaml theme={null}
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: random-number-generator
spec:
  containers:
    - name: alpine
      image: alpine
      command: ["/bin/sh", "-c"]
      args:
        - shuf -i 0-100 -n 1 >> /opt/number.out
      volumeMounts:
        - name: data-volume
          mountPath: /opt
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: myclaim
```

<Callout icon="lightbulb">
  Static provisioning works, but each new disk requires manual cloud CLI steps. Maintenance and scaling can become cumbersome.
</Callout>

***

## Dynamic Provisioning with StorageClass

With a **StorageClass**, Kubernetes can automatically create and bind a PV when you apply a PVC. This **dynamic provisioning** eliminates manual disk creation.

### StorageClass Definition

Define a StorageClass that uses the GCE PD provisioner:

```yaml theme={null}
# sc-definition.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
```

***

### Using a Dynamic PVC and Pod

1. Create a PVC that references your StorageClass:
   ```yaml theme={null}
   # pvc-dynamic.yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: myclaim
   spec:
     storageClassName: google-storage
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 500Mi
   ```
2. Deploy a Pod that mounts the PVC:
   ```yaml theme={null}
   # pod-dynamic.yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: random-number-generator
   spec:
     containers:
       - name: alpine
         image: alpine
         command: ["/bin/sh", "-c"]
         args:
           - shuf -i 0-100 -n 1 >> /opt/output.txt
         volumeMounts:
           - name: data-volume
             mountPath: /opt
     volumes:
       - name: data-volume
         persistentVolumeClaim:
           claimName: myclaim
   ```

Kubernetes will then:

1. Provision a new GCE PD of the requested size.
2. Create a corresponding PV.
3. Bind your PVC to that PV.
4. Attach the volume to your Pod.

***

## Comparing Provisioning Methods

| Feature       | Static Provisioning                 | Dynamic Provisioning (StorageClass)    |
| ------------- | ----------------------------------- | -------------------------------------- |
| Disk Creation | Manual via cloud CLI                | Automated by Kubernetes                |
| PV Definition | Pre-created `PersistentVolume`      | Generated automatically                |
| PVC Binding   | Manual or automatic if labels match | Automatic                              |
| Scalability   | Limited (manual work for each disk) | High (one PVC, one step)               |
| Flexibility   | Low                                 | High (parameters, tiers, provisioners) |

***

## Customizing StorageClass Parameters

Most provisioners let you fine-tune disks. For GCE PD, you can specify:

```yaml theme={null}
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard        # pd-standard or pd-ssd
  replication-type: none   # none or regional-pd
```

<Callout icon="triangle-alert">
  Be cautious with `regional-pd`: it offers high availability at higher cost. Always choose based on your SLA requirements.
</Callout>

***

## Defining Service Tiers

You can create multiple StorageClasses to represent different performance tiers:

```yaml theme={null}
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: silver
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  replication-type: none
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gold
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: none
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: platinum
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: regional-pd
```

| Tier     | Disk Type   | Replication | Use Case                            |
| -------- | ----------- | ----------- | ----------------------------------- |
| silver   | pd-standard | none        | Development, testing                |
| gold     | pd-ssd      | none        | Production, low-latency             |
| platinum | pd-ssd      | regional-pd | Mission-critical, high-availability |

When you create a PVC, just set `storageClassName` to select your tier. Kubernetes handles provisioning and binding behind the scenes.

***

## Links and References

* [Kubernetes StorageClass Documentation](https://kubernetes.io/docs/concepts/storage/storage-classes/)
* [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* [GCE PD Provisioner](https://kubernetes.io/docs/concepts/storage/volumes/#gcepersistentdisk)
* [gcloud compute disks create](https://cloud.google.com/sdk/gcloud/reference/compute/disks/create)

***

Mastering StorageClasses empowers you to build scalable, self-service storage in your Kubernetes clusters—no more manual volume management!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/57187452-58a0-499e-af29-98348721afc6" />
</CardGroup>


# Volume Driver Plugins in Docker

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Volume-Driver-Plugins-in-Docker/page

This article explains Dockers volume driver plugins for managing persistent data storage across containers.

## Understanding Storage Drivers vs Volume Plugins

Storage drivers handle the low-level management of image and container layers. For persistent data, Docker uses **volumes**, which rely on volume driver plugins rather than storage drivers.

<Callout icon="lightbulb">
  Volumes are decoupled from image storage drivers. They ensure your data persists across container restarts and removals.
</Callout>

## Default Local Volume Driver

Docker’s default volume driver is `local`. It creates volumes on the host under `/var/lib/docker/volumes`. This driver is ideal for simple, on-host storage needs.

## Third-Party Volume Driver Plugins

To integrate with external storage platforms, Docker supports many community and commercial volume plugins. Below is a summary of popular options:

| Plugin       | Storage Provider(s)                                      | Reference      |
| ------------ | -------------------------------------------------------- | -------------- |
| Azure File   | Azure File Storage                                       | `azurefile`    |
| Convoy       | Various (via driver extensions)                          | `convoy`       |
| DigitalOcean | Block Storage                                            | `digitalocean` |
| Blocker      | Block Storage                                            | `blocker`      |
| GCE PD       | Google Persistent Disk                                   | `gcepd`        |
| ClusterFS    | Clustered filesystems                                    | `clusterfs`    |
| NetApp       | NetApp storage arrays                                    | `netapp`       |
| RexRay       | AWS EBS/S3, EMC Isilon/ScaleIO, GCE PD, OpenStack Cinder | `rexray`       |
| Portworx     | Portworx clusters                                        | `pxd`          |
| vSphere      | VMware vSphere storage                                   | `vsphere`      |

<Frame>
  ![The image lists different types of storage and volume drivers, including AUFS, ZFS, and Azure File Storage, with a link to Docker documentation.](https://kodekloud.com/kk-media/image/upload/v1752874037/notes-assets/images/Docker-Certified-Associate-Exam-Course-Volume-Driver-Plugins-in-Docker/storage-volume-drivers-docker.jpg)
</Frame>

<Callout icon="triangle-alert">
  Ensure each volume driver plugin is installed and configured on your Docker host. Verify compatibility and installation steps in the [Docker Storage Plugins](https://docs.docker.com/engine/extend/plugins/) guide.
</Callout>

## Multi-Provider Example: RexRay

RexRay can provision volumes across multiple storage backends. To run a MySQL container with an AWS EBS volume:

```bash theme={null}
docker run -it \
  --name mysql \
  --mount type=volume,volume-driver=rexray/ebs,source=ebs-vol,target=/var/lib/mysql \
  mysql
```

When this container stops or is removed, your data remains intact on the attached EBS volume.

<Callout icon="lightbulb">
  This approach extends to Kubernetes. Explore how Kubernetes **PersistentVolumes** and **StorageClasses** manage dynamic provisioning with external drivers.
</Callout>

## Links and References

* [Docker Volumes](https://docs.docker.com/storage/volumes/)
* [RexRay Documentation](https://rexray.readthedocs.io/)
* [Docker Storage Plugins](https://docs.docker.com/engine/extend/plugins/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/0367a659-2e0a-4b02-97ed-1f8b291679e8" />
</CardGroup>
