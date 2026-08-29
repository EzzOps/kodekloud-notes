# Update packages, install and start Apache (Amazon Linux/CentOS style)
yum update -y
yum install -y httpd
systemctl enable httpd
systemctl start httpd

# Write a simple web page
echo "Hello from $(hostname -f)" > /var/www/html/index.html
```

How to view user data from inside an instance

* IMDSv1 (not recommended for new deployments):

```bash theme={null}
curl http://169.254.169.254/latest/user-data
```

* IMDSv2 (recommended — requires a session token):

```bash theme={null}
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/user-data
```

Retrieve user data via the AWS CLI

* Many EC2 API outputs provide the user data Base64-encoded; decode it after retrieval:

```bash theme={null}
# Describe the instance attribute (userData) and decode the Base64 value
aws ec2 describe-instance-attribute \
  --instance-id i-0123456789abcdef0 \
  --attribute userData \
  --query 'UserData.Value' \
  --output text | base64 --decode
```

> **warning** User data execution differs by OS and AMI:

  * Linux AMIs: usually processed by cloud-init (which supports multiple formats and modules).
  * Windows AMIs: processed by EC2Config or EC2Launch.
    If you require a script to run on every boot, configure the appropriate per-boot mechanism (cloud-init per-boot hooks, systemd units, or Windows Scheduled Tasks/Startup scripts) rather than relying on the one-time user data execution.

Links and references

* AWS EC2 user data and metadata: [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html)
* cloud-init documentation: [https://cloud-init.io/](https://cloud-init.io/)
* IMDSv2 (Instance Metadata Service Version 2): [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)
* AWS CLI: [https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

Further reading and patterns

* Use user data to fetch larger config or artifacts from S3, Git, or an artifact repository if your bootstrap exceeds the 16 KB limit.
* For immutable infrastructure, consider baking user data changes into a new AMI or using automation pipelines that rebuild instances with desired configuration.

- [Watch Video](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2/module/6b1df5fc-e1d3-4e1d-9dd1-035d0c2737d4/lesson/82b1483c-fccc-4f06-923b-dcfe0bd428a9)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2/module/6b1df5fc-e1d3-4e1d-9dd1-035d0c2737d4/lesson/61664800-7049-4ae2-ae54-b59b61fdf4ce)


# EC2 static and dynamic IP address

Source: https://notes.kodekloud.com/docs/Amazon-Elastic-Compute-Cloud-EC2/Basics-of-EC2/EC2-static-and-dynamic-IP-address/page

This guide explains how Amazon EC2 instances obtain public IP addresses, covering dynamic and static options for different workloads.

In this guide, you’ll learn how Amazon EC2 instances obtain public IP addresses—both dynamic and static—and when to choose each option for your workloads.

## Real-World Analogies

To understand EC2 public IP behavior, consider these everyday scenarios:

1. **Static allocation (phone number):**\
   When you purchase a SIM card, your mobile provider assigns you a permanent phone number. People can reach you consistently using that number.

2. **Dynamic allocation (hotel room):**\
   At a hotel, you get a room for the duration of your stay. Once you check out, the room returns to the pool and may be reassigned to someone else next time.

These maps neatly to AWS EC2’s public IP models:

* Static ⇨ Elastic IP
* Dynamic ⇨ Auto-assigned public IPv4 address

***

## Dynamic Public IP Addresses

![The image illustrates the structure of an AWS cloud setup, showing a region with an AWS account containing both a default and a custom VPC, each with their own public subnets, and a pool of public IPs.](https://kodekloud.com/kk-media/image/upload/v1752868983/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-static-and-dynamic-IP-address/aws-cloud-setup-vpc-structure-diagram.jpg)

### How Dynamic Public IPs Work

* **Default VPC:** EC2 instances launched in the default VPC receive a public IPv4 automatically.
* **Custom VPC:** Public IP assignment is disabled by default. Enable **Auto-assign public IPv4 address** on the subnet to grant instances a public IP on launch.

### Lifecycle and Limitations

![The image illustrates the concept of EC2 dynamic IP addresses within an AWS cloud environment, showing the relationship between AWS accounts, VPCs, and public subnets. It also notes that IPs are released back to the pool when instances are stopped, hibernated, or terminated.](https://kodekloud.com/kk-media/image/upload/v1752868984/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-static-and-dynamic-IP-address/ec2-dynamic-ip-aws-cloud-diagram.jpg)

* When an instance is **stopped**, **hibernated**, or **terminated**, its public IPv4 address is released back to AWS’s global pool.
* Restarting a stopped instance assigns a **new** public IP.
* You **cannot** manually associate or disassociate an auto-assigned public IP.
* Frequent IP changes can disrupt services with static DNS records.

> **lightbulb** Dynamic DNS services may take up to 24 hours to propagate a new IP, risking temporary downtime. For production-grade stability, consider Elastic IPs.

Learn more in the [AWS EC2 addressing guide][ec2-ip-addresses].

***

## Elastic IP Addresses (Static)

Elastic IPs are AWS’s solution for static, publicly routable IPv4 addresses—like owning a permanent phone number.

![The image is a diagram illustrating the concept of an EC2 Elastic IP Address within AWS Cloud, showing two regions (ap-southeast-1 and us-east-1) each containing an AWS Account.](https://kodekloud.com/kk-media/image/upload/v1752868985/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-static-and-dynamic-IP-address/ec2-elastic-ip-address-aws-diagram.jpg)

### Key Characteristics

1. **Region-bound:** You allocate an Elastic IP within a single AWS Region.
2. **Account-level allocation:** Once allocated, the address resides in your AWS account until you release it.
3. **Association:** Attaching to an EC2 instance binds the IP to eth0 (the primary network interface).
4. **Reassignment:** Disassociate and reattach to any eligible instance or network interface in the same region.
5. **Pricing:**
   * **Free** when attached to a running instance.
   * **Hourly charge** when allocated but not associated.

> **triangle-alert** Unused Elastic IPs incur charges. Always release any Elastic IP you no longer need to avoid unexpected costs.

For full details, see [Elastic IP address documentation][elastic-ip-docs].

***

## Comparing Static vs. Dynamic Public IPs

Below is a quick reference table summarizing the core differences between dynamic (auto-assigned) and static (Elastic) public IP addresses in EC2.

| Attribute         | Dynamic Public IP                     | Elastic IP (Static)                    |
| ----------------- | ------------------------------------- | -------------------------------------- |
| Assignment        | Auto-assigned on launch               | Allocated to your AWS account          |
| Lifetime          | Exists only while instance is running | Persists until you release it          |
| Manual Management | Not supported                         | You can associate/disassociate at will |
| DNS Stability     | IP changes on stop/start              | Fixed IP, no DNS propagation issues    |
| Cost              | Free while attached                   | Free when attached; charged when idle  |

![The image is a comparison table summarizing the differences between EC2 Static and Dynamic IP addresses, highlighting attributes such as region specificity, account assignment, and reallocation capabilities.](https://kodekloud.com/kk-media/image/upload/v1752868987/notes-assets/images/Amazon-Elastic-Compute-Cloud-EC2-EC2-static-and-dynamic-IP-address/ec2-static-dynamic-ip-comparison-table.jpg)

***

## Further Reading and References

* [AWS EC2 Public IPv4 Addresses][ec2-ip-addresses]
* [Amazon Elastic IP Addresses][elastic-ip-docs]
* [AWS EC2 Networking Concepts][ec2-networking]

[ec2-ip-addresses]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html#public-ip-addresses

[elastic-ip-docs]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html

[ec2-networking]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-networking.html

- [Watch Video](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2/module/6b1df5fc-e1d3-4e1d-9dd1-035d0c2737d4/lesson/126e3cce-ff21-40dc-b479-3105d76bca2e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2/module/6b1df5fc-e1d3-4e1d-9dd1-035d0c2737d4/lesson/d843a29b-5bfa-4edf-b848-80010ad9b489)
