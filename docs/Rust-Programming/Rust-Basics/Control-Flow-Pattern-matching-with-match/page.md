# Control Flow Pattern matching with match

Source: https://notes.kodekloud.com/docs/Rust-Programming/Rust-Basics/Control-Flow-Pattern-matching-with-match/page

Pattern matching in Rust using the match statement allows comparing values against patterns and executing corresponding code blocks for the first match.

Pattern matching using the match statement in Rust is one of the language's most powerful control flow constructs. It allows you to compare a value against a series of patterns and execute corresponding code blocks for the first pattern that matches. This approach is more robust than traditional switch statements in other languages because Rust's match statement supports an extensive range of pattern types—such as literals, variables, wildcards, tuples, and enums—enabling you to write concise, expressive, and maintainable code.

<Frame>
  ![The image is an introduction slide explaining the match statement in Rust, highlighting its power compared to switch statements, its ability to handle various patterns, and its use for writing concise and expressive code.](https://kodekloud.com/kk-media/image/upload/v1752883982/notes-assets/images/Rust-Programming-Control-Flow-Pattern-matching-with-match/rust-match-statement-introduction.jpg)
</Frame>

## Basic Syntax

Below is a simple example demonstrating the basic syntax of the match statement. You specify the value to evaluate after the keyword `match` and then define a series of arms. Each arm consists of a pattern followed by a block of code that executes if the match is successful:

```rust theme={null}
match value {
    pattern1 => {
        // Code to run if pattern1 matches
    },
    pattern2 => {
        // Code to run if pattern2 matches
    },
    _ => {
        // Code to run if no other patterns match (optional)
    },
}
```

## Example: Matching a Number

In this example, a number is compared against several specific patterns, with a default case to handle all other values:

```rust theme={null}
fn main() {
    let number = 3;

    match number {
        1 => println!("One"),
        2 => println!("Two"),
        3 => println!("Three"),
        _ => println!("Something else"),
    }
}
```

Since the number is 3, the output will be:

```text theme={null}
Three
```

## Using the OR Operator

Rust allows you to match multiple patterns for a single arm by using the OR operator (`|`). This feature makes it simple to execute the same block of code for multiple specific values:

```rust theme={null}
match number {
    1 | 2 | 3 => println!("One, two, or three"),
    _ => println!("Something else"),
}
```

Consider this complete example when the value is 2:

```rust theme={null}
fn main() {
    let number = 2;

    match number {
        1 | 2 | 3 => println!("One, two, or three"),
        _ => println!("Something else"),
    }
}
```

**Output:**

```text theme={null}
One, two, or three
```

## Matching Value Ranges

A useful feature of Rust's match statement is the ability to match ranges of values using the `..=` syntax. This allows you to check if a value falls within a specific range:

```rust theme={null}
fn main() {
    let number = 7;
    
    match number {
        1..=5 => println!("Between one and five"),
        6..=10 => println!("Between six and ten"),
        _ => println!("Something else"),
    }
}
```

Since 7 is within the range of 6 through 10, the output will be:

```text theme={null}
Between six and ten
```

## Destructuring Complex Data Types

Rust's match statement is not limited to simple values. It also supports destructuring of complex data types like tuples, structs, and enums, enabling you to work with their individual components efficiently.

### Destructuring a Tuple

The following example demonstrates how to destructure a tuple and add conditional extractions with additional logic:

```rust theme={null}
fn main() {
    let pair = (2, -2);

    match pair {
        (x, y) if x == y => println!("The numbers are equal"),
        (x, y) if x + y == 0 => println!("The numbers are opposites"),
        _ => println!("No special properties"),
    }
}
```

For the tuple `(2, -2)`, the second arm is executed because the numbers are opposites.

### Ignoring Unneeded Values

Sometimes you may only need part of the data from a tuple. In such cases, you can use the wildcard `_` to ignore the parts that are not required:

```rust theme={null}
fn main() {
    let pair = (2, 8);
    
    match pair {
        (x, _) => println!("The first number is: {}", x),
    }
}
```

This code will produce the output:

```text theme={null}
The first number is: 2
```

<Callout icon="lightbulb">
  Rust’s match statement ensures that all cases are covered at compile time, providing a safeguard against unexpected values.
</Callout>

## Summary

Pattern matching with the match statement in Rust provides a flexible and elegant way to handle decision-making in your code. In this article, we covered:

* The basic structure of a match statement for comparing a value against multiple patterns.
* Using the OR operator (`|`) to handle multiple patterns in a single arm.
* Matching ranges of values with the `..=` syntax.
* Destructuring complex data types such as tuples and selectively ignoring parts of a pattern.

<Frame>
  ![The image is a summary of four programming concepts related to pattern matching, including basic match statements, matching multiple patterns, matching ranges, and destructuring with match.](https://kodekloud.com/kk-media/image/upload/v1752883983/notes-assets/images/Rust-Programming-Control-Flow-Pattern-matching-with-match/pattern-matching-programming-summary.jpg)
</Frame>

Thank you for reading this article on Rust's pattern matching. For more information and advanced examples, consider exploring [Rust’s official documentation](https://www.rust-lang.org/learn).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/rust/module/f232d417-91e4-49e7-b538-be7db1e23daf/lesson/b4e48ad2-2244-4420-95eb-63d81ab37a31" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/rust/module/f232d417-91e4-49e7-b538-be7db1e23daf/lesson/a59f7a9a-f842-4ffb-92d4-41849c8d0a37" />
</CardGroup>
