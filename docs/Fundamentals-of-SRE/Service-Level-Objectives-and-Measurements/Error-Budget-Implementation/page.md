# What someone meant to do:
aws s3 cp file.txt s3://internal-bucket/

# What actually got deployed:
aws s3api put-bucket-acl --bucket internal-bucket --acl public-read

# ⚠️ Now every file in the bucket is publicly accessible
```

<Frame>
  <img alt="A slide titled &#x22;Common Risks in the Release Path&#x22; showing a &#x22;Vulnerability Domino Effect&#x22; graphic (a cracked shield on a monitor). It lists five numbered risks: widely used library, vulnerability found in production, no automated dependency scanning, manual audits of many services, and resulting panic/ executive escalations." />
</Frame>

Build security into CI/CD (shift left)

* Add automated checks in CI so vulnerabilities are detected before deployment.
* SAST (Static Application Security Testing) inspects source code for issues (SQL injection, XSS, hard-coded credentials, buffer overflows, weak crypto) without running programs.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Security Verification in CI/CD&#x22; explaining Static Application Security Testing (SAST) which scans source code for security issues without running the program. A sidebar lists common findings: SQL injection, cross-site scripting (XSS), buffer overflow, and hardcoded credentials." />
</Frame>

Example: GitHub CodeQL can be used as a SAST step in GitHub Actions. Keep CI configured to fail or require remediation for critical issues where appropriate.

```yaml theme={null}
# GitHub Actions example for CodeQL SAST scan (snippet)
name: Run SAST Scan
on: [push, pull_request]
jobs:
  codeql-analysis:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: javascript, python

      - name: Run CodeQL analysis
        uses: github/codeql-action/analyze@v2

      - name: Fail on critical issues
        if: env.CRITICAL_ISSUES != ''
        run: |
          echo "Critical security issues found. Failing build."
          exit 1
```

Dependencies and SBOMs

* Most modern apps include large third-party dependency trees. Automated dependency scanning prevents known vulnerable packages from reaching production.
* Tools: pip-audit, npm audit, GitHub Dependabot, SCA (Software Composition Analysis) solutions.

```bash theme={null}
# For Python
pip-audit --strict

# For Node.js
npm audit --audit-level=moderate
```

A Software Bill of Materials (SBOM) is an "ingredients list" for your software. With an SBOM you can rapidly identify which services are affected by a vulnerability (for example, during Log4Shell), rather than manually tracing dependency trees service by service.

<Frame>
  <img alt="A presentation slide titled &#x22;Security Verification in CI/CD&#x22; explaining Software Bill of Materials (SBOM) as a complete inventory of software components. It notes why SBOMs matter — they helped teams quickly identify at-risk apps during Log4Shell, whereas without them teams spent days or weeks manually checking services." />
</Frame>

Core principles and common practices

* Principle of Least Privilege: grant only the minimum permissions required.

```json theme={null}
// Bad: effectively full admin
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}

