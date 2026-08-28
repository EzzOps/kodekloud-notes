# Edit values.yaml to set:
# kubeProxyReplacement: true
# l2announcements.enabled: true
# k8sServiceHost: <API_SERVER_IP>
helm install cilium cilium/cilium -n kube-system -f values.yaml
```

Example installation output (abbreviated):

```text theme={null}
LAST DEPLOYED: Wed Jun  4 23:58:52 2025
NAMESPACE: kube-system
STATUS: deployed
REVISION: 1
NOTES:
You have successfully installed Cilium with Hubble.
Your release version is 1.17.2.
```

Verify Cilium pods are running:

```bash theme={null}
kubectl get pods -n kube-system
```

## 2. Deploy two simple applications with LoadBalancer services

Create a manifest named apps-and-svcs.yaml which deploys two HTTP echo applications and exposes each with a Service of type LoadBalancer.

apps-and-svcs.yaml:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1-deployment
  labels:
    app: app1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
    spec:
      containers:
      - name: app1
        image: hashicorp/http-echo
        args:
        - -listen=:80
        - -text="This is app1"
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app1-service
  labels:
    app: myapp
spec:
  type: LoadBalancer
  selector:
    app: app1
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2-deployment
  labels:
    app: app2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app2
  template:
    metadata:
      labels:
        app: app2
    spec:
      containers:
      - name: app2
        image: hashicorp/http-echo
        args:
        - -listen=:80
        - -text="This is app2"
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app2-service
  labels:
    app: myapp
spec:
  type: LoadBalancer
  selector:
    app: app2
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

Apply the manifest:

```bash theme={null}
kubectl apply -f apps-and-svcs.yaml
```

In a local Kind cluster, LoadBalancer services initially show EXTERNAL-IP as `<pending>`:

```bash theme={null}
kubectl get svc
NAME           TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
app1-service   LoadBalancer   10.96.207.254   <pending>     80:31514/TCP   5s
app2-service   LoadBalancer   10.96.157.80    <pending>     80:32546/TCP   5s
kubernetes     ClusterIP      10.96.0.1       <none>        443/TCP        9m
```

## 3. Provide external IPs to LoadBalancer services with Cilium IPAM

Create a CiliumLoadBalancerIPPool so Cilium can allocate external IPs for your services from an address block on your node subnet. In this demo the node subnet is 172.19.0.0/16 and we pick a small range:

ipam.yaml:

```yaml theme={null}
apiVersion: "cilium.io/v2alpha1"
kind: CiliumLoadBalancerIPPool
metadata:
  name: "default-pool"
spec:
  blocks:
  - start: "172.19.0.240"
    stop: "172.19.0.250"
```

Apply the pool:

```bash theme={null}
kubectl apply -f ipam.yaml
# ciliumloadbalancerippool.cilium.io/default-pool created
```

After creating the pool, services receive external IPs from that pool:

```bash theme={null}
kubectl get svc
NAME           TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)          AGE
app1-service   LoadBalancer   10.96.207.254   172.19.0.240     80:31514/TCP     4m52s
app2-service   LoadBalancer   10.96.157.80    172.19.0.241     80:32546/TCP     4m52s
kubernetes     ClusterIP      10.96.0.1       <none>           443/TCP          14m
```

Because these external IPs are on the same subnet as the host nodes, clients on that subnet will attempt to reach them via ARP. If no node responds to ARP for those IPs, traffic will not reach your services (curl will time out).

Example failing request before L2 announcement is configured:

```bash theme={null}
curl 172.19.0.240
# (no response / times out)
```

## 4. Configure the Cilium L2 Announcement policy

Create a CiliumL2AnnouncementPolicy to control which nodes and interfaces respond to ARP for which services. The example below:

* Matches services labeled app: myapp
* Excludes the control-plane node so only worker nodes respond
* Restricts interfaces with a regex '^eth\[0-9]+' (matches eth0, eth1, ...)
* Enables both externalIPs and loadBalancerIPs

l2announce.yaml:

```yaml theme={null}
apiVersion: "cilium.io/v2alpha1"
kind: CiliumL2AnnouncementPolicy
metadata:
  name: l2announce-policy
spec:
  serviceSelector:
    matchLabels:
      app: myapp
  nodeSelector:
    matchExpressions:
      - key: node-role.kubernetes.io/control-plane
        operator: DoesNotExist
  interfaces:
    - "^eth[0-9]+"
  externalIPs: true
  loadBalancerIPs: true
