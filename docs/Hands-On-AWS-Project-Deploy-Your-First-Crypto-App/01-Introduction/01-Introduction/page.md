# Introduction

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Introduction/Introduction/page

Hands-on course on designing, provisioning, and operating scalable microservices on AWS with Terraform, ECS, ALB, IAM, and observability

Hello and welcome to the Building Scalable Microservices on AWS course.

I'm Raghunandana Sanur, your instructor for this course.

Why this matters for DevOps and SRE engineers: modern, large-scale services (for example, Netflix or Airbnb) serve millions of requests by adopting microservice architectures. This course explains what microservices are, how they evolved from monolithic systems, and why they form the backbone of scalable, resilient systems.

We will design and build an application on AWS beginning with a simple architecture and iteratively evolving it. Along the way, we'll intentionally make design choices that create trade-offs you'll revisit later—this helps you learn how design decisions affect scalability, reliability, and operability. By the end of the course you'll have deployed an application capable of handling large volumes of traffic.

<Frame>
  <img alt="The image shows a person speaking, wearing a black &#x22;KodeKloud&#x22; t-shirt, with text beside them listing &#x22;Microservices Architecture Basics&#x22; and &#x22;Building Application on AWS.&#x22;" />
</Frame>

What you'll build and learn:

* Core microservice design patterns and trade-offs for scalability and resilience
* How to provision and configure infrastructure on AWS (VPC, ECS, ALB, IAM)
* Deploying services with Terraform and CI-friendly workflows
* Observability and operational best practices for production systems

| Topic                     | Focus                                                      | Outcome                                                            |
| ------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------ |
| Microservice fundamentals | Architecture, bounded contexts, interservice communication | Understand when and how to split monoliths into services           |
| AWS infrastructure        | VPC, ECS, Load Balancers, IAM roles                        | Hands-on provisioning and configuration of a production-like stack |
| Automation with Terraform | Modules, state, lifecycle                                  | Reproducible infrastructure as code for repeatable deployments     |
| Observability & ops       | Logging, metrics, scaling                                  | Operational readiness to run microservices at scale                |

This course is hands-on. KodeKloud labs provide just-in-time access to sandboxed infrastructure so you can follow along and run the same commands used in the lessons.

Run this sample command to initialize and apply the provided Terraform stack in the lab environment:

```bash theme={null}
cd /app/_assets__/terraform-stack && terraform init && terraform apply
```

The labs execute real provisioning and configuration steps. A truncated example of Terraform output you may see during an apply:

```bash theme={null}
module.section_5[0].data.aws_vpc.default: Reading...
module.section_5[0].data.aws_ami.amazon_linux_2: Reading...
module.section_5[0].aws_cloudwatch_log_group.this: Creating...
module.section_5[0].aws_iam_role.ecs_instance_role: Creating...
module.section_5[0].aws_ecs_cluster.this: Creating...
module.section_5[0].tls_private_key.ssh_key: Creating...
module.section_5[0].aws_lb_target_group.this: Creating...
module.section_5[0].tls_private_key.ssh_key: Creation complete after 0s [id=az2q82334653a]
module.section_5[0].aws_iam_role.this: Creation complete after 0s [id=arn:aws:iam::42013480:role/ecs-instance-role]
module.section_5[0].data.aws_vpc.default: Read complete after 0s [id=vpc-0fd61b45fadf5c649]
module.section_5[0].data.aws_subnets.default: Reading...
module.section_5[0].aws_iam_role_policy_attachment.this: Creating...
module.section_5[0].data.aws_ami.amazon_linux_2: Read complete after 0s [id=us-east-1]
module.section_5[0].aws_key_pair.deployer: Creation complete after 0s [id=aws_key_pair.deployer]
module.section_5[0].aws_ecs_task_definition.this: Creating...
module.section_5[0].aws_iam_role_policy_attachment.ecs_instance_role_attachment: Creating...
module.section_5[0].data.aws_subnets.default: Read complete after 0s [id=us-east-1]
module.section_5[0].aws_lb_target_group.this: Creation complete after 0s [id=arn:aws:elasticloadbalancing:us-east-1:674182:targetgroup/cwb-app/75baf4cf0262585]
```

> **lightbulb** Labs provision real infrastructure during the exercises. Use the provided sandbox accounts and follow the lab cleanup instructions to avoid leftover resources.

This course is interactive — not just a list of commands. You will get hands-on challenges to implement solutions and verify them on AWS. Lessons include design rationale, operational considerations, and trade-offs so you learn not only how to build systems, but how to operate and scale them in production.

At KodeKloud, community matters. Join our learner community to ask questions, collaborate with peers, and share progress as you work through the labs.

If you're ready, let's dive in. For further reading and references:

* [AWS Documentation — Getting Started](https://aws.amazon.com/getting-started/)
* [Terraform Documentation](https://www.terraform.io/docs)
* [Designing Data-Intensive Applications (book)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/cde44ed4-309b-47fe-898a-419ecffde072/lesson/649bc75a-6daf-440f-ab03-cf93f2b7f892)
