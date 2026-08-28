# Demo Setting up Kafka on EC2

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Project-Building-an-Event-Driven-System/Demo-Setting-up-Kafka-on-EC2/page

Guide to deploy a single-node Apache Kafka broker on an AWS EC2 instance using KRaft, Session Manager access, IAM role setup, security group configuration, and creating a demo topic

Welcome back. In this lesson you'll set up Apache Kafka on an EC2 instance. This single-node Kafka broker will act as the central message bus for our demo: front-end and back-end services will exchange events through the Kafka cluster running on this instance.

High-level steps

* Create an IAM role for the EC2 instance (to enable Session Manager).
* Launch an EC2 instance and attach the IAM role.
* Install Java and Apache Kafka.
* Configure Kafka to run in KRaft mode (no ZooKeeper).
* Open the Kafka broker port (9092) on the security group.
* Start Kafka and create a topic for the demo.

Let’s begin in the AWS console.

Create an IAM role for the EC2 instance and allow Session Manager access

1. Open the IAM console → Roles → Create role.
2. Choose EC2 as the trusted entity and continue.

<Frame>
  <img alt="The image shows an AWS IAM interface where a user is selecting a trusted entity type to create a role. Options include AWS service, AWS account, web identity, SAML 2.0 federation, and custom trust policy." />
</Frame>

On the permissions page, attach the SSM policy that allows Session Manager access (for example `AmazonSSMManagedInstanceCore`). Give the role a descriptive name such as `Kafka-demo` and create it.

<Frame>
  <img alt="The image shows an AWS IAM management console screen where a role is being created. It highlights steps for adding permissions and tags, with a focus on the &#x22;AmazonSSMFullAccess&#x22; policy." />
</Frame>

<Callout icon="lightbulb">
  Session Manager lets you open a browser-based shell to your EC2 instance without SSH keys or open SSH ports. Attaching an IAM role with SSM permissions is the recommended approach for secure, keyless access.
</Callout>

Launch an EC2 instance and attach the IAM role

* EC2 console → Launch Instance.
* Name the instance (e.g., `kafka-demo-broker`).
* Instance type: `t2.medium`.
* If you plan to use Session Manager you may skip creating an SSH key pair.
* Use the default security group for now (we'll update it to allow Kafka traffic).
* Increase the root volume from 8 GB to 16 GB.
* Under Advanced Details → IAM instance profile, select the `Kafka-demo` role you created.

<Frame>
  <img alt="The image shows a screenshot of the AWS EC2 console where an instance is being configured, including storage options and security settings. It provides details about the free tier eligibility and summary of the instance configuration." />
</Frame>

Launch the instance and wait until its state becomes running.

Connect to the instance via Session Manager

* Select the instance → Connect → Session Manager → Connect.
* A browser shell opens and you can run commands directly as the EC2 user.

Prepare the instance (become root and set up working directory)

```bash theme={null}
