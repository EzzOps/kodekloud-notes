# Importing in TypeScript

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/Importing-in-TypeScript/page

Guide to importing and exporting in TypeScript, module structuring, ESM import syntaxes, export strategies, and project best practices for readable reusable code

This lesson covers importing and exporting in TypeScript, configuring imports for modern build targets, and best practices for organizing a TypeScript project for readability and reuse. Learn how to structure modules, select the right export strategy, and use common import syntaxes that work with ECMAScript modules (ESM).

<Frame>
  <img alt="A horizontal three-step timeline slide about TypeScript showing step 01 (Importing in TypeScript) highlighted in teal, step 02 (Configuring TypeScript) in gray, and step 03 (TypeScript Project — Best Practices)." />
</Frame>

Why import?

* Importing breaks a large codebase into smaller, focused modules so code is easier to read, test, and maintain.
* It enables code reuse across files and packages and helps prevent name collisions when combined with aliasing or namespaces.

Common ESM import syntaxes in TypeScript

|                  Syntax | Example                                        | What it does                                                           |
| ----------------------: | ---------------------------------------------- | ---------------------------------------------------------------------- |
|            Named import | `import { exportedMember } from './fileName';` | Imports specific exported symbols by name.                             |
|          Default import | `import defaultExport from './fileName';`      | Imports the module's `default` export. Only one default per module.    |
| Namespace import (star) | `import * as utils from './utils';`            | Imports all exports and exposes them as properties of `utils`.         |
|          Aliased import | `import { add as sum } from './fileName';`     | Renames an imported symbol locally to avoid collisions.                |
|     Third‑party package | `import _ from 'lodash';`                      | Imports from npm packages (may require `esModuleInterop` in tsconfig). |

> **lightbulb** Your editor (for example [VS Code](https://code.visualstudio.com/)) will usually auto-complete and insert import statements for you. Rely on that to avoid manual errors.

Project example: module files (under ./import-examples)

* mathUtils.ts — named exports

```typescript theme={null}
// import-examples/mathUtils.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}
```

* utils.ts — named exports

```typescript theme={null}
// import-examples/utils.ts
export function multiply(a: number, b: number): number {
  return a * b;
}

export function divide(a: number, b: number): number {
  if (b === 0) throw new Error('Division by zero');
  return a / b;
}
```

* calculator.ts — default export

```typescript theme={null}
// import-examples/calculator.ts
export default function calculateTotal(prices: number[]): number {
  return prices.reduce((total, price) => total + price, 0);
}
```

Entry point (index.ts) — examples of different import styles and usage:

```typescript theme={null}
// index.ts
import { add } from './import-examples/mathUtils';
import { add as sum } from './import-examples/mathUtils';
import { divide, multiply } from './import-examples/utils';
import calculateTotal from './import-examples/calculator';
import * as utils from './import-examples/utils';
import _ from 'lodash'; // example third-party import (requires installation and may need tsconfig "esModuleInterop": true)

// Named import
console.log('add(1, 2) =', add(1, 2)); // 3

// Aliasing a named import
console.log('sum(2, 3) =', sum(2, 3)); // 5

// Named imports from the same module
console.log('multiply(2, 4) =', multiply(2, 4)); // 8
console.log('divide(8, 2) =', divide(8, 2));     // 4

// Namespace (star) import: access via the namespace object
console.log('utils.multiply(3, 3) =', utils.multiply(3, 3)); // 9

// Default import
console.log('calculateTotal([1,2,3]) =', calculateTotal([1, 2, 3])); // 6

// Third-party example (lodash)
console.log('_.add(5, 7) =', _.add(5, 7)); // 12
```

Quick notes and best practices

* Aliasing: `import { add as sum } from './import-examples/mathUtils';` helps avoid naming collisions when multiple modules export the same symbol name.
* Namespace imports: `import * as utils from './import-examples/utils';` are useful when you want a single object to group all exports (good for utility libraries).
* Default exports: Use `export default` when the module exports one primary value; use named exports when a module exports multiple utilities.
* Prefer named exports for libraries you expect to tree-shake and for clearer IDE auto-completion.
* Keep module responsibilities small — one concept or small set of related utilities per file.

When your framework expects an exported entry point
If your runtime or framework requires an exported function from the entry file (for example `index.ts` or `main.ts`), you can provide either a default export or named exports depending on the framework's convention.

Examples:

```typescript theme={null}
// Default export (single default export per module)
export default function main() {
  console.log('Main running');
}

// Named export
export const namedMain = () => {
  console.log('Named main running');
};
```

ESM vs CommonJS

* ECMAScript modules (ESM) — `import` / `export` — are the recommended approach for modern TypeScript projects and for native support in bundlers and Node (with proper configuration).
* CommonJS — `require()` / `module.exports` — is legacy and still used in some Node ecosystems. If interoperating with CommonJS packages, you may need `esModuleInterop` or `allowSyntheticDefaultImports` in your `tsconfig.json`.

Comparison table — default vs named exports

| Export style   | Use when                                                                     | Example                                           |
| -------------- | ---------------------------------------------------------------------------- | ------------------------------------------------- |
| Default export | Module has a single primary export (e.g., a class or main function)          | `export default function main() {}`               |
| Named exports  | Module provides multiple utilities; better tree-shaking and explicit imports | `export function a() {}; export function b() {};` |

Links and references

* TypeScript: [https://www.typescriptlang.org/docs/](https://www.typescriptlang.org/docs/)
* ECMAScript Modules (MDN): [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
* VS Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)
* Lodash (npm): [https://www.npmjs.com/package/lodash](https://www.npmjs.com/package/lodash)

This concludes the section on importing and exporting in TypeScript.

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/0541543a-8dbb-4a95-a12e-5f0e4c9333f0)
