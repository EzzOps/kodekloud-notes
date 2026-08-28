# Demo NVIDIA Architecture and Ollama

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Introduction/Demo-NVIDIA-Architecture-and-Ollama/page

Guide for running local LLM inference on a Linux host with a discrete NVIDIA GPU, covering VRAM architecture, monitoring with nvidia-smi and htop, and cloud provisioning considerations

This guide explains how to run local LLM inference on a discrete NVIDIA GPU in a Linux host, using an Arch Linux test machine with an NVIDIA GeForce RTX 4090 and 64 GB of system RAM as the concrete example. It covers the hardware memory model differences, how to monitor the GPU with `nvidia-smi`, system monitoring with `htop`, and cloud/provisioning considerations for GPU workloads.

## System summary (neofetch)

A representative neofetch output from the example system:

`````````````````````bash theme={null}
[jeremy@crashbox ~]$ neofetch
               .-/+oossssoo+/-.              
           `:+sssssssssssssssssssssso+:`          
         -+sssssssssssssssssssssssssssss+-        
       .ossssssssssssssssssssssssssssssssssso.      
      /sssssssssssssssssssssssssssssssssssssss/     
     /[SECRET_REDACTED]/    
    /sssssssssso-````````````````````-ossssssssss/    
   /ssssssssss/                  `-sssssssssss/   
   /ssssssssss:                   /ssssssssss/    
    /ssssssssssso.            .ossssssssssssss/     
     /ssssssssssssssso+--+osssssssssssssssssss/      
       /sssssssssssssssssssssssssssssssssss/        
         -+sssssssssssssssssssssssssss+-          
           `:+sssssssssssssssssssssso+:`          
               .-/+oossssoo+/-.              

jeremy@crashbox
-----------------
OS: Arch Linux x86_64
Host: MS-7A95 1.0
Kernel: 6.16.8-arch3-1
Uptime: 39 mins
Packages: 798 (pacman)
Shell: bash 5.3.3
Resolution: 1920x1080
Terminal: /dev/pts/1
CPU: Intel i9-9920X (24) @ 4.700GHz
GPU: NVIDIA GeForce RTX 4090
Memory: 3100MiB / 63943MiB
`````````````````````

## Important architectural note

<Callout icon="warning">
  Discrete NVIDIA GPUs have dedicated VRAM that is separate from system RAM. Unlike Apple Silicon’s unified memory, discrete GPUs cannot transparently page model memory between system RAM and GPU VRAM. If a model requires more VRAM than the GPU provides (24 GB for an RTX 4090 in this example), it will usually fail to load unless you use model-specific sharding or offloading strategies.
</Callout>

## Tip: model selection and performance

<Callout icon="lightbulb">
  For RTX 4090-class GPUs you can typically run models that fit within \~22–24 GB of VRAM. Models that fit will often perform substantially faster than on many Apple M-series chips. When choosing models, check their VRAM footprint for the batch sizes and sequence lengths you plan to use.
</Callout>

## Monitoring the GPU with nvidia-smi

NVIDIA ships `nvidia-smi` to inspect driver and CUDA versions, VRAM usage, power/temperature, and running GPU processes. Use it to verify drivers are installed correctly and to see which processes consume VRAM.

Example invocation and sample output:

```bash theme={null}
[jeremy@crashbox ~]$ nvidia-smi
Wed Oct  1 22:59:23 2025
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 580.82.09    Driver Version: 580.82.09    CUDA Version: 13.0     |
+-----------------------------------------------------------------------------+
| GPU  Name               Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap| Memory-Usage      | GPU-Util  Compute M.  MIG M. |
|===========================================================================================|
|   0  NVIDIA GeForce RTX 4090   Off  | 00000000:65:00.0  Off |  0%   31C    P8   15W / 450W |
|                               |  3555MiB / 24576MiB          |    0%        Default         |
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   PID   Type   Process name                          GPU Memory Usage     |
|=============================================================================|
|   0    878    G     /usr/lib/Xorg                               72MiB         |
|   0    938    C     .../stable-diffusion-webui/venv/bin/python   3052MiB       |
|   0   1167    C     .../comfyui/venv/bin/python                  386MiB       |
+-----------------------------------------------------------------------------+
```

What to inspect in `nvidia-smi`

* Driver Version and CUDA Version — required for many CUDA libraries and PyTorch/CUDA compatibility.
* Fan/Temp/Power and GPU Util — indicates idle vs heavy load.
* Memory-Usage — shows VRAM usage per GPU; if a model exceeds total VRAM it will not load.
* Processes — lists which processes use the GPU and how much VRAM they hold.

Quick reference table — nvidia-smi fields

| Field                         | Meaning                                                     |
| ----------------------------- | ----------------------------------------------------------- |
| Driver Version / CUDA Version | Compatibility requirements for CUDA-based frameworks        |
| Fan / Temp / Power            | Thermal and power telemetry to detect heavy workloads       |
| Memory-Usage                  | VRAM allocation: used / total (important for model fitting) |
| GPU-Util                      | Percent utilization of the GPU compute engines              |
| Processes                     | Active GPU processes and per-process VRAM consumption       |

## Monitoring CPU and system processes

For host-level resource monitoring (CPU, system RAM, threads), `htop` or `top` are useful. Use them alongside `nvidia-smi` to correlate VRAM usage with system memory pressure.

Sample trimmed `htop` output:

```bash theme={null}
Tasks: 342 total, 1 running, 341 sleeping
%Cpu(s):  0.1 us,  0.0 sy,  99.9 id
MiB Mem : 63943.5 total, 53635.0 free, 3749.2 used, 7245.8 buff/cache
PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
 938 jeremy    20   0   16.0g   1.3g   257M S   0.7  2.1  39:39.99 python
