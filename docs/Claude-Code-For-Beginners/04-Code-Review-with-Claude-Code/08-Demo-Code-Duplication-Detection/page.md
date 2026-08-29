# Claude 4 Models
"claude-opus-4-1-20250505"
"claude-opus-4-1"
"claude-opus-4-20250514"
"claude-opus-4-0"
"claude-sonnet-4-20250514"
"claude-sonnet-4-0"

# Claude 3.7 Models
"claude-3-7-sonnet-20250219"
"claude-3-7-sonnet-latest"

# Claude 3.5 Models
"claude-3-5-haiku-20241022"
"claude-3-5-haiku-latest"
```

There are SDKs and example snippets available for many languages. Two short illustrative examples:

```go theme={null}
// Go (illustrative)
package main

import (
	"context"
	"fmt"
	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
	client := anthropic.NewClient(option.WithAPIKey("my-anthropic-api-key"))
	msg, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_0,
		MaxTokens: 1024,
		Messages: []anthropic.Message{{
			Role:    "user",
			Content: "Hello, Claude",
		}},
	})
	if err != nil {
		panic(err)
	}
	fmt.Println(msg.Content)
}
```

```ruby theme={null}
# Ruby (illustrative)
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my_api_key") # or ENV["ANTHROPIC_API_KEY"]

message = anthropic.messages.create(
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
  model: "claude-sonnet-4-20250514"
)

puts(message.content)
```

> **lightbulb** Automating agents in CI/CD is a common pattern: run code-readability and security agents on pull requests, prevent merges when critical issues are found, and surface recommended fixes for developers to review before deployment.

Summary and best practices

* CLI: Use the interactive CLI to quickly generate, iterate, and run agents during development.
* SDK: Use language SDKs (Python, JS/TS, Go, Ruby, etc.) to integrate agents into CI/CD and automate checks.
* Agent files: Commit agent YAMLs to the repository so teams share the same audit and review rules.
* Permissions: Grant agents only the specific tools they need (read-only vs edit vs exec) to reduce risk.
* Model selection: Balance model capability vs. cost by selecting appropriate Sonnet/Haiku/Opus variants or inheriting the parent conversation model.

Links and references

* [Anthropic Claude Docs](https://www.anthropic.com/docs/)
* [Express.js Guide](https://expressjs.com/en/guide/routing.html)
* [express-validator](https://express-validator.github.io/docs/)
* [Node.js](https://nodejs.org/)
* Example SDKs and language docs are available from official Anthropic/Claude resources linked above.

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/a295c914-f61e-47bb-8adc-7a3145745aa6/lesson/2600436d-4843-474a-b6d2-93921ce1ef91)


# Demo Code Duplication Detection

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Code-Review-with-Claude-Code/Demo-Code-Duplication-Detection/page

Audit of an Express login demo identifying code duplication, suggesting utilities, centralized config and constants, and estimating low-effort refactors to improve DRYness and error handling

We examined a small Express login demo to identify duplication and suggest pragmatic, low-effort refactors. This walkthrough highlights where duplication exists, provides concrete code to centralize behavior, and estimates implementation effort so you can prioritize improvements quickly.

<Frame>
  <img alt="A presentation slide titled &#x22;Code Duplication Detection&#x22; with a dark teal curved panel on the right that says &#x22;Demo.&#x22; The bottom-left corner shows a small &#x22;© Copyright KodeKloud&#x22; notice." />
</Frame>

Below is the audit prompt used to drive the duplication analysis. It instructed the auditor to search for exact, near, structural, and data duplication and to produce a structured findings report.

```text theme={null}
Examine all the code in our application.

Identify and analyze code duplication in our project. Look for similar looking functions.

Check for:

1. EXACT DUPLICATES
  - Copy-pasted code blocks
  - Identical functions in different files

2. NEAR DUPLICATES
  - Similar logic with different variable names
  - Slightly modified algorithms

3. STRUCTURAL DUPLICATES
  - Similar patterns repeated
  - Boilerplate code

4. DATA DUPLICATION
  - Repeated constants
  - Configuration duplication
  - Schema duplication

