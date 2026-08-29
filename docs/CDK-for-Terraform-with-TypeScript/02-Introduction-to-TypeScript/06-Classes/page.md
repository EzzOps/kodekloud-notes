# Classes

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-TypeScript/Classes/page

Explains TypeScript classes using a PondDuck example to demonstrate encapsulation, properties, methods, and independent instance state

Now let's look at TypeScript classes and how they help model objects with state and behavior.

<Frame>
  <img alt="A minimalist slide showing the word &#x22;Classes&#x22; on a white background with a large teal curved shape on the right. A white icon of a vertical rectangle with three dots sits on the teal area, and a small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left." />
</Frame>

Elmer wants each duck to have its own behavior (for example: flying and landing). To model that, we create a TypeScript class that serves as a blueprint for duck objects. The example below shows a `PondDuck` class that encapsulates properties (state) and methods (behavior) for each duck instance.

```typescript theme={null}
class PondDuck {
  name: string;
  age: number;
  type: string;
  color: string;
  isFlying: boolean; // Ducks are not flying by default
  favoriteFood?: string; // Optional property

  constructor(name: string, age: number, type: string, color: string, favoriteFood?: string) {
    this.name = name;
    this.age = age;
    this.type = type;
    this.color = color;
    this.isFlying = false;
    this.favoriteFood = favoriteFood;
  }

  quack(times = 1): void {
    for (let i = 0; i < times; i++) {
      console.log(`${this.name} says: Quack!`);
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
      console.log(`${this.name} lands gracefully`);
    } else {
      console.log(`${this.name} is already on the ground!`);
    }
  }
}
```

This class demonstrates encapsulation: state (properties) and behavior (methods) are grouped together so each instance manages its own state and transitions. Next, create instances and invoke the methods to see how state changes per instance.

```typescript theme={null}
const daffy = new PondDuck('Daffy', 3, 'Mallard', 'Black');
const donald = new PondDuck('Donald', 5, 'Pekin', 'White');

daffy.fly();
daffy.fly();
daffy.land();
daffy.land();

donald.fly();
donald.quack(2);
```

Expected console output:

```text theme={null}
Daffy starts flying!
Daffy is already flying!
Daffy lands gracefully
Daffy is already on the ground!
Donald starts flying!
Donald says: Quack!
Donald says: Quack!
```

> **lightbulb** Each instance (`daffy`, `donald`) maintains independent state — calling `daffy.fly()` does not change `donald`. The `favoriteFood?: string` uses TypeScript's optional property syntax so the constructor can omit it.

Properties and methods at a glance:

| Member                   | Type / Signature               | Description                                        |
| ------------------------ | ------------------------------ | -------------------------------------------------- |
| `name`                   | `string`                       | Duck's name (instance property)                    |
| `age`                    | `number`                       | Duck's age in years                                |
| `type`                   | `string`                       | Species or breed (e.g., `Mallard`)                 |
| `color`                  | `string`                       | Plumage color                                      |
| `isFlying`               | `boolean`                      | Tracks whether the duck is currently flying        |
| `favoriteFood`           | `string?`                      | Optional favorite food                             |
| `constructor(...)`       | `constructor(name: string, …)` | Initializes a new `PondDuck` instance              |
| `quack(times = 1): void` | Method                         | Prints quack message `times` times                 |
| `fly(): void`            | Method                         | Toggles `isFlying` to `true` and logs start flying |
| `land(): void`           | Method                         | Toggles `isFlying` to `false` and logs landing     |

Key takeaways:

* Use classes to encapsulate related state and behavior.
* Optional properties use the `?` operator and can be omitted during construction.
* Methods should manage state transitions (e.g., `fly()`/`land()` check `isFlying` before changing it).
* Instances are independent; operations on one instance do not affect others.

Links and references:

* [TypeScript Classes — Handbook](https://www.typescriptlang.org/docs/handbook/classes.html)
* [Object-Oriented Programming (OOP) Concepts](https://en.wikipedia.org/wiki/Object-oriented_programming)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/eb523de4-1aeb-429a-820a-20d9f6426562/lesson/e591fbfb-cd71-44ca-9a30-f689670b2e74)
