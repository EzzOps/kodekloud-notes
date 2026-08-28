# Demo Authorization Implementation

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Security-Auditing-with-Claude-Code/Demo-Authorization-Implementation/page

A security assessment and remediation guide for implementing and auditing authorization, RBAC, JWT validation, object-level protections, and middleware order with concrete code fixes.

Having completed a detailed look at authentication, this lesson focuses on authorization: verifying who can do what after identity is established. We'll load Claude again, run an authorization review against the target application, and consolidate the findings, prioritized fixes, and ready-to-use remediation snippets.

<Frame>
  <img alt="A presentation slide titled &#x22;Authorization Implementation&#x22; with a dark curved shape on the right containing the word &#x22;Demo&#x22; in blue. A small &#x22;© Copyright KodeKloud&#x22; notice appears in the bottom-left." />
</Frame>

Load the prompts and automation used for this assessment from the public repository:
[https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts](https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts)

What to analyze

* Authorization implementation across all routes and endpoints.
* Broken Object Level Authorization (BOLA / IDOR).
* Broken Function Level Authorization.
* Missing authorization checks on sensitive endpoints (admin, bulk, debug).
* Role-based access control (RBAC) correctness and deny-by-default enforcement.
* Privilege escalation paths via update flows or misapplied defaults.
* JWT validation on protected routes and token revocation checks.
* Proper scope checking for API/service tokens and multi-tenant isolation.
* Field-level authorization, bulk protections, and consistent error handling.

Authorization Implementation checklist (consolidated)

| Check                                  | What to verify                                                                                    | Notes / Example                                                                    |
| -------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Object-level authorization (BOLA/IDOR) | Enforce ownership/tenant checks on GET/PUT/DELETE /:id and any identifier-based access.           | Validate IDs from URL/body/query against the authenticated user's tenantId/userId. |
| Function-level authorization           | Ensure server-side role/permission checks for all privileged routes.                              | Don't rely on client-side UI checks.                                               |
| Sensitive endpoints protected          | Audit for unprotected admin/debug/bulk export routes.                                             | Confirm middleware order: authN -> authZ -> handler.                               |
| RBAC mapping & deny-by-default         | Map roles to explicit permissions; prevent clients from setting roles.                            | Store role assignments server-side only.                                           |
| Privilege escalation vectors           | Block updates to fields like role, tenantId, isAdmin unless performed by authorized system flows. | Add field-level checks in update handlers.                                         |
| JWT verification                       | Use jwt.verify with algorithms, issuer, audience, and exp. Avoid trusting jwt.decode.             | Check jti/tokenVersion against a revocation list.                                  |
| API token scope checks                 | Enforce least-privilege scopes per token; separate user vs service tokens.                        | Validate audience and intended usage.                                              |
| Multi-tenant isolation                 | Filter list/search endpoints by tenant, enforce server-side tenant constraints.                   | Avoid client-provided tenant identifiers.                                          |
| Bulk protections                       | Verify ownership per item on bulk operations and limit sizes/rates.                               | Fail-safe per-item checks.                                                         |
| Field-level authorization              | Hide sensitive fields (SSN, apiKey, secrets) from non-privileged roles.                           | Use projection/serialization rules.                                                |
| Error handling/resource enumeration    | Return consistent 403 vs 404 to avoid leaking existence.                                          | Consider 404 when revealing existence is risky.                                    |
| Middleware ordering                    | Ensure no handlers run before auth middleware; check nested routers.                              | Use top-level auth middleware where appropriate.                                   |
| CORS & CSRF                            | Avoid wildcard origins with credentials; if cookies used, enforce SameSite/CSRF tokens.           | Harden cross-site risks.                                                           |
| Open redirect protections              | Validate redirect/next parameters against an allowlist.                                           | Prevent phishing by open redirects.                                                |
| Fallback/debug routes                  | Remove or protect `/seed`, `/reset`, `/debug` in prod.                                            | Make admin-only or gated behind feature flags.                                     |

High-level summary (assessment snapshot)

* Risk Score: 9.5/10 (Critical)
* Critical issues identified:
  1. No authentication/authorization middleware — endpoints are unprotected beyond login.
  2. Weak JWT implementation — missing strict verification parameters; possible default secrets.
  3. No RBAC or object-level authorization — vulnerable to BOLA/IDOR.
  4. Inconsistent error handling — may leak resource existence.

<Callout icon="lightbulb">
  This assessment indicates the application should not handle real user data in its current state. Immediate remediation is required before any production deployment.
</Callout>

Concrete remediation snippets

1. Authentication middleware (verify JWT)

```javascript theme={null}
// middleware/authenticate.js
const jwt = require('jsonwebtoken');

const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'] || '';
  const token = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : null;

  if (!token) {
    return res.status(401).json({ error: 'Missing Authorization token' });
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],
      issuer: process.env.JWT_ISS,   // e.g., 'your-app'
      audience: process.env.JWT_AUD // e.g., 'your-app-users'
    });
    // Keep minimal, validated claims only
    req.user = {
      userId: payload.userId,
      roles: payload.roles,
      tenantId: payload.tenantId,
      jti: payload.jti || payload.tokenVersion
    };
    return next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
};

module.exports = authenticateToken;
```

2. Issuing JWTs with recommended claims (login handler)

```javascript theme={null}
// routes/auth.js (excerpt)
const jwt = require('jsonwebtoken');

const token = jwt.sign(
  {
    userId: user.id,
    email: user.email,
    roles: user.roles,               // array or minimal role identifiers
    tenantId: user.tenantId,         // multi-tenant context if applicable
    tokenVersion: user.tokenVersion, // used to revoke tokens server-side
    iat: Math.floor(Date.now() / 1000)
  },
  process.env.JWT_SECRET,
  {
    algorithm: 'HS256',
    issuer: process.env.JWT_ISS,
    audience: process.env.JWT_AUD,
    expiresIn: '15m' // short-lived access token
  }
);
```

3. Object-level ownership authorization (authorizeOwnership middleware)

```javascript theme={null}
// middleware/authorizeOwnership.js
const pool = require('../db'); // adjust to your DB client

const authorizeOwnership = async (req, res, next) => {
  const resourceId = req.params.id;
  const userId = req.user && req.user.userId;

  if (!userId) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const result = await pool.query(
      'SELECT user_id FROM resources WHERE id = $1',
      [resourceId]
    );

    if (result.rows.length === 0) {
      // Optionally hide existence to prevent enumeration
      return res.status(404).json({ error: 'Resource not found' });
    }

    if (result.rows[0].user_id !== userId) {
      return res.status(403).json({ error: 'Access denied' });
    }

    next();
  } catch (err) {
    next(err);
  }
};

module.exports = authorizeOwnership;
```

4. Applying middleware and enforcing authN -> authZ -> handler order

```javascript theme={null}
// server.js (excerpt)
const express = require('express');
const authenticateToken = require('./middleware/authenticate');
const authorizeOwnership = require('./middleware/authorizeOwnership');
const app = express();

app.use(express.json());

// Public route
app.get('/', (req, res) => res.send('Public endpoint'));

// Protected route: authentication runs first, then ownership check, then handler
app.get('/api/resources/:id', authenticateToken, authorizeOwnership, async (req, res) => {
  // Safe to fetch and return resource because ownership was checked
  const resource = await getResourceById(req.params.id);
  res.json(resource);
});
```

Proof-of-Concept (what the assessment demonstrated)

```bash theme={null}