// Better: scoped to S3 object read/write in one bucket
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::app-uploads/*"
}
```

* Automate security checks: dependency scanning, secret detection, SAST/DAST, container image scanning, and infrastructure-as-code (IaC) checks should run in CI.
* Review and sign artifacts: build-time signing ensures the artifact you deploy is the artifact you built. cosign and sigstore are industry-standard tools for container/image signing and verification.

```bash theme={null}
# Example artifact signing with cosign (bash)
cosign sign --key cosign.key ghcr.io/my-org/myapp:v1.2.3

# Verify during deployment
cosign verify --key cosign.pub ghcr.io/my-org/myapp:v1.2.3
```

* Continuous monitoring: subscribe to advisories, configure automated CVE alerts, and periodically re-scan deployed images and running systems.

<Frame>
  <img alt="An infographic titled &#x22;Best Practices for Secure Releases&#x22; that lists four principles: Principle of Least Privilege, Automate Security Checks, Review and Sign Artifacts, and Monitor for New Vulnerabilities. A checklist below recommends subscribing to security advisories, setting up automated CVE alerts, and regularly reviewing infrastructure and apps." />
</Frame>

Progressive security pipeline — step by step
Evolve pipelines incrementally to reduce risk without blocking delivery:

1. Start with a basic build/deploy pipeline.
2. Add dependency vulnerability scanning so bad packages are blocked early.
3. Generate SBOMs so you can quickly identify affected apps when vulnerabilities surface.
4. Improve authentication and restrict permissions (least privilege).
5. Add container image scanning (Trivy, Grype, etc.).
6. Enforce environment separation and promotion gates (staging → production).

<Frame>
  <img alt="A presentation slide titled &#x22;Progressive Security Pipeline Evolution&#x22; that lists five steps: The Problem (Basic Insecure Pipeline), Dependency Vulnerability Scanning, Software Bill of Materials (SBOM), Secure Authentication and Permissions, and Container Security Scanning. A side note reads &#x22;Scan image for vulnerabilities&#x22; and the slide is copyrighted by KodeKloud." />
</Frame>

Working with the provided repository

* Fork and clone the repository locally to iterate on release workflows and test changes.

```bash theme={null}
git clone https://github.com/YOUR_USERNAME/kodekloud-records-store-web-app.git
cd kodekloud-records-store-web-app

# Create a branch for testing
git checkout -b develop-test
```

Design a consolidated, secure GitHub Actions workflow with:

* Explicit triggers (push branches and workflow\_dispatch for manual runs).
* Limited permissions using the top-level permissions block.
* Jobs: build-and-test, build-container (secure registry login, image build, SBOM generation, container scan), deploy-staging, and deploy-production (with manual approval).

Example workflow header and permissions:

```yaml theme={null}
# Workflow header + limited token permissions
name: Progressive Config Management & Secure Release Pipeline
on:
  push:
    branches:
      - main
      - develop-test
  pull_request:
    types: [closed]
    branches:
      - main
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment for deployment'
        required: true
        default: 'staging'
        type: choice
        options: [development, staging, production]
permissions:
  contents: read
  packages: write
  id-token: write
```

Build-and-test (important parts only):

```yaml theme={null}
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install --upgrade pip setuptools
          pip install -r requirements.txt

      - name: Dependency vulnerability scan (pip-audit)
        run: |
          source venv/bin/activate
          pip install pip-audit
          pip-audit --format json > security-report.json || echo "vulnerabilities found"
```

Authentication to container registry — avoid hardcoded credentials

* Never store plaintext credentials in workflows or source code.

<Callout icon="lightbulb">
  Never store plaintext credentials in workflows or in source code. Use the provided runtime tokens and secrets.
</Callout>

<Callout icon="warning">
  Do not commit static credentials. Hardcoded passwords in CI can be exposed in logs, forks, or via leaked access. Rotate any credentials that were committed immediately.
</Callout>

Bad example (do not use):

```bash theme={null}
# ❌ INSECURE: hardcoded password (do not use)
echo "password123" | docker login ghcr.io -u admin --password-stdin
```

Good example (use GitHub token at runtime):

```yaml theme={null}
- name: Log in to GitHub Container Registry
  run: |
    echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u $GITHUB_ACTOR --password-stdin
    echo "✅ Using secure GitHub token authentication"
```

Install Docker Compose and build/push images (use fixed URL for reproducibility):

```yaml theme={null}
- name: Install Docker Compose
  run: |
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose version

- name: Build and tag Docker image
  run: |
    docker build -t ghcr.io/${{ github.repository }}/kodekloud-records:${{ github.sha }} .
    docker push ghcr.io/${{ github.repository }}/kodekloud-records:${{ github.sha }}
```

Generate SBOM and upload as an artifact (example using syft):

```yaml theme={null}
- name: Generate Software Bill of Materials (SBOM)
  run: |
    curl -sSFL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
    syft -o cyclonedx-json . > sbom.json

- name: Upload SBOM as artifact
  uses: actions/upload-artifact@v4
  with:
    name: software-bill-of-materials
    path: sbom.json
```

Container scanning (example using Grype):

```yaml theme={null}
- name: Install Grype
  run: |
    curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

- name: Scan image for vulnerabilities
  run: |
    grype ghcr.io/${{ github.repository }}/kodekloud-records:${{ github.sha }} -o json > grype-report.json || true
```

Promotion gates and deploy jobs

* Deploy to staging automatically if scans pass.
* Require manual approval for production promotion (explicit human gate).

```yaml theme={null}
jobs:
  deploy-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          echo "Deploying to staging..."
          # deployment commands here

  deploy-production:
    environment: production
    runs-on: ubuntu-latest
    steps:
      - name: Production Promotion Gate
        run: |
          echo "🔒 MANUAL APPROVAL REQUIRED FOR PRODUCTION"
          echo "Approved by: ${{ github.actor }}"
```

Troubleshooting — failed authentication due to insecure login

* Common error when using hardcoded login:

```text theme={null}
Error response from daemon: Get "https://ghcr.io/v2/": denied: denied
Error: Process completed with exit code 1.
```

Use runtime tokens and secrets as shown above; replace insecure credentials and re-run the workflow.

When the pipeline runs successfully you will see GitHub Actions output indicating build, scans, SBOM upload, and staged deployment succeeded.

<Frame>
  <img alt="A screenshot of a GitHub repository's Actions page showing a workflow run titled &#x22;run secure pipeline #76.&#x22; The right pane shows the &#x22;deploy-staging&#x22; job and its steps (Set up job, Checkout code, Install Docker Compose, Create Staging Environment, Deploy to Staging, etc.)." />
</Frame>

Summary — what changed and why it matters

* Replaced insecure patterns with managed, auditable controls:
  * Token-based authentication instead of hard-coded secrets
  * Automated dependency and container scanning in CI
  * SBOM generation and artifact signing to ensure provenance
  * Principle of least privilege and environment-based promotion gates

Each layer reduces the chance that a single mistake or vulnerable dependency becomes a full-scale breach. Use the pipeline pattern shown here as a starting point: customize scanners, severity thresholds, and promotion gates to your organization’s risk profile.

<Frame>
  <img alt="A presentation slide titled &#x22;Progressive Security Pipeline Evolution&#x22; showing a Before vs After comparison: Before lists issues like hardcoded credentials, no scanning/SBOM, overly broad permissions, and no deployment controls; After lists fixes like token auth, automated/SBOM/container scanning, least privilege, and environment controls." />
</Frame>

Further reading and references

* GitHub CodeQL: [https://securitylab.github.com/tools/codeql](https://securitylab.github.com/tools/codeql)
* pip-audit: [https://github.com/trailofbits/pip-audit](https://github.com/trailofbits/pip-audit)
* npm audit docs: [https://docs.npmjs.com/cli/v9/commands/npm-audit](https://docs.npmjs.com/cli/v9/commands/npm-audit)
* syft (SBOM generation): [https://github.com/anchore/syft](https://github.com/anchore/syft)
* grype (container scanning): [https://github.com/anchore/grype](https://github.com/anchore/grype)
* cosign (artifact signing): [https://github.com/sigstore/cosign](https://github.com/sigstore/cosign)
* Trivy: [https://github.com/aquasecurity/trivy](https://github.com/aquasecurity/trivy)

Next, we’ll wrap up this section with a concise checklist of best practices and additional resources for hardening CI/CD pipelines.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/b1ba0f45-8f39-445f-bc44-5d77d3a56b1c/lesson/89af47ac-2b3f-4e78-b5e3-384f38776caa" />
</CardGroup>


# Error Budget Implementation

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Service-Level-Objectives-and-Measurements/Error-Budget-Implementation/page

Explains error budgets, converting SLOs into measurable allowances for downtime or failed requests, and how to measure, enforce, and use them to balance reliability and innovation.

An error budget is the explicit allowance of unreliability your service can tolerate while still meeting its Service Level Objective (SLO). It converts a percentage SLO into a practical, spendable resource teams can use for incidents, risky changes, experiments, and measured innovation without breaking user trust.

At its core, an error budget formalizes the trade-off between reliability and innovation: improving reliability often slows delivery, while pushing changes creates risk. Error budgets make that trade-off explicit, measurable, and actionable.

## Basic math: availability SLO → error budget

If your SLO is 99.9% uptime, the error budget is the remaining 0.1%. That 0.1% becomes a fixed amount of time (or requests) you may allow to degrade without violating the SLO.

Example: 99.95% availability → 0.05% downtime.

* For a 30-day month (30 × 24 × 60 = 43,200 minutes):
  * 0.05% of 43,200 = 21.6 minutes of allowable downtime per month.

<Frame>
  <img alt="A presentation slide titled &#x22;Calculating Error Budget for Different SLOs&#x22; showing a pie chart that illustrates 99.95% monthly availability (0.05% downtime). A side panel explains the time translation, calculating that 0.05% of 30 days equals about 21.6 minutes of allowed downtime per month." />
</Frame>

## Latency SLOs: same idea, applied to requests

For latency-based SLOs you apply the same math to request counts instead of elapsed time.

Example: SLO = “99% of requests complete under 200 ms” → error budget = 1% of requests.

* If you receive 1,000,000 requests in a month, 1% = 10,000 requests may exceed 200 ms before the SLO is missed.

<Frame>
  <img alt="A presentation slide titled &#x22;Calculating Error Budget for Different SLOs&#x22; showing a pie chart that illustrates 99.95% monthly availability (0.05% downtime). To the right is a &#x22;Latency Error Budgets&#x22; panel with examples explaining a 1% error budget (e.g., 99% of requests <200ms → 1% error budget; 1% of 1,000,000 = 10,000 slow requests)." />
</Frame>

## How to use error budgets in practice

Make budgets actionable by defining cadence, ownership, thresholds, and pre-agreed responses. Start with simple rules and iterate.

* Choose a measurement cadence (daily, weekly, monthly).
* Define consumption thresholds (for example: 50%, 75%, 100%) and the corresponding responses.
* Specify concrete actions for each threshold (slow releases, add safeguards, freeze changes).
* Document exceptions (e.g., emergency security patches) and a process for approvals.
* Periodically review and adjust SLOs, measurement windows, and policies.

<Callout icon="lightbulb">
  Define who measures the budget, how often the measurement runs, and which teams are notified at each threshold — these operational details make the budget actionable.
</Callout>

<Frame>
  <img alt="A slide titled &#x22;Implementing Effective Error Budget Policies&#x22; showing a horizontal timeline of the policy development process. It lists steps with icons and brief notes: Define Error Budget Measurement, Create Response Actions, Establish Consumption Thresholds, and Document Exceptions." />
</Frame>

## Implementation checklist: make error budgets repeatable

Follow these core steps to operationalize error budgets so they become part of your day-to-day decision-making:

1. Define clear SLOs for each critical service.
2. Document the calculation for each error budget so the math is auditable.
3. Build measurement systems to track SLI, SLO, and error-budget consumption in (near) real time.
4. Create dashboards so stakeholders can see trends and current consumption.
5. Define concrete policies and actions for threshold breaches.
6. Socialize the concept and train teams so everyone understands trade-offs.
7. Integrate error-budget checks into release and deployment workflows (automate gating where possible).
8. Iterate and refine policies based on observed behavior.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Implementing Effective Error Budget Practices&#x22; featuring an eight-step staircase infographic outlining steps like Identify Need, Document Calculations, Build Measurement Systems, Create Dashboards, Define Policies, Socialize Concept, Integrate Workflows, and Iterate and Refine. Each step is paired with a short description and small icons." />
</Frame>

## Practical example: KodeKloud Record Store

Suppose the KodeKloud Record Store API has an availability SLO of 99.9%. The monthly error budget is 0.1%:

* 0.1% of 43,200 minutes = 43.2 minutes of allowable downtime per month.

Attach a policy with actions at different consumption levels:

* At 75% consumed: slow down releases, increase pre-release testing, and prioritize reliability work.
* At 100% consumed: freeze new feature deployments, form a reliability task force, and report daily to leadership until stability is restored.

<Frame>
  <img alt="A presentation slide titled &#x22;KodeKloud Record Store Implementation&#x22; summarizing the API Error Budget: SLO 99.9% (monthly) and an error budget of 0.1% = 43.2 minutes of downtime per month. Below it is a graph labeled &#x22;Error Budget Consumption&#x22; showing essentially 0% of the budget consumed for 1d/7d/30d." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;KodeKloud Record Store Implementation&#x22; outlining an Error Budget Policy. It lists actions for 75% consumption (reduce deployment frequency, increase pre-release testing, prioritize reliability tasks) and for 100% consumption (freeze new features, form a reliability task force, daily updates to leadership)." />
</Frame>

## Measuring consumption (example: order processing)

If the order-processing flow has a 99.9% success SLO, the error budget is 0.1%—either \~43.2 minutes/month when measured by time, or 0.1% of requests when measured by request success.

A Prometheus-style query that computes percent of error budget consumed over a 30d window:

```promql theme={null}
clamp_max(
  100 * (1 - (sum(rate(http_requests_total{endpoint="/orders", status_code=~"2.."}[30d])) 
             / sum(rate(http_requests_total{endpoint="/orders"}[30d]))))
  / 0.001,
  100
)
```

How this works:

* Compute success rate: successful 2xx responses divided by total requests for /orders.
* Convert to error rate: 1 − success\_rate.
* Normalize by the error budget (0.001 = 0.1%) to get percent of budget consumed.
* Multiply by 100 to express as percent and clamp to 100.

Policy examples tied to consumption:

* At 50%: investigate database or queue performance, enhance instrumentation, notify engineering leadership.
* At 75%: restrict deployments that affect order processing, add manual verification steps, increase worker capacity.
* At 100%: freeze all changes, invoke incident response, and require executive approval to resume normal operations.

## Thresholds and recommended actions

| Consumption | Typical actions                                                                          |
| ----------- | ---------------------------------------------------------------------------------------- |
| 0–50%       | Continue normal development; consider faster delivery with standard safeguards.          |
| 50–75%      | Investigate root causes, increase monitoring, notify engineering leads.                  |
| 75–99%      | Slow or limit deployments that touch the service, prioritize reliability work.           |
| 100%        | Halt feature work, restore reliability, invoke incident response and leadership updates. |

## Decision-making scenarios

Scenario 1 — Low consumption (e.g., 20% used; 80% remaining): headroom exists. Accelerate feature delivery and take measured risks since the budget can absorb regressions.

<Frame>
  <img alt="A presentation slide titled &#x22;Error Budget-Based Decision Making&#x22; showing Scenario 1: Low Budget Consumption (80% remaining) with the decision to &#x22;Accelerate release of new features&#x22; and an upward bar-chart icon." />
</Frame>

Scenario 2 — High consumption (e.g., only 20% remaining): defer risky changes, preserve remaining budget for unexpected incidents, and focus on reliability improvements.

<Frame>
  <img alt="A presentation slide titled &#x22;Error Budget‑Based Decision Making — Scenario 2: High Budget Consumption (20% remaining)&#x22;. It recommends postponing planned infrastructure changes to preserve the remaining budget for unexpected issues." />
</Frame>

Scenario 3 — Budget fully consumed (100% depleted): stop feature work immediately and restore reliability. Error budgets make this a data-driven decision, removing subjective debates.

## Common pitfalls and mitigations

Common pitfalls:

* Inaccurate measurement: wrong metrics or broken tagging produce misleading consumption.
* Overly rigid enforcement: inflexibility can block necessary, time-sensitive work.
* Error budget hoarding: teams avoid meaningful work to “save” budget, stifling innovation.

<Frame>
  <img alt="A presentation slide titled &#x22;Common Error Budget Challenges&#x22; showing three rounded cards labeled &#x22;Inaccurate Measurement,&#x22; &#x22;Rigid Policy Enforcement,&#x22; and &#x22;Error Budget Hoarding,&#x22; each with a colored circular icon." />
</Frame>

Mitigations:

* Validate metrics and tagging; run audits so measurements are trustworthy.
* Publish a documented exceptions process for business‑critical or emergency changes.
* Encourage responsible risk-taking; consider “use-it-or-lose-it” policies to prevent hoarding.

<Frame>
  <img alt="A presentation slide titled &#x22;Addressing Common Error Budget Challenges&#x22; showing three stacked, colorful numbered blocks (1–3) with icons and short recommendations: Improve Measurement, Implement Exception Processes, and Encourage Risk‑Tasking, each with brief explanatory text." />
</Frame>

## Summary

Error budgets convert abstract reliability goals into concrete, actionable data. They help teams balance innovation and stability when:

* Measurements are trusted and auditable.
* Policies and thresholds are clear and socialized.
* Dashboards and automation make SLI/SLO/error-budget status visible across the organization.

For further reading:

* [Prometheus query language basics](https://prometheus.[SECRET_REDACTED]/)
* [Site Reliability Engineering — concepts and practices](https://sre.google/books/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/e801ee3d-7ee7-4029-8c2d-b95c6b6bdf7e/lesson/06135524-d9bd-4a5e-bc2f-6175203be973" />
</CardGroup>
