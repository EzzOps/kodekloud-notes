# Accessing Mapped Values

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Mappings/Accessing-Mapped-Values/page

Explains how to use the FindInMap intrinsic function in AWS CloudFormation to perform static lookups from the Mappings section for region and configuration specific values

Welcome to the lesson on accessing mapped values in an AWS CloudFormation template. This page explains how to use the Fn::FindInMap intrinsic function (YAML short form: !FindInMap) to look up static values from the template's Mappings section. Use this when you want region-, environment-, or configuration-specific values centralized and referenced cleanly across resources.

<Frame>
  <img alt="A blue-green gradient presentation slide with the centered title &#x22;Accessing Mapped Values.&#x22; There is a small &#x22;© Copyright KodeKloud&#x22; notice in the lower-left corner." />
</Frame>

How Fn::FindInMap works

* Fn::FindInMap performs a static lookup at stack creation or update.
* It requires three arguments: the mapping name, the top-level key (row), and the second-level key (column/label).
* The function returns the mapped value found at that intersection.

Syntax (short and long forms)

```yaml theme={null}
