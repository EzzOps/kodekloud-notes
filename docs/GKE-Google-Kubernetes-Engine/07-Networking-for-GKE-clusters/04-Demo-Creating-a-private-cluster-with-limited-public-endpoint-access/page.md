# Demo Creating a private cluster with limited public endpoint access

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/Networking-for-GKE-clusters/Demo-Creating-a-private-cluster-with-limited-public-endpoint-access/page

This hands-on tutorial guides you in creating a private GKE cluster with limited public endpoint access and explores related configurations.

In this hands-on tutorial, you will:

* Provision a **private Google Kubernetes Engine (GKE) cluster** with no external node IPs
* Explore how **private endpoints** restrict API access
* Attempt to authorize an external IP and observe the limitation
* Create a **public-endpoint cluster** with **Master Authorized Networks** for controlled external access

**Prerequisites**

* A Google Cloud project (set via `gcloud config set project [PROJECT_ID]`)
* [Cloud Shell](https://cloud.google.com/shell/docs/)
* [gcloud CLI](https://cloud.google.com/sdk/gcloud) installed

> Verify your active project:
>
> ```bash theme={null}
> gcloud config set project clgcporg8-037
> ```

<Frame>
  ![The image contains the text "Demo: Creating a Private Cluster" on a plain white background, with a copyright notice for KodeKloud.](../../../../images/kodekloud.com/kk-media/image/upload/v1752875677/notes-assets/images/GKE-Google-Kubernetes-Engine-Demo-Creating-a-private-cluster-with-limited-public-endpoint-access/demo-creating-private-cluster-kodekloud.jpg)
</Frame>

## 1. Set Your Compute Zone

Configure your default zone to `us-west1-a`:

```bash theme={null}
gcloud config set compute/zone us-west1-a
```

## 2. Create a Private-Endpoint Cluster

We’ll build a VPC-native cluster called `gke-deep-dive` with:

| Feature                | Description                                      |
| ---------------------- | ------------------------------------------------ |
| Private nodes          | Nodes with **no external IP**                    |
| Private endpoint       | Control plane accessible **only via private IP** |
| IP aliasing            | Pod and service CIDRs managed by GKE             |
| 10 GB PD-standard disk | Persistent disk for node OS and kubelet data     |

```bash theme={null}
gcloud container clusters create gke-deep-dive \
  --num-nodes=1 \
  --disk-type=pd-standard \
  --disk-size=10 \
  --create-subnetwork name=gke-deep-dive-subnet \
  --enable-ip-alias \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.32/28 \
  --zone=us-west1-a
```

<Callout icon="lightbulb">
  Cluster provisioning may take **10–15 minutes**.\
  You can monitor progress in the Cloud Console or via `gcloud container operations list`.
</Callout>

## 3. Verify the Private Cluster Configuration

Inspect the cluster to confirm private nodes and endpoint settings:

```bash theme={null}
gcloud container clusters describe gke-deep-dive --zone=us-west1-a
```

Look for:

```yaml theme={null}
privateClusterConfig:
  enablePrivateNodes: true
  masterIpv4CidrBlock: 172.16.0.32/28
  privateEndpoint: true
  publicEndpoint: false
```

> GKE still creates a public endpoint for Google-managed operations, but by default it is **not** accessible from outside the VPC.

## 4. Try Authorizing an External IP

Fetch your Cloud Shell VM’s public IP and attempt to whitelist it:

```bash theme={null}
MY_IP=$(dig +short myip.opendns.com @resolver1.opendns.com)
echo $MY_IP/32

gcloud container clusters update gke-deep-dive \
  --zone=us-west1-a \
  --enable-master-authorized-networks \
  --master-authorized-networks $MY_IP/32
```

You will receive:

```text theme={null}
ERROR: (gcloud.container.clusters.update) ...
Invalid master authorized networks: network "35.247.165.143/32" is not a reserved network,
which is required for private endpoints.
```

<Callout icon="triangle-alert">
  Private-endpoint clusters only accept **reserved VPC networks** for API access.\
  External public IPs **cannot** be added to master authorized networks in this configuration.
</Callout>

## 5. Create a Public-Endpoint Cluster with Master Authorized Networks

To allow restricted external API access, we’ll spin up `gke-deep-dive-public`:

```bash theme={null}
gcloud container clusters create gke-deep-dive-public \
  --num-nodes=1 \
  --disk-type=pd-standard \
  --disk-size=10 \
  --subnetwork=gke-deep-dive-subnet \
  --enable-ip-alias \
  --enable-private-nodes \
  --master-ipv4-cidr=172.16.0.16/28 \
  --zone=us-west1-a
```

<Callout icon="lightbulb">
  This cluster also takes **10–15 minutes** to provision.
</Callout>

### 5.1 Authorize Your External IP

Retrieve your IP again and whitelist it for the new cluster:

```bash theme={null}
MY_IP=$(dig +short myip.opendns.com @resolver1.opendns.com)
gcloud container clusters update gke-deep-dive-public \
  --zone=us-west1-a \
  --enable-master-authorized-networks \
  --master-authorized-networks $MY_IP/32
```

### 5.2 Confirm Master Authorized Networks

Run:

```bash theme={null}
gcloud container clusters describe gke-deep-dive-public --zone=us-west1-a
```

You should see:

```yaml theme={null}
masterAuthorizedNetworkConfig:
  cidrBlocks:
  - cidrBlock: 35.247.165.143/32
    enabled: true
privateClusterConfig:
  enablePrivateNodes: true
  masterIpv4CidrBlock: 172.16.0.16/28
  privateEndpoint: false
  publicEndpoint: true
```

## 6. Access Your Public-Endpoint Cluster

Configure `kubectl` and list nodes:

```bash theme={null}
gcloud container clusters get-credentials gke-deep-dive-public --zone=us-west1-a
kubectl get nodes
```

You should see one node in the `READY` state.

## 7. Compare Your Clusters

List all clusters in the zone:

```bash theme={null}
gcloud container clusters list --zone=us-west1-a
```

| Cluster Name         | Private Endpoint | Public Endpoint | Master Auth Networks |
| -------------------- | ---------------- | --------------- | -------------------- |
| gke-deep-dive        | Enabled          | Disabled        | N/A                  |
| gke-deep-dive-public | Disabled         | Enabled         | Your IP/32           |

***

## References

* [GKE Private Clusters](https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept)
* [Master Authorized Networks](https://cloud.google.com/kubernetes-engine/docs/how-to/authorized-networks)
* [VPC-native Clusters & IP Aliasing](https://cloud.google.com/kubernetes-engine/docs/concepts/ip-aliasing)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gke-google-kubernetes-engine/module/e39613e2-4771-4eaa-a8cf-6360f282895a/lesson/4fd4e74b-71f3-493f-a86b-c991a970d3a2" />
</CardGroup>
