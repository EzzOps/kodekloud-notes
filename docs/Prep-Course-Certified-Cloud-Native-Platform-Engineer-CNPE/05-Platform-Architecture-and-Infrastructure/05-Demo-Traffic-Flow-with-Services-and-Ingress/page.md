# persistentvolumeclaim/app-storage created
```

Watch the PVC in the `storage` namespace:

```bash theme={null}
kubectl get pvc -n storage -w
```

Because `VolumeBindingMode` is `WaitForFirstConsumer`, the PVC will initially be `Pending` until a Pod mounts it. Create a Pod that consumes the PVC to trigger provisioning:

```bash theme={null}
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: app
  namespace: storage
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - mountPath: /data
      name: storage
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: app-storage
EOF
# pod/app created
```

After scheduling, the PVC should transition from `Pending` to `Bound`:

```text theme={null}
NAME          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
app-storage   Bound    pvc-1dcc29bc-a8a1-4c97-a5f9-bb0e19dadc7   1Gi        RWO            fast           30s
```

A PV is created dynamically to satisfy the claim:

```bash theme={null}
kubectl get pv
```

Example:

```text theme={null}
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STORAGECLASS   STATUS   CLAIM
pvc-1dcc29bc-a8a1-4c97-a5f9-bb0e19dadc7    1Gi        RWO            Delete           fast           Bound    storage/app-storage
```

Explanation: Because the `fast` StorageClass has `ReclaimPolicy: Delete`, the underlying storage will be deleted automatically when the PVC (and its binding) is removed.

## Demonstrate reclaim policy difference: Retain (archive StorageClass)

The `archive` StorageClass in this cluster uses `ReclaimPolicy: Retain`. Create a PVC using that class.

Save this as `pvc-archive.yaml`:

```yaml theme={null}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: archive-storage
  namespace: storage
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: archive
  resources:
    requests:
      storage: 500Mi
