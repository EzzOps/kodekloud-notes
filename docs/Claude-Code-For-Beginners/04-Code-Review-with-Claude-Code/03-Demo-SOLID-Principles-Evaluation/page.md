# Demo SOLID Principles Evaluation

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Code-Review-with-Claude-Code/Demo-SOLID-Principles-Evaluation/page

Automated SOLID principles audit of an Express authentication demo identifying violations, scoring adherence, and providing actionable, code-level remediation steps for incremental refactoring

This lesson demonstrates an automated SOLID principles audit run against an Express authentication demo. The audit inspects architecture, domain boundaries, and implementation patterns, rates adherence to SOLID, and produces concrete, actionable remediation steps suitable for incremental refactoring.

> **lightbulb** This article summarizes the audit prompt, the SOLID principles checked, and the structured findings (with code-level remediation examples). Use the recommendations as minimal, drop-in changes where possible to improve testability, maintainability, and extensibility.

Below is the prompt used to drive the audit (kept verbatim for context):

```text theme={null}
cwd: /Users/jeremy/Repos/[Claude Code For Beginners](https://learn.kodekloud.com/user/courses/claude-code-for-beginners)/Express-login-demo

What's new:
• Fixed issue causing "OAuth authentication is currently not supported"
• Status line input now includes `exceeds_200k_tokens`
• Fixed incorrect usage tracking in /cost.
• Introduced `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_OPUS_MODEL` for controlling model aliases opusplan, opus, and sonnet.
• Bedrock: Updated default Sonnet model to Sonnet 4

> [Pasted text #1 +47 lines]
```

You can see the audit prompt asked for a line-by-line, code-location-aware SOLID evaluation and remediation. The audit evaluates:

* Single Responsibility Principle (SRP)
* Open/Closed Principle (OCP)
* Liskov Substitution Principle (LSP)
* Interface Segregation Principle (ISP)
* Dependency Inversion Principle (DIP)

Audit checklist used:

* SRP: Does each module have one reason to change? Identify modules violating SRP.
* OCP: Can we extend without modifying core logic? Look for hard-coded switch statements and if/else chains that should be polymorphic.
* LSP: Do derived classes properly extend base classes and preserve expected behavior?
* ISP: Are interfaces (or implicit method contracts) too large? Do clients depend on methods they don't use?
* DIP: Are modules depending on abstractions or concrete implementations? Check for constructor injection vs `new`/direct imports/use of low-level modules.

***

Application: Express Login Demo

Summary: The automated audit identified multiple violations across SOLID principles. The highest priority issues are concentrated in the auth route and direct use of low-level services (database, env, crypto). The recommendations below prioritize small, testable refactors that introduce seams for dependency injection and better separation of concerns.

## Quick Scores

| Principle | Score (out of 10) | Primary Concern                                                      |
| --------: | :---------------: | -------------------------------------------------------------------- |
|       SRP |        3/10       | Monolithic auth handler (validation, DB, crypto, JWT, error mapping) |
|       OCP |        4/10       | Hardcoded error switches and conditional logic                       |
|       LSP |        6/10       | Direct DB Pool construction blocks substitution and mocks            |
|       ISP |        5/10       | Handlers coupled to entire Express req/res objects                   |
|       DIP |        2/10       | High-level logic depends on concrete DB/env/crypto implementations   |

***

## Detailed Findings

### 1. Single Responsibility Principle (SRP) — Score: 3/10

High-severity violation: Monolithic auth route handler

* Location: `routes/auth.js:17-96` — `/login` route handler
* Issue: A single handler performs input validation, database queries, password checking, JWT generation, and error mapping.
* Impact: Multiple reasons to change (validation rules, auth flow, DB schema, token settings, error handling) increase coupling, reduce testability, and raise maintenance cost.

Anti-pattern example (simplified):

```javascript theme={null}
// routes/auth.js (simplified)
router.post('/login', async (req, res) => {
  // 1. Validate req.body
  // 2. Query database for user
  // 3. Compare password with bcrypt
  // 4. Generate JWT
  // 5. Handle and map errors to responses
  // ... ~79 lines of mixed concerns
});
```

Remediation: Split responsibilities into repository, service, and controller layers. Keep route handlers thin; move business logic into services and data access into repositories.

Example refactor (repository, service, controller):

```javascript theme={null}
// repositories/userRepository.js
class UserRepository {
  constructor(pool) { this.pool = pool; }
  async findByEmail(email) {
    const result = await this.pool.query('SELECT * FROM users WHERE email = $1', [email]);
    return result.rows[0];
  }
}
module.exports = UserRepository;

// services/authService.js
const bcrypt = require('bcrypt');
class AuthService {
  constructor(userRepository, jwtService) {
    this.userRepository = userRepository;
    this.jwtService = jwtService;
  }
  async login(email, password) {
    const user = await this.userRepository.findByEmail(email);
    if (!user) throw new Error('InvalidCredentials');
    const match = await bcrypt.compare(password, user.password_hash);
    if (!match) throw new Error('InvalidCredentials');
    return this.jwtService.generateToken({ id: user.id, email: user.email });
  }
}
module.exports = AuthService;

// routes/auth.js (controller)
const authController = (authService) => ({
  async login(req, res) {
    try {
      const token = await authService.login(req.body.email, req.body.password);
      res.json({ token });
    } catch (err) {
      // map domain errors to http responses
      res.status(401).json({ error: err.message });
    }
  }
});
```

