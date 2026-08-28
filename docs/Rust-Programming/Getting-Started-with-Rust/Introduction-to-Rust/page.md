# Output:
ls src/
# Output:
# main.rs
```

## Examining the Cargo.toml File

Open the `Cargo.toml` file in your favorite text editor. This file, formatted in TOML, contains essential details about your project, including package metadata and dependency information. A typical configuration might look like this:

```toml theme={null}
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at:
[dependencies]
```

The `[package]` section specifies the project name, version, and Rust edition, while the `[dependencies]` section is reserved for external libraries required by your project.

## Reviewing the Generated "Hello, World!" Program

Upon project creation, Cargo generates a simple "Hello, world!" program. Open the `src/main.rs` file to see the generated code:

```rust theme={null}
fn main() {
    println!("Hello, world!");
}
```

This minimal program serves as a starting point for further development.

## Building and Running the Project

Build your project by running the following command within the `hello_cargo` directory:

```bash theme={null}
cargo build
```

This command compiles your project, placing the executable in the `target/debug` folder. To run the executable directly, use:

```bash theme={null}
target/debug/hello_cargo
```

Alternatively, you can compile and execute in one step by running:

```bash theme={null}
cargo run
```

This approach makes development faster by automatically rebuilding your project when changes are detected.

## Checking Your Code for Errors

Cargo provides the `cargo check` command, which quickly verifies your code for errors without generating an executable. This is especially useful during development. For instance, if you accidentally omit a semicolon, running:

```bash theme={null}
cargo check
```

might produce an error message like:

```bash theme={null}
$ cargo check
    Checking hello_cargo v0.1.0 (/Users/priyanka/Desktop/my_projects/hello_rust)
error: expected `;`, found `println`
   --> src/main.rs:2:30
