# hello.c  hello.html  hello.js  hello.wasm
```

<Callout icon="triangle-alert">
  Ignore any `cache:INFO` messages during compilation—they’re just Emscripten diagnostics.
</Callout>

## 3. Run in the Browser

Serve the folder with a static server (for example, Live Server in VS Code) and open `hello.html`. You should see:

```text theme={null}
Hello, WebAssembly!
```

## 4. Explore the Generated Loader

Open `hello.html` to inspect how it integrates the loader:

```html theme={null}
<script>
  Module.setStatus('Downloading...');
  window.onerror = (event) => {
    Module.setStatus('Exception thrown, see JavaScript console');
    spinnerElement.style.display = 'none';
    Module.setStatus = (text) => {
      if (text) console.error('[post-exception status] ' + text);
    };
  };
</script>
<script async type="text/javascript" src="hello.js"></script>
```

Next, examine the key loader function in `hello.js`:

```javascript theme={null}
function instantiateAsync(binary, binaryFile, imports, callback) {
  if (!binary &&
      typeof WebAssembly.instantiateStreaming === 'function' &&
      isDataUri(binaryFile) &&
      !isFileURI(binaryFile)) {
    return fetch(binaryFile, { credentials: 'same-origin' })
      .then(response => {
        // Handle WebAssembly.instantiateStreaming response
      });
  }
}
```

<Frame>
  ![The image shows a code editor with JavaScript code open, specifically focusing on WebAssembly (WASM) file handling. The editor displays syntax highlighting and a file explorer on the left.](https://kodekloud.com/kk-media/image/upload/v1752874849/notes-assets/images/Exploring-WebAssembly-WASM-Demo-Running-a-Simple-C-application-in-Browser/javascript-wasm-file-handling-editor.jpg)
</Frame>

This snippet demonstrates how the `.wasm` binary is fetched and instantiated, completing the path from C source to browser execution.

## References

* [WebAssembly][webassembly]
* [Emscripten SDK][emscripten]
* [Visual Studio Code][vscode]
* [Google Chrome][chrome]

[webassembly]: https://webassembly.org

[emscripten]: https://emscripten.org

[vscode]: https://code.visualstudio.com

[chrome]: https://www.google.com/chrome

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/exploring-webassembly-wasm/module/35f32a4b-b0a4-45ba-a4a8-827feffc5940/lesson/5faa1d73-f079-4ffb-bea5-f639e88b4a5a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/exploring-webassembly-wasm/module/35f32a4b-b0a4-45ba-a4a8-827feffc5940/lesson/36283a85-1a9e-4c45-b475-a6c8bc7f5eb4" />
</CardGroup>


# Demo Setting up the Development Environment

Source: https://notes.kodekloud.com/docs/Exploring-WebAssembly-WASM/Getting-Started-with-WebAssembly/Demo-Setting-up-the-Development-Environment/page

This lesson covers installing and configuring the Emscripten SDK for compiling WebAssembly binaries and setting up a code editor for development.

In this lesson, you’ll install and configure the Emscripten SDK to compile WebAssembly (WASM) binaries and prepare your code editor for development.

## Prerequisites

* Git installed on your machine
* Homebrew (macOS), Chocolatey (Windows), or another package manager
* A modern code editor (we’ll use Visual Studio Code)

## 1. Clone and Install Emscripten via Git

Visit the official Emscripten site for full details: [https://emscripten.org](https://emscripten.org)

```bash theme={null}
