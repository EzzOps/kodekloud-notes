# Terraform code
resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-bucket-name"

  versioning {
    enabled = "invalid value" # No error until terraform apply/validate
  }
}
```

TypeScript (CDKTF) equivalent — the compiler detects the wrong type earlier:

```typescript theme={null}
// TypeScript (CDKTF) code
new s3Bucket.S3Bucket(this, 'my_bucket', {
  bucket: 'my-unique-bucket-name',
  versioning: {
    enabled: 'invalid value',
    // Compile error: Type 'string' is not assignable to type 'boolean | IResolvable | undefined'.
  },
});
```

Using TypeScript lets you validate infrastructure changes against types before execution, catching errors earlier and improving the development workflow.

## Setting up a TypeScript project from scratch

You can follow along locally or in an online lab environment (e.g., KodeKloud Labs). The steps below explain what to install and why.

### Prerequisite: Node.js

TypeScript runs on the JavaScript toolchain. Node.js is the runtime that lets you run JavaScript/TypeScript on your machine (outside the browser). KodeKloud Labs include Node; for local installs, choose the method appropriate for your OS.

> **warning** Homebrew is not a Node.js package manager. Ensure Homebrew is installed by following the official instructions at `https://brew.sh/`. Homebrew can install Node.js, but for Node package dependency management you should use npm, Yarn, pnpm, or Bun.

Example (macOS using Homebrew):

```bash theme={null}
# Install Node.js (example installs Node 20)
brew install node@20

# Verify Node and npm
node -v   # e.g., should print `v20.16.0`
npm -v    # e.g., should print `10.8.1`
```

Create your project directory:

```bash theme={null}
mkdir typescript-fundamentals
cd typescript-fundamentals
```

### Package manager choices

A package manager installs, updates, configures, and manages dependencies for your project. Common choices include npm, Yarn, pnpm, and Bun.

<Frame>
  <img alt="A presentation slide titled &#x22;Why do we need Package Manager?&#x22; with colorful rounded buttons labeled &#x22;Install,&#x22; &#x22;Update,&#x22; &#x22;Configure,&#x22; and &#x22;Manage.&#x22; Two gray buttons below read &#x22;Share&#x22; and &#x22;Reuse,&#x22; and a small gears icon sits above the main group." />
</Frame>

<Frame>
  <img alt="A slide titled &#x22;Package Manager&#x22; displaying four package manager logos in a row. From left to right: npm, Yarn, a cute dumpling/bao mascot, and the pnpm grid logo." />
</Frame>

Table — Popular package managers (short comparison):

| Package Manager | Pros                                               | Example install                |
| --------------- | -------------------------------------------------- | ------------------------------ |
| npm             | Default with Node; broadly supported               | `npm init -y`                  |
| Yarn            | Fast installs, caching, flexible configuration     | `corepack enable && yarn init` |
| pnpm            | Disk space efficient (stores single copy)          | `corepack enable && pnpm init` |
| Bun             | Very fast runtime & package manager (experimental) | `bun init`                     |

For this lesson we'll use Yarn because it's stable, fast, and caches packages locally. Other managers work similarly — choose the one you prefer.

Initialize a Yarn project:

```bash theme={null}
# Enable Corepack (manages Yarn/pnpm)
corepack enable

# Initialize the project interactively (creates package.json)
yarn init

# Configure Yarn to use the classic node_modules layout
yarn config set nodeLinker node-modules

# Install any initial dependencies (creates node_modules)
yarn install

# Verify yarn version
yarn -v  # e.g., 4.3.1
```

A minimal `package.json` created by `yarn init` might look like:

```json theme={null}
{
  "name": "typescript-fundamentals",
  "packageManager": "yarn@4.3.1"
}
```

Add TypeScript as a development dependency:

```bash theme={null}
yarn add -D typescript
```

After installing, `package.json` will include TypeScript in `devDependencies`:

```json theme={null}
{
  "name": "typescript-fundamentals",
  "packageManager": "yarn@4.3.1",
  "devDependencies": {
    "typescript": "^5.6.3"
  }
}
```

TypeScript is a dev dependency because it compiles code during development; the compiled JavaScript runs in production.

Optional: inspect installed TypeScript version:

```bash theme={null}
yarn info typescript version
# shows the installed version, e.g., 5.6.3
```

If you use Git, add `node_modules/` to `.gitignore`. `yarn init` typically creates a `.gitignore` with common entries.

## Hello World in TypeScript

Create `index.ts` as the application entry point:

```typescript theme={null}
// index.ts
const helloWorld: string = "Hello World";
console.log(helloWorld);
```

### Run TypeScript directly (no compile step)

