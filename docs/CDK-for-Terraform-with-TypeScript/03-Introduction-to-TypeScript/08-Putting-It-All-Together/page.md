# Putting It All Together

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/Putting-It-All-Together/page

Demonstrates TypeScript fundamentals using a duck pond example, covering enums, union types, interfaces, classes, pure versus impure functions, and coding best practices.

In this lesson we combine several TypeScript fundamentals—enums, union types, interfaces, classes with `implements`, optional parameters, and array usage—into a small "duck pond" management example. Along the way we highlight code-quality ideas such as preferring pure functions and using explicit typing when it improves clarity.

Below is the cleaned and complete TypeScript implementation used for this lesson. It demonstrates the concepts above and includes both pure and impure function examples.

```typescript theme={null}
// Enum for Duck Types
enum DuckType {
  Mallard = 'Mallard',
  Muscovy = 'Muscovy',
  Pekin = 'Pekin',
}

// Type for Duck Colors using a union type
type DuckColor = 'White' | 'Brown' | 'Black' | 'Mixed';

// Interface describing the shape of a Duck
interface IDuck {
  name: string;
  age: number;
  type: DuckType;
  color: DuckColor;
  favoriteToy?: string;
}

// Class implementing the IDuck interface
class PondDuck implements IDuck {
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
    this.isFlying = false; // Ducks start on the ground
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
      console.log(`${this.name} lands gracefully.`);
    } else {
      console.log(`${this.name} is already on the ground!`);
    }
  }
}

// Developer type and an example developer
type Developer = {
  name: string;
  favoriteDuckType: DuckType;
  skills: string[];
};

const elmer: Developer = {
  name: 'Elmer Code',
  favoriteDuckType: DuckType.Mallard,
  skills: ['TypeScript', 'Debugging', 'Problem Solving', 'Hunting Ducks!'],
};

console.log(`Developer ${elmer.name} is obsessed with ${elmer.favoriteDuckType} ducks!`);

// Create some PondDuck instances
const daffy = new PondDuck('Daffy', 3, DuckType.Mallard, 'Black');
const donald = new PondDuck('Donald', 5, DuckType.Pekin, 'White', 'Corn');
const howard = new PondDuck('Howard', 2, DuckType.Muscovy, 'Brown');

// Explicitly typed duck pond (prevents pushing non-Duck values)
const duckPond: PondDuck[] = [];
duckPond.push(daffy, donald, howard);

// Pure function: receives everything it needs (does not access external state)
function makeAllDucksQuack(ducks: PondDuck[], times = 1): void {
  ducks.forEach((duck) => duck.quack(times));
}

// Impure function example (reads from outer scope). This is less reusable/testable.
function findDuckAndFly_impure(name: string): void {
  const found = duckPond.find((d) => d.name === name);
  if (found) {
    found.fly();
  } else {
    console.warn(`No duck named ${name} found in the pond.`);
  }
}

// Preferred pure version: pass the pond in as an argument
function findDuckAndFly(name: string, pond: PondDuck[]): void {
  const found = pond.find((d) => d.name === name);
  if (found) {
    found.fly();
  } else {
    console.warn(`No duck named ${name} found in the pond.`);
  }
}

// Utility: count ducks by type
function countDucksByType(type: DuckType, pond: PondDuck[]): number {
  return pond.filter((duck) => duck.type === type).length;
}

// Usage examples
makeAllDucksQuack(duckPond, 2);           // All ducks quack twice
findDuckAndFly('Donald', duckPond);       // Donald starts flying!
const mallardCount = countDucksByType(DuckType.Mallard, duckPond);
console.log(`There are ${mallardCount} Mallard ducks in the pond.`);
console.log('Ducks in the pond:', duckPond.map((d) => d.name).join(', '));

// Export for use elsewhere
export { PondDuck, DuckType };
```

Discussion and key points

