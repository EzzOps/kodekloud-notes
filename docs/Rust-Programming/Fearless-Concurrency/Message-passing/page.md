# Run with info level logging
RUST_LOG=info cargo run --quiet
```

To include debug messages, use:

```bash theme={null}
RUST_LOG=debug cargo run --quiet
```

<Callout icon="lightbulb">
  Remember that the default settings in `env_logger` filter out debug messages when the log level is set to info.
</Callout>

***

## Logging with Application Logic

Enhance your application by combining logging with business logic. Consider the following example where configuration status is checked and a division function is utilized to demonstrate error handling with appropriate logging:

```rust theme={null}
use env_logger;
use log::{debug, error, info, warn};

fn main() {
    env_logger::init(); // Initialize the logger

    info!("Application started");

    let config_loaded: bool = false; // Simulate whether the config file is loaded
    if !config_loaded {
        warn!("Configuration not loaded; using defaults");
    }

    let result: Result<i32, String> = divide(10, 0); // Attempt division by zero
    match result {
        Ok(value) => info!("Division successful: {}", value),
        Err(e) => error!("Failed to divide: {}", e),
    }

    debug!("Application finished");
}

fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err(String::from("Division by zero"))
    } else {
        Ok(a / b)
    }
}
```

Run the application with debug logging enabled:

```bash theme={null}
RUST_LOG=debug cargo run --quiet
```

Expected output:

```plaintext theme={null}
[2024-11-23T21:14:22Z INFO  debug_rust] Application started
[2024-11-23T21:14:22Z WARN  debug_rust] Configuration not loaded; using defaults
[2024-11-23T21:14:22Z ERROR debug_rust] Failed to divide: Division by zero
[2024-11-23T21:14:22Z DEBUG debug_rust] Application finished
```

***

## Customizing Log Format with env\_logger and chrono

For more control over how logs are formatted, you can customize `env_logger` with the help of the `chrono` crate. This allows you to include timestamps and format messages to your preference.

First, add the `chrono` crate:

```bash theme={null}
cargo add chrono
```

Then, set up your custom logger as follows:

```rust theme={null}
use chrono::Local;
use env_logger::Builder;
use log::{debug, error, info, warn, LevelFilter};
use std::io::Write;

fn main() {
    // Initialize the logger with customized settings
    Builder::new()
        .filter(None, LevelFilter::Debug) // Default log level set to Debug
        .format(|buf, record| {
            writeln!(
                buf,
                "{} [{}] - {}",
                Local::now().format("%Y-%m-%d %H:%M:%S"), // Timestamp
                record.level(),                            // Log level
                record.args()                              // Log message
            )
        })
        .init();

    info!("Application started");

    let config_loaded: bool = false; // Simulate configuration loading
    if !config_loaded {
        warn!("Configuration not loaded; using defaults");
    }

    let result: Result<i32, String> = divide(10, 0);
    match result {
        Ok(value) => info!("Division successful: {}", value),
        Err(e) => error!("Failed to divide: {}", e),
    }

    debug!("Application finished");
}

fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err(String::from("Division by zero"))
    } else {
        Ok(a / b)
    }
}
```

Run the program with debug logging:

```bash theme={null}
RUST_LOG=debug cargo run --quiet
```

Sample output:

```plaintext theme={null}
2024-11-24 02:51:30 [INFO] - Application started
2024-11-24 02:51:30 [WARN] - Configuration not loaded; using defaults
2024-11-24 02:51:30 [ERROR] - Failed to divide: Division by zero
2024-11-24 02:51:30 [DEBUG] - Application finished
```

***

## Redirecting Logs to a File

Redirecting logs to a file can be useful for persistent logging. The following example demonstrates how to write logs to a file named `output.log`:

```rust theme={null}
use std::fs::OpenOptions;
use std::io::Write;
use env_logger::Builder;
use chrono::Local;
use log::{debug, error, info, warn, LevelFilter};

fn main() {
    // Open or create the log file
    let file = OpenOptions::new()
        .create(true)   // Create the file if it doesn't exist
        .write(true)    // Open the file for writing
        .append(true)   // Append messages to the file
        .open("output.log")
        .unwrap(); // Be sure to handle errors appropriately in production

    // Initialize the logger with custom settings directing output to the file
    Builder::new()
        .filter(None, LevelFilter::Debug)
        .format(|buf, record| {
            writeln!(
                buf,
                "{} [{}] - {}",
                Local::now().format("%Y-%m-%d %H:%M:%S"),
                record.level(),
                record.args()
            )
        })
        .target(env_logger::Target::Pipe(Box::new(file))) // Redirect logs to output.log
        .init();

    info!("Application started");

    let config_loaded: bool = false; // Simulate configuration status
    if !config_loaded {
        warn!("Configuration not loaded; using defaults");
    }

    let result: Result<i32, String> = divide(10, 0);
    match result {
        Ok(value) => info!("Division successful: {}", value),
        Err(e) => error!("Failed to divide: {}", e),
    }

    debug!("Application finished");
}

fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err(String::from("Division by zero"))
    } else {
        Ok(a / b)
    }
}
```

After running this application, all log output will be written to `output.log` instead of the terminal.

***

## Best Practices for Logging in Rust

Implement these best practices to ensure your logging system is both effective and secure:

| Best Practice                       | Description                                                                                    |
| ----------------------------------- | ---------------------------------------------------------------------------------------------- |
| Use println! for Quick Debugging    | Ideal for small tests; avoid overusing it in larger, production-grade applications.            |
| Categorize Message Levels           | Use appropriate levels like info, warn, error, and debug for better filtering.                 |
| Avoid Logging Sensitive Data        | Ensure that sensitive or personal data is not inadvertently logged, especially in production.  |
| Use Logging for Long-term Debugging | Rely on a robust logging system for ongoing maintenance instead of temporary print statements. |
| Environment-specific Configuration  | Apply verbose logging in development and restrict output in production environments.           |

<Frame>
  ![The image lists five best practices for logging, including using println! for quick debugging, categorizing log messages with appropriate log levels, avoiding logging sensitive information, using logging for long-term debugging, and configuring logging according to the environment.](https://kodekloud.com/kk-media/image/upload/v1752883872/notes-assets/images/Rust-Programming-Using-println-and-logging/best-practices-for-logging.jpg)
</Frame>

<Callout icon="triangle-alert">
  Always ensure that sensitive data, including credentials and personal information, is never logged to avoid security risks.
</Callout>

By tailoring your logging system to match your application's needs, you can significantly improve real-time debugging and production monitoring.

Happy debugging and coding in Rust!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/rust/module/fdebf97c-bade-4db7-bfcf-9881f9ec96fc/lesson/29f62fc1-d0ee-4cfe-8516-7326b0247a7f" />
</CardGroup>


# Message passing

Source: https://notes.kodekloud.com/docs/Rust-Programming/Fearless-Concurrency/Message-passing/page

This article explores message passing in Rust, focusing on safe communication between threads using channels to minimize data races.

In this lesson, we'll explore message passing in Rust, a powerful model for handling concurrency that enables safe communication between threads. By sending and receiving messages rather than sharing data directly, you can minimize the risk of data races while adhering to Rust’s ownership and borrowing principles.

When working with message passing in Rust, channels serve as the primary mechanism. They allow threads to send values to each other in a safe and efficient manner.

## What Is a Channel?

A channel in Rust is a communication primitive that enables threads to pass messages between one another. Think of it as a pipeline: one end (the sender) pushes data into the channel, while the other end (the receiver) pulls data out.

<Frame>
  ![The image is a diagram about "Message Passing" in programming, highlighting concepts of "Ownership" and "Borrowing," with a focus on doing so "Safely" and "Efficiently."](https://kodekloud.com/kk-media/image/upload/v1752883873/notes-assets/images/Rust-Programming-Message-passing/message-passing-ownership-borrowing-diagram.jpg)
</Frame>

Rust provides the `std::sync::mpsc` module—where MPSC stands for "multiple producers, single consumer"—as the standard way to create channels. This allows multiple threads to send messages into the channel while a single thread is designated to receive them.

Below is a simple example illustrating how to create a channel:

```Rust theme={null}
rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
}
```

In this code, `tx` represents the sender and `rx` represents the receiver. While this MPSC channel is suitable for many message-passing scenarios, Rust also supports more complex configurations like multi-consumer channels when needed.

<Frame>
  ![The image illustrates Rust's channel mechanism, highlighting "Multiple-Producer, Single-Consumer" with sections for "Multi-Producer" and "Multi-Consumer Channels."](https://kodekloud.com/kk-media/image/upload/v1752883874/notes-assets/images/Rust-Programming-Message-passing/rust-channel-mechanism-mpsc.jpg)
</Frame>

## Creating and Using Channels

Channels in Rust are created with the `channel` function, which returns a tuple containing a sender and a receiver. Here’s how you can create a channel for sending `String` messages:

```Rust theme={null}
rust
use std::sync::mpsc::{self, Sender, Receiver};

fn main() {
    let (tx, rx): (Sender<String>, Receiver<String>) = mpsc::channel();
}
```

If the type of messages is ambiguous, clear type annotations or sending an initial message can help the compiler infer the correct type.

For example, to send a message using the channel:

```Rust theme={null}
rust
use std::sync::mpsc::{self, Sender, Receiver};

fn main() {
    let (tx, rx): (Sender<String>, Receiver<String>) = mpsc::channel();
    tx.send(String::from("Hello")).unwrap();
}
```

The `send` method transfers ownership of the value into the channel. If the receiver is not present, this method will return an error.

<Callout icon="lightbulb">
  When running the program above, you might see a warning about the unused variable `rx`. To suppress this warning, either use the receiver in your code or prefix it with an underscore (i.e., `_rx`).
</Callout>

### Receiving Messages

On the receiving side, you can use the blocking `recv` method to wait for a message:

```Rust theme={null}
rust
use std::sync::mpsc::{self, Sender, Receiver};

