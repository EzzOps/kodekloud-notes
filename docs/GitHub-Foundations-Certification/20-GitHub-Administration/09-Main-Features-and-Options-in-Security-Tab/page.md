# Main Features and Options in Security Tab

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Administration/Main-Features-and-Options-in-Security-Tab/page

Overview of GitHub Security tab features and configurations for security policies, Dependabot, advisories, code scanning, secret scanning, and push protection to strengthen repository security

In this lesson we'll walk through the main features and options available in a repository's Security tab on GitHub. The Security tab centralizes automated tools that help you identify vulnerabilities, manage dependencies, and prevent accidental exposure of secrets—enabling a stronger security posture without slowing development.

This guide reviews each major section in the Security tab, how it helps protect your project, and practical configuration examples.

* Security policy (`SECURITY.md`)
* Dependabot (dependency monitoring and automated updates)
* Security advisories (private triage workspace)
* Code scanning (static analysis engines such as CodeQL)
* Secret scanning and push protection

## Why the Security tab matters

The Security tab aggregates preventive and detective controls that operate across the development lifecycle:

* Prevent accidental leaks (secret scanning, push protection).
* Detect vulnerable dependencies (Dependabot).
* Find code-level weaknesses early (code scanning).
* Enable responsible disclosure and safe triage (security policies and advisories).

## Security policy

Add a `SECURITY.md` file at the repository root to define how you want security issues reported. This provides a clear, private reporting path for researchers and reduces the chance vulnerabilities are published to public issue trackers before a coordinated fix is available.

<Callout icon="lightbulb">
  Including a `SECURITY.md` file directs responsible disclosure and helps ensure sensitive issues are reported privately instead of in public issues.
</Callout>

Example minimal `SECURITY.md`:

```markdown theme={null}
If you discover a security vulnerability, please report it privately to security@example.com. Do not open a public issue.
```

Best practices:

* Provide an email alias or triage form, not an individual's personal address.
* State expected response times and accepted vulnerability report formats.
* Describe any disclosure policy or bounty program links if applicable.

## Dependabot (software supply chain monitoring)

Dependabot monitors dependency manifests (e.g., `package.json`, `requirements.txt`, `pom.xml`) and alerts when dependencies have known vulnerabilities or malicious packages. It can also open pull requests that update vulnerable dependencies to fixed versions.

Configure Dependabot with `.github/dependabot.yml`. Example:

```yaml theme={null}
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
```

Key configuration options:

* `package-ecosystem`: npm, pip, maven, etc.
* `directory`: repository path where manifests live.
* `schedule.interval`: `daily`, `weekly`, or `monthly`.
* `allow` / `ignore` rules to whitelist or skip updates.

Use Dependabot for:

* Proactive dependency updates.
* Quick, auditable fixes via pull requests.
* Integration with security alerts to prioritize fixes.

## Security advisories (private triage workspace)

Security advisories provide a private space for maintainers to triage, patch, and test fixes for reported vulnerabilities without exposing details publicly. This prevents premature disclosure and exploitation while a coordinated fix and communication plan is prepared.

When to use:

* For newly reported vulnerabilities requiring coordinated patches across multiple repositories.
* When you need to draft a public advisory and CVE information before disclosure.

## Code scanning (static analysis such as CodeQL)

Code scanning analyzes source code to find potential vulnerabilities—like SQL injection, XSS, insecure deserialization, and logic flaws—before code is merged. GitHub's CodeQL is a common analysis engine that runs as part of GitHub Actions.

Example CodeQL workflow:

```yaml theme={null}
name: "CodeQL"
on:
  push:
  pull_request:
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: javascript
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
```

Tips for effective code scanning:

* Run scans on pull requests to block risky merges.
* Use scheduled scans to catch problems on default branches.
* Fine-tune query packs or exclude noisy directories to reduce false positives.

## Secret scanning and push protection

Secret scanning detects accidentally committed credentials (API keys, tokens, passwords). For some providers, secret scanning integrates with revocation or alerting workflows to speed remediation.

Push protection stops high-confidence secrets from being pushed to protected branches. This acts as a gate at push time and prevents credentials from entering your repository history.

<Callout icon="warning">
  Push protection can block a developer's push if a credential is detected. Ensure your team knows how to respond (remove the secret, rotate credentials, and follow repository policies for force-pushes when required).
</Callout>

Operational recommendations:

* Enforce push protection on protected branches used for production releases.
* Pair secret scanning with automation for secret rotation where possible.
* Educate contributors on using environment variables and secrets management tools instead of committing credentials.

## Feature summary

| Feature                           | Purpose                                         | Where to configure                      |
| --------------------------------- | ----------------------------------------------- | --------------------------------------- |
| Security policy                   | Define private reporting & disclosure processes | `SECURITY.md` at repo root              |
| Dependabot                        | Detect and auto-update vulnerable dependencies  | `.github/dependabot.yml`                |
| Security advisories               | Private triage & coordinated disclosure         | Security → Advisories in GitHub UI      |
| Code scanning                     | Static analysis for code-level vulnerabilities  | GitHub Actions workflows (e.g., CodeQL) |
| Secret scanning & push protection | Detect and stop credential leaks                | Repo settings / organization settings   |

## Quick-start checklist

* Add or update `SECURITY.md` with a private contact and disclosure guidelines.
* Enable Dependabot and configure update cadence for your package ecosystems.
* Turn on code scanning (CodeQL) for the languages you use and run on PRs.
* Enable secret scanning and push protection for protected branches.
* Establish an incident response and rotation plan for leaked credentials.

## Links and references

* [GitHub Security Documentation](https://docs.github.com/en/code-security)
* [Dependabot configuration options](https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically/configuration-options-for-dependency-updates)
* [CodeQL documentation](https://securitylab.github.com/tools/codeql)
* [Reporting a vulnerability](https://docs.github.com/en/code-security/security-advisories/about-security-advisories)

## Summary

The Security tab bundles complementary tools that together reduce risk across the software supply chain and codebase. Use `SECURITY.md` for coordinated reporting, Dependabot for dependency hygiene, security advisories for private triage, code scanning to catch logic and implementation issues early, and secret scanning with push protection to stop credential leaks. Implementing these controls consistently will help your team maintain secure, efficient development workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e1fb240f-a163-45b7-ae70-61c1e162023f/lesson/68eed9df-bc5e-4a93-9cdf-44b5a729e211" />
</CardGroup>
