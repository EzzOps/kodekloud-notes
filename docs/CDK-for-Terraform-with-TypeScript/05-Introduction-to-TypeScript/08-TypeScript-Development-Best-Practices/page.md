# Install dependencies (run once when you open the project)
yarn install

# Start the development build/watch process
yarn dev
```

A simple runtime example:

```typescript theme={null}
console.log("Let's go!!");
```

When the dev process is running, changes to files restart compilation and show runtime logs automatically.

Meet Elmer Codde: he's building an app to manage ducks on his pond. The app will include common actions such as making ducks quack, fly, and land. The first step is storing basic information about each duck (name, age, type, color).

<Frame>
  <img alt="A slide titled &#x22;Elmer – Introduction&#x22; shows a developer icon labeled &#x22;Elmer Code&#x22; with a speech bubble &#x22;Build an app.&#x22; An arrow labeled &#x22;Manage&#x22; points to a blue &#x22;Pond&#x22; containing nine circular duck icons, each labeled &#x22;duck.&#x22;" />
</Frame>

## Variables in TypeScript

TypeScript builds on JavaScript's `const`, `let`, and `var` keywords but adds static typing. Best practice is to prefer `const` and `let` over `var`.

| Keyword |                          Mutability | When to use                                | Example                             |
| ------- | ----------------------------------: | ------------------------------------------ | ----------------------------------- |
| `const` | Immutable binding (no reassignment) | For values that should never be reassigned | `const duckName: string = "Daffy";` |
| `let`   |                     Mutable binding | For values that will change over time      | `let duckAge: number = 3;`          |
| `var`   |            Function-scoped, hoisted | Legacy code only — avoid in modern TS/JS   | `var legacyDuck = "Old";`           |

Examples

Explicit typing with `const` (cannot be reassigned):

```typescript theme={null}
const duckName: string = "Daffy";
const duckAge: number = 3;

console.log(duckName); // Output: Daffy
```

Attempting to reassign a `const` triggers a compile-time error:

```typescript theme={null}
const duckAge: number = 3;
// duckAge = 4; // Error: Cannot assign to 'duckAge' because it is a constant.
```

Using `let` allows reassignment:

```typescript theme={null}
let mutableDuckName: string = "Daffy";
let mutableDuckAge: number = 3;

mutableDuckAge = 4; // OK
mutableDuckName = "Donald"; // OK

console.log(mutableDuckName, mutableDuckAge); // Output: Donald 4
```

## Explicit typing vs. type inference

TypeScript supports both explicit annotations and inference. When the type is obvious from the initializer, you can omit the annotation and let the compiler infer the type.

* Explicit typing: you declare variable types directly.
* Type inference: TypeScript infers the variable's type from its initial value and enforces it afterward.

Examples:

```typescript theme={null}
// Explicit typing
let duckType: string = "Mallard";

// Type inference (inferred as string)
let duckColor = "Black";

// The following assignment would cause a type error because duckColor is inferred as a string:
// duckColor = 1; // Error: Type 'number' is not assignable to type 'string'.
```

<Callout icon="lightbulb">
  Tip: Use explicit types for public APIs, exported values, and complex structures. For local variables with obvious initial values, type inference keeps code concise while preserving type safety.
</Callout>

## Quick checklist: variables & primitives

* Prefer `const` for values that won't be reassigned.
* Use `let` for mutable bindings.
* Avoid `var` in new code.
* Favor type inference for local, simple values; add explicit types for public interfaces and complex values.
* The TypeScript compiler enforces types at build time, reducing runtime type errors.

That concludes this focused overview of variables and primitives in TypeScript. Continue to the next section to learn about Arrays & Objects and how to model collections of ducks.

<Frame>
  <img alt="A horizontal seven-step timeline for a programming course with numbered circular nodes; step 01 &#x22;Variables & Parameters&#x22; is highlighted. The other nodes read Arrays & Objects, Types & Interfaces, Functions, Classes, Union Types & Enums, and Putting it All Together (© KodeKloud)." />
</Frame>

## Links and references

* [TypeScript Handbook — Basic Types](https://www.typescriptlang.org/docs/handbook/basic-types.html)
* [TypeScript Documentation](https://www.typescriptlang.org/docs/)
* [KodeKloud Labs — Learning Environment](https://kodekloud.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/9424b931-5259-41ea-a9f9-fca84b8bc920" />
</CardGroup>


# TypeScript Development Best Practices

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/TypeScript-Development-Best-Practices/page

Practical project-level best practices for organizing, linting, typing, naming, and testing TypeScript codebases to improve consistency, maintainability, and automation.

This lesson summarizes practical, project-level best practices for organizing and maintaining TypeScript codebases. These are pragmatic recommendations — not hard rules — because TypeScript is used for many contexts (backend APIs, front-end apps, infrastructure-as-code, libraries, etc.). Apply the guidance that fits your project and team.

<Callout icon="lightbulb">
  Best practices depend on your use case. What’s ideal for a NestJS backend may not fit a React SPA or an IaC project. Treat these recommendations as adaptable guidance rather than dogma.
</Callout>

## Organize code across multiple files

Prefer small files with a single responsibility. Clear separation of concerns improves readability, testability, and parallel collaboration.

* Group related types, functions, and classes, but keep files focused (e.g., one service, one module, one logical unit).
* Avoid very large files that mix responsibilities; split them into smaller units.
* Use index (barrel) files sparingly: they can simplify imports but may also hide large dependency graphs and create circular-dependency risks.

<Frame>
  <img alt="A slide titled &#x22;TypeScript Project – Best Practices&#x22; listing recommendations like organizing code across multiple files, encapsulating related logic with classes/interfaces and pure functions, and using linting/formatting tools. It also includes brief bullets explaining separation of concerns, improved collaboration, and tools like ESLint and Prettier." />
</Frame>

Some ecosystems favor classes and dependency injection (e.g., NestJS), while others favor functional composition. Either is fine — consistency and clear conventions matter most.

## Encapsulate related logic

Group behavior and data where it belongs so each unit has a clear contract and responsibilities.

* Classes & interfaces: good for explicit contracts and shared behavior across implementations.
* Pure functions: prefer small, deterministic functions with no side effects where possible — easier to test and reason about.
* Modules: expose a minimal public surface, keep implementation details private to the module.

Example — pure function vs. impure:

```ts theme={null}
// Pure
function add(a: number, b: number): number {
  return a + b;
}

