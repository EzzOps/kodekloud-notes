# Network Access Controls for ML Resources

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Solution-Monitoring-Maintenance-and-Security/Network-Access-Controls-for-ML-Resources/page

Guide to securing cloud ML workloads using AWS VPCs, security groups, VPC endpoints, IAM, and monitoring to protect SageMaker, S3, and EC2 resources.

Secure network design is essential when you run machine learning workloads in the cloud. This guide explains how to apply layered network access controls to protect ML data, models, and compute—focusing on AWS primitives and recommended configurations for SageMaker, S3, and EC2.

<Callout icon="lightbulb">
  This lesson explains how VPCs, security groups, VPC endpoints, IAM roles/policies, and AWS Config combine to create defense-in-depth for ML resources such as SageMaker, S3, and EC2.
</Callout>

<Frame>
  <img alt="The image illustrates network access controls for ML resources using AWS VPC and AWS Shield, displayed with respective icons." />
</Frame>

## Why network access controls matter

Start with the core ML services:

* SageMaker — training and hosting managed by AWS.
* S3 — storage for datasets, model artifacts, and checkpoints.
* EC2 — custom compute for training, preprocessing, or serving.

Applying network controls (VPCs, security groups, VPC endpoints) prevents unauthorized access and reduces the attack surface. Complement these controls with AWS Shield for DDoS protection at the edge and IAM for fine-grained authorization.

<Frame>
  <img alt="The image is an illustration explaining the use of network access controls for machine learning (ML) resources, featuring icons representing ML tools like SageMaker, S3, and EC2, followed by network controls such as VPC, SGS, and Endpoints, leading to secure and isolated access." />
</Frame>

## Core AWS network primitives for ML

Use the following AWS building blocks to secure ML workloads. They work together to isolate traffic, enforce least privilege, and keep data on the AWS network.

