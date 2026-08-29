# TYPE metric_one counter
metric_one{label="val1"} 11
# TYPE metric_two gauge
# HELP metric_two Just an example.
metric_two 100
EOF
```

Push another group (`job=archive`, `app=web`):

```bash theme={null}
cat <<EOF | curl --data-binary @- http://localhost:9091/metrics/job/archive/app/web
# TYPE metric_one counter
metric_one{label="val1"} 22
# TYPE metric_two gauge
# HELP metric_two Just an example.
metric_two 200
# TYPE metric_three gauge
metric_three 300
EOF
```

Inspect metrics filtered for the `archive` job:

```bash theme={null}
curl http://localhost:9091/metrics | grep archive -A2 -B1
```

You will see metrics grouped by the path labels, for example:

```prometheus theme={null}
metric_one{db="mysql",job="archive",label="val1"} 11
metric_two{db="mysql",job="archive"} 100

metric_one{app="web",job="archive",label="val1"} 22
metric_two{app="web",job="archive"} 200
metric_three{app="web",job="archive"} 300
```

## POST vs PUT vs DELETE — semantics and examples

The HTTP method you use affects how metrics are updated in the target group.

| Method | Semantics                                                                                                                                                          | Common curl usage                                                               |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| POST   | Replace only metrics in the group that have the same metric name as those in the POST payload; other metrics in the group remain unchanged. Also adds new metrics. | `curl --data-binary @- http://localhost:9091/metrics/job/<job>/<labels>`        |
| PUT    | Replace the entire group at the target URL. Any previously stored metrics in that group are deleted and replaced by the PUT payload (idempotent).                  | `curl -X PUT --data-binary @- http://localhost:9091/metrics/job/<job>/<labels>` |
| DELETE | Delete the entire group at the target URL.                                                                                                                         | `curl -X DELETE http://localhost:9091/metrics/job/<job>/<labels>`               |

Note: `curl --data-binary @-` sends a POST by default. Use `-X PUT` or `-X DELETE` to get PUT or DELETE semantics.

### POST example

POST a new value for `metric_one` (replaces only that metric in the `archive/app=web` group):

```bash theme={null}
cat <<EOF | curl --data-binary @- http://localhost:9091/metrics/job/archive/app/web
# TYPE metric_one counter
metric_one{label="val1"} 44
EOF
```

Resulting group contents:

```prometheus theme={null}
metric_one{app="web",job="archive",label="val1"} 44
metric_two{app="web",job="archive"} 200
metric_three{app="web",job="archive"} 300
```

### PUT example

Replace the entire `archive/app=web` group with only `metric_one`:

```bash theme={null}
cat <<EOF | curl -X PUT --data-binary @- http://localhost:9091/metrics/job/archive/app/web
# TYPE metric_one counter
metric_one{label="val1"} 44
EOF
```

After this PUT, the `archive/app=web` group will contain only:

```Prometheus theme={null}
metric_one{app="web",job="archive",label="val1"} 44
```

All previously stored metrics in that group are removed.

### DELETE example

Delete the `archive/app=web` group entirely:

```bash theme={null}
curl -X DELETE http://localhost:9091/metrics/job/archive/app/web
```

After the DELETE, only metrics from other groups (for example, `db=mysql`) remain.

## Recap

* The grouping key is encoded in the path: `job` plus any additional label/value path segments.
* Labels in the path are appended to every pushed metric.
* Use POST to update specific metric names within a group (non-destructive for other metrics in the group).
* Use PUT to replace the entire group.
* Use DELETE to remove the entire group.
* URL-encode path segments that include special characters.

> **lightbulb** When using `curl --data-binary @-`, curl sends a POST request by default. Use `-X PUT` or `-X DELETE` when you want the explicit PUT or DELETE semantics.

## Links and References