For each duplication found:
 - Calculate duplication percentage
 - Suggest extraction method (function, class, module)
 - Provide DRY (Don't Repeat Yourself) solution
 - Estimate refactoring effort

Create a utilities module for common functions.

## Provide:

A structured finding report

A scale of 1/10 on how important each finding is
```

***

## Executive Summary

* Overall Duplication Score: **2.5 / 10** (Very low)
* Total Estimated Refactoring Effort: **\~3–4 hours**
* Primary files to change:
  * `routes/auth.js`
  * `config/database.js`
  * `server.js`
* Suggested new modules:
  * `utils/index.js`
  * `constants/index.js`
  * `config/index.js`

> **lightbulb** This application is already reasonably DRY. The recommendations are small, focused refactors that improve consistency and help the codebase scale with minimal effort.

***

## Findings (detailed)

### 1. EXACT DUPLICATES

**Severity: 0/10 — None found**

No exact copy-pasted blocks were identified.

***

### 2. NEAR DUPLICATES

**Severity: 3/10 — Minor issues**

2.1 Similar Error Response Patterns

* Location: `routes/auth.js` (multiple handlers)
* Duplication: \~60% similar JSON error responses repeated.

Common pattern:

```javascript theme={null}
// Pattern repeated in multiple handlers
return res.status(STATUS_CODE).json({
  error: 'MESSAGE'
});
```

Remediation: centralize error responses into a utility function and reuse it across routes.

Suggested implementation (placed under utils):

```javascript theme={null}
// utils/index.js
function createErrorResponse(res, statusCode, message, details = null) {
  const response = { error: message };
  if (details) response.details = details;
  return res.status(statusCode).json(response);
}
```

Usage:

```javascript theme={null}
// in a route handler
const { createErrorResponse } = require('../utils');
createErrorResponse(res, 401, 'Invalid credentials');
```

Effort: Low (≈30 minutes)

2.2 Database Error Handling Pattern

* Location: `routes/*` (switch-case handling of DB errors)
* Duplication: similar switch/case or if/else blocks mapping DB error codes to responses.

Example repeated pattern:

```javascript theme={null}
switch (error.code) {
  case 'ECONNREFUSED':
    return res.status(503).json({ error: 'Database connection failed' });
  case '28P01':
    return res.status(503).json({ error: 'Database authentication failed' });
  default:
    return res.status(500).json({ error: 'Database error occurred' });
}
```

Remediation: map error codes to response metadata in a utility.

Suggested implementation:

```javascript theme={null}
// utils/index.js
const DB_ERROR_MAP = {
  'ECONNREFUSED': { status: 503, message: 'Database connection failed' },
  '28P01': { status: 503, message: 'Database authentication failed' },
  '3D000': { status: 503, message: 'Database does not exist' }
};

function handleDatabaseError(error, res) {
  const errorInfo = DB_ERROR_MAP[error.code];
  if (errorInfo) {
    return createErrorResponse(res, errorInfo.status, errorInfo.message);
  }
  return createErrorResponse(res, 500, 'Database error occurred');
}
```

Effort: Medium (≈1 hour)

***

### 3. STRUCTURAL DUPLICATES

**Severity: 2/10 — Patterns are good**

* Express router usage and database event handling are consistent.
* If the app scales (multiple routers or DBs), extract a router factory or a DB connection factory to avoid boilerplate.

Suggested future extraction: connection factory that takes connection options and registers lifecycle event handlers in one place.

***

### 4. DATA DUPLICATION

**Severity: 4/10 — Moderate**

4.1 Environment Variable References — scattered across multiple files\
Examples:

```javascript theme={null}
process.env.JWT_SECRET       // auth.js
process.env.JWT_EXPIRES_IN   // auth.js
process.env.DB_HOST          // config/database.js
process.env.DB_PORT          // config/database.js
```

Remediation: centralize configuration in `config/index.js` and import where needed.

Suggested implementation:

```javascript theme={null}
// config/index.js
module.exports = {
  server: {
    port: process.env.PORT || 3000
  },
  database: {
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT) || 5432,
    name: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '24h'
  }
};
```

Effort: Low (≈1 hour)

4.2 Magic Numbers / Strings (Constants)

* Repeated HTTP statuses and literal strings make refactors error-prone.

Remediation: create `constants/index.js` to centralize HTTP status codes and common messages.

Suggested implementation:

```javascript theme={null}
// constants/index.js
module.exports = {
  HTTP_STATUS: {
    OK: 200,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    NOT_FOUND: 404,
    INTERNAL_SERVER_ERROR: 500,
    SERVICE_UNAVAILABLE: 503
  }
};
```

Effort: Low (≈45 minutes)

***

## Recommended Utilities (full example)

Create a reusable utilities module to centralize error handling, DB error mapping, and validation handling. Place this at `utils/index.js` and import in routes as needed.

```javascript theme={null}
// utils/index.js
const { HTTP_STATUS } = require('../constants');

// Error response utilities
function createErrorResponse(res, statusCode, message, details = null) {
  const response = { error: message };
  if (details) response.details = details;
  return res.status(statusCode).json(response);
}

// Database error map
const DB_ERROR_MAP = {
  'ECONNREFUSED': { status: HTTP_STATUS.SERVICE_UNAVAILABLE, message: 'Database connection failed' },
  '28P01': { status: HTTP_STATUS.SERVICE_UNAVAILABLE, message: 'Database authentication failed' },
  '3D000': { status: HTTP_STATUS.SERVICE_UNAVAILABLE, message: 'Database does not exist' }
};

function handleDatabaseError(error, res) {
  const errorInfo = DB_ERROR_MAP[error.code];
  if (errorInfo) {
    return createErrorResponse(res, errorInfo.status, errorInfo.message);
  }
  return createErrorResponse(res, HTTP_STATUS.INTERNAL_SERVER_ERROR, 'Database error occurred');
}

// Validation result handler (express-validator-style)
function handleValidationErrors(validationResult, res) {
  if (!validationResult.isEmpty()) {
    return createErrorResponse(res, HTTP_STATUS.BAD_REQUEST, 'Validation failed', validationResult.array());
  }
  return null;
}

module.exports = {
  createErrorResponse,
  handleDatabaseError,
  handleValidationErrors
};
```

Place constants in `constants/index.js` and config in `config/index.js` (examples shown earlier). Then update route handlers to:

* Use `createErrorResponse` instead of manually building response objects.
* Use `handleDatabaseError` where DB errors are handled.
* Use centralized `config` values instead of `process.env` scattered throughout the code.

***

## Implementation Priority & Estimated Effort

| Priority        | Change                           | Files                                      | Estimated Effort |
| --------------- | -------------------------------- | ------------------------------------------ | ---------------- |
| High (4/10)     | Centralize environment variables | `config/index.js` + update imports         | \~1 hour         |
| Medium (3/10)   | Create error response utilities  | `utils/index.js` + update `routes/auth.js` | \~1 hour         |
| Low (2/10)      | Extract constants                | `constants/index.js`                       | \~45 minutes     |
| Optional (1/10) | DB error mapping, router factory | `utils/index.js`, future routers           | \~30–60 minutes  |

***

## Files to Create / Modify

* Add `utils/index.js` (utilities shown above)
* Add `config/index.js` (centralized configuration)
* Add `constants/index.js` (HTTP statuses and shared strings)
* Update `routes/auth.js` to use utilities
* Update `config/database.js` to import values from `config/index.js`
* Update `server.js` to import `config.server.port` instead of process.env.PORT directly

***

> **warning** Do not commit secrets (like JWT secret or DB passwords) to source control. Use environment variables or a secrets manager and ensure `.env` is excluded from version control.

***

## Links and References

* [Express — Official Documentation](https://expressjs.com/)
* [Node.js — Official Website](https://nodejs.org/)
* [express-validator — GitHub](https://github.com/express-validator/express-validator)
* [PostgreSQL — Official Website](https://www.postgresql.org/)

***

## Final Remarks

The codebase already follows good DRY and SOLID practices. The recommended changes are incremental, low-risk refactors that yield consistent error responses, centralized configuration, and fewer duplicated patterns—helping maintenance and future scaling.

***

*Generated by Claude Code Duplication Analyzer v1.0*

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/dd033355-c556-4619-993c-ac717c0f5741/lesson/240b403c-8c15-4ced-a27a-89217a63da9f)
