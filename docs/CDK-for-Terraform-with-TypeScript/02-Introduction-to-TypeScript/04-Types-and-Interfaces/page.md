# Types and Interfaces

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/Types-and-Interfaces/page

Overview of TypeScript types and interfaces, defining object shapes, optional properties, differences and examples for declaring and using them

Okay — now let's look at types and interfaces in TypeScript.

Elmer's objects are getting more complex, so we need a way to describe their shape. In TypeScript you can declare a type that specifies the properties an object must have. Below is a `Duck` type with an optional property:

```typescript theme={null}
type Duck = {
  name: string;
  age: number;
  type: string;
  color: string;
  favoriteFood?: string; // Optional property
};

const daffy: Duck = { name: 'Daffy', age: 3, type: 'Mallard', color: 'Black' };
```

When you write `const daffy: Duck = ...`, your editor will provide IntelliSense for the required properties: `name`, `age`, `type`, and `color`. The `favoriteFood` property is optional because of the `?`.

> **lightbulb** The `?` after a property name marks it optional — the object may include it or omit it. This helps model real-world objects that may not always have every property.

If you mistype a property name, TypeScript will report a compile-time error. For example, using the British spelling `colour` will trigger an error:

```typescript theme={null}
type Duck = {
  name: string;
  age: number;
  type: string;
  color: string;
  favoriteFood?: string;
};

const daffy: Duck = { name: 'Daffy', age: 3, type: 'Mallard', colour: 'Black' };
```

TypeScript error (cleaned):

```TypeScript theme={null}
error: Object literal may only specify known properties, but 'colour' does not exist in type 'Duck'. Did you mean to write 'color'?
```

Similarly, adding an unknown property that isn't declared on the type is an error:

```typescript theme={null}
type Duck = {
  name: string;
  age: number;
  type: string;
  color: string;
  favoriteFood?: string;
};

const daffy: Duck = {
  name: 'Daffy',
  age: 3,
  type: 'Mallard',
  color: 'Black',
  foo: 'bar' // Error: 'foo' does not exist on type 'Duck'
};
```

You can still add optional properties later by mutating the object referenced by a `const`. Mutating properties is allowed; reassigning the `const` variable itself is not.

```typescript theme={null}
type Duck = {
  name: string;
  age: number;
  type: string;
  color: string;
  favoriteFood?: string;
};

const daffy: Duck = { name: 'Daffy', age: 3, type: 'Mallard', color: 'Black' };

// Allowed: mutating a property on the object referenced by a const
daffy.favoriteFood = 'Pizza';

// Not allowed: reassigning the const variable
// daffy = null; // Error: Cannot assign to 'daffy' because it is a constant.
```

> **warning** You can mutate properties on an object declared with `const`, but you cannot reassign the `const` variable itself. This distinction prevents reassignment while allowing object mutation.

Another common way to describe object shapes in TypeScript is an `interface`. For many basic use cases, `type` aliases and `interface` declarations are interchangeable. Here is the same shape expressed both ways:

```typescript theme={null}
type DuckType = {
  name: string;
  age: number;
  type: string;
  color: string;
  favoriteFood?: string;
};

interface DuckInterface {
  name: string;
  age: number;
  type: string;
  color: string;
  favoriteFood?: string;
}
```

Both `DuckType` and `DuckInterface` describe the same required and optional properties. There are advanced differences (for example, declaration merging and some utility-type behaviors) — those are out of scope for this overview.

## Quick comparison

| Feature               | `type` alias                               | `interface`                                                        |
| --------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| Basic object shape    | `type DuckType = { ... }`                  | `interface DuckInterface { ... }`                                  |
| Extending / composing | `type A = B & C`                           | `interface A extends B, C {}`                                      |
| Declaration merging   | No                                         | Yes (interfaces can merge declarations)                            |
| Use cases             | Use for unions, tuples, mapped types, etc. | Preferred for public API shapes that may need merging or extension |

## Links and references

* [TypeScript Handbook — Interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html)
* [TypeScript Handbook — Advanced Types](https://www.typescriptlang.org/docs/handbook/advanced-types.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/c3255625-0eea-458e-853c-5b423596b037)
