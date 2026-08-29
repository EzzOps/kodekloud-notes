# Investigating ZAP for Penetration Testing

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Implement-Security-and-Validate-Code-Bases-for-Compliance/Investigating-ZAP-for-Penetration-Testing/page

This article discusses the OWASP Zed Attack Proxy (ZAP) for web application security testing and its features, benefits, and integration into workflows.

OWASP Zed Attack Proxy (ZAP) is a free, open-source web application security scanner trusted by developers and security teams. Operating as an HTTP/HTTPS proxy, ZAP intercepts and logs traffic between your browser and the target application. This setup lets you inspect, modify, and replay requests to uncover security flaws early.

## Key Benefits

* **Open-Source & Community-Driven**: Backed by OWASP with regular updates.
* **Extensible Add-Ons**: Customize scans with community scripts and extensions.
* **CI/CD Ready**: Automate security checks in your pipeline for continuous feedback.

## Testing Modes

| Scan Mode        | Description                                                                    | Ideal Use Case               |
| ---------------- | ------------------------------------------------------------------------------ | ---------------------------- |
| Passive Scanning | Observes traffic without alteration, flags missing headers or insecure cookies | Ongoing development          |
| Active Scanning  | Injects payloads and probes responses to detect vulnerabilities automatically  | Pre-release security testing |

## Baseline vs. In-Depth Scans

| Scan Type           | Scope                             | Duration | Use Case                 |
| ------------------- | --------------------------------- | -------- | ------------------------ |
| Baseline Assessment | Quick, non-intrusive checks       | Minutes  | CI/CD pre-merge checks   |
| In-Depth Analysis   | Comprehensive, rule-based testing | Hours    | Nightly or weekly audits |

![The image is an infographic about using Zed Attack Proxy (ZAP) for penetration testing, detailing modes of testing, baseline assessments, and in-depth scanning schedules. It includes elements like active engagement, passive monitoring, swift scans, and detailed analysis.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868025/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Investigating-ZAP-for-Penetration-Testing/zap-penetration-testing-infographic.jpg)

> **triangle-alert** Only perform active scans on applications you own or have explicit permission to test. Unauthorized scanning may violate legal or organizational policies.

> **lightbulb** By default, ZAP listens as a proxy on `http://127.0.0.1:8080`. Configure your browser or API client to route traffic through ZAP for accurate results.

## Getting Started with ZAP CLI

Scan from the command line to integrate seamlessly with scripts and pipelines:

```bash theme={null}
