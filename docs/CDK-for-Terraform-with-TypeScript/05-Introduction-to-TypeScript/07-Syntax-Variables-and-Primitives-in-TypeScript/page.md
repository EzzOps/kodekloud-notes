# Syntax Variables and Primitives in TypeScript

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/Syntax-Variables-and-Primitives-in-TypeScript/page

Overview of TypeScript variable declarations, primitive types, explicit typing, and type inference demonstrated via a simple duck pond example

This guide covers the core TypeScript syntax you'll use when writing infrastructure and application code: variable declarations, primitive types, explicit typing, and type inference. We'll follow a practical example — Elmer Codde building a small TypeScript app to manage the ducks on his pond — to demonstrate the concepts in context.

Project layout (example in the lab)

```bash theme={null}
EXPLORER
CODE
.vscode
.prettierrc
.profile
.yarnrc.yml
index.ts
package.json
tsconfig.json
yarn.lock

root in ~/code via ⬢ v20.17.0 on ⬢ (us-east-1)
❯
```

The lab environment already has TypeScript installed and configured, and the project is ready to run.

Example TypeScript definitions for the duck app (enums, union type, interface, and a simple class that implements the interface):

```typescript theme={null}
// Enum for Duck Types
enum DuckType {
  Mallard = "Mallard",
  Muscovy = "Muscovy",
  Pekin = "Pekin",
}

// Type for Duck Colors using a union type
type DuckColor = "White" | "Brown" | "Black" | "Mixed";

// Interface for a Duck's properties
interface IDuck {
  name: string; // Name of the duck
  age: number; // Age of the duck in years
  type: DuckType; // Type of duck, using the DuckType enum
  color: DuckColor; // Color of the duck, using the DuckColor union type
  favoriteToy?: string; // Optional property: favorite toy of the duck
}

// Simple PondDuck class that implements the IDuck interface
class PondDuck implements IDuck {
  constructor(
    public name: string,
    public age: number,
    public type: DuckType,
    public color: DuckColor,
    public favoriteToy?: string
  ) {}

  quack(): void {
    console.log(`${this.name} says "quack"!`);
  }

  fly(): void {
    console.log(`${this.name} takes off!`);
  }

  land(): void {
    console.log(`${this.name} lands on the pond.`);
  }
}
```

If you want to follow along locally in the lab environment:

```bash theme={null}
