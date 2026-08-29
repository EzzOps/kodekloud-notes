# Demo Initial Scan

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Security-Auditing-with-Claude-Code/Demo-Initial-Scan/page

Guide to performing an initial security audit of an Express.js login demo using automated tools to produce a structured Markdown report with prioritized findings and remediation steps.

In this lesson we perform an initial security audit of an Express login demo using Claude Code. The goal is to generate a repeatable, shareable Markdown audit you can review, convert (Google Docs / PDF / Word), and hand off to developers for remediation.

This workflow will help you:

* Create an `audits/` folder to store findings
* Run a project-structure analysis to identify entry points, routes, middleware, DB connections, and more
* Optionally run `npm audit` to detect vulnerable dependencies
* Produce `audits/SECURITY_AUDIT_REPORT.md` containing a high-level risk assessment and recommended fixes

Why this matters: repeatable, machine-assisted audits speed up vulnerability discovery and produce consistent remediation checklists for teams.

## What you'll produce

* audits/SECURITY\_AUDIT\_REPORT.md — a structured Markdown audit with an executive summary, project structure analysis, prioritized findings (Critical/High/Medium), and remediation guidance.
* Optional: artifacts from `npm audit` or other tooling (dependency vulnerability reports).

## Create the audits folder and run the initial analysis

Create a folder to store audit artifacts and outputs:

```bash theme={null}