Recommendation: Wire concrete implementations at bootstrap so controllers receive dependencies via constructor injection. This keeps handlers small, focused, and unit-testable.

***

### 2. Open/Closed Principle (OCP) — Score: 4/10

Medium-severity violations: Hardcoded error handling and switch statements

* Issue: Error handling logic contains switch statements on error codes. Adding new error cases requires editing the same function, violating OCP.
* Impact: Changing behavior for new error codes forces modifications in central logic rather than extending it.

Anti-pattern:

```javascript theme={null}
// Anti-pattern
switch (error.code) {
  case 'ECONNREFUSED':
    return res.status(503).json({ error: 'Database connection failed' });
  case '28P01':
    return res.status(503).json({ error: 'Database authentication failed' });
  // every new error code needs modifying this switch
}
```

Remediation: Implement an extensible error mapping strategy (map lookup or registry) so new mappings can be added without modifying core error handling logic.

Example:

```javascript theme={null}
// errorMapping.js
const errorMap = {
  ECONNREFUSED: { status: 503, body: { error: 'Database connection failed' } },
  '28P01': { status: 503, body: { error: 'Database authentication failed' } },
};

function mapDbError(err) {
  return errorMap[err.code] || { status: 500, body: { error: 'Internal Server Error' } };
}
module.exports = { mapDbError };

// Usage in route/service
const { mapDbError } = require('./errorMapping');
const { status, body } = mapDbError(err);
res.status(status).json(body);
```

This converts conditionals into data-driven behavior, enabling extension via configuration files or registration APIs.

***

### 3. Liskov Substitution Principle (LSP) — Score: 6/10

Issues: Limited abstraction for database clients; direct instantiation prevents safe substitution with mocks or alternate DB adapters.

* Problem: The code constructs a `Pool` in multiple locations, making it hard to replace with a mock or different DB adapter.
* Impact: Tests require a real DB connection or heavy mocking; swapping databases is expensive.

Remediation: Introduce an adapter base class and implement concrete adapters (Postgres, Mock) that conform to the same contract.

Example adapter pattern:

```javascript theme={null}
// adapters/databaseAdapter.js
class DatabaseAdapter {
  async query(text, params) { throw new Error('Must implement query'); }
}
module.exports = DatabaseAdapter;

// adapters/postgresAdapter.js
const { Pool } = require('pg');
const DatabaseAdapter = require('./databaseAdapter');

class PostgresAdapter extends DatabaseAdapter {
  constructor(config) {
    super();
    this.pool = new Pool(config);
  }
  async query(text, params) {
    return this.pool.query(text, params);
  }
}
module.exports = PostgresAdapter;
```

Construct adapters at bootstrap and inject them where needed. Tests can provide a mock adapter that adheres to the same contract, preserving substitutability.

***

### 4. Interface Segregation Principle (ISP) — Score: 5/10

Analysis: JavaScript's dynamic typing limits formal interfaces, but conceptual violations still exist.

* Issue: Route handlers depend on full Express `req`/`res` even when they use only a subset (e.g., `req.body.email`, `res.json`).
* Impact: Tight coupling to Express complicates unit testing and reuse.

Anti-pattern:

```javascript theme={null}
// route handler tied to full req/res
router.post('/login', (req, res) => {
  // uses req.body.email, req.body.password, and res.send/json/status
});
```

Remediation: Define handler interfaces that accept only necessary inputs and a minimal response handler. This decouples business logic from Express and simplifies unit tests.

Example lightweight handler interface:

```javascript theme={null}
// controllers/loginController.js
const loginHandler = async ({ email, password }, responseHandler) => {
  try {
    const token = await authService.login(email, password);
    responseHandler.success({ token });
  } catch (err) {
    responseHandler.error(401, { error: err.message });
  }
};

// wiring in routes
router.post('/login', (req, res) => {
  const credentials = { email: req.body.email, password: req.body.password };
  const responseHandler = {
    success: (data) => res.json(data),
    error: (status, body) => res.status(status).json(body),
  };
  loginHandler(credentials, responseHandler);
});
```

This approach reduces the surface area of dependencies and adheres to ISP by not forcing handlers to accept unused methods or objects.

***

### 5. Dependency Inversion Principle (DIP) — Score: 2/10

Critical violation: High-level auth logic depends on low-level implementations (DB pool, `process.env`, bcrypt/jwt concrete imports).

* Location: `routes/auth.js:5` — `const pool = require('../config/database');`
* Impact: Tight coupling prevents unit testing without DB, and swapping implementations is difficult. Direct access to `process.env` reduces test isolation.

> **warning** Critical: High-level modules should depend on abstractions. Introduce repository/adapter interfaces, service wrappers for third-party libs (jwt, bcrypt, crypto), and a ConfigService to encapsulate environment access before proceeding with large refactors.

