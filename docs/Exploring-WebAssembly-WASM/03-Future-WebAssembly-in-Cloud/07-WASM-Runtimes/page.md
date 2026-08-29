# Output:
# Hello, WASM in Server Side!
```

You’ve now compiled C to WASM and run it server-side—no browser needed.

## 5. Containerizing WASM with Docker

Package your Node.js + WASM service into a Docker container for consistent cloud deployments.

<Callout icon="lightbulb">
  Use a multi-stage Dockerfile to minimize image size by separating build and runtime dependencies.
</Callout>

Create `server.js`:

```javascript theme={null}
const express = require('express');
const app = express();
const wasm = require('./hello.js');

app.get('/hello', (req, res) => {
  wasm.onRuntimeInitialized = () => {
    wasm._main();           // invoke the C `main`
    res.send('Hello, WASM in Server Side!');
  };
});

app.listen(3000, () => console.log('Listening on port 3000'));
```

Create a `Dockerfile`:

```dockerfile theme={null}
FROM node:14
WORKDIR /app
COPY . .
RUN npm install express
CMD ["node", "server.js"]
```

Build and run:

```bash theme={null}
docker build -t hello-wasm-node-server .
docker run -p 3000:3000 hello-wasm-node-server
```

<Frame>
  ![Icons representing JavaScript (hello.js), WebAssembly (hello.wasm), and Docker container.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874828/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Beyond-the-Browser/wasm-in-action-docker-icons.jpg)
</Frame>

Access via `http://localhost:3000/hello` or:

```bash theme={null}
curl http://localhost:3000/hello
# Hello, WASM in Server Side!
```

<Frame>
  ![Terminal output showing "Hello, WASM in Server Side!" alongside Node.js, WASM, Docker, and cloud icons.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874829/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Beyond-the-Browser/wasm-in-action-terminal-output.jpg)
</Frame>

Deploying this image to any cloud service gives you a scalable, secure back-end powered by WASM.

## 6. Edge Computing with WebAssembly

Edge platforms reduce latency by running code near users or data sources. CDNs and edge services using WASM include:

* **Cloudflare Workers**: lightweight JavaScript/WASM functions at the edge
* **Fastly Compute\@Edge**: WASM applications with full crate support
* **AWS Wavelength** / **Azure Edge Zones**: containerized workloads closer to 5G networks

<Frame>
  ![Diagram of WASM integration with CDN nodes, Cloudflare Workers, and Fastly Compute@Edge, showing users, code files, and a WASM logo.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874830/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Beyond-the-Browser/wasm-cdn-integration-diagram.jpg)
</Frame>

As container and WASM ecosystems converge, deploying to edge nodes becomes as simple as any microservice.

## Conclusion

You’ve seen how WebAssembly extends:

* From the browser’s sandbox to high-performance server workloads
* Into cloud containers for easy scaling and portability
* All the way to edge nodes for minimal latency

WASM’s speed, security, and platform neutrality are shaping the future of distributed computing—beyond the browser and across every layer of the stack.

