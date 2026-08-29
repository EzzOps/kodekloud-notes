# CFN init Overview

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CFN-init-and-Resource-Imports/CFN-init-Overview/page

Explains how to use CloudFormation init to bootstrap and manage EC2 instances, including cfn-init, cfn-signal, cfn-hup, metadata sections, and practical examples

Welcome — this lesson explains CloudFormation init (commonly called cfn-init) and how to use it to bootstrap and manage EC2 instances from CloudFormation templates.

cfn-init is a helper script that runs on an EC2 instance during stack creation or updates. It reads the AWS::CloudFormation::Init metadata embedded in your CloudFormation template and performs instance-level configuration tasks such as installing packages, creating files, extracting application sources (from S3 or Git), executing commands, and starting or enabling services. You can optionally pair it with cfn-signal to notify CloudFormation about initialization status and with cfn-hup to detect and apply metadata changes automatically.

<Frame>
  <img alt="A presentation slide titled &#x22;CloudFormation Init – Overview&#x22; with a cfn-init icon on the left. On the right are two checklist points: &#x22;Lets you download files from a remote source&#x22; and &#x22;Can use cfn-hup to detect metadata changes and to apply those updates automatically.&#x22;" />
</Frame>

Typical flow when using cfn-init in a stack:

| Step | Action                                                     | Notes                                                                                                                     |
| ---- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1    | Launch an EC2 instance with an instance profile            | Ensure the instance profile grants permissions for any remote resources (for example S3 access if you download artifacts) |
| 2    | Add AWS::CloudFormation::Init metadata to the EC2 resource | Define packages, files, sources, commands, and services in the template metadata                                          |
| 3    | Invoke cfn-init from the instance (commonly via UserData)  | cfn-init reads the metadata and executes the configured actions                                                           |
| 4    | Optionally run cfn-signal to notify CloudFormation         | Signal success or failure so CloudFormation can proceed or rollback                                                       |
| 5    | Optionally install cfn-hup to detect metadata changes      | cfn-hup polls CloudFormation and can re-run cfn-init or hooks to apply updates                                            |

<Callout icon="lightbulb">
  Ensure the EC2 instance has the CloudFormation helper scripts installed (aws-cfn-bootstrap), and that its instance profile allows access to any remote resources you reference (for example, S3) as well as CloudFormation APIs if you use cfn-hup.
</Callout>

Key AWS::CloudFormation::Init sections

| Section  | Purpose                                                      | Example usage                                   |
| -------- | ------------------------------------------------------------ | ----------------------------------------------- |
| packages | Install OS packages via package managers (yum, apt, etc.)    | Install httpd, nginx, jq                        |
| files    | Create files with content, modes, and ownership              | Write /etc/myapp/config.json                    |
| sources  | Download and extract archives from S3 or remote URLs         | Extract myapp.zip to /opt/myapp                 |
| commands | Run commands during initialization, ordered by key           | Run database migrations or one-time setup       |
| services | Manage services (systemd, sysvinit) and ensure running state | Enable and start httpd with ensureRunning: true |

Example AWS::CloudFormation::Init metadata (YAML)

```yaml theme={null}
Metadata:
  AWS::CloudFormation::Init:
    config:
      packages:
        yum:
          httpd: []
      files:
        /var/www/html/index.html:
          content: "<h1>Hello from cfn-init</h1>"
          mode: "000644"
          owner: "root"
          group: "root"
      sources:
        /opt/myapp: https://my-bucket.s3.amazonaws.com/myapp.zip
      commands:
        01_migrate:
          command: "/opt/myapp/bin/migrate.sh"
      services:
        systemd:
          httpd:
            enabled: true
            ensureRunning: true
```

Example UserData snippet that invokes cfn-init and then signals CloudFormation

```bash theme={null}
#!/bin/bash
