# Demo Hands on creating complete infrastructure stack using gcloud CLI

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Development-CICD/Demo-Hands-on-creating-complete-infrastructure-stack-using-gcloud-CLI/page

Step-by-step gcloud CLI walkthrough to provision a GCP infrastructure stack including service account and IAM, VPC, subnet, firewall rules, a private Compute Engine VM, and cleanup.

Hello and welcome back.

In this walkthrough we'll provision a simple, production-like infrastructure stack in Google Cloud using only the gcloud CLI from Cloud Shell. The steps cover service account creation and IAM bindings, networking (VPC, subnet, firewall), and launching a Compute Engine VM that uses the service account. All commands shown are executed in Cloud Shell — replace the sample project `kodekloud-gcp-training` with your target project ID where needed.

<Frame>
  <img alt="A presentation slide reading &#x22;Hands-On - Create Complete Infrastructure Stack using gcloud cli&#x22; with a large teal curved shape on the right. The word &#x22;Demo&#x22; is shown in white inside the teal shape." />
</Frame>

We will:

* Create a service account.
* Grant the service account necessary IAM roles.
* Create a VPC, a subnet, and firewall rules.
* Launch a Compute Engine instance using the service account (no external IP).
* Verify resources and clean them up when finished.

<Callout icon="lightbulb">
  You don't need to memorize every gcloud flag. Learn the command structure and reference the gcloud CLI docs: [https://cloud.google.com/sdk/gcloud/reference](https://cloud.google.com/sdk/gcloud/reference). Use this guide as a step-by-step reference for common infra tasks.
</Callout>

***

## Prerequisites

Activate Cloud Shell and set the intended project (replace the project ID if different):

```bash theme={null}
gcloud config set project kodekloud-gcp-training
```

***

## Quick resource summary

| Resource          |                             Purpose | Example command                                                                                                           |
| ----------------- | ----------------------------------: | ------------------------------------------------------------------------------------------------------------------------- |
| Service account   |           Authentication for the VM | `gcloud iam service-accounts create demo-sa ...`                                                                          |
| IAM role binding  | Grant compute & storage permissions | `gcloud projects add-iam-policy-binding ... --role=roles/compute.instanceAdmin.v1`                                        |
| VPC (custom)      |                    Isolated network | `gcloud compute networks create demo-vpc --subnet-mode=custom`                                                            |
| Subnet            |     Regional IP range for instances | `gcloud compute networks subnets create demo-subnet --network=demo-vpc --region=us-central1 --range=10.0.1.0/24`          |
| Firewall rules    |                Allow SSH/HTTP/HTTPS | `gcloud compute firewall-rules create allow-ssh --network=demo-vpc --allow=tcp:22`                                        |
| Compute Engine VM |      Workload using service account | `gcloud compute instances create demo-vm --network-interface=subnet=demo-subnet,no-address --service-account=demo-sa@...` |

***

## 1. Create a service account

Create a service account named `demo-sa` with a display name and description:

```bash theme={null}
gcloud iam service-accounts create demo-sa \
  --display-name="Demo Service Account" \
  --description="Service account for demo infrastructure"
```

Verify the service account (CLI or Cloud Console):

```bash theme={null}
gcloud iam service-accounts list --filter="displayName:Demo Service Account"
```

Sample output:

```text theme={null}
DISPLAY NAME: Demo Service Account
EMAIL: demo-sa@kodekloud-gcp-training.iam.gserviceaccount.com
DISABLED: False
```

***

## 2. Grant IAM roles to the service account

Grant the permissions the VM needs to manage compute resources and access storage.

* Grant Compute Instance Admin (VM lifecycle and instance operations):

```bash theme={null}
gcloud projects add-iam-policy-binding kodekloud-gcp-training \
  --member=serviceAccount:demo-sa@kodekloud-gcp-training.iam.gserviceaccount.com \
  --role=roles/compute.instanceAdmin.v1
```

* Grant Storage Object Viewer (read-only access to Cloud Storage objects):

```bash theme={null}
gcloud projects add-iam-policy-binding kodekloud-gcp-training \
  --member=serviceAccount:demo-sa@kodekloud-gcp-training.iam.gserviceaccount.com \
  --role=roles/storage.objectViewer
```

Note: If your project has policy bindings with conditions, gcloud may prompt to choose a condition (e.g., choose `2` for None unless you need a specific condition).

***

## 3. Create a VPC network

Create a custom-mode VPC named `demo-vpc` with regional BGP routing:

```bash theme={null}
gcloud compute networks create demo-vpc \
  --subnet-mode=custom \
  --bgp-routing-mode=regional
```

Example creation output includes the network name and mode. Instances on the new network require firewall rules to be reachable — we'll add those next.

Verify the network:

```bash theme={null}
gcloud compute networks describe demo-vpc
```

