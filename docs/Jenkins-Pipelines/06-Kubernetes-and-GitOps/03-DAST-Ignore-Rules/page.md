# DAST Ignore Rules

Source: https://notes.kodekloud.com/docs/Jenkins-Pipelines/Kubernetes-and-GitOps/DAST-Ignore-Rules/page

This article explains how to bypass specific warnings during dynamic application security testing with OWASP ZAP in CI/CD pipelines.

In this article, we explain how to bypass specific warnings during dynamic application security testing (DAST) with OWASP ZAP. Previously, a DAST run terminated because of an unexpected content type warning. While the ideal approach is to resolve the issue in your application code, this guide demonstrates how you can ignore such warnings for testing purposes.

## Example DAST Output

Below is an example output from a DAST run that logged one warning:

```bash theme={null}
#### REPLACE below with Kubernetes http://IP_Address:30000/api-docs/ 
#### chmod 777 $(pwd)
docker run -v $(pwd):/zap/wrk/:/zapproxy zap-api-scan.py -t http://134.209.155.222:30000/
PASS: .intaccess Information Leak [40032]
PASS: Hidden File Finder [40035]
PASS: Spring Actuator Information Leak [40024]
PASS: Log4Shell [40034]
PASS: SpringShell [40045]
PASS: Script Active Scan Rules [5000]
PASS: Script Passive Scan Rules [5001]
PASS: Path Traversal [6]
PASS: Remote File Inclusion [7]
PASS: Java Serialization Object [90023]
PASS: HTTP Request Smuggling [90031]
PASS: Insufficient Site Isolation Against Spectre Vulnerability [90004]
PASS: XSLT Injection [9001]
PASS: Server Side Code Injection [9006]
PASS: Unauthorized Command Execution [9005]
PASS: Application Error Disclosure [90082]
PASS: External Entity Attack [90043]
PASS: Generic Padding Oracle [90025]
PASS: WSDL File Detection [90080]
PASS: Security Scoped Cookie Protection [9006]
PASS: Server Metadata Potentially Exposed [90053]
WARN-NEW: Unexpected Content-Type was returned [10001] x 5
http://134.209.155.222:30000/ [200 OK]
http://134.209.155.222:30000/1684169206451124338 [404 Not Found]
http://134.209.155.222:30000/latest/version [404 Not Found]
FAIL-NEW: 0  WARN-INPROG: 0  INFO: 0 IGNORE: 0  PASS: 112
script returned exit code 2
```

<Callout icon="lightbulb">
  For demonstration purposes, this guide explains how to bypass errors. In production, always address the underlying vulnerabilities.
</Callout>

## Ignoring Warnings During the Scan

To ignore specific warnings during a scan, create a configuration file that uses the "ignore" tag for designated warnings. The following command runs the scan while ignoring errors:

```bash theme={null}
#### REPLACE below with Kubernetes http://IP_Address:30000/api-docs/ ######
chmod 777 $(pwd)
docker run -v $(pwd):/zap/wrk ghcr.io/zaproxy/zap-api-scan.py -t http://134.209.155.222:8080/
```

> Remember: Always consult the OWASP ZAP documentation to decide which findings can be safely ignored.

## Creating the ZAP Ignore Configuration File

You must create a configuration file to specify the warnings you wish to ignore. When executing the Docker command, pass the configuration file using the `-c` option. You can generate a default configuration file using the `-g` option. Below is an excerpt from a sample configuration file:

```plaintext theme={null}
