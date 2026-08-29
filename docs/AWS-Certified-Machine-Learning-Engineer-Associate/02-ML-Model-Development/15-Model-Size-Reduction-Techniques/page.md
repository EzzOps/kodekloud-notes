# Model Size Reduction Techniques

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Model-Size-Reduction-Techniques/page

Methods to reduce large language model size and optimize deployments using pruning, quantization, distillation, and low-rank factorization for edge, mobile, and low-resource environments.

Modern large language models (LLMs) can exceed one trillion parameters and often need dozens to hundreds of GPUs to run efficiently. Many target platforms—phones, IoT devices, drones, and wearables—have limited memory, compute power, and energy. This article explains why model size reduction matters, the most common techniques for compressing models, and how to select and validate methods that fit your deployment constraints.

<Frame>
  <img alt="The image lists scenarios that need size reduction, including phones, IoT devices, drones, and wearables, with a focus on limited memory." />
</Frame>

Why model size reduction matters

* Reduced memory footprint: Fit models on-device or into smaller cloud instances.
* Faster inference: Lower compute cost and reduced latency for real-time applications.
* Lower infrastructure cost: Smaller models reduce CPU/GPU time and energy consumption.
* Offline usage: Enable functionality without persistent network connectivity.
* Easier distribution and updates: Smaller artifacts are faster to transfer and deploy.

Because large models require more computation, they often produce slower predictions. Latency is critical for many real-time applications—on-device AR, robotics, and mobile assistants—so compressing and optimizing models is essential.

<Frame>
  <img alt="The image illustrates a comparison between large and small models, highlighting that large models have slower predictions while small models have faster predictions." />
</Frame>

Common deployment motivations

* Deploy to edge and mobile devices
* Improve inference throughput and latency
* Reduce cloud infrastructure cost
* Support offline/low-bandwidth scenarios
* Accelerate fine-tuning and iterative development

<Frame>
  <img alt="The image presents four reasons for reducing model size: deployment on edge and mobile devices, faster inference time, reduced infrastructure cost, and offline usage." />
</Frame>

Overview of popular model-reduction techniques

* Pruning
* Quantization
* Knowledge distillation
* Low-rank factorization

<Frame>
  <img alt="The image lists four popular model reduction techniques: pruning, quantization, knowledge distillation, and low-rank factorization." />
</Frame>

Pruning
Pruning removes redundant or low-importance weights, neurons, or filters from a network to reduce parameter count and computation. Typical pruning strategies include:

* Magnitude pruning: drop small-magnitude weights.
* Structured pruning: remove entire neurons, channels, or filters for hardware-friendly sparsity.
* Iterative pruning and retraining: prune gradually and fine-tune to recover accuracy.

Pruning usually reduces both storage and runtime cost, but it commonly requires a fine-tuning step to regain performance.

<Frame>
  <img alt="The image shows a comparison between a neural network model and its pruned version, illustrating how pruning reduces the number of connections and nodes." />
</Frame>

Quantization
Quantization reduces numerical precision of model weights and/or activations, shrinking model size and often speeding up inference on CPUs, some GPUs, and accelerators.

Common quantization options:

* FP16 (half precision): often minimal accuracy loss, widely used on GPUs.
* INT8 (8-bit integer): much smaller footprint and faster CPU inference; often needs calibration or quantization-aware training.
* Dynamic (post-training) quantization: convert weights on the fly with no calibration data.
* Static (calibrated) quantization: uses calibration dataset to determine ranges.
* Quantization-aware training (QAT): simulates quantization during training to preserve accuracy.

Always evaluate post-quantization accuracy and latency on the target hardware.

<Frame>
  <img alt="The image illustrates the concept of quantization in neural networks, showing a comparison between a regular model and a quantized model with simplified numerical values." />
</Frame>

Knowledge distillation
Knowledge distillation transfers behavior from a large (teacher) model to a smaller (student) model. Instead of training the student purely on hard labels, the student learns to match the teacher’s soft output distributions—this can encode richer information about class similarities and calibration.

Key points:

* Can produce compact models that retain much of the teacher’s capability.
* Often combines distillation loss with label loss.
* Commonly used for both classification and generative tasks.
* Requires additional training of the student model.

<Frame>
  <img alt="The image illustrates a knowledge distillation process, showing input data being fed into a teacher model and a smaller student model with a loss function to optimize the training." />
</Frame>

Low-rank factorization
Low-rank factorization approximates large weight matrices as products of smaller matrices to reduce both storage and multiply-add cost. For a matrix A (m × n), approximate:

A ≈ U (m × k) × V (k × n) with k \< min(m, n).

Choosing k trades off accuracy vs. parameter count. A common approach to compute a low-rank approximation is truncated singular value decomposition (SVD).

Example using NumPy:

```python theme={null}
import numpy as np
