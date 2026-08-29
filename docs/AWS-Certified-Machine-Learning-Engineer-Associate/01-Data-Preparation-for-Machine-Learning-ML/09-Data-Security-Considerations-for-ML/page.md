# Data Security Considerations for ML

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Data-Security-Considerations-for-ML/page

Securing machine learning data and pipelines on AWS by protecting datasets, preventing poisoning, enforcing encryption and access controls, and monitoring deployments for privacy and integrity

Machine learning relies on data as its foundation. If training data is stolen, tampered with, or exposed, model behavior — including accuracy, fairness, and safety — can be compromised. Threats range from targeted data-poisoning attacks that bias outcomes to accidental leaks that expose sensitive information or intellectual property.

<Frame>
  <img alt="The image illustrates a data security issue in machine learning, depicting how data can be tampered with or stolen by a hacker, affecting the ML model training and resulting in compromised outputs." />
</Frame>

Sensitive datasets often include regulated or personally identifiable information (PII) — for example, protected health information governed by [HIPAA](https://www.hhs.gov/hipaa/index.html), payment card data under [PCI DSS](https://www.pcisecuritystandards.org/), or user metadata such as geolocation and biometrics. In addition to privacy risks, curated datasets and labeling pipelines can be valuable intellectual property. Prioritizing security reduces the risk of data breaches, regulatory fines, and erosion of customer trust.

<Frame>
  <img alt="The image highlights data security as a critical factor in machine learning, showing how data relates to healthcare, finance, and user data, with potential issues like fines (GDPR, HIPAA), legal action, and data breaches." />
</Frame>

A common privacy attack is membership inference. In this method, an adversary queries a deployed model with inputs that are either from the training set or not, then analyzes differences in the model outputs to infer whether a specific record was used during training. Models that behave differently on training samples versus unseen data leak membership information and thereby expose private data.

<Frame>
  <img alt="The image illustrates a &#x22;Membership Inference Attack&#x22; on a machine learning model, showing a private training dataset used by the model, whose outputs are observed by an adversary to compare responses for members versus non-members." />
</Frame>

These risks make it clear that security must protect datasets, model artifacts, deployed endpoints, and every stage of the ML pipeline — from ingestion to monitoring.

Cloud security follows a shared responsibility model: cloud providers protect the underlying infrastructure (data centers, hardware, and managed services), while customers are responsible for securing their data, configurations, access controls, and applications. Understanding and enforcing this boundary is essential for compliance and secure ML operations. For the AWS implementation, see the AWS [shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/).

<Callout icon="lightbulb">
  AWS secures the underlying infrastructure; you are responsible for protecting your data, model artifacts, access policies, and runtime configurations. Apply controls across every stage of the ML lifecycle.
</Callout>

<Frame>
  <img alt="The image depicts the AWS Shared Responsibility Model, illustrating the division of security responsibilities between AWS and the customer, with distinct layers like data, software, and infrastructure." />
</Frame>

Security controls should be applied across the ML lifecycle:

* Encrypt data at rest and in transit.
* Secure streaming and ingestion pipelines during collection.
* Protect data during preprocessing and labeling (least-privilege access, audit logs).
* Protect training jobs and dataset artifacts with isolation and key management.
* Harden deployed endpoints with authentication, authorization, and traffic encryption.
* Monitor and log access to detect anomalies and support forensics.

<Frame>
  <img alt="The image is a flowchart illustrating key areas of security in ML workflows, including data collection, storage, preprocessing, training, deployment, and monitoring. It emphasizes the interconnected steps in the machine learning process." />
</Frame>

On AWS, there are native services and patterns to support these controls. For ingestion and streaming, consider [Amazon Kinesis](https://aws.amazon.com/kinesis/) or [AWS IoT Core](https://aws.amazon.com/iot-core/) to capture data securely. Use [AWS Key Management Service (KMS)](https://aws.amazon.com/kms/) to manage encryption keys and [AWS Identity and Access Management (IAM)](https://aws.amazon.com/iam/) for fine-grained authorization.

<Frame>
  <img alt="The image depicts a simplified diagram of data collection and ingestion on AWS, showing data flowing from three sources into a centralized data storage, with Amazon Kinesis and AWS IoT Core as components involved in the process." />
</Frame>

For labeled data, use managed labeling services like [Amazon SageMaker Ground Truth](https://aws.amazon.com/sagemaker/groundtruth/). Ground Truth includes encryption, human-review audit trails, and can run labeling jobs inside a VPC to minimize exposure and reduce exfiltration risks.

<Frame>
  <img alt="The image is a diagram showing data preprocessing and labeling, featuring icons for data storage, Amazon SageMaker Ground Truth, and Amazon VPC." />
</Frame>

During model training:

* Encrypt datasets and artifacts with KMS-managed keys.
* Run training jobs in isolated, private environments (for example, within a VPC).
* Apply access controls and continuous monitoring of data access to detect unauthorized reads or modifications. These measures lower the risk of model-poisoning or dataset tampering.

<Frame>
  <img alt="The image illustrates a model training process involving data, AWS KMS (Key Management Service), and the resulting ML model, depicted with icons and a flow arrow." />
</Frame>

For model deployment and inference:

* Host endpoints inside private VPCs where possible.
* Enforce IAM-based permissions for internal services and consider [Amazon Cognito](https://aws.amazon.com/cognito/) for authenticated external users.
* Require TLS 1.2 or TLS 1.3 for all API traffic.
* Use [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) to collect runtime metrics and logs, and [AWS WAF](https://aws.amazon.com/waf/) to filter anomalous traffic patterns and protect against abuse.

<Frame>
  <img alt="The image illustrates &#x22;Model Deployment and Inference&#x22; featuring a diagram with a machine learning model icon and mentions AWS Identity and Access Management (IAM) and Amazon Cognito." />
</Frame>

For continuous monitoring and audits:

* Enable [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) to record API activity and changes.
* Use [SageMaker Model Monitor](https://aws.amazon.com/sagemaker/features/model-monitor/) to detect data drift, concept drift, and anomalous inference inputs.
* Centralize logs and security telemetry in repositories such as [Amazon Security Lake](https://aws.amazon.com/security-lake/), [Amazon S3](https://aws.amazon.com/s3/), or your SIEM for correlation, alerting, and forensics.

Finally, combine least-privilege access controls, managed encryption keys, runtime monitoring, and periodic audits to maintain a secure, compliant ML pipeline from ingestion through deployment and operations.

Best-practice summary (ML lifecycle controls):

| ML Stage                       |                               Key Risks | Recommended Controls                                                                   |
| ------------------------------ | --------------------------------------: | -------------------------------------------------------------------------------------- |
| Data ingestion & streaming     | Data tampering, unauthorized collection | Use secured streams (Kinesis, IoT Core), TLS, authentication, and ingestion validation |
| Preprocessing & labeling       |        Data leakage, incorrect labeling | Run labeling in VPC, use Ground Truth, enable audit trails, restrict access            |
| Training                       |       Data poisoning, exposed artifacts | Encrypt with KMS, train in private VPCs, enforce IAM, monitor dataset access           |
| Deployment & inference         |   Unauthorized access, model extraction | Host endpoints in VPC, enforce IAM/Cognito, require TLS, use WAF                       |
| Monitoring & incident response |              Undetected breaches, drift | Enable CloudTrail, CloudWatch, Model Monitor; centralize logs in Security Lake/SIEM    |

Common threats and mitigations:

| Threat               | Description                                      | Mitigation                                                                               |
| -------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Membership inference | Attacker infers if a sample was in training data | Reduce overfitting, add prediction noise, use differential privacy techniques            |
| Model poisoning      | Malicious data alters model behavior             | Strong data validation, provenance tracking, signed datasets, restricted labeling access |
| Model extraction     | Adversary reconstructs model via queries         | Rate-limit queries, authentication, response minimization                                |
| Data exfiltration    | Unauthorized data download or access             | Encryption at rest/in-transit, audit logs, least-privilege IAM, VPC isolation            |

Links and references

* [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/)
* [Amazon Kinesis](https://aws.amazon.com/kinesis/)
* [AWS IoT Core](https://aws.amazon.com/iot-core/)
* [AWS Key Management Service (KMS)](https://aws.amazon.com/kms/)
* [AWS Identity and Access Management (IAM)](https://aws.amazon.com/iam/)
* [Amazon SageMaker Ground Truth](https://aws.amazon.com/sagemaker/groundtruth/)
* [Amazon VPC](https://aws.amazon.com/vpc/)
* [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
* [AWS WAF](https://aws.amazon.com/waf/)
* [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)
* [SageMaker Model Monitor](https://aws.amazon.com/sagemaker/features/model-monitor/)
* [Amazon Security Lake](https://aws.amazon.com/security-lake/)

Adopt a layered approach: enforce strong identity controls, use managed encryption, isolate sensitive workloads, monitor behavior in production, and regularly audit your ML systems to reduce risk and meet compliance obligations.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/e79ce005-44d9-4078-995a-7ea650b34bbd" />
</CardGroup>
