# Demo Backup and Restore with Aurora

Source: https://notes.kodekloud.com/docs/AWS-RDS/AWS-Aurora/Demo-Backup-and-Restore-with-Aurora/page

Explains Amazon Aurora backup and restore workflows, covering manual snapshots, automated backups and point in time restore via AWS Console and CLI, plus retention and recovery best practices

In this lesson you'll learn how backups and recovery work for an Amazon Aurora database. This demo reuses an existing Aurora cluster. If you don't have one to follow along, create an Aurora cluster first (see links at the end).

## Overview

* Manual snapshots capture the entire cluster state at the moment you take them and are retained until you delete them.
* Automated backups (base snapshots + transaction logs) allow you to perform point-in-time restore (PITR) within a configured retention window.
* Use manual snapshots for indefinite rollback points (for example, before upgrades), and PITR to recover to a precise timestamp within the automated backup window.

## Prerequisite

Make sure you have:

* An Aurora cluster in the same AWS account and region you will use.
* The RDS console or AWS CLI configured with permissions to create snapshots and restores.

## Create a manual snapshot (Console + CLI)

Console:

1. Open the RDS console and select your Aurora cluster.
2. Choose Actions → Take snapshot.
3. Provide a snapshot identifier and confirm. The manual snapshot will remain until you explicitly delete it.

AWS CLI example:

```bash theme={null}
aws rds create-db-cluster-snapshot \
  --db-cluster-identifier my-aurora-cluster \
  --db-cluster-snapshot-identifier my-aurora-snapshot-2026-03-17
```

After taking the snapshot, you can view it in the RDS console snapshot list.

<Frame>
  <img alt="A screenshot of the Amazon RDS web console (eu-central-1) showing the Databases page. It displays Backup and Snapshots sections with automated backups enabled, no pending maintenance, and an empty snapshot table." />
</Frame>

## Automated backups and retention

Console:

1. Select the database, then open the **Maintenance & backups** (or **Maintenance and backup**) section.
2. Review and configure:
   * Automated backup retention period (for example, 7 days).
   * Maintenance window and backup window.

Automated backups include periodic snapshots and transaction logs, and they enable point-in-time restores for any time within the retention window.

Recommended retention guidance:

| Retention Window | Use Case                                                          |
| ---------------- | ----------------------------------------------------------------- |
| 1–7 days         | Short-term recovery from recent accidental changes                |
| 7–30 days        | Standard operational recovery and troubleshooting                 |
| 30+ days         | Long-term compliance or infrequent restore needs (cost trade-off) |

## Point-in-time restore (PITR)

Console:

1. Select the cluster (or instance) you want to recover.
2. Choose Actions → Restore to point in time.
3. Pick a restore timestamp within the automated backup retention window.
4. Provide a new DB identifier for the restored cluster and launch the restore. AWS will create a new DB cluster restored to that exact timestamp.

Example UI may show "8 minutes 21 seconds ago" — choose the precise time (for example just before a problematic migration) and proceed. Restoring creates a separate cluster so your original cluster remains unchanged.

AWS CLI example (cluster-level restore):

```bash theme={null}
aws rds restore-db-cluster-to-point-in-time \
  --source-db-cluster-identifier my-aurora-cluster \
  --restore-type full-copy \
  --restore-to-time "2026-03-17T12:34:00Z" \
  --db-cluster-identifier my-aurora-cluster-restored
```

If you prefer to restore to the latest restorable time:

```bash theme={null}
aws rds restore-db-cluster-to-point-in-time \
  --source-db-cluster-identifier my-aurora-cluster \
  --restore-type full-copy \
  --use-latest-restorable-time \
  --db-cluster-identifier my-aurora-cluster-restored
```

<Frame>
  <img alt="A screenshot of the AWS RDS console on the &#x22;Restore to point in time&#x22; page, showing options to select the restore time and settings. The DB engine dropdown is set to Aurora PostgreSQL and there is a field for the new DB instance identifier." />
</Frame>

## When to use manual snapshots vs. PITR

| Feature   | Manual Snapshot                             | Point-in-Time Restore (PITR)                                                             |
| --------- | ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Retention | Indefinite, until you delete it             | Limited to automated backup retention window                                             |
| Use case  | Pre-upgrade checkpoints, long-term archival | Recover to a specific recent timestamp (undo destructive migrations, accidental deletes) |
| Creation  | Manual via console/CLI/API                  | Automated backups + transaction logs; restore initiated when needed                      |
| Cost      | Snapshot storage costs while retained       | Automated backup storage + restored cluster costs during recovery                        |

<Callout icon="lightbulb">
  Point-in-time restore depends on automated backups (base snapshot + transaction logs). Ensure automated backups are enabled and the retention window covers the period you might need to recover. Manual snapshots are independent and are not removed by automated retention policies.
</Callout>

## Typical recovery scenario (example workflow)

1. A deployed migration accidentally adds a column and breaks queries in production.
2. Immediately: identify the approximate time of failure.
3. Use PITR to restore a new cluster to a timestamp just before the migration.
4. Update the application connection string to point to the restored cluster while you fix the migration.
5. Once the fix is validated, cut over or re-sync data as needed.

This approach minimizes downtime and gives you a safe rollback point without modifying the original cluster.

<Callout icon="warning">
  Make sure automated backups are enabled and your IAM user or role has necessary RDS permissions to create snapshots and perform restores. Note that storing snapshots and running restored clusters incur charges — review costs in your AWS Billing console.
</Callout>

## Summary

* Manual snapshots give you permanent rollback points until you explicitly delete them.
* Automated backups + transaction logs enable PITR within the retention window.
* Use the console for quick operations and the AWS CLI for automation and scripting.
* Combine manual snapshots and PITR in your disaster recovery plan for flexibility.

<Frame>
  <img alt="A screenshot of the AWS RDS Databases console showing an Aurora PostgreSQL cluster named &#x22;database-1&#x22; (eu-central-1) with available writer and reader instances listed. The page shows instance roles, sizes, CPU/activity metrics, and a &#x22;Create database&#x22; button." />
</Frame>

## Links and references

* [Amazon RDS Backups and Snapshots](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)
* [Restore a DB Cluster to a Point in Time (AWS CLI)](https://docs.aws.amazon.com/cli/latest/reference/rds/restore-db-cluster-to-point-in-time.html)
* [Amazon Aurora documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/dbfb72c4-207e-424e-ac83-55f55758740a/lesson/f1171b8e-919d-4abe-87d9-1f279dd3f641" />
</CardGroup>
