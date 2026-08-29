# __main__.py
import pulumi
from pulumi_aws import s3, ec2

# Create an S3 bucket
bucket = s3.Bucket('my-bucket')

# Export the name/ID of the bucket
pulumi.export('bucket_name', bucket.id)

# Create an EC2 instance. Replace ami with an AMI ID valid in your region.
ec2_instance = ec2.Instance('web-server',
    ami="ami-053b0d53c279acc90",    # replace with a region-appropriate AMI
    instance_type="t3.nano",
    key_name="test1",
    tags={
        "Name": "web"
    }
)

# Export the public IP of the instance so Pulumi prints it after creation.
# Note: this value will only be set if the instance receives a public IP (e.g., launched in a subnet
# with auto-assign public IP enabled or by specifying associate_public_ip_address).
pulumi.export('public_ip', ec2_instance.public_ip)
```

> **lightbulb** AMI IDs are region-specific. Select an AMI appropriate for your region (for example, Ubuntu 22.04 LTS) from the EC2 console or query the AWS CLI. See the EC2 console's Launch Instance workflow for the image's AMI ID.

To find and copy an AMI ID from the AWS Console, open the EC2 Launch Instance workflow and choose the desired image (Ubuntu in this example). Paste the AMI ID into the `ami` field of the code above.

<Frame>
  <img alt="A screenshot of the AWS EC2 &#x22;Launch Instance&#x22; console showing the Amazon Machine Image selection (Ubuntu Server 22.04 LTS) on the left and a summary panel on the right with the instance type (t2.micro), storage details, and a &#x22;Launch instance&#x22; button." />
</Frame>

EC2 instance arguments at a glance:

| Resource Field | Purpose                                                  | Example                   |
| -------------- | -------------------------------------------------------- | ------------------------- |
| ami            | The AMI ID to use for the instance (string).             | `"ami-053b0d53c279acc90"` |
| instance\_type | Instance size/flavor.                                    | `"t3.nano"`               |
| key\_name      | Name of an existing EC2 key pair for SSH access.         | `"test1"`                 |
| tags           | Key/value tags for easier identification in the console. | `{"Name":"web"}`          |

Run pulumi up to preview and apply the changes. The preview shows the planned resources:

```console theme={null}
$ pulumi up

Previewing update (dev)

    Type                          Name               Plan
pulumi:pulumi:Stack              pulumi-demo-dev
└─ aws:ec2:Instance              web-server          create

Outputs:
  + public_ip : output<string>

Resources:
  + 1 to create
    2 unchanged

Do you want to perform this update? [Use arrows to move, type to filter]
> yes
```

After you confirm, Pulumi will create the EC2 instance and print outputs, including the public IP once the instance receives one:

```console theme={null}
Updating (dev)

    Type                              Name               Status
pulumi:pulumi:Stack                 pulumi-demo-dev
+  aws:ec2:Instance                  web-server         created (13s)

Outputs:
    bucket_name: "my-bucket-5d138fe"
+   public_ip  : "34.205.89.1"

Resources:
  + 1 created
  2 unchanged

Duration: 15s
```

With the public IP printed, SSH into the instance using the PEM file for the key pair you specified. For an Ubuntu AMI, the default user is `ubuntu`:

```bash theme={null}
ssh -i test1.pem ubuntu@34.205.89.1
```

> **warning** By default, the security group attached to a new EC2 instance may not allow SSH from the internet. If you cannot connect, check the instance’s Security Group inbound rules and ensure SSH (port 22) is allowed from your IP (or an appropriate CIDR). Restrict access to your IP rather than opening SSH to 0.0.0.0/0 whenever possible.

Troubleshooting checklist:

* Verify the AMI ID is valid in your AWS region.
* Confirm your key pair name matches an existing key pair and you have the corresponding PEM file.
* Inspect the instance’s public IP in Pulumi outputs or the EC2 console.
* Check Security Group inbound rules to allow SSH from your IP.
* Ensure the instance was launched in a subnet that provides/associates a public IP or explicitly set associate\_public\_ip\_address if needed.

References and further reading:

* Pulumi AWS provider: [https://www.pulumi.com/docs/reference/pkg/aws/](https://www.pulumi.com/docs/reference/pkg/aws/)
* EC2 documentation: [https://docs.aws.amazon.com/ec2/](https://docs.aws.amazon.com/ec2/)
* Finding AMIs in the AWS Console: [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html)

<Frame>
  <img alt="A screenshot of the AWS EC2 console displaying an instance's Details and Security sections, including public IP, VPC/subnet, launch time, and security group inbound/outbound rules. The left sidebar shows EC2 navigation options like Instances, Images, and Elastic Block Store." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/pulumi-essentials/module/883d8d6f-c8be-44af-ac4d-ba0835d32f5d/lesson/84cfaf53-946e-4164-943e-82555a2374d6)


# Creating Security Group

Source: https://notes.kodekloud.com/docs/Pulumi-Essentials/Pulumi-Essentials/Creating-Security-Group/page

This article demonstrates creating and managing a custom security group with Pulumi for EC2 instances, including configuring rules and deploying multiple instances.

In this lesson, we'll demonstrate how to create and manage a custom security group using Pulumi, ensuring that only the required ports are open for your EC2 instances. You'll configure a security group with two inbound rules (SSH and HTTP) and one outbound rule (allowing all outbound traffic). We'll attach this security group to an EC2 instance, and later extend the setup to create multiple instances programmatically.

Below is a comprehensive example that illustrates how to create a security group, define its rules, and attach it to an EC2 instance.

***

## 1. Creating a Security Group and Attaching It to an EC2 Instance

Start by initializing your Pulumi program. In the code snippet below, we create an S3 Bucket (for demonstration), set up a security group for our web server, configure security rules, and launch an EC2 instance with the security group attached.

```python theme={null}
import pulumi
from pulumi_aws import s3, ec2
