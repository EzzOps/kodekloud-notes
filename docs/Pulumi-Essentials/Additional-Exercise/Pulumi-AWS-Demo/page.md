# Pulumi AWS Demo

Source: https://notes.kodekloud.com/docs/Pulumi-Essentials/Additional-Exercise/Pulumi-AWS-Demo/page

This documentation provides instructions for installing Pulumi, configuring AWS, initializing a project, and deploying an HTML page to S3.

Welcome to the Pulumi AWS demo guide. This documentation provides step-by-step instructions on installing Pulumi, configuring AWS credentials, initializing a new Pulumi project using YAML, and deploying a simple HTML page via an S3 bucket. If you have any questions regarding various configurations, please note that reply lengths might be limited.

***

## Install Pulumi

To install Pulumi on your system, open your terminal and run the following command:

```bash theme={null}
$ curl -fsSL https://get.pulumi.com | sh
```

Below is an example of the installation output you may see:

```bash theme={null}
controlplane ~ curl -fsSL https://get.pulumi.com | sh
+ Upgrading Pulumi v3.72.2 to v3.72.2
+ Downloading https://get.pulumi.com/releases/sdk/pulumi-v3.72.2-linux-x64.tar.gz...
+ Total    * Received    % Xferd  Average Speed  Time      Time     Time  Current
                         Dload   Upload   Total   Spent    Left Speed
100 136M  100 136M    0     0   197M      0 --:--:-- --:--:-- --:--:-- 197M
+ Extracting to /root/pulumi/bin
=== Pulumi is now installed! ===
+ Get started with Pulumi: https://www.pulumi.com/docs/quickstart
controlplane ~ export AWS_ACCESS_KEY_ID=
```

***

## Configure AWS Credentials

Set your AWS credentials by exporting your AWS access key and secret key in your terminal:

```bash theme={null}
export AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>
```

Below is another complete sample session illustrating the Pulumi installation along with AWS credential export:

```bash theme={null}
controlplane ~ % curl -fsSL https://get.pulumi.com | sh
+ Upgrading Pulumi to v3.72.2
+ Downloading https://get.pulumi.com/releases/sdk/pulumi-v3.72.2-linux-x64.tar.gz...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                  Dload   Upload   Total   Spent   Left  Speed
100  136M  100  136M    0     0  197M      0 --:--:-- --:--:-- --:--:-- 197M
+ Extracting to /root/.pulumi/bin

=== Pulumi is now installed! ===
+ Get started with Pulumi: https://www.pulumi.com/docs/quickstart
controlplane ~ % export AWS_ACCESS_KEY_ID=AKIAUKDIID0FAHDLZUQR
controlplane ~ % export AWS_SECRET_ACCESS_KEY=/AdLO962uQaA56sSYaelVLSXNRyWhxti+IdErin
controlplane ~ % export
```

***

## Initialize a New Pulumi Project

To begin your Pulumi project, create a new directory and initialize your project using the AWS YAML template:

```bash theme={null}
$ mkdir quickstart && cd quickstart
$ pulumi new aws-yaml
```

The session below demonstrates environment variable exports and project initialization:

```bash theme={null}
controlplane ~ export AWS_ACCESS_KEY_ID=AKIAUKDIIOFAAHDLZQR
controlplane ~ export AWS_SECRET_ACCESS_KEY=/Ad+LO962uQkA56sSYaleVLSXNRyWhxti+idEri
controlplane ~ export PULUMI_ACCESS_TOKEN=pul-c471c52451fb2638f64f6bbc8d8a9ffef1394c2
controlplane ~ mkdir quickstart && cd quickstart && pulumi new aws-yaml
Login using access token from PULUMI_ACCESS_TOKEN
Enter a value or press <ENTER> to accept the default.

project name: yaml_project
project description: (a minimal AWS Pulumi YAML program)
Created project 'yaml_project'

Please enter your desired stack.
To create a stack in an organization, use the format <org-name>/<stack-name> (e.g. 'acme/prod').
stack name: (dev)
Created stack 'dev'

aws:region: The AWS region to deploy into: (us-east-1)
Saved config

Your new project is ready to go!
To perform an initial deployment, run 'pulumi up'
```

