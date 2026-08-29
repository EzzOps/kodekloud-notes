# Demo Creating a base template in YAML for Amazon S3

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Resources/Demo-Creating-a-base-template-in-YAML-for-Amazon-S3/page

Guide to creating a minimal AWS CloudFormation YAML template that provisions an Amazon S3 bucket, including file setup, Resources section, optional bucket name, validation, and deployment steps.

Welcome — in this lesson we'll create a minimal CloudFormation template (YAML) that provisions an Amazon S3 bucket. The workflow is simple and focused: create a project folder, add a YAML template file, and author the minimal CloudFormation content that instructs AWS to create the S3 bucket.

Steps (high level)

1. Create a project folder

2. Open the folder in an editor

3. Create the YAML template file

4. Add the minimal Resources section

5. Optionally set BucketName and additional properties

6. Save the file and (optionally) validate/deploy

7. Create a project folder

* On your Desktop create a new folder (for example: `cf-project`).

2. Open that folder in Visual Studio Code

* File → Open Folder → select your `cf-project` folder.

3. Create a new file for the template

* Click the new file icon and name it with a `.yaml` extension. Example:
  * `s3-bucket.yaml`
* Important: do not end filenames with a trailing dot (e.g., `s3-bucket.` is invalid). Use `.yaml` or `.yml` so CloudFormation recognizes the format.

<Callout icon="lightbulb">
  YAML is generally preferred for CloudFormation because it’s more concise and easier to scan than JSON. Use `.yaml` or `.yml` as the file extension.
</Callout>

4. Add the minimal template content

A CloudFormation template needs at least a top-level Resources section. In Resources you declare a logical ID (a template-local name) and the Type that tells CloudFormation which AWS resource to create.

Example minimal template:

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
```

Explanation:

* Resources: — required top-level section where every resource to be created is listed.
* MyS3Bucket — the logical ID (template-local identifier). Choose any valid name; it becomes a reference key inside the template.
* Type: AWS::S3::Bucket — instructs CloudFormation to create an S3 bucket.

5. (Optional) Specify a bucket name and other properties

To provision a bucket with a specific name, include a Properties block with BucketName. Remember bucket names must be globally unique across all AWS and must follow S3 naming rules.

Example with a specified bucket name:

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-unique-bucket-name-12345
```

<Callout icon="warning">
  BucketName must be globally unique and conform to S3 naming rules. If the name is already taken or invalid, stack creation will fail. Prefer letting CloudFormation generate a name, or ensure uniqueness by adding a random suffix.
</Callout>

6. Save the file

* Save `s3-bucket.yaml` in your project folder.

Optional — validate and deploy the template

* Validate the template locally with the AWS CLI:

```bash theme={null}
aws cloudformation validate-template --template-body file://s3-bucket.yaml
```

* Create or deploy the stack (example using aws cloudformation deploy):

```bash theme={null}
aws cloudformation deploy \
  --template-file s3-bucket.yaml \
  --stack-name my-s3-stack \
  --region us-east-1
```

Notes:

* Ensure your AWS credentials and region are configured (`aws configure`) and that your IAM principal has permission to create S3 buckets and CloudFormation stacks.
* For simple S3 bucket templates, you typically don't need extra capabilities flags. If your template uses IAM resources, add `--capabilities CAPABILITY_NAMED_IAM`.

Quick reference — Commands table

| Action            | Command example                                                                     | Notes                                      |
| ----------------- | ----------------------------------------------------------------------------------- | ------------------------------------------ |
| Validate template | `aws cloudformation validate-template --template-body file://s3-bucket.yaml`        | Checks template syntax and basic structure |
| Deploy stack      | `aws cloudformation deploy --template-file s3-bucket.yaml --stack-name my-s3-stack` | Creates or updates the stack               |
| View stack events | `aws cloudformation describe-stack-events --stack-name my-s3-stack`                 | Useful for troubleshooting                 |

Summary

* Create a folder and a `.yaml` file.
* Add a required Resources section with a logical ID and Type `AWS::S3::Bucket`.
* Optionally add Properties (for example, BucketName) but ensure global uniqueness.
* Validate locally and deploy via AWS CLI, Console, or your CI/CD pipeline.

Links and references

* [AWS CloudFormation documentation](https://docs.aws.amazon.com/cloudformation/index.html)
* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/index.html)
* [AWS CLI](https://aws.amazon.com/cli/)

Well done — you now have a base CloudFormation YAML template that creates an S3 bucket.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/c6a9b9c1-84c5-4d3e-957e-38673838de64/lesson/d15a591d-a37d-4b50-823b-42423241e174" />
</CardGroup>
