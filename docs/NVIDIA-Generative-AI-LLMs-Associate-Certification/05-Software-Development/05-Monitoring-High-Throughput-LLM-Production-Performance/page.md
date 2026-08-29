# Create an Accelerate config interactively, then run script using multiple GPUs and mixed precision
accelerate config
accelerate launch --multi_gpu --mixed_precision=fp16 my_inference_script.py
```

Example DeepSpeed config snippet (ZeRO Offload)

```json theme={null}
{
  "zero_optimization": {
    "stage": 3,
    "offload_param": {
      "device": "cpu"
    },
    "offload_optimizer": {
      "device": "cpu"
    }
  },
  "fp16": {
    "enabled": true
  }
}
```

When to use each method

* Inference of very large models: prioritize sharding/offload + mixed precision / quantization.
* Training very large models: use ZeRO/FSDP + gradient checkpointing (if activation memory is the bottleneck).
* Prototyping or constrained environments: try quantized weights (8-bit/4-bit) to run on smaller GPUs.
* No GPUs available: CPU-only execution as a fallback (expect significantly slower performance).

<Callout icon="lightbulb">
  For inference of very large models, combine sharding/offload with reduced precision (FP16/BF16 or quantization). For training, add gradient checkpointing if you need further memory savings at the cost of extra computation.
</Callout>

In short: use model parallelism or offloading techniques (optionally combined with lower precision) to manage GPU memory constraints; use gradient checkpointing mainly for training scenarios, and reserve CPU-only execution for situations where GPU-based solutions are unavailable.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/91679a6d-713b-47de-947c-6cb6060819ca" />
</CardGroup>


# Monitoring High Throughput LLM Production Performance

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/Monitoring-High-Throughput-LLM-Production-Performance/page

Explains monitoring high-throughput LLM production performance, recommending tokens per second as the primary metric and offering measurement, optimization, and diagnostic tips

Welcome to this section of the [NVIDIA Generative AI LLMs Associate Certification](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification) — Software Development.

## Question 1

When deploying an LLM for a production application with high-throughput requirements, which of the following is the most important performance metric to monitor?

* GPU memory utilization
* Tokens per second
* Model parameter count
* Cache hit ratio

Answer: Tokens per second

Tokens per second (TPS) is the primary metric for high-throughput LLM applications because it measures the actual serving throughput — how many tokens your system generates or processes per unit time. TPS captures end-to-end behavior (including batching, parallelism, and I/O), and directly maps to capacity planning (concurrent users, requests per second, SLA fulfillment).

Why TPS is the most important metric

* TPS reflects real user-facing throughput and is actionable for scaling and optimization decisions.
* Optimizations that increase TPS (better batching, improved GPU utilization, model parallelism, lower latency per token) directly increase the number of users you can serve.
* TPS captures effects of system-level factors (serializer/deserializer overhead, network latency, and model compute) that individual resource metrics alone do not show.

How to think about the other metrics

* GPU memory utilization: Important for determining fit of model and batch sizes on hardware, preventing OOMs, and guiding quantization or model sharding choices. Indirectly impacts TPS by limiting batch sizes or causing memory thrashing.
* Model parameter count: Describes model capacity and quality, not runtime throughput. Larger models often reduce TPS but may be required for accuracy trade-offs.
* Cache hit ratio: Improves effective throughput for repeated or similar requests by avoiding computation, but it’s workload-dependent. Cache effectiveness should be interpreted together with TPS.

Practical tips to measure and improve TPS

* Measure TPS directly: `TPS = tokens_processed / elapsed_seconds`. Instrument request handlers to emit tokens produced and time taken.
* Use batching: Group multiple requests into a single batch to amortize compute cost per token.
* Optimize model execution: Mixed precision (AMP), model quantization, weight sharding, and inference engines (e.g., NVIDIA Triton) often yield higher TPS.
* Profile end-to-end: Track CPU, GPU, memory, I/O, and network to identify bottlenecks that limit TPS (e.g., small batch sizes, data preprocessing overhead).
* Autoscale based on TPS and latency targets rather than only CPU/GPU utilization.

Comparison table — what to monitor and why

| Metric                 | Why it matters                                                      | How to monitor / optimize                                                                                |
| ---------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Tokens per second      | Direct measure of serving capacity and throughput                   | Instrument requests, emit `tokens_processed` and elapsed time; autoscale or tune batching by TPS targets |
| GPU memory utilization | Determines max model size and feasible batch size                   | NVIDIA DCGM, `nvidia-smi`; use quantization, model sharding, or larger instance types to fit models      |
| Model parameter count  | Indicates capacity/quality of model (not runtime throughput)        | Choose model size based on accuracy/throughput trade-offs; consider distillation or smaller variants     |
| Cache hit ratio        | Reduces compute for repeatable queries and lowers effective latency | Measure hits/misses; tune cache TTL and cache keys; combine cache metrics with TPS to judge benefit      |

<Callout icon="lightbulb">
  Monitor tokens per second as your primary throughput metric, and use GPU memory utilization, cache hit ratio, and latency metrics to diagnose and optimize bottlenecks. Instrument your inference pipeline to emit TPS so autoscaling and optimization are driven by the user-facing capacity metric.
</Callout>

<Frame>
  <img alt="The image contains a question about the most important performance metric to monitor when deploying a large language model (LLM) for high throughput applications, with the answer being &#x22;Tokens per second&#x22; and an explanation provided." />
</Frame>

References and further reading

* NVIDIA Triton Inference Server: [https://developer.nvidia.com/nvidia-triton-inference-server](https://developer.nvidia.com/nvidia-triton-inference-server)
* NVIDIA Data Center GPU Manager (DCGM): [https://developer.nvidia.com/dcgm](https://developer.nvidia.com/dcgm)
* Best practices for serving LLMs and throughput optimization: see vendor docs (Triton, Hugging Face Inference, NVIDIA guides) and profiling tools (nsight, DCGM, Prometheus)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/0348573f-9f82-4248-b999-61907254c60c" />
</CardGroup>
