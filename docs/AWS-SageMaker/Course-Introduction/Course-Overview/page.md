# Course Overview

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Course-Introduction/Course-Overview/page

A practical hands on AWS SageMaker course teaching end to end ML pipelines, labs, and role based workflows for data engineers, data scientists, and MLOps engineers.

Welcome to the AWS SageMaker course. I'm Alistair Sutherland, your guide through practical, production-focused machine learning with AWS SageMaker. SageMaker is AWS's managed platform for building, training, and deploying machine learning models at scale. Organizations such as Intuit, Thomson Reuters, Siemens, Airbnb, and GE Healthcare rely on SageMaker for its collaboration features, scalability, and integrated MLOps tooling.

This course emphasizes hands-on learning: concise lectures paired with practical labs so you can apply concepts immediately and gain real-world experience.

<Frame>
  <img alt="A screenshot of the AWS SageMaker lab interface showing step-by-step notebook setup instructions on the left and a terminal panel on the right. A small circular video overlay of an instructor appears in the bottom-right corner." />
</Frame>

By working directly in SageMaker you can experiment, iterate, and learn from real mistakes — the fastest path to technical proficiency and confidence when building ML systems.

<Frame>
  <img alt="A screenshot of the AWS SageMaker &#x22;Create notebook instance&#x22; page showing a success message for creating an IAM role and configuration options for root access, encryption, network, Git repositories, and tags. A circular video overlay in the bottom-right shows a presenter." />
</Frame>

<Callout icon="lightbulb">
  This course is practical-first. Expect short conceptual lectures followed by lab exercises in SageMaker Studio and the AWS Console so you can practice data preprocessing, model training, deployment, and monitoring workflows.
</Callout>

## Course structure — what you'll learn

Below is a high-level view of the course modules and what each covers:

| Module                      | Focus                                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------- |
| Prerequisites & Foundations | Core ML concepts, data basics, and environment setup                                        |
| The ML Pipeline             | Data collection, preprocessing, model training, evaluation, deployment, and monitoring      |
| Just Enough Math            | Essential math to understand model behavior and training dynamics                           |
| Confidence Blockers         | Troubleshooting, debugging training jobs, and common pitfalls in SageMaker and ML workflows |

Each module includes clear labs and step-by-step exercises using a real-world dataset (house prices) so you learn the end-to-end pipeline.

## Who this course is built for — three personas

We introduce three personas to focus lab tasks and show which responsibilities align with common job roles. This helps you see practical, role-based workflows in SageMaker.

| Persona        | Primary Responsibilities                                                             | Lab focus                                                              |
| -------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| Data Engineer  | Ingesting, cleaning, transforming, and building scalable data pipelines              | Data preparation for the house price dataset                           |
| Data Scientist | Feature engineering, experiment management, efficient model training, and evaluation | Model training, hyperparameter tuning, and tracking experiments        |
| MLOps Engineer | Automation, deployment, CI/CD, inference pipelines, and production monitoring        | Endpoint automation, deployment pipelines, and monitoring integrations |

* Data Engineer: prepares and processes datasets, ensuring pipelines are repeatable and scalable.
* Data Scientist: focuses on feature engineering, efficient model training, experiment management, and lifecycle tracking inside collaborative tooling.

<Frame>
  <img alt="A slide titled &#x22;Data Scientist&#x22; shows a diagram from a data scientist icon to three tasks: Data Exploration, Feature Engineering, and Model Training and Evaluation. A small presenter video circle is visible in the bottom-right." />
</Frame>

* MLOps Engineer: automates endpoint provisioning, builds inference pipelines, integrates CI/CD, and implements production-grade monitoring. We'll also cover how monitoring signals can trigger retraining workflows.

## Hands-on environments: Console, Studio, and collaborative tooling

We begin with the two primary SageMaker interfaces:

* AWS Management Console — quick tasks, resource overview, and ad-hoc notebook instances.
* SageMaker Studio — an integrated IDE (JupyterLab, code editor, experiment manager and terminals) designed for collaborative workflows.

You’ll learn key SageMaker constructs such as Domains, User Profiles, Studio notebooks, and how to manage collaborative spaces so teams can reproduce experiments reliably.

## Labs, community, and next steps

Each section includes labs that build on one another. Work through the exercises in order to reinforce concepts and create a portfolio of reproducible ML workflows.

* Join the KodeKloud community to discuss labs, ask questions, and share solutions.
* Track your experiments, version your data and models, and practice deploying repeatable CI/CD pipelines.

<Callout icon="warning">
  Running training jobs, endpoints, and managed instances in AWS may incur charges. Be sure to stop or delete resources when not in use. Review the AWS pricing pages for SageMaker to estimate costs.
</Callout>

## Links and references

* [AWS SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [SageMaker Studio Overview](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)
* [KodeKloud Community Forums](https://kodekloud.com/) (course discussion and peer support)

Are you ready to master SageMaker and become an indispensable part of the modern ML workforce? Let’s get started.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/a5b9a001-9205-4423-b395-957fee84177a/lesson/cb0a68f6-4db8-4f43-8012-1934d2fcfe63" />
</CardGroup>
