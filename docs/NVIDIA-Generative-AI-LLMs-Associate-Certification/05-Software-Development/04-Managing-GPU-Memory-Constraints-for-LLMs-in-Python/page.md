# Trip the breaker after 5 failures, reset after 60 seconds
llm_breaker = CircuitBreaker(fail_max=5, reset_timeout=60)

def call_llm_client(prompt: str) -> str:
    """
    Simulated LLM client call. Replace this with your real client invocation,
    e.g., llm_client.predict(prompt) or an HTTP request to the model endpoint.
    """
    # Simulate intermittent failures / latency
    if random.random() < 0.25:
        raise RuntimeError("Transient error from LLM backend")
    return f"LLM response for: {prompt}"

@llm_breaker
def call_llm(prompt: str) -> str:
    return call_llm_client(prompt)

def call_with_fallback(prompt: str) -> str:
    # Basic retry with exponential backoff for transient failures
    max_attempts = 3
    backoff = 0.5
    for attempt in range(1, max_attempts + 1):
        try:
            return call_llm(prompt)
        except CircuitBreakerError:
            # Circuit is open: return fallback immediately
            return "Service temporarily unavailable. Please try again later."
        except Exception as exc:
            # Transient error: retry with backoff
            if attempt == max_attempts:
                return "Could not complete request due to backend errors."
            time.sleep(backoff)
            backoff *= 2

# Example usage
if __name__ == "__main__":
    print(call_with_fallback("Summarize this document..."))
```

For more features and advanced configurations, see the pybreaker project: [https://github.com/danielfm/pybreaker](https://github.com/danielfm/pybreaker)

## Why not the other patterns?

* Decorator pattern: Great for adding behavior (logging, metrics, simple retries), but it doesn't provide the trip/half-open semantics required to isolate a failing service.
* Iterator pattern: Designed for traversal of collections; irrelevant for runtime failure isolation.
* Builder pattern: Used to construct complex objects; not applicable to handling runtime availability or failures.

> **lightbulb** Use the circuit breaker pattern (with sensible thresholds, observability, and fallbacks) to keep LLM deployments resilient and to prevent failures in one component from bringing down the whole system.

- [Watch Video](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/e1d1be4b-e6c9-4b8a-b9a8-9faba13783ff)


# Managing GPU Memory Constraints for LLMs in Python

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/Managing-GPU-Memory-Constraints-for-LLMs-in-Python/page

Strategies to manage GPU memory for large language models in Python, including model parallelism, offloading, reduced precision, quantization, and gradient checkpointing.

Question 11.

When implementing a Python script to load and use a large language model, which approach is most effective for managing GPU memory constraints?

* Loading the entire model at the highest precision possible
* Implementing gradient checkpointing
* Using model parallelism or offloading techniques
* Running exclusively on the CPU

Answer: Using model parallelism or offloading techniques.

<Frame>
  <img alt="The image is a question and answer about managing GPU memory constraints when using a large language model in Python. It highlights model parallelism or offloading techniques as the most effective approach." />
</Frame>

Summary

* Model parallelism and offloading are the most effective techniques to enable deployment of LLMs that exceed a single GPU’s memory capacity.
* Combine sharding/offload with lower precision (FP16/BF16 or quantization) for best results.
* Use gradient checkpointing primarily for training to reduce activation memory at the cost of extra computation.
* CPU-only execution should be a last resort due to large latency and throughput penalties.

Comparison of approaches

| Approach                                     |                                                       Best for | Pros                                                                                                                      | Cons                                                                                    | Typical tooling / notes                                                                 |
| -------------------------------------------- | -------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Model parallelism / Offloading (recommended) | Inference and training of models that exceed single-GPU memory | Distributes parameters/activations across multiple GPUs or swaps rarely-used state to CPU/NVMe; enables very large models | More complex setup and communication overhead                                           | DeepSpeed ZeRO / Offload, PyTorch FSDP, Megatron-LM, FairScale, Hugging Face Accelerate |
| Gradient checkpointing                       |                               Training with limited GPU memory | Reduces activation memory by recomputing activations during backward pass                                                 | Extra computation time; not typically useful for inference                              | PyTorch checkpoint, Hugging Face Trainer options                                        |
| Lower precision (FP16/BF16 / quantization)   |   Both training (mixed precision) and inference (quantization) | Large memory savings and often faster compute on supported hardware                                                       | Quantization can reduce model quality if not calibrated; FP16 requires hardware support | NVIDIA mixed precision, bitsandbytes (8-bit / 4-bit)                                    |
| CPU-only                                     |                                       When no GPU is available | Simplest to run                                                                                                           | Very slow for large models; impractical for latency-sensitive workloads                 | Use only if no GPU options exist                                                        |

Recommended workflow (practical, ordered steps)

1. Try a reduced-precision format first (FP16 / BF16) for inference. This often halves memory usage with minimal accuracy impact on supported hardware.
2. Add model sharding or pipeline/tensor parallelism to split parameters across GPUs.
3. Use offloading to CPU or NVMe for optimizer/state or rarely-used layers when GPU memory is still insufficient.
4. For training, consider gradient checkpointing to reduce activation memory and combine with ZeRO or FSDP to shard optimizer and parameter states.
5. If memory still blocks deployment and performance is non-critical, fall back to CPU-only execution.

Quick examples and references

* DeepSpeed ZeRO Offload: [https://www.deepspeed.ai/](https://www.deepspeed.ai/)
* Hugging Face Accelerate: [https://huggingface.co/docs/accelerate](https://huggingface.co/docs/accelerate)
* PyTorch FSDP: [https://pytorch.org/docs/stable/fsdp.html](https://pytorch.org/docs/stable/fsdp.html)
* Megatron-LM: [https://github.com/NVIDIA/Megatron-LM](https://github.com/NVIDIA/Megatron-LM)
* Quantization & bitsandbytes: [https://github.com/TimDettmers/bitsandbytes](https://github.com/TimDettmers/bitsandbytes)

Example CLI (inference with Hugging Face Accelerate)

```bash theme={null}
