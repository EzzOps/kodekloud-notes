# Functions

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/Functions/page

Explains TypeScript function parameters including optional and default parameters, nullish coalescing versus logical OR, and arrow function equivalents using a duck quack example.

In this lesson we'll explore TypeScript functions by helping Elmo make his ducks quack. You'll learn how to declare parameters (optional vs default), when to use nullish coalescing (`??`), and how to express the same behavior with arrow functions.

Keywords: TypeScript functions, optional parameters, default parameters, nullish coalescing, arrow functions

First, define a simple `Duck` type and a `daffy` instance:

```typescript theme={null}
type Duck = {
  name: string;
  age: number;
  type: string;
  color: string;
  favoriteFood?: string;
};

const daffy: Duck = { name: 'Daffy', age: 3, type: 'Mallard', color: 'Black' };
```

## Basic function with an optional parameter

Here is a function that accepts a `duck` and an optional `times` argument. If `times` is not provided, the function defaults to 1 quack using nullish coalescing (`??`), which only treats `null` or `undefined` as "no value".

```typescript theme={null}
function makeDuckQuack(duck: Duck, times?: number): void {
  // Use nullish coalescing to default only when `times` is null or undefined.
  const quackCount = times ?? 1;
  for (let i = 0; i < quackCount; i++) {
    console.log(`${duck.name} says: Quack!`);
  }
}

makeDuckQuack(daffy, 2);
```

Console output:

```text theme={null}
Daffy says: Quack!
Daffy says: Quack!
```

> **lightbulb** Prefer `times ?? 1` over `times || 1` when you want to treat only `null` or `undefined` as "no value" and still allow `0`.

> **warning** Avoid using `times || 1` if `0` is a meaningful value for `times` — `||` treats `0` as falsy and will wrongly fall back to `1`.

## Using a default parameter

You can also declare a default value directly in the parameter list. TypeScript infers the parameter type from the default, so an explicit `: number` is not required.

```typescript theme={null}
function makeDuckQuack(duck: Duck, times = 1): void {
  for (let i = 0; i < times; i++) {
    console.log(`${duck.name} says: Quack!`);
  }
}

makeDuckQuack(daffy); // uses the default
```

Console output:

```text theme={null}
Daffy says: Quack!
```

Notes:

* With a default parameter (`times = 1`), callers may omit `times` and it will default to `1`.
* If you explicitly want `times` to possibly be `undefined` inside the function, use an optional parameter (`times?: number`) instead of a default.

## Arrow function equivalent

You can write the same function as an arrow function. For most use cases arrow functions behave the same as regular function expressions, but be aware of differences in `this` binding and hoisting.

```typescript theme={null}
const makeDuckQuack = (duck: Duck, times = 1): void => {
  for (let i = 0; i < times; i++) {
    console.log(`${duck.name} says: Quack!`);
  }
};

makeDuckQuack(daffy, 2);
```

## Quick comparison

| Feature             | Syntax example   | Behavior                                                                                        |     |                                                                                     |
| ------------------- | ---------------- | ----------------------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------------------------- |
| Optional parameter  | `times?: number` | Parameter may be `undefined`; you can handle fallback inside the function (e.g., `times ?? 1`). |     |                                                                                     |
| Default parameter   | `times = 1`      | Parameter defaults to `1` if omitted by the caller—inside the function it's never `undefined`.  |     |                                                                                     |
| Nullish coalescing  | `times ?? 1`     | Fallback only when `times` is `null` or `undefined` (keeps `0` intact).                         |     |                                                                                     |
| Logical OR fallback | \`times          |                                                                                                 | 1\` | Fallback when `times` is any falsy value (`0`, `''`, `null`, `undefined`, `false`). |

## Summary

* Optional parameters are declared with `?` (e.g., `times?: number`) and may be `undefined`.
* Default parameters are declared with `=` (e.g., `times = 1`) and supply an automatic fallback.
* Prefer `??` over `||` for fallbacks when `0` is a meaningful value.
* Arrow functions provide a concise alternative; they differ from regular functions in `this` behavior and hoisting.

Further reading:

* TypeScript function documentation: [https://www.typescriptlang.org/docs/handbook/functions.html](https://www.typescriptlang.org/docs/handbook/functions.html)
* MDN: Nullish coalescing operator (`??`): [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish\_coalescing\_operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_operator)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/3102a69a-afd3-46c1-b297-07c2a8cd4c62)
