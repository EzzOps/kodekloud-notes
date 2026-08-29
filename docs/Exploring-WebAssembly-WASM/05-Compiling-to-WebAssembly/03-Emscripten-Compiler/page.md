# Emscripten Compiler

Source: https://notes.kodekloud.com/docs/Exploring-WebAssembly-WASM/Compiling-to-WebAssembly/Emscripten-Compiler/page

Learn to use Emscripten to compile C/C++ into WebAssembly and JavaScript for high-performance web applications.

In this lesson, you'll learn how to use **Emscripten**—the powerful compiler toolchain that converts C and C++ into high-performance [WebAssembly (WASM)](https://webassembly.org) and JavaScript. Emscripten enables both browsers and server environments (like [Node.js](https://nodejs.org)) to run native code with near-native speed, making it ideal for games, graphics libraries, and utility ports.

## Why Emscripten Matters

* Brings established C/C++ applications to the Web platform
* Enables game engines, graphics libraries, and frameworks to run in browsers
* Supports modern optimizations and a simulated file system

Mozilla and Epic Games showcased **Unreal Engine 3** and **4** running in Firefox, illustrating WebAssembly’s potential for gaming.

![The image features logos of Mozilla Firefox and Epic Games, with a central graphic representing Unreal Engine 3. The word "Background" is at the top left.](https://kodekloud.com/kk-media/image/upload/v1752874774/notes-assets/images/Exploring-WebAssembly-WASM-Emscripten-Compiler/mozilla-firefox-epic-games-unreal-engine-background.jpg)

Unity joined the movement, announcing “[WebAssembly is here](https://blog.unity.com/technology/webassembly-is-here)” to accelerate game performance on the web.

![The image shows a Unity blog post titled "WebAssembly is here" by Marco Trivellato, featuring a black banner with the WebAssembly logo.](https://kodekloud.com/kk-media/image/upload/v1752874775/notes-assets/images/Exploring-WebAssembly-WASM-Emscripten-Compiler/webassembly-is-here-unity-blog.jpg)

***

## Emscripten in Action

Emscripten powers ports of:

| Category              | Examples                                                                                                                      |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Game Engines          | [Unity](https://unity.com), [Nebula 3](https://github.com/nebula/nebula3), [GeoGram](http://alice.loria.fr/software/geogram)  |
| Graphics Libraries    | [OpenGL ES 2.0](https://www.khronos.org/opengles/2_X), [ImGui](https://github.com/ocornut/imgui)                              |
| Frameworks & Apps     | [PyQt](https://riverbankcomputing.com/software/pyqt), [.NET Blazor](https://dotnet.microsoft.com/apps/aspnet/web-apps/blazor) |
| Utilities & Emulators | Classic emulators, image tools, and more                                                                                      |

![The image is an infographic about Emscripten, showing its applications in game engines, graphics programs, and application frameworks, with examples like Unity, OpenGL ES 2.0, and Python's QT.](https://kodekloud.com/kk-media/image/upload/v1752874776/notes-assets/images/Exploring-WebAssembly-WASM-Emscripten-Compiler/emscriptent-applications-infographic.jpg)

***

## A Closer Look at Emscripten

Emscripten integrates the LLVM toolchain—[Clang](https://clang.llvm.org) and [LLVM](https://llvm.org)—plus Google’s [Closure Compiler](https://developers.google.com/closure/compiler) to output optimized WebAssembly modules and JavaScript glue code.

![The image is a diagram titled "A Bit About Emscripten," showing Emscripten with components Clang, LLVM, and Closure.](https://kodekloud.com/kk-media/image/upload/v1752874777/notes-assets/images/Exploring-WebAssembly-WASM-Emscripten-Compiler/emscripten-diagram-clang-llvm-closure.jpg)

Invoke the frontend `emcc` just like `gcc` or `clang`:

```bash theme={null}