```

Apply the policy:

```bash theme={null}
kubectl apply -f l2announce.yaml
# ciliuml2announcementpolicy.cilium.io/l2announce-policy created
```

Describe the policy to confirm settings:

```bash theme={null}
kubectl describe ciliuml2announcementpolicy l2announce-policy
# Name: l2announce-policy
# Spec:
#   External IPs: true
#   Interfaces: ^eth[0-9]+
#   Load Balancer IPs: true
#   Node Selector: matchExpressions: node-role.kubernetes.io/control-plane DoesNotExist
#   Service Selector: matchLabels: app=myapp
```

## 5. Which node responds for each service IP? (Leases)

Cilium coordinates which node will answer ARP for a given external IP using Lease objects. You can list the leases in the kube-system namespace:

```bash theme={null}
kubectl get lease -n kube-system
NAME                                      HOLDER                 AGE
cilium-l2announce-default-app1-service    my-cluster-worker2     65s
cilium-l2announce-default-app2-service    my-cluster-worker      65s
...
```

The HOLDER field shows which node currently holds the lease and will therefore respond to ARP for the service IP.

## 6. Test connectivity and validate ARP

After the L2 announcement policy is active, clients on the same subnet can reach the LoadBalancer external IPs:

```bash theme={null}
curl 172.19.0.240
curl 172.19.0.241
# "This is app2"
```

Verify the local ARP table shows the service IP entries mapped to the node MAC addresses:

```bash theme={null}
arp -a | egrep "172.19.0.24[01]"
# ? (172.19.0.240) at 02:42:ac:13:00:04 [ether] on br-2c6b6be1a367
# ? (172.19.0.241) at 02:42:ac:13:00:03 [ether] on br-2c6b6be1a367
```

In Kind-based setups the MAC addresses correspond to the Docker/Kind bridge interfaces for node containers. You can inspect the node container interfaces to confirm which node IP/MAC answered ARP. Example:

```bash theme={null}
docker ps
# CONTAINER ID   IMAGE                NAMES
# ... my-cluster-worker2
# ... my-cluster-worker
docker exec my-cluster-worker2 ip addr show eth0
# ... inet 172.19.0.4/16 ...
# link/ether 02:42:ac:13:00:04
```

The link/ether value should match the ARP mapping for the external IP owned by that node.

## 7. Summary and quick references

* Enable l2announcements and kube-proxy replacement in Cilium (via Helm values or values.yaml).
* Create a CiliumLoadBalancerIPPool to allocate external IPs on the node subnet for LoadBalancer services.
* Create a CiliumL2AnnouncementPolicy to specify which services, nodes, and interfaces should respond to ARP (externalIPs and/or loadBalancerIPs).
* Inspect Leases to determine which node is announcing each external IP, and validate connectivity with curl and arp.

Key resources and commands:

| Resource / Object          | Purpose                                              | Example command                                                 |
| -------------------------- | ---------------------------------------------------- | --------------------------------------------------------------- |
| Cilium Helm values         | Enable kube-proxy replacement and l2announcements    | helm install cilium cilium/cilium -n kube-system -f values.yaml |
| CiliumLoadBalancerIPPool   | Provide external IPs for LoadBalancer services       | kubectl apply -f ipam.yaml                                      |
| CiliumL2AnnouncementPolicy | Control ARP announcements per service/node/interface | kubectl apply -f l2announce.yaml                                |
| Lease objects              | Show which node currently announces a service IP     | kubectl get lease -n kube-system                                |

Further reading and docs:

* [Cilium L2 Announcement docs](https://docs.cilium.io/) (search for "L2 announcements")
* [Kind - Kubernetes in Docker](https://kind.sigs.k8s.io/)
* [Helm documentation](https://helm.sh/docs/)

This completes the demonstration of Cilium's L2 announcement feature for local clusters.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/301b05fd-6c57-44ff-9a6d-9d8f794d2dde" />
</CardGroup>


# Demo LoadBalancer IPAM

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/BGP-External-Networking/Demo-LoadBalancer-IPAM/page

Demonstrates using Cilium LoadBalancer IPAM to assign external IPs from a configured pool to Kubernetes LoadBalancer Services in on-premises clusters.

In this lesson we demonstrate how to use Cilium's LoadBalancer IPAM to assign EXTERNAL-IP addresses to Kubernetes Services of type `LoadBalancer` in an on-premises cluster (where cloud-managed load balancers are not available).

<Frame>
  <img alt="A presentation slide showing the word &#x22;Demo&#x22; on the left and a teal curved panel on the right labeled &#x22;LoadBalancer IPAM.&#x22; The slide also has a small &#x22;© Copyright KodeKloud&#x22; notice in the corner." />
</Frame>

## Scenario

* Cluster runs on-premises (not on AWS/EKS/AKS).
* No external load-balancer controller (e.g., MetalLB) is installed.
* We have two sample deployments and corresponding Services; one Service is `LoadBalancer` type and will initially show `EXTERNAL-IP` as `<pending>`.

## Verify current Services

Check Services before deploying the sample apps:

```shell theme={null}
user1@control-plane:~$ kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP    4h18m
```

## Apply the sample Deployment and Services

Apply the manifest that creates two applications (`myapp` and `myapp2`) and their Services:

```shell theme={null}
user1@control-plane:~$ kubectl apply -f deployment.yaml
deployment.apps/myapp-deployment created
service/myapp-service created
deployment.apps/myapp2-deployment created
service/myapp2-service created
```

List Services again. Notice `myapp-service` is `LoadBalancer` type but its `EXTERNAL-IP` remains `<pending>` because no external IP provider exists in this on-prem cluster:

```shell theme={null}
user1@control-plane:~$ kubectl get svc
NAME           TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)           AGE
kubernetes     ClusterIP      10.96.0.1       <none>        443/TCP           4h19m
myapp-service  LoadBalancer   10.100.44.117   <pending>     80:32109/TCP      7s
myapp2-service ClusterIP      10.97.231.39    <none>        80/TCP            7s
```

## Provide external IPs with CiliumLoadBalancerIPPool

Instead of installing a separate external load balancer solution (for example, MetalLB), Cilium can allocate external IP addresses for `LoadBalancer` Services using a `CiliumLoadBalancerIPPool` resource.

Create a file named `lb-ipam.yaml` with the IP block you want Cilium to manage. Example:

```yaml theme={null}
apiVersion: "cilium.io/v2alpha1"
kind: CiliumLoadBalancerIPPool
metadata:
  name: "my-pool"
