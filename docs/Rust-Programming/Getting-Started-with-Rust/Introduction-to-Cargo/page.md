# Introduction to Cargo

Source: https://notes.kodekloud.com/docs/Rust-Programming/Getting-Started-with-Rust/Introduction-to-Cargo/page

Cargo is the essential tool for managing Rust projects, serving as both the package manager and build system.

Cargo is the essential tool for managing Rust projects, serving as both the package manager and build system. It streamlines many aspects of Rust development—including project management, dependency resolution, testing, and more—all in one handy command-line utility.

<Frame>
  ![The image explains that Cargo is the Rust package manager and build system, highlighting its functions: managing Rust projects, handling dependencies, and running tests.](https://kodekloud.com/kk-media/image/upload/v1752883902/notes-assets/images/Rust-Programming-Introduction-to-Cargo/cargo-rust-package-manager-functions.jpg)
</Frame>

Rust applications can quickly become complex with numerous dependencies. Manually managing these can be error-prone and time-consuming. Cargo automates this process, ensuring all libraries are at the correct versions and that your project compiles successfully.

<Frame>
  ![The image explains that Rust projects often involve multiple dependencies, which can be error-prone and time-consuming, and highlights that Cargo automates version control and ensures proper compilation.](https://kodekloud.com/kk-media/image/upload/v1752883904/notes-assets/images/Rust-Programming-Introduction-to-Cargo/rust-projects-dependencies-cargo.jpg)
</Frame>

## Creating a New Rust Project

To begin leveraging Cargo, start by creating a new Rust project. Open your terminal, navigate to the directory of your choice, and execute the following commands:

```bash theme={null}
cd path/to/your/directory
cargo new hello_cargo
```

This creates a new `hello_cargo` directory with a minimal Rust project setup. Next, navigate into the project directory:

```bash theme={null}
cd hello_cargo
```

Inside, you'll find a `src` folder containing a `main.rs` file and a `Cargo.toml` file. The `Cargo.toml` file maintains your project's metadata and dependency list. Running a directory listing should display the following structure:

```bash theme={null}
ls
