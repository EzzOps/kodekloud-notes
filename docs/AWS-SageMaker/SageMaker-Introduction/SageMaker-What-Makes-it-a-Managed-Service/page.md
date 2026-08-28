# In [1]:
a = 10
b = 5
print(a + b)
# Output:
# In [2]:
prices = [500000, 600000, 650000, 44000, 127000]
for price in prices:
    print(f'Current price is {price}')
# Output:
# Current price is 500000
# Current price is 600000
# Current price is 650000
# Current price is 44000
# Current price is 127000
```

## Comparison with other Python environments

Jupyter Notebooks combine interactive execution, inline visualization, and narrative markdown — making them ideal for data exploration, reproducibility, and teaching. REPLs are interactive but lack integrated visualization and reproducibility features; IDEs excel at debugging, code navigation, and production development, but are less naturally suited to exploratory, step-by-step scientific workflows.

<Frame>
  <img alt="A slide titled &#x22;Solution: Comparison of Python Environments&#x22; showing a table that compares features (interactive coding, data visualization, text+code mix, reproducibility, collaboration, kernel support, teaching, debugging) across Jupyter Notebook, Python Shell, and Python IDE (e.g., PyCharm). Each cell uses checkmarks, warning icons, and crosses to indicate strengths, limitations, or lack of support." />
</Frame>

Use the table below to quickly compare environments by common use case:

|                   Resource Type | Best for                                                                  | Strengths                                                       |
| ------------------------------: | ------------------------------------------------------------------------- | --------------------------------------------------------------- |
|   Jupyter Notebook / JupyterLab | Exploratory data analysis, visualization, reproducible research, teaching | Inline plots, markdown + code, shareable .ipynb, easy iteration |
| Python REPL (interactive shell) | Quick experiments, learning                                               | Immediate feedback, minimal overhead                            |
|   Python IDE (VS Code, PyCharm) | Production apps, debugging, refactoring                                   | Advanced debugging, linting, project tooling, scalability       |

## Jupyter vs JupyterLab

Two common interfaces:

* Jupyter (classic): a simpler UI focused on one notebook at a time. Files use the .ipynb extension.
* JupyterLab: a modern, extensible IDE-like multi-pane interface. Supports multiple open files, terminals, and many extensions (Git integration, linters, documentation tools, vendor plugins).

JupyterLab includes a built-in terminal so you can install packages directly into the running environment without leaving the browser.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Jupyter Notebook vs Jupyter Lab&#x22; comparing the two tools. It shows two panels listing Jupyter's classic, single‑tab interface and JupyterLab's modern, multi‑pane, extensible IDE‑like workspace." />
</Frame>

### Example: install packages from a notebook-attached terminal

```bash theme={null}
# Install visualization libraries in the notebook environment
pip install matplotlib seaborn
```

## Files, version control, and collaboration

Notebooks are saved as .ipynb files that embed code cells, markdown cells, and the outputs produced by executed cells. For collaborative projects use version control (e.g., [Git](https://git-scm.com/)), but be mindful of large outputs and binary-encoded images included in notebooks.

<Callout icon="lightbulb">
  Best practice: Use markdown cells to explain intent and decisions, keep notebooks modular (one experiment per notebook or clear sections), and clear heavy outputs before committing. Consider tools like [nbstripout](https://github.com/kynan/nbstripout) or [nbdime](https://github.com/jupyter/nbdime) to produce cleaner diffs and reduce repository noise.
</Callout>

<Callout icon="warning">
  Warning: Never commit notebooks that contain secrets or credentials. Also avoid large binary outputs (heavy plots, full datasets); store data externally and load it at runtime to keep repositories lightweight.
</Callout>

## Summary

* Jupyter Notebooks provide an interactive, web-based environment ideal for exploratory data analysis, visualization, and reproducible experiments.
* They combine executable code, inline outputs (including charts), and rich markdown documentation to tell the story of your analysis.
* Choose JupyterLab for a multi-pane, extensible, IDE-like experience with integrated terminal and plugin support.
* Use traditional IDEs when you need advanced debugging, project organization, and production-ready development workflows.

## Links and references

* [Jupyter Project](https://jupyter.org/)
* [JupyterLab documentation](https://jupyterlab.readthedocs.io/)
* [Matplotlib](https://matplotlib.org/)
* [Seaborn](https://seaborn.pydata.org/)
* [Git documentation](https://git-scm.com/)
* [nbstripout](https://github.com/kynan/nbstripout)
* [nbdime](https://github.com/jupyter/nbdime)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/8dba4cbc-6eb7-4985-b97a-c5b7e6d23161/lesson/8edbb935-5bbf-42b2-9c79-9d5993284702" />
</CardGroup>


# SageMaker What Makes it a Managed Service

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-Introduction/SageMaker-What-Makes-it-a-Managed-Service/page

Explains managed vs unmanaged AWS services and how Amazon SageMaker abstracts infrastructure for ML workflows, highlighting benefits, trade-offs, and key features like notebooks, training, and hosting

In this lesson we examine managed vs unmanaged services on AWS, why AWS offers managed services, the trade-offs and benefits of using them, and how those concepts apply specifically to Amazon SageMaker. By the end you’ll understand what to expect when you choose SageMaker as your managed ML platform.

<Frame>
  <img alt="A dark-blue presentation slide from KodeKloud showing the title &#x22;AWS Managed Services&#x22; with the subtitle &#x22;Theory.&#x22; The KodeKloud logo appears at the top." />
</Frame>

<Callout icon="lightbulb">
  This lesson focuses on conceptual differences and practical consequences of choosing managed vs unmanaged services, with concrete examples (EC2, RDS) and how SageMaker leverages managed service patterns for ML workflows.
</Callout>

Agenda

* Define unmanaged vs managed services.
* Illustrate with EC2 (unmanaged) and RDS (managed).
* Describe benefits and challenges of managed services.
* Map managed-service concepts to Amazon SageMaker (notebooks, training, hosting).
* Summarize expected results when using SageMaker.

<Frame>
  <img alt="A presentation slide titled &#x22;Agenda&#x22; showing six numbered items. The points cover managed vs unmanaged services in AWS, the need and challenges of managed services, benefits, a workflow for building an AI platform, and expected results." />
</Frame>

Overview: approach used in this lesson

* First, contrast a low-level compute example (EC2) to show what “unmanaged” means.
* Next, compare that to a straightforward managed example (RDS) to highlight the operational differences.
* Finally, apply those same principles to SageMaker to explain how it abstracts infrastructure while exposing the controls ML teams need.

## Unmanaged services — EC2 example

Amazon EC2 (Elastic Compute Cloud) is a representative unmanaged service. When you launch and maintain EC2 instances, you are responsible for the full stack required to run and operate them:

* Create and manage an AWS account.
* Provision a VPC (virtual private cloud) and define subnets.
* Configure security groups, routing, and NACLs.
* Launch and manage the instance OS: patching, monitoring, backups.
* Configure high availability across Availability Zones, scaling, and failover.

You perform these tasks using the console, CLI, SDKs, or IaC tools (CloudFormation, Terraform). That approach provides maximum flexibility but also places the operational burden on your team.

<Frame>
  <img alt="A diagram titled &#x22;Managed vs Unmanaged Services in AWS&#x22; showing an AWS Cloud with a Virtual Private Cloud spanning two Availability Zones, each containing a public subnet, a security group, and an instance. Colored dashed boxes indicate the network and security boundaries." />
</Frame>

Because EC2 is “unmanaged” in this context, you trade convenience for control: full configurability at the cost of ongoing maintenance (patches, backups, scaling, redundancy).

<Frame>
  <img alt="A slide titled &#x22;AWS Unmanaged Services&#x22; with three numbered panels. Each panel describes aspects of unmanaged setups: Manual Setup (you provision VPCs, subnets, EC2, autoscaling), Full Control (complete flexibility), and Responsibility (you manage failover, redundancy, and updates)." />
</Frame>

## Managed services — concept and example

Managed services abstract and operate the underlying infrastructure for you. The cloud provider (AWS) provisions, monitors, patches, and maintains the service components while you consume higher-level primitives.

Example: Amazon RDS

* With RDS you request a managed database instance and optionally enable high availability.
* AWS takes care of provisioning, replication, automated backups, OS and database patches, and failover.
* A single configuration change or checkbox can enable replication and automatic failover across AZs.

Benefits of the managed approach:

* Reduces infrastructure complexity.
* Provides built-in scaling and availability patterns.
* Delivers faster time-to-value by removing low-level provisioning tasks.

<Frame>
  <img alt="A slide titled &#x22;AWS Managed Services&#x22; listing three benefits: 01 Abstracts Complexity, 02 Auto-Scaling and Availability, and 03 Faster Time-to-Value. Each box has a short explanation about AWS handling infrastructure, scaling, and quick startup." />
</Frame>

Operational advantage: AWS runs teams and tooling that handle monitoring, patching, and maintenance at scale—resources that would be costly for each team to duplicate.

<Frame>
  <img alt="A presentation slide titled &#x22;AWS Managed Services&#x22; showing two feature cards. One highlights &#x22;24/7 Support&#x22; for uptime and reliability, and the other lists &#x22;Minimal Maintenance&#x22; with scaling, updates, and fault tolerance." />
</Frame>

## SageMaker as a managed service for ML workflows

Amazon SageMaker applies the managed-service model specifically to ML development and production. It exposes higher-level constructs—hosted notebooks, training jobs, and endpoints—while AWS manages the underlying compute, networking, and container orchestration.

Key stages SageMaker supports and what it manages for you:

* Exploratory data analysis
  * Hosted, managed JupyterLab notebooks close to your data.
  * Avoids local hardware limits and simplifies secure data access.

* Data processing and training
  * Create discrete processing jobs or training jobs by declaring compute requirements and container images.
  * SageMaker provisions the necessary compute (EC2 instances), networking, and storage, and runs jobs reliably.

* Model hosting and inference
  * Deploy models to managed endpoints where SageMaker handles instance provisioning, autoscaling, rolling updates, and traffic-splitting (A/B, canary).
  * Supports managed multi-model endpoints and serverless inference (depending on use case).

Under the hood, SageMaker orchestrates VPCs, EC2 instances, containers, and storage for you while exposing controls for compute sizing, distributed training options, and scaling policies.

<Frame>
  <img alt="A presentation slide titled &#x22;SageMaker AI – Built-in Features and Integrations&#x22; showing three boxes: Permissions & Security, Compute & Storage, and Built-in Capabilities. Each box lists examples like AWS IAM, VPC, KMS; ECR and managed Jupyter notebooks; and prebuilt algorithms, autoscaling, and A/B testing." />
</Frame>

## Key integrations and built-in capabilities

SageMaker leverages many AWS services to provide a secure and scalable managed ML platform. The table below maps core integrations to their purpose:

| Integration                                | Primary use case                                          | Example                                                |
| ------------------------------------------ | --------------------------------------------------------- | ------------------------------------------------------ |
| AWS IAM                                    | Identity and fine-grained permissions                     | Roles for notebooks, training jobs, and S3 access      |
| Amazon VPC                                 | Network isolation and secure access to internal resources | Place processing/training jobs inside a custom VPC     |
| AWS KMS                                    | Encryption of data at rest and in transit                 | Encrypt S3 artifacts, EBS volumes, and model artifacts |
| Amazon ECR                                 | Container image storage for algorithms and custom code    | Host custom training/inference images                  |
| SageMaker built-in algorithms / containers | Rapid experimentation with optimized algorithms           | XGBoost, Linear Learner containers                     |
| Autoscaling & deployment strategies        | Production resilience and safe rollouts                   | Endpoint autoscaling, canary/A/B traffic shift         |

These integrations allow SageMaker to provide managed compute and storage while giving you the configurability needed for a variety of ML workloads.

<Frame>
  <img alt="Slide titled &#x22;SageMaker AI – Built-in Features and Integrations&#x22; showing user roles (Data Scientist, Developer, Business User) on the left connected to a central AI icon and a list of features on the right: Provisioning Compute, Managing Containers, Distributed Training, and Autoscaling and Deployment." />
</Frame>

## Operational behavior and flexibility

SageMaker manages infrastructure but keeps important levers in your control:

* Compute sizing: choose instance types (vCPU, memory, GPU).
* Parallelism and distribution: pick single-node or distributed training.
* Autoscaling and capacity: define autoscaling policies for endpoints.
* Deployment strategies: perform blue/green or canary rollouts and traffic-splitting.

This balance lets ML teams focus on model design, feature engineering, and evaluation while delegating low-level infrastructure and operational tasks to AWS.

<Callout icon="warning">
  Managed services provide strong operational benefits, but be aware of trade-offs: reduced control over low-level configuration, potential vendor lock-in, and the need to monitor managed costs. Evaluate these factors when designing your ML platform.
</Callout>

## Practical effects and advantages of using managed services like SageMaker

* Faster time-to-value: skip manual provisioning and move quickly into data work and model development.
* Focused expertise: data scientists spend more time on ML problems and less on ops.
* Rapid experimentation: quickly iterate on ideas with on-demand compute and managed environments.
* Reduced operational burden: AWS handles patching, monitoring, scaling, and failure remediation.

These benefits enable teams to iterate faster and focus resources on delivering ML-driven business value.

<Frame>
  <img alt="A slide titled &#x22;Managed Services – Effects and Advantages&#x22; with four numbered panels. They list benefits—Faster Results, Optimized Expertise, Quick Start, and Less Infrastructure Burden—each noting less time on infrastructure, more focus on ML, faster experimentation, and AWS handling scaling/failures." />
</Frame>

## Summary

* AWS offers both managed and unmanaged services. EC2 is a typical unmanaged service; RDS, S3, and SageMaker are examples of managed services.
* Managed services abstract much of the infrastructure provisioning and operations, reducing time to value and operational costs.
* The trade-off is less low-level control, but you retain the ability to specify compute sizing (CPU, memory, GPUs), distributed training behavior, and endpoint autoscaling.
* SageMaker applies managed-service principles to ML: hosted notebooks, managed training and processing jobs, containerized algorithms, distributed training, and autoscaled endpoints—helping teams prototype quickly and deploy models to production without managing the underlying infrastructure.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; that lists five numbered points comparing AWS managed vs unmanaged services and describing SageMaker's handling of infrastructure. The left side has a dark panel with the title and the right side shows turquoise numbered markers with short text about abstraction, control trade-offs, compute sizing/scaling, and faster time to value versus EC2/ECS." />
</Frame>

Further reading and references

* Amazon SageMaker documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* AWS general documentation: [https://docs.aws.amazon.com/](https://docs.aws.amazon.com/)
* EC2 overview: [https://docs.aws.amazon.com/ec2/index.html](https://docs.aws.amazon.com/ec2/index.html)
* Amazon RDS overview: [https://docs.aws.amazon.com/rds/index.html](https://docs.aws.amazon.com/rds/index.html)

That concludes this lesson. The course also includes an introduction to Jupyter notebooks and practical steps for starting exploratory data analysis in SageMaker.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/8dba4cbc-6eb7-4985-b97a-c5b7e6d23161/lesson/0926c0bf-627b-4901-841b-4ca86513bcbc" />
</CardGroup>
