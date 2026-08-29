# CDKTF Introduction

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-CDKTF/CDKTF-Introduction/page

Guide to using CDKTF with TypeScript to scaffold local project files, covering prerequisites, init, synth and deploy workflows, CLI usage, and applying patterns to cloud providers.

Welcome to the CDKTF introduction module. This guide explains what CDKTF is, the prerequisites and tooling you need, and how to initialize a minimal TypeScript CDKTF project. We'll follow a practical example — Arthur's journey — to automate repetitive local project scaffolding using Terraform's local provider. This local example is a compact, hands-on way to introduce CDKTF concepts before applying them to cloud providers like AWS.

CDKTF (Cloud Development Kit for Terraform) lets you define and provision infrastructure using familiar programming languages (TypeScript, Python, Go, etc.) while taking advantage of Terraform's provider ecosystem and state management. It combines Terraform's declarative model with the expressiveness of general-purpose languages and constructs.

<Frame>
  <img alt="A developer icon points to a panel with two buttons labeled &#x22;Define&#x22; and &#x22;Provision.&#x22; Below the panel are logos for TypeScript, Python, Go, and Terraform." />
</Frame>

We assume you have a basic working knowledge of TypeScript. This lesson shows how to use that knowledge with CDKTF to provision resources locally (files) via Terraform's local provider, and prepares you to extend the same patterns to cloud providers later.

Overview

* Define the problem CDKTF will solve.
* Review prerequisites and essential tools.
* Initialize a TypeScript CDKTF project from scratch.
* Introduce the `cdktf` CLI and synth/deploy workflow.

Arthur's problem
Arthur frequently creates new projects and repeatedly types the same boilerplate files (for example `.gitignore`, `README.md`, `package.json`). In this module we automate generating those files locally using CDKTF + Terraform `local` provider. While a shell script might be the most pragmatic choice for production scaffolding, using CDKTF here teaches the core workflow and patterns you'll reuse with cloud providers.

Meet Arthur — repetitive project setup in a code editor (example Visual Studio Code):

<Frame>
  <img alt="A dark-themed Visual Studio Code window with the Explorer sidebar on the left, a right-click context menu open, and the integrated terminal visible along the bottom. The editor area is mostly empty with a large faint icon in the center." />
</Frame>

Typical files Arthur creates:

* `.gitignore`
* `README.md`
* `package.json` (for Node/TypeScript projects)

Example boilerplate files
package.json

```json theme={null}
{
  "name": "project-1",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  }
}
```

README.md

```markdown theme={null}
This is the project-1 project.
```

The idea: automate this repetitive work with CDKTF so Arthur can generate the same files consistently across projects.

Exploring CDKTF
Define Terraform resources using programming languages you already know, synthesize them into Terraform configuration, and apply via Terraform.

<Frame>
  <img alt="A presentation slide titled &#x22;Exploring CDKTF&#x22; showing the AWS Cloud Development Kit logo paired with the HashiCorp Terraform logo and the caption: &#x22;Allows you to define Terraform resources using familiar programming languages.&#x22;" />
</Frame>

Arthur chooses TypeScript because he is already familiar with it.

<Frame>
  <img alt="A presentation slide titled &#x22;Author's Decision&#x22; listing two choices. It shows using CDKTF to automate project setups and using TypeScript (with corresponding icons)." />
</Frame>

Prerequisites and tools
Before you start, install the tools listed below. These are the minimums required to run CDKTF with TypeScript.

| Tool                              | Purpose                                               | Notes / Links                                                                                                |
| --------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Node.js                           | Runtime for TypeScript tooling and package management | Install from [nodejs.org](https://nodejs.org/)                                                               |
| Terraform CLI                     | Applies the generated Terraform configuration         | Install instructions: [https://developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform) |
| cdktf CLI                         | Local CLI helper for CDKTF (optional global)          | Can be installed globally or added as a dev dependency per project                                           |
| Package manager (npm, Yarn, pnpm) | Install project dependencies                          | Use your team's preferred manager for reproducible builds                                                    |

<Frame>
  <img alt="A presentation slide titled &#x22;Install Node.js&#x22; showing bullet points to &#x22;Install Homebrew&#x22; and &#x22;Install node&#x22; with a link to the Node.js download page. The slide shows a KodeKloud copyright at the bottom." />
</Frame>

Install Terraform (example on macOS using Homebrew)

```bash theme={null}
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
brew update
terraform --version
```

Install the CDKTF CLI globally (optional)

```bash theme={null}
npm install -g cdktf-cli
cdktf --version
```

If you prefer not to install a global CLI (recommended for CI reproducibility), add `cdktf-cli` to each project as a dev dependency — CI runners will then use the local binary.

> **lightbulb** Using local Terraform state is convenient for demos and quick experiments, but it is not recommended for team or production environments. For collaborative workflows use remote state backends such as Terraform Cloud, S3 + DynamoDB locking, or other supported backends.

Initialize a new TypeScript CDKTF project

1. Create an empty directory and open a terminal there.
2. (Optional) Install the `cdktf` CLI globally or add it as a dev dependency.
3. Run the CDKTF init wizard to scaffold a TypeScript project.

Quick start

```bash theme={null}
