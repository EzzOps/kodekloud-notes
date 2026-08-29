# Create a resource group
az group create \
  --name DevSecOpsRG \
  --location eastus

# Deploy the VM
az deployment group create \
  --resource-group DevSecOpsRG \
  --template-file azuredeploy.json \
  --parameters @azuredeploy.parameters.json
```

### Google Cloud Platform (gcloud) Commands

Or spin up a GCP instance:

```bash theme={null}
gcloud compute instances create devsecops-cloud \
  --zone=us-central1-a \
  --machine-type=n1-standard-4 \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --tags=http-server,https-server
```

### Local VirtualBox Deployment (Vagrant)

For local testing with Vagrant:

```bash theme={null}
# Start the VM
vagrant up --provider=virtualbox
```

## Software Installation

SSH into your VM and run the installer:

```bash theme={null}
ssh ubuntu@<VM_PUBLIC_IP>
git clone https://github.com/yourrepo/devsecops-vm-setup.git
cd devsecops-vm-setup
chmod +x install.sh
./install.sh
```

### Installation Breakdown

| Component                 | Version | Purpose                       |
| ------------------------- | ------- | ----------------------------- |
| Docker CE                 | Latest  | Container runtime             |
| kubeadm, kubelet, kubectl | v1.21.x | Kubernetes cluster tools      |
| OpenJDK                   | 8       | Jenkins runtime               |
| Maven                     | 3.6.x   | Java build automation         |
| Jenkins LTS               | 2.xx.x  | Continuous Integration server |

<Callout icon="lightbulb">
  The `install.sh` script updates packages, installs Docker CE, sets up Kubernetes tools, initializes a single-node cluster, and deploys Jenkins.
</Callout>

## Cluster Configuration

Enable pod scheduling on the master node:

```bash theme={null}
kubectl taint nodes --all node-role.kubernetes.io/master-
```

Verify node readiness:

```bash theme={null}
kubectl get nodes
```

## Download Resources

Grab all templates and scripts from the GitHub repo:

* [azuredeploy.json](https://github.com/yourrepo/devsecops-vm-setup/blob/main/azuredeploy.json)
* [azuredeploy.parameters.json](https://github.com/yourrepo/devsecops-vm-setup/blob/main/azuredeploy.parameters.json)
* [Vagrantfile](https://github.com/yourrepo/devsecops-vm-setup/blob/main/Vagrantfile)
* [install.sh](https://github.com/yourrepo/devsecops-vm-setup/blob/main/install.sh)

For more details, visit the [Azure Documentation](https://docs.microsoft.com/azure/) and [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/324472ab-2f3c-4fa3-a3e1-20c910fc4481" />
</CardGroup>


# DAST Basics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/DAST-Basics/page

This article explains Dynamic Application Security Testing (DAST), its characteristics, advantages, limitations, and how it differs from Static Application Security Testing (SAST).

Dynamic Application Security Testing (DAST) simulates real-world attacks against a running application to uncover security flaws that only appear in a live environment. Unlike Static Application Security Testing (SAST), DAST has no access to source code—it interacts with the application’s interfaces (e.g., HTTP endpoints) to discover vulnerabilities.

## What Is Dynamic Application Security Testing (DAST)?

DAST evaluates an application from the outside in, detecting issues that might be missed when scanning code alone.

<Callout icon="lightbulb">
  DAST is best suited for QA or pre-production environments. Running DAST in production can reveal critical flaws—but must be done with caution to avoid service disruptions.
</Callout>

Key characteristics:

* Executed against a live, deployed application
* No access to source code or binaries
* Ideal for catching misconfiguration and runtime issues
* Focuses on externally visible vulnerabilities

## Common Vulnerabilities Detected by DAST

DAST tools target many OWASP Top 10 risks. The table below shows typical findings:

| Vulnerability           | Description                                        | OWASP Category                        |
| ----------------------- | -------------------------------------------------- | ------------------------------------- |
| Cross-Site Scripting    | Injection of malicious scripts into client pages   | A03:2021 – XSS                        |
| SQL Injection           | Malicious SQL statements altering database queries | A03:2021 – Injection                  |
| Command Injection       | Execution of system commands via user inputs       | A05:2021 – Security Misconfigurations |
| Insecure Configurations | Weak server settings, default credentials, etc.    | A05:2021 – Security Misconfigurations |

## Pros and Cons of DAST

### Advantages

| Advantage                     | Details                                                                                                                        |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Technology Independence       | Works across languages and frameworks—no code parsing required.                                                                |
| Low False-Positive Rate       | According to the [OWASP Benchmark Project](https://owasp.org/www-project-benchmark/), DAST tools report fewer false positives. |
| Configuration Issue Discovery | Exposes runtime misconfigurations that static analysis might overlook.                                                         |

### Limitations

| Limitation           | Details                                                                           |
| -------------------- | --------------------------------------------------------------------------------- |
| Limited Scalability  | Requires expert-crafted test cases; difficult to automate fully at scale.         |
| No Code Visibility   | Cannot pinpoint the exact line in source code where a flaw originates.            |
| Performance Overhead | Scans can take hours or days, delaying feedback and increasing remediation costs. |

<Frame>
  ![The image is an informational graphic about DAST (Dynamic Application Security Testing), highlighting its features, advantages, and limitations in identifying security vulnerabilities in applications. It contrasts DAST with SAST (Static Application Security Testing) and lists specific vulnerabilities DAST can detect, such as cross-site scripting and SQL injection.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873606/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-DAST-Basics/dast-security-testing-graphic-features.jpg)
</Frame>

## DAST vs. SAST

Comparing Static vs. Dynamic analysis:

| Aspect              | SAST                                              | DAST                                              |
| ------------------- | ------------------------------------------------- | ------------------------------------------------- |
| Analysis Type       | Static source-code scanning                       | Runtime interaction with a live application       |
| Visibility          | Pinpoints issues to specific code lines           | Identifies externally visible flaws only          |
| False-Positive Rate | Can generate more false positives without context | Generally lower when properly configured          |
| Use Case            | Early in SDLC, developer feedback                 | QA, pre-production, and (with caution) production |

<Callout icon="triangle-alert">
  Running DAST against production workloads can impact performance. Schedule scans during low-traffic windows and ensure proper monitoring.
</Callout>

## Next Steps

In the following lesson, we’ll use [OWASP ZAP](https://www.zaproxy.org/) to perform a dynamic scan on an application deployed in a Kubernetes cluster. You'll learn how to:

1. Configure OWASP ZAP for automated scanning
2. Interpret scan reports to prioritize fixes
3. Integrate DAST into a CI/CD pipeline

## Links and References

* [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
* [OWASP ZAP](https://www.zaproxy.org/)
* [OWASP Benchmark Project](https://owasp.org/www-project-benchmark/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/606da94b-5581-42bc-84b6-a6cada1c8196" />
</CardGroup>
