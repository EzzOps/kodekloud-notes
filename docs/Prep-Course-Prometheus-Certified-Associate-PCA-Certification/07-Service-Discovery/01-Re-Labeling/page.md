# Re Labeling

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Service-Discovery/Re-Labeling/page

Guide to Prometheus relabeling for filtering, renaming, and normalizing discovery and metric labels pre and post scrape, including common actions, examples, and debugging tips.

In this lesson we cover Prometheus relabeling: how to rewrite label sets for discovered targets and scraped metrics. Relabeling is essential for classifying, filtering, and normalizing targets and metrics before ingestion or during metric processing.

Common use cases

* Filter discovered targets you don't want to scrape (e.g., non-production instances).
* Rename or extract parts of labels (for example, remove ports from addresses).
* Drop unwanted labels or specific metrics to reduce cardinality.

Two relabeling phases

| Phase       | Where it runs                                           | Available labels                                                    | Typical use cases                                                                                             |
| ----------- | ------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Pre-scrape  | `relabel_configs` under a `scrape_configs` entry        | Service discovery metadata (e.g., `__meta_ec2_*`) and target labels | Filter discovered targets, map discovery metadata into target labels, normalize target labels before scraping |
| Post-scrape | `metric_relabel_configs` under a `scrape_configs` entry | Scraped metrics and their labels (including `__name__`)             | Drop or rename metrics, remove metric labels, create metric-level labels                                      |

Example showing both sections (placeholders wrapped in backticks to avoid MDX/JSX parsing):

```yaml theme={null}
scrape_configs:
  - job_name: ec2
    relabel_configs:
      # relabeling before scraping (has access to discovery labels)
    metric_relabel_configs:
      # relabeling after scraping (has access to scraped metrics)
    ec2_sd_configs:
      - region: `<region>`
        access_key: `<access key>`
        secret_key: `<secret key>`
```

Service discovery (for example, Amazon EC2) exposes many `__meta_*` labels. Example:

```text theme={null}
__meta_ec2_tag_env = dev | prod
```

These `__meta_*` labels are available during pre-scrape relabeling but are discarded after the relabeling pipeline unless you explicitly map them to target labels.

If you inspect scraped series you might see entries such as:

```text theme={null}
up{instance="172.31.1.156:80", job="ec2"}
up{instance="172.31.1.34:80", job="ec2"}
```

The `instance` and `job` labels are examples of target labels that will appear on scraped time series. Discovery-specific labels beginning with `__` are metadata only and will not be preserved unless mapped.

> **warning** Relabeling rules are evaluated sequentially. A common pitfall is using `action: keep` without care — any target not matched by a `keep` rule is implicitly dropped. Validate your rules to avoid unintentionally excluding targets.

***

## Basic relabeling (pre-scrape)

A relabeling rule typically reads one or more `source_labels`, joins them (with a separator), applies a `regex`, and performs an `action` such as `keep`, `drop`, or `replace`.

Example: keep only targets discovered with `env=prod`:

```yaml theme={null}
scrape_configs:
  - job_name: example
    relabel_configs:
      - source_labels: [__meta_ec2_tag_env]
        regex: prod
        action: keep
```

Fields explained

* `source_labels`: array of label names to concatenate and match.
* `regex`: applied to the joined `source_labels` values.
* `action`: the operation to perform when the regex matches.

Action semantics (common)

| Action    | Effect                                                                                   | Example use                           |
| --------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| `keep`    | Retains targets that match; non-matching targets are dropped immediately                 | Keep production targets               |
| `drop`    | Drops targets that match                                                                 | Exclude `env=dev` hosts from scraping |
| `replace` | Set or overwrite a `target_label` with a `replacement` (optionally using capture groups) | Extract IP from `__address__`         |

Example: drop any target tagged with `env=dev`:

```yaml theme={null}
scrape_configs:
  - job_name: example
    relabel_configs:
      - source_labels: [__meta_ec2_tag_env]
        regex: dev
        action: drop
```

### Matching multiple source labels

When multiple `source_labels` are specified, Prometheus concatenates their values using a delimiter (default `;`) before applying `regex`.

Example: keep only targets where `env=dev` and `team=marketing`:

```yaml theme={null}
scrape_configs:
  - job_name: example
    relabel_configs:
      - source_labels: [env, team]
        regex: dev;marketing
        action: keep
```

Change the join delimiter with `separator`:

```yaml theme={null}
scrape_configs:
  - job_name: example
    relabel_configs:
      - source_labels: [env, team]
        regex: dev-marketing
        action: keep
        separator: "-"
```

***

## Turning discovery metadata into target labels

Discovery labels that begin with `__` (for example, `__meta_ec2_*`) are metadata and are discarded after relabeling unless you explicitly map them to target labels.

