# CSV
import pandas as pd
df = pd.read_csv("s3://bucket/data.csv")

# Parquet
df = pd.read_parquet("s3://bucket/data.parquet")

# HDF5
import h5py
with h5py.File("data.h5", "r") as f:
    arr = f["/dataset"][...]
```

<Frame>
  <img alt="The image is a table comparing tabular data formats: CSV, Parquet, and HSF5, detailing their respective use cases and notes. It highlights CSV for structured data, Parquet for big data and cloud ML, and HSF5 for large numerical datasets." />
</Frame>

## Text and NLP formats

* TXT: Plain text for raw corpora. Universal and simple; requires preprocessing (tokenization, normalization).
* JSON / JSONL: Structured text for annotations and nested metadata. `JSONL` (one JSON object per line) is common for scalable ingestion and streaming.
* Recommended patterns:
  * Use `JSONL` for document-level metadata and per-example labels.
  * Use compressed archives (e.g., `.gz`) when transporting large text corpora.

## Binary ML-native formats

These formats optimize sequential reads, sharding, and integration with training frameworks:

| Format        |           Typical frameworks | Use case                                                             |
| ------------- | ---------------------------: | -------------------------------------------------------------------- |
| TFRecord      |                   TensorFlow | Binary, protobuf-backed; good for sharding and fast streaming reads  |
| RecordIO      | MXNet, some legacy pipelines | Sequential binary records optimized for streaming                    |
| Pickle (.pkl) |             Python ecosystem | Serializes Python objects and models; convenient for local artifacts |

<Callout icon="warning">
  Pickles can execute arbitrary code on load. Do not unpickle data from untrusted sources. Prefer language-agnostic formats (TFRecord, Parquet, JSON) for shared datasets.
</Callout>

<Frame>
  <img alt="The image is a table comparing binary formats, highlighting the use cases, key features, and common tools for TFRecord, RecordIO, and Pickle (.pkl)." />
</Frame>

## Image, audio, and video formats

Media formats depend on fidelity, compression needs, and downstream processing tools:

* Images:
  * JPEG — lossy, widely used for image-model training where compression is acceptable.
  * PNG — lossless, useful for images requiring pixel-perfect fidelity.
* Audio:
  * WAV — uncompressed, high quality; larger storage footprint.
  * MP3 — compressed, lower size; good for distribution.
  * FLAC — lossless compressed audio; good for speech datasets.
* Video:
  * MP4 (H.264) — widely supported, good compression/quality balance.
  * AVI — less compressed, larger files; sometimes used when minimal codec transformations are desired.

Quick reference for preprocessing libraries:

* Images: PIL / OpenCV / torchvision
* Audio: librosa / torchaudio / pydub
* Video: ffmpeg / OpenCV

<Frame>
  <img alt="The image is a table summarizing different media formats (JPEG, PNG, WAV, MP3, MP4, AVI), their types, use cases, notes, and popular tools associated with each format." />
</Frame>

## AWS storage and analytics: format recommendations

AWS supports many formats; choose based on workload patterns (scan-heavy analytics vs. sequential training reads):

| AWS Service              |                          Recommended formats | Rationale                                    |
| ------------------------ | -------------------------------------------: | -------------------------------------------- |
| Amazon S3                | Parquet, TFRecord, CSV, images, audio, video | Object store for raw and processed artifacts |
| Amazon Athena / AWS Glue |                      Parquet, ORC, JSON, CSV | Querying and ETL for analytics               |
| Amazon Redshift          |                  Parquet, ORC (via Spectrum) | Columnar formats for fast analytic queries   |
| AWS Lake Formation       |                           Parquet, ORC, JSON | Centralized governance for data lakes on S3  |

* Amazon S3 is the foundational storage layer for many pipelines. Use lifecycle policies and compression to control cost.
* Consider partitioning and file sizing (e.g., Parquet row groups \~128 MB) to optimize query and read performance.

<Frame>
  <img alt="The image is a table showing supported data formats for various AWS services like Amazon S3, Amazon Athena, Amazon Redshift, and AWS Lake Formation. Each service lists the specific formats it supports, such as CSV, JSON, Parquet, and ORC." />
</Frame>

## Processing and streaming on AWS

Match processing tools to data format and latency requirements:

* AWS Glue: Serverless ETL; supports `CSV`, `JSON`, `Parquet`, `Avro`, and `ORC`. Good for schema discovery and format conversions.
  * Use Glue jobs or Glue Studio for converting CSV/JSON to Parquet for analytics.
* Amazon EMR (Spark/Hadoop): Read/write Parquet, ORC, Avro, sequence files. Ideal for large-scale transformations and feature engineering.
* Amazon Kinesis: Ingest streaming events (often JSON or binary protobufs); used for near-real-time use cases.
* AWS Lambda: Receives JSON payloads (and base64-encoded binary data). Suitable for lightweight transformations and event-driven processing.

Best practices:

* For streaming ingestion, keep messages small and schema-stable (e.g., Avro/Protobuf).
* Convert raw event streams to columnar formats in downstream storage for efficient analytics.

<Frame>
  <img alt="The image is a table listing AWS services and their supported data formats for data processing and streaming, including AWS Glue, AWS EMR, Amazon Kinesis, and AWS Lambda with formats like CSV, JSON, and AVRO." />
</Frame>

## ML services and specialized formats

Common AWS ML services and their preferred input types:

* Amazon SageMaker: Supports CSV, Parquet, TFRecord, images, audio, and pickled artifacts for training and hosting. Use SageMaker processing jobs to convert formats at scale.
* Amazon Transcribe: Accepts WAV, MP3, FLAC, and MP4 for speech-to-text.
* Amazon Rekognition: Works with standard image and video formats (JPEG, PNG, MP4) for computer vision tasks.

When designing ML pipelines on AWS:

* Use columnar compressed formats (Parquet/ORC) for analytics and feature stores.
* Use binary ML-native formats (TFRecord/RecordIO) to maximize throughput for distributed training.
* Keep raw media in their native formats (JPEG/WAV/MP4) and extract features or convert to optimized formats only when necessary.

## Summary checklist

* Use Parquet/ORC for analytics and feature engineering—columnar layout reduces I/O and improves query performance.
* Use TFRecord/RecordIO for high-throughput, sharded training pipelines.
* Keep media in standard containers (JPEG/PNG, WAV/FLAC, MP4) and preprocess with specialized libraries.
* Avoid insecure serialization formats (untrusted pickles) when sharing datasets across teams or services.
* Optimize file sizing, partitioning, and compression to balance read performance and storage cost.

## Links and references

* [Amazon S3](https://aws.amazon.com/s3/)
* [Amazon Athena](https://aws.amazon.com/athena/)
* [Amazon Redshift](https://aws.amazon.com/redshift/)
* [AWS Glue](https://aws.amazon.com/glue/)
* [Amazon EMR](https://aws.amazon.com/emr/)
* [Amazon Kinesis](https://aws.amazon.com/kinesis/)
* [Amazon SageMaker](https://aws.amazon.com/sagemaker/)
* [Amazon Transcribe](https://aws.amazon.com/transcribe/)
* [Amazon Rekognition](https://aws.amazon.com/rekognition/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/59a5c701-2300-4810-b1ca-1ec24cfd4ec0" />
</CardGroup>


# Data Labeling with SageMaker Ground Truth

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Data-Labeling-with-SageMaker-Ground-Truth/page

Overview of Amazon SageMaker Ground Truth for scalable data labeling using auto-labeling, active learning, human review, workforce options, and AWS integrations to produce high quality training datasets.

High-quality labeled data is the foundation of successful supervised machine learning. Without reliable labels, models lack ground truth to learn from, which leads to poor, biased, or unpredictable predictions. Labeling converts raw inputs—pixels, words, or audio—into structured examples a model can learn from, such as:

* marking objects in images,
* tagging sentiment or entities in text, and
* transcribing and timestamping audio.

A well-labeled dataset enables models to generalize accurately to new inputs.

<Frame>
  <img alt="The image illustrates the importance of data labeling, showing a machine learning model being trained on raw data leading to poor predictions due to a lack of guidance." />
</Frame>

Labeling provides the structure and context raw data lacks. When examples are consistently and accurately annotated, models can learn meaningful patterns and produce reliable predictions.

<Frame>
  <img alt="The image illustrates the importance of data labeling in machine learning, showing a process flow from raw data to labeled data, through ML model training, resulting in accurate predictions." />
</Frame>

## What is SageMaker Ground Truth?

Amazon SageMaker Ground Truth is a managed data-labeling service that accelerates dataset creation by combining machine learning–assisted auto-labeling with human review workflows. Ground Truth stores both inputs and labeled outputs in Amazon S3 and provides mechanisms to reduce cost and improve labeling quality through automation and built-in quality controls.

Typical Ground Truth flow:

1. Raw data is ingested from Amazon S3.
2. Auto-labeling (model-in-the-loop) labels high-confidence items.
3. Low-confidence or ambiguous items are routed to human workers for review.
4. Consolidated, quality-checked labels are written back to S3 for model training.

Ground Truth’s active learning approach helps reduce labeling costs by prioritizing human effort where it is most needed.

<Frame>
  <img alt="The image illustrates the workflow of Amazon SageMaker Ground Truth, showing the process from input data to labeled datasets, using human labelers and auto-labeling ML, leading to model training in SageMaker." />
</Frame>

## Human workforces: options and when to use them

Choose the appropriate workforce based on scale, sensitivity, and label quality requirements. Ground Truth supports three workforce types:

| Workforce Type                                          |                                      Best For | Notes / Considerations                                                                                                                 |
| ------------------------------------------------------- | --------------------------------------------: | -------------------------------------------------------------------------------------------------------------------------------------- |
| [Amazon Mechanical Turk](https://aws.amazon.com/mturk/) |         High-scale, lower-cost labeling tasks | Large crowdsource pool; suitable for non-sensitive data and simple labeling tasks.                                                     |
| Vendor workforces                                       | Managed vendor labeling for scale and quality | Third-party vendors provide managed teams and SLAs—useful when you need consistent labeling quality without building an internal team. |
| Private teams                                           |                 Sensitive or proprietary data | Use internal employees for highest control over data privacy and domain expertise.                                                     |

<Frame>
  <img alt="The image illustrates different types of workforces—Amazon Mechanical Turk, Vendor Workforce, and Private Team—used in the Amazon SageMaker Ground Truth for human labeling." />
</Frame>

## Key features and capabilities

Ground Truth provides a suite of features to scale labeling and maintain high quality:

* Active learning and model-in-the-loop auto-labeling to reduce manual effort.
* Multiple workforce options to balance cost, scale, and data sensitivity.
* Secure integration with Amazon S3 for storage, access control, and auditability.
* Scalability to handle datasets with millions of records.
* Built-in quality controls and metrics (annotation consolidation, worker performance tracking, and consensus algorithms).

## Supported labeling tasks

Ground Truth supports common labeling modalities across image, text, and video. Use this table to quickly identify task types and examples.

| Modality | Task examples                                                                         |
| -------- | ------------------------------------------------------------------------------------- |
| Images   | classification, object detection (bounding boxes), semantic and instance segmentation |
| Text     | classification, sentiment analysis, named-entity recognition (NER)                    |
| Video    | frame-level labeling, activity detection, object tracking, temporal segmentation      |

The end-to-end workflow ingests raw data, applies automated labeling where possible, routes uncertain items to humans, performs quality consolidation, and exports the final labels back to Amazon S3 for downstream training.

<Frame>
  <img alt="The image is a workflow diagram titled &#x22;Ground Truth Workflow Overview&#x22; depicting the process of input data being processed by Amazon SageMaker Ground Truth, with low-confidence outputs leading to human reviews, and resulting translations stored in Amazon S3." />
</Frame>

## Active learning and cost reduction

Ground Truth’s active learning loop is a practical way to reduce manual labeling overhead:

* The system trains or uses an existing model (auto-labeler) to label examples it is confident about.
* Low-confidence or ambiguous examples are routed to human labelers.
* Human-reviewed labels are fed back to improve the auto-labeler, increasing automation and lowering costs over time.

<Callout icon="lightbulb">
  Ground Truth’s active learning and auto-labeling significantly reduce labeling costs and accelerate dataset creation by prioritizing human effort for the most uncertain examples.
</Callout>

## Integrations and downstream use

Ground Truth integrates with core AWS ML services to complete the labeling-to-training pipeline:

* Amazon SageMaker — train and deploy models using the labeled datasets.
* Amazon Rekognition — leverage prebuilt vision capabilities or seed auto-labelers.
* Amazon Comprehend — use NLP services for preprocessing or transfer learning for text tasks.
* Amazon Translate — assist multilingual labeling workflows.
* Amazon S3 — secure storage for raw inputs, annotations, and outputs.

## Summary

SageMaker Ground Truth streamlines the labeling pipeline by combining automation, active learning, and human-in-the-loop reviews. It supports multiple workforce options, a broad set of labeling tasks, and tight AWS integrations—helping teams produce accurate, scalable, and cost-effective labeled datasets for training robust ML models.

Further reading and references:

* [Amazon SageMaker Ground Truth](https://aws.amazon.com/sagemaker/ground-truth/)
* [Amazon S3](https://aws.amazon.com/s3/)
* [Amazon Mechanical Turk](https://aws.amazon.com/mturk/)
* [Amazon Rekognition](https://aws.amazon.com/rekognition/)
* [Amazon Comprehend](https://aws.amazon.com/comprehend/)
* [Amazon Translate](https://aws.amazon.com/translate/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/b02b5604-f189-4d75-acd3-4aca7dc0e582" />
</CardGroup>
