# Demo Error Handling Resilience Audit

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Code-Review-with-Claude-Code/Demo-Error-Handling-Resilience-Audit/page

Audit of an Express/Node.js login demo identifying error-handling and resilience gaps, prioritizing findings, and providing minimal drop‑in remediation code and configuration suggestions

This audit inspects an Express/Node.js login demo to identify error-handling and resilience gaps, prioritize findings, and provide minimal, drop‑in remediation snippets. The goal is actionable fixes that integrate cleanly into the existing codebase (e.g., `server.js`, `routes/auth.js`, `database.js`), with minimal surface area change.

Example interactive prompt used to drive the audit:

```text theme={null}
* Welcome to [Claude Code For Beginners](https://learn.kodekloud.com/user/courses/claude-code-for-beginners)!

/help for help, /status for your current setup

cwd: /Users/jeremy/Repos/Claude Code Course/Express-login-demo

> Try "create a util `logging.py` that..."

? for shortcuts
```

Audit focus (excerpt from the evaluation prompt)

```text theme={null}
4. ERROR RECOVERY
  - Graceful degradation
  - Retry mechanisms
  - Circuit breakers
  - Fallback strategies

5. ERROR INFORMATION
  - Development vs production error details
  - Stack trace exposure
  - Error logging completeness
  - User-friendly error messages

Identify error handling gaps and provide improved implementation.

## Provide:
A structured finding report
A scale of 1/10 on how important each finding is
Remediation: precise code-level fix or config change (snippets welcome)

## Constraints & style:
Be concrete and cite exact code locations and identifiers.
Prefer minimal, drop-in fix snippets over prose.
Do not invent files or functions that aren't present; if context is missing, mark as Unable to verify and say what code would prove it.
Write this into a markdown file and place it in the audits/ folder.
```

Evaluation checklist (used during the audit)

```text theme={null}
1. ERROR HANDLING CONSISTENCY
  - Centralized error handler?
  - Uniform error responses?
  - Custom error classes vs generic Error?

2. ERROR CATEGORIES
  - 400/401/403/404/409/429/500/503 mapping

3. ASYNC ERROR HANDLING
  - Unhandled promise rejections
  - Async middleware wrapper usage

4. ERROR RECOVERY
  - Graceful degradation, retries, breakers, fallbacks

5. ERROR INFORMATION
  - Dev vs prod details, stack trace exposure, logging completeness
```

Executive summary (condensed)

* Overall score: **3.5 / 10** — current demo not ready for production.
* Major problems: no centralized error handling, inconsistent response format, unhandled promise rejections, no retry/circuit-breaker patterns, and sensitive info written to logs.
* Immediate priorities: add a centralized error middleware, register process-level handlers for unhandled rejections/uncaught exceptions, and stop logging raw error objects.

Critical findings (short table)

| Category                   | Score | Status  | Critical Issues                                  |
| -------------------------- | ----: | ------- | ------------------------------------------------ |
| Error Handling Consistency |  2/10 | FAIL    | No centralized error handling (server.js)        |
| Error Categories           |  4/10 | PARTIAL | Missing 403, 404, 429, 409 mappings              |
| Async Error Handling       |  3/10 | FAIL    | No unhandledRejection/uncaughtException handlers |
| Error Recovery             |  1/10 | FAIL    | No retry/circuit-breaker/fallback patterns       |
| Error Information          |  4/10 | PARTIAL | Console-only logs; raw error objects leaked      |

> **lightbulb** During development, verbose stack traces are helpful. In production, never expose stack traces or raw error objects to API responses or unprotected logs—use sanitized, structured logs and environment-based response behavior.

> **warning** Logging full error objects (which may include DB URIs, SQL, tokens, or user credentials) is a high-risk data-exposure vector. Sanitize or redact sensitive fields before logging.

Image: project context (keeps original placement with explanation)

<Frame>
  <img alt="A screenshot of a Visual Studio Code workspace showing a project explorer on the left and a terminal/editor pane on the right filled with notes about error handling (authorization errors, async error handling, error recovery, error information). The project is named &#x22;express-login-demo&#x22; with files like server.js, database.js, and schema.sql visible." />
</Frame>

***

## Detailed findings and concrete remediation

Below are prioritized findings with precise remediation snippets suitable for drop-in changes. Where new helper files are recommended, place them under `utils/` or `middleware/` unless your repo already contains equivalents. If a file does not exist, add it; if you prefer not to add files, the contents can be placed inline in `server.js`, but separating increases maintainability.

1. ERROR HANDLING CONSISTENCY — CRITICAL

* Location: `server.js` (top-level Express setup)
* Evidence: No centralized error middleware or standardized response format.

Current minimal example (evidence of missing middleware):

```javascript theme={null}
// server.js - simplified
app.use(express.json());
app.use('/api/auth', require('./routes/auth'));
// ❌ Missing error middleware
app.listen(PORT, () => {
  console.log('Server listening on', PORT);
});
```

Recommended remediation (drop-in): add a central error response shape and middleware.

a) ErrorResponse utility (create `utils/errorResponse.js`):