* Explicit typing vs inference
  * Declaring `const duckPond: PondDuck[] = []` makes it explicit that only `PondDuck` instances can be added to that array. This is useful when the container starts empty or receives external data.
  * If you instead define an array from existing elements (for example, `const duckPondInferred = [daffy, donald, howard];`), TypeScript will infer the element type from those items. Attempts to push a different type (e.g. a string) will produce a compile-time error.
  * Prefer inference when it reduces boilerplate, but favor explicit types at boundaries (empty containers, external inputs).

* Pure functions vs impure functions
  * `makeAllDucksQuack(ducks, times)` follows a pure-style approach because it receives all required inputs as parameters.
  * `findDuckAndFly_impure(name)` reads `duckPond` from the outer scope; it depends on external state and is therefore impure. The pure variant `findDuckAndFly(name, pond)` is easier to test and reuse.

* Interfaces and `implements`
  * The `implements IDuck` on `PondDuck` enforces that the class matches the interface shape (at least the specified properties), helping catch structure mismatches at compile time.

* Optional parameters and defaults
  * Both `quack(times = 1)` and `makeAllDucksQuack(ducks, times = 1)` demonstrate default parameter values.
  * Optional properties on types and interfaces use the `?` suffix (for example, `favoriteToy?: string`).

* Small utility functions
  * Utilities like `countDucksByType` help keep logic isolated, readable, and simple to test.

Function summary

| Function / Utility     | Signature                                                    | Purpose                                                                       |
| ---------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| makeAllDucksQuack      | `makeAllDucksQuack(ducks: PondDuck[], times = 1): void`      | Pure-style: ask each duck in the provided array to quack N times              |
| findDuckAndFly\_impure | `findDuckAndFly_impure(name: string): void`                  | Impure: looks up a duck in the module-level `duckPond` and commands it to fly |
| findDuckAndFly         | `findDuckAndFly(name: string, pond: PondDuck[]): void`       | Pure-style: same as above but accepts the pond as an argument                 |
| countDucksByType       | `countDucksByType(type: DuckType, pond: PondDuck[]): number` | Returns the number of ducks of a given `DuckType` in the provided pond        |

> **lightbulb** Prefer pure functions when possible — functions that accept all inputs and avoid accessing or mutating external state are easier to reason about, test, and reuse.

<Frame>
  <img alt="A presentation slide titled &#x22;Syntax – Key Takeaways&#x22; that summarizes TypeScript/JavaScript concepts like variables, primitive and complex types, variable declarations (let/const), arrays/objects, type inference, classes, and enums/union types. It lists brief definitions and examples for each bullet point." />
</Frame>

Summary

* We modeled structured data using enums and union types, and enforced shape with interfaces.
* We implemented a class (`PondDuck`) with methods and optional properties, then managed instances in an explicitly typed array.
* We contrasted pure and impure designs and showed simple utility functions for common pond operations.
* Use TypeScript inference to reduce boilerplate, but declare explicit types at public or empty boundaries for safety.
* Favor small, pure utilities for clarity, reusability, and easier testing.

<Frame>
  <img alt="A presentation slide titled &#x22;Syntax – Advanced TypeScript Concepts&#x22; that lists next-step topics (Generics, Utility Types, Core JavaScript, Async/Await, Decorators) with short descriptions. The slide appears to be from KodeKloud and recommends these topics to deepen TypeScript skills." />
</Frame>

Next steps (recommended)

* Generics and reusable data structures
* Utility types (`Partial`, `Pick`, `Record`, etc.)
* Deeper core JavaScript concepts (closures, prototype, event loop)
* Async/await patterns and Promise handling
* Decorators and advanced class patterns

Links and references

* [TypeScript Handbook — Basic Types](https://www.typescriptlang.org/docs/handbook/basic-types.html)
* [TypeScript Handbook — Classes](https://www.typescriptlang.org/docs/handbook/classes.html)
* [MDN Web Docs — JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/f044a3ce-0352-4334-9148-34666a0f0c61)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/5e113100-9832-4049-806e-14d4d8720547)
