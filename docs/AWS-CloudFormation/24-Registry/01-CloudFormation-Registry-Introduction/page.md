# CloudFormation Registry Introduction

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Registry/CloudFormation-Registry-Introduction/page

Overview of AWS CloudFormation Registry, explaining how to create, publish, register, version, and use custom and third party resource types, plus CLI commands, security, and best practices.

The CloudFormation Registry extends AWS CloudFormation by enabling custom and third‑party resource types (also called "extensions") to be used inside CloudFormation templates. This lets you manage additional resources with the same declarative lifecycle (create, update, delete) and drift detection that CloudFormation provides.

> **lightbulb** Quick overview: Use the CloudFormation Registry to publish, version, and activate custom resource providers (resource types). Providers package a JSON schema and handler code (create/update/delete) so CloudFormation can perform lifecycle operations for non‑native resources.

This guide gives a concise, actionable overview: what the Registry provides, naming conventions, the typical provider lifecycle, example CLI commands, how to use custom types in templates, recommended tooling, versioning concepts, security considerations, and best practices.

## What the Registry provides

* A central place to publish and register resource types (extensions) so CloudFormation can use them.
* Support for:
  * Private extensions (owned and maintained within your account/organization).
  * Public third‑party extensions available in the CloudFormation Registry.
* A mechanism to define a resource's schema (JSON Schema) and handlers (the code executed on create/update/delete).
* Versioning, activation, and lifecycle management for type versions.

Table: Registry resource types and use cases

| Resource Type           | Use Case                                                | Example                            |
| ----------------------- | ------------------------------------------------------- | ---------------------------------- |
| Private Type            | Internal automation, custom resources for your org      | `MyCompany::MyService::MyResource` |
| Public Third‑party Type | Vendor-provided integrations that extend CloudFormation | `VendorX::Service::Resource`       |
| AWS Type                | Native AWS resources maintained by AWS                  | `AWS::S3::Bucket`                  |

## Type namespaces and naming

* AWS types: begin with `AWS::` (built-in).
* Third‑party/public types: typically use the vendor namespace, e.g., `Vendor::Service::Resource`.
* Private types: use your company or account scope, e.g., `MyCompany::Service::Resource`.

Example:

```text theme={null}
MyCompany::MyService::MyResource
```

Use clear naming and semantic versioning so consumers understand scope and compatibility.

## Typical provider workflow

1. Author a resource provider:
   * Define the resource schema (JSON Schema) describing properties, required fields, and return values.
   * Implement handlers that perform create, read, update, delete, and list (CRUDL) operations.
   * Use the cloudformation-cli to scaffold, build, and test handlers in supported languages (Python, Java, Go).
2. Package the provider into a Schema Handler Package (SHP) and upload to a supported location (for example, Amazon S3).
3. Register the type with CloudFormation (register-type).
4. Activate the type version you want to use.
5. Reference the registered type inside CloudFormation templates.
6. Manage new versions: register, test, and activate updates when ready.

## Common CLI commands

Table: Core CloudFormation Registry commands

| Action                    | AWS CLI command                                 | Notes                                                 |
| ------------------------- | ----------------------------------------------- | ----------------------------------------------------- |
| Register type             | `aws cloudformation register-type`              | Provide `--schema-handler-package` pointing to SHP    |
| Check registration status | `aws cloudformation describe-type-registration` | Use the registration token                            |
| List types                | `aws cloudformation list-types`                 | Filter by `--visibility PRIVATE` or `PUBLIC`          |
| Describe a type           | `aws cloudformation describe-type`              | Use `--type-name` to get details and `TypeVersionArn` |
| Deregister type           | `aws cloudformation deregister-type`            | Removes a type registration                           |

Example: Register a resource type

```bash theme={null}
aws cloudformation register-type \
  --type RESOURCE \
  --type-name MyCompany::MyService::MyResource \
  --schema-handler-package s3://my-bucket/my-shp.zip
```

Check registration status

```bash theme={null}
aws cloudformation describe-type-registration --registration-token <token>
```

List registered private types

```bash theme={null}
aws cloudformation list-types --visibility PRIVATE
```

Describe a specific type (show TypeVersionArn)

```bash theme={null}
aws cloudformation describe-type \
  --type RESOURCE \
  --type-name MyCompany::MyService::MyResource \
  --query "TypeVersionArn"
```

Deregister a type

```bash theme={null}
aws cloudformation deregister-type --type-name MyCompany::MyService::MyResource --type RESOURCE
```

## Using custom types in templates

After you've registered and activated a type, reference it in your CloudFormation templates using its Type name and supply the properties defined by the provider schema.

Example (YAML):

```yaml theme={null}
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyCustomResource:
    Type: MyCompany::MyService::MyResource
    Properties:
      PropertyOne: "value"
      PropertyTwo: 42
```

CloudFormation routes lifecycle events for that resource to the provider's handlers, so the provider is responsible for provisioning the underlying resource and returning the required attributes and identifiers.

## Development tools

* cloudformation-cli: Official tool to initialize, build, test, and submit resource providers in supported languages.
* Local testing: cloudformation-cli includes contract testing and local invocation helpers to validate handler behavior against the provider schema.
* Packaging: Build an SHP (Schema Handler Package) containing schema and handler artifacts; host it in a secure location such as an S3 bucket.

Example: Bootstrapping a Python provider

```bash theme={null}
pip install cloudformation-cli
cfn init
