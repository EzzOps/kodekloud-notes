# Data Loss Prevention DLP API

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Security-Encryption/Data-Loss-Prevention-DLP-API/page

Overview of Google Cloud Data Loss Prevention API for discovering, classifying, and de‑identifying sensitive data across storage, databases, logs, and images with monitoring and integration best practices.

Hello everyone — welcome back.

This article explains Google Cloud's Data Loss Prevention (DLP) API and why it matters for data engineers and security teams.

As data engineers we routinely handle sensitive information such as credit card numbers, personal IDs, addresses, and health records. If any of that information leaks, it can cause serious financial and legal problems for an organization. Google Cloud's DLP API helps you locate, classify, and protect sensitive data across databases, storage, logs, text, and images.

Why use the DLP API

* Discover: Find sensitive data inside CSV files, BigQuery tables, Cloud Storage objects, logs, or user input.
* Classify: Identify the type of data — e.g., email address, passport ID, phone number, or medical info.
* De-identify: Mask, redact, tokenize, or cryptographically transform data so the original values are not exposed.
* Monitor and audit: Keep track of scans, transformations, and re-identification events for compliance.

Think of the DLP API as a guard that says, “That looks private — let me hide it before it can be misused.”

How DLP works

* Inspect: Analyze content (text, images, structured data) against built-in detectors (150+ predefined info types) and custom detectors.
* Classify: Return findings annotated with the info type, likelihood, and location (offsets or table/column references).
* De-identify: Apply transformations — e.g., replace characters with a mask, tokenize values, or encrypt using Cloud KMS.
* Re-identify: When authorized, reverse a reversible transform (for example, decrypt or detokenize) under strict access controls.
* Asynchronous scanning: For large datasets, create long-running background jobs that persist results and logs.

Core DLP API methods
The DLP API exposes a few primary calls you’ll use when integrating it into pipelines. Below is a concise reference.

| Method                    | Purpose                                               | Typical use case                                       |
| ------------------------- | ----------------------------------------------------- | ------------------------------------------------------ |
| `content.inspect`         | Scan text, images, or files for sensitive information | Inspecting logs before exporting them to BigQuery      |
| `content.deidentify`      | Transform findings (mask, redact, tokenize, encrypt)  | Hiding all but the last four digits of a credit card   |
| `content.reidentify`      | Reverse a prior de-identification (when authorized)   | Authorized forensic or fraud investigations            |
| `projects.dlpJobs.create` | Create long-running DLP jobs for large datasets       | Full scans of BigQuery tables or Cloud Storage buckets |

Example: primary method names

```text theme={null}
content.inspect()
content.deidentify()
content.reidentify()
projects.dlpJobs.create()
```

Quick example: mask credit card numbers (REST request snippet)

```json theme={null}
{
  "inspectConfig": {
    "infoTypes": [{"name": "CREDIT_CARD_NUMBER"}],
    "minLikelihood": "POSSIBLE"
  },
  "deidentifyConfig": {
    "infoTypeTransformations": {
      "transformations": [{
        "primitiveTransformation": {
          "maskConfig": {"maskingCharacter": "*", "numberToMask": 12}
        }
      }]
    }
  },
  "item": {"value": "My credit card number is 4111-1111-1111-1111"}
}
```

This request instructs DLP to locate the credit card number and mask it, leaving only the last four characters visible.

Best practices

* Use DLP templates (inspect and de-identify templates) to keep detection and masking rules consistent across projects and teams.
* Apply least-privilege access for any re-identification operations; require strong IAM roles and keep an audit trail when original values are restored.
* Prefer `dlpJobs.create` for large, asynchronous scans (BigQuery, Cloud Storage) so scans run in the background without blocking processing pipelines.
* Combine detectors: use both built-in and custom regex detectors for domain-specific identifiers.
* Monitor and log DLP jobs, findings, and re-identification events for compliance and incident response.

| Recommendation    | Why it matters                                    |
| ----------------- | ------------------------------------------------- |
| Use templates     | Centralize policies and simplify updates          |
| Least privilege   | Minimize risk when re-identifying data            |
| Asynchronous jobs | Scale to large datasets without impacting latency |
| Audit trails      | Demonstrate compliance and detect misuse          |

<Callout icon="lightbulb">
  Tip: Create reusable DLP inspect and de-identify templates. These templates ensure consistent policy enforcement across services and make it easier to update masking rules centrally.
</Callout>

<Callout icon="warning">
  Warning: Re-identification restores sensitive values. Restrict who can call `content.reidentify` and require logging and approvals. Treat re-identification as a high-risk operation in your security and compliance processes.
</Callout>

Integrations and common workflows

* BigQuery: Scan tables with `dlpJobs.create` for scheduled or one-off discovery jobs. Use de-identification to create masked export tables.
* Cloud Storage: Scan objects (CSV, JSON, text) and optionally redact or move sensitive copies to a protected bucket.
* Logging/Streaming: Inspect logs or streaming data in real-time before they are forwarded to sinks (e.g., Pub/Sub -> BigQuery).
* Images: Use image inspection to detect text-based PII inside images (OCR + info type detectors).
* Workflows: Combine DLP with Cloud Functions or Dataflow to automate inspection and transformation as part of ETL pipelines.

Additional links and references

* [Google Cloud DLP Documentation](https://cloud.google.com/dlp)
* [BigQuery Documentation](https://cloud.google.com/bigquery)
* [Cloud Storage Documentation](https://cloud.google.com/storage)
* [Cloud KMS Documentation](https://cloud.google.com/kms)

Thanks for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/82c9cad5-507a-414f-a878-0916d4d45978/lesson/273fd747-0b5c-45ba-a475-583188911665" />
</CardGroup>