To run TypeScript files directly, use `ts-node`. For automatic restarts during development use `ts-node-dev`.

```bash theme={null}
# For one-off execution
yarn add -D ts-node

# For development with auto-restart on file change
yarn add -D ts-node-dev
```

> **lightbulb** `ts-node` runs TypeScript files directly without a separate compile step. `ts-node-dev` adds file watching and automatic restarts (useful for iterative development). For production you typically compile `.ts` to `.js` using `tsc`.

Add a convenient run script to `package.json` for development:

```json theme={null}
{
  "name": "typescript-fundamentals",
  "packageManager": "yarn@4.4.0",
  "scripts": {
    "dev": "ts-node-dev --respawn index.ts"
  },
  "devDependencies": {
    "ts-node": "^10.9.2",
    "ts-node-dev": "^2.0.0",
    "typescript": "^5.6.3"
  }
}
```

Note: `--respawn` instructs `ts-node-dev` to restart the process whenever a watched file changes.

### TypeScript compiler configuration

Create `tsconfig.json` to control compilation behavior. A sensible starter configuration:

```json theme={null}
{
  "compilerOptions": {
    "target": "ES2018",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist"
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules"]
}
```

Now run the app:

```bash theme={null}
yarn dev
```

You should see:

```text theme={null}
Hello World
```

If you use `ts-node-dev`, editing `index.ts` and saving will automatically restart the process and print the updated output.

## Recap

* TypeScript is a typed superset of JavaScript that improves reliability by catching many errors at compile time.
* Static typing is especially helpful when authoring infrastructure-as-code (IaC) — it surfaces type mismatches before you run provisioning commands.
* We covered prerequisites (Node.js), package manager options, initializing a Yarn project, installing TypeScript and development tooling, adding a `tsconfig.json`, and running a Hello World using `ts-node-dev`.

<Frame>
  <img alt="A slide titled &#x22;Recap&#x22; showing three connected boxes: the Node.js logo on the left, the Yarn logo in the middle, and the TypeScript (TS) logo on the right." />
</Frame>

Next, we'll build on this foundation and demonstrate how TypeScript-based IaC tooling (such as CDK for Terraform) can initialize project scaffolding and validate types while you design infrastructure.

## Links and References

