# Pre training Bias Metrics for Different Data Types

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Pre-training-Bias-Metrics-for-Different-Data-Types/page

Guidance on detecting and mitigating dataset bias before training, covering bias types, metrics for categorical numerical text and image data, and mitigation strategies to improve fairness.

Bias introduced during data collection or labeling often persists through model training and into production. If raw data misrepresents the target population or encodes unfair historical patterns, model predictions and automated decisions can disadvantage groups or mischaracterize real-world outcomes. Detecting and correcting bias early—during collection, labeling, and preprocessing—reduces the risk that models will amplify unfair patterns.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Flow of Bias,&#x22; illustrating how bias in raw data collection can lead to biased models and results, which may disadvantage certain groups or misrepresent the population." />
</Frame>

Addressing bias in the data pipeline (rather than only post-deployment) is more effective: when preprocessing removes systematic distortions, downstream models are trained on fairer, more representative inputs and produce more equitable results.

<Callout icon="lightbulb">
  Detect and mitigate bias early in the data pipeline—collection, labeling, and preprocessing—so models are trained on representative and high-quality data.
</Callout>

<Frame>
  <img alt="The image illustrates a flowchart titled &#x22;Fair Path,&#x22; depicting the process of addressing bias in raw data, model training, and achieving fair results through detecting and fixing bias during data collection." />
</Frame>

Common forms of bias in ML datasets

* Sampling bias — the dataset composition does not match the target population proportions.
* Label bias — annotations contain systematic errors or inconsistent criteria.
* Measurement bias — sensors, instruments, or protocols distort recorded values.
* Historical bias — past societal inequities are encoded in historical data.

<Frame>
  <img alt="The image lists four types of bias in machine learning datasets: sampling bias, label bias, measurement bias, and historical bias, each with a brief description." />
</Frame>

Sampling bias
Sampling bias occurs when the dataset no longer reflects the real-world population proportions. For instance, if the true population is 53% blue and 47% green but training data is 67% blue and 33% green, the model will favor blue examples and underperform for green examples. Typical causes include skewed collection channels, under-sampling of minority groups, or convenience sampling.

<Frame>
  <img alt="The image illustrates sampling bias with a grid of blue and green circles, showing different proportions of each color in the overall sample versus a biased sample subset." />
</Frame>

Label bias
Label bias arises from inconsistent or subjective annotation choices. Different annotators may apply different standards, or ambiguous instructions can produce systematic label errors. Tasks heavily reliant on human judgment—sentiment analysis, clinical labels, content moderation—are particularly sensitive to label bias.

<Frame>
  <img alt="The image illustrates the concept of label bias, showing how human labelers create labels that influence a model, potentially leading to bias due to human error or inconsistent criteria." />
</Frame>

Measurement bias
Measurement bias appears when instruments or collection procedures systematically distort values. Examples include sensor calibration drift, differing sampling rates, or environmental factors that affect readings. Left unchecked, measurement bias and related data-quality issues (noise, missing values, low resolution) provide misleading signals to models.

<Frame>
  <img alt="The image illustrates &#x22;Measurement Bias,&#x22; depicting data collected from two sensors (A and B) being processed and fed into a model. It highlights potential inaccuracies in data collection methods or instruments." />
</Frame>

Historical bias
Historical bias captures societal or structural inequities reflected in past records. A dataset spanning 1990–2020 may faithfully record historical discrimination; training on that data without adjustment can perpetuate those inequities into modern systems.

<Frame>
  <img alt="The image illustrates the concept of historical bias, showing past data from years 1990, 2000, 2010, and 2020 being input into a model to produce a document for 2025." />
</Frame>

Bias across data modalities
Bias shows up differently depending on data type, so choose metrics and mitigations accordingly:

* Categorical data (representation bias): Are group proportions aligned with the target population?
* Numerical data (distribution bias): Which ranges are over- or underrepresented? Are distributions shifted or truncated?
* Textual data (perspective/historical bias): Which voices or narratives are emphasized or missing?
* Image data (coverage bias): Which groups, regions, contexts, or conditions dominate samples?

<Frame>
  <img alt="The image is a table showing data types (categorical, numerical, text, image), with examples and relevant bias metrics for each type." />
</Frame>

Practical examples and checks

* Example: An astronaut-candidate dataset containing 50% pilots, 30% engineers, and 20% scientists will bias a suitability model toward pilots. Detect this with categorical coverage metrics and rebalance via targeted collection, resampling, or loss reweighting.
* Categorical checks: class proportions and subgroup coverage for sensitive attributes.
* Numerical checks: min/max, percentiles, distributional tests, and subgroup-specific summaries.

<Frame>
  <img alt="The image presents &#x22;Other Bias Metrics,&#x22; listing two categories: &#x22;Categorical&#x22; (who's included/excluded) and &#x22;Numerical&#x22; (what values are over-/under-represented), with associated icons." />
</Frame>

Recommended bias metrics and mitigations (quick reference)

| Data type   | Useful metrics                                                                       | Typical mitigation strategies                                                  |
| ----------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| Categorical | Representation ratio, class imbalance, subgroup precision/recall                     | Targeted data collection, resampling, class weights, stratified splits         |
| Numerical   | Distribution overlap (e.g., KL divergence), summary stats, outlier rates             | Normalization, imputation, stratified sampling, sensor recalibration           |
| Text        | Token-level representation counts, sentiment/stance coverage, annotator disagreement | Diverse sourcing, annotation guidelines, data augmentation, debiasing lexicons |
| Image       | Demographic coverage, lighting/pose condition counts, detector performance by group  | Collect diverse conditions, augmentation, balanced sampling, domain adaptation |

Combine quantitative metrics (representation ratios, KL divergence, label disagreement rates, subgroup performance gaps) with qualitative review—auditor checks, annotator feedback, and domain-expert analysis—to build confidence that the dataset is representative and reliable before training models.

Further reading and tools

* Google: Fairness in Machine Learning — [https://developers.google.com/machine-learning/fairness-overview](https://developers.google.com/machine-learning/fairness-overview)
* IBM: AI Fairness 360 toolkit — [https://aif360.mybluemix.net/](https://aif360.mybluemix.net/)
* Research primer on dataset bias and mitigation strategies

<Callout icon="warning">
  Ignoring pre-training bias can embed and amplify unfair outcomes. Prioritize detection and remediation during collection and preprocessing to reduce harm and improve model generalization.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/8f5ee9bf-7558-4066-9035-7efc3e672310" />
</CardGroup>
