# SBOM Workflow

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Supply-Chain-Security/SBOM-Workflow/page

This article provides a comprehensive guide to generating and managing a Software Bill of Materials (SBOM) for secure software supply chain practices.

In this article, we provide a clear and comprehensive guide to generating and managing a Software Bill of Materials (SBOM). This guide covers the entire process—from SBOM generation and secure storage to vulnerability scanning, detailed analysis, remediation, and continuous monitoring. Integrating these practices helps you maintain a secure, compliant software supply chain throughout the development lifecycle.

## Overview of the SBOM Process

The SBOM process is comprised of the following key steps:

1. Generate the SBOM.
2. Securely store the SBOM.
3. Scan the SBOM for vulnerabilities.
4. Analyze the scan results.
5. Remediate the identified issues.
6. Continuously monitor the SBOM.

Two key formats dominate in the SBOM space: SPDX and CycloneDX.

![The image illustrates an "SBOM Workflow" with steps: Generate SBOM, Store SBOM, Scan SBOM, Analyze Results, Remediate Issues, and Monitor.](https://kodekloud.com/kk-media/image/upload/v1752871712/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-SBOM-Workflow/frame_30.jpg)

Choose the format that best meets your needs:

* Use SPDX for open-source projects and enterprises that require licensing compliance, trace software origins, audit security, and manage vulnerabilities.
* Opt for CycloneDX to enhance vulnerability management across the software lifecycle and to ensure software integrity.

![The image presents a choice between two SBOM standards: SPDX and CycloneDX.](https://kodekloud.com/kk-media/image/upload/v1752871713/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-SBOM-Workflow/frame_50.jpg)

## Generating an SBOM

Syft is a widely used tool for generating SBOMs. To get started, download Syft from the official site. It supports scanning both Docker images and local source code directories. Use the commands below as examples:

```bash theme={null}
