# GPU Applications

Source: https://notes.kodekloud.com/docs/Computer-Architecture/Graphics-Processing-Unit-GPU/GPU-Applications/page

How GPUs accelerate AI, graphics, and scientific workloads by parallelizing large matrix computations, contrasted with CPU roles, and practical uses in gaming, research, medical imaging, and autonomous systems.

When your phone suggests the next word as you type, it uses short, local patterns computed on-device. Modern large language models (LLMs) do something far more extensive: they analyze whole sentences, context, and statistical relationships across billions of words to generate coherent text.

<Frame>
  <img alt="Two smartphone UI mockups are shown side-by-side — the left illustrating predictive text suggestions in a messaging app and the right displaying a ChatGPT-style response about dark matter. A presenter wearing a KodeKloud t-shirt stands to the right of the mockups." />
</Frame>

Your phone handles short-pattern predictions locally and sequentially. LLMs must process massive datasets and perform trillions of numerical operations to learn language structure and generate responses. That scale is why GPU hardware is central to modern AI.

Why not rely only on CPUs? Consider this analogy:

* A CPU is like a careful reader flipping through a dictionary entry by entry — excellent at complex, branching logic and low-latency tasks.
* A GPU is like thousands of eyes scanning many pages in parallel — optimized for carrying out many similar calculations at once.

AI training and inference depend heavily on linear algebra (large matrix multiplications and tensor operations). GPUs are architected for massive parallelism and high memory bandwidth, making them far faster than CPUs for these workloads. Training a model on CPUs would be impractically slow: days or weeks on GPUs could become months or years on CPUs.

Here’s a tiny numeric example resembling an isolated operation that’s part of much larger matrix computations during training or evaluation:

```python theme={null}
