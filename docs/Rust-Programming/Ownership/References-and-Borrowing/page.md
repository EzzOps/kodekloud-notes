# References and Borrowing

Source: https://notes.kodekloud.com/docs/Rust-Programming/Ownership/References-and-Borrowing/page

This article explains pointers and references in Rust, focusing on memory safety, immutable references, and the concepts of borrowing versus ownership.

Before diving into Rust-specific features, it is essential to understand some fundamental concepts about pointers and references, as they form the backbone of Rust’s memory safety guarantees.

## Pointers vs. References

A pointer is a variable that stores the memory address of another variable. This low-level concept is widely used in languages like C and C++.

On the other hand, a reference in Rust is a high-level abstraction akin to pointers but comes with additional safety features. References in Rust are guaranteed to be valid and can never be null, making them the preferred method for accessing data safely.

<Frame>
  ![The image explains the concepts of pointers and references, highlighting that pointers store memory addresses and are low-level, while references in Rust are high-level, safe, and cannot be null.](https://kodekloud.com/kk-media/image/upload/v1752883952/notes-assets/images/Rust-Programming-References-and-Borrowing/pointers-references-rust-explained.jpg)
</Frame>

## Immutable References

An immutable reference permits you to borrow a value without altering it or taking ownership. This ensures that while you have access to the value, its state remains unchanged. The typical syntax for creating an immutable reference is:

```rust theme={null}
let reference = &value; // Creates an immutable reference to value
```

For example, consider the following code snippet:

```rust theme={null}
let x = 10;
let y = &x; // Immutable reference to x
println!("The value of x is: {}", y); // You can read x, but cannot modify it through y
```

Here, the ampersand (&) operator creates an immutable reference to x. While y provides access to x's value, it does not have the ability to modify it.

<Frame>
  ![The image is a diagram explaining immutable references in Rust, showing how a reference y points to a value x using the \&x syntax. It highlights that x holds the value 10, and y does not own the value, allowing x to remain valid even if y goes out of scope.](https://kodekloud.com/kk-media/image/upload/v1752883953/notes-assets/images/Rust-Programming-References-and-Borrowing/immutable-references-rust-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  Immutable references enable safe data access without transferring ownership, ensuring your original data remains intact.
</Callout>

## Borrowing Versus Ownership

In Rust, transferring a variable to a function usually means transferring its ownership. After such a transfer, the original variable becomes invalid, which can be limiting if further operations on that variable are required.

Consider the following example where ownership is transferred:

```rust theme={null}
fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(s1);
    // println!("{}", s1); // Error: s1 is no longer valid
    println!("The length of the string is {}", len);
}

fn calculate_length(s: String) -> usize {
    s.len()
}
```

In this instance, the function `calculate_length` takes ownership of `s1`, resulting in `s1` being unusable after the function call.

Borrowing offers a solution by allowing a function to access data via a reference without taking ownership. This method ensures that the original data remains accessible even after the function call. Here’s an example that demonstrates borrowing:

```rust theme={null}
fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1);
    println!("The length of '{}' is {}.", s1, len);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}
```

In this improved version, the `calculate_length` function borrows the string by accepting a reference (`&String`) as its parameter. Consequently, the main function retains ownership of `s1`, enabling its continued use post-function call.

<Callout icon="lightbulb">
  Borrowing is a core feature in Rust that allows efficient access to data without compromising safety or ownership.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/rust/module/48702f90-cc95-4c81-939c-a4565969de71/lesson/9d19fff4-3911-42ba-9926-107573d375fd" />
</CardGroup>
