# Course Introduction and Objectives

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Course-Introduction/Course-Introduction-and-Objectives/page

Introduction to using TypeScript with CDK for Terraform to define, test, and deploy AWS infrastructure through hands-on labs and best practices for maintainable IaC.

Welcome to this lesson on the Cloud Development Kit for Terraform (CDKTF). This course teaches a code-first approach to provisioning cloud infrastructure using TypeScript and CDKTF. It’s designed for developers and DevOps professionals who want to define, test, and deploy infrastructure with familiar programming constructs and robust tooling.

## Overview

CDKTF combines the expressiveness of TypeScript with Terraform’s provider ecosystem. Instead of authoring HCL, you’ll use TypeScript classes, types, and IDE tooling to model infrastructure as code (IaC). This lesson emphasizes practical, hands-on labs and a repeatable local development environment so you can continue practicing beyond the course.

> **lightbulb** Throughout the lesson we’ll use hands-on labs for demonstrations. You’ll also get step-by-step guidance to set up the same environment locally so you can practice and iterate on your own machine.

## Who this course is for

| Audience                                                             | Why this course helps                                                                               |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Front-end or back-end developers familiar with JavaScript/TypeScript | Learn how to deploy applications and infrastructure using languages you already know.               |
| DevOps / Platform engineers                                          | Add TypeScript-based workflows to your Terraform toolset for better tests, abstractions, and reuse. |
| Engineers new to CDKTF                                               | No prior CDKTF experience required — basic Terraform concepts are helpful but not mandatory.        |

## What you will achieve

By the end of this lesson you will be able to:

* Explain core infrastructure-as-code concepts and where CDKTF fits in the IaC ecosystem.
* Understand why CDKTF is a strong option: use TypeScript constructs, static types, and IDE tooling to author infrastructure.
* Apply TypeScript fundamentals in the context of CDKTF projects.
* Use CDKTF to define resources, compose constructs, and apply best practices for maintainable IaC.
* Build and deploy practical AWS infrastructure including Lambda functions, IAM roles, and S3 buckets.
* Organize infrastructure code with constructs and patterns suitable for teams and long-lived projects.

## Course approach

* Hands-on labs and worked examples driven by TypeScript + CDKTF.
* Incremental learning: we begin with fundamentals and progress to real-world deployments.
* Practical guidance on structuring projects, testing infrastructure code, and managing Terraform state.

## Lesson plan (high level)

1. Environment setup and CDKTF project bootstrapping.
2. Defining resources in TypeScript and synthesizing Terraform JSON.
3. Using constructs to encapsulate and reuse infrastructure patterns.
4. Deploying to AWS: Lambda, IAM, S3 examples.
5. Testing, local iteration, and Terraform state management best practices.

## Prerequisites

* Basic familiarity with JavaScript or TypeScript.
* Recommended: a working installation of Node.js (LTS), npm or yarn, and an AWS account (for AWS labs).
* Optional: prior knowledge of Terraform fundamentals (providers, state) will accelerate learning but is not required.

> **warning** When you deploy real infrastructure, manage credentials and Terraform state carefully. Use secure mechanisms like environment-specific workspaces, remote state backends (e.g., S3 + DynamoDB), and avoid committing secrets or provider credentials to source control.

## What you’ll do in this lesson

* Set up a local CDKTF development environment.
* Create your first CDKTF TypeScript project and synthesize Terraform configuration.
* Deploy and test AWS resources (Lambda, IAM roles, S3) using CDKTF-generated Terraform.
* Learn patterns for organizing and testing infrastructure code using constructs.

## Links and references

* CDK for Terraform (CDKTF) docs: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* Terraform documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* TypeScript: [https://www.typescriptlang.org/](https://www.typescriptlang.org/)
* AWS docs: [https://docs.aws.amazon.com/](https://docs.aws.amazon.com/)

You will set up your development environment and create your first CDKTF project so you can start authoring infrastructure with TypeScript.

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/69389be2-0fe9-44bb-879a-f2224796ec79)
