# Demo Secrets Management Audit

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Security-Auditing-with-Claude-Code/Demo-Secrets-Management-Audit/page

Walkthrough for auditing secrets management to find hard‑coded credentials, exposed .env files, weak rotation and encryption, with evidence, safe PoCs, and prioritized remediation steps.

In this walkthrough we perform a secrets management audit to identify hard-coded credentials, insecure environment handling, and gaps in rotation and encryption practices. The goal: produce reproducible findings with evidence, safe proofs-of-concept, and prioritized remediation steps you can track in issues or tickets.

<Frame>
  <img alt="A presentation slide titled &#x22;Secrets Management Audit&#x22; with a large dark curved shape on the right containing the word &#x22;Demo.&#x22;" />
</Frame>

## Scope and quick checklist

Use this checklist to drive automated scans and manual reviews across the repository:

| Checklist item                                                                           | Why it matters                                                     |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Scan codebase for hard-coded secrets (API keys, passwords, JWT secrets, encryption keys) | Prevents leaked credentials in VCS and public mirrors              |
| Verify environment variable usage; ensure `.env` is not committed                        | Builds separation of config from code and avoids plaintext secrets |
| Check secret rotation capability for DB passwords, API keys, certs                       | Limits blast radius after exposure                                 |
| Review encryption and key management (KDFs, salts, key storage)                          | Ensures cryptographic primitives are configured correctly          |
| Ensure startup environment validation (fail fast in production)                          | Prevents deploying weak default secrets to prod                    |
| Produce structured findings (severity, evidence, remediation snippet)                    | Enables prioritized remediation and tracking                       |

> **lightbulb** Use both automated scanners (trufflehog, git-secrets) and targeted repository searches for keywords like `JWT_SECRET`, `API_KEY`, `password`, `env`, `encrypt`, `salt`, `bcrypt`, and `rotate` to collect evidence before manual verification.

## Example prompts and audit orchestration

Typical audit workflow:

* Run repository-wide keyword search and secret scanners.
* For each candidate finding, extract file paths and line ranges (evidence).
* Produce a risk score (0–10), top prioritized fixes, and a checklist diff (Pass/Fail/NA).
* Provide safe, non-destructive PoC (where necessary) and remediation snippets for developers.

Automated and manual steps complement each other: scanners find likely issues; manual inspection validates context and false positives.

## What the audit looks for (high level)

* Hard-coded secrets: API keys, DB credentials, JWT secrets, encryption keys.
* Environment variables: are secrets only in env vars and is `.env` tracked in git?
* Rotation: ability to rotate and revoke tokens, API keys, and DB credentials.
* Encryption management: use of salts, KDF parameters (bcrypt/Argon2), and secure key storage.
* Startup checks: validations preventing default dev/test secrets from being used in production.

## Repository scan highlights (example output)

* Found tracked `.env` file in repo.
* Found default JWT secret placeholder: `JWT_SECRET=your_jwt_secret_key_here`.
* Found DB credential placeholders: `DB_USER=your_db_user`, `DB_PASSWORD=your_db_password`.
* No evidence of secret rotation mechanisms or CI secret scanning configured.
* Password hashing may be using low bcrypt cost parameter.

## Key findings (summary)

| Severity |                                                       Finding | Impact                                                |
| -------- | ------------------------------------------------------------: | ----------------------------------------------------- |
| Critical | Default/placeholder JWT secret present and referenced in code | Enables token forgery if secret is unchanged          |
| Critical |        `.env` tracked in git with DB credentials in plaintext | Exposed credentials and compliance risk               |
| High     |            No secret rotation mechanism or revocation support | Long-lived secrets increase exposure window           |
| Medium   |                          Password hashing cost may be too low | Easier to brute-force/accelerate attacks              |
| High     |                     Missing environment validation on startup | Weak dev/test secrets could be deployed to production |

> **warning** If a `.env` (or any secrets file) is committed, treat the repository as potentially compromised. Remove secrets from version control, rotate them immediately, and enable CI secret scanning. Follow a documented rotation procedure.

## Evidence and examples

1. Placeholder JWT secret present

* Evidence: `.env` — contains `JWT_SECRET=your_jwt_secret_key_here`
* Evidence: `routes/auth.js` (or equivalent) references `process.env.JWT_SECRET`

2. `.env` tracked in git

* Evidence: Repository index lists `.env` as a tracked file and `.gitignore` does not exclude it

3. Database credentials in plain text

* Evidence: `.env` contains `DB_USER=your_db_user`, `DB_PASSWORD=your_db_password`
* Evidence: `config/database.js` reads these env vars directly

## Proof-of-concept — JWT forgery with known placeholder secret

This safe PoC demonstrates how an attacker can forge a token when the placeholder secret is used. Do not use forged tokens against live systems.

```javascript theme={null}
// PoC: Forge a JWT when secret is the known placeholder
const jwt = require('jsonwebtoken');

const forgedToken = jwt.sign(
  { userId: 1, email: 'admin@example.com' },
  'your_jwt_secret_key_here' // Known default secret from repo placeholder
);

console.log('Forged token:', forgedToken);
```

## Quick remediation commands

How to remove `.env` from git and add it to `.gitignore`:

```bash theme={null}
