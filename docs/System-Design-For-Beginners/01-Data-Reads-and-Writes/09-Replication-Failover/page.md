# Replication Failover

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/Replication-Failover/page

Guide to configuring primary-replica database replication, observing lag, simulating primary failure, and promoting a replica to primary with best practices and engine-specific considerations.

In this lesson you'll configure a primary database and a replica, observe replication lag, then simulate a failure and promote the replica so it becomes the new primary. The walkthrough is implementation-agnostic and uses example SQL to illustrate observable behaviors. Replace generic steps and example commands with engine-specific procedures for PostgreSQL, MySQL, MongoDB, or other systems.

You will:

* Create a table on the primary and insert a row.
* Read from the replica and observe that the row may appear after a short delay (replication lag).
* Simulate a primary failure and promote the replica to primary.
* Confirm that destructive operations performed on the original primary (for example, deletes) are applied on the replica.

> **lightbulb** This article uses generic SQL examples to demonstrate replication and failover behavior. Consult your database vendor's documentation for exact configuration steps and production best practices.

## High-level overview

A typical workflow to set up replication and test failover:

1. Configure the primary to accept replication connections and create a replication user (engine-specific).
2. Take a base backup of the primary and restore it on the replica host.
3. Configure the replica to connect to the primary (host/port and replication credentials).
4. Start replication on the replica and confirm it is streaming or receiving changes.
5. Run test writes on the primary and observe how (and when) they appear on the replica.
6. Simulate a primary failure, promote the replica, and validate read/write behavior on the promoted node.

Note: Asynchronous replication acknowledges writes on the primary before replicas confirm receipt. This can produce observable replication lag and the potential for data loss during failover. Use synchronous replication where zero data loss is required and supported.

## 1) Prepare the primary and replica (high level)

Follow these engine-specific tasks to establish replication:

* Configure listener settings and networking so the primary accepts replication connections.
* Create a dedicated replication user with minimal privileges.
* Produce a consistent base backup from the primary and restore it to the replica.
* Configure replica connection settings (primary host/port and replication credentials).
* Start replication on the replica and verify it is receiving changes (look for streaming/replication state using engine-specific diagnostics).

For example, monitoring tools or commands typically include:

* PostgreSQL: `pg_stat_replication`, `pg_wal_lsn_diff()`, `pg_basebackup` (engine-specific).
* MySQL: `SHOW SLAVE STATUS\G` / `SHOW REPLICA STATUS\G`, `mysqldump` or binary-log based restore.
* MongoDB: `rs.status()` and `rs.initiate()` for replica sets.

## Replication modes and tradeoffs

| Mode             | Behavior                                               | Pros                            | Cons                          |
| ---------------- | ------------------------------------------------------ | ------------------------------- | ----------------------------- |
| Synchronous      | Primary waits for replicas to confirm commits          | Minimal data loss risk          | Higher write latency          |
| Semi-synchronous | Primary waits for at least one replica acknowledgement | Balanced durability and latency | Some lag possible             |
| Asynchronous     | Primary does not wait for replicas                     | Lowest write latency            | Risk of data loss on failover |

## 2) Create a test table and insert a row on the primary

On the primary database, create a table and insert a row to observe replication behavior.

```sql theme={null}
-- primary
CREATE TABLE users (
  id   SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

INSERT INTO users (name) VALUES ('alice');
```

If your SQL dialect does not support `SERIAL`, use the appropriate auto-increment or sequence construct for your database engine.

## 3) Read from the replica and observe replication lag

On the replica (which is typically read-only), poll the same table to see when the row becomes visible:

```sql theme={null}
-- replica (read-only replica)
SELECT id, name FROM users;
```

* If replication is near real-time (synchronous or low-latency streaming), the row should appear almost immediately.
* With asynchronous replication, you may see a short delay before the row is present.

Tip: Use a short loop or repeated queries to demonstrate lag. On PostgreSQL you can compare LSN positions (`pg_current_wal_lsn()` vs `pg_last_wal_replay_lsn()`); on MySQL check `Seconds_Behind_Master` in `SHOW SLAVE STATUS\G`.

## 4) Perform a delete on the primary (replication of destructive operations)

On the primary, perform a destructive action such as a DELETE. Replication systems typically propagate all data-change operations (insert, update, delete) via WAL/binlog, so the replica will apply these changes too.

```sql theme={null}
-- primary
DELETE FROM users WHERE name = 'alice';
```

Then verify on the replica:

```sql theme={null}
-- replica
SELECT id, name FROM users;
```

Once the DELETE replicates and is applied, the row should no longer be present on the replica.

## 5) Simulate a failure and promote the replica

To test failover behavior, simulate a primary failure and promote the replica:

1. Simulate primary failure by stopping the service or container:
   * Systemd-managed: `sudo systemctl stop postgresql` (PostgreSQL) or `sudo systemctl stop mysql` (MySQL).
   * Containers: stop or remove the primary container.
   * Managed services: use your cloud provider’s tools to simulate downtime.

2. Promote the replica to primary using engine-specific commands:
   * PostgreSQL (streaming): `pg_ctl promote` or use orchestrators like `repmgr` or `Patroni`.
   * MySQL Group Replication / InnoDB Cluster: use cluster tooling to elect or promote a new primary.
   * MongoDB: use replica set election or `rs.stepDown()` to trigger leadership change.

3. After promotion, enable writes on the promoted node and validate both writes and reads:

```sql theme={null}
-- promoted replica (now primary)
INSERT INTO users (name) VALUES ('bob');

SELECT id, name FROM users;
```

You should now be able to read and write to the promoted server as the new primary.

> **warning** Be careful when promoting a replica in production. If replication was asynchronous, you risk losing recent transactions that had not reached the replica. Use fencing, quorum-based elections, and well-defined failover policies to prevent split-brain and data loss.

## 6) Expected behaviors and best practices

* Replication propagates data-change operations (inserts, updates, deletes) from primary to replica; replicas generally remain read-only until promoted.
* Asynchronous replication can show lag; the replica may be behind the primary.
* When a replica is promoted after primary failure, it becomes writable and accepts new changes.
* Destructive operations performed on the primary are reproduced on the replica; replicas do not selectively ignore deletes or other changes.
* For production systems, automate monitoring, use proper backup strategies, test failover procedures regularly, and prefer synchronous or semi-synchronous configurations if application-level durability is required.

## Quick checklist before performing failover tests

* Confirm replication is healthy and caught up (use engine-specific status checks).
* Ensure backups and snapshots are available.
* Validate your monitoring and alerting.
* Test promotion on staging first, and document the promotion and rollback steps.

## Links and references

* PostgreSQL replication and failover: [https://www.postgresql.org/docs/current/high-availability.html](https://www.postgresql.org/docs/current/high-availability.html)
* MySQL replication: [https://dev.mysql.com/doc/refman/en/replication.html](https://dev.mysql.com/doc/refman/en/replication.html)
* MongoDB replica sets: [https://www.mongodb.com/docs/manual/replication/](https://www.mongodb.com/docs/manual/replication/)
* General database high-availability concepts: [https://en.wikipedia.org/wiki/High\_availability](https://en.wikipedia.org/wiki/High_availability)

Replace the generic commands in this guide with the precise procedures for your database engine and orchestration tooling to achieve a production-ready, safe setup.

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/336f1b7a-a546-4575-b6f3-88126c927acd)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/ed484991-177a-4da3-9fbb-cc20804cf730)