***

## Pulumi YAML Configuration

Below is the Pulumi YAML configuration for the minimal AWS project. This configuration creates an S3 bucket and exports its name.

```yaml theme={null}
name: quickstart
runtime: yaml
description: A minimal AWS Pulumi YAML program

resources:
  # Create an AWS resource (S3 Bucket)
  my-bucket:
    type: aws:s3:Bucket

outputs:
  # Export the name of the bucket
  bucketName: ${my-bucket.id}
```

When running `pulumi up`, you will see a preview similar to the following:

```bash theme={null}
$ pulumi up

Previewing update (dev):
    Type                              Name                 Plan       
 +  pulumi:pulumi:Stack              quickstart-dev       create     
 +  └─ aws:s3:Bucket                my-bucket           create     

Resources:
    + 2 to create

Do you want to perform this update?
> yes
    no
    details
```

***

## Detailed Deployment Log

Below is an extended log from an update operation:

```bash theme={null}
controlplane --> /quickstart > pulumi up
Previewing update (dev)

Downloading plugin: 161.68 MiB / 161.68 MiB [==============================] 100.00% 0s [resolution]
Installing plugin: aws-5.41.0
> pulumi:pulumi:Stack yaml_project-dev
  +  aws:s3:Bucket my-bucket
Outputs:
  bucketName: output<string>

Resources:
    + 2 to create

Do you want to perform this update? yes
View in Browser (Ctrl+0): https://app.pulumi.com/trungkodekloud/yaml_project-dev/updates/1/
Type   Name                      Status
pulumi:pulumi:Stack yaml_project-dev creating (0s)
```

And here is the final output once the update is complete:

```bash theme={null}
Previewing update (dev):
    Type                                    Name                 Plan
 *  pulumi:pulumi:Stack                    quickstart-dev      create
 *  └─ aws:s3:Bucket                       my-bucket          create

Resources:
    + 2 to create

Do you want to perform this update?
> yes
    no
    details

Do you want to perform this update? yes
Updating (dev):
    Type                                    Name                 Status
 *  pulumi:pulumi:Stack                    quickstart-dev      created (4s)
 *  └─ aws:s3:Bucket                       my-bucket          created (2s)

Outputs:
    bucketName: "my-bucket-58ec361"
```

After deployment, you might see a summary similar to:

```plaintext theme={null}
pulumi:Stack       yaml_project-dev
aws:s3:Bucket     my-bucket     create

Outputs:
    bucketName: "my-bucket-25423dc"

controlplane ~/quickstart ➔ clear
```

***

## Deploy a Simple HTML Page to S3

To serve a simple HTML page from S3, first create an HTML file:

```bash theme={null}
echo '<html>
<body>
<h1>Hello, Pulumi!</h1>
</body>
</html>' > index.html
```

Next, update your Pulumi YAML configuration to include an S3 BucketObject for the HTML file. Here is the updated configuration:

```yaml theme={null}
name: quickstart
runtime: yaml
description: A minimal AWS Pulumi YAML program

resources:
  # Create an AWS resource (S3 Bucket)
  my-bucket:
    type: aws:s3:Bucket
  
  # Create an S3 Bucket object for index.html
  index.html:
    type: aws:s3:BucketObject
    properties:
      bucket: ${my-bucket.id}
      source: fn:fileAsset('./index.html')

outputs:
  # Export the name of the bucket
  bucketName: ${my-bucket.id}
```

You can verify the bucket deployment and the HTML file with the following commands:

```bash theme={null}
controlPlane ~/quickstart * pulumi stack output bucketName
my-bucket-25423dc
```

To create or inspect your `index.html`, use these commands:

```bash theme={null}
controlPlane ~/quickstart * echo '<html>
<body>
    <h1>Hello, Pulumi!</h1>
</body>
</html>' > index.html

controlPlane ~/quickstart * ls
index.html  Pulumi.dev.yaml  Pulumi.yaml

controlPlane ~/quickstart * cat index.html
<html>
<body>
    <h1>Hello, Pulumi!</h1>
</body>
</html>
```

If you need to modify the configuration, your `Pulumi.yaml` might look like one of the following:

Without the HTML object:

```yaml theme={null}
