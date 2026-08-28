# Demo Update Lambda Configuration

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/AWS-Lambda-and-Advanced-Deployment-Techniques/Demo-Update-Lambda-Configuration/page

This tutorial explains how to update AWS Lambda environment variables using the AWS CLI and automate the process in a Jenkins CI/CD pipeline.

In this tutorial, you’ll learn how to update AWS Lambda environment variables using the AWS CLI and automate the process in a Jenkins CI/CD pipeline. We’ll cover:

* Updating Lambda configuration with `aws lambda update-function-configuration`
* Integrating environment updates and code deployment in Jenkins
* Handling OWASP Dependency Check failures
* Verifying updates in the AWS Lambda console

## Updating Lambda Configuration with AWS CLI

The AWS CLI’s `update-function-configuration` command lets you modify Lambda settings, including environment variables. For full details, see the [AWS CLI Command Reference][aws-cli-ref].

<Frame>
  ![The image shows a webpage from the AWS CLI Command Reference, specifically detailing the "update-function-configuration" command for AWS Lambda. It includes sections like description, synopsis, options, and examples.](https://kodekloud.com/kk-media/image/upload/v1752870277/notes-assets/images/Certified-Jenkins-Engineer-Demo-Update-Lambda-Configuration/aws-cli-update-function-configuration.jpg)
</Frame>

### Key Parameters

| Parameter         | Description                                 | Example                           |
| ----------------- | ------------------------------------------- | --------------------------------- |
| `--function-name` | Name or ARN of the Lambda function          | `my-function`                     |
| `--environment`   | JSON or shorthand for environment variables | `Variables={KEY1=val1,KEY2=val2}` |

### Environment Syntax

| Syntax    | Format                                                                                 |
| --------- | -------------------------------------------------------------------------------------- |
| Shorthand | `--environment Variables={Key1=val1,Key2=val2}`                                        |
| JSON      | `--environment '{"Variables":{"Key1":"val1","Key2":"val2"}}'` or via `file://env.json` |

<Callout icon="lightbulb">
  When using inline JSON on the command line, wrap the JSON in single quotes to avoid shell parsing errors.
</Callout>

### Example: Update and Confirm

```bash theme={null}
