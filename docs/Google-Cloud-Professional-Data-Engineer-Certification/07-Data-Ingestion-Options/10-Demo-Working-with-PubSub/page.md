# Example: publish_demo.sh invoked from Cloud Shell
$ bash publish_demo.sh
messageIds:
- '16406407522493350'
messageIds:
- '16406765299791405'
messageIds:
- '16406424317703217'
```

Wait for the subscription's configured batching interval (1 minute in this demo), then inspect the bucket `kodekloud-pubsub-bucket` in the Cloud Console. You should see new objects created by Pub/Sub; download them to view the JSON payloads.

Example Cloud Storage object URLs produced by this integration:

```text theme={null}
https://storage.googleapis.com/kodekloud-pubsub-bucket/2025-11-23T10%3A02%3A44%2B00%3A00_f879d9
https://storage.cloud.google.com/kodekloud-pubsub-bucket/2025-11-23T10%3A02%3A44%2B00%3A00_f879d9
gs://kodekloud-pubsub-bucket/2025-11-23T10:02:44+00:00_f879d9
```

Why this is useful

* Zero-infrastructure ingestion: Pub/Sub writes directly to Cloud Storage; you don't need a streaming consumer running all the time.
* Files can be consumed by downstream tools: bulk load to BigQuery, process with Dataflow/Spark, run batch analytics, or archive raw events.

Step 5 — Clean up resources
To avoid unexpected charges, delete resources you created when finished. Example cleanup commands (run in Cloud Shell):

```bash theme={null}
# Delete subscriptions
$ gcloud pubsub subscriptions delete kodekloud-pull-sub
Deleted subscription [projects/kodekloud-gcp-training/subscriptions/kodekloud-pull-sub].

$ gcloud pubsub subscriptions delete kodekloud-storage-sub
Deleted subscription [projects/kodekloud-gcp-training/subscriptions/kodekloud-storage-sub].

# Delete topic
$ gcloud pubsub topics delete kodekloud-demo-topic
Deleted topic [projects/kodekloud-gcp-training/topics/kodekloud-demo-topic].

# Delete bucket and its objects using gsutil (fast)
$ gsutil -m rm -r gs://kodekloud-pubsub-bucket
Removing gs://kodekloud-pubsub-bucket/2025-11-23T10:02:44+00:00_f879d9#1763892224947144...
Removing gs://kodekloud-pubsub-bucket/2025-11-23T10:02:45+00:00_9c0f14#1763892226046057...
Removing gs://kodekloud-pubsub-bucket/2025-11-23T10:02:46+00:00_921f91#1763892227045748...
Removing gs://kodekloud-pubsub-bucket/2025-11-23T10:02:48+00:00_ce2906#1763892229247529...
Removing gs://kodekloud-pubsub-bucket/2025-11-23T10:02:49+00:00_a39d4e#1763892230246973...
/ [5/5 objects] 100% Done
Operation completed over 5 objects.
Removing gs://kodekloud-pubsub-bucket/...
```

> **warning** Always delete test topics, subscriptions, and buckets after your demo to prevent ongoing storage or Pub/Sub costs.

Resources used in this demo

| Resource                              | Example name / ID         | Purpose                                   |
| ------------------------------------- | ------------------------- | ----------------------------------------- |
| Pub/Sub topic                         | `kodekloud-demo-topic`    | Source of published messages              |
| Subscription (Cloud Storage delivery) | `kodekloud-storage-sub`   | Writes messages to Cloud Storage          |
| Cloud Storage bucket                  | `kodekloud-pubsub-bucket` | Destination for message files (JSON/Avro) |

Links and references

* Pub/Sub documentation: [https://cloud.google.com/pubsub/docs](https://cloud.google.com/pubsub/docs)
* Cloud Storage documentation: [https://cloud.google.com/storage/docs](https://cloud.google.com/storage/docs)
* BigQuery export for Pub/Sub: [https://cloud.google.com/pubsub/docs/integrations#bigquery](https://cloud.google.com/pubsub/docs/integrations#bigquery)

That’s it for this lesson — see you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/4b70dd08-59b3-4756-8bf0-d51821b7e59b)


# Demo Working with PubSub

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Demo-Working-with-PubSub/page

Guide demonstrating how to create Pub/Sub topics and subscriptions in GCP, publish JSON messages with attributes using gcloud, and pull messages while following best practices

This demo shows how to create a topic and subscription in the Google Cloud Console, publish JSON messages with attributes using Cloud Shell and the `gcloud` CLI, and pull those messages from a pull subscription. It covers best practices for labels, retention, and message attributes so you can organize and filter messages efficiently.

## 1. Create a Topic in the GCP Console

1. Open the GCP Console and search for "Pub/Sub".
2. From the Pub/Sub home page, click Create topic and choose a meaningful Topic ID (for this demo we use `kodekloud-demo-topic`). Keep defaults unless you need a schema, ingestion setting, or export configuration.
3. Scroll down and click Create. Pub/Sub manages the underlying infrastructure for you.

<Frame>
  <img alt="A screenshot of the Google Cloud Console Pub/Sub &#x22;Create topic&#x22; page showing a Topic ID field and various options (Add a default subscription, use a schema, enable ingestion, export to BigQuery, etc.). A blue &#x22;Create&#x22; button and a section for Transforms are visible near the bottom." />
</Frame>

After creating the topic, open it to review or edit configuration such as schema, ingestion, or export options. Under Details you can view metadata and configuration parameters.

Best practice: add labels when creating topics so you can organize, search, and filter resources later.

<Frame>
  <img alt="Screenshot of the Google Cloud Console showing Pub/Sub topic &#x22;kodekloud-demo-topic&#x22; details with a warning that messages will be lost unless a subscription or retention is set. Visible options include exporting to BigQuery or Cloud Storage and topic metadata/tabs." />
</Frame>

## 2. Create a Subscription

From the left-hand menu click Subscriptions → Create subscription.

* Subscription ID: e.g. `kodekloud-pull-sub`
* Topic: `kodekloud-demo-topic`
* Delivery type: Pull (this demo uses Pull)

Retention: by default Pub/Sub retains unacknowledged messages for up to 7 days. Retaining acknowledged messages must be explicitly enabled. The retention duration is configurable.

A pull subscription requires your application to request messages (good for batch or controlled processing). Push subscriptions forward messages to an HTTP(S) endpoint.

<Frame>
  <img alt="A screenshot of the Google Cloud Console showing the Pub/Sub &#x22;Create subscription&#x22; page. The Subscription ID is &#x22;kodekloud-pull-sub&#x22; with the topic set to &#x22;kodekloud-demo-topic&#x22; and the delivery type selected as &#x22;Pull.&#x22;" />
</Frame>

> **lightbulb** Pull subscriptions require the client to explicitly request messages. Push subscriptions send messages to a configured endpoint. Choose the mode that suits your processing pattern.

## 3. Publish Messages with Cloud Shell and gcloud

Open Cloud Shell and set environment variables:

```bash theme={null}
export PROJECT_ID="kodekloud-gcp-training"
export TOPIC_ID="kodekloud-demo-topic"
export MESSAGE_ID_PREFIX="kodekloud-message"
gcloud config set project "$PROJECT_ID"
```

Create a small Bash script `publish_demo.sh` to publish three JSON messages with attributes:

```bash theme={null}
#!/bin/bash
for i in 1 2 3; do
  gcloud pubsub topics publish "$TOPIC_ID" \
    --message "{\"id\":\"${MESSAGE_ID_PREFIX}${i}\", \"status\": \"created\", \"source\": \"kodekloud\"}" \
    --attribute env=demo \
    --attribute team=kodekloud
