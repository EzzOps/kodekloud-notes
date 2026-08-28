# Repositories

Source: https://notes.kodekloud.com/docs/AWS-CodePipeline-CICD-Pipeline/CICD-Pipeline-with-CodeCommit-CodeBuild-and-CodeDeploy/Repositories/page

This article explores repositories for AWS CI/CD pipelines, covering version control, collaboration, and integration with AWS services.

Welcome to the deep dive on repositories for your AWS CI/CD pipeline. In this lesson, we’ll explore how repositories enable version control, collaboration, and seamless integration with AWS services.

We’ll cover:

* What a repository is and its core benefits
* Git-based hosting: [GitHub][GitHub] and [Bitbucket][Bitbucket]
* AWS’s native Git service: [AWS CodeCommit][AWS CodeCommit]
* Using [Amazon S3][Amazon S3] as a pipeline source

By the end, you’ll know which repository solution fits your workflow and how it ties into AWS CodePipeline.

## What Is a Repository?

A repository (repo) is a version control system that records changes to files over time. With version control, you can:

* Revert to previous states without manual backups
* Collaborate across distributed teams
* Develop features or fixes on isolated branches
* Merge approved changes back into the main codebase

Instead of duplicating files before edits, a repo automates tracking, branching, and merging.

<Frame>
  ![The image shows a diagram with a central document surrounded by four developers, illustrating collaboration features like tracking changes, independent resolution, and simultaneous work.](https://kodekloud.com/kk-media/image/upload/v1752862652/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Repositories/collaboration-diagram-developers-document.jpg)
</Frame>

## Comparison of Repository Services

| Service        | Hosting Type   | Key Features                                         |
| -------------- | -------------- | ---------------------------------------------------- |
| GitHub         | Cloud Git      | Pull requests, branch protection, community packages |
| Bitbucket      | Cloud Git      | Free private repos, built-in pipelines               |
| AWS CodeCommit | Managed Git    | IAM integration, encryption, unlimited repo size     |
| Amazon S3      | Object Storage | File versioning, high durability (no Git workflows)  |

## GitHub

[GitHub][GitHub] is the most popular cloud-based Git hosting platform. Core workflows include:

* Creating or cloning repositories
* Committing changes with descriptive messages
* Pushing updates and opening pull requests
* Reviewing, approving, and merging code

These capabilities make GitHub ideal for open-source and enterprise projects alike.

## Bitbucket

[Bitbucket][Bitbucket] offers Git hosting with free private repositories and integrated CI/CD pipelines (Bitbucket Pipelines). It supports standard Git commands and can migrate repos into AWS CodeCommit for a fully AWS-centric workflow.

## AWS CodeCommit

[AWS CodeCommit][AWS CodeCommit] is a fully managed, cloud-native Git service. It supports all standard Git operations and integrates seamlessly with other AWS developer tools.

<Callout icon="lightbulb">
  AWS CodeCommit integrates natively with AWS IAM, enabling granular access control and audit trails.
</Callout>

<Frame>
  ![The image is a split graphic with information about AWS CodeCommit on the right, highlighting its features such as being an AWS service, cloud-based, supporting Git commands, and GitHub compatibility. The left side lists these features with corresponding color-coded icons.](https://kodekloud.com/kk-media/image/upload/v1752862654/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Repositories/aws-codecommit-features-graphic.jpg)
</Frame>

Key benefits:

* Fully managed backups, scaling, and maintenance
* Unlimited repository size—pay only for storage used
* Encryption at rest and in transit with IAM policies
* High availability with built-in redundancy
* Native integration with CodeBuild, CodeDeploy, and CodePipeline

<Frame>
  ![The image is a promotional graphic for AWS CodeCommit, highlighting features such as being fully managed, scalable, secure, highly available, and cloud-based.](https://kodekloud.com/kk-media/image/upload/v1752862654/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Repositories/aws-codecommit-promotional-graphic.jpg)
</Frame>

## Amazon S3

[Amazon S3][Amazon S3] serves as an alternative source for your pipeline, offering:

* File versioning to restore previous object versions
* Monitoring and lifecycle management

<Callout icon="triangle-alert">
  Amazon S3 does not support branches or pull requests like Git-based services. Use it for artifacts or simple file versioning only.
</Callout>

## Summary

In this lesson, we explored:

1. The role of a repository in version control and collaboration
2. Git hosting options: GitHub and Bitbucket
3. AWS CodeCommit’s managed Git features
4. Amazon S3 as a non-Git source with versioning

<Frame>
  ![The image is a summary slide listing four topics: "Repository and the benefits," "GitHub," "AWS CodeCommit," and "Amazon Simple Storage Service (AWS S3)."](https://kodekloud.com/kk-media/image/upload/v1752862655/notes-assets/images/AWS-CodePipeline-CICD-Pipeline-Repositories/repository-benefits-github-aws-s3.jpg)
</Frame>

Next, we’ll dive into AWS CodeBuild to automate build processes.

## Links and References

* [GitHub][GitHub]
* [Bitbucket][Bitbucket]
* [AWS CodeCommit][AWS CodeCommit]
* [Amazon S3][Amazon S3]

[GitHub]: https://github.com

[Bitbucket]: https://bitbucket.org

[AWS CodeCommit]: https://aws.amazon.com/codecommit/

[Amazon S3]: https://aws.amazon.com/s3/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline/module/8236e523-f637-4f0a-98c2-0accfd2cb74e/lesson/45c98db6-050a-415e-9c5d-5812382eea18" />
</CardGroup>
