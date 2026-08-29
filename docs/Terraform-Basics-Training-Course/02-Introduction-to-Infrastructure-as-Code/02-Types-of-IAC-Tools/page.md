# Types of IAC Tools

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Introduction-to-Infrastructure-as-Code/Types-of-IAC-Tools/page

This article introduces Infrastructure as Code and reviews popular IAC tools for automating infrastructure provisioning and management.

In this article, we introduce the concept of Infrastructure as Code (IAC) and review several popular IAC tools that help automate the provisioning and management of infrastructure.

Traditionally, infrastructure provisioning was performed manually using the management consoles provided by various cloud providers. However, a more robust approach is to codify the entire provisioning process. By writing and executing code, you can define, provision, configure, update, and ultimately decommission infrastructure resources. This approach is known as Infrastructure as Code (IAC). With IAC, almost every component—such as databases, networks, storage systems, and application configurations—can be managed via code.

Consider the following example of a Bash shell script that provisions an [Amazon Elastic Compute Cloud (EC2)](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) instance, waits until it reaches a running state, verifies its status, and then associates an IP address with it:

```bash theme={null}
#!/bin/bash

IP_ADDRESS="10.2.2.1"

EC2_INSTANCE=$(ec2-run-instances --instance-type t2.micro ami-0edab43b6fa892279)

INSTANCE=$(echo ${EC2_INSTANCE} | sed 's/.*INSTANCE //; s/ .*//')
