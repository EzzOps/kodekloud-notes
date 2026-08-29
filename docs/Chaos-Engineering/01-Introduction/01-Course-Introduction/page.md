# Update the OS
sudo yum update -y

# Install Git
sudo yum install -y git
```

Clone the workshop repository and bootstrap the environment:

```bash theme={null}
git clone https://github.com/aws-samples/fis-workshop-experiments.git
cd fis-workshop-experiments

# Install Docker, kubectl, Node.js, AWS CDK, and other dependencies
bash bootstrap.sh
```

This script installs:

* Docker Engine
* Kubernetes CLI tools (`kubectl`, `eksctl`)
* Node.js and npm
* AWS CDK Toolkit (`npm install -g aws-cdk`)

## 4. Automate with CloudFormation (Optional)

Skip steps 1–2 by deploying our CloudFormation template. It creates both the IAM role and EC2 instance in one stack:

```bash theme={null}
aws cloudformation deploy \
  --template-file infrastructure/dev-environment.yaml \
  --stack-name fis-workshop-dev \
  --capabilities CAPABILITY_NAMED_IAM
```

***

## Cloud9 Deprecation & Alternative IDEs

AWS no longer provides preconfigured Cloud9 environments for new accounts as of July 2024. You can continue with your custom Cloud9 IDE, or choose one of these alternatives:

* [AWS Toolkit for VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [AWS Toolkit for JetBrains IDEs](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [AWS CloudShell](https://aws.amazon.com/cloudshell/)

![The image announces the deprecation of Cloud 9 IDE as of July 2024 and informs that the account does not have access to the Cloud9 service, suggesting alternatives like AWS Toolkits and AWS CloudShell.](https://kodekloud.com/kk-media/image/upload/v1752871954/notes-assets/images/Chaos-Engineering-Pre-requisite-to-Deploy-Application-Cloud-9-Deprecation/cloud9-ide-deprecation-notice-alternatives.jpg)

All scripts and detailed instructions are available in the [fis-workshop-experiments GitHub repository](https://github.com/aws-samples/fis-workshop-experiments).

***

## References

* [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/latest/guide/home.html)
* [AWS CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/index.html)
* [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
* [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/chaos-engineering/module/a6b84b48-a401-48a4-8278-0be5a8bb0d38/lesson/fccf590b-0c4f-44ee-b45a-aacea604f18c)


# Course Introduction

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Introduction/Course-Introduction/page

This lesson introduces chaos engineering using AWS Fault Injection Simulator to design and analyze fault-injection experiments for system resilience.

Welcome to this lesson on chaos engineering with AWS Fault Injection Simulator (FIS). I’m **Nasia Ullas**, and I’ll guide you through designing, executing, and analyzing fault-injection experiments to strengthen your system resilience.

As modern architectures grow in complexity, unexpected failures can lead to significant downtime costs:

* 44% of organizations report that **1 hour of downtime** costs between **\$1 million and \$5 million**.
* In 2021, Facebook incurred **\$80 million+** in losses from **seven hours** of downtime.
* A recent “blue screen of death” outage impacted airlines, banks, healthcare providers, and countless other businesses worldwide.

![The image shows a Windows blue screen error message indicating that the PC ran into a problem and needs to restart, with a progress indicator at 5% complete.](https://kodekloud.com/kk-media/image/upload/v1752871956/notes-assets/images/Chaos-Engineering-Course-Introduction/windows-blue-screen-error-restart.jpg)

Chaos engineering is the practice of intentionally injecting faults into a system to uncover weaknesses and validate its ability to withstand real-world disruptions. In this course, we’ll leverage [AWS Fault Injection Simulator (FIS)](https://aws.amazon.com/fis/) to conduct controlled experiments in your AWS environment.

***

## Course Outline

We’ll cover seven high-level modules, each focusing on different AWS services and fault types:

* **Module 1: Basic FIS Experiments**\
  Configure IAM, create experiment templates, execute tests, and monitor results with dashboards.

* **Module 2: Sample Application & Steady-State Metrics**\
  Deploy a reference application and define baseline performance metrics.

* **Module 3: Disk Fill Scenario on EC2**\
  Simulate disk saturation on EC2 instances and analyze its impact on application behavior.

* **Module 4: Aurora Reader Reboot**\
  Inject a reboot fault into an Aurora reader node and observe recovery processes.

* **Module 5: Fargate Load Stress Test**\
  Apply CPU and memory stress to a serverless Fargate task and evaluate performance under high load.

* **Module 6: EKS Memory Stress & Pod Deletion**\
  Perform memory saturation tests and pod-deletion experiments in your EKS cluster to validate self-healing.

* **Module 7: Availability Zone Power Interruption**\
  Simulate a power outage in an entire availability zone to assess multi-AZ resilience.

***

## Conclusion

By the end of this lesson, you’ll have a solid understanding of how to:

* Design robust failure scenarios for cloud applications.
* Execute controlled experiments safely.
* Analyze results to strengthen your system’s resilience.

Let’s get started and build more reliable, fault-tolerant architectures with AWS FIS!

***

## Further Reading

* [AWS Fault Injection Simulator Documentation](https://docs.aws.amazon.com/fis/latest/userguide/)
* [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
* [AWS X-Ray](https://aws.amazon.com/xray/)
* [Amazon EC2](https://aws.amazon.com/ec2/)
* [Amazon Aurora](https://aws.amazon.com/rds/aurora/)
* [AWS Fargate](https://aws.amazon.com/fargate/)
* [Amazon EKS](https://aws.amazon.com/eks/)

- [Watch Video](https://learn.kodekloud.com/user/courses/chaos-engineering/module/bb393f1a-9255-467e-8fbb-a2ddc0160053/lesson/4fa712b1-8c9c-458c-92d2-f3973b91b798)