4555 jeremy    20   0   11156   7808   5636 R   0.3  0.0   0:00.02 top
  1 root      20   0   22964  13648   9824 S   0.0  0.0   0:00.87 systemd
```

## Cloud and provisioning considerations

* Most cloud GPU offerings use NVIDIA hardware; the management plane typically abstracts the host OS. For GPU-heavy LLM work, NVIDIA instances are the common choice.
* If you need Apple Silicon specifically, some cloud providers expose macOS instances, but they are less common for GPU workloads.
* Memory rules described here apply across frameworks: Ollama, Hugging Face Transformers, `llama.cpp`, LM Studio, and various Llama frontends. If a model's VRAM requirement exceeds the GPU, you must use model sharding, tensor offloading, or other model-parallel strategies.

Comparison: Discrete NVIDIA GPU vs Apple M-series memory

| Characteristic                    | Discrete NVIDIA GPU (e.g., RTX 4090)                             | Apple M-series (unified memory)                                                |
| --------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Memory type                       | Dedicated VRAM (e.g., 24 GB)                                     | Unified system/GPU memory (varies by model)                                    |
| Paging between RAM and VRAM       | Not transparent; model must fit VRAM or support sharding/offload | Unified memory and swap can allow larger models to run (with performance cost) |
| Typical outcome if model > memory | Usually fails to load without sharding                           | May run slowly using unified memory & swap                                     |
| Best use case                     | High-performance inference for models that fit VRAM              | Flexible development and smaller models; good integration on Apple devices     |

Summary — key takeaways

* Discrete NVIDIA GPUs have isolated VRAM; a model must fit within that VRAM (roughly 24 GB on an RTX 4090) unless you use sharding/offloading.
* The RTX 4090 can deliver much faster inference for models that fit its VRAM compared to many M-series chips.
* Use `nvidia-smi` to check driver/CUDA versions, VRAM usage, power/temperature, and active GPU processes; use `htop`/`top` for system CPU and RAM monitoring.
* These principles apply across local LLM frameworks like Ollama, Hugging Face Transformers, `llama.cpp`, and LM Studio.

Links and references

* [Ollama course — Running local LLMs with Ollama](https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama)
* [Hugging Face Transformers documentation](https://huggingface.co/docs/transformers)
* [llama.cpp repository](https://github.com/ggerganov/llama.cpp)
* [LM Studio](https://lmstudio.ai/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/18c192ac-9730-42f7-9dbf-6c67f9ceeb61/lesson/52d89767-85d3-4061-bf98-6bec94541f3a" />
</CardGroup>