* Prometheus Pushgateway (GitHub): [https://github.com/prometheus/pushgateway](https://github.com/prometheus/pushgateway)
* Prometheus exposition formats: [https://prometheus.io/docs/instrumenting/exposition\_formats/](https://prometheus.io/docs/instrumenting/exposition_formats/)
* Prometheus client libraries: [https://prometheus.io/docs/instrumenting/clientlibs/](https://prometheus.io/docs/instrumenting/clientlibs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/18b41166-411a-42a8-91c2-18a5b49bc189/lesson/2ea926a1-5349-4263-8205-7364ecbb84a1)


# AWS

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Service-Discovery/AWS/page

Guide to configuring Prometheus EC2 service discovery, IAM setup, metadata labels, and validation to automatically discover and scrape metrics from AWS EC2 instances

Cloud environments are dynamic: instances are created and terminated continuously (especially with auto-scaling). Prometheus’ EC2 service discovery lets your Prometheus server automatically discover and scrape metrics from EC2 instances in a given AWS region — avoiding manual target management.

This guide explains the required IAM setup, how to configure `prometheus.yml` for EC2 service discovery, what metadata is exposed for discovered targets, and how to validate the configuration in the Prometheus UI.

> **lightbulb** Use an IAM user with the minimum permission set required: the AWS-managed policy **AmazonEC2ReadOnlyAccess**. For higher security, prefer using an instance role (EC2 IAM role) for Prometheus or an external secrets manager instead of hard-coding access keys in `prometheus.yml`.

## Prerequisites

* A Prometheus server with network reachability to the EC2 instances you want to scrape.
* An AWS account and permission to create IAM users/policies.
* Knowledge of the AWS region(s) you want to monitor (for example `us-east-1`).

## 1) Create an IAM user for Prometheus

Create a new IAM user that Prometheus will use for EC2 discovery. This user only needs programmatic access and the Amazon EC2 Read Only Access policy attached.

<Frame>
  <img alt="This image shows a screen from the AWS Management Console for adding a new user, where you can enter a username and select the AWS access type." />
</Frame>

* In the IAM console: Users → Create user.
* Select **Programmatic access** so you can obtain an Access Key ID and Secret Access Key.
* Attach the AWS managed policy **AmazonEC2ReadOnlyAccess**.

<Frame>
  <img alt="The image shows an AWS interface for adding a user, with options to set permissions, add the user to a group, or copy permissions from an existing user. There is also an option to set a permissions boundary." />
</Frame>

* Skip tags (optional), review, and create the user.

<Frame>
  <img alt="The image shows an AWS IAM console where a user is in the process of adding permissions by attaching existing policies. Several EC2-related AWS managed policies are listed for selection." />
</Frame>

* After creation, record the **Access Key ID** and **Secret Access Key**. You’ll need them for the Prometheus config.

<Frame>
  <img alt="The image shows a user creation confirmation screen in the AWS Management Console, indicating success with a user's access key ID and secret access key." />
</Frame>

> **warning** Do NOT commit AWS keys to version control. Prefer instance roles, environment variables, or a secrets manager (e.g., AWS Secrets Manager) for production deployments. Hard-coding keys in `prometheus.yml` is only acceptable for short-term testing.

## 2) Configure Prometheus for EC2 service discovery

Edit your Prometheus configuration file (usually `/etc/prometheus/prometheus.yml`) and add an EC2 scrape job under `scrape_configs`. The minimal `ec2_sd_configs` block requires:

* `region`: the AWS region to discover (e.g., `us-east-1`).
* `access_key`: the IAM user Access Key ID (or omit if using instance role / environment credentials).
* `secret_key`: the Secret Access Key (or omit if using instance role / environment credentials).

Example `prometheus.yml` (showing only relevant parts):

```yaml theme={null}
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
      - targets:
        - alertmanager:9093

rule_files:
  # - "first_rules.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node"
    static_configs:
      - targets: ["192.168.1.168:9100"]

  - job_name: "ec2"
    ec2_sd_configs:
      - region: us-east-1
        access_key: AKIAQS0UAYMSDJI177
        secret_key: G2y3/xjKr0m0sWmA0SWh/VCWCBr/ShmqMJHRJkoX1h
```

Notes:

* Replace `us-east-1`, `access_key`, and `secret_key` with your region and credentials.
* If Prometheus runs on an EC2 instance with an appropriate IAM role, omit `access_key`/`secret_key` entirely — the AWS SDK will use the instance role credentials automatically.

After saving changes, restart Prometheus:

```bash theme={null}
sudo systemctl restart prometheus
```

## 3) What metadata does EC2 SD provide?

Prometheus extracts many EC2 metadata fields as labels for each discovered target. These are available under Service Discovery in the Prometheus UI and can be used for relabeling or filtering.

Example discovered labels for an EC2 target:

```bash theme={null}
address="172.31.1.156:80"
meta_ec2_ami="arn:aws:ec2:us-east-1:123456789012:ami/abcde123"
meta_ec2_architecture="x86_64"
meta_ec2_availability_zone="us-east-1b"
meta_ec2_availability_zone_id="use1-az4"
meta_ec2_instance_id="i-0e23a196c0a198db"
meta_ec2_instance_state="running"
meta_ec2_instance_type="t2.micro"
meta_ec2_owner_id="604794731401"
meta_ec2_primary_subnet_id="subnet-0fde537cdc8041"
meta_ec2_private_dns_name="ip-172-31-1-156.ec2.internal"
meta_ec2_private_ip="172.31.1.156"
meta_ec2_public_dns_name="ec2-3-80-117-102.compute-1.amazonaws.com"
meta_ec2_public_ip="3.80.117.102"
meta_ec2_subnet_id="subnet-0fde537cdc8041"
meta_ec2_tag_instance="web"
meta_ec2_tag_id="vp-id:xyz123456"
metrics_path="/metrics"
scheme="http"
scrape_interval="15s"
scrape_timeout="10s"
job="EC2"
```

Table — Common `meta_ec2_*` labels and their meaning:

| Label                        | Meaning                                   | Example                        |
| ---------------------------- | ----------------------------------------- | ------------------------------ |
| `meta_ec2_instance_id`       | EC2 instance ID                           | `i-0e23a196c0a198db`           |
| `meta_ec2_private_ip`        | Instance private IP                       | `172.31.1.156`                 |
| `meta_ec2_public_ip`         | Instance public IP (if assigned)          | `3.80.117.102`                 |
| `meta_ec2_instance_type`     | Instance type                             | `t2.micro`                     |
| `meta_ec2_availability_zone` | AZ (e.g., us-east-1b)                     | `us-east-1b`                   |
| `meta_ec2_ami`               | AMI ARN                                   | `arn:aws:ec2:...:ami/abcde123` |
| `meta_ec2_tag_<key>`         | Tag value for tag key `<key>`             | `meta_ec2_tag_instance="web"`  |
| `address`                    | The target address Prometheus will scrape | `172.31.1.156:80`              |

> **lightbulb** By default Prometheus uses the instance's private IP for the `instance` label and for scraping (`address`), because it assumes Prometheus runs near (in the same network/VPC as) the targets. If Prometheus runs outside the VPC and you need to use the public IP, use relabeling to map `meta_ec2_public_ip` into the `__address__`/`instance` labels — or run Prometheus within the same VPC.

## 4) Validate in the Prometheus UI

1. Open your Prometheus server web UI (e.g., `http://<prometheus-host>:9090`).
2. Navigate to Status → Service Discovery. You should see the EC2 job and the list of discovered instances.
3. Go to Status → Targets to check reachability and scrape status:
   * Up: reachable and being scraped.
   * Down: unreachable (often a network/firewall issue between Prometheus and the EC2 instance).

If targets are Down, verify:

* Network connectivity (security groups, VPC routing).
* Prometheus can reach the target port (`/metrics` path).
* Correct credentials/region for discovery.

## Additional references

* Prometheus EC2 SD docs: [https://prometheus.io/docs/prometheus/latest/configuration/configuration/#ec2\_sd\_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#ec2_sd_config)
* AWS IAM docs: [https://docs.aws.amazon.com/iam/](https://docs.aws.amazon.com/iam/)
* AWS EC2 docs: [https://docs.aws.amazon.com/ec2/](https://docs.aws.amazon.com/ec2/)

With EC2 service discovery in place, Prometheus will continually refresh the list of targets as instances are launched or terminated, keeping your monitoring accurate and up-to-date.

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/20a3a57d-ee2d-4096-888e-de1166cf7e3a/lesson/ad7f1274-06f0-4045-90ec-8520eca4ac9f)
