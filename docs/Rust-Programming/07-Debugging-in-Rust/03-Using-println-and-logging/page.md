# Using println and logging

Source: https://notes.kodekloud.com/docs/Rust-Programming/Debugging-in-Rust/Using-println-and-logging/page

This article explores debugging techniques in Rust using the println! macro and advanced logging for efficient application troubleshooting and monitoring.

In this article, we continue our debugging series in Rust by exploring two essential techniques: quick debugging with the `println!` macro and advanced logging for larger applications. These techniques are beneficial for both beginners and seasoned developers seeking to efficiently troubleshoot and monitor their applications.

***

## Quick Debugging with println!

The `println!` macro is a straightforward way to print text and variable values to the console, making it ideal for quick and simple debugging tasks. By inserting `println!` statements in your code, you can trace execution, verify variable contents, and troubleshoot conditional logic.

### Basic println! Usage

The example below illustrates how to print the values of variables using `println!`:

```rust theme={null}
fn main() {
    let x = 5;
    println!("The value of x is: {}", x);

    let y = 10;
    println!("The value of y is: {}", y);

    let z = x + y;
    println!("x + y = {}", z);
}
```

> **lightbulb** Incorporate `println!` statements at strategic points in your code to verify that your logic and variable states are as expected.

### Common Use Cases for println!

* **Printing Variable Values:** Insert print statements to display values at critical stages.
* **Tracing Execution Paths:** Log the sequence of executed code segments.
* **Evaluating Conditional Branches:** Debug if-else blocks by indicating which branch is executed.

![The image lists three use cases of the println function: checking variable values, tracing execution flow, and debugging conditional logic.](https://kodekloud.com/kk-media/image/upload/v1752883869/notes-assets/images/Rust-Programming-Using-println-and-logging/println-use-cases-debugging.jpg)

***

## Advanced Debugging with Logging

For more robust and scalable debugging, leveraging logging capabilities is essential. Logging provides finer control over the output, allowing you to define levels of verbosity, categorize messages, and choose specific output destinations.

### Why Use Logging?

* **Control Output Levels:** Filter messages based on severity (e.g., errors, warnings, debug).
* **Categorize Messages:** Utilize log levels such as info, warn, error, and debug.
* **Flexible Output Destinations:** Direct logs to the console, files, or remote systems for further analysis.

### Leveraging Rust’s Logging Ecosystem

Rust offers a powerful logging ecosystem with the [log crate](https://docs.rs/log) acting as a facade. When paired with logging backends like `env_logger` or `fern`, you can build a robust logging framework tailored to your application's needs.

![The image is an introduction slide titled "Logging in Rust" and highlights three features: control over output, categorized messages, and configurable output destinations.](https://kodekloud.com/kk-media/image/upload/v1752883869/notes-assets/images/Rust-Programming-Using-println-and-logging/logging-in-rust-introduction-slide.jpg)

![The image is a diagram titled "Setting Up Logging With log crate," showing two components: "Log Crate" and "Logging Backend," with the Rust logo in between.](https://kodekloud.com/kk-media/image/upload/v1752883871/notes-assets/images/Rust-Programming-Using-println-and-logging/setting-up-logging-log-crate-diagram.jpg)

***

## Setting Up Logging in Your Project

To begin using logging, add the `log` and `env_logger` crates to your `Cargo.toml` file:

```toml theme={null}
[dependencies]
env_logger = "0.11.5"
log = "0.4.22"
```

Once added, building your project might output messages indicating the installation of related dependencies:

```bash theme={null}
Adding is_terminal_polyfill v1.70.1
Adding memchr v2.7.4
Adding regex v1.11.1
...
debug_rust on 'master' [?] is v0.1.0 via v1.82.0 took 3s
```

The `log` crate provides logging macros such as `info!`, `warn!`, `error!`, and `debug!`, while `env_logger` handles formatting and output based on the environment configuration.

### Basic Logging Example

The following code demonstrates how to initialize the logger and output various log messages:

```rust theme={null}
use env_logger;
use log::{debug, error, info, warn};

fn main() {
    env_logger::init(); // Initialize the logger

    info!("Application started");
    warn!("This is a warning message");
    error!("An error occurred");
    debug!("This is a debug message");
}
```

By default, `env_logger` only prints log messages at the error level and above. To view more detailed logs, set the `RUST_LOG` environment variable:

```bash theme={null}
