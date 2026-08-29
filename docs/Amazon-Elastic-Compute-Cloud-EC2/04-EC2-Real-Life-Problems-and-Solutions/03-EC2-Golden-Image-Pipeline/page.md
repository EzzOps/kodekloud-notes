# Create a lifecycle policy for daily snapshots
aws dlm create-lifecycle-policy \
  --description "Daily snapshot policy for critical volumes" \
  --state ENABLED \
  --resource-types VOLUME \
  --schedules "Name=DailySchedule,CopyTags=true,TagsToAdd=[{Key=Backup,Value=Daily}],CreateRule={Interval=24,IntervalUnit=HOURS}"
```

### Restoring from a Snapshot

```bash theme={null}
# Restore a volume from a snapshot
aws ec2 create-volume \
  --availability-zone us-west-2a \
  --snapshot-id snap-1234567890abcdef0 \
  --volume-type gp3 \
  --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=RestoredVolume}]'
```

## References

* [Amazon EC2 User Guide](https://docs.aws.amazon.com/ec2/)
* [AWS Backup Documentation](https://docs.aws.amazon.com/backup/)
* [Amazon Data Lifecycle Manager](https://docs.aws.amazon.com/dlm/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2/module/1132ee02-eae9-44e0-a8a5-8f325254ba92/lesson/a82025fe-d813-43e6-b14c-cdb6d77029c8" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2/module/abe7fd58-449e-4102-b73c-b0f2e63b1c3f/lesson/5d472900-44c3-4355-9ffd-4ff4822bc5ac" />
</CardGroup>


# EC2 Golden Image Pipeline

Source: https://notes.kodekloud.com/docs/Amazon-Elastic-Compute-Cloud-EC2/EC2-Real-Life-Problems-and-Solutions/EC2-Golden-Image-Pipeline/page

This article discusses using golden AMIs in an immutable infrastructure approach to streamline EC2 instance management and address common operational challenges.

Cloud administrators often tackle scaling challenges that drive up costs and complexity. In this lesson, we follow Alex at Acme Corporation as he manages hundreds of EC2 instances across development, staging, and production. We’ll explore common pitfalls—like configuration drift and version upgrades—and demonstrate how an immutable infrastructure approach using golden AMIs can streamline operations.

***

## Case Study: Acme Corporation’s AWS Infrastructure

Acme operates three environments—development, staging, and production—each hosting front-end (Nginx) and back-end services (Node.js, Go). Rapid growth led to dual back-ends on some apps, increasing operational overhead.

| Environment | Front-end | Back-end    |
| ----------- | --------- | ----------- |
| Development | Nginx     | Node.js, Go |
| Staging     | Nginx     | Node.js, Go |
| Production  | Nginx     | Node.js, Go |

<Frame>
  ![The image is a diagram of the Acme Corporation's AWS cloud environment, showing production, staging, and development stages with components like Nginx, Node.js, and Go. It also indicates frontend and backend sections.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869076/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-Golden-Image-Pipeline/acme-corporation-aws-cloud-diagram.jpg)
</Frame>

***

## Common Challenges

### 1. Configuration Drift

Over time, developers applied manual updates and installed varying software versions across environments. As a result, staging no longer mirrors production, making debugging unpredictable.

<Frame>
  ![The image is a diagram illustrating "Configuration Drift" in AWS Cloud, showing different environments (Production, Staging, Development) with varying software versions and configurations across two environments.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869077/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-Golden-Image-Pipeline/configuration-drift-aws-diagram.jpg)
</Frame>

### 2. Version Upgrade Complexity

Compliance mandates a uniform Nginx version, but automating upgrades can fail in edge cases. Skipped releases or unexpected behavior complicate rollbacks and extend maintenance windows.

<Frame>
  ![The image illustrates a version upgrade process within AWS Cloud, showing different environments (Production, Staging, Development) across two environments with version numbers and Nginx icons. It also includes icons representing business, development, and management processes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869078/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-Golden-Image-Pipeline/aws-version-upgrade-process-diagram.jpg)
</Frame>

### 3. Security Vulnerability Remediation

A critical Node.js vulnerability forces Alex to:

1. Identify which environments run the affected version
2. Patch or upgrade them—risking compatibility issues if untested builds are deployed

Automation tools can scan and update instances, but handling live servers remains error-prone.

***

## Potential Approaches

Traditional configuration management (Ansible, Chef) enforces state but often leads to lengthy runs and unpredictable outcomes on mutable servers. An immutable infrastructure pattern—where servers are replaced rather than modified—offers greater consistency and reliability.

<Frame>
  ![The image shows a comparison between Ansible and Chef, with their respective icons and names, under the heading "Solution."](../../../../images/kodekloud.com/kk-media/image/upload/v1752869079/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-Golden-Image-Pipeline/ansible-chef-comparison-solution-icons.jpg)
</Frame>

***

## Golden AMI Solution

A **golden AMI** is a versioned, pre-configured image containing the OS, patches, monitoring agents, and application runtimes. By rebuilding these images via a pipeline, you eliminate drift, simplify upgrades, and accelerate vulnerability remediation.

<Callout icon="lightbulb">
  Tag each AMI with metadata (version, build date, environment) and use [AWS Launch Templates](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html) to ensure consistent instance provisioning.
</Callout>

### Image Building Pipeline

Each pipeline stage produces a new AMI, feeding into the next:

| Stage | Input AMI                  | Actions                                                      | Output AMI     |
| ----- | -------------------------- | ------------------------------------------------------------ | -------------- |
| OS    | Base AMI (AWS Marketplace) | Kernel updates, OS upgrades, security patches                | OS-stage AMI   |
| Tool  | OS-stage AMI               | Install monitoring agents (CloudWatch Agent), security tools | Tool-stage AMI |
| Tech  | Tool-stage AMI             | Install Nginx, Node.js, Go runtimes                          | Tech-stage AMI |

<Frame>
  ![The image illustrates an "Image Building Process" pipeline, showing stages from Base OS to Tools and Technology, with components like Patch, Security, and CloudWatch, leading to different AMI outputs.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869081/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-Golden-Image-Pipeline/image-building-process-pipeline-ami.jpg)
</Frame>

### Deployment Strategy

Once golden AMIs are built, roll them out in sequence:

| Environment | Trigger                     | Timing                |
| ----------- | --------------------------- | --------------------- |
| Development | Successful Tech-stage build | Immediate             |
| Staging     | After 24 h of testing       | Next day              |
| Production  | Post-staging validation     | Scheduled maintenance |

<Frame>
  ![The image illustrates a "Golden AMI Solution" with an image build process creating different AMIs (ami-789, ami-900, ami-901) and their deployment across AWS Cloud environments: Production, Staging, and Development.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869082/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-Golden-Image-Pipeline/golden-ami-solution-image-build-process.jpg)
</Frame>

Automating image builds and progressive rollouts ensures consistent environments, simplifies version management, and accelerates security patches—addressing drift, upgrades, and vulnerabilities in one streamlined workflow.

***

## References

* [AWS EC2 AMIs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
* [Immutable Infrastructure Patterns](https://martinfowler.com/bliki/ImmutableServer.html)
* [AWS Launch Templates](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2/module/1132ee02-eae9-44e0-a8a5-8f325254ba92/lesson/dbadcfb7-796e-474f-bb46-3e736cc0e5c6" />
</CardGroup>
