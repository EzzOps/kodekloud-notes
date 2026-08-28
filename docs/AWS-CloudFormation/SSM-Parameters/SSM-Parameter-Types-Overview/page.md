# SSM Parameter Types Overview

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/SSM-Parameters/SSM-Parameter-Types-Overview/page

Overview of AWS Systems Manager Parameter Store types and guidance for String, StringList, and SecureString including size limits, KMS encryption, permissions, and best practices

Welcome — this lesson covers SSM parameter types: what they are, why they matter, and how to choose the right type when storing values in AWS Systems Manager Parameter Store.

SSM parameter types determine how Parameter Store formats, stores, retrieves, and secures values. Picking the correct type affects storage limits, retrieval semantics, and encryption behavior — for example, whether a value is plain text, a comma-separated list, or encrypted with AWS KMS.

<Frame>
  <img alt="A slide titled &#x22;SSM Parameter Types&#x22; showing a simple diagram where &#x22;Data&#x22; is stored via AWS Systems Manager into the Parameter Store. Icons illustrate a database on the left, the AWS Systems Manager in the center, and a locked parameter store on the right." />
</Frame>

## Summary table

| Parameter Type | Best for                                                                       | Key behavior                                                                                               | Example create (CLI)                                                                                                    |
| -------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| String         | Single scalar values: URLs, paths, numeric config as text, small JSON snippets | Plain-text value up to 4 KB (standard); up to 8 KB for advanced parameters (may incur costs)               | `aws ssm put-parameter --name "/myapp/config/endpoint" --value "https://api.example.com" --type "String"`               |
| StringList     | Small lists that can be parsed by splitting on commas (hostnames, ports)       | Stored as one comma-delimited string. Do not include commas inside items.                                  | `aws ssm put-parameter --name "/myapp/allowed_hosts" --value "host1.example.com,host2.example.com" --type "StringList"` |
| SecureString   | Secrets: API keys, passwords, certificates                                     | Encrypted with AWS KMS. Requires kms:Decrypt and ssm:GetParameter (with decryption) to retrieve plaintext. | `aws ssm put-parameter --name "/myapp/credentials/api_key" --value "my-secret" --type "SecureString"`                   |

## Parameter types — details and CLI examples

### 1) String

Description: A plain-text parameter for single scalar values (URLs, file paths, configuration text, or short JSON).

Size limits:

* Standard parameters: up to 4 KB (4096 characters).
* Advanced parameters: larger sizes up to \~8 KB (8192 characters) — advanced parameters may incur additional charges. For much larger payloads consider Amazon S3 or AWS Secrets Manager.

Create:

```bash theme={null}
aws ssm put-parameter \
  --name "/myapp/config/endpoint" \
  --value "https://api.example.com" \
  --type "String"
```

Retrieve:

```bash theme={null}
aws ssm get-parameter \
  --name "/myapp/config/endpoint" \
  --query "Parameter.Value" \
  --output text
```

### 2) StringList

Description: A single parameter that stores a comma-separated list of strings. Use when your application can split values on commas.

Notes:

* The entire comma-separated value is treated as one string. SSM does not expose list semantics beyond the comma delimiter.
* Avoid commas inside list items because they will be interpreted as separators.

Create:

```bash theme={null}
aws ssm put-parameter \
  --name "/myapp/allowed_hosts" \
  --value "host1.example.com,host2.example.com,host3.example.com" \
  --type "StringList"
```

Retrieve:

```bash theme={null}
aws ssm get-parameter \
  --name "/myapp/allowed_hosts" \
  --query "Parameter.Value" \
  --output text
```

Then split the returned string on commas in your application.

### 3) SecureString

Description: An encrypted parameter for sensitive data (API keys, passwords, certificates). Values are encrypted using AWS KMS.

KMS key usage:

* By default, Parameter Store uses the AWS-managed key alias/aws/ssm.
* You may specify a customer-managed KMS key with `--key-id` when creating the parameter.

Permissions:

* To retrieve plaintext, callers must have `kms:Decrypt` permission on the KMS key and `ssm:GetParameter` with decryption permission.
* If using a customer-managed key, ensure the KMS key policy allows the principal to use the key (and that the SSM service can perform decryption if required).

Create (default AWS-managed KMS key):

```bash theme={null}
aws ssm put-parameter \
  --name "/myapp/credentials/api_key" \
  --value "my-very-secret-api-key" \
  --type "SecureString"
```

Create (custom KMS key):

```bash theme={null}
aws ssm put-parameter \
  --name "/myapp/credentials/api_key" \
  --value "my-very-secret-api-key" \
  --type "SecureString" \
  --key-id "arn:aws:kms:us-east-1:123456789012:key/abcd-1234-ef56-..."
```

Retrieve (decrypted):

```bash theme={null}
aws ssm get-parameter \
  --name "/myapp/credentials/api_key" \
  --with-decryption \
  --query "Parameter.Value" \
  --output text
```

<Callout icon="lightbulb">
  Use SecureString for secrets. Make sure your IAM roles and the KMS key policy allow both reading the parameter (ssm:GetParameter) and decrypting the key (kms:Decrypt). If you need rotation, versioning, or advanced secret lifecycle features, consider using a dedicated secrets service such as AWS Secrets Manager.
</Callout>

## Additional notes and best practices

* Parameter naming: Adopt hierarchical names like `/application/environment/key` to organize parameters and to make IAM/resource policies more effective.
* Permissions: Control access using AWS IAM. For SecureString parameters, also ensure appropriate KMS permissions.
* Choosing the right service:
  * Use Parameter Store for configuration data and lightweight secrets.
  * Use AWS Secrets Manager when you require automatic rotation, built-in secret lifecycle, or cross-account replication.
* Large payloads: For very large data blobs, consider storing data in Amazon S3 (and referencing it from Parameter Store) or use a purpose-built secrets solution.

This concludes the SSM parameter types overview. In short:

* Use String for general text values.
* Use StringList for small comma-separated lists that your application can split.
* Use SecureString for sensitive data encrypted with KMS.

## Links and references

* AWS Systems Manager Parameter Store: [https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
* AWS KMS overview: [https://docs.aws.amazon.com/kms/latest/developerguide/overview.html](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
* AWS Secrets Manager: [https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* AWS IAM documentation: [https://docs.aws.amazon.com/iam/latest/UserGuide/introduction.html](https://docs.aws.amazon.com/iam/latest/UserGuide/introduction.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/d60f94d7-425d-4607-9f69-f9b95e203287/lesson/918ab026-62b4-4859-88fe-05f0d4219dbc" />
</CardGroup>
