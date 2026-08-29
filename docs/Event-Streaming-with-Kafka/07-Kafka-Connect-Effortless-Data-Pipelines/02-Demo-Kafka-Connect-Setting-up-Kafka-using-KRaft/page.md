# Demo Kafka Connect Setting up Kafka using KRaft

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Connect-Effortless-Data-Pipelines/Demo-Kafka-Connect-Setting-up-Kafka-using-KRaft/page

Guide to provisioning an EC2 instance and setting up a single-node KRaft Kafka broker for Kafka Connect and S3 integration

Welcome — in this lesson you'll provision an EC2 instance, install a single-node KRaft-based Kafka broker+controller, and prepare the host for Kafka Connect so you can later sync topic data to S3 using an S3 connector. This guide covers:

* Creating an IAM role for SSM access
* Launching an EC2 instance with the role attached
* Connecting via Session Manager (browser shell)
* Installing Java and Kafka
* Formatting KRaft metadata storage and configuring `server.properties`
* Opening the Kafka port and starting the broker

Prerequisites

* An AWS account with permission to create IAM roles and EC2 instances.
* Basic familiarity with the AWS Console and SSH/Session Manager.
* Browser access for the Session Manager shell (no SSH key required for this demo).

## Create an IAM role

Create an IAM role for EC2 that allows Session Manager (SSM) access:

1. In the AWS Console, search for and open **IAM**.
2. Click **Roles → Create role**.
3. Select **EC2** as the trusted entity.
4. Click **Next**.
5. Attach at minimum the `AmazonSSMManagedInstanceCore` managed policy. This enables Session Manager connectivity.
6. Name the role (example: `Kafka S3 Demo`) and create it.

This is the EC2 instance trust policy that corresponds to the role you just created:

```json theme={null}
{
  "Principal": {
    "Service": [
      "ec2.amazonaws.com"
    ]
  }
}
```

## Launch an EC2 instance

Launch an EC2 instance and attach the IAM role you created. Recommended configuration for this demo:

| Setting        | Recommended value    | Notes                                                    |
| -------------- | -------------------- | -------------------------------------------------------- |
| Instance name  | `Kafka S3 Demo`      | Human-readable tag to identify the instance              |
| Instance type  | `t2.medium`          | Small demo node; scale for production                    |
| Key pair       | None required        | Using Session Manager; no SSH key required for this demo |
| Security group | Default (edit later) | We'll open port 9092 explicitly below                    |
| Root volume    | `16 GiB` (optional)  | Helps store logs and KRaft metadata                      |
| IAM role       | `Kafka S3 Demo`      | Attach the role created earlier under Advanced details   |

1. In the AWS Console, open **EC2 → Instances → Launch Instance**.
2. Configure the instance using the recommended settings above.
3. Under **Advanced details**, select the IAM role (`Kafka S3 Demo`) you created.
4. Launch the instance.

<Frame>
  <img alt="The image shows a portion of the AWS EC2 management console, where a user is configuring the settings for launching an EC2 instance. The settings include network, firewall, and storage configurations, along with a summary of the instance details and free tier information." />
</Frame>

## Connect to the instance using Session Manager

Because the EC2 instance has the SSM role attached, you can open a browser shell without an SSH key.

1. Go to **EC2 → Instances**.
2. Select the instance and click **Connect**.
3. Choose **Session Manager** and click **Connect** to open a browser-based shell.

> **lightbulb** Session Manager is convenient for demos and secure access: no inbound SSH port or key pairs are required. Ensure your instance has the SSM agent installed (most recent AMIs include it by default) and the attached IAM role has `AmazonSSMManagedInstanceCore`.

## Switch to root, download Kafka, and inspect files

Once connected, become root and move to the home directory:

```bash theme={null}
sudo su
cd ~
```

Download and extract a Kafka binary release (example uses Kafka 3.0.0 with Scala 2.13):

```bash theme={null}
