# Check Consul version
consul version
```

```text theme={null}
Consul v1.9.3+ent
Revision bd0dc9e5d
Protocol 2 spoken by default, understands 2 to 3
```

```bash theme={null}
# Confirm the binary in PATH
ls /usr/local/bin
```

```text theme={null}
consul
```

```bash theme={null}
# List systemd service files
ls /etc/systemd/system
```

```text theme={null}
consul.service  consul-snapshot.service  basic.target.wants  ...  
```

You should see both `consul.service` and `consul-snapshot.service`.

***

## 3. Reviewing the Systemd Service File

Open `/etc/systemd/system/consul.service` to inspect how Consul is managed:

```ini theme={null}
[Unit]
Description="HashiCorp Consul - A service mesh solution"
Documentation=https://www.consul.io/
Requires=network-online.target
After=network-online.target
ConditionFileNotEmpty=/etc/consul.d/config.hcl

[Service]
Type=notify
User=consul
Group=consul
ExecStart=/usr/local/bin/consul agent -config-file=/etc/consul.d/config.hcl
ExecReload=/usr/local/bin/consul reload
KillMode=process
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

This unit ensures Consul starts after networking is available and points to our main configuration file.

***

## 4. Reviewing the Consul Configuration (Node A)

Below is the JSON-based configuration at `/etc/consul.d/config.hcl` for **node A** (`10.0.101.110`):

```json theme={null}
{
  "log_level": "INFO",
  "node_name": "consul-node-a",
  "server": true,
  "ui": true,
  "leave_on_terminate": true,
  "data_dir": "/etc/consul.d/data",
  "datacenter": "us-east-1",
  "client_addr": "0.0.0.0",
  "bind_addr": "10.0.101.110",
  "advertise_addr": "10.0.101.110",
  "retry_join": ["10.0.101.248"],
  "enable_syslog": true,
  "performance": {
    "raft_multiplier": 1
  }
}
```

Key configuration parameters:

| Parameter   | Description                                  |
| ----------- | -------------------------------------------- |
| server      | Enables server mode                          |
| ui          | Activates the built-in web UI                |
| retry\_join | List of peer addresses for automatic joining |
| data\_dir   | Location for Raft logs and state             |
| bind\_addr  | Network interface for cluster communication  |

***

## 5. Starting Consul on Both Nodes

Open required ports (8300–8302, 8500, 8600) in your security groups before proceeding.

### Node A

```bash theme={null}
sudo systemctl start consul
```

### Node B

On the second instance (`10.0.101.248`), the `/etc/consul.d/config.hcl` is identical except for IP addresses and `node_name`:

```json theme={null}
{
  "node_name": "consul-node-b",
  "bind_addr": "10.0.101.248",
  "advertise_addr": "10.0.101.248",
  "retry_join": ["10.0.101.110"],
  ...
}
```

Start the service:

```bash theme={null}
sudo systemctl start consul
```

### Verify Cluster Membership

Run on either node:

```bash theme={null}
consul members
```

```text theme={null}
Node           Address             Status  Type    Build       Protocol  DC          Segment
consul-node-a  10.0.101.110:8301   alive   server  1.9.3+ent   2         us-east-1   <all>
consul-node-b  10.0.101.248:8301   alive   server  1.9.3+ent   2         us-east-1   <all>
```

| Node          | Address           | Status | Type   |
| ------------- | ----------------- | ------ | ------ |
| consul-node-a | 10.0.101.110:8301 | alive  | server |
| consul-node-b | 10.0.101.248:8301 | alive  | server |

Because of the `retry_join` settings, both servers automatically discover each other and form a cluster.

***

That concludes this lab. You’ve learned how to:

* Run Consul in **dev mode** locally
* Prepare EC2 instances and verify Consul installation
* Inspect systemd service and configuration files
* Bootstrap a two-node Consul server cluster on AWS

***

## Links and References

* [Consul Documentation](https://www.consul.io/docs)
* [Consul Agent Overview](https://www.consul.io/docs/agent)
* [Consul Web UI](https://www.consul.io/docs/ui)
* [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
* [Packer by HashiCorp](https://www.packer.io/)
* [Systemd Service Files Best Practices](https://www.consul.io/docs/platforms/systemd)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/a1f79019-1fbb-4b11-8935-0f09bdc9da3c/lesson/549f2484-f81b-4d2b-81a5-178c9bc87220)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/a1f79019-1fbb-4b11-8935-0f09bdc9da3c/lesson/32cfa511-85e4-48e6-8fdc-8b3a50c6f511)


# Manage the Consul Process

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Deploy-a-Single-Datacenter/Manage-the-Consul-Process/page

This guide covers essential tasks for managing the Consul process, including restarting, stopping, gracefully removing nodes, and reloading configuration.

In this guide, we cover essential tasks for Consul process management: restarting the agent, performing a graceful node removal, stopping the service, and reloading configuration without downtime.

## Table of Contents

* [Restarting Consul](#restarting-consul)
* [Stopping Consul](#stopping-consul)
* [Graceful Node Removal](#graceful-node-removal)
* [Reloading Configuration](#reloading-configuration)
* [Command Reference](#command-reference)
* [Links and References](#links-and-references)

## Restarting Consul

To apply updates or recover from errors, restart the Consul agent via your system's service manager. On systemd-based Linux distributions:

```bash theme={null}
systemctl restart consul
```

## Stopping Consul

Shutting down the Consul agent cleans up local resources and halts background processes:

```bash theme={null}
systemctl stop consul
```

> **triangle-alert** If you exit the service abruptly, active sessions and health checks may fail. Always prefer a graceful approach when decommissioning nodes.

## Graceful Node Removal

When decommissioning a server, notify the Consul cluster that the node is leaving before stopping the service:

```bash theme={null}
consul leave
systemctl stop consul
```

> **triangle-alert** Running `consul leave` ensures the cluster marks this node as offline. Skipping this step can result in stale node entries and disrupted service discovery.

## Reloading Configuration

Consul supports reloading a subset of configuration changes in-place without restarting the agent. After editing reloadable files—such as ACL tokens, health checks, log levels, node metadata, service definitions, TLS certificates, or watches—apply them on-the-fly:

```bash theme={null}
consul reload
```

This command instructs the running agent to re-read its configuration and continue operation.

> **lightbulb** Not all settings are reloadable. Changes to network parameters, bootstrap options, or data directory settings require a full service restart. For a detailed list, refer to the [Consul reload documentation](https://www.consul.io/docs/commands/reload).

### Reloadable Configuration Types

| Configuration Type     | Reloadable |
| ---------------------- | ---------- |
| ACL Tokens             | Yes        |
| Health Checks          | Yes        |
| Log Levels             | Yes        |
| Node Metadata          | Yes        |
| Service Definitions    | Yes        |
| TLS Settings           | Yes        |
| Watches                | Yes        |
| Network & Bootstrap    | No         |
| Data Directory Options | No         |

## Command Reference

| Action                                      | Command                    |
| ------------------------------------------- | -------------------------- |
| Restart the Consul service (systemd)        | `systemctl restart consul` |
| Stop the Consul service                     | `systemctl stop consul`    |
| Gracefully leave the Consul cluster         | `consul leave`             |
| Reload agent configuration without downtime | `consul reload`            |

## Links and References

* [Consul Documentation](https://www.consul.io/docs)
* [Consul Commands: reload](https://www.consul.io/docs/commands/reload)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/a1f79019-1fbb-4b11-8935-0f09bdc9da3c/lesson/8728d959-b5ab-4e53-aabb-097f8ff1ec20)