***

## 4. Create a subnet

Create a regional subnet `demo-subnet` in `us-central1` with CIDR `10.0.1.0/24` and attach it to `demo-vpc`:

```bash theme={null}
gcloud compute networks subnets create demo-subnet \
  --network=demo-vpc \
  --range=10.0.1.0/24 \
  --region=us-central1
```

Verify the subnet:

```bash theme={null}
gcloud compute networks subnets describe demo-subnet --region=us-central1
```

***

## 5. Create firewall rules

Allow SSH (22), HTTP (80), and HTTPS (443) ingress from anywhere to instances on `demo-vpc`. Create one rule per port for clarity and minimal privileges.

Allow SSH:

```bash theme={null}
gcloud compute firewall-rules create allow-ssh \
  --network=demo-vpc \
  --allow=tcp:22 \
  --source-ranges=0.0.0.0/0 \
  --description="Allow SSH traffic"
```

Allow HTTP:

```bash theme={null}
gcloud compute firewall-rules create allow-http \
  --network=demo-vpc \
  --allow=tcp:80 \
  --source-ranges=0.0.0.0/0 \
  --description="Allow HTTP traffic"
```

Allow HTTPS:

```bash theme={null}
gcloud compute firewall-rules create allow-https \
  --network=demo-vpc \
  --allow=tcp:443 \
  --source-ranges=0.0.0.0/0 \
  --description="Allow HTTPS traffic"
```

List firewall rules for the VPC:

```bash theme={null}
gcloud compute firewall-rules list --filter="network:demo-vpc"
```

***

## 6. Create a Compute Engine instance

Create a VM named `demo-vm` in zone `us-central1-a` that uses the `demo-sa` service account and is attached to `demo-subnet` without an external IP (private-only instance):

```bash theme={null}
gcloud compute instances create demo-vm \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=demo-subnet,no-address \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=10GB \
  --boot-disk-type=pd-standard \
  --service-account=demo-sa@kodekloud-gcp-training.iam.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform
```

Sample output:

```text theme={null}
WARNING: You have selected a disk size of under [200GB]. This may result in poor I/O performance. For more information, see: https://developers.google.com/compute/docs/disks#performance.
Created [https://www.googleapis.com/compute/v1/projects/kodekloud-gcp-training/zones/us-central1-a/instances/demo-vm].
NAME: demo-vm
ZONE: us-central1-a
MACHINE_TYPE: e2-micro
INTERNAL_IP: 10.0.1.2
EXTERNAL_IP:
STATUS: RUNNING
```

Verify instance details (note the zone format `us-central1-a`):

```bash theme={null}
gcloud compute instances describe demo-vm --zone=us-central1-a
```

You can also confirm using the Compute Engine page in the GCP Console.

***

<Callout icon="warning">
  Cleanup is important to avoid unexpected charges. Delete resources in reverse order of creation and confirm prompts. If you plan to keep resources, consider applying labels and budgets to manage costs.
</Callout>

## 7. Cleanup (delete resources)

When you're finished, remove resources in reverse creation order. Answer `Y` to confirmation prompts.

Delete the VM:

```bash theme={null}
gcloud compute instances delete demo-vm --zone=us-central1-a
```

Delete firewall rules:

```bash theme={null}
gcloud compute firewall-rules delete allow-ssh
gcloud compute firewall-rules delete allow-http
gcloud compute firewall-rules delete allow-https
```

Delete the subnet:

```bash theme={null}
gcloud compute networks subnets delete demo-subnet --region=us-central1
```

Delete the VPC:

```bash theme={null}
gcloud compute networks delete demo-vpc
```

Delete the service account:

```bash theme={null}
gcloud iam service-accounts delete demo-sa@kodekloud-gcp-training.iam.gserviceaccount.com
```

After these deletions the resources created in this demo should be removed and no longer show in the console.

***

## Closing notes

This guide demonstrated how to provision a basic infrastructure stack using only gcloud CLI commands: creating a service account, assigning IAM roles, creating a custom VPC/subnet, adding firewall rules, and launching a private Compute Engine VM using the service account. For production environments, automate and parameterize these steps using scripts or infrastructure-as-code tools such as Terraform.

Further reading and references:

* gcloud CLI reference: [https://cloud.google.com/sdk/gcloud/reference](https://cloud.google.com/sdk/gcloud/reference)
* VPC networks overview: [https://cloud.google.com/vpc/docs/vpc](https://cloud.google.com/vpc/docs/vpc)
* Compute Engine instances: [https://cloud.google.com/compute/docs/instances](https://cloud.google.com/compute/docs/instances)

See you next time.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/02c15300-8e2a-455b-9032-0d4630391b66/lesson/1832cb95-750c-4331-8c4a-b8d3899e0a81" />
</CardGroup>
