# Demo Accessing MinIO

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Accessing-MinIO/page

Guide to access and inspect the Argo Workflows bundled MinIO artifact repository, including exposing the UI, retrieving credentials, browsing artifacts, and verifying archived workflow logs.

This guide shows how to access the default MinIO artifact repository installed by the Argo Workflows quick-start / minimal configuration. The bundled MinIO server stores workflow artifacts and archived logs so you can inspect them from a web UI or via S3-compatible tools.

## 1. Confirm MinIO pod and service are running

First, verify the MinIO pod and service exist in the `argo` namespace:

```bash theme={null}
kubectl -n argo get po,svc | grep -i minio
```

Example output:

```bash theme={null}
pod/minio-5cb4ff75c9-stmmw   1/1   Running   0   4h40m
service/minio               ClusterIP   10.108.36.67   <none>   9000/TCP,9001/TCP   4h40m
```

By default the service is a ClusterIP and not directly reachable from outside the cluster.

## 2. Expose the MinIO web UI (quick demo options)

To view the MinIO web console in your browser you can either:

* Change the Service to a NodePort (quick one-off demo), or
* Use `kubectl port-forward` (recommended for local access without changing cluster services), or
* Configure an Ingress with authentication for production.

Quick method: edit the MinIO service and change the type to `NodePort`:

```bash theme={null}
kubectl -n argo edit svc minio
