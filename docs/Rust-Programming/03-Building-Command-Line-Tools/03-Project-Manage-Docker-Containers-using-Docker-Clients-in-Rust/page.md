# Project Manage Docker Containers using Docker Clients in Rust

Source: https://notes.kodekloud.com/docs/Rust-Programming/Building-Command-Line-Tools/Project-Manage-Docker-Containers-using-Docker-Clients-in-Rust/page

Guide to building a Rust CLI that manages Docker containers and images using Bollard and Clap, supporting list start stop and pull commands

Build a compact Rust CLI to manage Docker: list containers/images, start/stop containers, and pull images. This guide walks through scaffolding the project, adding async Docker support with Bollard, parsing commands with Clap, organizing a modular code layout, and implementing the core commands.

<Frame>
  <img alt="A presentation slide titled &#x22;Project: Manage Docker Containers using Docker Clients in Rust.&#x22; A teal-blue curved shape on the right shows a white monitor/code icon, with a small &#x22;© Copyright KodeKloud&#x22; in the bottom-left." />
</Frame>

Prerequisites

* Rust toolchain (rustup + cargo)
* Docker running locally (Docker Desktop on macOS/Windows or Docker daemon on Linux)
* Basic familiarity with async/await in Rust
* Optional: VS Code (or your preferred editor)

Create the project

From your projects directory:

```bash theme={null}