```

<Callout icon="lightbulb">
  Using `cargo check` during development can significantly speed up debugging by catching issues without the overhead of a full build.
</Callout>

## Summary

Cargo simplifies Rust development by managing dependencies, automating builds, and running code efficiently. While small projects might run fine using `rustc` directly, Cargo's advantages become more prominent as your codebase grows and becomes increasingly modular.

<Frame>
  ![The image is a summary of Cargo, highlighting its role in simplifying Rust development by managing dependencies, building projects, and running code efficiently. It features a Venn diagram with these three aspects.](https://kodekloud.com/kk-media/image/upload/v1752883905/notes-assets/images/Rust-Programming-Introduction-to-Cargo/cargo-rust-development-summary-diagram.jpg)
</Frame>

For larger projects with multiple files and external dependencies, Cargo helps streamline the build process and provides a clear framework for project management. Its comprehensive approach makes it an indispensable tool for every Rust developer.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/rust/module/b5f13fcf-f3bf-4b15-bd04-80798493bce7/lesson/e0a36fe2-6771-48eb-8044-426a931a0aa0" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/rust/module/b5f13fcf-f3bf-4b15-bd04-80798493bce7/lesson/932c9c3f-7399-4242-b2c2-cf2513c4e856" />
</CardGroup>


# Introduction to Rust

Source: https://notes.kodekloud.com/docs/Rust-Programming/Getting-Started-with-Rust/Introduction-to-Rust/page

This article introduces Rust, a programming language known for its performance and safety features, suitable for both students and professionals in systems programming.

Hello everyone, my name is Priyanka Yadav and I'll be your instructor for this lesson. Today, we'll explore Rust, a programming language that is quickly becoming one of the most sought-after tools in the tech industry. Whether you are an experienced developer or just beginning your coding journey, Rust offers a rich mix of performance and safety features that can benefit everyone.

## Why Rust?

Rust is a systems programming language designed to help you build fast and reliable software. It uniquely blends high-level ergonomics with low-level control. This means you can write safe, expressive code using Rust's comprehensive standard libraries and powerful syntax, while retaining the ability to manually manage system resources like memory when performance or precision is key.

<Frame>
  ![The image is an introduction to Rust, featuring the Rust logo and an illustration of a person coding on a large screen, with text stating it helps in writing fast and reliable software.](https://kodekloud.com/kk-media/image/upload/v1752883906/notes-assets/images/Rust-Programming-Introduction-to-Rust/rust-introduction-coding-software.jpg)
</Frame>

## Rust's High-Level Ergonomics and Low-Level Control

Rust stands out by combining the benefits of high-level programming convenience with the raw control over hardware typically reserved for low-level languages. This synthesis allows developers to create clean, safe, and high-performance code without compromising on flexibility.

<Frame>
  ![The image highlights Rust's features, emphasizing its combination of high-level ergonomics and low-level control.](https://kodekloud.com/kk-media/image/upload/v1752883907/notes-assets/images/Rust-Programming-Introduction-to-Rust/rust-features-ergonomics-control.jpg)
</Frame>

## Rust for Students

Rust is an ideal language for students interested in systems programming. Here’s why:

1. **Comprehensive Documentation:** Extensive and accessible documentation simplifies the learning curve, making complex systems programming topics approachable.
2. **Strong Community Support:** The Rust community is welcoming and collaborative. You can find active forums, chat rooms, and mentorship programs ready to help you overcome coding challenges.
3. **Practical Learning:** With Rust’s focus on safety and performance, you gain hands-on experience with critical concepts like memory management, concurrency, and low-level programming.

<Frame>
  ![The image is a diagram for students highlighting three aspects: educational resources, practical learning, and community support. Each aspect is represented by a colored triangle with icons and brief descriptions.](https://kodekloud.com/kk-media/image/upload/v1752883908/notes-assets/images/Rust-Programming-Introduction-to-Rust/educational-resources-learning-support-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  If you're new to systems programming, Rust's clear and detailed resources make it an excellent first language to learn.
</Callout>

## Rust for Professionals

For professionals, Rust brings a host of advantages that streamline development and enhance code reliability:

1. **Reliable Code:** Rust’s compiler enforces strict safety checks, which help reduce bugs and improve code maintainability.
2. **High Performance:** With speed comparable to C and C++, Rust is perfect for developing high-efficiency applications.
3. **Modern Tooling:** Tools like Cargo for dependency management, Rustfmt for consistent code formatting, and Rust Analyzer for IDE support significantly boost productivity.

<Frame>
  ![The image highlights three benefits of using Rust for professionals: reliable code, performance, and modern tooling. It emphasizes Rust's compiler for safety, C/C++-like performance, and tools like Cargo for productivity.](https://kodekloud.com/kk-media/image/upload/v1752883909/notes-assets/images/Rust-Programming-Introduction-to-Rust/rust-benefits-reliable-performance-tooling.jpg)
</Frame>

<Callout icon="lightbulb">
  Using Rust can lead to fewer runtime errors and improved application performance, making it a smart choice for modern software development.
</Callout>

## Industrial Adoption

Rust is trusted by numerous leading companies for its performance and reliability. Some notable adopters include:

* **Mozilla:** Rust was originally developed at Mozilla to improve the performance of critical components in the Firefox browser.
* **Dropbox:** Parts of Dropbox’s file storage backend leverage Rust to enhance speed and reliability.
* **Coursera:** Rust powers data processing pipelines at Coursera, capitalizing on the language's safety and efficiency.
* **Figma:** Seeking improved performance, Figma transitioned their multiplayer synchronization engine from TypeScript to Rust.
* **Microsoft:** Rust is employed in various systems programming projects at Microsoft to boost safety and performance.

Regardless of whether you are a student beginning your exploration or a professional seeking a dependable, high-performance language, Rust is well-suited to address a diverse range of programming challenges.

Thank you for joining me on this in-depth exploration of Rust. I am excited to continue our learning journey together throughout this lesson.

For further reading and detailed tutorials, check out these resources:

* [Rust Official Documentation](https://www.rust-lang.org/learn)
* [Rust Programming Language Book](https://doc.rust-lang.org/book/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/rust/module/b5f13fcf-f3bf-4b15-bd04-80798493bce7/lesson/21189ee6-b619-4b22-951f-b6486b5d3e42" />
</CardGroup>
