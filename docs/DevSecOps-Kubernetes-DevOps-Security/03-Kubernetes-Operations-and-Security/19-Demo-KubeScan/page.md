# Identify the kubelet process
ps -ef | grep kubelet

# Display the Kubelet configuration
cat /var/lib/kubelet/config.yaml
```

In `config.yaml`, confirm `anonymous` auth is disabled:

```yaml theme={null}
authentication:
  anonymous:
    enabled: false
```

> **triangle-alert** If anonymous auth is set to `true`, update the YAML, then reload and restart the service:

  ```bash theme={null}
  sudo systemctl daemon-reload
  sudo systemctl restart kubelet
  ```

## Installing kube-bench

[kube-bench on GitHub] is a Go-based tool from Aqua Security that automates CIS checks. To install on Ubuntu:

![The image shows a GitHub page for the "kube-bench" project, which is a Go application for checking Kubernetes security compliance. It includes details like release version, downloads, and a brief description of the tool.](https://kodekloud.com/kk-media/image/upload/v1752873758/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Kube-bench/kube-bench-github-page-security-compliance.jpg)

```bash theme={null}
# Download the latest .deb package (version may vary)
curl -L -O https://github.com/aquasecurity/kube-bench/releases/download/v0.3.1/kube-bench_0.3.1_linux_amd64.deb

# Install kube-bench
sudo apt install ./kube-bench_0.3.1_linux_amd64.deb -y
```

## Running kube-bench

Execute all CIS checks (master, node, etcd, control plane):

```bash theme={null}
kube-bench
```

Example summary:

```text theme={null}
== Summary ==
   42 checks PASS
    3 checks FAIL
   24 checks WARN
    0 checks INFO
```

![The image shows a terminal window displaying a security configuration summary for a Kubernetes worker node, with various checks marked as PASS, FAIL, or WARN. The interface appears to be from a remote connection tool, with a sidebar listing files and directories.](https://kodekloud.com/kk-media/image/upload/v1752873760/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Kube-bench/kubernetes-worker-node-security-summary.jpg)

You can target specific components:

| Component | Command             | Description                           |
| --------- | ------------------- | ------------------------------------- |
| All       | `kube-bench`        | Run all CIS checks                    |
| Master    | `kube-bench master` | Validate control plane configurations |
| Node      | `kube-bench node`   | Inspect worker node settings          |
| Etcd      | `kube-bench etcd`   | Check etcd data store security        |

```bash theme={null}
# Run checks on the master node
kube-bench master

# Run checks on worker nodes
kube-bench node
```

![The image shows a terminal window with instructions for editing Kubernetes configuration files, including encryption and pod specifications. It also displays a summary of checks with pass, fail, and warning statuses.](https://kodekloud.com/kk-media/image/upload/v1752873761/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Kube-bench/kubernetes-configuration-terminal-instructions.jpg)

## JSON Output and Filtering

For CI automation, output results in JSON and use `jq` to filter:

```bash theme={null}
kube-bench node --check 4.2.1 --json | jq
```

```json theme={null}
{
  "id": "4",
  "version": "1.5",
  "text": "Worker Node Security Configuration",
  "node_type": "node",
  "tests": [
    {
      "section": "4.2",
      "pass": 1,
      "fail": 0,
      "info": 0,
      "desc": "Kubelet",
      "results": [
        {
          "test_number": "4.2.1",
          "test_desc": "Ensure that the --anonymous-auth argument is set to false (Scored)",
          "status": "PASS",
          "remediation": "If using a Kubelet config file, edit the file to set authentication: anonymous: enabled to false..."
        }
      ]
    }
  ]
}
```

To extract failure count:

```bash theme={null}
total_fail=$(kube-bench node --check 4.2.1 --json | jq '.[].total_fail')
echo "Total fails: $total_fail"
```

![The image shows a terminal window with a list of security checks for a Kubernetes environment, indicating pass, warn, and fail statuses for each check. The interface appears to be part of a remote monitoring tool.](https://kodekloud.com/kk-media/image/upload/v1752873762/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Kube-bench/kubernetes-security-checks-terminal-window.jpg)

> **lightbulb** Ensure `jq` is installed (`sudo apt install jq`) to parse JSON output.

## Jenkins Integration

Integrate kube-bench into a Jenkins pipeline to enforce CIS compliance:

```groovy theme={null}
stage('K8S CIS Benchmark') {
  steps {
    script {
      parallel(
        'Master': {
          sh 'bash cis-master.sh'
        },
        'Etcd': {
          sh 'bash cis-etcd.sh'
        },
        'Kubelet': {
          sh 'bash cis-kubelet.sh'
        }
      )
    }
  }
}
```

Each script runs targeted checks, parses JSON, and exits with code `1` on failures. Example `cis-kubelet.sh`:

```bash theme={null}
#!/bin/bash

# Run specific Kubelet tests
total_fail=$(kube-bench node \
  --version 1.15 \
  --check 4.2.1,4.2.2 \
  --json | jq -r '.[].total_fail')

if [[ "$total_fail" -ne 0 ]]; then
  echo "CIS Benchmark Failed: Kubelet checks 4.2.1,4.2.2"
  exit 1
else
  echo "CIS Benchmark Passed: Kubelet checks 4.2.1,4.2.2"
fi
```

Repeat similar scripts for `cis-master.sh` (e.g., checks 1.1.12, 1.2.1) and `cis-etcd.sh` (e.g., check 2.2).

> **triangle-alert** Failing any CIS test will mark the Jenkins stage as failed. Adjust thresholds as needed.

## Conclusion

By combining **kube-bench** with JSON output and `jq` filters, you can automate CIS Kubernetes Benchmark checks in your CI/CD pipeline. These scans help ensure your cluster adheres to security best practices before production deployment.

## References

* [CIS Kubernetes Benchmark]: https://www.cisecurity.org/benchmark/kubernetes/
* [kube-bench on GitHub]: https://github.com/aquasecurity/kube-bench
* [jq Manual]: https://stedolan.github.io/jq/

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/abe4709d-7317-4c53-8877-e77595764adb)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/84f7a4ea-c8cf-4dac-b055-42d05495eb52)


# Demo KubeScan

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Demo-KubeScan/page

This guide explains how to deploy OctarineSec KubeScan for continuous assessment and monitoring of Kubernetes workloads.

In this guide, you’ll learn how to deploy OctarineSec KubeScan to continuously assess and monitor Kubernetes workloads. KubeScan computes a risk score between **0 (no risk)** and **10 (high risk)** for each workload based on configurable runtime rules.

![The image shows a GitHub repository page for "kube-scan" by "octarinesec," displaying files, commit history, and repository details. The page includes options to view code, issues, pull requests, and more.](https://kodekloud.com/kk-media/image/upload/v1752873763/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-KubeScan/kube-scan-github-repo-octarinesec.jpg)

## Prerequisites

* A Kubernetes cluster (v1.16+)
* `kubectl` configured for your cluster
* Docker CLI for building and pushing images
* Git for cloning the repository

## 1. Clone & Build

Since the official images might not be publicly pullable, clone the source and build both UI and server components:

```bash theme={null}
git clone https://github.com/octarinesec/kube-scan.git
cd kube-scan
