# Demo OpenSearch

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-2/Demo-OpenSearch/page

Hands-on tutorial to provision an Amazon OpenSearch domain, explore OpenSearch Dashboards with sample data, and index documents using the REST API

This tutorial walks through provisioning an Amazon OpenSearch domain (cluster), exploring OpenSearch Dashboards with sample data, and indexing documents using the REST API (curl). It’s designed for a hands-on demo environment — for production deployments, apply stronger availability, security, and sizing choices.

## What you'll do

* Create an OpenSearch domain in the AWS console
* Connect to the cluster and OpenSearch Dashboards
* Add sample data and explore prebuilt dashboards
* Inspect indices and mappings
* Query documents in Discover
* Index documents via the REST API (single PUT and bulk)
* Clean up the domain to avoid charges

***

## 1) Create a domain (cluster)

1. Open the AWS Console, search for **OpenSearch**, and open the service page.
2. Click **Create domain**. A domain is an OpenSearch cluster with its own instance configuration, storage, and settings.
3. Choose **Standard create** to view and control each option (use Easy create only for fast experiments).
4. Select a template: **Production** for production workloads or **Dev/Test** for demos and labs (this guide uses **Dev/Test**).

Key decisions to make during creation (examples shown for a demo):

| Setting                   | Consideration                     | Demo example                                                 |
| ------------------------- | --------------------------------- | ------------------------------------------------------------ |
| Standby nodes             | Automated failover vs cost        | Skip for single-AZ demos; enable for HA                      |
| Availability Zones (AZs)  | Multi-AZ for resilience           | Single AZ for lab                                            |
| OpenSearch engine version | Choose a supported version        | OpenSearch 2.x                                               |
| Instance types & counts   | Size for expected load and shards | `t3.small.search`, 1 node/AZ                                 |
| Storage                   | EBS type and size per node        | 10 GiB EBS for demo                                          |
| Dedicated master nodes    | Improve cluster stability         | Disabled for simple demos                                    |
| Network access            | Public vs VPC                     | VPC + security groups for production; public for short demos |
| Access control            | IAM or master user (fine-grained) | Create master user for this demo                             |

Example ARN format for IAM principals:

```text theme={null}
arn:<partition>:iam::<account>:<type>/<id>
