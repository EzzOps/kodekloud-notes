# Simple division example
2788374 / 71134
# Output: 39.19889223157
```

Before 2017 many sequence models processed tokens sequentially (for example using recurrent neural networks like LSTMs). The transformer architecture (introduced in 2017) changed this by using self-attention, enabling the model to compare tokens across the entire input in parallel. That shift to parallel token processing maps directly to GPU strengths.

> **lightbulb** Transformers process tokens in parallel using self-attention, producing many simultaneous matrix operations — exactly the sort of compute GPUs accelerate.

Because GPUs can execute the required dense linear algebra operations quickly and at scale, they made practical the widespread adoption of large conversational models used in chatbots, voice assistants, and semantic search. GPUs provide the compute density and VRAM bandwidth required to run these models interactively.

Beyond AI: GPUs in science, engineering, and real-time systems
GPUs accelerate many scientific and engineering problems by enabling large-scale parallel computation that turns multi-day or multi-week jobs into interactive or same-day results.

<Frame>
  <img alt="A presenter in a KodeKloud t-shirt gestures beside a slide. The slide shows a CO2/thermometer Earth icon labeled &#x22;Climate Models&#x22; and a &#x22;GPU Applications&#x22; menu listing scientific research, autonomous vehicles, and medical imaging." />
</Frame>

Common GPU-accelerated domains:

* Scientific research: climate simulations, molecular dynamics, and genomics pipelines run far faster using GPU kernels.
* Autonomous vehicles: GPUs perform sensor fusion (camera, LiDAR, radar) and perception inference in real time.
* Medical imaging: accelerated reconstruction and analysis for MRI and CT scans.
* Cybersecurity: rapid anomaly detection across large log datasets.
* Graphics and gaming: real-time rendering, shading, and ray tracing.

Platform teams and DevOps engineers ensure GPU workloads are efficient and cost-effective — handling scheduling, multi-tenant sharing, scaling, and monitoring for both research and production workloads.

<Frame>
  <img alt="A slide showing a &#x22;GPU Efficiency&#x22; bar chart on the left and a cartoon figure labeled &#x22;DevOps Engineers&#x22; in the center. A presenter wearing a black KodeKloud t-shirt stands at the lower right." />
</Frame>

Practical example: CPU and GPU roles while gaming
To see CPUs and GPUs in action, consider running a graphics-intensive game while watching system performance. This demonstrates how work is split across CPU cores and the GPU.

On many systems the CPU workload is shown as multiple separate core graphs (one per core), while GPU usage is shown as a single combined graph. At idle, both CPU and GPU are mostly unused. When the game launches, GPU usage typically jumps immediately.

<Frame>
  <img alt="A split-screen showing system performance graphs (CPU cores and GPU) on the left and a Minecraft game at night on the right. A man wearing a black &#x22;KodeKloud&#x22; t‑shirt stands in the lower-right foreground." />
</Frame>

The GPU spikes because it renders 3D geometry, shading, lighting, and textures in real time. The CPU also gets busier but usually to a lesser extent.

Why is the CPU still active?

* Game logic and AI decision-making
* Physics coordination and collision handling
* Input processing and OS interactions
* Asset streaming, file I/O, and orchestrating data transfers to the GPU

<Frame>
  <img alt="A split-screen screenshot showing CPU and GPU usage graphs on the left and a Minecraft game window on the right. A presenter wearing a KodeKloud t-shirt stands in the lower-right corner." />
</Frame>

When you close the game, both GPU and CPU activity drop quickly as rendering and related tasks stop.

Quick summary: GPU vs CPU at a glance

| Characteristic    |                                                       GPU | CPU                                                  |
| ----------------- | --------------------------------------------------------: | :--------------------------------------------------- |
| Best for          |               Thousands of similar, parallel computations | Complex, branching, low-latency tasks                |
| Architecture      |                Many parallel cores; high memory bandwidth | Few powerful cores; deep pipelines and caches        |
| Typical workloads | Matrix multiplications, image/vision inference, rendering | OS tasks, scheduling, control logic, sequential code |
| Memory            |              High-bandwidth VRAM optimized for throughput | System RAM with lower bandwidth per channel          |
| Examples          |       AI training/inference, scientific kernels, graphics | Game logic, I/O, database coordination               |

Hardware components that matter for GPU workloads:

* Many parallel CUDA/OpenCL cores or tensor cores
* High-bandwidth VRAM for fast data access
* High throughput for compute-intensive kernels

GPUs power a wide range of applications: gaming and real-time graphics, large-scale AI, scientific computing, medical imaging, autonomous systems, and cybersecurity.

Next up: memory and storage
We'll next examine how CPUs and GPUs store, move, and access the data they need — including VRAM, system RAM, caches, and I/O paths.

<Frame>
  <img alt="A stylized 3D illustration of a motherboard with labeled components like CPU, RAM, storage, and ports on a dark background. A person stands on the right wearing a T‑shirt that reads &#x22;KodeKloud.&#x22;" />
</Frame>

Links and references

* Transformer architecture: "Attention Is All You Need" (Vaswani et al., 2017) — [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
* Overview of GPU computing: NVIDIA CUDA documentation — [https://developer.nvidia.com/cuda-zone](https://developer.nvidia.com/cuda-zone)
* GPU use in scientific computing: Examples from climate modeling and genomics research
* Further reading on deep learning and hardware acceleration: common ML/AI textbooks and vendor guides

- [Watch Video](https://learn.kodekloud.com/user/courses/computer-architecture/module/e3c31d19-97a9-464e-b94f-5ff231dc9677/lesson/6910a132-0863-41bd-8764-43e3dc133f04)


# GPU Architecture

Source: https://notes.kodekloud.com/docs/Computer-Architecture/Graphics-Processing-Unit-GPU/GPU-Architecture/page

Explains GPU architecture differences from CPUs and how cores, memory, clock speed, and specialized units affect AI training and inference performance and efficiency

Welcome back. In the previous section you rolled out laptops across your company. Now your R\&D team is building an internal chatbot (think ChatGPT trained on company data). Training that model is painfully slow on CPUs alone—it's like trying to read a library one page at a time. To accelerate training we need to run thousands of calculations in parallel, which is exactly what GPUs are designed to do.

In this lesson you'll learn:

* What architectural differences make GPUs better for certain workloads than CPUs.
* How GPU performance depends on core structure, clock speed, and memory.
* Which GPU features matter for AI training and inference.

<Frame>
  <img alt="A stylized, purple-themed diagram of a computer motherboard highlighting components like the GPU, CPU, RAM and ports. A presenter wearing a &#x22;KodeKloud&#x22; shirt stands at the right and a small cartoon cat character appears at the lower left." />
</Frame>

High-level comparison: CPUs versus GPUs

* CPU: A few powerful cores optimized for complex, branching, single-threaded or moderately parallel tasks.
* GPU: Thousands of simpler cores optimized for performing the same operation over large data sets in parallel.

The GPU approach—massive parallelism—matches workloads such as rendering pixels, applying shaders across vertices, and dense matrix math in machine learning. For deep learning, GPUs can run thousands of arithmetic operations at once, reducing training time from days to hours compared to CPU-only training.

<Frame>
  <img alt="A dark purple presentation slide titled &#x22;Compare GPUs and CPUs&#x22; with bullet headings like Architecture, Processing Model, Workloads, and a second point about how GPU performance is influenced by various factors. A cartoon cat is on the left and a presenter wearing a KodeKloud T‑shirt stands on the right." />
</Frame>

Why thousands of cores?

GPUs organize their many cores into clusters—often called streaming multiprocessors (NVIDIA) or compute units (AMD). These clusters let teams of cores work in lockstep, increasing throughput and reducing coordination overhead. Imagine a factory: teams specialize in packaging, assembly, and quality checks; the coordinated teams achieve far higher throughput than the same number of lone workers.

<Frame>
  <img alt="A stylized infographic comparing a GPU (shown with many small gradient squares and labeled &#x22;1,000+ Cores&#x22;) to a CPU (eight larger gradient blocks labeled &#x22;8 Cores&#x22;). A presenter wearing a KodeKloud t-shirt stands at the right against a dark, tech-themed background." />
</Frame>

<Frame>
  <img alt="A presenter in a black &#x22;KodeKloud&#x22; T-shirt stands at the right speaking with hands clasped. To the left is a purple-themed infographic showing a factory scene and a GPU cluster grid labeled &#x22;AI Training&#x22; with panels for Team A (Packaging), Team B (Assembling), and Team C (Quality Checking)." />
</Frame>

Specialized AI hardware

Many modern GPUs include dedicated accelerators—tensor cores, matrix cores, or vendor-specific AI units—designed for dense matrix operations and mixed-precision math (FP16, BF16). These units dramatically increase throughput for neural-network operations. A training job that takes many hours on a general-purpose GPU can finish in a fraction of that time on a GPU with specialized AI cores.

<Frame>
  <img alt="A dark tech-themed slide showing a glowing purple-pink 3x3 cube icon with buttons labeled &#x22;Tensor Core&#x22; and &#x22;Matrix Core&#x22; and a &#x22;Specialized Cores&#x22; banner. A presenter wearing a black KodeKloud T‑shirt appears at the right, speaking and gesturing." />
</Frame>

Memory and data movement: VRAM matters

GPU cores only run as fast as they can get data. Video RAM (VRAM) is high-bandwidth memory attached directly to the GPU and stores textures, frame buffers, or large matrices for ML. Two key properties:

* Capacity: how large a model or batch you can store on-device.
* Bandwidth: how fast data moves between VRAM and compute cores.

> **lightbulb** VRAM capacity and bandwidth are crucial for AI workloads: capacity limits the size of models and batch sizes you can process, while bandwidth reduces stalls by keeping compute units fed. Running out of VRAM forces data transfers or smaller batches, which slow training.

<Frame>
  <img alt="A presentation slide illustrating GPU and Video RAM with a traffic-lane analogy for low vs. high bandwidth on the left and a grid of GPU blocks on the right. A presenter stands at the lower-right corner explaining the diagram." />
</Frame>

Clock speed vs parallelism

GPUs typically run at lower per-core clock speeds than CPUs (for example, `2.5 GHz` vs `5 GHz`), but they compensate by having orders of magnitude more cores. Think of a race car (`high single-thread speed`) versus a freight train (`lots of throughput`). GPU designs prioritize total operations per second over single-thread latency.

<Frame>
  <img alt="A dark presentation slide showing stylized, colorful GPU and CPU icons with callouts reading &#x22;2.5GHz 16,000 GPU Cores&#x22; and &#x22;5GHz 16 Cores&#x22; under a &#x22;Clock Speed&#x22; banner. A man wearing a KodeKloud T‑shirt stands at the right as if presenting." />
</Frame>

Power and efficiency

High-performance GPUs can draw hundreds of watts. Data centers running continuous AI workloads must account for power delivery and cooling. Modern GPU architectures emphasize performance-per-watt with dynamic boost clocks and power scaling to improve cost efficiency.

> **warning** High-performance GPUs require adequate cooling and power. When planning for continuous AI training, include power consumption and data-center cooling in hardware selection and total cost calculations.

<Frame>
  <img alt="A presenter wearing a KodeKloud t-shirt stands beside a slide. The slide compares &#x22;High-Performance GPU&#x22; and &#x22;Modern GPU&#x22; with colorful cube illustrations and notes about power, performance-per-watt, and dynamic power scaling." />
</Frame>

Quick comparison table

| Feature           |                                                    CPU | GPU                                                         |
| ----------------- | -----------------------------------------------------: | ----------------------------------------------------------- |
| Cores             | Few, powerful cores optimized for complex control flow | Thousands of simpler cores optimized for parallel workloads |
| Processing model  |                  Serial / branching tasks, low latency | SIMD / SIMT parallelism, high throughput                    |
| Specialized units |                    Vector units, general-purpose cores | Tensor/matrix cores for AI acceleration                     |
| Memory            |                           System RAM (lower bandwidth) | High-bandwidth VRAM (higher throughput)                     |
| Clock speed       |                    Higher per-core clocks (`~3–5 GHz`) | Lower per-core clocks (`~1–3 GHz`) but many cores           |
| Energy            |  Optimized for response latency and single-thread perf | Performance-per-watt focus; can draw high total power       |

<Frame>
  <img alt="A presentation slide showing a table that compares CPU and GPU features (cores, processing model, VRAM, clock speed, energy efficiency). A person wearing a black &#x22;KodeKloud&#x22; t-shirt stands at the right side of the image." />
</Frame>

Choosing the right GPU for AI

When selecting GPUs for training or inference, weigh:

* VRAM capacity: large models and big batch sizes require more memory.
* Memory bandwidth: reduces stalls and speeds up compute.
* Specialized cores: tensor/matrix cores accelerate common NN ops.
* Power and cooling: ensure infrastructure can support continuous loads.
* Price vs performance: the most expensive GPU isn’t always the best fit—consider workload characteristics (training, inference, or graphics) and cost efficiency.

References and further reading

* [NVIDIA CUDA Documentation](https://developer.nvidia.com/cuda-zone)
* [NVIDIA Tensor Cores overview](https://developer.nvidia.com/tensorcores)
* [AMD GPU Architecture](https://www.amd.com/en/technologies/graphics-architecture)
* [Deep Learning & Mixed Precision Training](https://arxiv.org/abs/1710.03740)

Now that you understand GPU architecture and how it differs from CPUs, you’re better equipped to pick hardware for AI training, inference, or graphics workloads.

- [Watch Video](https://learn.kodekloud.com/user/courses/computer-architecture/module/e3c31d19-97a9-464e-b94f-5ff231dc9677/lesson/4e354eef-e308-46e6-aca0-5ff0325d8743)
