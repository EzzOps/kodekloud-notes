# Demo Code Quality Metrics Standards

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Code-Review-with-Claude-Code/Demo-Code-Quality-Metrics-Standards/page

A focused code-quality audit of an Express login demo assessing complexity, coupling, cohesion, and LOC, with concrete refactor recommendations to improve readability, testability, and maintainability.

<Frame>
  <img alt="A presentation slide titled &#x22;Code Quality Metrics & Standards&#x22; with a large &#x22;Demo&#x22; label on a dark curved shape at the right. A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

This article walks through a focused code-quality audit for an Express login demo. The audit inspects code complexity, maintainability, and coupling, and it provides concrete refactor recommendations to improve readability and testability.

You can fetch the full set of prompts used for these audits from the repository:

```text theme={null}
https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts
```

<Callout icon="lightbulb">
  You can reuse the prompts from the repository to run similar audits against other codebases or to extend this analysis.
</Callout>

***

## Audit prompt (used to generate the analysis)

```text theme={null}
> Analyze code complexity across the codebase:

    Look for complex functions/methods.

    Also look at functions/methods and calculate/evaluate:

    1. CYCLOMATIC COMPLEXITY
      - Functions with complexity > 10
      - Nested if/else depth
      - Switch statement complexity
      - Recommend refactoring for high complexity

    2. COGNITIVE COMPLEXITY
      - How hard is the code to understand?
      - Nested loops and conditions
      - Recursive calls
      - Mixed levels of abstraction

    3. LINES OF CODE METRICS
      - Functions over 50 lines
      - Files over 300 lines
      - Classes over 500 lines
      - Identify candidates for splitting

    4. COUPLING METRICS
      - Afferent coupling (dependencies on this module)
      - Efferent coupling (dependencies of this module)
      - Instability index
      - Identify tightly coupled modules

    5. COHESION ANALYSIS
      - Are related functions grouped?

Provide specific refactoring recommendations for complex areas.
```

***

## What this audit looks for (quick reference)

* Cyclomatic complexity: counts decision points (if/else, switch, loops, logical operators, ternary). Typical threshold: > 10 → consider refactor.
* Cognitive complexity: a human-centered score reflecting how hard the code is to understand (deep nesting, mixed abstractions).
* Lines-of-code (LOC) metrics: functions > 50 LOC, files > 300 LOC, classes > 500 LOC suggest candidates for splitting.
* Coupling: afferent/efferent coupling and instability — identify tightly coupled modules that are hard to change or test.
* Cohesion: whether related functions are grouped and whether modules follow single-responsibility.

Note on subjectivity:

* Cyclomatic complexity is objective and easy to calculate.
* Cognitive complexity is subjective but reducing it improves maintainability and reviewability.

***

## Initial files identified by the audit

|  # | File                 | Role                         | Approx LOC |
| -: | -------------------- | ---------------------------- | ---------: |
|  1 | `server.js`          | Main application entry point |         19 |
|  2 | `routes/auth.js`     | Authentication route handler |         98 |
|  3 | `config/database.js` | Database configuration       |         19 |

***

## Executive summary

* The codebase is generally small and well-structured at a module level.
* The principal hotspot is the authentication route handler (`routes/auth.js`): the login handler mixes validation, DB access, credential verification, token creation, and error mapping in a single long function.
* Recommended immediate actions: split responsibilities (validation, service layer, token utility, error mapping) to reduce cyclomatic and cognitive complexity and to enable easier unit testing.

***

## 1. Cyclomatic Complexity

### High complexity function (> 10)

* Location: `routes/auth.js` (approx lines 17–96)
* Cyclomatic Complexity: 12
* Concerns:
  * Multiple decision points: validation checks, user lookup results, password verification, error-code mapping (switch), token creation flow.
  * Nested if/else depth and switch statement increase branching.

Suggested immediate actions:

* Extract responsibilities into separate functions:
  * Input validation
  * User lookup
  * Password check
  * Token generation
  * Error mapping (use an error-mapper utility instead of inline switch)

Representative decision points (code path):

1. Input validation (e.g., `!errors.isEmpty()`)
2. User lookup result (user found or not)
3. Password validation success/failure
4. Presence of `error.code`
5. Error mapping switch (multiple cases)
6. Token creation and response paths

***

## 2. Cognitive Complexity

* The login handler mixes domain and infrastructure logic (DB queries and business rules), increasing mixed abstractions and cognitive load.
* Nested conditionals reach three levels deep, making the flow harder to reason about during reviews.
* Recommendation: move DB and infra logic into a service layer so the route handler becomes an orchestrator that composes those services.

***

## 3. Lines-of-Code (LOC) Metrics

* Functions > 50 LOC: 1 (the login handler, \~80 lines) — candidate for splitting.
* Files > 300 LOC: none.
* Classes > 500 LOC: none.
* Recommendation: split the large handler into well-named functions or service modules to improve readability and unit testing.

***

## 4. Coupling Metrics

* The authentication module depends on several external libraries (validation, DB client, JWT).
* Afferent/efferent coupling is moderate — expected for authentication—but introducing dependency injection for the DB client and token utility will improve testability and reduce tight coupling.

