# SageMaker Canvas Low Code Data Preparation and ML Training Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Engineer/SageMaker-Canvas-Low-Code-Data-Preparation-and-ML-Training-Part-2/page

Overview of SageMaker Canvas and Data Wrangler for low-code data preparation, AutoML model building, explainability, deployment, and cost considerations for tabular ML workflows.

After you inspect the Data Quality and Insights report in Data Wrangler, return to the Data Wrangler data-flow canvas to continue preparing your dataset. The Data Quality and Insights report is an inspection step (it does not transform data). To add actual transformations to the raw data, open the Data types node and use the blue plus (+) icon to insert transforms.

Use the search box to quickly find built-in transforms (for example, search for "drop column" or "impute"). Each transform you add becomes a node in the flow; nodes execute sequentially so the output of one transform feeds the next. Typical workflows begin by dropping irrelevant columns, then handling outliers and missing values, and finally encoding categorical variables. Keeping the pipeline compact early (dropping irrelevant columns sooner) reduces cost and speeds downstream processing.

<Frame>
  <img alt="A dark-themed slide showing a data pipeline titled &#x22;Workflow: Transformations,&#x22; with connected nodes like Source (Canvas Dataset), Data types, Data Quality and Insights Report, Quantile numeric outliers, and Ordinal encode. The diagram illustrates the flow of a canvas-sample-housing.csv dataset through various transformation and quality-check steps." />
</Frame>

Example transformation sequence (typical pattern)

* Drop irrelevant identifiers and high-cardinality fields first.
* Clip or cap extreme values (e.g., quantile numeric outliers).
* Impute missing values (mean/median for numeric, mode for categorical).
* Apply encoders: ordinal encode for ordered categories, one-hot for nominal categories.
* Scale numeric features if required by downstream models.

Because Data Wrangler is visual, you can chain many transforms (10–15+). The flowchart makes dependencies and order explicit, which helps when debugging or exporting the pipeline.

Exporting transformed data

* Add an Export node at the end of the flow to save the prepared dataset.
* Data Wrangler supports exporting transformed datasets to Amazon S3.
* Optionally generate a reproducible Jupyter Notebook containing Python code that matches the visual transforms: useful for hand-off to ML engineers (note: the generated notebook can be verbose).

Table — Export options at a glance

| Export Target    | Use Case                                       | Notes                                         |
| ---------------- | ---------------------------------------------- | --------------------------------------------- |
| Amazon S3        | Reuse transformed data for training or sharing | Standard choice for SageMaker pipelines       |
| Jupyter Notebook | Reproduce/inspect transformation code          | Notebook tends to be verbose but reproducible |

With a cleaned, transformed dataset you can use SageMaker Canvas AutoML to build models without writing code. From the Canvas UI you select the exported dataset, name the model, and choose the problem type. For the housing example, the target column `median_house_value` signals a regression problem. Canvas uses pre-sized compute and automatic algorithm selection plus automated hyperparameter handling to produce candidate models.

When Canvas starts an AutoML build, it creates a standard SageMaker training job under the hood:

* The job name typically includes the prefix "canvas".
* Training job details include source S3 locations, output artifact location, and the container/algorithm used.
* You can inspect these jobs in SageMaker Studio under Jobs → Training.

For more on training job internals see: [Amazon SageMaker training jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html)

<Frame>
  <img alt="A screenshot of an AutoML workflow (SageMaker Canvas) showing the Build tab for a &#x22;KodeKloudHousePriceModel&#x22; with the target column set to &#x22;median_house_value&#x22; and a histogram of its value distribution. The interface also shows dataset columns (e.g., total_rooms, total_bedrooms), summary stats, and a prominent &#x22;Quick build&#x22; button." />
</Frame>

After training completes Canvas surfaces model metrics and explainability:

* For regression, view RMSE (root mean squared error) and MSE, which summarize average prediction error magnitude. Lower RMSE generally indicates a better fit.
* Canvas shows per-feature impact (feature importance) and interactive visualizations (scatterplots, partial dependence–style views) to help you understand how features influence predictions.
* Use quick-build for rapid evaluation, one-off predictions with manual input, or perform a standard/manual build for longer searches.

<Frame>
  <img alt="Screenshot of an AutoML workflow dashboard for a house-price model showing model metrics (RMSE and MSE). It also shows feature impact rankings with median_income top and a scatterplot of median_income versus predicted median_house_value." />
</Frame>

What SageMaker Canvas provides

* Low-code end-to-end flow for data preparation, AutoML model building, and deployment.
* Auto preprocessing, basic encoding, and cleaning (with finer-grain control available via Data Wrangler).
* Automated model selection and basic explainability (feature impact and visual diagnostics).
* One-click deployment to a SageMaker endpoint (real-time inference) or batch predictions.

However, there are trade-offs. The most important limitations to consider:

* Limited customization: you cannot pick specific algorithms or fully control hyperparameters from the Canvas UI.
* Focus on tabular data: Canvas is optimized for common tabular problems (regression, classification, forecasting); for deep learning, NLP, or vision use SageMaker code-first workflows.
* Limited compute control: Canvas chooses instance sizing; it may not be optimal for very large datasets or specialized hardware.
* No training code export: Data Wrangler can export transformation code, but Canvas does not expose AutoML training code.
* No built-in hyperparameter tuning management; use SageMaker hyperparameter tuning jobs for advanced HPO.
* Deployment is primarily to SageMaker endpoints; alternative hosting and custom inference setups require additional steps.
* No multi-model ensemble training or advanced ML features (transfer learning, custom loss functions) within Canvas.

