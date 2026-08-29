# LLM Evaluation Metric for Factual Accuracy

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Core-Machine-Learning-and-AI-Knowledge/LLM-Evaluation-Metric-for-Factual-Accuracy/page

Explains using truthfulness scores to evaluate LLM factual accuracy and compares them to perplexity, BLEU, and speed

Let's review Question 3.

When evaluating an LLM for deployment, which metric best measures the model's ability to generate factually accurate responses?

Options: Perplexity, BLEU score, Truthfulness score, Token generation speed.

Correct answer: truthfulness score — because it is specifically designed to evaluate factual accuracy.

<Frame>
  <img alt="The image shows a question about evaluating LLM performance, asking which metric measures factual accuracy. The options are Perplexity, BLEU score, Truthfulness score (highlighted), and Token generation speed." />
</Frame>

Why truthfulness score is the right choice

* Truthfulness scores are created to measure factual correctness: they check generated claims against ground-truth facts, knowledge bases, or fact-checking systems.
* These scores aim to quantify hallucinations and misinformation risk, which are central concerns when deploying LLMs in real-world applications (search, assistants, medical or legal apps).

Comparison of common metrics

| Metric                 | Primary focus                             | Useful for                                                                                              | Not appropriate for                                                           |
| ---------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Truthfulness score     | Factual accuracy and misinformation       | Detecting incorrect claims, evaluating factuality on QA/fact-check benchmarks (e.g., TruthfulQA, FEVER) | Measuring fluency or latency                                                  |
| Perplexity             | Model likelihood / next-token prediction  | Assessing model fluency and how well the model fits training distribution                               | Detecting factual errors or hallucinations                                    |
| BLEU score             | n-gram overlap with reference text        | Evaluating literal similarity in translation or constrained generation                                  | Measuring factual correctness when correct answers can be phrased differently |
| Token generation speed | System performance (latency / throughput) | Infrastructure and production performance tuning                                                        | Anything about content correctness or factuality                              |

Short descriptions

* Truthfulness score: Evaluates whether an output is factually correct, typically by comparing model assertions to a fact base or using automated fact-checkers and QA-based evaluation.
* Perplexity: Measures how surprised a model is by a test sequence; useful for fluency and model fit but not for verifying facts.
* BLEU score: Quantifies surface-level overlap with reference text; useful in translation but unreliable for factuality when many correct phrasings exist.
* Token generation speed: A systems metric that reports latency or throughput; unrelated to whether generated content is true.

Best practices for assessing factual accuracy

* Use truthfulness-specific automated evaluations (e.g., QA-based checks, fact verification datasets like FEVER or TruthfulQA) combined with targeted human review for nuanced or context-dependent claims.
* Complement automated truthfulness metrics with downstream task checks (retrieval-augmented verification, knowledge-grounded generation) to reduce hallucinations.
* Keep separate evaluation axes for fluency (perplexity), similarity (BLEU), and performance (latency) — each serves different decisions in model development and deployment.

> **lightbulb** When measuring factual accuracy, prefer truthfulness-oriented evaluations (automated fact-checkers, QA-based factuality tests, or specialized benchmarks). Combine automated truthfulness scores with focused human evaluation to catch subtle or context-dependent errors.

> **warning** Do not rely solely on perplexity, BLEU, or generation speed to judge factual accuracy. These metrics can indicate fluency or system performance but will miss hallucinations unless paired with truthfulness-specific evaluations.

Further reading and resources

* TruthfulQA benchmark: [https://github.com/sylinrl/TruthfulQA](https://github.com/sylinrl/TruthfulQA)
* FEVER fact verification dataset: [https://fever.ai/](https://fever.ai/)
* Survey of evaluation for factuality and hallucinations in NLG: see recent literature on factuality metrics and QA-based evaluation methods.

- [Watch Video](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/875d98e8-3b09-4f35-b877-2758b84443ca/lesson/7ca35633-42ec-46be-97ac-c7120066c9ea)