***

## 5. Cohesion Analysis

* Overall project modules are cohesive (server, config, routes), but the login handler violates single-responsibility by handling multiple concerns within one function.
* Recommendation: reorganize into smaller cohesive modules (validation, authService, tokenUtil, errorMapper).

***

* Extract validation into a helper function (throws structured error on validation failure).
* Move authentication logic into an `authService` that encapsulates user lookup and password verification.
* Create a `tokenUtil` for JWT generation.
* Consolidate DB/infrastructure error mapping into a small `errorMapper` utility.

Example helper implementations (illustrative — keep for guidance):

```javascript theme={null}
// validateLoginRequest.js
const { validationResult } = require('express-validator');
const ValidationError = require('../errors/ValidationError');

const validateLoginRequest = (req) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    throw new ValidationError(errors.array());
  }
  return req.body;
};

module.exports = validateLoginRequest;
```

```javascript theme={null}
// tokenUtil.js
const jwt = require('jsonwebtoken');

const generateAuthToken = (user) => {
  return jwt.sign(
    { userId: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRES_IN || '24h' }
  );
};

module.exports = generateAuthToken;
```

Suggested final structure after refactor:

* routes/auth.js — lightweight orchestrator: validate -> authService -> tokenUtil -> response
* services/authService.js — user lookup, password verification, and business logic
* utils/tokenUtil.js — JWT creation
* utils/errorMapper.js — map DB and infra errors into HTTP-friendly errors

***

## Priority refactor list

|        Priority | Task                                                                                             | Rationale                                        |
| --------------: | ------------------------------------------------------------------------------------------------ | ------------------------------------------------ |
|   High (7–8/10) | Reduce cyclomatic complexity of login handler by extracting branching and error handling         | Lowers maintenance burden and simplifies testing |
|   High (7–8/10) | Split the login handler into multiple single-responsibility functions or an `authService` module | Improves readability and unit-testability        |
| Medium (5–6/10) | Flatten nested conditionals and separate DB/business logic                                       | Reduces cognitive complexity                     |
| Medium (5–6/10) | Introduce a centralized `errorMapper` for DB/infrastructure errors                               | Centralized mapping simplifies handler logic     |
|    Low (1–4/10) | Apply dependency injection for DB and token utilities                                            | Facilitates mocking in unit tests                |
|    Low (1–4/10) | Monitor LOC growth and add tests                                                                 | Prevents regressions and complexity creep        |

<Callout icon="warning">
  Prioritize splitting the login handler and creating the `authService`. These actions yield the highest immediate benefit for maintainability and test coverage.
</Callout>

***

## Refactoring implementation plan (phased)

* Phase 1: Add small utilities (validation helper, token util, error mapper). Keep changes backward-compatible.
* Phase 2: Move DB queries into `authService` and inject the DB client (improves testability).
* Phase 3: Replace the monolithic route handler with a slim orchestrator that composes services and returns standardized responses.
* Phase 4: Add unit tests for each service and integration tests for the route layer.

***

## Metrics summary

| Metric                     |  Current |       Target | Status               |
| -------------------------- | -------: | -----------: | -------------------- |
| Files > 300 LOC            |        0 |            0 | ✅ Good               |
| Functions > 50 LOC         |        1 |            0 | ⚠️ Needs improvement |
| Cyclomatic Complexity > 10 |        1 |            0 | ⚠️ Needs improvement |
| Cognitive Complexity > 15  |        1 |            0 | ⚠️ At threshold      |
| Module Coupling            | Moderate | Low-Moderate | ✅ Acceptable         |

***

## Concluding remarks

* The codebase has a solid module-level structure, but the authentication route handler concentrates unnecessary complexity.
* Breaking the handler into smaller functions/services (validation, service layer, token util, error mapper) will reduce cyclomatic and cognitive complexity and make the code easier to test and maintain.
* After refactors, re-run complexity analysis and add unit tests to validate improvements.

***

## Next steps

* Implement the Phase 1 refactors (validation helper, token util, error mapper) and run tests.
* Re-run static complexity checks (e.g., ESLint plugins that compute complexity) and compare metrics.
* Address any code duplication and follow DRY principles across services.

***

## Links and references

* Repository of audit prompts: [https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts](https://github.com/JeremyMorgan/Claude-Code-Reviewing-Prompts)
* express-validator: [https://express-validator.github.io/docs/](https://express-validator.github.io/docs/)
* jsonwebtoken (JWT): [https://github.com/auth0/node-jsonwebtoken](https://github.com/auth0/node-jsonwebtoken)
* Cyclomatic complexity overview: [https://en.wikipedia.org/wiki/Cyclomatic\_complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
* Cognitive complexity concept (SonarSource): [https://www.sonarsource.com/resources/what-is-cognitive-complexity/](https://www.sonarsource.com/resources/what-is-cognitive-complexity/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/dd033355-c556-4619-993c-ac717c0f5741/lesson/47965253-b4e3-4b98-8e1a-6a971255e651" />
</CardGroup>
