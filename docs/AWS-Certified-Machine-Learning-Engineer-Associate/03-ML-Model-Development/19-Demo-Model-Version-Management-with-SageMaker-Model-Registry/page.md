# Demo Model Version Management with SageMaker Model Registry

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Demo-Model-Version-Management-with-SageMaker-Model-Registry/page

Guide to Amazon SageMaker Model Registry for versioning models, tracking metadata and evaluations, and enforcing approval workflows for reproducible, auditable deployments.

All right — let's walk through the Amazon SageMaker Model Registry and how it enables model version control, release gating, and reproducible deployments.

Whenever you write new code or collaborate on features you typically use Git for version control. Git lets multiple contributors work in parallel, preserves history, and enables rollbacks. The SageMaker Model Registry provides a comparable workflow for trained models: it organizes model artifacts, tracks metadata and evaluation results, and enforces approval workflows before models reach production.

The Model Registry uses model package groups (often referred to as model groups) as namespaces. Each registered model artifact becomes a model package (a version) in that group and is assigned a sequential version number. The registry stores metadata such as name, description, tags, creation time, and evaluation artifacts. It also supports approval states like `Approved`, `Rejected`, and `PendingManualApproval` so teams can gate which model versions are eligible for deployment.

Now, after you train or fine-tune a model, you can inspect registered models in [SageMaker Studio](https://learn.kodekloud.com/user/courses/aws-sagemaker).

<Frame>
  <img alt="The image shows the Amazon SageMaker Studio interface, specifically the &#x22;Models&#x22; section, with options for exploring, evaluating, and deploying models, including a spotlight on specific models like Qwen3.5-4B and Qwen3.5-9B." />
</Frame>

You can open My Models in SageMaker Studio to view a model group — think of it as a logical container that holds every version of a model. Each group includes a name, a description, and tags that capture ownership, purpose, and other contextual metadata.

Every time you retrain, fine-tune, or otherwise update a model, register the resulting artifact to the same model group. The registry preserves historical versions while adding the new one as a numbered model package so teams can:

* Compare versioned evaluation metrics and artifacts side-by-side.
* Roll back to a previous version if a newer release has issues.
* Enforce an approval gate to control which versions are promoted to production.

Key benefits at a glance:

| Feature              | Purpose                                        | Example/Notes                       |
| -------------------- | ---------------------------------------------- | ----------------------------------- |
| Model package groups | Logical namespace for related models           | `customer-churn-predictor`          |
| Versioning           | Sequential model packages per group            | Version 1, Version 2, ...           |
| Metadata & tags      | Ownership, dataset, hyperparameters, notes     | Tags: `team:payments`, `dataset:v2` |
| Evaluation artifacts | Metrics, confusion matrices, test data outputs | Stored with the model package       |
| Approval states      | Control deployment eligibility                 | `PendingManualApproval`, `Approved` |

How teams typically use the Model Registry (high-level steps):

1. Train or fine-tune a model artifact.
2. Register the artifact in a model package group (creates a version).
3. Attach evaluation artifacts and metadata (metrics, plots, notes).
4. Review and set the approval status for deployment.
5. Promote `Approved` versions to staging/production and monitor them.

Best practices

* Use clear, consistent naming for model package groups to make model discovery easier.
* Attach evaluation artifacts (metrics, visualizations) to each model package for traceable decisions.
* Enforce a manual approval step for production rollouts to reduce risk.
* Tag model packages with environment, team, and dataset version for reproducibility.

Links and references

* [SageMaker Model Registry Overview](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* [Amazon SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)

> **lightbulb** Use model groups to keep related model iterations together and use approval statuses to enforce a deployment gate — this helps with reproducibility, auditability, and safer rollouts.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/867c7a85-0ae4-4375-831e-96d08165860b)