| Resource                                                                                    | Purpose                                                               | When to use                                                                                        |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [VPC (Virtual Private Cloud)](https://aws.amazon.com/vpc/)                                  | Isolates network resources and defines routing.                       | Always: deploy SageMaker, EC2, and related services inside a VPC for isolation.                    |
| [Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) | Instance-level, stateful allow-lists for inbound/outbound traffic.    | Control access to instances and endpoints; prefer narrow rules (source IPs / SGs and port ranges). |
| [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html)        | Keeps traffic to supported AWS services off the public internet.      | Use gateway endpoints for S3/DynamoDB and interface endpoints (PrivateLink) for other AWS APIs.    |
| [IAM policies and roles](https://aws.amazon.com/iam/)                                       | AuthZ controls for who/what can perform actions and access resources. | Enforce least privilege for training jobs, inference, and data access.                             |

<Frame>
  <img alt="The image lists AWS tools for network access controls, including VPC, Security Group, and VPC Endpoint." />
</Frame>

## Design pattern: place ML resources inside a VPC

Best practice: run SageMaker training/hosting, EC2 instances, and any custom endpoints inside a VPC with private subnets that do not route directly to an Internet Gateway. This approach keeps both management and data-plane traffic within your controlled network boundaries and reduces exposure to the public internet.

* Use private subnets for compute and model hosting.
* Use NAT/egress proxies only when necessary and lock them down.
* Centralize shared services (artifact stores, logging, model registries) in controlled VPCs or via VPC peering/Transit Gateway.

<Frame>
  <img alt="The image is a diagram illustrating the configuration of a VPC for machine learning resources, showing the connection between SageMaker, a VPC (Private Network), and isolated subnets with no internet." />
</Frame>

## Security groups: allow only the minimum

Security groups are your first line of defense for instance-level traffic:

* Permit inbound traffic only from trusted IP ranges or other security groups (use security group IDs for cross-instance communication).
* Limit access to required ports (e.g., 443 for HTTPS).
* Avoid 0.0.0.0/0 or overly broad CIDR blocks on sensitive ports.

If you need subnet-level, stateless controls use [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html), but favor security groups for stateful, instance-level protection and flexibility.

<Frame>
  <img alt="The image is a diagram showing the configuration of security groups for machine learning resources, allowing only trusted IPs/ports and blocking all other traffic." />
</Frame>

## VPC endpoints: keep traffic on the AWS network

Routing service traffic over the public internet increases exposure. Use VPC endpoints to keep communication internal to AWS:

* Gateway endpoints — for S3 and DynamoDB. Add a route in your route table so resources in private subnets reach S3 without leaving the AWS network.
* Interface endpoints (AWS PrivateLink) — create private ENIs to access many AWS service APIs and supported partner services.

Using endpoints ensures model artifacts and data transferred between SageMaker and S3 (or other AWS services) do not traverse the public internet.

<Frame>
  <img alt="The image is a diagram illustrating the configuration of VPC endpoints for machine learning resources, showing a flow from SageMaker to an S3 bucket via a VPC Endpoint." />
</Frame>

## Integrating IAM with network controls

Network controls and IAM should be used together for defense-in-depth:

* Create IAM roles with least privilege for SageMaker training jobs, inference, and any EC2 instances.
* Use resource-based policies (S3 bucket policies, VPC endpoint policies) to restrict which principals and networks can access artifacts.
* Combine IAM restrictions with VPC placement and security group rules so compromised credentials alone are not sufficient to exfiltrate sensitive data.

<Frame>
  <img alt="The image illustrates integrating IAM with network controls, showing a flow from IAM Role to VPC + Security Groups, and finally to accessing ML resources securely." />
</Frame>

## Monitoring, compliance, and drift detection

Continuously validate and audit network configurations:

* Use [AWS Config](https://aws.amazon.com/config/) to codify desired states for VPCs, subnets, security groups, and endpoints.
* Monitor changes and get automated compliance reports and alerts for drift from the baseline.
* Integrate AWS Config with AWS CloudWatch Events, Lambda, or Systems Manager Automation for automated remediation.

<Frame>
  <img alt="The image illustrates a process flow for &#x22;Security and Compliance With Network Controls,&#x22; showing steps involving AWS Config, monitoring VPC and Security Groups, and generating a Compliance Report." />
</Frame>

<Callout icon="warning">
  Anti-patterns to avoid: wide-open security groups (0.0.0.0/0 on sensitive ports), sending ML traffic over the public internet instead of using VPC endpoints, and assigning overly broad IAM admin permissions where scoped roles would suffice.
</Callout>

## Anti-patterns (concise)

* Allowing 0.0.0.0/0 on sensitive ports.
* Not using VPC endpoints for S3/model traffic.
* Granting broad administrative IAM permissions to service roles.

## Summary: key action items

1. Use VPCs and private subnets to isolate ML workloads from the public internet.
2. Apply least-privilege security groups—allow only required sources and ports.
3. Add VPC endpoints (gateway or interface) so traffic to AWS services stays private.
4. Combine scoped IAM policies and roles with network controls for defense-in-depth.
5. Continuously monitor configurations with AWS Config and remediate drift.

<Frame>
  <img alt="The image is a slide titled &#x22;Summary and Action Items&#x22; with five steps: using VPC for isolation, restricting SGs, adding VPC endpoints, combining IAM with network controls, and monitoring with AWS." />
</Frame>

## Links and references

* [AWS VPC overview](https://aws.amazon.com/vpc/)
* [Amazon SageMaker](https://aws.amazon.com/sagemaker/)
* [Amazon S3](https://aws.amazon.com/s3/)
* [EC2](https://aws.amazon.com/ec2/)
* [VPC endpoints](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html)
* [Security groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
* [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
* [AWS IAM](https://aws.amazon.com/iam/)
* [AWS Config](https://aws.amazon.com/config/)
* [AWS Shield](https://aws.amazon.com/shield/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/e07ceb86-4976-4c8e-a6f8-3518534ec115/lesson/92024dcb-e77f-41fe-a56b-127664992822" />
</CardGroup>