Example: extract the IP from `__address__` (e.g., `172.31.1.156:80`) and save it to a target label named `ip`:

```yaml theme={null}
scrape_configs:
  - job_name: example
    relabel_configs:
      - source_labels: [__address__]
        regex: '(.*):.*'
        target_label: ip
        action: replace
        replacement: '$1'
```

Explanation:

* `regex` captures the portion before the colon in group 1.
* `replacement: '$1'` places the captured value into the new `ip` label.

You can also drop or retain labels by name using `labeldrop` and `labelkeep`.

Example: drop a discovery label named `__meta_ec2_owner_id`:

```yaml theme={null}
scrape_configs:
  - job_name: example
    relabel_configs:
      - regex: __meta_ec2_owner_id
        action: labeldrop
```

Example: keep only `instance` and `job` labels and drop all others:

```yaml theme={null}
scrape_configs:
  - job_name: example
    relabel_configs:
      - regex: instance|job
        action: labelkeep
```

<Frame>
  <img alt="The image shows a table of discovered labels and target labels for an EC2 instance, with a note explaining that labels beginning with &#x22;__&#x22; will be discarded after re-labeling." />
</Frame>

### Mapping discovery keys into target label names: `labelmap`

`labelmap` renames label keys (not values). A common use is to convert discovery keys like `__meta_ec2_AMI` into readable target labels like `ec2_AMI`.

Example: map all `__meta_ec2_*` keys to `ec2_*` target labels:

```yaml theme={null}
scrape_configs:
  - job_name: example
    relabel_configs:
      - regex: '__meta_ec2_(.*)'
        action: labelmap
        replacement: 'ec2_$1'
```

This preserves the values but makes the keys normal target label names visible on scraped series.

***

## Metric relabeling (post-scrape)

`metric_relabel_configs` runs after a scrape and operates on each metric and its labels. The fields are the same as `relabel_configs`, but now `__name__` refers to the metric name.

Example: drop an entire metric called `http_errors_total`:

```yaml theme={null}
scrape_configs:
  - job_name: example
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: http_errors_total
        action: drop
```

Rename a metric (change the metric name):

```yaml theme={null}
scrape_configs:
  - job_name: example
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: http_errors_total
        action: replace
        target_label: __name__
        replacement: http_failures_total
```

Drop a metric label (remove `code` from all metrics):

```yaml theme={null}
scrape_configs:
  - job_name: example
    metric_relabel_configs:
      - regex: code
        action: labeldrop
```

Create a new metric label by transforming an existing label. Example: turn `path="/api/v1"` into `endpoint="api/v1"` by stripping the leading slash:

```yaml theme={null}
scrape_configs:
  - job_name: example
    metric_relabel_configs:
      - source_labels: [path]
        regex: '/(.*)'
        action: replace
        target_label: endpoint
        replacement: '$1'
```

Notes:

* Use capture groups `(...)` in `regex` and reference them as `$1`, `$2`, etc. in `replacement`.
* `relabel_configs` has access to service-discovery metadata (the `__meta_*` labels); `metric_relabel_configs` has access to scraped metric names and labels (`__name__` and metric labels).

> **lightbulb** All relabeling rules are applied in order. Test and verify your relabeling pipeline in a staging environment, and use the Prometheus web UI service discovery pages and target pages to inspect label lifecycles and debug rules.

***

## Quick reference: common actions and examples

| Action      | Purpose                                         | Example snippet                                                         |       |
| ----------- | ----------------------------------------------- | ----------------------------------------------------------------------- | ----- |
| `keep`      | Only retain targets/metrics that match          | `action: keep`                                                          |       |
| `drop`      | Exclude targets/metrics that match              | `action: drop`                                                          |       |
| `replace`   | Set or overwrite a label value (or metric name) | `action: replace`, `target_label: ip`, `replacement: '$1'`              |       |
| `labeldrop` | Remove label(s) by regex                        | `action: labeldrop`, `regex: code`                                      |       |
| `labelkeep` | Keep only matching label(s)                     | `action: labelkeep`, \`regex: instance                                  | job\` |
| `labelmap`  | Rename label keys using regex/replacement       | `action: labelmap`, `regex: '__meta_ec2_(.*)'`, `replacement: 'ec2_$1'` |       |

***

## Links and references

* [Prometheus relabeling docs](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config)
* [Prometheus metric\_relabel\_configs docs](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#metric_relabel_configs)
* [Kubernetes Service Discovery](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Amazon EC2 documentation](https://docs.aws.amazon.com/ec2/)

Use these references to deepen your understanding and validate edge cases for complex relabeling pipelines.

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/20a3a57d-ee2d-4096-888e-de1166cf7e3a/lesson/d64a976c-94eb-40e4-94bf-8b9a30f4867a)
