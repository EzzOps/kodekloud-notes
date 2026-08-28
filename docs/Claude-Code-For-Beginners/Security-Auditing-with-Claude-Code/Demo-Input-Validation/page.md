# create the audits folder (example command)
mkdir -p audits
```

Provide Claude Code a clear instruction set to analyze the project and write results into that folder. Below is an example prompt used to drive an initial project analysis. Use it as a template and adapt to your codebase:

```text theme={null}
Perform a Project Structure Audit

Analyze the entire project structure and identify:
1. All entry points (app.js, server.js, etc.)
2. All routes and endpoints
3. Middleware chain and order
4. External service integrations
5. Database connection points
6. Authentication/authorization flow
7. File upload handling locations
8. API rate limiting implementation

Start by examining these core files:
- package.json (for vulnerable dependencies)
- app.js or server.js (for middleware configuration)
- All files in routes/
- All files in middleware/

Create a security audit report with initial risk assessment and write it to audits/SECURITY_AUDIT_REPORT.md.
```

After submitting the prompt, Claude Code will read project files (for example: `package.json`, `server.js`, `routes/*`, `middleware/*`, `config/database.js`, `schema.sql`) and may prompt to run commands such as `npm audit` to detect vulnerable dependencies.

<Callout icon="warning">
  If you choose to run interactive commands (like `npm audit`) from the audit environment, ensure you understand any npm scripts or postinstall hooks. Running tools may modify lockfiles or node\_modules—use a safe environment or a CI job when possible.
</Callout>

Example of running an npm audit as part of the workflow:

```bash theme={null}
# Example command run by the tool (interactive)
npm audit --audit-level moderate
```

Claude Code will prompt about running commands and writing files. When it asks to create or update the audit file, confirm the write permission. The assistant will then create `audits/SECURITY_AUDIT_REPORT.md` and open it for review.

## Example: Generated Security Audit Report (excerpt)

Claude Code produces a structured Markdown report. Below is an excerpt of a generated `audits/SECURITY_AUDIT_REPORT.md` to illustrate the expected format and level of detail.

```markdown theme={null}
# Security Audit Report - Express Login Demo
**Project:** Express Login Demo  
**Audit Date:** August 20, 2025  
**Auditor:** Security Analysis Tool

## Executive Summary

This security audit analyzed the Express.js login demo application with JWT authentication and PostgreSQL database integration. The audit examined 5 core files and identified several **CRITICAL** and **HIGH** risk vulnerabilities that require immediate attention.

Key Findings:
- Overall Risk: HIGH
- 3 CRITICAL vulnerabilities requiring immediate attention
- 3 HIGH risk issues needing quick fixes
- 3 MEDIUM risk concerns for optimization

Most Critical Issues:
1. No security headers (helmet.js needed)
2. Missing rate limiting (brute force vulnerability)
3. JWT secret validation missing
4. No HTTPS enforcement
5. Information disclosure in error handling

## Project Structure Analysis
### Core Components
- **Database:** PostgreSQL with pg driver
- **Authentication:** JWT with bcrypt password hashing
- **Validation:** express-validator

## Critical Security Vulnerabilities

### 🔴 CRITICAL: Missing Security Headers
**File:** `server.js:1-19`  
**Risk Level:** CRITICAL  
**Description:** No security headers implemented (CORS settings, HSTS, CSP, X-Frame-Options, etc.)  
**Impact:** Application vulnerable to XSS, clickjacking, and other client-side attacks  
**Recommendation:** Implement helmet middleware and configure CSP/HSTS appropriately.

### 🔴 CRITICAL: No Rate Limiting
**Files:** `server.js:1-19`, `routes/auth.js:9-96`  
**Risk Level:** CRITICAL  
**Description:** No rate limiting on authentication endpoints (login, password reset)  
**Impact:** Vulnerable to brute force attacks and credential stuffing  
**Recommendation:** Implement express-rate-limit with progressive delays and account lockout policies.

### 🔴 CRITICAL: JWT Secret Configuration
**File:** `routes/auth.js:53`  
**Risk Level:** CRITICAL  
**Description:** JWT_SECRET loaded from environment without validation  
**Impact:** Weak or missing JWT secrets compromise authentication tokens  
**Recommendation:** Validate JWT_SECRET length and complexity at startup; fail fast if missing.

## High and Medium Risk Issues
- Information disclosure in error handling — sanitize error messages returned to clients.
- Missing HTTPS enforcement — enable HSTS and redirect HTTP to HTTPS.
- Missing input sanitation in a few endpoints — ensure validation and sanitization on all user inputs.
```

When the tool writes the file, you’ll see a confirmation like:

```bash theme={null}
# Example output after writing the report
I Wrote 169 lines to audits/SECURITY_AUDIT_REPORT.md
```

<Frame>
  <img alt="A screenshot of a computer desktop showing a Google Docs window with a security audit report open, highlighting &#x22;Immediate Action Items&#x22; like implementing security headers, rate limiting, and HTTPS enforcement. The left sidebar shows document tabs and risk indicators, and a code editor/IDE is visible in the background." />
</Frame>

## Quick summary table (example)

|                    Outcome | Why it matters                               | Action                                     |
| -------------------------: | -------------------------------------------- | ------------------------------------------ |
|   Missing security headers | Exposes app to XSS, clickjacking             | Add helmet, configure CSP/HSTS             |
|           No rate limiting | Enables brute-force / credential stuffing    | Add express-rate-limit + account lockout   |
|    Weak/missing JWT secret | Session compromise                           | Validate secret at startup; rotate secrets |
| Dependency vulnerabilities | Remote code execution / privilege escalation | Run `npm audit`, patch or upgrade deps     |

## How to use the report

* Use the report as a prioritized remediation checklist for development and ops teams.
* Convert the Markdown to Google Docs or PDF for stakeholder review or compliance artifacts.
* Prioritize CRITICAL items (helmet, rate limiting, JWT secret validation, HTTPS enforcement) before deploying to production.
* Attach the audit file to tickets or CI/CD pipelines to track progress.

<Callout icon="lightbulb">
  Validate environment secrets and fail fast: ensure JWT\_SECRET is present and meets complexity requirements at app startup. Also add helmet and express-rate-limit for immediate mitigation.
</Callout>

## Repository and prompts

The repository accompanying this lesson includes reusable prompt templates and examples tailored to Express/Node.js applications. Reuse or adapt them to your codebase and security requirements.

<Frame>
  <img alt="A dark-themed desktop screenshot showing a browser window open to a code-hosting repository page listing Markdown files and recent commits. Behind it is a code editor with a project file tree and an open security audit Markdown file." />
</Frame>

Example prompt files you can reuse:

* 000-initial-project.md
* api-and-infrastructure.md
* authentication-flow-review\.md
* authorization-implementation.md
* business-logic-vulnerabilities.md
* comprehensive-security-report.md

These prompts are adaptable to many Node.js/Express codebases and will help standardize audits across projects.

## Next steps

This lesson focused on the initial scan and reporting workflow. Recommended follow-ups:

* Deep-dive into authentication and authorization flows (JWT best practices, refresh tokens, session invalidation)
* Implement recommended middleware: helmet, express-rate-limit, cors (with secure configuration)
* Harden error handling and logging to avoid information disclosure
* Integrate automated audits into CI (npm audit / Snyk / Dependabot) for continuous dependency monitoring

Links and references:

* [Express.js — Getting started](https://expressjs.com/)
* [Helmet — Security middleware for Express](https://github.com/helmetjs/helmet)
* [express-rate-limit — Basic IP rate-limiting middleware](https://github.com/nfriedly/express-rate-limit)
* [OWASP Top Ten — Web Application Security Risks](https://owasp.org/www-project-top-ten/)

Use these resources to expand and harden your audit process with automated checks and developer remediation playbooks.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/eaf75a67-f28f-4217-a3f9-92d411403129/lesson/24a7a710-e16c-4b6d-beb9-ba2ee2a2bbb3" />
</CardGroup>


# Demo Input Validation

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Security-Auditing-with-Claude-Code/Demo-Input-Validation/page

Guidance on input validation and security auditing for web applications, covering common injection risks, audit checklist, automated audit example, and practical mitigations for Node Express apps.

In this lesson we cover input validation — the checks and protections applied to any data that users (or automated clients) supply to your application. Robust input validation reduces the attack surface for SQL/NoSQL injection, command injection, XSS, path traversal, XML External Entity (XXE) attacks, and other common vectors.

Below we outline what to look for in an audit, demonstrate an automated audit run, and provide practical mitigations and patterns you can apply immediately.

<Callout icon="lightbulb">
  Treat all external inputs as untrusted. Validate types, lengths, allowed values, and apply context-appropriate encoding before using data in queries, file operations, or rendered HTML.
</Callout>

## Why input validation matters

Inputs arrive via HTML forms, APIs, file uploads, headers, query strings, and other external interfaces. Even if no human attacker is targeting your app, automated scanners and bots continuously probe services for weaknesses.

The classic “Little Bobby Tables” example shows how untrusted input interpolated into a SQL statement can cause data loss (SQL injection). Any time you build queries, shell commands, file paths, or HTML using external data, assume the input could be malicious and take steps to validate, sanitize, or parameterize it.

For example, avoid building SQL like:

```sql theme={null}
SELECT * FROM users WHERE username = '...user input...' ;
```

An attacker-controlled username like:

```sql theme={null}
'; DROP TABLE students; --
```

could terminate and append destructive SQL. Use parameterized queries and strong validation instead.

## What to check for

Checklist of common input validation and related issues:

* SQL injection: concatenation of raw inputs into SQL, unsanitized dynamic queries, unsafe stored procedure use.
* NoSQL injection (MongoDB): unvalidated operator expressions (e.g., \$where) or executing JavaScript in queries.
* Command injection: passing unsanitized input to shell commands or child processes.
* Cross-site scripting (XSS): missing output encoding or HTML sanitization for user content.
* XXE (XML External Entity): insecure XML parsing that allows external entity resolution.
* Path traversal: insufficient normalization/validation of file paths (../ attacks).
* Request validation gaps: missing body-size limits, parameter pollution, lack of typed validation, or missing required fields.

Create a validation matrix mapping every endpoint to the protections applied (parameterized queries, schema validation, file handling constraints, rate limits, body-size limits, etc.). This helps prioritize fixes and ensures consistent coverage across routes.

<Frame>
  <img alt="A screenshot of a code editor (VS Code) with a file tree on the left and an open Markdown file titled &#x22;Input Validation Security Audit Report&#x22; listing security issues like SQL/NoSQL injection, command injection, XSS, XXE, path traversal, and request validation. The editor uses a dark blue theme." />
</Frame>

## Running an automated audit (example session)

Here is an example interactive session with an auditing assistant that generates a comprehensive input validation audit and writes it to the repository.

Example CLI startup:

```bash theme={null}
◉ jeremy@MACSTUDIO Express-login-demo % claude

* Welcome to Claude Code!

/help for help, /status for your current setup

cwd: /Users/jeremy/Repos/Claude Code Course/Express-login-demo

> Try "fix typecheck errors"

? for shortcuts
```

The assistant produces a detailed Markdown audit at `audits/INPUT_VALIDATION_SECURITY_REPORT.md`. Typical contents include a risk score, critical findings, proof-of-concept examples (for owned systems only), and targeted remediation steps.

## Example audit summary

(The following is a consolidated, edited excerpt from a generated audit report.)

```markdown theme={null}
**Application:** Express Login Demo  
**Audit Date:** 2025-08-20  
**Auditor:** Claude Code  
**Overall Risk Score:** 6/10 (Medium-High)

## Executive Summary
This security audit analyzed the Express.js login application for input validation vulnerabilities across all endpoints and data processing functions. The application demonstrates good foundational security practices with parameterized queries and [express-validator](https://express-validator.github.io/docs/) usage, but has critical gaps in security controls that create notable risk.

**Key Findings**
- ✅ SQL Injection protection implemented correctly (parameterized queries)
- ✅ Input validation present ([express-validator](https://express-validator.github.io/docs/))
- ❌ Missing rate limiting on authentication endpoints — critical
- ❌ No request size limits — DoS through memory exhaustion possible
- ❌ Weak JWT secret configuration in production
- ❌ Incomplete input sanitization for some outputs
- ❌ Missing security headers in responses
```

## Critical findings and remediation

### 1) Missing rate limiting (Critical)

* CWE: CWE-307 (Improper Restriction of Excessive Authentication Attempts)
* Risk: Without throttling on endpoints like `/api/auth/login`, attackers can brute-force credentials or overload the endpoint.

Exploitability (example brute-force loop — do not run against third-party systems):

```bash theme={null}
