# Demo WASM in Serverside with NodeJS

Source: https://notes.kodekloud.com/docs/Exploring-WebAssembly-WASM/Future-WebAssembly-in-Cloud/Demo-WASM-in-Serverside-with-NodeJS/page

This tutorial teaches how to compile a C program into WebAssembly and execute it in a Node.js environment.

In this tutorial, you’ll learn how to compile a simple C program into WebAssembly (WASM) using Emscripten and then execute it in a Node.js environment. The workflow mirrors browser-based builds, but outputs a JavaScript “glue” file suitable for server-side execution.

## Prerequisites

* Node.js (tested with v14.18.2)
* Emscripten SDK with `emcc` available in your `PATH`

> **lightbulb** Before you begin, make sure you’ve [installed Node.js](https://nodejs.org/) and set up the [Emscripten SDK](https://emscripten.org/docs/getting_started/downloads.html).\
  Run `emcc --version` to verify your installation.

Check your Node.js version:

```bash theme={null}
node -v
