# Introduction

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Course-Introduction/Introduction/page

A hands on course teaching TypeScript and CDK for Terraform to author, structure, and deploy AWS infrastructure including Lambda and IAM with practical labs and Terraform migration guidance.

Welcome to "CDK for Terraform with TypeScript."

I'm Simon Verhoeven — your instructor for this course. I have over a decade of experience in software engineering, spanning large-scale banking systems, AI startups, and serverless architectures on AWS. In this course we'll combine that experience with hands-on labs to teach you how to author, manage, and deploy cloud infrastructure using TypeScript and the Cloud Development Kit for Terraform (CDKTF).

This course is aimed at developers who want to automate cloud infrastructure with a modern developer experience. Whether you have front-end or back-end experience with JavaScript/TypeScript or you're moving from pure Terraform HCL, you'll find practical, project-oriented lessons that help you adopt infrastructure as code (IaC) effectively.

By the end of the course you will:

* Understand the CDKTF development workflow using TypeScript.
* Be able to scaffold and structure CDKTF projects with reusable constructs.
* Deploy AWS resources (IAM, Lambda, API Gateway) using CDKTF.
* Migrate an existing Terraform project into CDKTF.

> **lightbulb** If you're new to TypeScript or Terrafrom, start with the Modules 1–3 sequence: Course Introduction → TypeScript fundamentals → CDKTF basics. These build the foundation before moving into AWS-specific deployments.

## Course Overview

Below is a concise map of the course modules and what you’ll learn in each.

| Module                         | Focus                                   | Key outcomes                                                  |
| ------------------------------ | --------------------------------------- | ------------------------------------------------------------- |
| Module 1 — Course Introduction | Overview of IaC and automated workflows | Compare ClickOps with automated IaC, setup course environment |
| Module 2 — TypeScript          | TypeScript fundamentals for CDKTF       | Interfaces, classes, typing patterns used in CDKTF            |
| Module 3 — CDKTF               | CDKTF project structure and constructs  | Scaffold projects, create reusable constructs, synth/apply    |
| Module 4 — AWS with CDKTF      | Deploy AWS resources using CDKTF        | Configure AWS provider, IAM roles, Lambda, API Gateway        |
| Module 5 — Course Conclusion   | Best practices & migration              | Summarize takeaways, migrate Terraform → CDKTF                |

* Module 1 — Course Introduction: We’ll introduce core IaC concepts and demonstrate the differences between manual ClickOps and automated workflows. You’ll see short demos of manual setup followed by Terraform and CDKTF automation.

* Module 2 — TypeScript: Fundamentals and idiomatic TypeScript patterns you’ll use in CDKTF. We’ll cover type annotations, interfaces, classes, modules, and how to structure your code for reusability.

* Module 3 — CDKTF: Hands-on configuration of a CDKTF project, authoring constructs, synthesizing Terraform configuration, and applying changes. Best practices for structuring larger CDKTF codebases will be covered.

* Module 4 — AWS with CDKTF: We’ll connect to AWS, configure providers, and deploy common resources such as IAM roles, Lambda functions, and API Gateway endpoints. This module includes a practical lab where you deploy a Lambda function with the required IAM role and policy.

<Frame>
  <img alt="A slide-like screenshot showing the AWS &#x22;Sign up for AWS&#x22; page with the header &#x22;Connecting to AWS,&#x22; the AWS logo, and a password/signup form. A small circular webcam video of a person appears in the bottom-right corner." />
</Frame>

We will walk through a practical, hands-on lab to deploy a Lambda function along with its IAM role and policy, so you can see the end-to-end flow from TypeScript code to deployed AWS resources.

<Frame>
  <img alt="A presentation slide titled &#x22;Deploying Lambda Function&#x22; showing a diagram of a Lambda Function construct with a Lambda function linked to an IAM role that contains a policy. A small circular video thumbnail of the presenter appears in the bottom-right corner." />
</Frame>

* Module 5 — Course Conclusion: A final review of key concepts, recommended next steps for learning, and guidance on converting an existing Terraform HCL project to CDKTF.

<Frame>
  <img alt="A split-screen image: the left side shows a slide titled &#x22;CDK for Terraform with TypeScript&#x22; listing course sections, and the right side shows a man wearing glasses and a KodeKloud t-shirt speaking to the camera." />
</Frame>

Throughout the course you'll work through labs that reinforce each module's concepts, and you'll be encouraged to participate in community forums to ask questions and share progress.

> **warning** Deploying cloud resources can incur AWS charges. Use the provided lab accounts or the free tier when possible and remember to destroy resources after use (`cdktf destroy` or the AWS console).

## Quick TypeScript Example (used early in the course)

This simple example demonstrates importing a utility function and running it with ts-node. It’s the same pattern you’ll use when breaking up CDKTF projects into modules.

File: import-example.ts

```typescript theme={null}
// import-example.ts
export default function calculateTotal(prices: number[]): number {
  return prices.reduce((sum, p) => sum + p, 0);
}
```

File: app.ts

```typescript theme={null}
// app.ts
import calculateTotal from './import-example';

const prices: number[] = [10, 20, 30, 40];
const total = calculateTotal(prices);
console.log(`The total price is: ${total}`);
```

Run the example with ts-node:

```bash theme={null}