fn main() {
    let (tx, rx): (Sender<String>, Receiver<String>) = mpsc::channel();
    tx.send(String::from("Hello")).unwrap();

    let received: String = rx.recv().unwrap();
    println!("Received: {}", received);
}
```

In the example above, `rx.recv()` blocks the current thread until a message is available, and the message is then printed to the console.

Alternatively, if you prefer a non-blocking approach, you can use `try_recv`. This method immediately returns an error if no message has arrived yet:

```Rust theme={null}
rust
use std::sync::mpsc::{self, Sender, Receiver};

fn main() {
    let (tx, rx): (Sender<String>, Receiver<String>) = mpsc::channel();
    tx.send(String::from("Hello")).unwrap();

    let received: String = rx.try_recv().unwrap();
    println!("Received: {}", received);
}
```

Running either of these examples should produce the following output:

```Rust theme={null}
bash
cargo run --quiet
Received: Hello
```

## Message Passing Between Threads

A common scenario for using channels is communicating between threads. Consider this example, where a child thread sends a message to the main thread:

```Rust theme={null}
rust
use std::sync::mpsc::{self, Sender, Receiver};
use std::thread;

fn main() {
    let (tx, rx): (mpsc::Sender<String>, mpsc::Receiver<String>) = mpsc::channel();

    thread::spawn(move || {
        let msg = String::from("Hi from thread");
        tx.send(msg).unwrap(); // Sends a message to the main thread
    });

    let received = rx.recv().unwrap(); // Receives the message
    println!("Received: {}", received);
}
```

Notice how the `move` keyword is used to transfer ownership of the sender `tx` into the child thread. Attempting to use `tx` in the main thread after the move would result in a compiler error.

To ensure proper synchronization, you can capture the thread handle and call `join` to wait for the thread to complete:

```Rust theme={null}
rust
use std::sync::mpsc::{self, Sender, Receiver};
use std::thread::{self, JoinHandle};

fn main() {
    let (tx, rx): (mpsc::Sender<String>, mpsc::Receiver<String>) = mpsc::channel();

    let handle: JoinHandle<()> = thread::spawn(move || {
        let msg = String::from("Hi from thread");
        tx.send(msg).unwrap(); // Sends a message to the main thread
    });

    let received = rx.recv().unwrap(); // Receives the message
    println!("Received: {}", received);
    handle.join().unwrap();
}
```

## Cloning the Sender for Multiple Producers

When you need multiple threads to send messages to a single receiver, you can clone the sender. The example below spawns five threads, each sending an integer to the receiver:

```Rust theme={null}
rust
use std::sync::mpsc::{self, Sender, Receiver};
use std::thread;

fn main() {
    let (tx, rx): (mpsc::Sender<i32>, mpsc::Receiver<i32>) = mpsc::channel();

    for i in 0..5 {
        // Clone the sender for each thread
        let tx_clone = tx.clone();
        thread::spawn(move || {
            tx_clone.send(i).unwrap();
        });
    }

    // Use the iterator interface to receive exactly five messages
    for received in rx.iter().take(5) {
        println!("Received: {}", received);
    }
}
```

A sample output might be:

```Rust theme={null}
bash
cargo run --quiet
Received: 0
Received: 1
Received: 2
Received: 4
Received: 3
```

Since thread execution is non-deterministic, the order of messages may vary.

Alternatively, you can let the receiver’s iterator run until all sender handles are dropped, automatically ending the loop once all messages have been processed:

```Rust theme={null}
rust
use std::sync::mpsc::{self, Sender, Receiver};
use std::thread;

fn main() {
    let (tx, rx): (mpsc::Sender<i32>, mpsc::Receiver<i32>) = mpsc::channel();

    for i in 0..5 {
        let tx_clone = tx.clone();
        thread::spawn(move || {
            tx_clone.send(i).unwrap();
        });
    }

    // Iterates over incoming messages until the channel is closed
    for received in rx {
        println!("Received: {}", received);
    }
}
```

Once all messages are received and all sender handles go out of scope, the receiver’s iterator exits, and the program terminates gracefully.

## Recap

Message passing in Rust offers a safe and efficient mechanism to manage concurrency by transferring ownership through channels. Use this approach when you need to coordinate work among several threads without sharing mutable state. Its seamless integration with Rust's ownership and borrowing model makes it an essential tool in your Rust programming toolkit.

For more detailed information, consider checking out [Rust's official documentation](https://doc.rust-lang.org/std/sync/mpsc/) on channels.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/rust/module/0418d83c-2090-4aac-8b6e-8c3eab45d649/lesson/5b733589-f0b5-479b-97ce-12f03026d5fc" />
</CardGroup>
