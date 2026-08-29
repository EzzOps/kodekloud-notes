# Demo Hands on with PubSub Subscription and its integration

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Demo-Hands-on-with-PubSub-Subscription-and-its-integration/page

Hands on demo connecting Pub/Sub topic to Cloud Storage so published messages are written as files for zero infrastructure ingestion and downstream processing.

Welcome back. In this hands-on demo you'll extend your Pub/Sub knowledge by connecting a Pub/Sub topic to Cloud Storage so that published messages land as files in a bucket. This pattern is useful for simple, zero-infrastructure ingestion pipelines (for example, later loading objects into BigQuery or processing them with Spark).

Prerequisites

* A Google Cloud project with billing enabled.
* Pub/Sub API and Cloud Storage enabled.
* A Pub/Sub topic already created (this demo uses `kodekloud-demo-topic`).

What we'll do

1. Create a Cloud Storage bucket.
2. Inspect the Pub/Sub topic.
3. Create a subscription that writes messages to the bucket.
4. Publish messages and confirm files appear in Cloud Storage.
5. Clean up resources.

Step 1 — Create a Cloud Storage bucket

1. In the Cloud Console search for "Buckets" → Create.
2. Provide a globally unique name (demo uses `kodekloud-pubsub-bucket`).
3. Leave other settings at their defaults and click Create.

<Frame>
  <img alt="A screenshot of the Google Cloud Console &#x22;Create a bucket&#x22; page showing a bucket name field filled with &#x22;kodekloud-pubsub-bucket.&#x22; The right side shows location and pricing details for the storage configuration." />
</Frame>

Step 2 — Open the Pub/Sub topic and view metrics
Open the topic you created earlier (`kodekloud-demo-topic`). The topic details page shows helpful monitoring metrics (published message count, publish requests, throughput) and export options (BigQuery, Cloud Storage).

<Frame>
  <img alt="A Google Cloud Console Pub/Sub topic details page for &#x22;kodekloud-demo-topic.&#x22; It shows export options to BigQuery and Cloud Storage and metrics panels (published message count, publish requests)." />
</Frame>

Step 3 — Create a subscription that writes to Cloud Storage
Create a subscription that delivers messages from the topic into your Cloud Storage bucket:

1. Go to Pub/Sub → Subscriptions → Create subscription.
2. Enter a subscription ID (demo: `kodekloud-storage-sub`).
3. Select the topic `projects/<your-project>/topics/kodekloud-demo-topic`.
4. For Delivery type choose **Write to Cloud Storage**.
5. Browse and select the bucket `kodekloud-pubsub-bucket`.
6. Choose file format: `Avro` or `JSON` (demo uses `JSON`).
7. Configure file batching (how frequently Pub/Sub writes files). Demo uses a 1 minute batch interval.

When "Write to Cloud Storage" is selected, Pub/Sub needs permission to create objects in the bucket. The Console will detect missing permissions and offer a one-click option to set them.

<Frame>
  <img alt="Screenshot of the Google Cloud Console Pub/Sub &#x22;Create subscription&#x22; page showing a Subscription ID set to &#x22;kodekloud-storage-sub&#x22; and a topic selection dropdown listing projects/kodekloud-gcp-training/topics/kodekloud-demo-topic. The message retention duration settings and delivery options are visible below." />
</Frame>

<Callout icon="lightbulb">
  Pub/Sub requires permission to write objects into the destination bucket (typically the Pub/Sub service account needs Object Creator and Object Viewer roles). The Console can auto-assign these when you click "Set permission" during subscription creation.
</Callout>

Finalize the subscription creation. With a 1 minute batching interval, Pub/Sub will write files to the bucket approximately once per minute (subject to batching thresholds).

<Frame>
  <img alt="A screenshot of the Google Cloud Console “Create subscription” screen for Pub/Sub, with the &#x22;Write to Cloud Storage&#x22; delivery option selected and a bucket named kodekloud-pubsub-bucket. A right-side panel prompts assigning Reader and Creator roles so Pub/Sub can write to the destination bucket." />
</Frame>

Step 4 — Publish messages and verify Cloud Storage objects
Publish messages to the topic to trigger the delivery. You can use a small publish script from Cloud Shell. Example output from a Cloud Shell publish run:

```bash theme={null}
