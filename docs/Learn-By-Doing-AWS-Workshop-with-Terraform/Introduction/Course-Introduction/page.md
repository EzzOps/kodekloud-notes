# Create a graph builder that uses this state shape
builder = StateGraph(GraphState)
```

## Benefits and common reducer patterns

Reducers are plain functions—easy to write, test, and reuse. They help with:

* Accumulation (lists of messages, logs, search results)
* Idempotence (avoid duplicate entries)
* Cleanup (remove or redact temporary or sensitive fields)
* Centralized business logic (same reducer reused across graphs)

|      Pattern | Use case                                   | Example                                             |
| -----------: | ------------------------------------------ | --------------------------------------------------- |
|   Accumulate | Keep chat history or logs                  | `messages: Annotated[list, add_messages]`           |
|  Merge lists | Combine tool outputs over time             | `tool_results: Annotated[list, merge_tool_results]` |
| Prune/Redact | Remove diagnostics or transient fields     | Reducer that returns `None` or filters keys         |
|      Replace | Single authoritative value (intent/status) | Default merge or reducer that returns `new`         |

## Reuse and modularity

Because reducers are normal functions, you can import them across graphs to keep merging logic centralized. This enforces consistent state behavior across different flows and makes testing straightforward.

<Frame>
  <img alt="The image is about reusing reducers across graphs, highlighting that reducers are functions that can be imported and plugged into different flows and keep business logic centralized." />
</Frame>

This separation promotes modular design: the graph describes structure and control flow, while reducers encapsulate state semantics. Nodes stay focused on producing outputs; reducers define how those outputs become part of the canonical state.

<Callout icon="lightbulb">
  Use field-level reducers to centralize accumulation and cleanup logic (e.g., chat history, tool logs, diagnostic traces). This avoids ad-hoc state manipulation inside nodes and prevents accidental overwrites.
</Callout>

## Best practices

* Define reducers for any field that represents accumulated history or logs.
* Keep reducers small and focused so they are easy to unit test.
* Use reducers to strip or redact sensitive data before it becomes persistent.
* Reuse reducers across graphs to maintain consistent state behavior.

## Summary

State reducers are foundational for predictable state evolution in LangGraph. They let you implement intelligent merging, prevent accidental overwrites, and keep your nodes simple. Use field-level reducers to centralize accumulation, cleanup, and deduplication logic so your graph's shared state remains reliable and auditable.

## Links and references

* [LangGraph documentation](https://langgraph.example/docs)
* Python: `typing_extensions` documentation
* Pattern references: accumulation, idempotence, and cleanup techniques in stateful systems

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-b366-4c4d-95d0-bce0c24aaf58/lesson/d4a0ce6a-78a6-41e5-8802-89f7b76e974c" />
</CardGroup>


# Course Introduction

Source: https://notes.kodekloud.com/docs/Learn-By-Doing-AWS-Workshop-with-Terraform/Introduction/Course-Introduction/page

Hands-on AWS Terraform workshop teaching infrastructure as code, state management, modules, CI/CD integration, and a final EC2 and RDS deployment project.

Welcome to the Learn-by-Doing course: AWS Workshop with Terraform.

Instructors:

* Vijin Palazhi
* Harshita Joshi

This hands-on workshop is built for DevOps engineers, system administrators, and cloud professionals who want to provision and manage AWS infrastructure using Terraform. Through practical labs you'll learn how to apply Terraform best practices to build scalable, secure, and maintainable cloud environments.

What you will learn

* How to install and configure Terraform and integrate it with AWS
* Writing infrastructure as code with HCL (HashiCorp Configuration Language) using `hcl-lang` concepts
* Managing Terraform state (local and remote backends) and locking
* Using advanced Terraform features: modules, workspaces, and provisioners
* Automating deployments and integrating Terraform with CI/CD pipelines
* Troubleshooting and debugging Terraform configurations
* Final project: deploy secure EC2 instances connected to a shared RDS database

Key learning outcomes:

* Write clear, reusable Terraform modules
* Manage state safely across teams
* Automate repeatable, auditable AWS deployments

Before you start the labs

* Treat the Overview tab as your course material and the Tasks tab as your step-by-step workbook.
* The Overview page is the default for each lab. It contains the lab description, temporary AWS credentials, and any important setup notes.
* Use the provided temporary AWS credentials shown on the Overview page (Access Key ID and Secret Access Key). You can retrieve them at any time in the lab environment using the `show creds` command.

<Frame>
  <img alt="The image shows a coding lab interface with an instruction panel for setting up Terraform with AWS on the left and a VS Code web interface with a terminal on the right." />
</Frame>

Lab workflow tips

* Follow the Overview for conceptual material and the Tasks tab for hands-on steps.
* Use the Hint and Solution tabs when you need help; use the Check button to validate task completion.
* Progress through labs in order—each lesson builds on the previous one so concepts and configurations will be introduced incrementally.

Course topics at a glance

| Topic                                        | What you'll practice                           | Example outcome                                     |
| -------------------------------------------- | ---------------------------------------------- | --------------------------------------------------- |
| Introduction to Terraform & AWS fundamentals | Learn core concepts and terminology            | Understand providers, resources, and HCL basics     |
| Setup Terraform with AWS                     | Configure CLI, credentials, and providers      | `terraform init` with AWS provider                  |
| Writing Terraform configurations             | Declare resources and outputs in HCL           | Create VPC, subnets, and security groups            |
| Managing Terraform state                     | Local vs remote backends and locking           | Configure `terraform backend` in S3/DynamoDB        |
| Advanced Terraform features                  | Modules, workspaces, and provisioners          | Build reusable modules and isolated workspaces      |
| Automating AWS deployments                   | CI/CD pipelines and automation patterns        | Integrate Terraform with GitHub Actions or Jenkins  |
| Troubleshooting Terraform                    | Debugging plans, graphs, and state issues      | Use `terraform plan` and `terraform state` commands |
| Final project: EC2 + RDS                     | Deploy production-like infrastructure securely | Launch EC2 instances connected to an RDS database   |

<Frame>
  <img alt="The image is a course topics overview for a Terraform course, listing topics such as Introduction to Terraform, Setup with AWS, Writing Configurations, Managing Terraform State, Advanced Features, Automating Deployment, Troubleshooting Terraform, and a Final Project with EC2 & RDS." />
</Frame>

Final project
The course culminates with a practical project where you'll apply everything learned to deploy secure EC2 instances that connect to a shared RDS database. This final lab emphasizes real-world architecture, secure configuration, and automation patterns.

<Callout icon="lightbulb">
  Tip: If you ever lose access to the temporary credentials for a lab, use the `show creds` command in the lab environment to retrieve them again.
</Callout>

Ready to begin?
Now that you understand the course layout and lab workflow, proceed to the first lab to start writing Terraform configurations and provisioning AWS resources.

Links and references

* HCL (HashiCorp Configuration Language): [https://hcl-lang.org](https://hcl-lang.org)
* Terraform documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* AWS documentation: [https://docs.aws.amazon.com/](https://docs.aws.amazon.com/)
* Related courses: [EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2), [RDS](https://learn.kodekloud.com/user/courses/aws-rds)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-by-doing-aws-workshop-with-terraform/module/78a13681-22b1-4517-b446-c01767507311/lesson/637e1844-709b-4784-a33e-158dd68857e6" />
</CardGroup>
