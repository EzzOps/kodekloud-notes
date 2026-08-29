# Demo Design Pattern Implementation Review

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Code-Review-with-Claude-Code/Demo-Design-Pattern-Implementation-Review/page

Design pattern audit of an Express login demo identifying architectural issues and providing concrete code fixes to improve maintainability, testability, and security.

This lesson/article reviews common design-pattern usage in a codebase (the Express Login Demo). The objective is to identify patterns present, evaluate whether they are appropriate and correctly implemented, and recommend concrete, minimal-code remediation where needed to improve maintainability, testability, and security.

<Frame>
  <img alt="A presentation slide titled &#x22;Design Pattern Implementation Review&#x22; with a large dark curved shape on the right containing the word &#x22;Demo.&#x22; A small &#x22;© Copyright KodeKloud&#x22; note appears in the bottom-left." />
</Frame>

> **lightbulb** This article synthesizes a design-pattern analysis and provides concrete remediation snippets (JavaScript/Node.js) intended as drop-in suggestions for an Express-based login app. Use them as a starting point and adapt to your application's conventions, environment variables, and module style.

## How the analysis was run (example CLI output)

The automated inspection writes a markdown report to `audits/` and prints interactive prompts. Example (trimmed) output:

```bash theme={null}
saved to /audits/SOFTWARE_DESIGN_ARCHITECTURE_ANALYSIS.md

jeremy@MACSTUDIO Express-login-demo % claude
Welcome to Claude Code!
/help for help, /status for your current setup
cwd: /Users/jeremy/Repos/Claude Code Course/Express-login-demo

What's new:
• Fixed issue causing "OAuth authentication is currently not supported"
• Status line input now includes `exceeds_200k_tokens`
• Fixed incorrect usage tracking in /cost
• Introduced `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_OPUS_MODEL` for controlling model aliases
• Bedrock: Updated default Sonnet model to Sonnet 4

> Try "how do I log an error?"
? for shortcuts

In SOFTWARE_DESIGN_ARCHITECTURE_ANALYSIS.md
Found 1188 lines
Now creating the comprehensive design pattern analysis report...
Wrote 534 lines to audits/DESIGN_PATTERN_ANALYSIS.md
Found 49 new diagnostic issues in 1 file
```

## Analysis prompt (condensed)

This is the condensed prompt used to inspect the repo:

```text theme={null}
Review the code base for design pattern usage. Identify and evaluate:
1. CREATIONAL PATTERNS (Singleton, Factory, Builder)
2. STRUCTURAL PATTERNS (Adapter, Facade, Decorator, Proxy)
3. BEHAVIORAL PATTERNS (Strategy, Observer, Chain of Responsibility, Command)
4. DOMAIN PATTERNS (Repository, Service Layer, DTO, Domain Model)

For each pattern found:
 - Is it appropriate for the use case?
 - Is it implemented correctly?
 - Could a simpler solution work?
 - Are there missing patterns that would improve the code?

Provide:
 - A structured findings report
 - A 1–10 severity for each finding
 - Remediation: precise code-level fix or config change (snippets welcome)
Constraints:
 - Be concrete and cite code locations/identifiers where possible.
 - Prefer minimal, drop-in fix snippets.
 - Do not invent files/functions that aren't present; if context is missing, mark "Unable to verify" and say what code would prove it.
 - Write this into audits/DESIGN_PATTERN_ANALYSIS.md
```

***

## Executive summary

Key observations and prioritized recommendations for the Express Login Demo:

* Critical (9/10): Direct SQL inside route handlers — extract a Repository layer (`UserRepository`) to separate data access from HTTP concerns.
* Critical (9/10): Business logic in route handlers — create an `AuthService` (Service layer).
* High (7–8/10): Single authentication approach — introduce a Strategy abstraction for extensibility (local, OAuth, SSO).
* High (8/10): Missing JWT authentication middleware — add token verification for protected routes.
* High (7/10): Hardcoded token creation — centralize token creation with a Token Factory.
* Medium (5–6/10): No application-level event system — consider using an EventEmitter for auth events.
* Medium (5–6/10): No caching/proxy layer — consider a DatabaseProxy for cached queries.
* Low (1–4/10): Minimal DTOs/domain models — formalize responses with DTOs and add domain entities if domain complexity grows.

Recommended migration order:

1. Extract `UserRepository` (move SQL out of routes)
2. Create `AuthService` (move business logic out of controllers)
3. Add `authenticateToken` middleware for JWT verification
4. Implement `TokenFactory` to centralize token logic
5. Add application events and DTOs as next steps

> **warning** Critical security and maintainability issues detected: move data access out of route handlers and add JWT verification middleware as high-priority fixes. These reduce the attack surface, simplify testing, and improve code organization.

***

## Summary table — findings and priority

|                       Finding | Category                | Severity | Recommended action                                |
| ----------------------------: | ----------------------- | -------: | ------------------------------------------------- |
|          Direct SQL in routes | Repository              |     9/10 | Extract `UserRepository`                          |
| Business logic in controllers | Service Layer           |     9/10 | Implement `AuthService`                           |
|          Single auth approach | Behavioral / Strategy   |   7–8/10 | Add Strategy abstraction                          |
|             No JWT middleware | Structural / Middleware |     8/10 | Add `authenticateToken`                           |
|      Hardcoded token creation | Creational / Factory    |     7/10 | Implement `TokenFactory`                          |
|           No app-level events | Behavioral / Observer   |   5–6/10 | Add `AuthEventEmitter`                            |
|              No caching/proxy | Structural / Proxy      |   5–6/10 | Consider `DatabaseProxy`                          |
|          Anemic DTOs/entities | Domain                  |   1–4/10 | Introduce `UserDTO` and domain `User` when needed |

***

## Detailed findings and remediation (by pattern)

Below are grouped findings, assessments, and minimal remediation snippets. Adapt imports/exports to your project's module style (CommonJS or ES modules).

### 1. CREATIONAL PATTERNS

#### 1.1 Singleton (database connection pool)

Location: `config/database.js` (exports a shared pool)

Assessment:

* Implemented as a singleton pooling instance via `pg.Pool`. Connection and error handlers are present and sufficient.
* Severity: 3/10 — no changes required.

Example (already correct):

```javascript theme={null}
// config/database.js
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

pool.on('connect', () => {
  console.log('Connected to PostgreSQL database');
});

pool.on('error', (err) => {
  console.error('Database connection error:', err);
});

module.exports = pool;
```

References:

* [https://node-postgres.com/](https://node-postgres.com/)

#### 1.2 Factory (Token creation)

Status: Missing — centralize token generation to control claims and lifetimes.

Recommendation: TokenFactory (minimal, drop-in)

```javascript theme={null}
// utils/tokenFactory.js
const jwt = require('jsonwebtoken');

class TokenFactory {
  static createAccessToken(user) {
    return jwt.sign(
      { userId: user.id, email: user.email, type: 'access' },
      process.env.JWT_SECRET,
      { expiresIn: '15m' }
    );
  }

  static createRefreshToken(user) {
    return jwt.sign(
      { userId: user.id, type: 'refresh' },
      process.env.JWT_REFRESH_SECRET,
      { expiresIn: '7d' }
    );
  }
}

module.exports = TokenFactory;
```

Usage:

```javascript theme={null}
const TokenFactory = require('../utils/tokenFactory');
const accessToken = TokenFactory.createAccessToken(user);
```

References:

* [https://github.com/auth0/node-jsonwebtoken](https://github.com/auth0/node-jsonwebtoken)

#### 1.3 Builder

Status: Not necessary for current app complexity. Express-validator chains can act as builder-like constructs.

***

### 2. STRUCTURAL PATTERNS

#### 2.1 Facade (Express router)

Assessment:

* Express routers already act as a façade for route grouping. This is appropriate; no structural change needed.

#### 2.2 Decorator (middleware chain)

Assessment:

* Middleware is correctly used as a decorator chain for request preprocessing. Missing JWT authentication middleware — high priority.

Remediation: JWT authentication middleware

```javascript theme={null}
// middleware/authenticateToken.js
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) return res.sendStatus(401);

  jwt.verify(token, process.env.JWT_SECRET, (err, payload) => {
    if (err) return res.sendStatus(403);
    req.user = payload; // attach payload to request for downstream handlers
    next();
  });
}

module.exports = authenticateToken;
```

Use:

```javascript theme={null}
const authenticateToken = require('./middleware/authenticateToken');
app.get('/protected', authenticateToken, (req, res) => { /* ... */ });
```

References:

* [https://expressjs.com/](https://expressjs.com/)
* [https://jwt.io/](https://jwt.io/)

#### 2.3 Proxy (query caching)

Status: Not implemented. A simple DatabaseProxy can reduce DB load for frequently-run read queries.

Remediation: DatabaseProxy (in-memory TTL cache)

```javascript theme={null}
// utils/databaseProxy.js
class DatabaseProxy {
  constructor(pool, cacheTTL = 5 * 60 * 1000) {
    this.pool = pool;
    this.cache = new Map();
    this.cacheTTL = cacheTTL;
  }

  async query(text, params) {
    const key = `${text}:${JSON.stringify(params)}`;
    const cached = this.cache.get(key);

    if (cached && (Date.now() - cached.timestamp) < this.cacheTTL) {
      return cached.result;
    }

    const result = await this.pool.query(text, params);
    this.cache.set(key, { timestamp: Date.now(), result });
    return result;
  }
}

module.exports = DatabaseProxy;
```

Usage:

```javascript theme={null}
const pool = require('./config/database');
const DatabaseProxy = require('./utils/databaseProxy');
const db = new DatabaseProxy(pool);
```

Note: For production-scale caching, consider Redis or a second-level cache.

***

### 3. BEHAVIORAL PATTERNS

#### 3.1 Chain of Responsibility

Assessment:

* Express middleware is an appropriate chain-of-responsibility for request processing. No changes needed.

#### 3.2 Strategy (authentication strategies)

Status: Only a local auth approach present. If you expect OAuth, SSO, or future providers, introduce a Strategy to avoid conditional logic and make authentication pluggable.

Remediation: Minimal Strategy abstraction

```javascript theme={null}
// auth/strategies/authStrategy.js
class AuthStrategy {
  async authenticate(credentials) {
    throw new Error('authenticate() must be implemented');
  }
}
module.exports = AuthStrategy;
```

Local strategy example:

```javascript theme={null}
// auth/strategies/localStrategy.js
const AuthStrategy = require('./authStrategy');
// assume userRepository and bcrypt are available
class LocalStrategy extends AuthStrategy {
  constructor(userRepository) {
    super();
    this.userRepository = userRepository;
  }

  async authenticate({ email, password }) {
    const user = await this.userRepository.findByEmail(email);
    if (!user) throw new Error('Invalid credentials');
    const match = await bcrypt.compare(password, user.password);
    if (!match) throw new Error('Invalid credentials');
    return user;
  }
}
module.exports = LocalStrategy;
```

An AuthenticationService can select a strategy based on configuration or request context.

#### 3.3 Observer (EventEmitter)

Status: Useful for audit logging, rate-limiting, or integrations (login success/failure). Add an EventEmitter to decouple side-effects.

Remediation: auth event emitter

```javascript theme={null}
// events/authEvents.js
const EventEmitter = require('events');
class AuthEventEmitter extends EventEmitter {}
const authEvents = new AuthEventEmitter();

module.exports = authEvents;

// Example emission in auth flow:
authEvents.emit('user:login:success', { userId: user.id, ip: req.ip });

// Example listener setup (e.g., in app bootstrap)
authEvents.on('user:login:failed', ({ email, ip }) => {
  console.log(`Failed login attempt for ${email} from ${ip}`);
  // add rate-limiting or alerting hooks here
});
```

#### 3.4 Command

Status: Not needed for current app scope. Consider for background tasks or job queues.

***

### 4. DOMAIN PATTERNS

#### 4.1 Repository Pattern

Problem: Direct SQL in route handlers — example from `routes/auth.js`:

```javascript theme={null}
const userQuery = 'SELECT id, email, name, password FROM users WHERE email = $1';
const userResult = await pool.query(userQuery, [email]);
```

Assessment:

* Direct SQL in controllers violates separation of concerns. This makes testing harder and couples controllers to storage details.
* Severity: 9/10 — move SQL logic to a repository layer.

Remediation: Extract `UserRepository`

```javascript theme={null}
// repositories/UserRepository.js
class UserRepository {
  constructor(pool) {
    this.pool = pool;
  }

  async findByEmail(email) {
    const query = 'SELECT id, email, name, password FROM users WHERE email = $1';
    const result = await this.pool.query(query, [email]);
    return result.rows[0] || null;
  }

  async create({ email, name, password }) {
    const query = 'INSERT INTO users (email, name, password) VALUES ($1, $2, $3) RETURNING id, email, name';
    const result = await this.pool.query(query, [email, name, password]);
    return result.rows[0];
  }
}

module.exports = UserRepository;
```

Use this repository from services or controllers rather than executing queries directly.

References:

* Repository pattern overview: [https://martinfowler.com/eaaCatalog/repository.html](https://martinfowler.com/eaaCatalog/repository.html)

#### 4.2 Service Layer (AuthService)

Status: Auth/business logic resides in route handlers. Extract an `AuthService` to encapsulate authentication and token creation.

Remediation: `AuthService`

```javascript theme={null}
// services/AuthService.js
const bcrypt = require('bcrypt');
const TokenFactory = require('../utils/tokenFactory');

class AuthService {
  constructor(userRepository) {
    this.userRepository = userRepository;
  }

  async authenticateUser(email, plainPassword) {
    const user = await this.userRepository.findByEmail(email);
    if (!user) throw new Error('Invalid credentials');

    const match = await bcrypt.compare(plainPassword, user.password);
    if (!match) throw new Error('Invalid credentials');

    const accessToken = TokenFactory.createAccessToken(user);
    const refreshToken = TokenFactory.createRefreshToken(user);

    return {
      user,
      tokens: { accessToken, refreshToken }
    };
  }
}

module.exports = AuthService;
```

Then keep routes thin:

```javascript theme={null}
const authService = new AuthService(new UserRepository(pool));
const { user, tokens } = await authService.authenticateUser(email, password);
res.json({ token: tokens.accessToken, user: { id: user.id, email: user.email, name: user.name } });
```

#### 4.3 DTO (Data Transfer Objects)

Status: Responses are assembled inline. Use a DTO to formalize API contracts and reduce accidental leakage of sensitive fields.

Remediation: Minimal `UserDTO`

```javascript theme={null}
// dtos/UserDTO.js
class UserDTO {
  constructor(user) {
    this.id = user.id;
    this.email = user.email;
    this.name = user.name;
  }
}

module.exports = UserDTO;
```

Usage:

```javascript theme={null}
const UserDTO = require('../dtos/UserDTO');
res.json({ token, user: new UserDTO(user) });
```

#### 4.4 Domain model (User entity)

Status: Anemic domain model. Add a domain entity when business rules grow (password hashing, validation, state transitions).

Remediation: `User` entity

```javascript theme={null}
// domain/User.js
const bcrypt = require('bcrypt');

class User {
  constructor(id, email, name, password) {
    this.id = id;
    this.email = email;
    this.name = name;
    this.password = password;
  }

  static async create(email, name, plainPassword) {
    const hashedPassword = await bcrypt.hash(plainPassword, 10);
    return new User(null, email, name, hashedPassword);
  }

  async verifyPassword(plainPassword) {
    return bcrypt.compare(plainPassword, this.password);
  }

  toPublicObject() {
    return { id: this.id, email: this.email, name: this.name };
  }
}

module.exports = User;
```

Integrate `User` into repository and service flows for stronger encapsulation.

***

## Final recommendations & prioritized checklist

Immediate (apply within sprints 0–1)

* Implement `UserRepository` and update routes to use it (move SQL out of controllers).
* Create `AuthService` and move authentication logic out of route handlers.
* Add `authenticateToken` middleware and apply to protected endpoints.

Short term (next sprint)

* Implement `TokenFactory` to centralize token formats/claims.
* Add `authEvents` EventEmitter to emit login/signup events (for logging, alerts, rate-limiting hooks).
* Add `UserDTO` to formalize API responses.

Medium term (optional)

* Introduce Strategy abstraction if multiple auth providers are required (OAuth, SAML, etc.).
* Consider `DatabaseProxy` or external caching (Redis) for heavy-read endpoints.
* Add richer domain entities if domain complexity increases.

References and further reading

* Express: [https://expressjs.com/](https://expressjs.com/)
* jsonwebtoken: [https://github.com/auth0/node-jsonwebtoken](https://github.com/auth0/node-jsonwebtoken)
* Node-postgres (pg): [https://node-postgres.com/](https://node-postgres.com/)
* Repository pattern (conceptual): [https://martinfowler.com/eaaCatalog/repository.html](https://martinfowler.com/eaaCatalog/repository.html)

***

This report is intended to be actionable: suggested snippets are minimal and designed to integrate cleanly into the Express login demo to improve testability, maintainability, and security.

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/dd033355-c556-4619-993c-ac717c0f5741/lesson/3147e16f-8b9f-456d-b856-e763dc2d543d)
