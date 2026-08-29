# The Snow Family storage focused

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Services-Migration-and-Transfer/The-Snow-Family-storage-focused/page

Overview of AWS Snow Family devices for secure offline data transfer and edge compute, enabling terabyte to exabyte migrations and local processing before ingestion into Amazon S3.

In this lesson we cover the AWS Snow Family — a set of rugged, physical storage and compute devices for moving and processing very large datasets into and out of AWS. Rather than transferring many terabytes or petabytes over a network (which can be slow, costly, or impossible), you load data onto a Snow device and ship it to AWS for ingestion into Amazon S3 and other services.

Why choose a physical Snow device over network transfer?

* Very large transfers (terabytes → petabytes) over the Internet can take days/weeks and incur high bandwidth costs.
* Source locations may have limited, intermittent, or no network connectivity.
* Snow devices provide efficient, secure offline transfer and optionally run compute at the edge to reduce the amount of data moved.

## Core features and benefits

* Rugged and portable
  * Devices are designed for field conditions. Snowcone (\~4.5 lb) and Snowball devices (typically under \~50 lb) are portable while protecting data during transit.
* File system compatibility
  * Snow devices can be mounted as NFS (v3) targets so on-prem systems and file-based apps can write directly. File metadata is preserved until objects are converted during import into S3.
* On-device compute
  * Supported devices can run EC2 instances, host AWS IoT Greengrass, and (on some models) execute Lambda functions. You can select EC2 AMIs to preload when ordering a device.
* Strong encryption
  * All data at rest on Snow devices is encrypted with 256-bit keys managed by AWS KMS; keys are not stored on the device.
* Offline data migration workflow
  * Devices are shipped to you, you load data locally, then ship them back to AWS for ingestion into the S3 bucket(s) you specify.
  <Callout icon="lightbulb">
    Configure the destination [S3 bucket](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) and the required IAM roles/policies before ordering a Snow device. The import workflow requires a target S3 bucket.
  </Callout>
* Tamper resistance and device integrity
  * Snow devices include a Trusted Platform Module (hardware root of trust) and tamper-evident features.
* Tracking and lifecycle
  * Shipping labels and tracking are integrated with AWS. After data ingestion, devices are wiped per AWS procedures.

## Snow Family device overview

* Snowball Edge
  * Rugged (\~50 lb) with onboard storage and compute. Good for local processing + data transfer.
* Snowcone
  * Ultra-portable, secure, and rugged. Ideal for small edge sites, field data collection, and when you need portability.
* Snowball (standard)
  * Suitcase-sized rugged device in variants:
    * Snowball Edge Compute Optimized — for compute-heavy edge workloads.
    * Snowball Edge Storage Optimized — for data-heavy transfers.
* [Snowmobile](https://aws.amazon.com/snowmobile/)
  * Exabyte-scale migration (semi-trailer truck), up to \~100 PB per Snowmobile.

| Device                          | Best for                              |                             Key specs (typical) | Typical use cases                                                      |
| ------------------------------- | ------------------------------------- | ----------------------------------------------: | ---------------------------------------------------------------------- |
| Snowcone                        | Ultra-portable edge/remote            |                    Small footprint, lightweight | Sensor/IoT aggregation, remote data collection, local preprocessing    |
| Snowball Edge (Storage/Compute) | Edge compute + medium-large transfers | Up to tens to hundreds of TB, onboard CPUs/GPUs | Video analytics, ML inference at edge, pre-processing before S3 import |
| Snowball (standard)             | Large offline data transfer           |                  High-capacity HDD/NVMe options | Data migration from branch sites or labs                               |
| Snowmobile                      | Exabyte-scale migrations              |                     Truck-scale, up to \~100 PB | Migrating large datacenters or very large archives to AWS              |

<Frame>
  <img alt="A presentation slide titled &#x22;Snow Family – Components&#x22; showing four AWS Snow devices: AWS Snowball Edge, AWS Snowcone, AWS Snowball, and AWS Snowmobile with corresponding icons. Below are capacity/spec callouts like &#x22;104 vCPU&#x22;, &#x22;80 TB HDD / 210 TB NVMe&#x22;, and &#x22;Exabyte scale Data Migration.&#x22;" />
</Frame>

## When to use each device

* Snowcone and Snowball Edge: when connectivity is limited or intermittent, or when you need edge compute (e.g., image/video analytics, ML inference, IoT aggregation). Suited for rugged or remote environments (ships, field sites, construction).
* Snowball and Snowmobile: when on-network transfer is impractical due to data volume, cost, or time — e.g., large datacenter migrations.

## Common use cases

* Edge computing and data aggregation in disconnected or harsh environments
* Bulk data migration from corporate datacenters to Amazon S3
* Running analytics, ML inference, or custom EC2 workloads locally before shipping refined datasets to AWS

<Frame>
  <img alt="A diagram titled &#x22;Snow Use Cases&#x22; showing Edge Computing (DDIL) and a Corporate Data Center (Data Migration) feeding into the AWS Snow Family. The Snow devices then transfer data to an S3 bucket in the AWS Cloud." />
</Frame>

## Integrations and supported services

* Primary ingestion target: Amazon S3 — configure target buckets before creating a Snow job.
* Compute and edge services: supported devices can run EC2 instances, Lambda functions (on some models), and host AWS IoT Greengrass for edge applications.
* AWS DataSync: can be used with Snowcone for online transfers where network connectivity permits.

## Practical checklist before ordering a Snow device

* Create and confirm the target S3 bucket(s).
* Ensure IAM roles and policies for the import job are in place.
* Decide whether you need preloaded EC2 AMIs or runtime compute (for Snowball Edge).
* Plan logistics: shipping address, staging area, and physical security for the device.

## Security & compliance

* Data encrypted with AWS KMS-managed 256-bit keys; encryption keys are not stored on the device.
* Trusted Platform Module (TPM) and tamper-evident hardware protect device integrity.
* AWS provides tracking and secure wiping procedures after ingestion.

## Summary

The AWS Snow Family spans portable devices for edge collection and compute (Snowcone, Snowball Edge) to suitcase-sized data movers and truck-scale Snowmobile for exabyte migrations. Choose a device based on portability, compute needs, and total data volume. Use Snow devices when network-based transfers are too slow, costly, or impossible, or when you need to preprocess data at the edge.

## Links and references

* [AWS Snow Family](https://aws.amazon.com/snow/)
* [Amazon S3 documentation](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [AWS EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
* [AWS Lambda](https://learn.kodekloud.com/user/courses/aws-lambda)
* [AWS IoT Greengrass](https://aws.amazon.com/greengrass/)
* [AWS DataSync](https://aws.amazon.com/datasync/)
* [AWS KMS](https://aws.amazon.com/kms/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/4fd27446-288a-44dc-a3f3-99e943f92fe2/lesson/f44f5349-9119-40fd-b290-badb9ad7ee96" />
</CardGroup>
