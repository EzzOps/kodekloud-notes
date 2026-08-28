# AddingRemoving Consul Agents to the Cluster

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Deploy-a-Single-Datacenter/AddingRemoving-Consul-Agents-to-the-Cluster/page

This guide explains how to add and remove Consul agents in a cluster, covering join methods, graceful removal, and listing cluster members.

In this guide, you’ll learn how to add and remove Consul agents—both servers and clients—in your cluster. We’ll cover three primary join methods, how to gracefully remove agents, and how to list all cluster members.

## Overview of Agent Membership

Consul agents use the Gossip Protocol to share membership updates. When a new agent joins, it contacts an existing member; the protocol then propagates that change across the entire cluster. You can even merge two independent clusters by having an agent in one contact a node in the other.

| Join Method                                | Description                                                     | Use Case                                     |
| ------------------------------------------ | --------------------------------------------------------------- | -------------------------------------------- |
| CLI (`consul join`)                        | One-off join via DNS name or IP address                         | Ad-hoc testing, quick lab setups             |
| Static Configuration (`join`/`retry_join`) | Defined in agent config file; supports one-time and retry logic | Automated deployments, predictable startup   |
| Cloud Auto-Join                            | Leverages cloud metadata (tags) to discover and join peers      | Dynamic cloud environments (AWS, GCP, Azure) |

## 1. Joining via the CLI

You can manually join an agent to the cluster by specifying any existing member’s hostname or IP:

```bash theme={null}
consul join consul-node-a.example.com
