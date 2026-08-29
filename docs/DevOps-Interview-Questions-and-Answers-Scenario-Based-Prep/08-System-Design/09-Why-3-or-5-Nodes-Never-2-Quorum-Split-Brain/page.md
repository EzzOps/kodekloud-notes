# Why 3 or 5 Nodes Never 2 Quorum Split Brain

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/System-Design/Why-3-or-5-Nodes-Never-2-Quorum-Split-Brain/page

Explains why etcd clusters use three or five nodes, quorum voting prevents split brain and how odd-sized clusters maximize fault tolerance

Have you noticed that Kubernetes control planes (etcd clusters) are typically deployed with three or five members — but almost never two? The reason is fundamental to distributed systems: how a cluster reaches agreement (consensus) about critical state, and how it avoids split-brain when network failures occur.

<Frame>
  <img alt="The image discusses how many nodes should be in a Kubernetes control plane, recommending three or five nodes, while advising against having one or two nodes." />
</Frame>

Consensus protocols (like Raft, used by etcd) require replicated components to agree on three things: which node is leader, what the most recent committed write is, and whether a peer is alive. When the network is healthy this is straightforward; the challenge is network partitions or partial failures.

<Frame>
  <img alt="The image illustrates the concept of node agreement within a cluster, highlighting queries about leadership, recent writes, and node status, accompanied by a triangular diagram representing nodes." />
</Frame>

Consider a two-node cluster and a broken link between the nodes. Node A can no longer talk to Node B and may assume B is dead and promote itself to leader. Node B sees the same and may promote itself as well.

<Frame>
  <img alt="The image depicts a two-node cluster with Node 1 as the leader, and a question about Node 1's status. There is a line between the nodes with a break, suggesting a potential connection issue." />
</Frame>

Both leaders will accept writes independently — the data diverges, and reconciling the two branches when the partition heals is extremely difficult. This dangerous state is called split-brain.

The standard defense is majority voting (quorum). A member can only lead or commit writes if a majority of nodes agree. Because two disjoint partitions cannot both hold a majority, split-brain is prevented.

Key behavior by cluster size:

* 3 nodes → majority = 2. One node can fail or be isolated; the remaining two still make progress.
* 2 nodes → majority = 2. If the link breaks, neither side can see a majority of peers; each may erroneously assume leadership and split-brain can occur.
* 4 nodes → majority = 3. The cluster can tolerate one failure; two failures leave only two nodes and no majority, so the cluster refuses to make progress.
* 5 nodes → majority = 3. The cluster tolerates up to two failures and still has a majority.

To summarize, odd-sized clusters maximize fault tolerance per added member under majority voting: adding a fourth voting member to a three-member cluster does not increase the number of simultaneous failures you can tolerate (both 3- and 4-node clusters tolerate one failure), whereas going to five members does (tolerate two failures).

<Frame>
  <img alt="The image explains why an odd number of nodes is preferred in a Kubernetes' database, illustrating that with four nodes, two don't form a majority, whereas three of four do. It highlights that both four and three nodes can survive one failure." />
</Frame>

| Nodes | Quorum (majority) | Max tolerated failures | Notes                                               |
| ----- | ----------------: | ---------------------: | --------------------------------------------------- |
| 1     |                 1 |                      0 | Single point of failure; not HA.                    |
| 2     |                 2 |                      0 | No tolerated failures; vulnerable to split-brain.   |
| 3     |                 2 |                      1 | Common small HA setup for etcd.                     |
| 4     |                 3 |                      1 | Same tolerated failures as 3 nodes.                 |
| 5     |                 3 |                      2 | Better fault tolerance; common for larger clusters. |

<Callout icon="lightbulb">
  Rule of thumb: run an odd number of etcd members (3, 5, 7, ...) so each additional member increases cluster fault tolerance. Etcd requires a majority (quorum) to make progress; quorum size determines how many failures you can tolerate.
</Callout>

<Callout icon="warning">
  Never run a two-node etcd cluster for high availability. Two members have a quorum size of two, which leaves zero tolerance for failures and creates split-brain risk during partitions. If you need HA, use 3 or more voting members.
</Callout>

Practical checks and quick commands

* List etcd members (requires etcd client config / TLS in production):

```bash theme={null}
etcdctl member list
```

* Check cluster health:

```bash theme={null}
etcdctl endpoint status --write-out=table
```

* For Kubernetes control plane health, inspect etcd and API server pods:

```bash theme={null}
kubectl get pods -n kube-system -l component=etcd
kubectl get pods -n kube-system -l component=kube-apiserver
```

Further reading and references

* [etcd: Raft consensus protocol and clustering](https://etcd.io/docs/)
* [Kubernetes: Configure and upgrade etcd](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)
* [Raft: Understandable distributed consensus](https://raft.github.io/)

Now tell me in the comments: have you ever encountered split-brain or quorum loss in a cluster, and how did you recover from it?

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/ef53ec43-96e9-4d1b-8a6e-e6eb97b0d0dc/lesson/6dce7f23-d696-4c5e-ba0a-61b790257b0d" />
</CardGroup>
