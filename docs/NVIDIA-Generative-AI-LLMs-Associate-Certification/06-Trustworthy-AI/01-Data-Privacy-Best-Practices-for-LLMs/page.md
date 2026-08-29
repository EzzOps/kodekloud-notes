# Enable INT8 mode
config.set_flag(trt.BuilderFlag.INT8)

# Attach an INT8 calibrator implementation (must implement TensorRT calibrator interface)
# calibrator = MyCalibrator(calibration_cache="calib.cache")
# Build engine (network must be populated)
# engine = builder.build_engine(network, config)
```

Note: A calibrator is required for post-training static INT8 quantization unless you use QAT. Replace `MyCalibrator` with your calibrator implementation or use TensorRT utilities that provide calibrators.

Important considerations when using INT8

* The calibration dataset must be representative of inference inputs (token distributions, sequence lengths, etc.).
* Some layers/operators are more sensitive to quantization; leave those in FP16/FP32 if necessary (mixed precision).
* Generation tasks with rare tokens or long-range dependencies may require more careful calibration or QAT to maintain quality.
* Measure generation quality (e.g., perplexity, BLEU, human evaluation) and latency/throughput to validate trade-offs.

Comparison with other optimization techniques

| Technique              | Primary benefit                                           | Typical cost/effort                                                        | When to use                                                               |
| ---------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| INT8 quantization      | Large latency and throughput improvements on supported hw | Requires calibration or QAT; may need mixed-precision fallbacks            | First choice for latency gains with minimal accuracy loss                 |
| Layer fusion           | Reduces kernel launches and memory passes                 | Low effort when supported by framework; modest gains for very large LLMs   | Complementary optimization                                                |
| Model pruning          | Lowers compute and model size                             | Often needs retraining or fine-tuning; risk of accuracy drop if aggressive | Use if compute budget or memory footprint must shrink beyond quantization |
| Knowledge distillation | Produces smaller, faster student models                   | Requires retraining; time-consuming; may change behavior/features          | When you can train a student model and accept behavioral differences      |

Practical recommendations

* Start with INT8 quantization using a representative calibration dataset and validate generation outputs.
* Use TensorRT engine-building best practices: export a stable ONNX/SavedModel, enable INT8 with a calibrator, and test mixed-precision fallbacks.
* Apply layer fusion and other graph-level optimizations as complementary steps.
* Consider pruning or distillation only when you need additional size or latency reductions and can invest in retraining.

References

* TensorRT: [https://developer.nvidia.com/tensorrt](https://developer.nvidia.com/tensorrt)
* NVIDIA Tensor Cores: [https://developer.nvidia.com/tensor-cores](https://developer.nvidia.com/tensor-cores)
* ONNX: [https://onnx.ai/](https://onnx.ai/)
* SavedModel: [https://www.tensorflow.org/guide/saved\_model](https://www.tensorflow.org/guide/saved_model)
* Quantization-aware training (QAT) guide: [https://www.tensorflow.org/model\_optimization/guide/quantization/training](https://www.tensorflow.org/model_optimization/guide/quantization/training)

> **lightbulb** Use a representative calibration dataset and validate generation quality after quantization. If specific layers degrade significantly under INT8, consider mixed-precision (INT8 + FP16) or QAT for those layers.

- [Watch Video](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/928a084f-42c4-495d-a079-aef1bfca417a)


# Data Privacy Best Practices for LLMs

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Trustworthy-AI/Data-Privacy-Best-Practices-for-LLMs/page

Guidance on data privacy best practices for LLMs, focusing on data minimization, purpose limitation, retention policies, security controls, and user transparency

Question 4 — Which approach to data privacy in LLM applications represents a best practice according to ethical AI principles?

* Collecting all available user data to improve model performance.
* Implementing data minimization and purpose limitation.
* Storing user interaction data indefinitely for future analysis.
* Sharing user data across applications without specific consent.

Answer: Implementing data minimization and purpose limitation.

> **lightbulb** Implementing data minimization and purpose limitation means collecting only the data strictly necessary for a stated purpose and not using it beyond that purpose without additional consent. This approach balances utility with privacy and aligns with ethical and legal data-protection frameworks.

<Frame>
  <img alt="The image presents a multiple-choice question about data privacy best practices in LLM applications, with the correct answer being &#x22;Implementing data minimization and purpose limitation.&#x22; A detailed explanation of this choice is provided below the answer." />
</Frame>

Why this is the best practice

* Data minimization: Collect only the data required to deliver the requested functionality (for example, short-lived session context needed to fulfill a prompt). Avoid broad, unrelated telemetry or personal data collection.
* Purpose limitation: Define and document the explicit purposes for data collection up front. Do not repurpose data for analytics, training, or third-party sharing without clear, informed consent.
* Privacy-preserving controls: Use technical controls such as role-based access control, end-to-end encryption (in transit and at rest), aggregation, anonymization/pseudonymization, and techniques like differential privacy when aggregating usage data for analytics or model improvement.
* Retention and disposal: Implement and enforce retention schedules so personal or sensitive data is deleted or irreversibly anonymized once it is no longer needed.
* Transparency and user rights: Provide clear privacy notices, enable users to access, correct, or delete their data, and require explicit consent for new processing activities beyond the original scope.

Comparison: approaches and risks

| Approach                                              |                                                        Why teams choose it | Risks / Why it's not best practice                                |
| ----------------------------------------------------- | -------------------------------------------------------------------------: | ----------------------------------------------------------------- |
| Implementing data minimization and purpose limitation | Balances model utility and compliance; reduces legal and reputational risk | Requires upfront planning and scope discipline                    |
| Collecting all available user data                    |                   May seem to improve model performance or analytics depth | Increases attack surface, noncompliance risk, and user mistrust   |
| Storing data indefinitely                             |                             Enables long-term analysis and future research | Magnifies breach impact, conflicts with many regulations          |
| Sharing data across applications without consent      |                                 Facilitates cross-product features quickly | Violates user expectations and many privacy laws; high legal risk |

Why the other options are harmful

* Collecting everything: Indiscriminate collection increases exposure to breaches and regulatory penalties while offering diminishing returns on model performance.
* Storing indefinitely: Long retention periods multiply breach impact and often violate data-protection principles like storage limitation.
* Sharing without consent: Unconsented sharing undermines user trust and usually contravenes legal frameworks such as GDPR, CCPA, and other privacy laws.

Key takeaways

* Adopt a privacy-by-design posture: bake minimization, purpose limitation, and retention policies into system design and development workflows.
* Use technical and organizational safeguards together: encryption, access controls, logging, and regular audits.
* Document policies and obtain explicit consent for secondary uses or model training that rely on user data.
* Monitor legal and ethical guidance: stay aligned with frameworks such as GDPR, ISO 27001, and NIST privacy recommendations.

Further reading and references

* [GDPR Overview](https://gdpr.eu/)
* [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
* [Differential Privacy — Google Research](https://research.google/pubs/pub46419/)

- [Watch Video](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/f5fcaa31-ee4e-4d79-9474-be230c1c96b7/lesson/7774ff60-4ce5-4204-b44a-5fed29ab8fd7)
