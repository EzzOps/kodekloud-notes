# Successfully joined cluster by contacting 1 nodes.
```

Replace `consul-node-a.example.com` with an IP address if preferred. CLI joins are best suited for testing or small labs—automated config is recommended in production.

## 2. Joining via Configuration

Add join settings directly to your agent’s JSON or HCL config. There are two options:

| Parameter   | Behavior                                                            |
| ----------- | ------------------------------------------------------------------- |
| join        | One-time contact; agent startup fails if unreachable                |
| retry\_join | Continuously retries until it successfully joins or the agent stops |

Example (`config.json`):

```json theme={null}
{
  "bootstrap": false,
  "bootstrap_expect": 3,
  "server": true,
  "retry_join": ["10.0.10.34", "10.0.11.72"]
}
```

This instructs the agent to keep retrying until it joins one of the specified IPs.

<Callout icon="lightbulb">
  Use `retry_join` for environments where agents start in an unpredictable order.\
  If you need a single attempt only, use the `join` option instead.
</Callout>

## 3. Cloud Auto-Join

Cloud auto-join uses provider metadata (tags or labels) to discover peers automatically. Supported providers include AWS, Azure, GCP, Kubernetes, and more. You must grant the agent appropriate API permissions (for example, via an AWS IAM role).

<Frame>
  ![The image is a slide titled "Adding Servers," detailing methods for an agent to join a cluster using a configuration file and cloud auto-join, listing various cloud services like AWS, Azure, and Kubernetes. It also mentions the requirement of credentials for authentication.](https://kodekloud.com/kk-media/image/upload/v1752877800/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-AddingRemoving-Consul-Agents-to-the-Cluster/adding-servers-cluster-join-methods.jpg)
</Frame>

Example AWS auto-join config:

```json theme={null}
{
  "bootstrap": false,
  "bootstrap_expect": 3,
  "server": true,
  "retry_join": ["provider=aws tag_key=consul tag_value=true"]
}
```

Each agent queries AWS EC2 for instances tagged `consul=true` and attempts to join them.

<Callout icon="triangle-alert">
  Ensure your cloud credentials or IAM roles only grant enough permissions to list instances—avoid overly broad access.
</Callout>

***

## Removing Agents from the Cluster

To gracefully remove an agent and inform the cluster:

```bash theme={null}
consul leave
# Graceful leave complete
```

A graceful leave updates the Raft peer set (for servers) and ensures nodes treat the departure as intentional rather than a failure.

## Listing Cluster Members

Use the `members` command to see all servers and clients:

```bash theme={null}
consul members
# Node        Address         Status  Type    Build   Protocol  DC    Segment
# consul-a    10.0.2.10:8301  alive   server  1.9.0   2         dc1   -
# consul-b    10.0.2.11:8301  alive   server  1.9.0   2         dc1   -
# web-app-01  10.0.8.9:8301   alive   client  1.8.6   2         dc1   -
```

In production, clusters can scale to hundreds or thousands of nodes across multiple datacenters.

## Links and References

* [Consul Agent CLI Commands](https://www.consul.io/docs/commands/agent)
* [Consul Configuration](https://www.consul.io/docs/configuration)
* [Consul Auto-Join with Cloud Providers](https://www.consul.io/docs/discovery/auto-join)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/a1f79019-1fbb-4b11-8935-0f09bdc9da3c/lesson/e93f12f6-10c0-4b76-be94-ecc9b464d696" />
</CardGroup>


# Configure Networking and Ports

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Deploy-a-Single-Datacenter/Configure-Networking-and-Ports/page

This guide explains how to configure Consuls network addresses and ports for reliable communication between internal agents and external clients.

In this guide, you’ll learn how to set up Consul’s network addresses and ports so that both internal agents and external clients can communicate reliably. Whether you have a single network interface or a complex NAT topology, these settings ensure that your Consul cluster remains accessible and secure.

## Default Consul Ports

Consul exposes several ports by default. Ensure that clients and applications can reach these ports on every node:

| Interface     | Protocol | Port | Purpose                       |
| ------------- | -------- | ---- | ----------------------------- |
| HTTP API      | TCP      | 8500 | RESTful HTTP API              |
| LAN gossip    | TCP/UDP  | 8301 | Cluster membership and gossip |
| DNS interface | TCP/UDP  | 8600 | Service discovery via DNS     |

<Frame>
  ![The image provides instructions on configuring Consul network addresses and ports, emphasizing DNS settings and the need to avoid running Consul as a root user.](https://kodekloud.com/kk-media/image/upload/v1752877801/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Configure-Networking-and-Ports/consul-network-configuration-dns-settings.jpg)
</Frame>

## DNS Port Considerations

By default, Consul listens on port 8600 for DNS queries. In environments where DNS is restricted to UDP/TCP port 53, it’s better to redirect traffic rather than run Consul as root.

<Callout icon="triangle-alert">
  Binding to ports below 1024 requires root privileges. Instead, redirect DNS requests with `iptables`, `firewalld`, or `dnsmasq` to maintain security.
</Callout>

### Redirecting DNS Traffic with iptables

```bash theme={null}
