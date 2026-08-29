# Anyone can access the public endpoint
curl http://localhost:3000/

# Login returns a JWT, but if routes do not validate it, downstream endpoints remain unprotected:
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Recommended immediate actions (prioritized)

1. Replace any default JWT secret (e.g., JWT\_SECRET=your\_jwt\_secret\_key\_here) with a strong secret (256-bit recommended) stored in a secure secret manager.
2. Implement and apply authentication middleware (jwt.verify with algorithms/issuer/audience) across all protected routes before any business logic.
3. Add object-level ownership checks for all /:id and object-access routes; enforce deny-by-default for RBAC decisions.
4. Audit and remove or strictly protect debug/admin routes (e.g., `/seed`, `/reset`, `/debug`) in production.
5. Normalize error handling to avoid resource enumeration (use 404 for not-found and 403 for explicit access-denied where appropriate).

Full report and remediation expectations
For each finding produce:

* Title, Severity, CWE (if applicable)
* Evidence (file/function/lines)
* Why it matters
* Exploitability notes
* Minimal PoC (safe)
* Code-level remediation snippets
* Defense-in-depth guidance and recommended tests

Also produce a checklist diff marking each verification item as Pass / Fail / Not Applicable.

Notes on LLM-generated code

* LLMs synthesize examples from many sources and may suggest working but insecure defaults (weak secrets, missing validations). Treat generated code as a starting point: run automated security tests and manual code review to harden before production.

Suggested follow-up reviews

* Input validation and sanitization for user- or bot-controlled inputs (prevent SQLi, injection).
* Rate limiting and brute-force protections for sensitive routes.
* Token revocation and refresh token patterns (rotate and revoke via tokenVersion/jti).
* Logging, monitoring, and alerting for suspicious authorization failures.

Links and references