* Node.js official: [https://nodejs.org/](https://nodejs.org/)
* Yarn: [https://yarnpkg.com/](https://yarnpkg.com/)
* TypeScript docs: [https://www.typescriptlang.org/docs/](https://www.typescriptlang.org/docs/)
* CDK for Terraform (CDKTF): [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* KodeKloud Labs: [https://learn.kodekloud.com/](https://learn.kodekloud.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/74685d7e-5598-4b66-a660-eb38f3813172)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/2d62a4e6-ce48-4573-ad21-98a70c845c40)


# Union Types and Enums

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/Union-Types-and-Enums/page

Explains TypeScript union literal types and enums, comparing use cases and trade offs to improve type safety and prevent invalid values with duck examples.

In this lesson we'll explore how union literal types and enums in TypeScript improve type safety and when you should prefer one over the other. These features help prevent invalid values at compile time and make your domain models clearer to consumers of your types.

## The problem: using plain `string` allows invalid values

If a property is typed as `string`, any string is allowed — including nonsensical values such as `"Banana"`. This can lead to bugs only caught at runtime.

```typescript theme={null}
class PondDuck {
  name: string;
  age: number;
  type: string;
  color: string; // problem: any string allowed
  isFlying: boolean;

  constructor(name: string, age: number, type: string, color: string) {
    this.name = name;
    this.age = age;
    this.type = type;
    this.color = color;
    this.isFlying = false;
  }

  fly(): void {
    if (!this.isFlying) {
      this.isFlying = true;
      console.log(`${this.name} starts flying!`);
    } else {
      console.log(`${this.name} is already flying!`);
    }
  }

  land(): void {
    if (this.isFlying) {
      this.isFlying = false;
      console.log(`${this.name} lands gracefully`);
    } else {
      console.log(`${this.name} is already on the ground!`);
    }
  }
}

const daffy = new PondDuck('Daffy', 3, 'Mallard', 'Banana'); // allowed when color is `string`
daffy.fly();
```

## Union literal types: restrict a value to a fixed set of literals

A union of literal types restricts a variable to one of several specified literal values. This keeps invalid values out at compile time while remaining lightweight (no runtime object is created).

```typescript theme={null}
type DuckColor = 'White' | 'Brown' | 'Black' | 'Mixed';

// This will be a compile-time error:
// const myColor: DuckColor = 'Banana'; // Error: Type '"Banana"' is not assignable to type 'DuckColor'.

// You can add other allowed literals:
const myColor: DuckColor = 'Black';
```

Notes about literal unions:

* Each union member is a literal type (for example the type `"White"`, not `string`).
* Literal unions can combine primitives and more complex literal values:

```typescript theme={null}
type WeirdColor = 'White' | 3 | { shade: 'dark'; color: 'Green' };

const a: WeirdColor = 'White';
const b: WeirdColor = 3;
const c: WeirdColor = { shade: 'dark', color: 'Green' };
```

## When to use an enum

Enums group related named constants. They are useful when you want a named collection that you can reference across your codebase and benefit from editor completions. Enums also produce a runtime object (which can be numeric or string-valued).

Numeric enum example:

```typescript theme={null}
enum NumericDuckType {
  Mallard,  // 0
  Muscovy,  // 1
  Pekin     // 2
}

console.log(NumericDuckType.Mallard); // 0
```

String enum example:

```typescript theme={null}
enum DuckType {
  Mallard = 'Mallard',
  Muscovy = 'Muscovy',
  Pekin = 'Pekin',
}

console.log(DuckType.Mallard); // 'Mallard'
```

> **lightbulb** Use union literal types when you want a compact set of allowed literals (strings/numbers) without an extra runtime object. Use enums when you want a named collection you can reference (with code completion) and potentially map to numeric or string values at runtime.

## Putting it together: a typed Duck class

Replace unconstrained `string` types with `DuckColor` (a union of literals) and `DuckType` (an enum). The compiler now prevents invalid values and provides better tooling support.

```typescript theme={null}
type DuckColor = 'White' | 'Brown' | 'Black' | 'Mixed';

enum DuckType {
  Mallard = 'Mallard',
  Muscovy = 'Muscovy',
  Pekin = 'Pekin',
}

class PondDuck {
  name: string;
  age: number;
  type: DuckType;
  color: DuckColor;
  isFlying: boolean;
  favoriteFood?: string;

  constructor(
    name: string,
    age: number,
    type: DuckType,
    color: DuckColor,
    favoriteFood?: string
  ) {
    this.name = name;
    this.age = age;
    this.type = type;
    this.color = color;
    this.isFlying = false;
    this.favoriteFood = favoriteFood;
  }

  quack(times = 1): void {
    for (let i = 0; i < times; i++) {
      console.log(`${this.name} the ${this.color} ${this.type} duck says: Quack!`);
    }
  }

  fly(): void {
    if (!this.isFlying) {
      this.isFlying = true;
      console.log(`${this.name} starts flying!`);
    } else {
      console.log(`${this.name} is already flying!`);
    }
  }

  land(): void {
    if (this.isFlying) {
      this.isFlying = false;
      console.log(`${this.name} lands gracefully!`);
    } else {
      console.log(`${this.name} is already on the ground!`);
    }
  }
}

// Correct usage:
const daffy = new PondDuck('Daffy', 3, DuckType.Mallard, 'Black', 'Corn');
const donald = new PondDuck('Donald', 5, DuckType.Pekin, 'White');

daffy.fly();
daffy.fly();
daffy.land();
daffy.land();
donald.fly();

// Invalid usage (will be a TypeScript compile error):
// const bad = new PondDuck('Elmer', 2, DuckType.Mallard, 'Banana');
// Error: Type '"Banana"' is not assignable to parameter of type 'DuckColor'.
```

Sample runtime output (when valid values are used):

```text theme={null}
Daffy starts flying!
Daffy is already flying!
Daffy lands gracefully!
Daffy is already on the ground!
Donald starts flying!
```

## Quick comparison: union literal types vs enums

| Feature           | Union literal types                                      | Enums                                                   |                                         |
| ----------------- | -------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------- |
| Runtime footprint | None (compile-time only)                                 | Creates a runtime object                                |                                         |
| Best for          | Small sets of primitives (strings/numbers)               | Named collections, mapping to runtime values            |                                         |
| Tooling           | Type safety, autocomplete on variables typed with unions | Strong autocomplete for enum members and runtime access |                                         |
| Example           | \`type DuckColor = 'White'                               | 'Brown'\`                                               | `enum DuckType { Mallard = 'Mallard' }` |

## Summary

* Use union literal types to restrict values to a compact set of allowed literals at the type level.
* Use enums when you want a named runtime object (numeric or string) and stable identifiers across your code.
* Applying these TypeScript features makes your APIs and domain models safer, more self-documenting, and easier to use.

## Links and references

* [TypeScript Handbook: Union Types](https://www.typescriptlang.org/docs/handbook/unions-and-intersections.html)
* [TypeScript Handbook: Enums](https://www.typescriptlang.org/docs/handbook/enums.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/2c9dcf6b-2550-4677-90c2-062589ed9929)
