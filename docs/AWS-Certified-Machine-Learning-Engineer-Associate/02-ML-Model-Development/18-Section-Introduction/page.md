# Replace these values for your environment
role = "arn:aws:iam::123456789012:role/SageMakerRole"
s3_train_path = "s3://your-bucket/path/train"
s3_val_path = "s3://your-bucket/path/validation"

xgb = XGBoost(
    entry_point="train.py",             # your training script
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    framework_version="1.3-1",          # XGBoost container version
    hyperparameters={
        "max_depth": 5,
        "eta": 0.2,
        "objective": "binary:logistic",
        "num_round": 100,
    },
)

# Map channel names to S3 locations and start the training job
xgb.fit({"train": s3_train_path, "validation": s3_val_path})
```

This example demonstrates:

* Launching a managed SageMaker training job with the XGBoost built-in container.
* Using Script Mode (`entry_point="train.py"`) so you can provide custom preprocessing and training code.
* Specifying compute resources (instance type and count) and hyperparameters.
* Providing `train` and `validation` channels that point to S3 prefixes.

Further reading and references

* [Amazon SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [SageMaker JumpStart models and solutions](https://aws.amazon.com/sagemaker/jumpstart/)
* [SageMaker Pipelines](https://aws.amazon.com/sagemaker/pipelines/)
* [SageMaker Clarify](https://aws.amazon.com/sagemaker/clarify/)
* [SageMaker Python SDK — Estimators](https://sagemaker.readthedocs.io/en/stable/api/training/estimators.html)

End of article.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/3715ee50-3846-428e-bc51-fcc75fa715df" />
</CardGroup>


# Section Introduction

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Section-Introduction/page

Framework mapping ML model development phases on AWS to a space mission analogy, covering design, assembly, testing, deployment, monitoring, and post-deployment review

NASA doesn't just launch a rocket — they first define the mission: land on Mars, place a satellite into geostationary orbit, or resupply the International Space Station. In machine learning, the parallel is defining the problem you need to solve: fraud detection, customer churn prediction, or image recognition. You shouldn't build an ML solution without a clear mission objective and success criteria.

In this lesson we map the phases of ML model development on AWS to a space mission. That mapping helps clarify responsibilities, tools, and checkpoints across the model lifecycle:

* Design: plan the experiment, define metrics, and choose data sources.
* Assembly: prepare data, select algorithms, and build training pipelines.
* Testing: validate models with held-out data and perform performance/stability checks.
* Launch: deploy the model to production and enable real-time or batch predictions.
* Mid-course correction: monitor model quality, detect drift, and retrain or adjust as needed.
* Landing: evaluate final outcomes and determine whether objectives were met.

<Frame>
  <img alt="The image outlines the key phases of ML model development on AWS, including Design, Assembly, Testing, Launch, Mid-Course Correction, and Landing, each with a brief description." />
</Frame>

Choosing the right tools is like NASA selecting the correct rocket, fuel, instruments, and landing modules. In ML this choice includes the training framework, feature store, orchestration tools, and cloud services such as SageMaker for training and deployment, S3 for durable storage, and Glue for ETL.

<Callout icon="lightbulb">
  When selecting tools, align them to mission constraints: latency, throughput, cost, security, and maintainability. For example, use `Amazon SageMaker` for managed training and deployment, `Amazon S3` for raw and processed data storage, and `AWS Glue` for ETL pipelines.
</Callout>

<Frame>
  <img alt="The image compares selecting the right tools to building rocket components, with icons representing elements like a rocket, fuel, and landing modules alongside algorithm, training framework, and AWS services." />
</Frame>

Not every mission requires every module — a cargo mission doesn't need a crew capsule, and a clustering problem doesn't require a classifier. Model training is your mission simulation: you reproduce conditions using historical data, iterate quickly, and validate assumptions before committing to production.

Before launch, NASA runs full mission simulations — orbit insertion, atmospheric re-entry, and communications checks — to ensure systems behave as expected. Likewise, training and validation are your simulation stage: run experiments, analyze failure modes, and iterate on feature engineering and hyperparameters until objectives and acceptance criteria are satisfied.

<Frame>
  <img alt="The image contains text comparing testing in wind tunnels to model training, explaining that machine learning involves models learning from historical data, accompanied by a simple robot icon." />
</Frame>

After the rocket passes tests it's launched; mission control then tracks telemetry, fuel, and trajectory. Similarly, once a model is deployed you must continuously monitor prediction quality, latency, and data drift. Instrumentation (logs, metrics, and alerts) enables mid-course corrections: retrain, roll back, or update features. Finally, a post-mission review (landing) assesses KPIs, cost, and the long-term plan for the model.

<Callout icon="warning">
  Monitoring and observability are critical. Without telemetry you can't detect data drift, performance regressions, or user-impacting issues. Design monitoring from day one and define thresholds and automated responses.
</Callout>

## ML Model Development Phases — Quick Reference

| Phase                 | What it means                                    | Typical AWS services & tasks                                 |
| --------------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| Design                | Define objectives, metrics, and success criteria | Documentation, metric definitions, experiment plans          |
| Assembly              | Prepare data, features, code, and pipelines      | `Amazon S3`, `AWS Glue`, feature stores, SageMaker notebooks |
| Testing               | Validate models (accuracy, fairness, robustness) | Cross-validation, A/B testing, SageMaker Experiments         |
| Launch                | Deploy model to production                       | SageMaker Endpoints, Batch Transform, CI/CD pipelines        |
| Mid-course correction | Monitor, detect drift, and update models         | CloudWatch, SageMaker Model Monitor, automated retraining    |
| Landing               | Post-deployment review and decommissioning       | Cost analysis, model registry cleanup, lessons learned       |

## Links and References

* [Amazon SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) — managed training and deployment.
* [Amazon S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) — object storage for datasets and artifacts.
* [AWS Glue](https://aws.amazon.com/glue/) — serverless ETL and data cataloging.

Use this mission-based framework to structure your ML projects on AWS: it helps teams communicate clearly, assign responsibilities, and instrument the right checkpoints from planning to final evaluation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/40a6e853-618a-4732-9605-1e0fce1ab5e6" />
</CardGroup>