* Prompts and automation: [https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts](https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts)
* JSON Web Tokens: [https://jwt.io/](https://jwt.io/)
* OWASP Broken Access Control: [https://owasp.org/www-project-top-ten/2017/A5\_2017-Broken\_Access\_Control](https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control)

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/eaf75a67-f28f-4217-a3f9-92d411403129/lesson/7776d385-de2b-4b34-ac18-a5ca70dcb773)


# Demo Business Logic Vulnerabilities

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Security-Auditing-with-Claude-Code/Demo-Business-Logic-Vulnerabilities/page

Guide to auditing and fixing business logic vulnerabilities in web applications focusing on authentication timing attacks, rate limiting, workflow bypasses, and remediation code examples.

In this lesson we audit application business logic — the sequence of operations, rules, and state transitions that define how an application behaves as users interact with it. Business-logic vulnerabilities are often subtle and can enable attackers to bypass intended workflows, manipulate values, or expose sensitive information.

<Frame>
  <img alt="A presentation slide titled &#x22;Business Logic Vulnerabilities&#x22; with a dark blue curved panel on the right containing the word &#x22;Demo.&#x22; The bottom left shows a small &#x22;© Copyright KodeKloud&#x22; notice." />
</Frame>

What is business logic?

* Business logic implements application functionality: login/logout, purchases, transfers, approvals, workflows, and the rules that guard them.
* Small applications can still expose serious business-logic flaws (for example: user enumeration via timing differences or missing brute-force protections in a login flow).
* When auditing, focus on where server-side enforcement is missing, where state transitions are inconsistent, or where client-supplied values are treated as authoritative.

Sample interactive prompt that appears in the project context:

```text theme={null}
* Welcome to Claude Code!

/help for help, /status for your current setup

cwd: /Users/jeremy/Repos/Claude Code Course/Express-login-demo

> Try "create a util logging.py that..."

? for shortcuts

In SESSION_COOKIE_SECURITY_AUDIT.md
```

Audit assistant prompts and repo

* If you want to review the prompts used to drive these audits, they are published here:
  * [https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts](https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts)

Below is the auditing prompt we drop into the assistant to drive this business-logic review (trimmed for clarity):

```text theme={null}
Exploitability notes and, where safe, a minimal PoC or reproduction steps (no real secrets).

Remediation: precise code-level fix or config change (snippets welcome), plus defense-in-depth guidance.

A summary risk score (0–10) and top 3–5 prioritized fixes that reduce risk fastest.

A checklist diff: which items from the “Check for” list are Pass/Fail/Not Applicable.

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren't present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
```

Primary business-logic issue classes to check

* Race conditions: concurrent request handling, double-spending prevention, inventory updates.
* Price and value manipulation: client-side totals, coupon/discount abuse, currency tampering.
* Workflow bypass: skipping validation steps, status manipulation, approval-flow circumvention.
* Time-based vulnerabilities: TOCTOU (Time of Check, Time of Use), expiration bypasses, timezone issues.
* Integer overflow/underflow: calculation errors and negative-value handling.

Table — Issue classes, what to check, and examples

| Issue class        | What to verify                                                            | Example                                                        |
| ------------------ | ------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Race conditions    | Atomicity of state updates, DB transactions, optimistic/pessimistic locks | Two simultaneous checkouts decrement same inventory item       |
| Price manipulation | Server-side price calculation and validation                              | Client submits modified total or discount code directly        |
| Workflow bypass    | Endpoint sequencing, required status checks                               | Calling approval endpoint directly to mark request as approved |
| Time-based issues  | Normalize time comparisons, use server time for expiry checks             | Using client time to validate a token expiry                   |
| Integer overflow   | Use proper numeric types and bounds checks                                | Balance underflow when subtracting large values                |

Common examples and short explanations

* Double-spend / race conditions: Concurrent requests modify shared state (e.g., inventory) without suitable locking or transactional safeguards.
* Client-side price validation: Never trust totals or prices from the client; compute and validate authoritative values server-side.
* Workflow bypass: Ensure each step in a workflow enforces required checks and transitions; attackers can call endpoints out-of-order to override intended flow.
* Time-based attacks: Differences between time of check and time of use may allow expiry bypasses or TOCTOU issues.
* Integer issues: Watch for underflow/overflow in financial calculations, counters, and balances.

> **lightbulb** Always validate critical values on the server — client-side checks are for better UX only and can be bypassed by an attacker.

Example: audit output produced by the tool

```text theme={null}
Write(audits/BUSINESS_LOGIC_VULNERABILITY_AUDIT.md)
└ Wrote 203 lines to audits/BUSINESS_LOGIC_VULNERABILITY_AUDIT.md
**Application:** Express Login Demo
**Date:** 2025-08-21
**Scope:** Authentication flow, user management, and business logic security

## Executive Summary
**Risk Score: 6.5/10 (Medium-High)**
```

Key findings (summary)

* Risk Score: 6.5/10 — five vulnerabilities identified; rate limiting and timing attacks are top priority.
* Top findings:
  1. Timing attack / user enumeration via measurable response-time differences.
  2. Missing rate limiting (no brute-force protection on login endpoint).
  3. Weak JWT secret present in development configuration.
  4. Error information disclosure (detailed DB errors returned).
  5. Missing account lockout / failed-attempt tracking.

Detailed example — Timing attack (user enumeration)

* The audit flagged a measurable timing discrepancy in the authentication path. When a login attempt references a non-existent user, the code returns immediately. When a user exists, the code calls bcrypt.compare(), which adds a measurable delay (\~100 ms). Attackers can distinguish valid accounts by measuring response times across many requests.

Evidence (excerpted from `routes/auth.js:29-46`):

```javascript theme={null}
// Line 29-30: Database lookup
const userResult = await pool.query(userQuery, [email]);

// Line 32-36: Early return if user not found
if (userResult.rows.length === 0) {
  return res.status(401).json({ error: 'Invalid credentials' });
}

// Line 40: Password comparison only if user exists
const isPasswordValid = await bcrypt.compare(password, user.password);
```

Why it matters

* Early return for non-existent users vs. bcrypt.compare() for existing users produces measurable timing differences.
* Attackers can enumerate valid accounts by measuring average response times.

Remediation — normalize timing by always performing a password hash comparison, using a dummy hash when the account is not found:

```javascript theme={null}
// Perform lookup
const userResult = await pool.query(userQuery, [email]);
const user = userResult.rows[0];

// Dummy bcrypt hash (cost appropriate for your environment)
// You can generate a dummy hash once and store it in config; use the same hash for timing normalization.
const DUMMY_HASH = '$2b$10$C6UzMDM.H6dfI/f/IKcDReW1Z8G9YfnmY0g8b6KQ/7Qk7Yb1r6l6a'; // example bcrypt hash

// Use the real password hash if user exists, otherwise the dummy hash.
// This prevents response time differences between “user exists” and “user does not exist”.
const hashToCompare = user ? user.password : DUMMY_HASH;
const isPasswordValid = await bcrypt.compare(password, hashToCompare);

if (!isPasswordValid) {
  // Return the same generic error for both non-existent users and bad passwords.
  return res.status(401).json({ error: 'Invalid credentials' });
}
```

Brute-force protection — add rate limiting

* The login endpoint lacked rate limiting. Add express-rate-limit or a similar middleware to slow or block brute-force attempts.

Example using express-rate-limit:

```javascript theme={null}
const rateLimit = require('express-rate-limit');

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // limit to 5 requests per window per IP (adjust as needed)
  message: { error: 'Too many login attempts, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});

router.post('/login', loginLimiter, [/* validation middleware */], async (req, res) => {
  // existing login handler
});
```

Account lockout / failed-attempt tracking

* Implement server-side counters and temporary lockouts after repeated failures. Use business-appropriate backoff and unlock mechanisms (email or admin unlock) to avoid permanent denial for legitimate users.

Weak JWT secret

* Do not use default or development secrets in production. Generate secure secrets and fail-fast if missing.

Generate a strong secret:

```bash theme={null}
openssl rand -base64 64
```

Enforce JWT secret presence/strength at startup:

```javascript theme={null}
if (!process.env.JWT_SECRET || process.env.JWT_SECRET === 'your_jwt_secret_key_here') {
  throw new Error('JWT_SECRET must be set to a secure random value');
}
```

Error information disclosure

* Avoid returning detailed database or stack traces to clients. Log internal details server-side and return a concise, generic error to the caller.

Example error handling pattern:

```javascript theme={null}
switch (error.code) {
  case 'ECONNREFUSED':
    // internal logging
    console.error('Database error:', error.code, error.message);
    return res.status(503).json({ error: 'Service temporarily unavailable' });
  case '28P01':
    console.error('Database authentication failed:', error.code);
    return res.status(503).json({ error: 'Service temporarily unavailable' });
  default:
    console.error('Database error:', error);
    return res.status(500).json({ error: 'Internal server error' });
}
```

Checklist results (from the audit)

| Check                        | Result                                  |
| ---------------------------- | --------------------------------------- |
| Race conditions              | Pass                                    |
| Price manipulation           | Not applicable                          |
| Workflow bypass              | Pass                                    |
| Time-based vulnerabilities   | Fail (timing attack / user enumeration) |
| Integer overflow/underflow   | Not applicable                          |
| Rate limiting                | Fail                                    |
| Account lockout              | Fail                                    |
| Error information disclosure | Fail                                    |

Top 5 prioritized fixes

1. Add rate limiting on authentication endpoints.
2. Normalize authentication timing to mitigate user enumeration.
3. Validate and require a strong JWT secret; fail startup if missing.
4. Implement account lockout / failed-attempt tracking with safe unlock paths.
5. Sanitize error responses to avoid leaking internal details.

> **warning** Do not use development default secrets in production. Rotate weak secrets and enforce secure values in deployment pipelines.

Summary

* Business-logic vulnerabilities can meaningfully increase application risk even in small demos.
* In this Express login demo the primary issues were timing-based user enumeration and missing brute-force protections; both can be fixed with the code snippets above.
* After applying fixes, re-run the audit to confirm mitigations and detect regressions.

Recommended next topic: secrets management and safe secret injection into CI/CD pipelines.

Links and references

* Audit prompts repository: [https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts](https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts)
* express-rate-limit: [https://www.npmjs.com/package/express-rate-limit](https://www.npmjs.com/package/express-rate-limit)
* bcrypt documentation: [https://www.npmjs.com/package/bcrypt](https://www.npmjs.com/package/bcrypt)
* JWT best practices: [https://auth0.com/learn/json-web-tokens/](https://auth0.com/learn/json-web-tokens/)
* OWASP Authentication Cheat Sheet: [https://cheatsheetseries.owasp.org/cheatsheets/Authentication\_Cheat\_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/eaf75a67-f28f-4217-a3f9-92d411403129/lesson/3e63fe66-1df4-43dc-81b3-f09c0765f18b)