Table — Canvas features vs limitations

| Area           | Canvas strengths                                           | Limitations                                                         |
| -------------- | ---------------------------------------------------------- | ------------------------------------------------------------------- |
| Data prep      | Visual Data Wrangler integration, many built-in transforms | Complex pipelines may still need code                               |
| Training       | Quick AutoML, low-code model builds                        | No algorithm choice, limited hyperparameter control                 |
| Explainability | Feature impact and visual diagnostics                      | Not as deep as custom explainability toolkits                       |
| Deployment     | One-click endpoint deploy                                  | Limited deployment targets; manual export required for alternatives |
| Cost control   | Fast prototyping                                           | Canvas session + training + endpoint costs billed separately        |

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Cost Saving&#x22; stating that Canvas is billed in multiple dimensions. Four numbered cards list cost areas: Canvas session time; model training compute & time; predictions (single & batch inference); and S3 storage/upload of datasets." />
</Frame>

Billing considerations

* Canvas session time: Canvas sessions are billed while the managed instance is running. Typical rates vary by region; leaving sessions idle can accumulate cost.
* Training jobs: SageMaker training costs (instance hours, instance types) apply to each training job Canvas creates.
* Inference: Real-time endpoints are billed while running; batch transform jobs are billed per-job.
* Storage: S3 storage for datasets and artifacts is billed at standard S3 pricing.
* Clean up: Stop and delete any running training jobs, batch jobs, endpoints, or unnecessary S3 objects to avoid ongoing charges.

<Callout icon="warning">
  Shutting down the Canvas session does not automatically stop all resources provisioned during the session. Check for running training jobs, deployed endpoints, and stored datasets in S3—these continue to incur charges until you terminate or delete them.
</Callout>

Using SageMaker Canvas AutoML saves time by automating exploratory analysis and many preprocessing steps, but don’t skip careful data preparation. The Data Quality and Insights report in Data Wrangler helps identify issues — missing values, duplicates, and outliers — and suggests remediation such as mean/mode imputation, dropping duplicates, or clipping outliers. Fixing these problems before training typically improves model performance.

<Frame>
  <img alt="A presentation slide titled &#x22;Results With SageMaker Canvas AutoML&#x22; showing four numbered panels. Each panel lists a benefit: automating exploratory data analysis to save time, improving model accuracy by finding and fixing data issues, reducing human error with handling recommendations, and helping non-technical users understand data before training." />
</Frame>

Key takeaways

* SageMaker Canvas is a low-code UI that integrates Data Wrangler for visual data preparation, offers AutoML model building, and supports managed deployment to SageMaker endpoints.
* Data Wrangler has hundreds of built-in transforms (one-hot encoding, scaling, imputation, column drop, outlier clipping) you can chain to prepare data for training.
* Canvas AutoML automates model selection and training and provides basic explainability, but trades off detailed control (algorithm selection, HPO, training code).
* After training you can run immediate predictions or deploy a model with a single click to a managed endpoint.
* Monitor and manage resources (Canvas sessions, training jobs, endpoints, S3 storage) to control cost.

<Frame>
  <img alt="A presentation slide titled &#x22;SageMaker Canvas AutoML – Limitations.&#x22; It shows three boxed points: limited customization, support only for tabular data, and compute constraints." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;SageMaker Canvas AutoML – Limitations&#x22; showing three boxed items: 04 Dataset size limits, 05 No code export, and 06 No hyperparameter tuning. Each box has a short explanation (processing time/quotas; only trained models/datasets can be exported; no built-in HPO)." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;SageMaker Canvas AutoML – Limitations&#x22; showing three numbered cards that list: limited deployment, no multi-model training, and no advanced ML features. Each card includes a brief explanation (e.g., models can only be deployed to SageMaker Endpoints or downloaded; no transfer learning or deep learning frameworks)." />
</Frame>

This lesson covered:

* An introduction to SageMaker Canvas as a low-code interface for tabular data prep, AutoML model building, and managed deployment.
* How Data Wrangler (integrated with Canvas) helps prepare data with many built-in transformations and a Data Quality and Insights report.
* How Canvas AutoML automates model selection and provides basic explainability, while limiting low-level control and advanced ML workflows.
* The importance of careful data preparation to improve model accuracy.
* Billing and operational considerations for Canvas and SageMaker resources.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; that lists five numbered points about AWS SageMaker tools. It highlights SageMaker Canvas, Data Wrangler, AutoML in Canvas, Interactive Predictions, and billing/runtime considerations." />
</Frame>

Further reading and references

* Amazon SageMaker Canvas overview: [https://docs.aws.amazon.com/sagemaker/latest/dg/canvas.html](https://docs.aws.amazon.com/sagemaker/latest/dg/canvas.html)
* Data Wrangler documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html)
* SageMaker training jobs: [https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html)

That wraps up this lesson. The next lesson will include a live demo walking through the Canvas UI end-to-end.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/dc8df298-eaee-4f8a-b1d0-0ec66f9c6d20/lesson/21ac08a5-2528-4b06-b7f1-4696a580b61f" />
</CardGroup>
