# Concurrent Runs amp Queued State

Source: https://notes.kodekloud.com/docs/Spacelift-Elevate-Your-Infrastructure-Deployment/Spacelift-Basics/Concurrent-Runs-amp-Queued-State/page

This article explains handling concurrent runs and queued states in Spacelift when multiple engineers modify Terraform configurations simultaneously.

In this article, we explain how changes in your Terraform configuration trigger concurrent runs in Spacelift and how to handle queued states when multiple engineers modify the code simultaneously.

## Updating the Terraform Configuration

We begin by updating the main Terraform configuration file (main.tf) to deploy a simple AWS EC2 instance. The configuration below specifies the required Terraform version, AWS provider settings, and resource details for the EC2 instance:

```hcl theme={null}
required_version = ">= 1.2.0"

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-02396cdd13e9a1257"
  instance_type = "t2.micro"
}
```

Next, verify that your AWS credentials are correctly stored on your local system. This ensures that authentication is properly configured:

```bash theme={null}
space lift-demo on main via default
> cat ~/.aws/credentials
[default]
aws_access_key_id = [AWS_ACCESS_KEY_ID]
aws_secret_access_key = [AWS_SECRET_ACCESS_KEY]

space lift-demo on main via default
> [AWS_ACCESS_KEY_ID]
```

## Creating a VPC

Now, let’s create a simple Virtual Private Cloud (VPC) with a CIDR block of 10.0.0.0/16, named "tf-example". After you save, add, and commit these changes to your Git repository, a new run is triggered in Spacelift.

Below is the Terraform configuration for creating the VPC:

```hcl theme={null}
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "tf-example"
  }
}
```

After committing these changes, the Git output might look like this:

```bash theme={null}
1 file changed, 8 insertions(+)
spacelift-demo on main [!] via ⬢ default
> git push
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 12 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 415 bytes | 415.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/Sanjeev-Thiyagarajan/spacelift-demo.git
   2e4d018..1587182  main -> main
spacelift-demo on main via ⬢ default took 2s
```

Back in Spacelift, the run corresponding to the "add VPC" commit starts by initializing, generating a plan, and then moving into an unconfirmed state. The plan output indicates that a new VPC will be created:

```plaintext theme={null}
