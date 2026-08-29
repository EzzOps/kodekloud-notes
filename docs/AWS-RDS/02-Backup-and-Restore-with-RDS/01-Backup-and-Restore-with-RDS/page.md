# Backup and Restore with RDS

Source: https://notes.kodekloud.com/docs/AWS-RDS/Backup-and-Restore-with-RDS/Backup-and-Restore-with-RDS/page

Guide to Amazon RDS backup and restore practices, covering automated backups, manual snapshots, point in time recovery, cross region restores, testing, and retention for disaster recovery and compliance

In this lesson we explain why database backups are essential and how Amazon RDS handles backups and restores. Reliable backups protect your applications from hardware failure, human error, and regional outages — and enable you to meet compliance and retention requirements.

Common reasons to implement database backups:

* Disaster recovery — restore service after infrastructure or regional failures.
* Data loss prevention — recover from accidental deletes or corruption.
* Compliance — meet legal, regulatory, and audit requirements for retention and recoverability.

<Frame>
  <img alt="A presentation slide titled &#x22;Backup and Restore With RDS&#x22; that lists reasons to back up a database: Disaster Recovery, Data Loss Prevention, and Compliance, each shown with a colored icon." />
</Frame>

A backup strategy must include both reliable backups and tested restores. Backups without validation can leave you unable to recover when it matters most. Plan for Recovery Time Objective (RTO) and Recovery Point Objective (RPO) when choosing retention windows, snapshot schedules, and cross-region replication.

How Amazon RDS backups work (high level)

* Automated backups: When enabled, RDS creates periodic storage snapshots and captures transaction logs so you can perform point-in-time recovery (PITR) to any second within the retention window.
* Manual DB snapshots: You can create snapshots on-demand; these snapshots remain until you explicitly delete them.
* Backup window: Backups run during a preferred backup window you configure to reduce performance impact during peak hours.
* Instance stopped behavior: Automated backups are not taken while a DB instance is stopped.
* Engine differences: Implementation varies by engine—Amazon Aurora uses continuous backups to the cluster volume and supports fast PITR, while traditional engines rely on periodic snapshots and transaction log capture. See the Aurora and RDS docs for engine-specific details.

Useful links:

* [Amazon RDS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
* [Amazon Aurora Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Welcome.html)
* [Snapshot Export to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ExportSnapshot.html)
* [Amazon S3](https://docs.aws.amazon.com/s3/index.html)

Important storage detail: RDS stores snapshots in AWS-managed, S3-backed storage owned by the RDS service. Those snapshot objects are not visible in your own S3 buckets unless you export or copy them using supported features.

<Frame>
  <img alt="A presentation slide titled &#x22;Backup and Restore With RDS&#x22; showing a diagram of a VPC inside a region with an RDS icon and AWS Backup/S3, plus bullet points about point-in-time backups and restoring a database to a new region." />
</Frame>

Practical notes, guarantees, and behaviors

* Point-in-time recovery: With automated backups enabled and an appropriate retention period, you can restore to any time within the retention window. The window length is the maximum look-back period.
* Manual snapshots: Retained until you delete them, independent of automated backup settings.
* Paused backups: If you stop a DB instance, automated backups are suspended while it is stopped.
* Re-enabling automated backups: If you disable and later re-enable automated backups, PITR is only available from the time you re-enable — you cannot recover to times during the disabled interval.
* Cross-region restores: You can copy manual snapshots to another region to support disaster recovery and regional failover.

Backup types comparison

| Backup Type              | Retention                     | Typical Use Case                           | Notes                                                                           |
| ------------------------ | ----------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------- |
| Automated backups        | Configurable retention window | Regular PITR and daily recovery            | Includes periodic snapshots + transaction logs; retained by RDS-managed storage |
| Manual DB snapshots      | Until explicitly deleted      | Long-term retention, pre-change checkpoint | Can be copied across regions                                                    |
| Aurora continuous backup | Continuous                    | Fast PITR, minimal RPO                     | Writes backups to cluster volume; faster restores for Aurora clusters           |

<Callout icon="lightbulb">
  Enable automated backups with a retention window that meets your RPO. Use manual snapshots for long-term retention, before major changes, or when preparing for cross-region copy/restore.
</Callout>

Cross-region backup and restore

* Copy manual snapshots to another AWS region for disaster recovery and geographic redundancy.
* AWS copies snapshot data into the destination region’s managed storage, enabling you to restore a new DB instance there.
* For replicated or multi-AZ architectures, validate cross-region workflows as part of your DR plan.

Testing your backups

* Regular restore tests validate that backups are usable and that procedures meet your RTO targets.
* Measure Mean Time To Recovery (MTTR) during drills and document any gaps in runbooks, permissions, or automation.
* Test both within-region and cross-region restores if your recovery plan depends on regional failover.

<Callout icon="warning">
  Do not assume backups are valid without testing. Regular restore drills and verification are essential for recoverability and compliance.
</Callout>

Summary and next steps

* Backups are essential for disaster recovery, data protection, and compliance.
* Amazon RDS supports automated backups with PITR, manual snapshots for long-term retention, and engine-specific features (e.g., Aurora continuous backups).
* RDS snapshots are stored in AWS-managed S3-backed storage; use snapshot copy or export to transfer data between regions or into your own S3 buckets.
* Configure an appropriate backup window and retention period, and run regular restore tests to validate recoverability.

Further reading and references

* [Amazon RDS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
* [Amazon Aurora User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Welcome.html)
* [Exporting DB Snapshot Data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ExportSnapshot.html)
* [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/index.html)

A hands-on session will walk through the RDS console to demonstrate enabling automated backups, creating manual snapshots, copying snapshots to another region, and performing restores.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/6bd9d043-1ee1-471f-ae73-b00e951f4205/lesson/21bf334b-d463-4763-95c4-2fbcadf776d1" />
</CardGroup>
