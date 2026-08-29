# Conditions Introduction

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CloudFormation-Conditions-and-Policies/Conditions-Introduction/page

Explains AWS CloudFormation Conditions and how to use intrinsic functions to conditionally create resources, set properties, and make templates environment aware

Welcome to the lesson on AWS CloudFormation Conditions. This page explains what Conditions are, how they work, and how to use them to make templates dynamic and environment-aware.

Conditions let a template decide, at stack create or update time, whether to create resources, set property values, or include outputs. They evaluate to true or false using intrinsic functions and can be driven by parameters, mappings, or other runtime inputs.

## Where Conditions live

Conditions are defined in the top-level `Conditions` section of a CloudFormation template. Use them in two primary ways:

* Attach a Condition to a resource or output using the `Condition` attribute so the entire resource/output is included only when the condition evaluates to true.
* Use the `Fn::If` intrinsic function (`!If` in YAML shorthand) inside a property to select between two values depending on the Condition.

## Basic Condition example

Define a condition that checks whether a parameter named `EnvironmentType` equals `"Production"`:

```yaml theme={null}
Conditions:
  IsProduction: !Equals [ !Ref EnvironmentType, "Production" ]
```

`IsProduction` evaluates to true when the `EnvironmentType` parameter equals `Production`.

## Conditional resource creation

Attach the Condition to a resource so it's created only when the condition is true:

```yaml theme={null}
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Condition: IsProduction
    Properties:
      BucketName: my-prod-bucket
```

When `IsProduction` is false, `MyBucket` and its associated physical resource are not created.

## Conditional properties with !If

Use `!If` to choose between two values for a property:

```yaml theme={null}
Properties:
  PublicAccessBlockConfiguration: !If
    - IsProduction
    - { BlockPublicAcls: false }
    - { BlockPublicAcls: true }
```

How `!If` works:

* First item: condition name (`IsProduction`).
* Second item: value returned when condition is true.
* Third item: value returned when condition is false.

If you need to remove a property entirely when the condition is false, return the pseudo parameter `AWS::NoValue` from the false branch. Otherwise, `!If` will substitute one of the two values, and the property will remain present.

> **lightbulb** When using `!If`, the two return values must match the data type expected by the property (for example, both mappings if a mapping is expected). The exception is using the pseudo value `AWS::NoValue` to remove a property entirely. Conditions are evaluated at stack creation or update time based on parameter values and template logic.

## Combining Conditions

Use the other intrinsic functions to build more complex logic:

* `Fn::And` / `!And` — true if all conditions are true
* `Fn::Or` / `!Or` — true if any condition is true
* `Fn::Not` / `!Not` — inverse of a condition
* `Fn::Equals` / `!Equals` — compares two values

Example: require `IsProduction` and a `UseS3` parameter to both be true before creating a resource:

```yaml theme={null}
Conditions:
  CreateProdBucket: !And
    - !Equals [ !Ref EnvironmentType, "Production" ]
    - !Equals [ !Ref UseS3, "true" ]
```

## Common patterns and best practices

|                  Pattern | Use case                                    | Example                                      |
| -----------------------: | ------------------------------------------- | -------------------------------------------- |
| Resource-level condition | Include or exclude entire resources/outputs | `Condition: IsProduction` on a resource      |
| Property-level condition | Change or remove specific properties        | `!If` with `AWS::NoValue` to omit a property |
|      Combined conditions | Complex environment logic                   | `!And`, `!Or`, `!Not` with parameter checks  |
| Reusable condition names | Use clear, descriptive names                | `IsProduction`, `EnableFeatureX`             |

## Things to watch out for

> **warning** Conditions cannot change resource logical IDs or resource types. Also ensure both branches returned by `!If` match the expected data type for the property — otherwise template validation or runtime errors can occur. Use `AWS::NoValue` when you intend to omit a property entirely.

* Conditions are evaluated during stack creation or update — they are not dynamic at runtime after the stack is active.
* `!If` cannot remove a property unless one branch returns `AWS::NoValue`. If you need to omit the whole resource, use the `Condition` attribute on the resource instead.
* You may reference parameters, mappings, and pseudo parameters inside Conditions, but avoid referencing attributes of resources that may not exist due to other conditions.

## Quick reference snippets

Conditional resource:

```yaml theme={null}
Resources:
  ConditionalInstance:
    Type: AWS::EC2::Instance
    Condition: CreateEC2
    Properties:
      InstanceType: t3.micro
```

Conditional property with AWS::NoValue:

```yaml theme={null}
Properties:
  Tags: !If
    - IncludeTags
    - - Key: Environment
        Value: !Ref EnvironmentType
    - !Ref AWS::NoValue
```

Combined condition example:

```yaml theme={null}
Conditions:
  IsProdAndHasFeature: !And
    - !Equals [ !Ref EnvironmentType, "Production" ]
    - !Equals [ !Ref FeatureEnabled, "true" ]
```

## Links and references

* [AWS CloudFormation – Conditions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html)
* [CloudFormation Intrinsic Functions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)
* [AWS::NoValue pseudo parameter](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html)

Conditions are a powerful way to make your CloudFormation templates reusable and environment-aware. Start by adding simple parameter-driven Conditions, then combine them with intrinsic functions as your template logic grows.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/216ef226-4efe-45ed-b547-b3ab7c5dd29b/lesson/c5495584-b9c0-4788-8bee-7f00fa2e61ef)
