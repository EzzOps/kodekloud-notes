# Demo Apple Silicon and Ollama

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Introduction/Demo-Apple-Silicon-and-Ollama/page

How Apple Silicon unified memory and memory‑mapping enable running larger local LLMs with Ollama, explaining performance trade offs, tooling, and practical testing advice

In this lesson we explain what you need to know about running Ollama and similar local LLM runtimes (for example the [Transformers library](https://huggingface.co/docs/transformers) or [LM Studio](https://lmstudio.ai)) on Apple Silicon Macs. You’ll learn how Apple’s unified memory model enables running larger models locally via memory-mapping, where the trade-offs are compared to using an NVIDIA GPU, and what to watch for when testing models locally.

Here’s a sample system summary from an M2 Ultra machine used throughout this lesson:

```plaintext theme={null}
jeremy@MACSTUDIO.local
------------------------
OS: macOS 14.6 23G80 arm64
Host: Mac14,14
Kernel: 23.6.0
Uptime: 11 mins
Packages: 135 (brew)
Shell: zsh 5.9
Resolution: 3440x1440
DE: Aqua
WM: Quartz Compositor
WM Theme: Blue (Dark)
Terminal: /dev/ttys001
CPU: Apple M2 Ultra
GPU: Apple M2 Ultra
Memory: 3285MiB / 131072MiB
```

## Unified memory on Apple Silicon

Apple’s M-series chips (M1 — M4) use a unified memory architecture: CPU, GPU, and other accelerators share the same physical memory pool. This allows model runtimes to memory-map model files from disk into the single address space and bring pages into RAM on demand, which can make it possible to run larger models than would fit entirely in a discrete GPU’s VRAM.

<Frame>
  <img alt="The image is a diagram illustrating &#x22;Unified Memory on Mac,&#x22; showing 128 GB of unified memory distributed to both the CPU and GPU." />
</Frame>

## How Ollama and memory-mapping work

Runtimes like Ollama often use memory-mapped files (`mmap`) to access model weights on disk. Instead of loading the entire model into VRAM up front, the runtime maps the model file into the process address space and the OS pulls pages into unified memory only as they are needed. This reduces upfront RAM pressure and lets the system host models larger than available GPU VRAM—at the cost of potential page faults and higher latency when accessing unmapped pages.

* Small models: most pages are touched quickly and performance is good for interactive use.
* Large models: more pages are touched, increasing page faults and potential pauses as the OS reads from disk.

<Frame>
  <img alt="The image illustrates &#x22;OLLAMA Memory Mapping,&#x22; showing a model on disk using a small part of RAM, with small LLM usage." />
</Frame>

## Why Macs can run some larger models than a single GPU

A discrete GPU (for example an NVIDIA 4090) has a fixed VRAM size (e.g., 24 GB). If a model’s working set exceeds that VRAM, you need model parallelism, offloading, or external memory techniques. On an M-series Mac with, say, 128 GB of unified memory, the OS can map many more pages into the process address space. That makes it possible to run models locally that would otherwise not fit entirely on a single GPU.

<Frame>
  <img alt="The image highlights the unified memory advantage of the MacBook Pro, stating that its 32-GB unified memory can run larger models than a 24-GB VRAM." />
</Frame>

## Performance trade-offs: latency, bandwidth, and compute

Unified memory capacity is a practical advantage, but there are important trade-offs that affect latency and throughput:

* Memory capacity: Macs can provide a much larger addressable RAM pool than a single GPU’s VRAM.
* Bandwidth & latency: Dedicated GPU memory (GDDR/HBM) typically offers higher bandwidth and lower latency for GPU-bound workloads.
* Compute and software: NVIDIA GPUs benefit from CUDA-optimized libraries and high GPU FLOPs. Apple Silicon has strong CPU cores, GPUs, and ML accelerators (Neural Engine and M-series improvements), but raw GPU throughput and CUDA ecosystem advantages often favor NVIDIA for high-throughput GPU workloads.

Platform trade-off summary:

| Aspect                  |                                                        Apple Silicon (Unified Memory) |                                 NVIDIA GPU (Discrete VRAM) |
| ----------------------- | ------------------------------------------------------------------------------------: | ---------------------------------------------------------: |
| Addressable memory      |                                                  Larger single pool (e.g., 64–192 GB) |                           Limited by VRAM (e.g., 24–48 GB) |
| Bandwidth / latency     |                          Lower bandwidth for some GPU ops; higher latency when paging |              Higher bandwidth (GDDR/HBM) and lower latency |
| Ecosystem optimizations |                                                  Metal / MPS, native Apple toolchains |                CUDA, cuBLAS, optimized inference libraries |
| Typical best use        | Large models that need more addressable memory; CPU/ML accelerator-friendly workloads | High-throughput, low-latency GPU compute; multi-GPU setups |

<Frame>
  <img alt="The image compares Mac's unified memory, highlighting its large size and slower speed, and impressive M4 + AI chip, with NVIDIA's video memory, emphasizing its faster speed, optimization, and greater processing power." />
</Frame>

## Practical implications

* Large models (tens to hundreds of billions of parameters): On a Mac with abundant unified memory you may be able to run models that can’t fit on a single GPU VRAM. Expect slower performance and possible unresponsiveness when the OS must page heavily.
* Interactive workloads: Smaller models and well-optimized M-series runtimes often deliver excellent interactive performance on Macs.
* Production/high-throughput: For the lowest latency and best throughput for GPU-heavy inference, multi-GPU NVIDIA servers or cloud GPU instances are typically superior.

<Frame>
  <img alt="The image illustrates the comparison of running large language models (70B-100B parameters) on Mac using unified memory and on NVIDIA using video memory, highlighting the advantages and limitations of each." />
</Frame>

## Tool availability and compatibility

Support and performance vary across tools and frameworks:

* CUDA-only optimizations target NVIDIA hardware and won’t run on macOS without alternative backends.
* Some frameworks provide Metal/MPS backends or Apple Silicon builds (for example certain [PyTorch MPS builds](https://pytorch.org/docs/stable/notes/mps.html)).
* Ollama and other optimized runtimes may offer native Apple Silicon performance benefits; always check the runtime docs and community reports for platform-specific instructions and limitations.

When choosing a platform:

* Verify that your chosen model and runtime support Metal/MPS or have Apple Silicon optimizations.
* Test early on your target hardware—some models or operators may fall back to slower implementations on macOS.

<Frame>
  <img alt="The image outlines tool limitations on Mac, highlighting issues with AI tool compatibility and performance, while noting that Macs perform well with specific models like Big Giant Huge and Ollama." />
</Frame>

## Monitoring and diagnostics

Use system monitoring tools to measure memory, CPU, GPU, and I/O while running models:

* macOS Activity Monitor (GUI)
* Command-line: `htop`, `vm_stat`, `top`, and `sudo dtrace`-style utilities
* Ollama or runtime logs for model load times and page faults

<Callout icon="lightbulb">
  Monitor memory and CPU/GPU usage while testing a model. Large models mapped from disk may look feasible but can become unresponsive if the working set causes extensive paging or swapping.
</Callout>

<Callout icon="warning">
  If you see sustained high paging activity or the app becomes unresponsive, stop the run and test with a smaller model or increase available memory. Paging can severely degrade interactivity.
</Callout>

## Summary

* Apple Silicon’s unified memory lets you memory-map model files and run models that might not fit into a single GPU’s VRAM.
* This increases the addressable memory available for models but introduces trade-offs in bandwidth, latency, and overall GPU compute performance.
* Choose your platform based on the model sizes, runtimes, and latency/throughput needs: Macs are excellent for certain local workloads and convenience; NVIDIA multi-GPU setups are often better for raw GPU throughput.

Links and references

* [Ollama](https://ollama.com)
* [Transformers — Hugging Face](https://huggingface.co/docs/transformers)
* [LM Studio](https://lmstudio.ai)
* [PyTorch MPS notes](https://pytorch.org/docs/stable/notes/mps.html)
* [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)

A stray path from the original recording (kept here for completeness):

```plaintext theme={null}
/Applications/Utilities/Adobe Creative Cloud/ACC/Creative
```

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/18c192ac-9730-42f7-9dbf-6c67f9ceeb61/lesson/b6067c9e-0bac-4c98-98be-cd3a93a1f3d4" />
</CardGroup>
