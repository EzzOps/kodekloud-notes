# On worker1
docker swarm join \
  --token SWMTKN-1-xxxxxxxxxxxxxxxxxxxxxxxx \
  172.31.46.126:2377

# On worker2
docker swarm join \
  --token SWMTKN-1-xxxxxxxxxxxxxxxxxxxxxxxx \
  172.31.46.126:2377
```text

<Callout icon="lightbulb" color="#1CB2FE">
If you lose the join token, regenerate it on the manager:

```bash
docker swarm join-token worker
```text
</Callout>

## 3. Verify Cluster Nodes

On the manager, list all nodes:

```bash
docker node ls
```text

Example output:

```plain
ID                            HOSTNAME   STATUS  AVAILABILITY  MANAGER STATUS  ENGINE VERSION
91uxgq6i78j1hu5v7moq7vgz *    manager1   Ready   Active        Leader          19.03.8
2lux7z6p96g6vtx0h6a2wo2r       worker1    Ready   Active        \<none>          19.03.8
w0qr6k2cee3ojawmflc26pvp3      worker2    Ready   Active        \<none>          19.03.8
```text

| Column            | Description                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| **STATUS**        | Ready: node is healthy and participating                                                     |
| **AVAILABILITY**  | Active: scheduler assigns tasks<br>Pause: no new tasks, existing continue<br>Drain: tasks moved off |
| **MANAGER STATUS**| Leader: primary manager<br>Reachable: manager node able to take over<br>&lt;none&gt;: worker |

The `*` marks the node where the command was run.

## 4. Inspect a Node

Get detailed info on any node:

```bash
docker node inspect manager1 --pretty
```text

Sample output:

```plain
ID:             91uxgq6i78j1hu5v7moq7vgz
Hostname:       manager1
  State:        Ready
  Availability: Active
  Address:      172.31.46.126
Manager Status:
  Address:      172.31.46.126:2377
  Raft Status:  Reachable
````

This reveals role, status, and network details.

***

## Next Steps

In the next lesson, you’ll learn how to:

* Promote a worker to manager
* Drain nodes for maintenance
* Update and roll back services

## Links and References