```

Apply it:

```bash theme={null}
kubectl apply -f pvc-archive.yaml
# persistentvolumeclaim/archive-storage created
```

Create a Pod that mounts the `archive-storage` claim:

```bash theme={null}
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: archive-app
  namespace: storage
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - mountPath: /data
      name: storage
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: archive-storage
EOF
# pod/archive-app created
```

After scheduling, the PVC will bind and a PV will be provisioned for the `archive` StorageClass. The PV will show `RECLAIM POLICY: Retain`:

```bash theme={null}
kubectl get pv
```

Example (trimmed):

```text theme={null}
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STORAGECLASS   STATUS   CLAIM
pvc-aaaa1111-...                           500Mi      RWO            Retain           archive        Bound    storage/archive-storage
```

## What happens on deletion with different reclaim policies

1. For fast (ReclaimPolicy: Delete)
   * Delete the Pod and the PVC:
     ```bash theme={null}
     kubectl delete pod -n storage app
     kubectl delete pvc -n storage app-storage
     ```
   * Result: The PV and the underlying storage resource are deleted automatically.

2. For archive (ReclaimPolicy: Retain)
   * Delete the Pod, then delete the PVC:
     ```bash theme={null}
     kubectl delete pod -n storage archive-app
     kubectl delete pvc -n storage archive-storage
     ```
   * Result: The PV remains in the cluster and moves to `Released` state. The underlying data is preserved and requires administrator action to reclaim or reuse the volume.

Example after deleting a PVC for a `Retain` PV:

```bash theme={null}
kubectl get pv
```

Example output:

```text theme={null}
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STORAGECLASS   STATUS     CLAIM
pvc-aaaa1111-...                           500Mi      RWO            Retain           archive        Released   <none>
```

When a PV is `Released` with `Retain`, an administrator must:

* Inspect and back up data if needed
* Clean or wipe data to make the volume reusable
* Remove or update `claimRef` on the PV to allow re-binding
* Or manually delete the underlying storage resource

<Callout icon="lightbulb">
  Choose reclaim policies based on workload needs:

  * Use `Retain` for critical, stateful workloads (databases, logs) to prevent accidental data loss.
  * Use `Delete` for ephemeral or test workloads to automate cleanup.
    Also confirm correct access modes (`ReadWriteOnce`, `ReadWriteMany`) and zone affinity by using `WaitForFirstConsumer` in multi-zone clusters.
</Callout>

## Recap / Best practices

* Inspect StorageClasses before creating PVCs:
  * `kubectl get sc` and `kubectl describe sc <name>`
* Understand reclaim behavior:
  * `Delete` — automated cleanup
  * `Retain` — manual intervention required
* Use `WaitForFirstConsumer` to avoid cross-zone provisioning in multi-zone clusters.
* Prefer explicitly setting `storageClassName` in PVCs unless you intentionally rely on a default StorageClass.
* Confirm access modes and size requirements match application needs.
* Monitor resource lifecycle:
  * `kubectl get pvc -n <ns> -w`
  * `kubectl get pv`

## Links and references

* [Kubernetes Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
* [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* [Persistent Volume Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)

Explore your cluster’s StorageClasses, create PVCs and Pods, and observe how Kubernetes dynamically provisions and manages storage according to StorageClass settings.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/989346de-0207-4837-af11-bf456d188972/lesson/d09019f0-e51f-485c-aa53-736128144afd" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/989346de-0207-4837-af11-bf456d188972/lesson/b55e9c11-0076-440f-b2bb-735326813468" />
</CardGroup>


# Demo Traffic Flow with Services and Ingress

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-Architecture-and-Infrastructure/Demo-Traffic-Flow-with-Services-and-Ingress/page

Demo explaining Kubernetes Services, ClusterIP, NodePort, and Ingress with an nginx ingress controller showing routing, service discovery, and handling ephemeral pod lifecycles.

Every Kubernetes platform engineer faces the same challenge early on: pods are ephemeral. They are created and destroyed frequently, and each new pod receives a different IP address. Relying on pod IPs for connectivity doesn't scale — services provide a stable abstraction for discovery and load balancing. This demo shows why Services are essential, how ClusterIP and NodePort services work, and how an Ingress + Ingress controller lets you route external traffic to multiple services through a single entry point.

## 1) Pods are ephemeral — deployment example

Create a Deployment named `web` (nginx) with three replicas:

```bash theme={null}
kubectl create deployment web --image=nginx --replicas=3
```

List pods and their IPs:

```bash theme={null}
kubectl get pods -o wide
```

Example output (IPs will vary):

```text theme={null}
NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE
web-68d995574f-4qvnb        1/1     Running   0          2m    172.17.0.6    controlplane
web-68d995574f-nhgxz        1/1     Running   0          2m    172.17.0.7    controlplane
web-68d995574f-6hjj         1/1     Running   0          2m    172.17.0.8    controlplane
```

If you delete a pod, the Deployment controller will create a replacement pod with a different IP:

```bash theme={null}
kubectl delete pod web-68d995574f-4qvnb
kubectl get pods -o wide
```

Example replacement:

```text theme={null}
NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE
web-68d995574f-4vnqv        1/1     Running   0          15s  172.17.0.9    controlplane
web-68d995574f-nhgxz        1/1     Running   0          2m   172.17.0.7    controlplane
web-68d995574f-6hjj         1/1     Running   0          2m   172.17.0.8    controlplane
```

Any client using the old pod IP (for example `172.17.0.6`) will lose connectivity. This is the primary reason we use Services.

## 2) ClusterIP service (internal cluster access)

Expose the `web` Deployment as a ClusterIP service named `web-svc` on port 80:

```bash theme={null}
kubectl expose deploy web --port=80 --target-port=80 --name=web-svc
kubectl describe svc web-svc
```

Key fields from `kubectl describe svc web-svc`:

```text theme={null}
Name:                     web-svc
Namespace:                default
Selector:                 app=web
Type:                     ClusterIP
IP:                       172.20.212.114
Port:                     80/TCP
TargetPort:               80/TCP
Endpoints:                172.17.0.9:80,172.17.0.7:80,172.17.0.8:80
```

* ClusterIP is internal-only (accessible from inside the cluster).
* The Service uses selectors (labels) to discover matching pods — the Deployment assigned the label `app=web`.

Check pod labels:

```bash theme={null}
kubectl get pods --show-labels
```

Example output:

```text theme={null}
NAME                        READY   STATUS    RESTARTS   AGE   LABELS
web-68d995574f-4vnqv        1/1     Running   0          1m   app=web,pod-template-hash=68d995574f
web-68d995574f-nhgxz        1/1     Running   0          2m   app=web,pod-template-hash=68d995574f
web-68d995574f-6hjj         1/1     Running   0          2m   app=web,pod-template-hash=68d995574f
```

## 3) NodePort service (external access for labs or single-node)

If you need external access in a lab or single-node environment (without a cloud load balancer), use NodePort:

```bash theme={null}
kubectl expose deploy web --port=80 --target-port=80 --type=NodePort --name=web-nodeport
kubectl get svc web-nodeport
```

Example:

```text theme={null}
NAME           TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)
web-nodeport   NodePort   172.20.11.172   <none>        80:30309/TCP
```

Curl the NodePort (on the node IP or `localhost` if running locally):

```bash theme={null}
curl localhost:30309
```

You should receive the NGINX default welcome page HTML.

Note: NodePort assigns a port in the 30000–32767 range. This is convenient for testing but not ideal for production (awkward ports, limited range, no TLS termination). For path-based routing, virtual hosts, and TLS termination, use Ingress (with an Ingress controller).

<Callout icon="lightbulb">
  Ingress provides host-based and path-based routing, and TLS termination. It requires an Ingress controller to implement the routing (for example, [nginx-ingress](https://kubernetes.github.io/ingress-nginx/), [Traefik](https://traefik.io/), or other controllers).
</Callout>

## 4) Ingress controller — verify it's running

This lab uses the nginx ingress controller in namespace `ingress-nginx`. Verify controller pods and service:

```bash theme={null}
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

Example:

```text theme={null}
