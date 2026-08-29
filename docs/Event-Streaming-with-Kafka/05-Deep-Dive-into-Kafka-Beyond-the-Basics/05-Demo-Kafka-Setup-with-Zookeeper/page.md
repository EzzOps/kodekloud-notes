# Demo Kafka Setup with Zookeeper

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Deep-Dive-into-Kafka-Beyond-the-Basics/Demo-Kafka-Setup-with-Zookeeper/page

Guide to installing and running Apache Kafka with ZooKeeper on CentOS, showing download, configuration, starting services, and verifying Kafka connects to ZooKeeper

Welcome — this guide walks through setting up Apache Kafka with ZooKeeper on a CentOS (or similar) Linux host. It explains how Kafka depends on ZooKeeper, how to start both services, and how to verify they are communicating.

Prerequisite

* A CentOS machine (or similar Linux host) with network access to download Kafka binaries.

Step 1 — Download and extract Kafka
Download the Kafka 3.0.0 binary and extract it:

```bash theme={null}
bob@centos-host ~ $ wget https://archive.apache.org/dist/kafka/3.0.0/kafka_2.13-3.0.0.tgz
bob@centos-host ~ $ tar -xzf kafka_2.13-3.0.0.tgz
```

List and change into the extracted directory:

```bash theme={null}
bob@centos-host ~ $ ls -lrt
total 84380
drwxr-xr-x 7 bob bob  4096 Sep 20 2021 kafka_2.13-3.0.0

bob@centos-host ~ $ cd kafka_2.13-3.0.0/
bob@centos-host ~/kafka_2.13-3.0.0 $ ls -lrt
total 64
-rw-r--r--  1 bob bob  28184 Sep  8  2021 NOTICE
-rw-r--r--  1 bob bob  14521 Sep  8  2021 LICENSE
drwxr-xr-x  2 bob bob   4096 Sep  8  2021 config
drwxr-xr-x  3 bob bob   4096 Sep  8  2021 bin
drwxr-xr-x  2 bob bob   4096 Apr 16 18:06 site-docs
drwxr-xr-x  2 bob bob   4096 Apr 16 18:06 libs
```

Notes:

* All start/stop scripts are in the `bin` directory.
* Default configuration files live in `config`.

Step 2 — Inspect ZooKeeper-related scripts
Change into `bin` and list ZooKeeper scripts:

```bash theme={null}
bob@centos-host ~/kafka_2.13-3.0.0 $ cd bin
bob@centos-host ~/kafka_2.13-3.0.0/bin $ ls -lrt | grep zookeeper
-rwxr-xr-x 1 bob bob  1019 Sep  8 2021 zookeeper-shell.sh
-rwxr-xr-x 1 bob bob 1366 Sep  8 2021 zookeeper-server-stop.sh
-rwxr-xr-x 1 bob bob 1393 Sep  8 2021 zookeeper-server-start.sh
-rwxr-xr-x 1 bob bob  867 Sep  8 2021 zookeeper-security-migration.sh
```

Quick reference table for the files you’ll use:

| File                        | Purpose                                              | Example usage                                               |
| --------------------------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| `zookeeper-server-start.sh` | Starts a standalone ZooKeeper server (used by Kafka) | `bin/zookeeper-server-start.sh config/zookeeper.properties` |
| `zookeeper-server-stop.sh`  | Stops the ZooKeeper server                           | `bin/zookeeper-server-stop.sh`                              |
| `zookeeper-shell.sh`        | A shell client for interacting with ZooKeeper        | `bin/zookeeper-shell.sh localhost:2181`                     |

Step 3 — Inspect the default ZooKeeper config
The default ZooKeeper configuration file is `config/zookeeper.properties`. List the config directory:

```bash theme={null}
bob@centos-host ~/kafka_2.13-3.0.0/bin $ cd ../config
bob@centos-host ~/kafka_2.13-3.0.0/config $ ls -lrt
total 76
-rw-r--r-- 1 bob bob  1205 Sep  8 2021 zookeeper.properties
-rw-r--r-- 1 bob bob  2547 Sep  8 2021 server.properties
...
```

What to check in `zookeeper.properties`:

* Client port (default: `2181`)
* Data directory (`dataDir`)
* Clustering settings (if running an ensemble)

Step 4 — Start ZooKeeper
You can start ZooKeeper either from the Kafka root or from the `bin` directory.

Example — start from Kafka root:

```bash theme={null}
bob@centos-host ~/kafka_2.13-3.0.0 $ bin/zookeeper-server-start.sh config/zookeeper.properties
```

Example — start from `bin` directory:

```bash theme={null}
bob@centos-host ~/kafka_2.13-3.0.0/bin $ ./zookeeper-server-start.sh ../config/zookeeper.properties
```

Tip: If you see a path-related error, confirm the relative path to `zookeeper.properties` matches your current working directory.

ZooKeeper startup logs (stdout) include lines such as:

```text theme={null}
[2025-04-16 18:09:25,198] INFO  Binding to port 0.0.0.0:2181 (org.apache.zookeeper.server.NIOServerCnxnFactory)
[2025-04-16 18:09:25,376] INFO  Snapshot loaded in 14 ms, highest zxid is 0x1 (org.apache.zookeeper.server.snapshot.SnapshotLog)
[2025-04-16 18:09:25,484] INFO  ZooKeeper audit is disabled. (org.apache.zookeeper.server.auth.XKAuditProvider)
```

> **lightbulb** By default ZooKeeper listens on port 2181 (the client port). Kafka connects to ZooKeeper on that port unless you change `zookeeper.connect` in Kafka’s `server.properties`.

Step 5 — Start the Kafka broker (in a new terminal)
Open a second terminal, change into the Kafka folder, and start the broker:

```bash theme={null}
bob@centos-host ~ $ cd kafka_2.13-3.0.0
bob@centos-host ~/kafka_2.13-3.0.0 $ bin/kafka-server-start.sh config/server.properties
```

During startup Kafka reads `server.properties`. By default it contains:

```text theme={null}
zookeeper.connect = localhost:2181
zookeeper.session.timeout.ms = 18000
```

Watch the broker logs for confirmation it started and connected to ZooKeeper:

```text theme={null}
[2025-04-16 18:10:55,688] INFO Loaded logs to directory /tmp/kafka-logs (kafka.log.LogManager)
[2025-04-16 18:10:56,763] INFO Starting log cleanup with a period of 300000 ms. (kafka.log.LogManager)
[2025-04-16 18:10:56,687] INFO [BrokerToControllerChannelManager broker=...] Starting (kafka.server.BrokerToControllerRequestThread)
```

Troubleshooting

* If Kafka cannot connect to ZooKeeper, it will fail during broker initialization. Confirm:
  * ZooKeeper is running and reachable on the address in `zookeeper.connect`.
  * Network/iptables allow traffic to port `2181`.
  * The `server.properties` and `zookeeper.properties` file paths are correct when launching the scripts.

Conclusion
This demo covered:

* Downloading and extracting Kafka binaries
* Locating ZooKeeper startup scripts and configuration files
* Starting ZooKeeper and verifying it binds to port 2181
* Starting the Kafka broker and confirming it connects to ZooKeeper

Further reading and references

* [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
* [ZooKeeper Documentation](https://zookeeper.apache.org/doc/current/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/9aa104e8-faa5-4099-977f-71744306b99d/lesson/7f934bbb-2acd-4691-9efb-047f9c559856)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/9aa104e8-faa5-4099-977f-71744306b99d/lesson/0da97c74-0c4a-495e-b69d-2c77581a9aef)
