# Demo Consul Snapshots

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Back-up-and-Restore/Demo-Consul-Snapshots/page

Learn to back up and restore your Consul service state using snapshot commands for disaster recovery and cluster portability.

In this guide, you’ll learn how to back up and restore your Consul service state using snapshot commands. We’ll cover:

* Creating a snapshot file
* Inspecting snapshot metadata
* Restoring a cluster from a snapshot

These steps are critical for disaster recovery and cluster portability.

***

## Prerequisites

* A running Consul server (open source) cluster
* Consul CLI installed and in your `$PATH`
* Permissions to read/write snapshot files

<Callout icon="lightbulb">
  Ensure you have sufficient disk space in your working directory before creating large snapshots.
</Callout>

***

## 1. Taking a Snapshot

1. SSH into one of your Consul server nodes.
2. Change to a writable directory (e.g., `/tmp`):
   ```bash theme={null}
   cd /tmp
   ```
3. Run the `save` subcommand to generate a snapshot file:
   ```bash theme={null}
   consul snapshot save consul.snap
   ```
4. Confirm the operation:
   ```text theme={null}
   ==> Consul snapshot saved: consul.snap
   ```
5. Verify the file exists:
   ```bash theme={null}
   ls -lh
   # -rw-r--r-- 1 consul consul  13K Jul  5 12:34 consul.snap
   ```

***

## 2. Inspecting a Snapshot

To view metadata about an existing snapshot file, use the `inspect` subcommand:

```bash theme={null}
consul snapshot inspect consul.snap
```

Sample output:

```text theme={null}
ID:            17-3678-1613078754824
Size:          13367
Index:         3678
Term:          17
Version:       1

Type                   Count     Size
----                   -----     ----
Register               14        9KB
License                1         1.2KB
KVS                    7         837B
...
Total                  —         13.1KB
```

<Callout icon="lightbulb">
  * The **Version** field refers to the snapshot format, not the Consul binary version.
  * **Index** and **Term** reflect the Raft state at snapshot creation.
</Callout>

***

## 3. Restoring a Snapshot

When recovering a failed cluster or migrating state, restore from your snapshot:

```bash theme={null}
consul snapshot restore consul.snap
```

After the restore completes:

1. Restart all Consul agents or services to load the restored data.
2. Check cluster status:
   ```bash theme={null}
   consul operator raft list-peers
   consul members
   ```

<Callout icon="triangle-alert">
  Do **not** restore a snapshot into an active cluster without first stopping agents—this can lead to data corruption.
</Callout>

***

## Snapshot Commands Reference

| Command                   | Description                        | Example Usage                         |
| ------------------------- | ---------------------------------- | ------------------------------------- |
| `consul snapshot save`    | Create a new snapshot file         | `consul snapshot save backup.snap`    |
| `consul snapshot inspect` | Show metadata for a snapshot       | `consul snapshot inspect backup.snap` |
| `consul snapshot restore` | Restore state from a snapshot file | `consul snapshot restore backup.snap` |

***

## Links and References

* [Consul Snapshot Documentation](https://www.consul.io/docs/commands/snapshot)
* [Consul Disaster Recovery Guide](https://www.consul.io/docs/platform/dr)
* [HashiCorp Consul Official Site](https://www.consul.io/)

***

By following these steps, you can efficiently manage Consul snapshots, ensuring reliable backups and quick recovery for your service cluster.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/6525b457-c93a-43ac-839a-7a301c64b51b/lesson/e15237c4-37c7-414b-b1a4-e59261bb7043" />
</CardGroup>
