# Initialize the JumpStart model by model_id (region/account-specific)
model = JumpStartModel(model_id="meta-textgeneration-llama-2-7b-f")

# Deploy the model to a managed SageMaker endpoint
# You can pass additional args like instance_type, initial_instance_count, etc.
predictor = model.deploy()

# Invoke the deployed endpoint with an input prompt and generation parameters
response = predictor.predict(
    {
        "inputs": "Write a short story about a robot learning emotions.",
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }
)

print(response)
```

Notes about the example:

* Ensure the `model_id` exists in your AWS region and account — JumpStart model identifiers vary by region.
* `deploy()` supports deployment options such as `instance_type` and `initial_instance_count`.
* The `predict()` request schema can vary by model family (text-generation vs. text-embedding vs. vision models); always consult the model card.

<Callout icon="lightbulb">
  Before deploying a model, verify available `model_id`s in your account/region and read the JumpStart model card to confirm input/output schema, latency expectations, and required compute resources.
</Callout>

## SageMaker JumpStart vs Amazon Bedrock

Use cases and trade-offs between the two services:

| Dimension         | SageMaker JumpStart                                                                                     | Amazon Bedrock                                                               |
| ----------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Intended users    | ML engineers & data scientists who want control over training, fine-tuning, and managed SageMaker infra | Application developers who want serverless API access to foundation models   |
| Customization     | Full customization and fine-tuning using SageMaker training jobs                                        | API-centric; some providers offer customization but workflow is more managed |
| Infrastructure    | Deploy models as SageMaker endpoints or training jobs (managed infra you configure)                     | Serverless model hosting — no endpoint management                            |
| Integration       | Deep integration with SageMaker Studio, SDKs, and other AWS ML services                                 | Simple web APIs for quick application integration                            |
| Typical scenarios | Custom model fine-tuning, complex ML pipelines, data-heavy workflows                                    | Low-overhead inference, quick prototyping inside applications                |

## Best practices and cost considerations

* Choose appropriate instance types and initial instance counts based on expected throughput and latency.
* Monitor endpoint usage and set autoscaling policies where applicable.
* Delete unused endpoints and snapshot large models when idle to avoid ongoing costs.
* Review model cards for memory and GPU requirements; some models need large GPUs (e.g., `p4d`, `p5`) or multiple GPUs.

<Callout icon="warning">
  Large foundation models can incur significant compute and storage costs during deployment and inference. Monitor usage, choose cost-appropriate instance types, and remove unused endpoints to prevent unexpected charges.
</Callout>

## References and further reading

* SageMaker JumpStart — [https://aws.amazon.com/sagemaker/jumpstart/](https://aws.amazon.com/sagemaker/jumpstart/)
* Amazon Bedrock — [https://aws.amazon.com/bedrock/](https://aws.amazon.com/bedrock/)
* Common Crawl — [https://commoncrawl.org/](https://commoncrawl.org/)
* SageMaker Studio — [https://aws.amazon.com/sagemaker/studio/](https://aws.amazon.com/sagemaker/studio/)

Use these links and the model cards within JumpStart to evaluate models, understand input/output formats, and plan resource requirements before deploying to production.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/f56823ab-228e-487e-a606-4f8208cb5d0f" />
</CardGroup>


# Hyperparameter Tuning Techniques

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Hyperparameter-Tuning-Techniques/page

Overview of hyperparameter tuning methods, pros and cons, and managed tools like SageMaker for optimizing machine learning model performance and resource use.

Hyperparameter tuning (also called hyperparameter optimization, HPO) is the process of selecting the best set of hyperparameters for a machine learning model. Hyperparameters are set before training — unlike model parameters (weights, biases) that are learned — and they control data preprocessing, training dynamics, model capacity, and evaluation. Choosing the right hyperparameters is essential for building models that generalize well and are stable in production.

Why tuning matters

* Correct hyperparameters control the trade-off between underfitting and overfitting.
* They influence convergence speed, final accuracy, and resource usage (compute and time).
* Effective tuning can reduce cost by lowering the number of expensive training runs needed to reach target performance.

<Frame>
  <img alt="The image illustrates the process of why tuning matters in machine learning, showing a flow from input data to a model, resulting in high-quality predictions, with hyperparameter tuning as a key component." />
</Frame>

Types of hyperparameters
Hyperparameters fall into several categories depending on what aspect of the training or model they affect:

* Model-specific: number of layers, number of neurons, max depth (decision trees), kernel type (SVM).
* Regularization: L1/L2 penalties, dropout rate, weight decay.
* Training process: learning rate, batch size, optimizer, number of epochs.
* Evaluation / early stopping: validation split, early-stopping patience, checkpoint frequency.

Table: common hyperparameter categories and examples

| Category                | Purpose                                          | Examples                                                             |
| ----------------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| Model-specific          | Controls model capacity/architecture             | `num_layers`, `hidden_units`, `max_depth`, `kernel`                  |
| Regularization          | Prevents overfitting and improves generalization | `dropout_rate`, `l1_lambda`, `l2_lambda`, `weight_decay`             |
| Training process        | Affects optimization dynamics and resource use   | `learning_rate`, `batch_size`, `optimizer`, `num_epochs`             |
| Evaluation / scheduling | Controls evaluation cadence and early exit       | `validation_split`, `early_stopping_patience`, `checkpoint_interval` |

<Frame>
  <img alt="The image is a slide titled &#x22;Common Hyperparameters,&#x22; highlighting model-specific parameters such as layers/neurons, max depth, and kernel type, with a geometric icon on the left." />
</Frame>

Overview of tuning strategies
Common tuning strategies include manual tuning, grid search, random search, and Bayesian optimization. Each technique balances exploration, exploitation, cost, and the number of training trials differently. Choose the method that fits your compute budget, search space size, and required repeatability.

<Frame>
  <img alt="The image outlines tuning techniques with three options: Manual Tuning, Grid Search, and Random Search. It includes a process flow of &#x22;Try,&#x22; &#x22;Train,&#x22; &#x22;Evaluate,&#x22; and &#x22;Adjust,&#x22; indicating a repeatable cycle." />
</Frame>

Comparative summary of tuning techniques

| Technique             |                                                Pros | Cons                                                    | Best for                                        |
| --------------------- | --------------------------------------------------: | ------------------------------------------------------- | ----------------------------------------------- |
| Manual tuning         |        Fast for small experiments; builds intuition | Not scalable, subjective                                | Quick prototypes, educational experiments       |
| Grid search           |   Deterministic, parallelizable, exhaustive on grid | Explodes combinatorially for many params                | Small, bounded discrete search spaces           |
| Random search         |        Efficient in high-dimensional spaces, simple | Still brute-force, may miss narrow optima               | Medium-to-large spaces with limited budget      |
| Bayesian optimization | Sample-efficient; balances exploration/exploitation | More complex to implement; overhead for surrogate model | Expensive training runs; when trials are costly |

Manual tuning

* Pros: Simple, increases practitioner intuition about which hyperparameters matter.
* Cons: Time-consuming, not scalable, often yields suboptimal configurations.
* When to use: Exploratory experiments, small models, or educational settings.

Grid search
Grid search evaluates all combinations from a pre-specified grid of values.

* Pros: Exhaustive within the grid and easy to parallelize.
* Cons: Infeasible for large or continuous search spaces; wastes trials on unimportant parameters.
* When to use: Low-dimensional, discrete search spaces where guaranteed grid coverage is desired.

<Frame>
  <img alt="The image presents tuning techniques with a focus on &#x22;Grid Search&#x22;, highlighting its pros (exhaustive, easy to parallelize) and cons (slow for large spaces, wasteful with irrelevant combinations)." />
</Frame>

Random search
Random search samples configurations from specified distributions or discrete sets.

* Pros: More efficient than grid search in many practical high-dimensional problems; tends to find good configurations with fewer trials.
* Cons: Still random and can miss narrow optimal regions.
* When to use: Medium-to-large search spaces where budget is limited and you want broader coverage than a grid.

<Frame>
  <img alt="The image shows a diagram of tuning techniques for machine learning, highlighting Manual Tuning, Grid Search, and Random Search with parameters for learning rate and batch size." />
</Frame>

<Frame>
  <img alt="The image presents tuning techniques, highlighting &#x22;Random Search&#x22; with pros like efficiency and speed, and cons like potentially missing optimal values." />
</Frame>

Bayesian optimization
Bayesian optimization constructs a probabilistic surrogate (often a Gaussian Process) to model the relationship between hyperparameters and the objective metric. An acquisition function (e.g., Expected Improvement, Upper Confidence Bound) selects the most promising hyperparameters to evaluate next, yielding sample-efficient search that typically converges faster than grid or random search.

* Pros: Great for expensive-to-evaluate objectives; reduces number of required trials.
* Cons: Additional implementation complexity; surrogate model overhead for many parallel experiments.
* When to use: Long training runs, costly compute (GPU/TPU), or when each trial is expensive in time or money.

<Frame>
  <img alt="The image depicts a graph illustrating Bayesian Optimization with GP (Gaussian Process) estimation, showing the true function, GP mean, confidence interval, and observed values. It emphasizes smarter, fewer trials and faster convergence in tuning techniques." />
</Frame>

Amazon SageMaker hyperparameter tuning
Amazon SageMaker exposes managed hyperparameter tuning jobs (HPO) to orchestrate many training jobs with different hyperparameter combinations. SageMaker handles parallelization, resource provisioning, logging, and supports both random and Bayesian (SMBO) optimization strategies, making it practical for production pipelines where scale, cost control, and observability are important.

* Key features:
  * Define hyperparameter ranges and distributions.
  * Choose optimization strategies (random or Bayesian/SMBO).
  * Run many training jobs in parallel with resource management.
  * Aggregate results, log metrics, and automatically select the best model.

<Frame>
  <img alt="The image illustrates the Amazon SageMaker automatic model tuning process, showing the flow from data preprocessing to tuning jobs and model deployment, integrated with various AWS services like ECR, EBS, and CloudWatch." />
</Frame>

When to prefer managed or Bayesian HPO

* Use Bayesian optimization or a managed HPO service (like SageMaker HPO) when training is expensive or each trial takes hours/days.
* Use random search for a balance of simplicity and efficiency on larger search spaces.
* Reserve grid search for small, discrete, and well-bounded parameter grids.

<Callout icon="lightbulb">
  When training is expensive (long training times or high compute cost), prefer Bayesian optimization or managed tuning services that reduce the number of trials needed to find a good configuration.
</Callout>

Further reading and references

* [Kubernetes Documentation](https://kubernetes.io/docs/) (deployment patterns for training clusters)
* [Amazon SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) (managed model training and HPO)
* Research on Bayesian optimization and SMBO for hyperparameter tuning

Use these techniques and tools to match your problem constraints — computation budget, time-to-result, and repeatability — and to move from intuition-driven experiments to production-ready, well-tuned models.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/54987cb0-9cea-4937-8a4d-103c5f5c964a" />
</CardGroup>