Remediation: Introduce abstractions and inject dependencies (repositories, jwt service, config service). Wrap third-party libraries behind small, test-friendly services that act as seams.

Example repository + service + bootstrap wiring:

```javascript theme={null}
// repositories/userRepository.js (interface-like)
class UserRepository {
  async findByEmail(email) { throw new Error('Not implemented'); }
}
module.exports = UserRepository;

// repositories/postgresUserRepository.js
const UserRepository = require('./userRepository');
class PostgresUserRepository extends UserRepository {
  constructor(dbAdapter) { super(); this.db = dbAdapter; }
  async findByEmail(email) {
    const result = await this.db.query('SELECT * FROM users WHERE email = $1', [email]);
    return result.rows[0];
  }
}
module.exports = PostgresUserRepository;

// services/jwtService.js
class JwtService {
  constructor(config) { this.config = config; }
  generateToken(payload) {
    const jwt = require('jsonwebtoken'); // JwtService is the seam for mocking
    return jwt.sign(payload, this.config.jwtSecret, { expiresIn: this.config.jwtExpiresIn });
  }
}
module.exports = JwtService;

// Application wiring (bootstrap)
const config = { jwtSecret: process.env.JWT_SECRET, jwtExpiresIn: process.env.JWT_EXPIRES_IN || '24h' };
const dbAdapter = new PostgresAdapter(pgConfig);
const userRepository = new PostgresUserRepository(dbAdapter);
const jwtService = new JwtService(config);
const authService = new AuthService(userRepository, jwtService);
```

Also prefer injecting a `ConfigService` instead of scattering `process.env` throughout the codebase:

```javascript theme={null}
// services/configService.js
class ConfigService {
  get jwtSecret() { return process.env.JWT_SECRET; }
  get jwtExpiresIn() { return process.env.JWT_EXPIRES_IN || '24h'; }
}
module.exports = new ConfigService();
```

Hardcoded crypto/third-party dependencies should be wrapped so they can be replaced with test doubles during unit tests.

***

## Priority Remediation Plan

Follow an incremental, low-risk migration strategy: introduce seams and keep current behavior until replacements are proven.

|                          Phase | Focus                                  | Actions                                                                                                                                                         |
| -----------------------------: | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Phase 1 — Critical / Immediate | Make auth testable and reduce coupling | - Extract AuthService, UserRepository, JwtService, ConfigService. - Replace direct DB error switches with mapping. - Add centralized error handling middleware. |
|                 Phase 2 — High | Replace concrete third-party usage     | - Wrap crypto/bcrypt/jwt in service wrappers. - Add simple DI container or bootstrap wiring to compose dependencies.                                            |
|               Phase 3 — Medium | Extendability & testing                | - Implement pluggable auth strategies (OAuth, LDAP) using Strategy pattern. - Introduce test doubles (mocks/fakes) for adapters.                                |

Recommended file layout (example):

```text theme={null}
├── services/
│   ├── authService.js
│   ├── jwtService.js
│   └── configService.js
├── repositories/
│   └── userRepository.js
├── adapters/
│   └── postgresAdapter.js
├── strategies/
│   └── authStrategies.js
├── middleware/
│   ├── validation.js
│   └── errorHandler.js
```

***

## Code Quality Metrics (audit snapshot)

* Cyclomatic Complexity: High (login function has 8+ decision points)
* Lines per Function: Excessive (login function ≈ 79 lines)
* Coupling: High (direct dependencies on 5+ low-level modules)
* Testability: Poor (no DI, direct env & DB usage)

Final assessment: The application demonstrates some separation of concerns but requires targeted refactors to meet SOLID expectations. Start with seams for DI and thin controllers; this yields immediate improvements in testability and maintainability while allowing gradual replacement of concrete implementations.

The audit also notes that common example code patterns can bias generated or copied code toward imperfect designs—this repo appears influenced by such patterns. Use the remediation plan above to progressively harden the codebase.

Prompts used for code review are available in the repository referenced below.

<Frame>
  <img alt="A dark-mode GitHub repository page titled &#x22;Claude-Code-Reviewing-Prompts&#x22; listing many markdown files (e.g., 000-initial-project.md, LICENSE, authentication-flow-review.md) and repo details. A code editor/IDE with files and code is visible in the background around the browser window." />
</Frame>

## Links and References

* [Express.js Documentation](https://expressjs.com/)
* [Node.js Documentation](https://nodejs.org/en/docs/)
* [jsonwebtoken (JWT)](https://www.npmjs.com/package/jsonwebtoken)
* [bcrypt (password hashing)](https://www.npmjs.com/package/bcrypt)
* [pg (node-postgres)](https://node-postgres.com/)
* [SOLID Principles Overview](https://en.wikipedia.org/wiki/SOLID)

Consider reviewing error handling and resilience as a next step.

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/dd033355-c556-4619-993c-ac717c0f5741/lesson/5b31cb19-905f-4582-9078-640cc8a8c37a)
