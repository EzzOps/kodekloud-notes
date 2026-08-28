# Demo Exception Flow Analysis

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Code-Review-with-Claude-Code/Demo-Exception-Flow-Analysis/page

Audit of Express login demo focusing on error handling, database resilience, JWT hardening, structured logging, and prioritized minimal fixes for improved reliability and observability

In this lesson we audit how an Express-based login demo handles exceptions. The goal is to trace error flows for critical failure paths, identify anti-patterns, and provide prioritized, minimal remediation snippets to standardize error handling across the app.

<Frame>
  <img alt="A presentation slide titled &#x22;Exception Flow Analysis&#x22; with a large &#x22;Demo&#x22; label on a dark curved shape at right. A small &#x22;© Copyright KodeKloud&#x22; appears in the lower-left corner." />
</Frame>

<Callout icon="lightbulb">
  This audit focuses on improving Express error handling, Node.js process safety, PostgreSQL connection resilience, JWT configuration, and observability (structured logging and metrics). The recommendations favor low-friction, drop-in fixes that can be prioritized by severity.
</Callout>

## Objective

Trace error handling through the application for these critical paths:

1. Database connection failure
2. Third-party API timeout
3. Invalid user input
4. Authentication failure
5. File system errors

For each path, verify:

* Where the error is caught
* How it is transformed
* What gets logged
* What the user sees
* Whether the system state remains consistent

Also identify common anti-patterns (swallowed exceptions, catch-all handlers, errors-as-flow-control, missing boundaries, inconsistent error formats) and provide:

* A standardized error response template
* Prioritized remediation steps (favor small, drop-in improvements first)

Example CLI context observed during the audit:

```bash theme={null}
jeremy@MACSTUDIO Express-login-demo % claude
* Welcome to Claude Code!
/help for help, /status for your current setup
cwd: /Users/jeremy/Repos/Claude Code Course/Express-login-demo
> Evaluate this entire application.
```

***

## Executive summary

The application contains multiple error handling gaps that can lead to service disruption, information disclosure, and inconsistent state. Key issues:

* No global error middleware or consistent error response format.
* PostgreSQL pool lacks connection limits and query timeouts.
* Logging is console-only (no structured logs or centralized monitoring).
* JWT creation/verification lacks explicit algorithm and startup secret validation.
* No rate limiting or account lockout for authentication attempts.
* No retry/circuit-breaker or graceful degradation strategies for dependencies.

Prioritize: 1) global error handler and process-level safety, 2) DB pool timeouts and query timeouts, 3) structured logging + JWT hardening, 4) rate limiting and lockout.

***

## Application architecture (short)

* Main server: `server.js` — no global error middleware, and no request-level timeouts configured.
* Authentication route: `routes/auth.js` — single POST `/api/auth/login` handler; validation exists but is inconsistent.
* Database config: `config/database.js` — creates a PostgreSQL pool without limits/timeouts.

Dependencies referenced:

* Express — [https://expressjs.com/](https://expressjs.com/)
* jsonwebtoken — [https://github.com/auth0/node-jsonwebtoken](https://github.com/auth0/node-jsonwebtoken)
* bcrypt — [https://www.npmjs.com/package/bcrypt](https://www.npmjs.com/package/bcrypt)
* pg (node-postgres) — [https://node-postgres.com/](https://node-postgres.com/)
* express-validator — [https://express-validator.github.io/docs/](https://express-validator.github.io/docs/)

Note: No filesystem operations or third-party API clients were found in the scanned code. If added later, apply the same resilience patterns.

***

## Audit findings (critical paths)

### 1) Database connection / query failure — Severity: 9/10

Error origin locations:

* `config/database.js:3-9` — pool created without connection/timeouts
* `routes/auth.js:30` — DB query executed without query-level timeout

Observed flow:
PostgreSQL Connection Error -> pool.query() -> routes/auth.js catch -> error.code switch -> user-facing 5xx

What’s good:

* Some specific PostgreSQL error codes are mapped to 503 responses.

Gaps:

* No query-level timeouts or server-side statement\_timeout configured.
* Pool has no `max`, `connectionTimeoutMillis`, `idleTimeoutMillis`.
* No retry/circuit-breaker for transient DB errors.
* Sensitive error details written to console.

Recommended minimal changes:

* Add pool limits/timeouts.
* Wrap queries with a timeout helper.
* Consider server-side statement\_timeout or client cancellation for long queries.

### 2) Third-party API timeouts — Not present (info)

No third-party HTTP clients detected. For any future integrations, require:

* request-level timeouts
* retry with exponential backoff
* a circuit-breaker pattern (e.g., opossum)

### 3) Invalid user input — Severity: 6/10

Good:

* Email format validation and normalization via express-validator in places.
* Some password length checks.

Gaps:

* No consistent max-length enforcement on inputs.
* Output sanitization (XSS) not addressed if server reflects user input.
* Validation error details exposed to clients (can leak internal structure).
* No rate limiting for endpoints that validate input (DoS risk).

Fixes:

* Enforce RFC-consistent max lengths (email \<= 254) and password reasonable max.
* Sanitize output where appropriate.
* Return minimal, structured validation error responses.

### 4) Authentication failure handling — Severity: 7/10

Good:

* Generic message for invalid credentials (reduces user enumeration).
* Uses bcrypt.compare for password checks.
* 401 status code returned for invalid credentials.

Gaps:

* No startup validation that `JWT_SECRET` exists.
* JWT signing lacks explicit algorithm and secure defaults (expiresIn).
* No express-rate-limit or account lockout to mitigate brute-force.
* JWT expiry values not validated at startup.

Fixes:

* Validate JWT secret on boot.
* Sign tokens with algorithm and expiresIn.
* Add rate limiting and user lockout after failed attempts.

### 5) File system errors — Not present

No `fs` usage found. Future FS operations should include permission checks, try/catch, and path validation.

***

## Error handling anti-patterns (summary)

1. Generic catch-all handlers that swallow context — Severity: 8/10
2. Console-only logging; no structured logs — Severity: 7/10
3. Missing global error handler / middleware — Severity: 9/10
4. No error boundaries or circuit breakers — Severity: 8/10
5. Inconsistent error response formats — Severity: 5/10

Example of console-only logging that should be replaced:

```javascript theme={null}
// routes/auth.js
console.error('Login error:', error);
```

Replace ad-hoc console.\* calls with a logger and centralized error handling.

***

## Error flow (conceptual)

Input Validation          Authentication         Database          JWT\
(400 errors)              (401 errors)           (503 errors)      (500)

|
v

TRANSFORMATION LAYER

Validation Details    Auth Check Generic Msg    DB Error Code Switch

|
v

FINAL HANDLING

HTTP Status Code    Error JSON Response   Structured Log (sensitive data redacted)

|
v

RECOVERY MECHANISMS
✖ NONE PRESENT\
Missing: Retry logic, circuit breakers, graceful degradation

***

## Structured findings (prioritized)

|  # | Finding                          | Location                 | Severity | Impact                            | Remediation Complexity |
| -: | -------------------------------- | ------------------------ | -------: | --------------------------------- | ---------------------- |
|  1 | Missing global error handler     | `server.js`              |     9/10 | Service crash on unhandled errors | Low                    |
|  2 | DB pool without timeouts/limits  | `config/database.js:3-9` |     9/10 | Resource exhaustion / hangs       | Medium                 |
|  3 | Generic error swallowing         | `routes/auth.js:92-94`   |     8/10 | Hidden issues                     | Low                    |
|  4 | No DB circuit breaker / retries  | `routes/auth.js:68-96`   |     8/10 | Cascading failures                | High                   |
|  5 | Insecure/weak JWT config         | `routes/auth.js:48-57`   |     7/10 | Token compromise                  | Low                    |
|  6 | No auth rate limiting/lockout    | `routes/auth.js:17-96`   |     7/10 | Brute force attacks               | Medium                 |
|  7 | Console-only logging             | `routes/auth.js:69`      |     7/10 | Poor observability                | Medium                 |
|  8 | No input length limits           | `routes/auth.js:10-16`   |     6/10 | DoS via large payloads            | Low                    |
|  9 | Validation error detail exposure | `routes/auth.js:20-25`   |     5/10 | Info disclosure                   | Low                    |
| 10 | Inconsistent error formats       | Multiple                 |     5/10 | Client/integration issues         | Medium                 |

***

## Detailed remediation guide (practical snippets)

Priorities: Fix global handler and DB timeouts first, then logging, JWT hardening, and rate limiting.

### 1) Add a global error handler (Immediate)

Place this after all route registrations in `server.js`:

```javascript theme={null}
// server.js (after routes)
app.use((err, req, res, next) => {
  // Use structured logging in production instead of console.error
  console.error('Unhandled error:', err);

  const message = process.env.NODE_ENV === 'production'
    ? 'Internal server error'
    : err.message || 'Internal server error';

  // Standardized response
  res.status(err.status || 500).json({
    error: {
      type: err.type || 'InternalError',
      message
    }
  });
});
```

Handle process-level failures (place early in server startup). Warning: practice caution with process.exit in production; prefer graceful shutdown with drains and alerts.

```javascript theme={null}
// process-level handlers - place in server startup file
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Consider graceful shutdown or alerting here
  process.exit(1);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  // Consider graceful shutdown or alerting here
  process.exit(1);
});
```

<Callout icon="warning">
  Be careful using process.exit in production. Instead, try to perform a graceful shutdown: stop accepting new requests, finish inflight requests, flush logs, and then exit. Uncontrolled exits can cause cascading failures in some orchestrated environments.
</Callout>

### 2) Harden database pool and add query timeouts (High priority)

Update `config/database.js` to set pool limits and timeouts:

```javascript theme={null}
// config/database.js
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // max connections
  idleTimeoutMillis: 30000,      // 30s
  connectionTimeoutMillis: 30000 // 30s to obtain a new connection
});

module.exports = pool;
```

Add a small helper to enforce a query timeout around `pool.query()`:

```javascript theme={null}
// utils/db.js
const queryWithTimeout = (pool, text, params = [], timeout = 10000) => {
  return Promise.race([
    pool.query(text, params),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Query timed out')), timeout)
    )
  ]);
};

module.exports = { queryWithTimeout };
```

Note: Promise.race will reject after the timeout but does not cancel the in-flight server-side query. To stop long-running queries on the DB, configure PostgreSQL's statement\_timeout or use client cancellation APIs where available.

Replace direct `pool.query(...)` calls with `queryWithTimeout(pool, sql, params, 10000)` or configure server-side statement\_timeout for per-connection or per-query protection.

### 3) Validate JWT secret and sign tokens securely

Fail fast if the JWT secret is missing:

```javascript theme={null}
// startup or server.js
if (!process.env.JWT_SECRET) {
  throw new Error('JWT_SECRET environment variable is required');
}
```

Sign tokens with algorithm and expiry:

```javascript theme={null}
// routes/auth.js
const token = jwt.sign(
  { sub: user.id, email: user.email },
  process.env.JWT_SECRET,
  { algorithm: 'HS256', expiresIn: '1h' }
);
```

Verify tokens using the same algorithms option:

```javascript theme={null}
jwt.verify(token, process.env.JWT_SECRET, { algorithms: ['HS256'] });
```

### 4) Add rate limiting for authentication endpoints

Install and register express-rate-limit:

```javascript theme={null}
// server.js
const rateLimit = require('express-rate-limit');

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5,                   // limit each IP to 5 login attempts per windowMs
  skipSuccessfulRequests: true,
  message: { error: 'Too many login attempts, please try again later' }
});

app.use('/api/auth/login', loginLimiter);
```

Consider additional account-level lockout logic (persist failed attempt counts) and exponential backoff.

### 5) Structured logging (replace console.\*)

Create a logger (example using winston) and use it across the app:

```javascript theme={null}
// utils/logger.js
const { createLogger, format, transports } = require('winston');

const logger = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: format.combine(
    format.timestamp(),
    format.errors({ stack: true }),
    format.json()
  ),
  transports: [
    new transports.Console()
    // add file or cloud transports (ELK, CloudWatch) as needed
  ]
});

module.exports = logger;
```

Replace `console.error` / `console.log` with `logger.error()` / `logger.info()` and avoid logging sensitive data like plaintext passwords or secrets.

### 6) Improve input validation and sanitization

Use express-validator and return minimal validation errors:

```javascript theme={null}
// routes/auth.js
const { body, validationResult } = require('express-validator');

router.post('/login', [
  body('email')
    .isEmail()
    .withMessage('Please provide a valid email address')
    .normalizeEmail()
    .isLength({ max: 254 }).withMessage('Email too long'),
  body('password')
    .isLength({ min: 8, max: 128 }).withMessage('Password must be 8-128 characters long')
], async (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: { type: 'ValidationError', message: 'Validation failed' }
    });
  }
  // ...rest of handler
});
```

Do not expose full validation stacks in production; return concise, actionable messages.

### 7) Standardized error response helper

Centralize error response formatting:

```javascript theme={null}
// utils/error-response.js
const sendErrorResponse = (res, statusCode, errorType, message, details = null) => {
  const payload = {
    error: {
      type: errorType,
      message
    }
  };
  if (details && process.env.NODE_ENV !== 'production') {
    payload.error.details = details;
  }
  return res.status(statusCode).json(payload);
};

module.exports = { sendErrorResponse };
```

Use this helper everywhere for consistent client-facing responses.

***

## Testing suggestions (quick checks)

* Simulate long DB queries to verify timeouts:

```bash theme={null}