spec:
  blocks:
    - start: "172.19.255.1"
      stop:  "172.19.255.45"
  # Optional: restrict IP assignment to services matching these labels
  # serviceSelector:
  #   matchLabels:
  #     color: red
```

* The `blocks` range specifies the pool of external IPs that Cilium can allocate.
* Optionally use `serviceSelector` to limit assignments to Services with specific labels.

Apply the pool:

```shell theme={null}
user1@control-plane:~$ kubectl apply -f lb-ipam.yaml
ciliumloadbalancerippool.cilium.io/my-pool created
```

Now re-check Services:

```shell theme={null}
user1@control-plane:~$ kubectl get svc
NAME           TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
kubernetes     ClusterIP      10.96.0.1       <none>          443/TCP          4h22m
myapp-service  LoadBalancer   10.100.44.117   172.19.255.1    80:32109/TCP     2m25s
myapp2-service ClusterIP      10.97.231.39    <none>          80/TCP           2m25s
```

The `myapp-service` now has `EXTERNAL-IP` assigned (`172.19.255.1`), taken from the configured pool. Subsequent `LoadBalancer` Services will receive `.2`, `.3`, etc., up to the `stop` address.

<Callout icon="lightbulb">
  Cilium will allocate the EXTERNAL-IP from the pool, but you must ensure the cluster network and upstream routers/switches can route or reach those addresses. Typical methods include L2 advertisement (ARP/NDP) or BGP announcements so external clients can reach the assigned IPs.
</Callout>

<Callout icon="warning">
  If the assigned IPs are not reachable from your network, traffic to the external IP will fail—even though Kubernetes and Cilium show the IP as assigned. Configure ARP/NDP or BGP on your network infrastructure or use an appropriate routing/advertisement mechanism.
</Callout>

## Quick reference

| Resource                 | Purpose                                                                                           | Example / Notes                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| CiliumLoadBalancerIPPool | Defines a pool of external IP addresses for Cilium to allocate to Services of type `LoadBalancer` | YAML example shown above                                     |
| Service (LoadBalancer)   | Requests an external IP to expose the Service outside the cluster                                 | `kubectl get svc` shows `EXTERNAL-IP` populated by Cilium    |
| MetalLB                  | Alternative open-source load balancer for on-prem clusters                                        | [https://metallb.universe.tf/](https://metallb.universe.tf/) |

## Useful links and further reading

* Cilium documentation: [https://docs.cilium.io/](https://docs.cilium.io/)
* MetalLB: [https://metallb.universe.tf/](https://metallb.universe.tf/)

That’s the LoadBalancer IPAM workflow with Cilium: create a pool, apply it, and Cilium allocates external IPs for `LoadBalancer` Services (optionally scoped by label selectors).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/2951060d-4947-4ed5-87a9-f47f068fbe98" />
</CardGroup>
