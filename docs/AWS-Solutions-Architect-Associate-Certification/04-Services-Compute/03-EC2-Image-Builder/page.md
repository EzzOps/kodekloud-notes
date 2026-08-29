# Expected output:
# ec2.pem
# kubeseal-windows-installer/
# main.pem
# main2.pem
# test.code-workspace
# test.yaml
# wacom.pem
```

Use the SSH command with the following format to connect to your instance:

```bash theme={null}
ssh -i ec2.pem username@<PUBLIC_IP_OR_DNS>
```

Refer to the AMI documentation for the correct default username. For an Amazon Linux AMI, the username is typically "ec2-user". AWS also provides connection instructions when you click the "Connect" button. An example command is:

```bash theme={null}
chmod 400 ec2-demo.pem
ssh -i "ec2-demo.pem" ec2-user@ec2-3-88-162-255.compute-1.amazonaws.com
```

After executing the command, type "yes" when prompted to confirm the connection. Once connected, your prompt should look similar to the following:

```bash theme={null}
[ec2-user@ip-172-31-81-100 ~]$ ls
[ec2-user@ip-172-31-81-100 ~]$ ls -la
total 12
drwx------.  3 ec2-user ec2-user  74 Sep 28 23:43 .
drwxr-xr-x.  3 root     root       22 Sep 28 23:43 ..
-rw-r--r--.  1 ec2-user ec2-user 141 Jan 28  2023 .bash_profile
-rw-r--r--.  1 ec2-user ec2-user 492 Jan 28  2023 .bashrc
drwx------.  2 ec2-user ec2-user   29 Sep 28 23:43 .ssh
[ec2-user@ip-172-31-81-100 ~]$
```

> **lightbulb** Always ensure your PEM file permissions are set correctly using the chmod command (e.g., chmod 400 ec2-demo.pem) to avoid connection issues.

***

## Stopping and Terminating the Instance

To avoid unnecessary costs, it is important to stop or terminate your instance after use. To stop the instance, navigate back to the AWS console, select your instance, and choose "Stop instance" from the "Instance State" menu. The state will transition from "running" to "stopping" and finally to "stopped". You can restart, reboot, or hibernate the instance if needed.

![The image shows an AWS EC2 management console with details of a stopped instance named "ec2-demo-instance." The instance type is t2.micro, and it is located in the N. Virginia region.](https://kodekloud.com/kk-media/image/upload/v1752864830/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-EC2-Demo/aws-ec2-console-stopped-instance.jpg)

For complete cleanup and to prevent incurring additional charges, terminate the instance by selecting "Terminate" from the instance state options and confirming the action. After termination, the instance state will be updated to "terminated", and you will no longer be billed.

> **triangle-alert** Always terminate instances that are no longer in use to prevent unexpected billing charges.

***

This concludes our comprehensive guide on deploying, connecting to, and managing an Amazon EC2 instance. Enjoy your journey in cloud computing and explore more advanced AWS features to scale your infrastructure!

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/afe0c951-fe76-47f2-9fc4-18858721be70/lesson/efba7507-bb4d-4073-b95a-7d4938cd0a74)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/afe0c951-fe76-47f2-9fc4-18858721be70/lesson/c3240323-f7b9-486d-9574-628a009fa3e9)


# EC2 Image Builder

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Services-Compute/EC2-Image-Builder/page

EC2 Image Builder automates the creation, management, and deployment of customized AMI images for AWS accounts.

EC2 Image Builder is an AWS managed service designed to automate the creation, management, and deployment of customized AMI images. Whether you prefer to use the AWS Management Console, CLI, or APIs, EC2 Image Builder streamlines the process of producing tailored images for your AWS account.

![The image is a flowchart illustrating the process of using Amazon EC2 Image Builder to create AMIs (Amazon Machine Images) and deploy instances, with inputs from a console or CLI.](https://kodekloud.com/kk-media/image/upload/v1752864831/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-EC2-Image-Builder/amazon-ec2-image-builder-flowchart.jpg)

Organizations often start with a "golden image" when creating an AMI. A golden image is a pre-configured, fully provisioned master image that includes essential software applications, configurations, and settings. It acts as the definitive standard from which all subsequent instances are derived.

## How to Create a Golden Image

Follow these steps to create a golden image with EC2 Image Builder:

1. **Select a Base Image:**\
   Begin with a clean operating system installation like Ubuntu or macOS. This base image serves as your starting point for further customization.

2. **Build Phase:**
   * Install necessary applications and tools.
   * Remove any unwanted software packages to maintain a lean image.

3. **Customization:**\
   Adjust system and network settings and run any custom scripts to further tailor the image to your requirements.

4. **Testing Phase:**\
   Execute functional tests or security checks to confirm that the image meets your standards. While AWS offers built-in tests, you can also define custom tests suited to your environment.

5. **Distribution Phase:**\
   Specify the AWS regions where the image should be available and share it with other AWS accounts if needed.

Let's visualize this golden image creation process using EC2 Image Builder:

![The image illustrates the process of creating a "Golden Image" using EC2 Image Builder, involving steps like building, customizing, testing, and distributing from a source image.](https://kodekloud.com/kk-media/image/upload/v1752864832/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-EC2-Image-Builder/golden-image-ec2-image-builder.jpg)

During the build phase, a pre-existing AMI serves as the source image. Customizations such as adding or removing software packages, adjusting settings, and running scripts transform the image. After extensive testing to ensure both functionality and security, the image is distributed to your specified AWS regions or shared accounts.

## Deploying the Custom Image

Once your new image is ready, the process advances to the run stage. In this phase, deploy one or more EC2 instances using the custom image. You can manage this deployment seamlessly via the CLI, console, or SDK.

![The image is a flowchart illustrating the EC2 Image Builder process, including steps for building, testing, distributing, and running custom images.](https://kodekloud.com/kk-media/image/upload/v1752864833/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-EC2-Image-Builder/ec2-image-builder-flowchart.jpg)

## Automating Your Image Creation Pipeline

EC2 Image Builder allows you to automate the entire image creation pipeline. The process starts with specifying a source image and a build component (or "recipe"). Then, you configure the necessary infrastructure settings—such as VPCs, subnets, and security groups—for the build and testing phases. Finally, you set up the distribution configuration, which dictates where and how the image should be shared.

![The image illustrates the EC2 Image Builder Pipeline, showing the process from "Image Recipe" through "Infrastructure Config" and "Distribution Config" to create a "Golden Image."](https://kodekloud.com/kk-media/image/upload/v1752864834/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-EC2-Image-Builder/ec2-image-builder-pipeline-diagram.jpg)

> **lightbulb** * **Automated Image Creation:** Eliminates manual steps and minimizes human error.
  * **Enhanced Security:** Automates patch management and applies AWS or custom security policies.
  * **Consistent Workflows:** Ensures standardization across all deployments.
  * **Simplified Version Management:** Easily roll back to previous images if needed.

![The image lists five features: Automated Image Creation, Golden Image Creation, Simpler to Secure, Consistent Workflow, and Version Management, each with an icon.](https://kodekloud.com/kk-media/image/upload/v1752864835/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-EC2-Image-Builder/image-features-automation-icons.jpg)

By automating these processes, EC2 Image Builder significantly reduces manual efforts, minimizes security vulnerabilities, and guarantees consistent deployments across various environments.

For more detailed guidance and best practices, consider exploring the [AWS Documentation](https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html) and other related resources.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/afe0c951-fe76-47f2-9fc4-18858721be70/lesson/8b24ac17-6f13-4e6a-9d0f-f740df444d59)