done
```

Make the script executable and run it:

```bash theme={null}
bash publish_demo.sh
```

Example concise output (each publish returns a message ID):

```console theme={null}
messageIds:
- '16406205265696513'
messageIds:
- '16406362145303396'
messageIds:
- '16406178636819281'
```

Note: Attributes are small key/value metadata attached to a message. They are useful for filtering and routing, but they consume part of the message size quota—design attributes accordingly.

## 4. Pull Messages from the Subscription (Console)

1. In the Pub/Sub Console go to Subscriptions → select `kodekloud-pull-sub`.
2. Open Messages → Pull to trigger a pull request and view messages.

Pulled message payloads will look like the JSON bodies below:

```json theme={null}
{"id":"kodekloud-message-1","status":"created","source":"kodekloud"}
{"id":"kodekloud-message-2","status":"created","source":"kodekloud"}
{"id":"kodekloud-message-3","status":"created","source":"kodekloud"}
```

The UI displays message attributes as well (for example `env: demo`, `team: kodekloud`). You can use these attributes with subscription filters or in your subscriber logic to process only relevant messages.

If you update the script to change attributes (for example `team=kodekloud` → `team=raghu`) and publish again, the new attribute values will appear when pulling messages. This demonstrates how attributes enable flexible metadata-based routing for multiple producers sharing a topic.

## Quick Reference

| Resource           | Purpose                                       | Example CLI                                                                                            |
| ------------------ | --------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Topic              | Message hub to which publishers send messages | `gcloud pubsub topics create kodekloud-demo-topic`                                                     |
| Subscription       | Consumer view of a topic (Pull or Push)       | `gcloud pubsub subscriptions create kodekloud-pull-sub --topic=kodekloud-demo-topic --ack-deadline=10` |
| Message attributes | Key/value metadata for filtering/routing      | `--attribute env=demo`                                                                                 |

For full Pub/Sub concepts and best practices, see the official documentation: [Cloud Pub/Sub documentation](https://cloud.google.com/pubsub/docs).

## Summary

* Create a topic in the GCP Console; add labels for easier organization.
* Create a subscription (choose Pull or Push based on your consumer architecture).
* Publish messages using the `gcloud` CLI or client libraries; include attributes for metadata and filtering.
* Pull messages from pull subscriptions (console, client libraries, or `gcloud`).
* Use subscription filters and message attributes to route and process only relevant messages.

That concludes this demo: creating a topic, publishing messages, and pulling them from a subscription.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/f1645d43-cd05-4d27-a919-ecc23f8192a0)