* [Docker Engine Documentation](https://docs.docker.com/engine/)
* [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
* [Swarm Mode Networking](https://docs.docker.com/engine/swarm/networking/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/7b921aaf-ea53-4a52-84cd-b8069a1093a1" />
</CardGroup>


# Swarm in HA mode

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Swarm-in-HA-mode/page

This guide explains how to configure a Docker Swarm cluster in high-availability mode with multiple manager and worker nodes.

In this guide, you’ll learn how to configure a Docker Swarm cluster in HA mode with three manager nodes and three worker nodes. We’ll cover initialization, adding managers and workers, testing quorum, and restoring cluster health.

## Prerequisites

* Six CentOS 7.6 VMs (2 vCPU, 4 GB RAM) on AWS
* Docker 19.03 installed on all nodes
* Swarm ports open (2377, 7946 TCP/UDP, 4789 UDP)
* Fully qualified hostnames and name resolution for all nodes

| Hostname     | IP Address    | Role (after setup) |
| ------------ | ------------- | ------------------ |
| managerone   | 172.31.42.232 | Manager (Leader)   |
| managertwo   | 172.31.42.xxx | Manager (Replica)  |
| managerthree | 172.31.42.xxx | Manager (Replica)  |
| workerone    | 172.31.39.115 | Worker             |
| workertwo    | 172.31.39.xxx | Worker             |
| workerthree  | 172.31.39.xxx | Worker             |

Verify OS and Docker:

```bash theme={null}
[root@managerone ~]# cat /etc/centos-release
CentOS Linux release 7.6.1810 (Core)
[root@managerone ~]# nproc
2
[root@managerone ~]# docker version --format '{{.Server.Version}}'
19.03.8
```

Verify network connectivity:

```bash theme={null}
[root@managerone ~]# ping -c2 workerone
PING workerone (172.31.39.115): 56 data bytes
64 bytes from workerone: icmp_seq=1 ttl=64 time=0.45 ms
```

## 1. Initialize the Swarm

On **managerone**, initialize the Swarm and advertise its IP:

```bash theme={null}
[root@managerone ~]# docker swarm init --advertise-addr 172.31.42.232
Swarm initialized: current node (kvbht...) is now a manager.
```

Confirm Swarm status:

```bash theme={null}
[root@managerone ~]# docker info --format '{{.Swarm.LocalNodeState}}'
active
```

<Callout icon="lightbulb">
  The `--advertise-addr` flag sets the manager’s reachable IP for new nodes.
</Callout>

## 2. Add Additional Managers

### 2.1 Retrieve Manager Join Token

On **managerone**:

```bash theme={null}
[root@managerone ~]# docker swarm join-token manager --quiet
SWMTKN-1-xxxxx-xxxx
```

### 2.2 Join `managertwo` and `managerthree`

On each additional manager node:

```bash theme={null}
[root@managertwo ~]# docker swarm join --token SWMTKN-1-xxxxx-xxxx 172.31.42.232:2377
This node joined a swarm as a manager.
```

Repeat on **managerthree**.

### 2.3 Verify Managers

From **managerone**:

```bash theme={null}
[root@managerone ~]# docker node ls
ID      HOSTNAME       STATUS  AVAILABILITY  MANAGER STATUS  ENGINE VERSION
* kvbht...  managerone     Ready   Active        Leader          19.03.8
  s2zym...  managertwo     Ready   Active        Reachable       19.03.8
  u81im...  managerthree   Ready   Active        Reachable       19.03.8
```

## 3. Add Worker Nodes

### 3.1 Retrieve Worker Join Token

On **managerone**:

```bash theme={null}
[root@managerone ~]# docker swarm join-token worker --quiet
SWMTKN-1-yyyyy-yyyy
```

### 3.2 Join `workerone`, `workertwo`, `workerthree`

On each worker:

```bash theme={null}
[root@workerone ~]# docker swarm join --token SWMTKN-1-yyyyy-yyyy 172.31.42.232:2377
This node joined a swarm as a worker.
```

Verify all nodes:

```bash theme={null}
[root@managerone ~]# docker node ls
ID      HOSTNAME       ROLE      MANAGER STATUS  AVAILABILITY  ENGINE VERSION
* kvbht...  managerone   Manager   Leader          Active        19.03.8
  s2zym...  managertwo   Manager   Reachable       Active        19.03.8
  u81im...  managerthree Manager   Reachable       Active        19.03.8
  38oeh...  workerone    Worker    —               Active        19.03.8
  1pqdd...  workertwo    Worker    —               Active        19.03.8
  k4gc5...  workerthree  Worker    —               Active        19.03.8
```

## 4. Testing Manager Quorum

Docker Swarm requires a majority of manager nodes to maintain a leader.

### 4.1 Simulate One Manager Failure

On **managertwo**:

```bash theme={null}
[root@managertwo ~]# systemctl stop docker
```

Check from **managerone**:

```bash theme={null}
[root@managerone ~]# docker node ls
… managertwo     Down    Active    Unreachable   19.03.8
```

The cluster remains healthy (2 of 3 managers online).

### 4.2 Simulate Two Manager Failures

On **managerthree**:

```bash theme={null}
[root@managerthree ~]# systemctl stop docker
```

Then on **managerone**:

```bash theme={null}
[root@managerone ~]# docker node ls
Error response from daemon: … The swarm does not have a leader …
```

With only one manager online, the cluster loses quorum and cannot elect a leader.

<Callout icon="triangle-alert">
  Never simulate quorum loss in production. You will lose control over scheduling and service updates.
</Callout>

## 5. Restoring Quorum

1. Start Docker on **managertwo**:
   ```bash theme={null}
   [root@managertwo ~]# systemctl start docker
   ```
2. Wait for the node to rejoin (quorum 2/3 restored).
3. Start Docker on **managerthree**:
   ```bash theme={null}
   [root@managerthree ~]# systemctl start docker
   ```
4. Verify:

   ```bash theme={null}
   [root@managerone ~]# docker node ls
   ```

All managers should show `Leader` or `Reachable`.

## Conclusion

You’ve now deployed a Docker Swarm in HA mode, added managers and workers, tested quorum behavior, and restored cluster health. This setup ensures fault tolerance and continuous service availability.

## Links and References

* [Docker Swarm Mode Overview](https://docs.docker.com/engine/swarm/)
* [Swarm Init](https://docs.docker.com/engine/reference/commandline/swarm_init/)
* [Swarm Join](https://docs.docker.com/engine/reference/commandline/swarm_join/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/16b8b1e1-1e1f-4e11-976f-8d5c1223c53d/lesson/40648232-d303-4140-8471-41c8f837cf78" />
</CardGroup>
