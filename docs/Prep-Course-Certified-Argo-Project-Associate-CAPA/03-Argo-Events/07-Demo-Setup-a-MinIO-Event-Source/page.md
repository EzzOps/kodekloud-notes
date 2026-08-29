# Demo Setup a MinIO Event Source

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/Demo-Setup-a-MinIO-Event-Source/page

Setting up an Argo Events EventSource to receive MinIO bucket notifications, including credentials, manifest, testing, and troubleshooting for object create and delete events

In this lesson you'll register an Argo Events EventSource that listens for MinIO bucket notifications. Argo Events receives events in a CloudEvents-style JSON envelope; a simplified example looks like:

```json theme={null}
{
  "context": {
    "type": "type_of_event_source",
    "specversion": "cloud_events_version",
    "source": "name_of_the_event_source",
    "id": "unique_event_id",
    "time": "event_time",
    "datacontenttype": "type_of_data",
    "subject": "name_of_the_configuration_within_event_source"
  },
  "data": {
    "notification": [
      {
        "eventName": "s3:ObjectCreated:Put",
        "bucket": { "name": "argo-events-bucket" },
        "object": { "key": "path/to/object" }
      }
    ]
  }
}
```

This is the schema MinIO sends for bucket notifications. Your EventSource must be able to reach the MinIO API endpoint and have valid credentials (access key + secret key) available in the `argo-events` namespace.

## Prerequisites & connectivity

Ensure the following before creating the EventSource:

| Requirement                        | Purpose                                                      | Example / Notes                                           |
| ---------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------- |
| Reachable MinIO API                | Argo Events must connect to MinIO (default port 9000)        | Service endpoint like `minio.argo.svc.cluster.local:9000` |
| Kubernetes Secret with MinIO creds | EventSource reads credentials from a secret in `argo-events` | `minio-creds` containing `accesskey` and `secretkey`      |
| Bucket to watch                    | The bucket that will emit notifications                      | `argo-events-bucket`                                      |

> **lightbulb** If your cluster's DNS or service discovery differs, adjust the endpoint to the correct FQDN or ClusterIP:port. Confirm the MinIO API is accessible from the `argo-events` namespace.

## Port-forward locally and set up the MinIO client (optional)

If you prefer to configure the bucket from your workstation using the MinIO client (`mc`), port-forward the MinIO service and configure an alias:

```bash theme={null}
