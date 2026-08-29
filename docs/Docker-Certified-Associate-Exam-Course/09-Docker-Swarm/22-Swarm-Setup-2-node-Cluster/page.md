# Swarm Setup 2 node Cluster

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Swarm-Setup-2-node-Cluster/page

Learn to set up a Docker Swarm cluster with one manager and two workers, perform node operations, and verify cluster status.

````markdown theme={null}
In this guide, you'll learn how to set up a Docker Swarm cluster with one manager and two workers, perform basic node operations, and verify cluster status. By the end, you'll be ready to add, promote, or drain nodes in your Swarm.

## Prerequisites

1. Three machines (physical or virtual), on-premise or cloud.  
2. Static IPs assigned:
   - **manager1**: 172.31.46.126  
   - **worker1**: 172.31.46.127  
   - **worker2**: 172.31.46.128  
3. Install [Docker Engine](https://docs.docker.com/engine/install/) on each host.  
4. Open firewall ports for Swarm communication:

| Port     | Protocol | Description                          |
|----------|----------|--------------------------------------|
| 2377     | TCP      | Cluster management                   |
| 7946     | TCP/UDP  | Node-to-node communication           |
| 4789     | UDP      | Overlay network (VXLAN) traffic      |

<Callout icon="triangle-alert" color="#FF6B6B">
Ensure your firewall rules allow traffic on these ports; otherwise, worker nodes cannot join the Swarm.
</Callout>

## Verify Docker and Swarm Status

After installation, run:

```bash
docker system info
```text

Look for:

```plain
Swarm: inactive
```text

If `Swarm: inactive`, the node is not yet part of a Swarm cluster.

## 1. Initialize the Swarm Manager

On **manager1**, execute:

```bash
docker swarm init --advertise-addr 172.31.46.126
```text

This:

- Configures the host as the Swarm manager  
- Prints the `docker swarm join` command with a token for workers  

Re-run `docker system info` to confirm:

```plain
Swarm: active
```text

## 2. Join Worker Nodes

Copy the join command from the manager’s output and run on each worker:

```bash
