# Section Introduction

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Section-Introduction/page

Overview of MLOps comparing model deployment to satellite launches, covering CI/CD mapping, orchestration, monitoring, drift detection, reproducibility, and safe rollouts

Deploying a machine learning model is much like launching a satellite: both require careful design, rigorous testing, and continuous operations after launch. During development you test algorithms in simulators or offline environments—this corresponds to model training and validation. When the model is ready for production, you package and validate it (the "rocket design" phase), then finally launch it into a production environment, which is the deployment step.

<Frame>
  <img alt="The image is a slide titled &#x22;Deployment and Orchestration of ML Workflows,&#x22; describing the development phase where testing is done in simulators. There is also a graphic featuring a cube with a lightbulb on top and lines extending from the cube." />
</Frame>

Once launched, mission control continuously monitors the satellite and issues corrective commands as needed. Similarly, after a model is deployed you must continuously monitor its performance, detect drift, and apply updates or rollbacks when necessary. Operational practices—logging, metrics, alerting, canary tests, and automated rollback—are the mission-control procedures of production ML.

<Frame>
  <img alt="The image is about the &#x22;Deployment and Orchestration of ML Workflows,&#x22; showing a graphic of a person monitoring multiple screens with charts, emphasizing the need for constant monitoring and tweaks post-launch." />
</Frame>

CI/CD pipelines for ML act like a launch readiness sequence. Below is a concise mapping that helps you design robust MLOps workflows and automated gates.

| CI/CD Phase                 | Launch Analogy                          | Typical ML Activities                                                                        |
| --------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------- |
| Continuous Integration (CI) | Rocket assembly & subsystem tests       | Unit tests, data validation, feature transforms, model training runs, reproducibility checks |
| Continuous Delivery (CD)    | Staging and rollout of mission software | Model packaging, containerization, staging deployment, canary or blue/green releases         |
| Automated Checks & Gates    | Pre-launch checklists                   | Validation tests, performance thresholds, security scans, bias and fairness checks           |
| Orchestration & Monitoring  | Mission control & telemetry             | Scheduling pipelines, automatic retries, monitoring, drift detection, alerts, rollbacks      |

Translate these phases into concrete automation: versioned datasets and models, reproducible training pipelines, artifact registries, deployment manifests, and monitoring dashboards. Orchestration platforms (e.g., workflow schedulers, Kubernetes operators, or managed MLOps services) coordinate these steps so releases are safe and repeatable.

<Frame>
  <img alt="The image outlines the deployment and orchestration of ML workflows, comparing CI/CD pipelines to NASA's launch readiness sequence, with focus on continuous integration and continuous delivery." />
</Frame>

> **lightbulb** Think of MLOps as the combination of aerospace engineering and operations: careful pre-launch validation plus continuous post-launch monitoring and correction. This ensures models remain safe, accurate, and maintainable in production.

## Quick Reference and Further Reading

* MLOps & Model Deployment best practices: CI/CD, reproducibility, monitoring, and governance.
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) — orchestration for containerized model services.
* [Terraform Registry](https://registry.terraform.io/) — infrastructure as code for reproducible deployments.
* [Docker Hub](https://hub.docker.com/) — container images for model serving.

Use this section as a foundation: map your ML lifecycle to CI/CD stages, automate repeatable steps, and instrument production models with telemetry to detect drift and enable safe rollbacks.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/1da86b89-b352-43f7-be8e-0a265622dc66)
