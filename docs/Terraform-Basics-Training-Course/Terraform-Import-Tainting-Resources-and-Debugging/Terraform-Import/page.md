# export TF_LOG=<log_level>
$ export TF_LOG=TRACE
```

After setting this variable, running any Terraform command will produce detailed logs corresponding to the selected verbosity level. For example, a Terraform plan run with TF\_LOG set to TRACE might output hundreds or even thousands of lines, capturing every internal operation performed by Terraform plugins.

Below is an example output from running `terraform plan` with elevated logging:

```plaintext theme={null}
$ terraform plan
2020/10/18 22:08:30 [INFO] Terraform version: 0.13.0
2020/10/18 22:08:30 [INFO] Go runtime version: go1.14.2
2020/10/18 22:08:30 [INFO] CLI args: []string{"C:\\Windows\\system32\\terraform.exe", "plan"}
2020/10/18 22:08:30 [DEBUG] Attempting to open CLI config file: C:\\Users\\vpala\\AppData\\Roaming\\terraform.rc
2020/10/18 22:08:30 [DEBUG] File doesn't exist, but doesn't need to. Ignoring.
2020/10/18 22:08:30 [DEBUG] ignoring non-existing provider search directory terraform.d/plugins
2020/10/18 22:08:30 [DEBUG] ignoring non-existing provider search directory C:\Users\\vpala\AppData\Roaming\HashiCorp\Terraform\plugins
2020/10/18 22:08:30 [DEBUG] ignoring non-existing provider search directory 
2020/10/18 22:08:30 [INFO] CLI command args: []string{"plan"}
2020/10/18 22:08:30 [WARN] Log levels other than TRACE are currently unreliable, and are supported only for backward compatibility.
Use TF_LOG=TRACE to see Terraform's internal logs.
----
2020/10/18 22:08:30 [DEBUG] New state was assigned lineage "f413959c-538a-f9ce-524e-1615073518d4"
2020/10/18 22:08:30 [DEBUG] checking for provisioner in "."
2020/10/18 22:08:30 [DEBUG] checking for provisioner in "C:\\Windows\\system32"
2020/10/18 22:08:30 [INFO] Failed to read plugin lock file .terraform\plugins\windows_amd64\lock.json: The system cannot find the path specified.
2020/10/18 22:08:30 [INFO] backend/local: starting Plan operation
2020/10/18 22:08:30.646-0400 [DEBUG] plugin: starting plugin: path=terraform/plugins/registry.terraform.io/hashicorp/aws/3.11.0/windows_amd64/terraform-provider-aws_v3.11.0_x5.exe args=[]
2020/10/18 22:08:30.935-0400 [DEBUG] plugin: waiting for RPC address: path.terraform/plugins/registry.terraform.io/hashicorp/aws/3.11.0/windows_amd64/terraform-provider-aws_v3.11.0_x5.exe pid=34016
2020/10/18 22:08:30.974-0400 [DEBUG] plugin: configuring server automatic mTLS:
```

## Logging to a File

If you want to persist these logs to a file for later review or to include them in bug reports, set the environment variable TF\_LOG\_PATH with the desired file path as shown below:

```bash theme={null}
$ export TF_LOG_PATH=/tmp/terraform.log
```

All generated logs will then be recorded in the specified file. To quickly inspect the beginning of your log file, you can use a command like:

```bash theme={null}
$ head -10 /tmp/terraform.log
```

An example snippet from the log file might look like this:

```plaintext theme={null}
----
2020/10/18 22:08:30 [INFO] terraform version: 0.13.0
2020/10/18 22:08:30 [INFO] Go runtime version: go1.14.2
2020/10/18 22:08:30 [INFO] CLI args: []string{"C:\\Windows\\system32\\terraform.exe", "plan"}
2020/10/18 22:08:30 [DEBUG] Attempting to open CLI config file: C:\Users\vpalal\AppData\Roaming\terraform.rc
2020/10/18 22:08:30 [DEBUG] File doesn't exist, but doesn't need to. Ignoring.
2020/10/18 22:08:30 [DEBUG] ignoring non-existing provider search directory terraform.d/plugins
2020/10/18 22:08:30 [DEBUG] ignoring non-existing provider search directory C:\Users\vpalal\AppData\Roaming\terraform.d\plugins
2020/10/18 22:08:30 [DEBUG] ignoring non-existing provider search directory C:\Users\vpalal\AppData\Roaming\HashiCorp\Terraform\plugins
2020/10/18 22:08:30 [INFO] CLI command args: []string{"plan"}
```

## Disabling Debug Logs

To completely disable the debugging output, simply unset the environment variables:

```bash theme={null}
$ unset TF_LOG
$ unset TF_LOG_PATH
```

<Callout icon="triangle-alert">
  Remember to unset these variables when you no longer need detailed logs, as verbose logging can expose sensitive information and impact performance.
</Callout>

***

That concludes our discussion on debugging Terraform. Up next, you'll have the opportunity to practice Terraform tainting and explore additional debugging techniques through interactive exercises.

For more information, visit the [Terraform Documentation](https://www.terraform.io/docs/cli/index.html) for an in-depth look at other available commands and best practices.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/29825b4d-c0d3-4732-a4e0-ec3a2988e2a3/lesson/70e5a377-3313-4c19-ab5e-c0f20777a147" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/29825b4d-c0d3-4732-a4e0-ec3a2988e2a3/lesson/b8679030-52b9-4c91-aaad-42f1eafa5997" />
</CardGroup>


# Terraform Import

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Import-Tainting-Resources-and-Debugging/Terraform-Import/page

This guide explains how to import existing infrastructure into Terraform configuration using the Terraform import command.

In this guide, we will explain how to import existing infrastructure into your Terraform configuration using the Terraform import command. Typically, you create and manage resources with Terraform. However, in many real-world projects, some resources might be provisioned with tools like the AWS Management Console or Ansible. Importing these resources into Terraform helps streamline provisioning, updates, and deletion.

For instance, consider the following diagram illustrating AWS services managed by Terraform, Ansible, and the AWS Management Console:

<Frame>
  ![The image shows AWS services managed by Terraform, Ansible, and AWS Management Console, including EC2, DynamoDB, S3, Route 53, Elastic Block Store, and VPC.](https://kodekloud.com/kk-media/image/upload/v1752884193/notes-assets/images/Terraform-Basics-Training-Course-Terraform-Import/frame_40.jpg)
</Frame>

This diagram sets the stage for your inquiry: How can you bring externally created resources under Terraform’s direct management?

## Accessing Existing Resources Using Data Sources

Initially, you might leverage data sources in Terraform to fetch details from resources not currently managed by your configuration. Data sources allow you to read attributes and integrate existing infrastructure into your workflow without enabling Terraform to update or delete these resources.

For example, the configuration below reads attributes of an existing AWS instance using its instance ID:

```hcl theme={null}
data "aws_instance" "newserver" {
  instance_id = "i-026e13be10d5326f7"
}

output "newserver" {
  value = data.aws_instance.newserver.public_ip
}
```

When you run:

```bash theme={null}
$ terraform apply

data.aws_instance.newserver: Refreshing state... [id=i-026e13be10d5326f7]
aws_key_pair.web: Refreshing state... [id=terraform-2020101501348509100000001]
aws_security_group.ssh-access: Refreshing state... [id=sg-0a543f25009e14628]
aws_instance.webserver: Refreshing state... [id=i-068fad300d9df27ac]

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:
newserver = 15.223.1.176
```

Notice that while Terraform outputs the instance's public IP, it remains unmanaged by Terraform since it’s accessed as a data source.

## Importing an Existing Resource into Terraform

To fully control an existing resource, you need to import it into Terraform’s state. The syntax for the import command is as follows:

```plaintext theme={null}
