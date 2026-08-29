# df contains columns: 'text', 'true_label', 'pred_label', 'demographic_group'
results = []
for group, dfg in df.groupby('demographic_group'):
    acc = accuracy_score(dfg['true_label'], dfg['pred_label'])
    prec = precision_score(dfg['true_label'], dfg['pred_label'], average='binary')
    rec = recall_score(dfg['true_label'], dfg['pred_label'], average='binary')
    results.append({'group': group, 'accuracy': acc, 'precision': prec, 'recall': rec})

group_metrics = pd.DataFrame(results)
print(group_metrics)
```

Use bootstrap or other resampling to obtain confidence intervals for these metrics when subgroup sizes are limited.

## Metrics to track (examples)

| Metric                                         | Why it matters                                                    |
| ---------------------------------------------- | ----------------------------------------------------------------- |
| Accuracy / F1                                  | Baseline performance per group                                    |
| Precision / Recall                             | Reveals bias in error types (false positives vs false negatives)  |
| False positive rate / False negative rate      | Critical in high-stakes settings                                  |
| Calibration error                              | Whether model confidence aligns with actual correctness per group |
| Statistical parity difference / Equalized odds | Common fairness criteria to quantify disparities                  |

For reference implementations and libraries: consider Fairlearn ([https://fairlearn.org/](https://fairlearn.org/)) and IBM AI Fairness 360 ([https://aif360.mybluemix.net/](https://aif360.mybluemix.net/)).

<Callout icon="warning">
  Handle sensitive demographic data with care. Obtain consent where required, follow privacy regulations, and minimize re-identification risk when collecting or reporting demographic attributes.
</Callout>

## Practical considerations and tips

* Small groups: If a subgroup has few samples, avoid overinterpreting noisy metrics—use uncertainty quantification, combine targeted data collection with careful statistical methods, or aggregate similar slices thoughtfully.
* Intersectionality: Bias often appears at intersectional slices (e.g., gender × age × dialect). Evaluate those where relevant to the application.
* Labeling consistency: Ensure labeling practices are consistent across groups to avoid systematic label bias.
* Reporting: Always publish both aggregate and disaggregated results so stakeholders can assess overall and group-level performance.

## Why the other approaches fall short

* Model self-evaluation: LLMs are not reliable judges of their own biases—responses depend on prompts and can be gamed. Use external, systematic evaluation instead.
* Overall accuracy or a single random test set: These hide group disparities and can create false confidence about fairness.

## Summary

Disaggregated evaluation using stratified test sets and group-level metrics is the most effective way to detect and measure LLM performance disparities across demographic groups. It enables rigorous detection of bias, supports targeted mitigation, and provides transparent reporting to stakeholders. For best results, combine quantitative group metrics with qualitative error analysis, statistical testing, and strong privacy-aware data practices.

## Links and references

* Fairlearn: [https://fairlearn.org/](https://fairlearn.org/)
* IBM AI Fairness 360: [https://aif360.mybluemix.net/](https://aif360.mybluemix.net/)
* "Fairness" concepts and metrics: [https://en.wikipedia.org/wiki/Fairness\_(machine\_learning)](https://en.wikipedia.org/wiki/Fairness_\(machine_learning\))

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/44b444b3-19d6-4856-95a6-a46628fb2cf0/lesson/ed193d80-f5ad-49c4-b529-cc994f037a7c" />
</CardGroup>


# Evaluating LLM Quality Without Single Correct Answer

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-[AWS_SECRET_ACCESS_KEY]-LLM-Quality-Without-Single-Correct-Answer/page

Evaluating open-ended language model quality when no single correct answer exists, advocating RLHF with human preference-based reward modeling, workflow, comparisons, and practical trade-offs.

Welcome to the experimentation section.

Question 1.

Which technique is most appropriate for evaluating the performance of a language model when there is no single correct answer, but responses must be evaluated for quality: Reinforcement Learning from Human Feedback (RLHF), k-fold cross-validation, confusion matrix analysis, or mean squared error calculation?

<Frame>
  <img alt="The image displays a question about the most appropriate technique for evaluating the performance of a language model when responses must be assessed for quality. Three options are provided: Reinforcement Learning from Human Feedback (RLHF), K-fold cross-validation, and Confusion matrix analysis." />
</Frame>

Answer: RLHF (Reinforcement Learning from Human Feedback).

Why RLHF is the best fit

* RLHF is designed for open-ended tasks where multiple valid responses may exist and quality is subjective.
* Human evaluators provide comparative judgments or ratings of model outputs. Those judgments are used to train a reward model that represents human preference.
* A reinforcement learning algorithm (commonly Proximal Policy Optimization — PPO) is then used to fine-tune the policy (the LLM) to maximize the learned reward signal, aligning outputs with human preferences rather than a single deterministic label.

<Callout icon="lightbulb">
  Typical RLHF workflow: collect human preference data → train a reward model on that data → fine-tune the LLM using reinforcement learning to maximize the reward model's score → evaluate outputs with human raters and automated checks.
</Callout>

Quick comparison of the candidate techniques

| Technique                                         | Best suited for                                           | Why it fails for subjective / open-ended quality                                             |
| ------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Reinforcement Learning from Human Feedback (RLHF) | Aligning model outputs to human judgments and preferences | Explicitly models subjective preferences via a learned reward signal and policy optimization |
| K-fold cross-validation                           | Supervised tasks with fixed ground-truth labels           | Assumes a single correct label per input; not suitable when multiple responses are valid     |
| Confusion matrix analysis                         | Classification with known discrete classes                | Requires discrete labels and does not capture nuanced or preference-based quality            |
| Mean squared error (MSE)                          | Numeric regression tasks                                  | Measures distance to a numeric target; meaningless for open-ended text generation            |

Why the other choices are less appropriate

* K-fold cross-validation: Good for estimating generalization in supervised learning, but it requires definitive ground-truth labels for each sample. Open-ended generation lacks a single correct target, so cross-validation doesn’t capture subjective quality or preference.
* Confusion matrix analysis: This is for classification—true positives, false negatives, etc.—and assumes a closed set of classes. It doesn’t measure fluency, relevance, helpfulness, or preference among many valid responses.
* Mean squared error (MSE): A regression metric that quantifies numeric error. It cannot meaningfully evaluate semantic quality, style, or relevance in text outputs.

Practical considerations and trade-offs

* Cost and scale: RLHF requires human raters and careful annotation protocols, making it more expensive and time-consuming than purely automated metrics.
* Rater quality and bias: Reward models reflect the preferences of annotators. Clear guidelines, rater training, and diverse annotator pools are necessary to reduce bias.
* Overfitting to preferences: Models can over-optimize for specific annotator tastes or for the reward model’s weaknesses. Use holdout evaluations, diverse scenarios, and periodic human audits.
* Complementary evaluation: Combine RLHF with automated metrics (e.g., BLEU, ROUGE, or embedding-based similarity) and human evaluations for a robust assessment strategy.

Further reading and references

* Christiano, et al., “Deep Reinforcement Learning from Human Preferences” (arXiv): [https://arxiv.org/abs/1706.03741](https://arxiv.org/abs/1706.03741)
* OpenAI, Learning from Human Preferences: [https://openai.com/research/learning-from-human-preferences](https://openai.com/research/learning-from-human-preferences)
* Schulman, et al., “Proximal Policy Optimization Algorithms” (PPO): [https://arxiv.org/abs/1707.06347](https://arxiv.org/abs/1707.06347)

Note: RLHF is the recommended approach when objective labels don't exist and the evaluation target is human judgment of quality, relevance, or preference.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/44b444b3-19d6-4856-95a6-a46628fb2cf0/lesson/a0fa5edf-527f-4555-889b-4b316b8a38d4" />
</CardGroup>
