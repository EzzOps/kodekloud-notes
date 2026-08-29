# Data Classification Anonymization and Masking

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Data-Preparation-for-Machine-Learning-ML/Data-Classification-Anonymization-and-Masking/page

Protecting sensitive data in ML pipelines through classification, anonymization, masking, and access controls using AWS tools like Macie, Glue, and SageMaker.

Machine learning workflows commonly rely on large datasets that may contain personally identifiable information (PII) (names, addresses, phone numbers), protected health information (PHI) (medical history), and financial data (credit card numbers, bank accounts). If exposed, these data can lead to identity theft, fraudulent transactions, regulatory fines, and reputational damage. To reduce risk, teams must classify data, apply appropriate anonymization or masking techniques, and enforce access controls and auditability across ML pipelines.

<Frame>
  <img alt="The image illustrates a process of limiting data exposure in machine learning workflows, showing personal data being protected with limited access to the ML workflow." />
</Frame>

## Why classification matters

Data classification is the foundation of any data protection strategy. Tagging data by sensitivity and intended use enables automated enforcement of access policies, encryption rules, and retention schedules. Classification also guides downstream decisions—what data can be included in training, what must be masked or removed, and what requires stronger controls for audit and compliance.

Amazon Macie automates detection of common sensitive data patterns by scanning objects in Amazon S3. It discovers SSNs, email addresses, phone numbers, and other PII/PHI patterns and generates findings and metadata that you can use to trigger alerts, tag data, or initiate remediation workflows. Combine automated detection with manual review and rule-based tagging for the most accurate classification.

<Frame>
  <img alt="The image illustrates the use of Amazon Macie to identify and classify sensitive data types such as PII, PHI, and credentials within a dataset." />
</Frame>

Store classification results in a data catalog (for example, the AWS Glue Data Catalog) so tables and columns are tagged with sensitivity levels, regulatory controls, or categories such as `PII`, `PHI`, `FIN`, or `GDPR`. These tags enable access control policies and automated workflows to treat data appropriately throughout its lifecycle.

<Frame>
  <img alt="The image illustrates the use of AWS Glue Data Catalog, showing data classification with tags for sensitivity (&#x22;high&#x22;), compliance (&#x22;GDPR&#x22;), and classification (&#x22;PII&#x22;)." />
</Frame>

## Anonymization techniques

Data anonymization irreversibly removes or transforms identifying information so records cannot be traced back to individuals. Common techniques include:

* Generalization: Replace a precise value with a broader category (e.g., age 33 → age group 30–40).
* Suppression: Remove or omit fields entirely (e.g., drop `name` and exact `address`).
* Hashing: Apply an irreversible transformation (e.g., SHA-256). Use salting or HMACs for low-entropy fields to prevent brute-force/dictionary attacks.
* Tokenization: Replace a value with a random token and store the mapping securely if reversible re-identification is required.
* Perturbation: Add noise or alter values slightly to preserve statistical properties while obfuscating individuals.

SageMaker Data Wrangler makes it easy to add anonymization steps to an ML preprocessing pipeline. It can drop or mask PII/PHI columns, generalize numeric fields such as income ranges, and perform dataset transformations while preserving utility for model training. Data Wrangler integrates with Amazon S3 and SageMaker Pipelines for reproducible, auditable workflows.

<Frame>
  <img alt="The image outlines three steps for using SageMaker Data Wrangler to perform anonymization: dropping or masking columns with PII or PHI, generalizing fields like income, and transforming datasets while preserving utility for ML training." />
</Frame>

## Masking and format-preserving protection

Data masking conceals sensitive details while preserving format and usability for testing or preprocessing. For example, a credit card number can be transformed to a masked string that keeps length and grouping but hides digits. Masking methods are sometimes reversible (if mapping or keys are retained), whereas anonymization is intended to be irreversible.

> **lightbulb** Masking may be reversible if mappings or encryption keys are retained. Choose anonymization when you need irreversible de-identification.

<Frame>
  <img alt="The image is an illustration explaining data masking, showing how sensitive details like credit card and bank account numbers are concealed while maintaining a usable structure." />
</Frame>

> **warning** Hashing low-entropy values (for example, short IDs or dates) can be vulnerable to brute-force attacks. Use salts or keyed HMACs, or prefer tokenization with a secure vault for reversible mappings.

AWS Glue can implement masking and tokenization within an ETL job: read data from a source, apply masking or tokenization logic (regex redaction, format-preserving encryption, or other transformation code in the ETL script), and write the protected output back to Amazon S3. Applying these transformations consistently in ETL ensures downstream ML pipelines only consume appropriately protected datasets.

## Quick comparison: classification, anonymization, masking

| Method                 | Purpose                                                 | Reversibility                                  | Typical Use Cases                                                                       |
| ---------------------- | ------------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------- |
| Data classification    | Label data by sensitivity and compliance requirements   | N/A (metadata only)                            | Enforce access control, drive workflows, tag data in a catalog                          |
| Anonymization          | Irreversibly remove/transform identifiers               | Irreversible                                   | Privacy-preserving analytics, public datasets, model training without re-identification |
| Masking / Tokenization | Obscure values while preserving format or reversibility | Reversible or irreversible (depends on method) | Testing, staging, ML preprocessing when format is required                              |

<Frame>
  <img alt="The image is a summary table comparing data classification, anonymization, and masking, detailing aspects like purpose, reversibility, and examples for each method." />
</Frame>

## Recommended best practices

* Classify data early and keep classification metadata in a central data catalog.
* Apply the principle of least privilege: restrict access only to users and services that need the data.
* Prefer irreversible anonymization when re-identification is not required.
* Use format-preserving masking (or tokenization) for downstream testing and preprocessing needs.
* Log and audit transformations and data access for compliance (GDPR, HIPAA, CCPA).
* Combine automated detection (e.g., Amazon Macie) with human review to reduce false positives/negatives.

## Links and references

* Amazon Macie: [https://aws.amazon.com/macie/](https://aws.amazon.com/macie/)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* AWS Glue Data Catalog: [https://aws.amazon.com/glue/features/data-catalog/](https://aws.amazon.com/glue/features/data-catalog/)
* SageMaker Data Wrangler: [https://aws.amazon.com/sagemaker/data-wrangler/](https://aws.amazon.com/sagemaker/data-wrangler/)
* SageMaker Pipelines: [https://aws.amazon.com/sagemaker/pipelines/](https://aws.amazon.com/sagemaker/pipelines/)
* AWS Glue: [https://aws.amazon.com/glue/](https://aws.amazon.com/glue/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f6c821d2-a5b8-4946-9a75-624ec2ba0e75/lesson/6268d94a-96d6-44f3-9115-03595d9aed8a)
