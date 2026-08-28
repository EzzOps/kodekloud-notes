# pv-definition.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-vol1
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 500Mi
  gcePersistentDisk:
    pdName: pd-disk
    fsType: ext4
```

```yaml theme={null}
# pvc-definition.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

```yaml theme={null}
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: random-number-generator
spec:
  containers:
    - image: alpine
      name: alpine
      command: ["/bin/sh", "-c"]
      args: ["shuf -i 0-100 -n 1 >> /opt/number.out;"]
      volumeMounts:
        - mountPath: /opt
          name: data-volume
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: myclaim
```

Before applying the PV definition, ensure that the underlying disk exists. For example, on Google Cloud you would run:

```bash theme={null}
gcloud beta compute disks create \
  --size 1GB \
  --region us-east1 \
  pd-disk
```

***

## Dynamic Provisioning with Storage Classes

Dynamic provisioning automates the storage creation process. Instead of manually creating PVs, you use a storage class that defines a provisioner (like Google Cloud's persistent disk provisioner) to automatically create and attach a disk when a claim is made.

The dynamic provisioning workflow is as follows:

1. Create a StorageClass object using the API version `storage.k8s.io/v1` and specify parameters such as the provisioner (`kubernetes.io/gce-pd`) along with any additional configuration options.
2. In your PVC definition, reference the storage class by setting the `storageClassName` field.
3. When a PVC is created, the storage class's provisioner dynamically creates a new disk with the defined specifications, automatically generates a corresponding PV, and binds the PVC to that PV.

Below is an example for dynamic provisioning using a storage class:

```yaml theme={null}
# sc-definition.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
```

```yaml theme={null}
# pvc-definition.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: google-storage
  resources:
    requests:
      storage: 500Mi
```

```yaml theme={null}
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: random-number-generator
spec:
  containers:
    - image: alpine
      name: alpine
      command: ["/bin/sh", "-c"]
      args: ["shuf -i 0-100 -n 1 >> /opt/data-volume/output.txt"]
      volumeMounts:
        - mountPath: /opt
          name: data-volume
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: myclaim
```

With dynamic provisioning, there is no need for pre-created PV definitions; the storage class takes care of handling PV creation automatically when the PVC is submitted.

***

## Multiple Storage Classes

A key advantage of using storage classes is the ability to define different service levels tailored to various performance and replication needs. For example, you might use:

| Storage Class | Description                                         |
| ------------- | --------------------------------------------------- |
| Silver        | Uses standard persistent disks                      |
| Gold          | Uses SSD persistent disks                           |
| Platinum      | Uses SSD persistent disks with regional replication |

Below are sample YAML definitions for these storage classes:

```yaml theme={null}
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: silver
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  replication-type: none
```

```yaml theme={null}
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gold
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: none
```

```yaml theme={null}
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: platinum
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: regional-pd
```

When creating a PVC, simply specify the desired storage class name and Kubernetes will dynamically provision the volume with the characteristics defined.

***

<Callout icon="lightbulb">
  Storage classes enhance Kubernetes' storage management by automating the provisioning process and reducing manual intervention. By using dynamic provisioning, administrators can streamline resource allocation and ensure that storage resources match their application requirements.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/fbd7b99a-b2c1-4eda-9ef9-f5e0d7a20fce/lesson/c5a0cb55-fdfe-4262-91d9-0e92330a1942" />
</CardGroup>


# Automation and Tooling

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Compliance-and-Security-Frameworks/Automation-and-Tooling/page

This lesson reviews essential automation and tooling for cloud-native security, highlighting open source and commercial solutions across the application lifecycle.

In this lesson, we recap essential automation and tooling for cloud-native security. Throughout this course, you’ve explored multiple open source and commercial solutions. Here, we review those tools, highlight alternatives, and reference key resources such as the **Cloud Native Security Whitepaper** by SIG Security.

<Frame>
  ![The image is a cover for the "Cloud Native Security Whitepaper" by TAG Security, featuring a blue abstract background and a list of contributors and reviewers.](https://kodekloud.com/kk-media/image/upload/v1752880715/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Automation-and-Tooling/cloud-native-security-whitepaper-cover.jpg)
</Frame>

The Cloud Native Security Whitepaper provides foundational guidance authored by industry experts. To interactively explore security tools mapped to each phase of the application lifecycle, visit the Cloud Native Security Map:

<Frame>
  ![The image is a cover for a "Cloud Native Security Whitepaper" featuring a "Cloud Native Security Map," which serves as a guide for navigating the cloud native security landscape. It includes sections on development, distribution, deployment, runtime, security assurance, and compliance.](https://kodekloud.com/kk-media/image/upload/v1752880716/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Automation-and-Tooling/cloud-native-security-whitepaper-map.jpg)
</Frame>

<Callout icon="lightbulb">
  Explore the interactive map at [cnsmap.netfly.app](https://cnsmap.netfly.app) to discover security tools and best practices organized by **Develop**, **Distribute**, **Deploy**, and **Runtime** phases.
</Callout>

***

## Development Phase

The **Develop** phase emphasizes “shift-left” testing by integrating security early in code, Dockerfile, and infrastructure-as-code creation. Commit artifacts to repositories (GitHub, GitLab, etc.) with automated checks to:

* Block high-severity vulnerabilities when fixes exist
* Enforce non-root container execution
* Restrict allowed base images

<Frame>
  ![The image is a diagram illustrating a software development process, highlighting stages like coding, committing, distributing, deploying, and runtime, with an emphasis on "Shift-Left" for early testing and integration.](https://kodekloud.com/kk-media/image/upload/v1752880717/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Automation-and-Tooling/software-development-process-shift-left-diagram.jpg)
</Frame>

### Fuzz Testing with OSS-Fuzz

Google’s \[OSS-Fuzz]\[oss-fuzz] automates fuzz testing of open source projects to discover crashes and undefined behavior.

```python theme={null}
def parse_integer(input_string):
    try:
        return int(input_string)
    except ValueError:
        return "Error: Not a valid integer"
```

Below is a simple fuzz harness for `parse_integer`:

```python theme={null}
import random, string

def generate_random_string(length=10):
    charset = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(charset) for _ in range(length))

def fuzz_test_parse_integer(iterations=10):
    for _ in range(iterations):
        rand_in = generate_random_string(random.randint(1, 20))
        print(f"Testing: '{rand_in}' -> {parse_integer(rand_in)}")

fuzz_test_parse_integer()
```

Example output:

```plaintext theme={null}
Testing: '@123$%' -> Error: Not a valid integer
Testing: '87ab1' -> Error: Not a valid integer
Testing: '' -> Error: Not a valid integer
Testing: '42' -> 42
```

### IDE & CLI Security Extensions

* **\[Snyk VS Code Extension]\[snyk-vscode]**
* **Fabricate by Red Hat** (VS Code plugin)
* **\[kube-linter]\[kube-linter]** – Scan Kubernetes YAML:

```bash theme={null}
kube-linter lint pod.yaml
```

***

## Distribution Phase

In the **Distribute** phase, CI/CD pipelines build, test, and push container images to registries. Common tools include:

| CI/CD Pipeline Tool | Use Case                        |
| ------------------- | ------------------------------- |
| Tekton              | Kubernetes-native pipelines     |
| Jenkins             | Extensible automation server    |
| Travis CI           | Cloud-hosted continuous testing |
| CircleCI            | Container-based CI              |
| Flux CD             | GitOps continuous delivery      |
| Argo CD             | Declarative GitOps controller   |

Before building images, enforce policy compliance on manifests:

* **\[KubeSec]\[kubesec]** scans Kubernetes YAML for misconfigurations.
* **TeraScan** validates IaC (Terraform, Dockerfile, Helm, CloudFormation) against CIS, NIST, GDPR, HIPAA.

```plaintext theme={null}
Violation Details =
  Description: [Enabling S3 versioning allows easy recovery]
  file: modules/s3/main.tf
  Severity: 101
  Rule ID: AWS.S3Bucket.IAM.High.0370
```

<Callout icon="triangle-alert">
  Always validate manifests before image builds to prevent deployment of insecure configurations.
</Callout>

After validation, build and scan images:

| Scanner | Scope                                    | Example Command          |
| ------- | ---------------------------------------- | ------------------------ |
| Trivy   | Container images, filesystems, Git repos | trivy image myapp:latest |
| Clair   | Static image analysis via API            | API integration          |
| Grype   | Images & filesystem scanning             | grype myimage:tag        |
| Nuclei  | Custom checks via YAML templates         | nuclei -t templates/     |

To secure the software supply chain, use signing frameworks:

* **\[in-toto]\[in-toto]** – End-to-end supply chain security
* **\[Notary]\[notary]**, **\[TUF]\[tuf]**, **\[Sigstore]\[sigstore]**

<Frame>
  ![The image is a diagram illustrating a software development and distribution pipeline, featuring tools for build pipelines, app tests, container manifests, security tests, signing/trust, and container registry. It includes logos of various tools like Tekton, Jenkins, Trivy, and Dockerhub, organized under different stages from development to deployment.](https://kodekloud.com/kk-media/image/upload/v1752880718/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Automation-and-Tooling/software-development-distribution-pipeline-diagram.jpg)
</Frame>

***

## Deployment Phase

The **Deploy** phase covers pre-flight checks, observability, and incident response:

* **Pre-flight Checks**
  * **\[OPA Gatekeeper]\[gatekeeper]** – Policies in Rego
  * **\[Kyverno]\[kyverno]** – YAML-based policy management

* **Observability**
  * **\[Prometheus]\[prometheus]** + **\[Grafana]\[grafana]**
  * **\[Elasticsearch]\[elasticsearch]** + **\[Kibana]\[kibana]**
  * **\[OpenTelemetry]\[otel]**

* **Response & Investigation**
  * **\[Wazuh]\[wazuh]**
  * **\[Snort]\[snort]**
  * **\[Zeek]\[zeek]**

<Frame>
  ![The image illustrates a software development and deployment process, highlighting tools for pre-flight checks, observability, and response & investigation, with a dashboard showing incident response data.](https://kodekloud.com/kk-media/image/upload/v1752880719/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Automation-and-Tooling/software-development-deployment-process-dashboard.jpg)
</Frame>

***

## Runtime Phase

Once applications are live, enforce continuous security and reliability:

* **CIS Benchmarking**
  * **\[kube-bench]\[kube-bench]** – CIS checks for Kubernetes clusters:

```plaintext theme={null}
[FAIL] 1.1.1 Ensure --allow-privileged is false
[PASS] 1.1.2 Ensure --anonymous-auth is not set
```

* **Runtime Security**
  * **Falco** – System call monitoring
  * **Trivy** – Continuous workload scanning
  * **SPIFFE** – Workload identity via certificates

* **Service Mesh**
  * **Istio**, **Linkerd**

* **Storage Orchestration**
  * **Rook**, **Ceph**, **Gluster**

* **Access Management**
  * **Keycloak**, **Teleport**, **HashiCorp Vault**

<Frame>
  ![The image is a categorized list of DevOps tools used for development, distribution, and deployment processes, including sections for build pipelines, security tests, observability, and more. Each category contains specific tools like Jenkins, Prometheus, and Istio.](https://kodekloud.com/kk-media/image/upload/v1752880721/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Automation-and-Tooling/devops-tools-categorized-list-diagram.jpg)
</Frame>

***

## Summary

Map these tools to your cloud-native lifecycle for improved security and efficiency:

* **Develop**: Shift-left scanners & IDE plugins
* **Distribute**: CI/CD pipelines, manifest & image scanners, signing frameworks
* **Deploy**: Policy enforcement, observability, incident response
* **Runtime**: Continuous monitoring, service mesh, access & storage management

***

## Links and References

* OSS-Fuzz: [https://github.com/google/oss-fuzz](https://github.com/google/oss-fuzz)
* Snyk VS Code Extension: [https://marketplace.visualstudio.com/items?itemName=snyk-security.snyk-vulnerability-scanner](https://marketplace.visualstudio.com/items?itemName=snyk-security.snyk-vulnerability-scanner)
* kube-linter: [https://github.com/stackrox/kube-linter](https://github.com/stackrox/kube-linter)
* KubeSec: [https://github.com/controlplaneio/kubesec](https://github.com/controlplaneio/kubesec)
* in-toto: [https://github.com/in-toto/in-toto](https://github.com/in-toto/in-toto)
* Notary: [https://github.com/theupdateframework/notary](https://github.com/theupdateframework/notary)
* The Update Framework (TUF): [https://theupdateframework.io/](https://theupdateframework.io/)
* Sigstore: [https://sigstore.dev/](https://sigstore.dev/)
* OPA Gatekeeper: [https://github.com/open-policy-agent/gatekeeper](https://github.com/open-policy-agent/gatekeeper)
* Kyverno: [https://kyverno.io/](https://kyverno.io/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Grafana: [https://grafana.com/](https://grafana.com/)
* Elasticsearch: [https://www.elastic.co/elasticsearch](https://www.elastic.co/elasticsearch)
* Kibana: [https://www.elastic.co/kibana](https://www.elastic.co/kibana)
* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Wazuh: [https://wazuh.com/](https://wazuh.com/)
* Snort: [https://www.snort.org/](https://www.snort.org/)
* Zeek: [https://zeek.org/](https://zeek.org/)
* kube-bench: [https://github.com/aquasecurity/kube-bench](https://github.com/aquasecurity/kube-bench)
* Tekton: [https://tekton.dev/](https://tekton.dev/)
* Jenkins: [https://www.jenkins.io/](https://www.jenkins.io/)
* Travis CI: [https://travis-ci.org/](https://travis-ci.org/)
* CircleCI: [https://circleci.com/](https://circleci.com/)
* Flux CD: [https://fluxcd.io/](https://fluxcd.io/)
* Argo CD: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Docker Hub: [https://hub.docker.com/](https://hub.docker.com/)
* Harbor: [https://goharbor.io/](https://goharbor.io/)
* GitHub Container Registry: [https://github.com/features/packages](https://github.com/features/packages)
* Nexus Repository: [https://www.sonatype.com/product-nexus-repository](https://www.sonatype.com/product-nexus-repository)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/2d1969ad-ad49-4d47-93ca-493416c81c76/lesson/9157766e-1dc0-4d4e-8ffd-f4c384d5d2d5" />
</CardGroup>
