# Arrays and Objects

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/Arrays-and-Objects/page

Guide to arrays and objects in TypeScript, showing how to type lists and objects, combine them into arrays of typed items, and handle mutability and readonly usage

Okay — let's look at arrays and objects in TypeScript.

Elmer has multiple ducks and needs a way to store them together. This guide shows how to model lists with arrays and how to represent richer item data with objects and type annotations in TypeScript. You’ll learn basic syntax, how to combine arrays and objects, and best practices for reading and mutating these structures.

## Quick overview

* Arrays: ordered collections of values (e.g., a list of duck names).
* Objects: group related values into a single item (e.g., name, age, type, color).
* Combining both: arrays of objects let you model collections of richly-described items (e.g., a flock of ducks).

## Arrays

Declare an array of strings in TypeScript using either bracket syntax or the generic `Array<T>` form. Both are equivalent; pick the style your team prefers.

```typescript theme={null}
const ducks: string[] = ['Daffy', 'Howard', 'Donald'];
```

or

```typescript theme={null}
const ducksAlt: Array<string> = ['Daffy', 'Howard', 'Donald'];
```

Both examples enforce that every element in the array is a `string`.

Table — common array syntaxes

| Purpose            | Syntax                               | Example                                          |
| ------------------ | ------------------------------------ | ------------------------------------------------ |
| Simple typed array | `T[]`                                | `const names: string[] = ['Daffy']`              |
| Generic array type | `Array<T>`                           | `const namesAlt: Array<string> = ['Daffy']`      |
| Readonly array     | `readonly T[]` or `ReadonlyArray<T>` | `const namesRead: readonly string[] = ['Daffy']` |

Useful array operations (examples)

```typescript theme={null}
ducks.push('Plucky');        // add
const first = ducks[0];      // access by index
const allUpper = ducks.map(d => d.toUpperCase()); // transform
```

## Objects

When you need to store multiple properties about a single duck (for example: `name`, `age`, `type`, and `color`), use an object.

Object literal (untyped):

```typescript theme={null}
const duck = { name: 'Daffy', age: 3, type: 'Mallard', color: 'Black' };
```

Typed object using an `interface` for stronger guarantees:

```typescript theme={null}
interface Duck {
  name: string;
  age: number;
  type: string;
  color: string;
}

const duckTyped: Duck = { name: 'Daffy', age: 3, type: 'Mallard', color: 'Black' };
```

You can also use a `type` alias if you prefer:

```typescript theme={null}
type DuckType = {
  name: string;
  age: number;
  type: string;
  color: string;
};
```

### Accessing properties

Use dot notation for the common case:

```typescript theme={null}
console.log(duck.name); // Daffy
```

Console output:

```text theme={null}
Daffy
```

Bracket notation is useful when the property name is dynamic:

```typescript theme={null}
const prop = 'age';
console.log(duck[prop]); // 3
```

In the object `{ name: 'Daffy', age: 3, type: 'Mallard', color: 'Black' }`:

* Keys (properties): `name`, `age`, `type`, `color`
* Values: `'Daffy'`, `3`, `'Mallard'`, `'Black'`

## Putting arrays and objects together

Most real-world data models use arrays of objects. For example, a typed collection of `Duck` objects:

```typescript theme={null}
const flock: Duck[] = [
  { name: 'Daffy', age: 3, type: 'Mallard', color: 'Black' },
  { name: 'Howard', age: 2, type: 'Pekin', color: 'White' }
];
```

Access items and their properties:

```typescript theme={null}
console.log(flock[0].name); // Daffy
console.log(flock[1].age);  // 2
```

Common operations on an array of objects:

* Find an item: `flock.find(d => d.name === 'Howard')`
* Filter: `flock.filter(d => d.age > 2)`
* Map to a new shape: `flock.map(d => d.name)`

## Note about const and mutation

> **lightbulb** Declaring a variable with `const` prevents reassignment of the identifier but does not make the object or array immutable. You can still modify properties or change the array contents:

  ```typescript theme={null}
  duck.age = 4;
  flock.push({ name: 'Donald', age: 5, type: 'Mallard', color: 'White' });
  ```

  If you need immutability at the type level, prefer `readonly` properties and `readonly` arrays (e.g., `readonly Duck[]` or `ReadonlyArray<Duck>`).

## Summary

* Use `T[]` or `Array<T>` to type arrays.
* Use object literals for single items and `interface` or `type` to enforce a shape for objects.
* Combine arrays and objects to model lists of rich items (e.g., `Duck[]`).
* `const` protects the binding, not the contents — use `readonly` for immutability when appropriate.

## Links and references

* [TypeScript Handbook — Basic Types](https://www.typescriptlang.org/docs/handbook/basic-types.html)
* [TypeScript Handbook — Interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html)
* [MDN — JavaScript Arrays](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/3e6ec986-1e4d-48a5-b0c5-c63e3f9631b7)