***

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Emscripten](https://emscripten.org)
* [Wasmtime](https://github.com/bytecodealliance/wasmtime)
* [Cloudflare Workers](https://developers.cloudflare.com/workers)
* [Fastly Compute@Edge](https://developer.fastly.com/compute/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/exploring-webassembly-wasm/module/a9d35579-0f55-465c-8d70-eec38ff7c750/lesson/668cc558-9804-419c-bcad-d0eca6248f4b" />
</CardGroup>


# WASM Runtimes

Source: https://notes.kodekloud.com/docs/Exploring-WebAssembly-WASM/Future-WebAssembly-in-Cloud/WASM-Runtimes/page

This guide explores WASM runtimes, their operation, and popular options for running WebAssembly across various platforms.

WebAssembly (WASM) has evolved from a browser-only technology into a versatile, high-performance solution that runs on servers, desktops, and even embedded devices. In this guide, we’ll explore what a WASM runtime is, how it operates, and the most popular runtimes you can choose from.

<Frame>
  ![The image is a diagram explaining WASM runtimes, showing a flow from "Write Once Run Anywhere (WORA)" to "JVM" to "OS."](../../../../images/kodekloud.com/kk-media/image/upload/v1752874831/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/wasm-runtimes-wora-jvm-os-diagram.jpg)
</Frame>

## What Is a WASM Runtime?

A WebAssembly runtime is the execution environment that loads, validates, compiles, and runs a `.wasm` module. While browsers include an embedded WASM engine, standalone runtimes enable you to run the same modules on:

* **Servers**
* **Desktops**
* **Edge devices and IoT**

<Frame>
  ![The image illustrates the concept of WebAssembly (WASM) as a runtime environment, showing its applicability across mobile, server, and desktop platforms.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874832/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/wasm-runtime-environment-illustration.jpg)
</Frame>

### The Execution Pipeline

1. **Load & Decode**\
   The runtime unpacks and verifies the WASM binary.

2. **Compile to Machine Code**\
   A compiler backend (e.g., Cranelift) translates WASM to native instructions.

<Frame>
  ![The image illustrates the conversion of a WASM (WebAssembly) binary file into machine code, as part of exploring runtimes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874833/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/wasm-binary-to-machine-code.jpg)
</Frame>

3. **Ahead-of-Time (AOT) vs. Just-in-Time (JIT)**
   * AOT: Precompiles modules for predictable startup and performance.
   * JIT: Compiles at runtime for flexibility and faster iteration.

<Frame>
  ![The image compares "Ahead of time" (AOT) and "Just in time" (JIT) runtimes, represented by a document with a pencil and speech bubbles, respectively.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874834/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/aot-vs-jit-runtime-comparison.jpg)
</Frame>

4. **Execution & Isolation**\
   Secure sandboxing ensures memory safety and resource limits.

5. **Host Interactions**\
   The runtime mediates calls between WASM modules and host APIs (e.g., JavaScript in the browser or OS services on a server).

<Frame>
  ![The image illustrates the concept of exploring runtimes, showing a translated WASM module interacting with JavaScript and a server-like icon.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874835/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/wasm-runtime-exploration-diagram.jpg)
</Frame>

6. **Result Delivery & Teardown**\
   After running, the runtime returns outputs and frees resources.

<Frame>
  ![The image illustrates the role of a Wasm runtime, showing a flow from WASM to Runtimes to VM, with corresponding icons for each stage.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874836/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/wasm-runtime-flow-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  Different runtimes may prioritize AOT or JIT differently. Choose based on startup latency, memory footprint, and security requirements.
</Callout>

***

## Popular WASM Runtimes

Below are some of the leading runtimes in the WASM ecosystem, each with unique strengths.

### Wasmtime

Wasmtime, developed by the [Bytecode Alliance](https://bytecodealliance.org/), is a standalone runtime optimized for both AOT and JIT through Cranelift. It can be embedded in Rust, Python, or C programs and scales from microcontrollers to cloud servers.

<Frame>
  ![The image illustrates an example of runtime environments, featuring Bytecode Alliance's Wasmtime, with icons representing Python, C, and Rust, alongside labels for "Robust Server" and "Small IoT."](../../../../images/kodekloud.com/kk-media/image/upload/v1752874836/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/runtime-environments-wasmtime-icons.jpg)
</Frame>

### WasmCloud

WasmCloud offers a service-oriented model for deploying WebAssembly microservices. It provides actor-based messaging, built-in key-value storage, and secure capabilities — perfect for polyglot cloud and edge workloads.\
[Learn more ›](https://wasmcloud.dev)

### Lucet

Also from the Bytecode Alliance, Lucet is an AOT-only runtime designed for untrusted code at the edge. It focuses on minimal latency, tight sandboxing, and predictable resource usage — powering platforms like Fastly’s [Compute@Edge](https://www.fastly.com/products/compute).

<Frame>
  ![The image illustrates an example of a runtime environment involving Bytecode Alliance, Lucet, and Fastly, highlighting security, efficient runtime, and code execution.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874838/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/bytecode-alliance-lucet-fastly-runtime.jpg)
</Frame>

### Wasm3

Wasm3 is a super-lightweight interpreter ideal for constrained devices. Written in pure C, it fits platforms from microcontrollers to servers and starts in under 20ms on typical hardware.\
[Learn more ›](https://wasm3.dev)

### WAMR

The WebAssembly Micro Runtime (WAMR) targets embedded systems and IoT. At its core is iWasm, supporting interpretation, AOT, and JIT within a minimal footprint that adheres to the [W3C WASM MVP](https://www.w3.org/TR/wasm-core-1/).

<Frame>
  ![The image is a diagram illustrating a runtime example, featuring components like WASM Interpretation, AOT, JIT, and the iwasm VM, associated with the Bytecode Alliance and WAMR.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874839/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/wasm-runtime-example-diagram.jpg)
</Frame>

***

## Runtime Comparison

| Runtime   | Best For             | Key Features                                            |
| --------- | -------------------- | ------------------------------------------------------- |
| Wasmtime  | General-purpose      | AOT & JIT (Cranelift), embeddable in multiple languages |
| WasmCloud | Microservices        | Actor model, secure capabilities, polyglot support      |
| Lucet     | Edge environments    | AOT-only, minimal latency, strong isolation             |
| Wasm3     | Resource-constrained | Ultra-portable interpreter, tiny footprint              |
| WAMR      | IoT & embedded       | iWasm VM, AOT/JIT/interpretation, W3C-compliant         |

***

## Choosing the Right Runtime

<Frame>
  ![The image is a diagram showing the role of different runtimes: WASMER and WASMTIME for general purposes, WASMEdge for edge computing, Wasm3 for diverse platforms, and Emscripten for WASM in browsers.](../../../../images/kodekloud.com/kk-media/image/upload/v1752874840/notes-assets/images/Exploring-WebAssembly-WASM-WASM-Runtimes/wasm-runtimes-diagram-edge-computing.jpg)
</Frame>

* **Wasmtime & Wasmer**: Versatile, embeddable, multi-language
* **WasmEdge**: High performance at the edge ([WasmEdge](https://wasmedge.org))
* **Wasm3**: Best for minimal-resource devices
* **Emscripten**: Bridges C/C++ to browsers via WASM

<Callout icon="triangle-alert">
  When low startup time is critical, prefer AOT compilation. JIT may increase variability in performance and introduce additional dependencies.
</Callout>

***

## References

* [WebAssembly Official Site](https://webassembly.org)
* [Bytecode Alliance](https://bytecodealliance.org)
* [Wasmtime Documentation](https://bytecodealliance.github.io/wasmtime)
* [WasmCloud Docs](https://wasmcloud.dev)
* [Lucet Docs](https://bytecodealliance.github.io/lucet)
* [Wasm3 Homepage](https://wasm3.dev)
* [WAMR GitHub](https://github.com/bytecodealliance/wasm-micro-runtime)
* [WasmEdge](https://wasmedge.org)
* [Emscripten](https://emscripten.org)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/exploring-webassembly-wasm/module/a9d35579-0f55-465c-8d70-eec38ff7c750/lesson/57e0ddd9-b3fd-44b4-a395-c8ae9fd1763c" />
</CardGroup>
