# Data Formats for Machine Learning

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Data-Formats-for-Machine-Learning/page

Practical overview of data formats for machine learning pipelines with format recommendations for analytics, training, media, and AWS services

Machine learning pipelines are only as good as the data feeding them. Data can appear in many formats, and choosing the right one at each stage (ingest, storage, preprocessing, training, serving) directly affects training throughput, storage cost, query latency, and integration with analytics or ML services.

<Frame>
  <img alt="The image illustrates the importance of data format in machine learning, showing that machine learning relies on data, which is shown in a specific format." />
</Frame>

Selecting the optimal format reduces I/O overhead, improves compatibility with engines (Spark, Athena, Redshift), and lowers compute and storage bills—especially at scale.

<Frame>
  <img alt="The image visually explains why data format matters, highlighting its impact on performance, stage efficiency, and compatibility. It includes icons for each aspect and emphasizes that choosing the right format improves speed, cost, and compatibility." />
</Frame>

Below is a concise, practical overview of commonly used ML data formats, grouped by data type and use case. Use this as a quick reference when designing pipelines for analytics, feature stores, distributed training, and model serving.

<Callout icon="lightbulb">
  Match format to pipeline stage: use columnar compressed formats (Parquet/ORC) for analytics and feature stores, binary ML-native formats (TFRecord/RecordIO) for high-throughput training, and media-specific formats (JPEG/MP4/WAV) for raw multimedia inputs.
</Callout>

## Tabular data formats

Common choices for structured/tabular data, ranked by typical usage:

| Format  |                                                      Best for | Notes                                                                        |
| ------- | ------------------------------------------------------------: | ---------------------------------------------------------------------------- |
| CSV     |     Small datasets, quick inspection, spreadsheet interchange | Human-readable but lacks schema, inefficient for large-scale analytics       |
| Parquet |             Big data analytics, feature stores, query engines | Columnar, compressed, supports predicate pushdown (good for Athena/Redshift) |
| HDF5    | Large numerical arrays, hierarchical datasets, tensor storage | Excellent for large tensor datasets and model checkpoints in deep learning   |

Example: reading these formats with Python:

```python theme={null}
