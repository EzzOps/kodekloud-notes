# Demo WASM and Docker Integration

Source: https://notes.kodekloud.com/docs/Exploring-WebAssembly-WASM/Future-WebAssembly-in-Cloud/Demo-WASM-and-Docker-Integration/page

Learn to compile a C program to WebAssembly and package it into a Docker image with a minimal runtime.

Learn how to compile a simple C program to WebAssembly (WASM) using a WASI-compatible compiler and then package it into a Docker image with a minimal runtime.

<Callout icon="triangle-alert">
  Docker’s WASM integration is currently a beta feature available in a special technical-preview build of Docker Desktop. Refer to [Docker’s experimental WASM support][docker-wasm] when testing locally.
</Callout>

## Prerequisites

| Tool             | Version                    | Purpose                               |
| ---------------- | -------------------------- | ------------------------------------- |
| Clang (WASI SDK) | v16+                       | Compile C to WASM via WASI            |
| Docker Desktop   | Latest (technical preview) | Build and run WASM containers         |
| WasmEdge         | v0.14+                     | Execute the WASM binary inside Docker |

## 1. Write a simple C program

Create a file named `helloworld.c`:

```c theme={null}
#include <stdio.h>

int main() {
    printf("hello, world\n");
    return 0;
}
```

## 2. Compile to a WASM binary

Use the WASI SDK’s Clang to target `wasm32-wasi`:

```bash theme={null}
clang --target=wasm32-wasi -O3 helloworld.c -o helloworld.wasm
```

This produces a standalone `helloworld.wasm` in your working directory.

## 3. Create the Dockerfile

We’ll build **FROM scratch** so the final image only contains the WASM binary:

```dockerfile theme={null}
FROM scratch
COPY helloworld.wasm /helloworld.wasm
ENTRYPOINT [ "/helloworld.wasm" ]
```

Save this as `Dockerfile` alongside `helloworld.wasm`.

## 4. Build the Docker image

Run:

```bash theme={null}
cd path/to/your/project
docker build --platform=wasm/wasm32 -t helloworld-wasm .
```

<Callout icon="lightbulb">
  The `--platform=wasm/wasm32` flag instructs Docker to treat this as a WASM container.
</Callout>

## 5. Run the WASM container

Execute with the WasmEdge runtime support in containerd:

```bash theme={null}
docker run --rm \
  --name wasm-docker-c-program \
  --runtime=io.containerd.wasmedge.v1 \
  helloworld-wasm
```

You should see:

```text theme={null}
hello, world
```

Congratulations! You’ve compiled a C program to WebAssembly and run it inside a Docker container.

## Links and References

* [Docker’s experimental WASM support][docker-wasm]
* [WASI SDK releases][wasi-sdk]
* [WasmEdge runtime][wasmedge]

[docker-wasm]: https://docs.docker.com/desktop/experimental-features/wasm/

[wasi-sdk]: https://github.com/WebAssembly/wasi-sdk/releases

[wasmedge]: https://github.com/WasmEdge/WasmEdge

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/exploring-webassembly-wasm/module/a9d35579-0f55-465c-8d70-eec38ff7c750/lesson/f5015961-66ac-4aba-b50e-419e7e356ac4" />
</CardGroup>
