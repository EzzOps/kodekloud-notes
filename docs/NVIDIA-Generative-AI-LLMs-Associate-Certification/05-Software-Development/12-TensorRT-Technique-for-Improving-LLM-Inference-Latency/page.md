# TensorRT Technique for Improving LLM Inference Latency

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/TensorRT-Technique-for-Improving-LLM-Inference-Latency/page

Describes using TensorRT INT8 quantization to reduce LLM inference latency with minimal accuracy loss, covering calibration, mixed precision fallbacks, workflow steps, and comparisons to other optimizations

Question 3.

Which TensorRT technique is most effective for improving inference latency of LLMs without significant loss in accuracy?

INT8 quantization, model pruning, layer fusion, or knowledge distillation?

Answer: INT8 quantization.

INT8 quantization is the most effective and widely adopted technique for reducing LLM inference latency while maintaining acceptable accuracy. By lowering numeric precision from FP32/FP16 to 8-bit integers, INT8 reduces memory bandwidth and increases arithmetic throughput on supported hardware (notably NVIDIA GPUs with Tensor Cores and dedicated INT8 kernels). When applied with proper calibration or quantization-aware training (QAT), INT8 commonly delivers substantial latency and throughput improvements with minimal model-quality degradation.

Why INT8 works

* Precision reduction (FP32/FP16 → INT8) reduces memory footprint and memory traffic, which is frequently the bottleneck in LLM inference.
* On modern GPUs, INT8 kernels can execute more operations per cycle and leverage specialized instructions for higher throughput.
* Using per-channel quantization and representative calibration data minimizes precision loss across layers.

How INT8 achieves lower latency

* Smaller data types reduce cache/memory transfers.
* INT8 arithmetic increases compute density and uses optimized kernels.
* Mixed-precision fallback (keeping some ops in FP16/FP32) prevents accuracy degradation for sensitive operators.

Typical workflow with TensorRT

1. Export or convert the model to an intermediate format such as ONNX or SavedModel.
2. Create a TensorRT builder and enable INT8 in the builder configuration.
3. Provide a representative calibration dataset for post-training static quantization, or use QAT if needed.
4. Build the TensorRT engine and validate generation quality. If accuracy drops, selectively keep sensitive layers in FP16/FP32 (mixed precision) or use QAT.

Example: enabling INT8 in a TensorRT build (Python)

```python theme={null}
import tensorrt as trt

logger = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(logger)
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
config = builder.create_builder_config()
config.max_workspace_size = 1 << 30  # 1 GB workspace
