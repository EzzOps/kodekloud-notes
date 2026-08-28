# Demo Source Code reference and download

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Code-Editor-Setup-and-Source-Code/Demo-Source-Code-reference-and-download/page

Guide to a GitHub repository of AWS CloudFormation demo templates with usage instructions for cloning, validating, and deploying templates for learning and reference

Welcome — this short guide highlights the source code used in the demos and explains how to access and use it as a reference for AWS CloudFormation work. The repository contains the finished CloudFormation templates used throughout the course. Cloning the repo and experimenting locally is the best way to track changes and learn.

Repository (final CloudFormation templates)

* GitHub: [https://github.com/kodekloudhub/AWS-CloudFormation](https://github.com/kodekloudhub/AWS-CloudFormation)

Files included in the repo (representing final templates and artifacts):

| Filename          | Purpose / Usage                                                                             | Last modified             |
| ----------------- | ------------------------------------------------------------------------------------------- | ------------------------- |
| imports.yaml      | Shared Imports or mappings used by parent stacks                                            | Upload #1 — 7 minutes ago |
| intro.yaml        | Template used in the initial CloudFormation demonstration (used directly in the intro demo) | Upload #2 — 2 minutes ago |
| parent.yaml       | Parent stack that may reference nested stacks                                               | Upload #1 — 7 minutes ago |
| s3-bucket.yaml    | Example S3 bucket resource definition                                                       | Upload #1 — 7 minutes ago |
| simple-ec2.yaml   | Simple EC2 instance stack for demos                                                         | Upload #1 — 7 minutes ago |
| simple-s3.yaml    | Minimal S3 stack used in examples                                                           | Upload #1 — 7 minutes ago |
| ssm.yaml          | Systems Manager (SSM) configuration or association examples                                 | Upload #1 — 7 minutes ago |
| stack-policy.json | Example stack policy for protecting resources during updates                                | Upload #1 — 7 minutes ago |
| stackset.yaml     | StackSet example for multi-account / multi-region deployment                                | Upload #1 — 7 minutes ago |

One template in particular—intro.yaml—is referenced directly in the opening demonstration. Other files are used as final results or referenced by demos that combine pieces from multiple templates.

<Frame>
  <img alt="A dark-themed screenshot of a GitHub repository showing a file list of CloudFormation YAML files (cfn-init.yaml, cli.yaml, drift.yaml, ec2-instance.yaml, imports.yaml, intro.yaml, parent.yaml, s3-bucket.yaml). The right sidebar shows repository activity, watchers/forks info and a Releases section." />
</Frame>

How to get the repository

* Download ZIP: Click the "Code" button on the GitHub page and choose "Download ZIP".
* Clone with Git (recommended for tracking changes):

```bash theme={null}
git clone https://github.com/kodekloudhub/AWS-CloudFormation.git
```

Quick start recommendations

1. Clone the repository to your local machine.
2. Inspect templates to understand resource layout and parameters (start with `intro.yaml` and `parent.yaml`).
3. Validate templates locally with the AWS CLI:
   * aws cloudformation validate-template --template-body file://intro.yaml
4. When ready to deploy, use CloudFormation package/deploy steps (or the Console) to create stacks and observe the results.
5. Track changes with git and use branches for experimentations.

<Callout icon="lightbulb">
  This repository is intended as a reference for following along with the demos. Clone the repo and apply the templates locally so you can explore changes, validate templates, and safely iterate on your CloudFormation learning.
</Callout>

Links and references

* [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/index.html)
* [AWS CLI CloudFormation commands](https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]index.html)
* GitHub repo: [https://github.com/kodekloudhub/AWS-CloudFormation](https://github.com/kodekloudhub/AWS-CloudFormation)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/2e29934e-5554-4599-9f9b-5cdc229e9f2c/lesson/4d6615fc-6543-4481-a1c9-0926482e65c4" />
</CardGroup>
