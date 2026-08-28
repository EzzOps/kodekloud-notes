# Mappings Introduction

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Mappings/Mappings-Introduction/page

Explains CloudFormation mappings and using FindInMap for static, template-time lookups such as region AMI IDs, account settings, and environment labels

In this lesson we’ll cover CloudFormation mappings: a simple, static lookup mechanism for configuration values that never change at stack runtime. Mappings are ideal for things like region-specific AMI IDs, environment labels, or account-specific constants that you want to keep in a single, predictable place.

<Callout icon="lightbulb">
  Mappings are static. You cannot use intrinsic functions or parameter references inside the Mappings section; all mapping values must be literal constants.
</Callout>

## Anatomy of a mapping

A CloudFormation mapping is a nested lookup table with three conceptual parts:

* Mapping name — the top-level identifier (for example, DevMap).
* Top-level key — the first-level entries inside the mapping (for example, Arno or Alice).
* Second-level key — the nested label inside each top-level key (for example, Env).
* Value — the literal constant associated with the second-level key (for example, Development).

Example YAML mapping:

```yaml theme={null}
Mappings:
  DevMap:                # Mapping name
    Arno:                # Top-level key
      Env: Development   # Second-level key -> value
    Alice:
      Env: Production
```

Table: mapping anatomy at a glance

| Part             | Example                 | Description                                 |
| ---------------- | ----------------------- | ------------------------------------------- |
| Mapping name     | DevMap                  | Top-level label for the whole mapping       |
| Top-level key    | Arno, Alice             | First-level lookup keys inside the mapping  |
| Second-level key | Env                     | Nested lookup label used in FindInMap calls |
| Value            | Development, Production | Literal constants returned by the lookup    |

## Using a mapping (FindInMap)

To read values from a mapping, use the intrinsic function FindInMap (short form: !FindInMap or long form: Fn::FindInMap). The lookup requires three arguments:

1. Mapping name
2. Top-level key
3. Second-level key

Important: The entries within the Mappings section must be literal values, but the three arguments passed to !FindInMap can be literal strings, references to Parameters, or pseudo-parameters (for example, AWS::Region).

Short form example — referencing the mapping to set a Tag value:

```yaml theme={null}
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0abcdef1234567890
      Tags:
        - Key: Environment
          Value: !FindInMap [ DevMap, Arno, Env ]
```

Long form equivalent:

```yaml theme={null}
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      Tags:
        - Key: Environment
          Value:
            Fn::FindInMap:
              - DevMap
              - Arno
              - Env
```

You can combine parameters or pseudo-parameters in the lookup keys. For example, using a parameter to pick the top-level key:

```yaml theme={null}
Parameters:
  Tenant:
    Type: String
    Default: Arno

Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      Tags:
        - Key: Environment
          Value: !FindInMap [ DevMap, !Ref Tenant, Env ]
```

## When to use mappings

Mappings are best for static, template-time lookups with predictable, constant values. Use them when you need to:

| Use case             | Why use a mapping                                    |
| -------------------- | ---------------------------------------------------- |
| Region -> AMI ID     | Different AMIs per region, fixed per template        |
| Account -> settings  | Account-specific values that don’t change at runtime |
| Environment labels   | Map tenant or hostnames to environment names         |
| Static configuration | Any constant lookup not depending on runtime logic   |

<Callout icon="warning">
  Mappings are defined in the template and must contain literal values. Do not include intrinsic functions or parameter references inside the Mappings section — those values must be constants.
</Callout>

## Best practices

* Keep mapping entries small and focused (e.g., separate mappings for AMIs and environment labels).
* Use clear, consistent top-level key names (for example, account IDs, tenant names, or region codes).
* Prefer parameters or pseudo-parameters as arguments to !FindInMap when the actual lookup key needs to vary at template runtime.
* Store large or frequently changing data (like many AMI IDs) outside the template (for example, in SSM Parameter Store or a configuration management system) if they change often.

## Summary

* Mappings are static, table-like sections in a CloudFormation template defined under the top-level Mappings key.
* Use !FindInMap (short) or Fn::FindInMap (long) to look up values by mapping name, top-level key, and second-level key.
* Mapping values must be literal constants—no intrinsic functions or parameter references inside the Mappings block.
* Use mappings for predictable, template-time configuration such as region -> AMI mappings or account-specific settings.

## Links and references

* [AWS CloudFormation: Mappings](https://docs.aws.amazon.[SECRET_REDACTED]-section-structure.html)
* [AWS CloudFormation Intrinsic Functions: Fn::FindInMap](https://docs.aws.amazon.[SECRET_REDACTED]-function-reference-findinmap.html)
* [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/4e0caf18-41ee-4499-8c83-b0dc280c537a/lesson/cf128f1f-7150-419e-8e32-afaa4f0709f0" />
</CardGroup>