```javascript theme={null}
// utils/errorResponse.js
class ErrorResponse {
  constructor(message, statusCode = 500, details = null) {
    this.message = message;
    this.statusCode = statusCode;
    this.details = details;
  }

  toJSON() {
    return {
      error: {
        message: this.message,
        ...(this.details ? { details: this.details } : {})
      }
    };
  }
}

module.exports = ErrorResponse;
```

b) Centralized error middleware (create `middleware/errorHandler.js`):

```javascript theme={null}
// middleware/errorHandler.js
const ErrorResponse = require('../utils/errorResponse');

function errorHandler(err, req, res, next) {
  // Respect pre-built ErrorResponse instances
  if (err instanceof ErrorResponse) {
    return res.status(err.statusCode).json(err.toJSON());
  }

  const statusCode = err.statusCode || err.status || 500;
  const message = process.env.NODE_ENV === 'production'
    ? 'An unexpected error occurred.'
    : (err.message || 'Internal Server Error');

  const response = {
    error: { message }
  };

  if (process.env.NODE_ENV !== 'production' && err.stack) {
    response.error.stack = err.stack;
  }

  res.status(statusCode).json(response);
}

module.exports = errorHandler;
```

c) Mount middleware at the end of `server.js` after routes:

```javascript theme={null}
// server.js (after routes)
const errorHandler = require('./middleware/errorHandler');
// ... app.use routes above ...
app.use(errorHandler);
```

2. ERROR CATEGORIES — MEDIUM

* Current: routes only use a handful of statuses (400/401/500); missing common HTTP error mappings (403, 404, 409, 429).
* Impact: Clients and monitoring cannot reliably interpret failures.

Remediation: add a small HTTP error factory and use it in routes.

`utils/httpErrors.js`:

```javascript theme={null}
// utils/httpErrors.js
class HttpError extends Error {
  constructor(message, statusCode = 500, details = null) {
    super(message);
    this.statusCode = statusCode;
    this.details = details;
  }
}

const BadRequest = (msg, details) => new HttpError(msg || 'Bad Request', 400, details);
const Unauthorized = (msg, details) => new HttpError(msg || 'Unauthorized', 401, details);
const Forbidden = (msg, details) => new HttpError(msg || 'Forbidden', 403, details);
const NotFound = (msg, details) => new HttpError(msg || 'Not Found', 404, details);
const Conflict = (msg, details) => new HttpError(msg || 'Conflict', 409, details);
const TooManyRequests = (msg, details) => new HttpError(msg || 'Too Many Requests', 429, details);
const ServiceUnavailable = (msg, details) => new HttpError(msg || 'Service Unavailable', 503, details);

module.exports = {
  HttpError,
  BadRequest,
  Unauthorized,
  Forbidden,
  NotFound,
  Conflict,
  TooManyRequests,
  ServiceUnavailable
};
```

Usage example in `routes/auth.js`:

```javascript theme={null}
const { BadRequest, Unauthorized } = require('../utils/httpErrors');

if (!email || !password) {
  throw BadRequest('Email and password are required');
}

if (!user) {
  throw Unauthorized('Invalid credentials');
}
```

3. ASYNC ERROR HANDLING — CRITICAL

* Issues: no `process.on('unhandledRejection')` or `process.on('uncaughtException')` handlers; routes use manual try/catch scattered throughout.
* Evidence: missing global handlers in `server.js`.

Remediation:

a) Add global process handlers in `server.js` (near top, before `app.listen`):

```javascript theme={null}
// server.js (top-level)
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  if (global.__server) {
    global.__server.close(() => process.exit(1));
  } else {
    process.exit(1);
  }
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  if (global.__server) {
    global.__server.close(() => process.exit(1));
  } else {
    process.exit(1);
  }
});
```

b) Add an async wrapper to avoid repeating try/catch in every route (`middleware/asyncHandler.js`):

```javascript theme={null}
// middleware/asyncHandler.js
module.exports = fn => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};
```

Usage:

```javascript theme={null}
const asyncHandler = require('../middleware/asyncHandler');

router.post('/login', asyncHandler(async (req, res) => {
  // async code here; throw HttpError on validation failures
}));
```

4. ERROR RECOVERY — FAIL

* Issues: no retry logic for transient DB/network errors; no circuit-breaker or fallback strategies.
* Impact: transient errors lead to service outages and potential cascading failures.

Remediation (minimal, pragmatic examples):

a) Database connection retry (example `config/database.js`):

```javascript theme={null}
// config/database.js
const mongoose = require('mongoose');

async function connectWithRetry(uri, options = {}, attempts = 5, delayMs = 2000) {
  for (let i = 1; i <= attempts; i += 1) {
    try {
      await mongoose.connect(uri, options);
      console.log('Database connected');
      return;
    } catch (err) {
      console.warn(`DB connect attempt ${i} failed: ${err.message}`);
      if (i === attempts) throw err;
      await new Promise(r => setTimeout(r, delayMs));
    }
  }
}

module.exports = { connectWithRetry };
```

