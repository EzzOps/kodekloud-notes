# Creating of ECS cluster

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Deploying-serivce-on-to-ECS/Creating-of-ECS-cluster/page

Guide to creating an Amazon ECS EC2 launch type cluster via the AWS Console, covering CloudFormation provisioning, Auto Scaling, networking, capacity setup, and monitoring.

Hello and welcome to this lesson.

In this guide you'll create the Amazon ECS cluster used to deploy our application. The walkthrough covers the AWS Console steps, what happens behind the scenes (CloudFormation/Auto Scaling), and where to inspect the resources created for the cluster.

Before you begin, verify these prerequisites:

* AWS region is set to the region you want to use.
* You have IAM permissions to create ECS, EC2, CloudFormation, and Auto Scaling resources.
* A VPC and subnets available in that region (or be ready to select them during cluster creation).

<Callout icon="lightbulb">
  Ensure you have the correct AWS region selected and sufficient [IAM](https://learn.kodekloud.com/user/courses/aws-iam) permissions ([ECS](https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs), [EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2), [CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation), [Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)) before creating the cluster.
</Callout>

Step-by-step: create an ECS cluster (EC2 launch type)

1. Open the ECS console. If you frequently use ECS, add it to bookmarks; otherwise type “ECS” in the AWS console search and choose Amazon ECS.

<Frame>
  <img alt="The image shows the AWS Management Console home screen, displaying recently visited services, applications, AWS health status, and cost usage information." />
</Frame>

2. Click Create cluster.

3. Configure basic cluster settings:
   * Give the cluster a clear name (I used `production-cluster`).
   * Leave the default namespace unless you need to configure an AWS Cloud Map service discovery namespace.
   * For infrastructure, choose the launch type:
     * Select Amazon EC2 when you need control over underlying instances (custom AMIs, GPUs, specific instance types, or host-level configuration).
     * Choose AWS Fargate for serverless compute with no EC2 instance management.

Keep most other options at defaults unless you have specific networking or instance requirements.

<Frame>
  <img alt="The image shows the Amazon Elastic Container Service (ECS) web interface where a user is configuring a cluster named &#x22;ProductionCluster&#x22; with infrastructure options such as AWS Fargate and Amazon EC2 instances." />
</Frame>

4. Set capacity (Auto Scaling group) details:
   * Desired capacity: number of EC2 instances to start with (example uses `0`).
   * Maximum capacity: upper limit to scale to (example uses `5`).
   * Note: setting desired capacity to `0` means no instances will be launched until you scale the ASG or use ECS Capacity Providers with Managed Scaling. Without managed scaling, you must increase the ASG desired capacity manually.

5. Select VPC and subnets:
   * Choose subnets according to whether your instances need public IPs or only private connectivity.
   * Remove private subnets if you want instances launched into public subnets only.
   * Ensure security group selection allows required traffic (SSH for debugging, container ports, etc.).

<Frame>
  <img alt="The image shows the AWS Elastic Container Service (ECS) console where a user is configuring a cluster. It displays the selection of VPC and subnets, as well as options for selecting a security group." />
</Frame>

6. Review your settings and click Create.

What happens after you click Create

* When you create an ECS cluster with the EC2 launch type via the console, AWS triggers a CloudFormation stack on your behalf. The stack provisions the underlying infrastructure: Auto Scaling group, launch template (or configuration), EC2 instances, security groups, IAM roles/policies, and related resources.
* Use the “View in CloudFormation” button from the ECS console to inspect the stack progress.

7. Monitor CloudFormation provisioning:
   * In the CloudFormation console you can follow stack events, inspect created resources, and view the current stack status as it moves from CREATE\_IN\_PROGRESS to CREATE\_COMPLETE.

<Frame>
  <img alt="The image shows the AWS CloudFormation console with details of an ECS cluster stack labeled &#x22;Infra-ECS-Cluster-ProductionCluster-f94c4edb.&#x22; The stack status is &#x22;CREATE_IN_PROGRESS,&#x22; and the overview provides information such as stack ID, description, and creation time." />
</Frame>

8. Inspect stack resources and events:
   * The Resources tab lists the physical AWS resources created by the stack (ASG, Launch Template, IAM roles, etc.).
   * The Events tab shows a timestamped sequence of resource creation and status updates.

<Frame>
  <img alt="The image shows an AWS CloudFormation console displaying stack details for &#x22;Infra-ECS-Cluster-ProductionCluster-f94c4edb.&#x22; The events tab highlights various stack events with their timestamps, logical IDs, and statuses, most of which indicate &#x22;CREATE_COMPLETE.&#x22;" />
</Frame>

9. Return to the ECS console after CloudFormation completes:
   * Refresh the Clusters page and open your cluster. You should see it listed as active.
   * From the cluster details you can view services, tasks, and other cluster-level information.
   * We will use an ECS service to run and maintain our application tasks in a later lesson.

ECS exposes infrastructure-level cluster details:

* Click the Infrastructure tab to view capacity providers, container instances, and the Auto Scaling group associated with the cluster.

<Frame>
  <img alt="The image shows the AWS Management Console for Amazon Elastic Container Service (ECS), displaying details of a production cluster under the &#x22;Infrastructure&#x22; tab, with sections for capacity providers and container instances. The console has filters and options for tasks and service management." />
</Frame>

Adjusting cluster capacity and monitoring

* Quick capacity change: edit the Auto Scaling Group to update desired/min/max instance counts.
* Managed scaling: consider using ECS Capacity Providers with Managed Scaling to automate instance scale-in/scale-out based on workload.
* Alternatively, adjust the desired count of your ECS service (this will launch tasks, and if capacity providers are configured, scale instances accordingly).
* Use the Metrics tab for basic cluster metrics—CPU and memory utilization, registered container instances, and running tasks—to monitor health and scaling behavior.

Summary of typical resources created by the CloudFormation stack:

| Resource Type                          | Purpose                                                      |
| -------------------------------------- | ------------------------------------------------------------ |
| Auto Scaling Group (ASG)               | Manages EC2 instance fleet for the cluster                   |
| Launch Template / Launch Configuration | Defines EC2 instance details (AMI, instance type, user data) |
| EC2 Instances (container instances)    | Hosts for running container tasks (EC2 launch type)          |
| IAM Roles & Policies                   | Permissions for ECS agent, instances, and CloudFormation     |
| Security Groups                        | Network access rules for instances and control plane         |

<Callout icon="warning">
  Creating EC2 instances and associated infrastructure incurs AWS charges. Clean up unused clusters, Auto Scaling groups, and stacks when not needed to avoid unexpected costs.
</Callout>

Next steps

* With the ECS cluster ready, the next lesson will cover creating a task definition and deploying an ECS service to run your application on this production cluster.

Links and references

* [Amazon ECS — Getting started](https://docs.aws.amazon.com/ecs/latest/developerguide/what-is-ecs.html)
* [ECS Capacity Providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-capacity-providers.html)
* [AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/index.html)
* [Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/a5f47c01-ffdc-4186-8d6b-2b5189000482/lesson/91fce09d-eb17-4c33-9876-159a5fe9ecfb" />
</CardGroup>
