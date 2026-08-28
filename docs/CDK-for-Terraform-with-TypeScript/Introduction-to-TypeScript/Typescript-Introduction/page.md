# Typescript Introduction

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/Typescript-Introduction/page

Introduction to using TypeScript for infrastructure as code, covering setup, tooling, typing benefits, project initialization, and running a Hello World with ts-node and Yarn

Throughout this course we'll use TypeScript to define infrastructure-as-code. This first module builds a practical foundation in TypeScript so you can author and validate infrastructure with confidence. If you already know TypeScript, feel free to skip ahead.

Roadmap for this lesson:

* Why TypeScript is useful for infrastructure as code.
* TypeScript prerequisites and essential tools.
* How to initialize a TypeScript project from scratch.
* Run a simple Hello World script using TypeScript.

## What is TypeScript?

TypeScript is a superset of JavaScript that adds static typing and modern language features. Static types enable many errors to be caught at compile time instead of at runtime, making infrastructure code more predictable and easier to debug.

<Frame>
  <img alt="A slide-like graphic titled &#x22;Dictionary Definition&#x22; with a blue rounded rectangle containing a short definition of TypeScript. It states TypeScript is a superset of JavaScript that adds static typing to catch errors at compile time, making code more predictable and easier to debug." />
</Frame>

Key points:

* TypeScript is a strict superset of JavaScript — every valid JavaScript program is valid TypeScript.
* You can declare types for parameters, variables, and return values (for example, `string`). The TypeScript compiler and many editors then report mismatches before you run your code.

Example — JavaScript vs TypeScript

JavaScript version (no static typing; possible runtime error):

```javascript theme={null}
// JS code
function greet(name) {
  return "Hello, " + name.toUpperCase();
}

greet(42); // No compile-time error, but this will cause a runtime error
```

TypeScript version (static typing surfaces the problem at compile time):

```typescript theme={null}
// TS code
function greet(name: string): string {
  return "Hello, " + name.toUpperCase();
}

greet(42); // Compile-time error: Argument of type 'number' is not assignable to parameter of type 'string'
```

In editors with TypeScript support you'll typically see these type errors immediately as you type.

## Why TypeScript for infrastructure as code?

Static typing improves reliability for infrastructure code the same way it does for applications. For example, a type error in plain HCL may only show up during `terraform apply` or `terraform validate`, whereas TypeScript (with CDK for Terraform or other IaC frameworks) surfaces the problem during development.

Terraform HCL example (error detected only at apply/validate):

```hcl theme={null}
