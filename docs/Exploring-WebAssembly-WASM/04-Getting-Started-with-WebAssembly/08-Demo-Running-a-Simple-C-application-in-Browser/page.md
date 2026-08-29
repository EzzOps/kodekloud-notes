# Demo Running a Simple C application in Browser

Source: https://notes.kodekloud.com/docs/Exploring-WebAssembly-WASM/Getting-Started-with-WebAssembly/Demo-Running-a-Simple-C-application-in-Browser/page

This tutorial teaches how to compile and run a basic C program in the browser using WebAssembly.

In this tutorial, you'll learn how to compile and execute a basic C program directly in your browser using WebAssembly. By following these steps, you can seamlessly port native C code to the web.

> **lightbulb** * [Emscripten SDK][emscripten] installed and configured
  * [Visual Studio Code][vscode] (or any code editor)
  * A modern browser (e.g., [Google Chrome][chrome])

## 1. Create the C Source File

1. Open your project folder (e.g., `WASM`) in Visual Studio Code.
2. Create a file named `hello.c` with the following content:

```c theme={null}
#include <stdio.h>

int main() {
    printf("Hello, WebAssembly!\n");
    return 0;
}
```

## 2. Compile to WebAssembly

In the integrated terminal, run:

```bash theme={null}
emcc hello.c -o hello.html
```

This command produces three output files:

| Filename   | Description                                   |
| ---------- | --------------------------------------------- |
| hello.html | HTML shell to load and run the WASM module    |
| hello.js   | JavaScript loader and glue code               |
| hello.wasm | WebAssembly binary containing compiled C code |

Verify the files:

```bash theme={null}
ls
