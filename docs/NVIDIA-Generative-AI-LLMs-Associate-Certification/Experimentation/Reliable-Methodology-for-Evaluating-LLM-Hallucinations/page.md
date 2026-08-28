# Reliable Methodology for Evaluating LLM Hallucinations

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Experimentation/Reliable-Methodology-for-Evaluating-LLM-Hallucinations/page

Describes a hybrid methodology combining human expert annotation and automated knowledge-base checks to reliably evaluate LLM hallucinations, with recommended metrics and experimental practices

Question 4.

When designing an experiment to evaluate LLM hallucinations, which methodology would provide the most reliable assessment?

* Automated comparison of generated text against a knowledge base?
* Measuring the model's confidence scores for each generated statement?
* Human expert verification combined with factual knowledge-base checking?
* Counting the number of citations included in the model's response?

Answer: Human expert verification combined with factual knowledge-base checking.

Combining domain expert review with systematic checks against authoritative knowledge bases gives the most robust and reliable evaluation of hallucinations. Experts catch subtle context-dependent errors, ambiguous phrasing, and domain-specific nuances that automated checks often miss; automated knowledge-base verification supplies reproducible, objective evidence for claims that can be programmatically validated.

A recommended experimental methodology

* Define a representative, diverse test set of prompts and enumerate the specific factual claims or expected answers for each prompt. Include edge cases and ambiguous contexts.
* Recruit multiple domain experts to independently annotate model outputs for factuality and error type (e.g., fabrication, misattribution, omission, partial truth). Require annotators to record brief justifications for their labels to support adjudication.
* Run automated fact checks against one or more curated knowledge bases or canonical sources to flag claims that are clearly verifiable or falsifiable.
* Create a decision rule to combine expert annotations with automated flags into a final label for each claim (for example: factual / partially factual / hallucinated).
* Quantify annotation reliability with inter-annotator agreement measures such as [Cohen’s kappa](https://en.wikipedia.org/wiki/Cohen%27s_kappa) and [Krippendorff’s alpha](https://en.wikipedia.org/wiki/Krippendorff%27s_alpha).
* Report both aggregate metrics and representative qualitative examples. Include edge-case analyses to clarify limitations and interpretability.

<Frame>
  <img alt="The image presents &#x22;Question 4,&#x22; asking about the most reliable method for evaluating LLM hallucinations, suggesting &#x22;Human expert verification combined with factual knowledge base checking&#x22; as the answer. It explains that this approach leverages both domain expertise and systematic checking for accuracy." />
</Frame>

Why not rely solely on automated methods or confidence scores?

* Automated comparison against knowledge bases is useful for high-precision checks but can miss context-dependent or nuanced errors and is limited by the coverage and freshness of the knowledge base.
* Model confidence scores (e.g., logit-based or probability measures) do not consistently correlate with factual accuracy and can give a false sense of reliability.
* Counting citations is insufficient because models can fabricate references or include irrelevant/incorrect citations; citation presence does not guarantee factuality.

Recommended metrics to report

| Metric                    | Definition                                                             | Notes / Example                                       |
| ------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------- |
| Factual precision         | True factual claims / Claims labeled factual                           | Measures correctness among claims considered factual. |
| Factual recall            | True factual claims / Total true claims                                | Measures coverage of true claims identified.          |
| Hallucination rate        | Hallucinated claims / Total claims                                     | Key metric for overall hallucination prevalence.      |
| Inter-annotator agreement | Agreement among annotators (e.g., Cohen’s kappa, Krippendorff’s alpha) | Indicates label reliability and annotation quality.   |

<Callout icon="lightbulb">
  Best practice: adopt a hybrid evaluation—structured human annotation plus targeted automated checks. Publish both quantitative metrics and curated qualitative examples so readers can assess strengths, failure modes, and real-world applicability.
</Callout>

Links and references

* [Cohen’s kappa](https://en.wikipedia.org/wiki/Cohen%27s_kappa) — measure of inter-rater reliability
* [Krippendorff’s alpha](https://en.wikipedia.org/wiki/Krippendorff%27s_alpha) — flexible agreement coefficient for multiple raters and data types

Examples and further reading

* For practical toolchains, combine annotation platforms (for expert labeling) with programmable fact-checking pipelines that query curated databases or APIs.
* When publishing evaluations, include dataset examples, annotation guidelines, and adjudication rules so results are reproducible and actionable.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/44b444b3-19d6-4856-95a6-a46628fb2cf0/lesson/166007e8-026d-41ee-9638-e1a7d17c056d" />
</CardGroup>
