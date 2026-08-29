# ... additional update output ...
apt-get install ufw
```

After installation, check the current status of UFW:

```bash theme={null}
ufw status
```

The expected output should state:

```plaintext theme={null}
Status: inactive
```

## Configuring Default Firewall Rules

Since no firewall rules are active yet, begin by setting default policies. We want to permit all outbound traffic while denying inbound connections. Execute these commands as the root user:

```bash theme={null}
ufw default allow outgoing
```

The system will confirm:

```plaintext theme={null}
Default outgoing policy changed to 'allow'
(be sure to update your rules accordingly)
```

Next, set the default rule to deny all inbound connections:

```bash theme={null}
ufw default deny incoming
```

## Defining Specific Allow Rules

Now that the default policies are in place, add rules to allow specific traffic:

1. Allow SSH connections on port 22 only from the jump server with IP address 172.16.238.5:

   ```bash theme={null}
   ufw allow from 172.16.238.5 to any port 22 proto tcp
   ```

2. Allow HTTP connections on port 80 from the jump server:

   ```bash theme={null}
   ufw allow from 172.16.238.5 to any port 80 proto tcp
   ```

3. Allow HTTP access on port 80 from the internal network (IP range 172.16.100.0/28):

   ```bash theme={null}
   ufw allow from 172.16.100.0/28 to any port 80 proto tcp
   ```

Since port 8080 is actively listening but must be blocked, add an explicit deny rule:

```bash theme={null}
ufw deny 8080
```

<Callout icon="lightbulb">
  Although the default policy already denies incoming connections, explicitly denying port 8080 clarifies its intended blocked status.
</Callout>

## Enabling UFW

Before enabling UFW, verify that all necessary rules are correctly set to avoid unintended disconnections. Once reviewed, enable UFW with:

```bash theme={null}
ufw enable
```

The system warns that enabling UFW may disrupt existing SSH connections. Confirm by entering “y” when prompted:

```plaintext theme={null}
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
```

After UFW is enabled, check its status:

```bash theme={null}
ufw status
```

Expected output:

```plaintext theme={null}
Status: active
To                         Action      From
--                         -----       ----
22/tcp                     ALLOW       172.16.238.5
80/tcp                     ALLOW       172.16.238.5
80/tcp                     ALLOW       172.16.100.0/28
8080                       DENY        Anywhere
8080 (v6)                  DENY        Anywhere (v6)
```

## Deleting Firewall Rules

To remove a specific rule, such as the deny rule for port 8080, use the following command:

```bash theme={null}
ufw delete deny 8080
```

The system confirms the deletion:

```plaintext theme={null}
Rule deleted
Rule deleted (v6)
```

Alternatively, you can delete rules based on their line numbers listed in the firewall status. For example, if the deny rule for port 8080 is listed as rule number 5 and then as rule number 4, delete them one by one:

```bash theme={null}
ufw delete 5
# Confirm deletion when prompted, then:
ufw delete 4
```

After removing rules, recheck the status:

```bash theme={null}
ufw status
```

The updated rules should appear as follows:

```plaintext theme={null}
Status: active
To                         Action      From
--                         -----       ----
22/tcp                     ALLOW       172.16.238.5
80/tcp                     ALLOW       172.16.238.5
80/tcp                     ALLOW       172.16.100.0/28
8080                       DENY        Anywhere
```

## Summary

This lesson provided a comprehensive guide to configuring UFW on an Ubuntu server to secure SSH and HTTP traffic while blocking unauthorized connections. By setting default policies and specifying clear allow/deny rules, you can effectively manage your server's firewall and maintain a secure environment.

Practice these UFW commands to solidify your understanding and ensure your server remains protected against unwanted network traffic.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/d67be5ee-871d-4435-a187-382610cb6a1f/lesson/330f6887-f23b-41f4-8a6d-3db2f2fee5fd" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/d67be5ee-871d-4435-a187-382610cb6a1f/lesson/22eb9c61-27bc-4c84-a5fd-5672cac031de" />
</CardGroup>


# Built ASG based Architecture

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Building-a-Basic-FIS-experiment/Built-ASG-based-Architecture/page

This guide explains how to deploy an AWS architecture using the Management Console for the AWS Fault Injection Service experiment.

In this guide, you’ll deploy a simple AWS architecture using the Management Console to kick off an introduction to the AWS Fault Injection Service (FIS). We’ll create three components:

1. **EC2 Launch Template** tagged for our experiment
2. **Auto Scaling Group (ASG)** spanning two Availability Zones
3. **CloudWatch Log Group** for FIS experiment logs

<Callout icon="lightbulb">
  This demo uses **only** the AWS Management Console—no IaC templates or GitHub repositories required.
</Callout>

***

## 1. Create an EC2 Launch Template

An EC2 Launch Template defines the configuration (AMI, instance type, security groups, tags) that the ASG will use to provision EC2 instances.

1. Open the EC2 console and navigate to **Launch Templates**.
2. Click **Create launch template**.
3. Enter the following details:
   * **Launch template name**: `FIS-Experiment-Template`
   * **Template version description**: *Initial version for FIS experiment*
   * **Tags**:
     * Key: `experiment`
     * Value: `fault-injection`
   * Choose your **AMI**, **Instance Type**, **Key Pair**, **Security Groups**, etc.
4. Review and click **Create launch template**.

For more information, see the AWS documentation on [EC2 Launch Templates](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html).

***

## 2. Configure the Auto Scaling Group

Your Auto Scaling Group will maintain a desired capacity of 1 instance (minimum 1, maximum 4) across two Availability Zones. If an instance terminates, the ASG will automatically launch a replacement to maintain the desired capacity.

| Setting            | Value                                |
| ------------------ | ------------------------------------ |
| Launch template    | `FIS-Experiment-Template`            |
| Availability Zones | 2 (e.g., `us-east-1a`, `us-east-1b`) |
| Desired capacity   | 1                                    |
| Minimum capacity   | 1                                    |
| Maximum capacity   | 4                                    |

### Steps

1. In the EC2 console, go to **Auto Scaling Groups** → **Create Auto Scaling group**.
2. Select **Launch template** and choose `FIS-Experiment-Template`.
3. Select two subnets in different Availability Zones.
4. Under **Configure group size and scaling policies**, set the capacity values as shown above.
5. (Optional) Add scaling policies if you want the group to scale based on metrics.
6. Review and click **Create Auto Scaling group**.

<Callout icon="triangle-alert">
  Ensure your selected subnets have sufficient IP addresses to support up to 4 instances simultaneously.
</Callout>

***

## 3. Create a CloudWatch Log Group

AWS FIS will publish all experiment activity to CloudWatch Logs. Create a dedicated log group named `FIS-Experiment`.

1. Open the CloudWatch console and select **Logs** → **Log groups**.
2. Click **Create log group**.
3. Enter **Log group name**: `FIS-Experiment`
4. (Optional) Configure a retention policy (e.g., 30 days).
5. Click **Create**.

| Resource                    | Purpose                                                       |
| --------------------------- | ------------------------------------------------------------- |
| Log group: `FIS-Experiment` | Captures AWS FIS experiment logs from your Auto Scaling Group |

For more details, refer to the [Amazon CloudWatch Logs documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html).

***

With these three components in place—EC2 Launch Template, Auto Scaling Group, and CloudWatch Log Group—you’re ready to begin your AWS Fault Injection Service experiment. In the next section, we’ll configure and execute an FIS experiment against this architecture.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/chaos-engineering/module/d49a2b6d-60a1-4603-965d-7e8292688875/lesson/c2a24581-4089-4535-852f-ee7edd476dc0" />
</CardGroup>
