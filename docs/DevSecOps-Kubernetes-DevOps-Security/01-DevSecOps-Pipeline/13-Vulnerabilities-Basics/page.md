# Vulnerabilities Basics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Vulnerabilities-Basics/page

This lesson defines vulnerabilities and explores their relationship to exploits, threats, and risks while outlining a process for scanning, assessing, and remediating them.

In this lesson, we’ll define vulnerabilities, explore their relationship to exploits, threats, and risks, and walk through a standard process for scanning, assessing, and remediating them. Future modules will provide hands-on examples using tools like [Dependency Check](https://owasp.org/www-project-dependency-check/), [Trivy](https://github.com/aquasecurity/trivy), [OPA Conftest](https://www.conftest.dev/), and [Kubesec](https://kubesec.io/) to secure application code, container images, and Kubernetes resources.

***

## Key Concepts

| Term          | Definition                                                                                                  | Example                                     |
| ------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| Vulnerability | A flaw or bug in software that attackers can exploit.                                                       | SQL injection, broken authentication        |
| Exploit       | A script or technique that takes advantage of a vulnerability to perform malicious activity.                | Remote code execution, unauthorized mining  |
| Threat        | Any potential cause of an unwanted security incident, such as an attacker or malware.                       | Phishing campaign, zero-day malware         |
| Risk          | The potential for loss or damage when a threat exploits a vulnerability. Calculated by severity and impact. | High-severity CVE in production environment |

<Callout icon="lightbulb">
  A robust vulnerability management program reduces the window of exposure and lowers the overall security risk to your applications and infrastructure.
</Callout>

***

## Vulnerability Scanning & Databases

Vulnerability scanners inspect code, container images, and configuration files, then compare findings against public vulnerability repositories. Once confirmed, issues are catalogued with unique identifiers.

| Database / System                   | Description                                                                                        |
| ----------------------------------- | -------------------------------------------------------------------------------------------------- |
| [NVD](https://nvd.nist.gov/)        | The U.S. government’s repository of publicly disclosed vulnerabilities.                            |
| [CVE](https://cve.mitre.org/)       | Unique IDs for known cybersecurity flaws (e.g., CVE-2021-34527).                                   |
| [CVSS](https://www.first.org/cvss/) | A scoring framework (0–10) that measures vulnerability severity and potential impact.              |
| [CWE](https://cwe.mitre.org/)       | A taxonomy of software weaknesses, helping teams understand root causes and prevention strategies. |

***

## Vulnerability Assessment

Once scanning completes, generate an assessment report that includes:

* **Severity**: CVSS score or custom risk rating
* **Vulnerability Age**: Time since public disclosure
* **Exploit Availability**: Whether proof-of-concept code exists
* **Remediation Guidance**: Patching instructions or workarounds

<Callout icon="triangle-alert">
  Always address high-severity vulnerabilities with known exploits before lower-risk items. Automate prioritization using your CI/CD pipeline.
</Callout>

***

## Remediation Workflow

1. **Prioritize**
   * Rank CVEs by CVSS score, exploitability, and business impact.
2. **Remediate**
   * Update or patch affected dependencies and configurations.
   * Apply security fixes in code and container images.
3. **Verify & Monitor**
   * Re-scan to confirm fixes.
   * Implement continuous monitoring and alerting for new vulnerabilities.

***

<Frame>
  ![The image explains the concepts of vulnerability, exploit, threat, and risk, and outlines the process of vulnerability scanning, assessment, and remediation. It also mentions terms like CVE, CVSS, and NVD related to cybersecurity.](../../../../images/kodekloud.com/kk-media/image/upload/v1752873730/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Vulnerabilities-Basics/vulnerability-exploit-threat-risk-cybersecurity.jpg)
</Frame>

***

## Next Steps

In the following lessons, you’ll perform real-world vulnerability scans and enforce security policies using:

* [Dependency Check](https://owasp.org/www-project-dependency-check/) for open-source libraries
* [Trivy](https://github.com/aquasecurity/trivy) for container and filesystem scanning
* [OPA Conftest](https://www.conftest.dev/) to test your Kubernetes manifests
* [Kubesec](https://kubesec.io/) for policy checks in Kubernetes

By integrating these tools into your DevSecOps pipeline, you’ll streamline the detection and remediation of security issues from code commit to production.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/877bd662-968c-40a5-bda6-a42b600ea957/lesson/2565e018-72fa-4805-8b42-fe421fd69ace" />
</CardGroup>
