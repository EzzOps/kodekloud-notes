# Demo Swarm Cluster Setup

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Demo-Swarm-Cluster-Setup/page

Learn to bootstrap a resilient Docker Swarm cluster on CentOS 7.6 and manage node roles effectively.

In this step-by-step guide, you will learn how to bootstrap a resilient Docker Swarm cluster on CentOS 7.6, manage node roles, control availability, and gracefully remove nodes. By the end of this tutorial, you’ll have a three-node swarm (one manager, two workers) and know how to:

1. Initialize the swarm
2. Join worker nodes
3. Promote and demote managers
4. Drain and reactivate nodes
5. Remove nodes from the cluster

This tutorial assumes all nodes can resolve each other by hostname, have open swarm ports, and run Docker Engine v19.03.8 or later.

> **lightbulb** * Three CentOS 7.6 servers (`managerone`, `workerone`, `workertwo`)
  * 2 CPU cores and 4 GB RAM each
  * Hostname resolution (e.g., via `/etc/hosts` or DNS)
  * Open ports:
    * TCP 2377 for cluster management
    * TCP/UDP 7946 for node discovery
    * UDP 4789 for overlay networking
  * Docker Engine installed and running

## System Overview

| Node       | OS Release                           | CPUs | Memory (MiB) | Docker Version |
| ---------- | ------------------------------------ | ---- | ------------ | -------------- |
| managerone | CentOS Linux release 7.6.1810 (Core) | 2    | 3787         | 19.03.8        |
| workerone  | CentOS Linux release 7.6.1810 (Core) | 2    | 3787         | 19.03.8        |
| workertwo  | CentOS Linux release 7.6.1810 (Core) | 2    | 3787         | 19.03.8        |

## 1. Initialize the Swarm on `managerone`

1. Confirm Swarm is inactive:

   ```bash theme={null}
   docker system info | grep -i swarm
   # Swarm: inactive
   ```

2. Initialize with the manager’s advertise address:

   ```bash theme={null}
   docker swarm init --advertise-addr 172.31.42.232
   ```

   After initialization, note the worker join command output:

   ```bash theme={null}
   docker swarm join --token <SWARM_WORKER_TOKEN> 172.31.42.232:2377
   ```

## 2. Add the First Worker (`workerone`)

On **workerone**, run the join command displayed by the manager:

```bash theme={null}
docker swarm join \
  --token SWMTKN-1-3fdj9fgrjcrrj5t0pekb42n45tj96zgwxodtwd4ujv4qnhl-cop40spyhgc1tmzythfss49xn \
  172.31.42.232:2377