b) Circuit breaker helper (example using opossum — `npm i opossum`):

```javascript theme={null}
// utils/circuit.js
const CircuitBreaker = require('opossum');

function createBreaker(action, options = {}) {
  const breaker = new CircuitBreaker(action, {
    timeout: options.timeout || 3000,
    errorThresholdPercentage: options.errorThresholdPercentage || 50,
    resetTimeout: options.resetTimeout || 30000
  });
  return breaker;
}

module.exports = { createBreaker };
```

Apply breakers around brittle downstream calls (email, payment, external APIs) — do not wrap internal DB calls unless those are remote and flaky.

5. ERROR INFORMATION & LOGGING — CRITICAL / MEDIUM

* Evidence: application uses `console.log`/`console.error` and logs full error objects (including DB details).
* Impact: sensitive data (connection strings, SQL, tokens) may leak to logs.

Remediation: adopt structured logging (Winston, Pino) and sanitize inputs before logging.

a) Winston example logger (`utils/logger.js`):

```javascript theme={null}
// utils/logger.js
const { createLogger, format, transports } = require('winston');

const logger = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: format.combine(
    format.timestamp(),
    format.errors({ stack: true }),
    format.splat(),
    format.json()
  ),
  transports: [
    new transports.Console()
    // Add file / remote transports in production.
  ]
});

module.exports = logger;
```

b) Replace `console.error('Login error:', error)` with:

```javascript theme={null}
const logger = require('./utils/logger');
logger.error('Login error: %s', error.message, { stack: error.stack });
```

c) Sanitize and redact before logging:

* Never log full request body for authentication endpoints.
* Remove DB URIs, tokens, and passwords from logged objects.
* Consider sampling or PII redaction policies for high-volume endpoints.

6. ENVIRONMENT-SPECIFIC BEHAVIOR — HIGH\
   Ensure `NODE_ENV` controls verbosity:

* Development: include stack traces and verbose logs.
* Production: hide stack traces from API responses; log full details to secure destinations only.

The `errorHandler` above respects `NODE_ENV` and only includes stack traces when `NODE_ENV !== 'production'`.

***

## Priority remediation plan

|             Priority | Action                                                     | Target files / location                          |
| -------------------: | ---------------------------------------------------------- | ------------------------------------------------ |
|   Immediate (Week 1) | Centralized error handler + mount it                       | `middleware/errorHandler.js`, `server.js`        |
|   Immediate (Week 1) | Global unhandled rejection / uncaught exception handlers   | `server.js`                                      |
|   Immediate (Week 1) | Replace `console.*` with structured logger + sanitize logs | `utils/logger.js`, replace calls across codebase |
| Short-term (Month 1) | Add `asyncHandler` and refactor routes                     | `middleware/asyncHandler.js`, `routes/`          |
| Short-term (Month 1) | Standardize error types (httpErrors, ErrorResponse)        | `utils/httpErrors.js`, `utils/errorResponse.js`  |
|   Medium (Month 2–3) | Connection retry logic & circuit breaker wrappers          | `config/database.js`, `utils/circuit.js`         |
|   Medium (Month 2–3) | Implement graceful degradation & feature fallbacks         | application code & feature flags                 |

Estimated effort:

* Core fixes: 2–3 days for a small team (error middleware, global handlers, logger replacement).
* Full resilience: 2–3 months to implement retries, breakers, and staged fallbacks.

Security impact & production readiness

* Current: NOT READY for production.
* After critical fixes: improved readiness; still require monitoring, alerting, secret management, and secure logging destinations.

Notes on verification

* Audit referenced `server.js`, `routes/auth.js`, and `config/database.js`. For an automated verification run, include exact lines where `console.error` is used and route handlers are defined so tests can assert replacement by logger and async handlers.
* If any suggested file does not exist, create `utils/` and `middleware/` files as described. Alternatively, embed minimal logic into `server.js` for fast verification, but modular placement is recommended.

Final summary / checklist

* Implement the central error middleware and mount it after routes.
* Register process-level handlers for unhandled rejections and uncaught exceptions.
* Replace ad-hoc `console.*` with a structured logger (Winston/Pino) and enforce sanitization rules.
* Add `asyncHandler` to wrap async route handlers and standardize error objects via `httpErrors`/`ErrorResponse`.
* Add retry logic for DB connections and circuit-breaker wrappers for fragile external services.

Links & references

* Express error handling recommendations: [https://expressjs.com/en/guide/error-handling.html](https://expressjs.com/en/guide/error-handling.html)
* Node process `unhandledRejection` / `uncaughtException`: [https://nodejs.org/api/process.html#process\_event\_unhandledrejection](https://nodejs.org/api/process.html#process_event_unhandledrejection)
* Winston structured logging: [https://github.com/winstonjs/winston](https://github.com/winstonjs/winston)
* Opossum circuit breaker: [https://nodeshift.dev/opossum/](https://nodeshift.dev/opossum/)

Thank you for reading.

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/dd033355-c556-4619-993c-ac717c0f5741/lesson/60daca1c-a66f-4c9c-8087-8823972a6cce)
