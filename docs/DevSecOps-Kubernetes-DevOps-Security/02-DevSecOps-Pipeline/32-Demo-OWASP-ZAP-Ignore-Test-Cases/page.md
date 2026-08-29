# Demo OWASP ZAP Ignore Test Cases

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Demo-OWASP-ZAP-Ignore-Test-Cases/page

This article demonstrates upgrading Spring Security, configuring OWASP ZAP to ignore warnings, and adjusting Dependency-Check thresholds for continuous security in CI/CD pipelines.

In this walkthrough, we’ll demonstrate how to

1. Upgrade a vulnerable Spring Security dependency.
2. Configure OWASP ZAP API scan to ignore expected warnings.
3. Adjust OWASP Dependency-Check thresholds and verify results.

Integrating these steps into your CI/CD pipeline ensures continuous security hygiene for new code and dependencies.

***

## 1. Upgrade Spring Security Dependency

Run your Trivy scan to identify current vulnerabilities:

```bash theme={null}
bash trivy-k8s-scan.sh
```

```text theme={null}
siddharth67/numeric-app:98a731c56919f167918d79d396d327c4faf6c32 (alpine 3.13.5)
Total: 0 (LOW: 0, MEDIUM: 0, HIGH: 0)

home/k8s-pipeline/app.jar
Total: 2 (LOW: 0, MEDIUM: 0, HIGH: 2)
+-----------------------------------------------------------+
| LIBRARY                                                   |
| org.springframework.security:spring-security-core         |
|   CVE-2021-22112 | HIGH | 5.3.5.RELEASE → 5.4.4           |
| org.springframework.security:spring-security-web          |
|   (also fixed in 5.4.4)                                   |
+-----------------------------------------------------------+
Exit Code: 0
Image scanning passed. No vulnerabilities found
```

The scan reports two **HIGH** issues in Spring Security. We’ll upgrade both to **5.4.4**.

Open `pom.xml` and locate your parent and properties:

```xml theme={null}
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>2.3.5.RELEASE</version>
</parent>
...
<properties>
  <java.version>1.8</java.version>
</properties>
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  <!-- other dependencies -->
</dependencies>
```

Hover over the parent in your IDE to confirm Spring Security is at `5.3.5.RELEASE`. Then override it by adding the following to the `<properties>` block:

![The image shows a screenshot of a development environment, likely an IDE, displaying a POM file with a list of dependencies and their versions. The interface includes a file explorer on the left and a code editor on the right.](https://kodekloud.com/kk-media/image/upload/v1752873644/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-OWASP-ZAP-Ignore-Test-Cases/ide-pom-file-dependencies-screenshot.jpg)

```xml theme={null}
<project ...>
  <properties>
    <java.version>1.8</java.version>
    <spring.security.version>5.4.4</spring.security.version>
  </properties>
  <!-- rest of pom -->
</project>
```

Rebuild your project and rerun the Trivy scan. You should now see **no high-severity** Spring Security vulnerabilities.

***

## 2. Configure OWASP ZAP API Scan to Ignore Specific Warnings

By default, ZAP flags all rule violations, even those expected by your API. For example:

```bash theme={null}
bash zap.sh
...
WARN-New: Unexpected Content-Type returned [10001] x 3
  http://...:31933/ (200)
  http://...:31933/compare/10 (200)
  http://...:31933/compare/10/ (200)
FAIL-New: 0 WARN-New: 1 PASS: 115
Exit Code: 2
```

### 2.1 Generate Default ZAP Configuration

Use the OpenAPI scan script to generate a baseline `gen_file`:

```bash theme={null}
docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-weekly \
  zap-api-scan.py \
    -t http://devsecops-demo.eastus.cloudapp.azure.com:31933/v3/api-docs \
    -f openapi \
    -g gen_file
```

This creates a rules file where **all** rules are set to `WARN`.

![The image shows a list of security warnings and vulnerabilities from an OWASP ZAP scan, displayed in a web browser.](https://kodekloud.com/kk-media/image/upload/v1752873645/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-OWASP-ZAP-Ignore-Test-Cases/owasp-zap-security-warnings-list.jpg)

### 2.2 Define Ignored Rules

Create a `zap_rules` file at your repo root to ignore specific rule IDs:

```text theme={null}