// Impure (mutates external state)
let total = 0;
function addToTotal(x: number) {
  total += x;
}
```

## Linting and formatting

Run automated linting and formatting to maintain code quality and consistent style across the team.

* ESLint: catch likely bugs and enforce code-quality rules (unused vars, unreachable code, consistent use of `const`, etc.).
* Prettier: enforce formatting (line breaks, quotes, spacing). Prefer letting Prettier handle formatting and ESLint handle semantics.
* Integrate `@typescript-eslint/parser` and `@typescript-eslint/eslint-plugin` for TypeScript support.
* Use `eslint-config-prettier` to avoid rule conflicts between ESLint and Prettier.
* Add checks to pre-commit hooks (husky + lint-staged) and to CI pipelines.

Typical tooling setup:

| Tool                | Purpose                       | Example / Notes                                                                      |
| ------------------- | ----------------------------- | ------------------------------------------------------------------------------------ |
| ESLint              | Find bugs & enforce rules     | `eslint --ext .ts src/`                                                              |
| Prettier            | Code formatting               | `prettier --write "src/**/*.{ts,tsx,js,json}"`                                       |
| @typescript-eslint  | TypeScript rules              | installs: `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`            |
| husky + lint-staged | Local hooks for fast feedback | configure `lint-staged` to run `eslint --fix` and `prettier --write` on staged files |

Integrate linting and formatting into CI to ensure consistent quality across pull requests.

## File and identifier naming

Pick a convention early and stick to it. Document it in your repository’s style guide and enforce via linters.

| Resource              | Recommended convention                   | Examples                                               |
| --------------------- | ---------------------------------------- | ------------------------------------------------------ |
| Files                 | `kebab-case` or `camelCase` (choose one) | `user-profile.ts`, `data-service.ts`, `static-site.ts` |
| Types & Classes       | `PascalCase`                             | `UserProfile`, `DataService`                           |
| Variables & Functions | `camelCase`                              | `userName`, `fetchData()`                              |
| Boolean predicates    | Start with `is`, `has`, `should`         | `isValid`, `hasPermission`, `shouldUpdate`             |
| Constants             | `UPPER_SNAKE_CASE` or project default    | `API_TIMEOUT_MS` or `apiTimeoutMs`                     |

Examples in code:

```ts theme={null}
class UserProfile { /* ... */ }
interface DataService { /* ... */ }
const userName = "alice";
function fetchData() { /* ... */ }
```

## Additional practical items

* tsconfig: enable `strict` early and consider `noImplicitAny`, `strictNullChecks`, and `noUncheckedIndexedAccess` to catch issues early.
* Types: prefer explicit types on public APIs; rely on inference for local variables when it improves readability.
* Tests: unit tests for pure logic; integration tests for external interactions (databases, network, etc.).
* Scripts: include helpful npm scripts: `npm run build`, `npm run lint`, `npm test`, `npm run typecheck`.
* CI: run lint, typecheck, and tests in CI for every PR to avoid regressions.
* Dependencies: keep `devDependencies` separate from runtime dependencies; rely on lockfiles and update dependencies deliberately.

<Callout icon="warning">
  Enable TypeScript `strict` mode early in a project to catch subtle bugs. Migrating a large codebase to `strict` later can be time-consuming.
</Callout>

## Example naming summary

```text theme={null}
Files:        user-profile.ts, data-service.ts, static-site.ts
Classes:      UserProfile, DataService
Functions:    fetchData, getUser
Variables:    userName, currentCount
Predicates:   isValid, hasPermission, shouldUpdate
```

## Conclusion

These guidelines provide a practical starting point for structuring TypeScript projects. Focus on clarity, consistency, and automation (linting, formatting, CI). Decide conventions early, document them in a style guide, and enforce them with tools so your team can move fast without sacrificing maintainability.

This lesson covered project-level best practices. Subsequent lessons will show how to apply these patterns in real applications and concrete examples.

## Links and references

* [TypeScript Handbook](https://www.typescriptlang.org/docs/)
* [ESLint](https://eslint.org/)
* [@typescript-eslint](https://github.com/typescript-eslint/typescript-eslint)
* [Prettier](https://prettier.io/)
* [Husky](https://typicode.github.io/husky/#/)
* [lint-staged](https://github.com/okonet/lint-staged)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/d17fce09-5aff-4a79-8317-4c9841fc628d" />
</CardGroup>
