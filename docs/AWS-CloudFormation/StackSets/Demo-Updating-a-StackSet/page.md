# Demo Updating a StackSet

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/StackSets/Demo-Updating-a-StackSet/page

Guide to updating an AWS CloudFormation StackSet by modifying a template to add an S3 bucket tag and deploying the change across target accounts and regions.

In this lesson we’ll walk through updating an existing [AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation) StackSet. The goal is to modify the StackSet template to add a tag to the S3 bucket resource and then apply that updated template across all stack instances managed by the StackSet.

We will:

* Add a Tag to the S3 bucket resource in the StackSet template.
* Upload the updated template to the StackSet.
* Confirm and submit the update so it is deployed to each stack instance.

Here is the template change we will apply (adds a `Status: Active` tag to the bucket):

```yaml theme={null}
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'stackset-bucket-${AWS::Region}-${AWS::AccountId}'
      Tags:
        - Key: Status
          Value: "Active"
```

<Callout icon="lightbulb">
  When you update a StackSet template you re-submit the template and confirm the target accounts/regions and deployment options. The update is then pushed to each stack instance based on the StackSet's concurrency and failure tolerance settings.
</Callout>

Quick checklist before you begin:

| Task                                                      | Why it matters                                           |
| --------------------------------------------------------- | -------------------------------------------------------- |
| Verify template syntax                                    | Prevents failed updates due to template errors           |
| Confirm target accounts/regions                           | StackSet will only update the selected instances         |
| Review deployment options (concurrency/failure tolerance) | Controls how changes are rolled out and retried          |
| Ensure you have necessary permissions                     | Required for SELF\_MANAGED or service-managed operations |

Step-by-step

1. Open the StackSet you want to update, select it, and choose Actions → Edit StackSet details. Keep the existing configuration unless you need to change it. Choose the option to replace the current template by uploading your updated template file.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation StackSets console showing a selected StackSet named &#x22;DemoStackSet&#x22; (permission model SELF_MANAGED). The Actions dropdown is open with &#x22;Edit StackSet details&#x22; highlighted." />
</Frame>

2. Select "Upload a template file" then choose the updated template file (the file that contains the new tag). Click Next to continue.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation StackSets &#x22;Manage StackSet&#x22; page showing the Template source options with &#x22;Upload a template file&#x22; selected and a highlighted &#x22;Choose file&#x22; button. The page footer shows &#x22;Cancel&#x22; and an orange &#x22;Next&#x22; button, with the browser window and taskbar visible." />
</Frame>

3. On the next page confirm the target accounts and regions. For an existing StackSet these are usually pre-selected; keep them unless you intentionally want to change the scope. Review and set deployment options (maximum concurrent accounts, failure tolerance, region concurrency) as required, then submit the update.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation StackSets console showing the &#x22;DemoStackSet: Manage StackSet&#x22; page with regions listed (eu-west-1, us-east-1) and deployment options (maximum concurrent accounts 1, failure tolerance 0, region concurrency SEQUENTIAL). The orange Submit button in the bottom right is highlighted." />
</Frame>

4. The StackSet update operation will start. The StackSet status will show the operation in progress. Monitor the operation until it completes successfully — the console will show success for the StackSet and each stack instance when finished.

5. Verify the change was applied to your resources. For this example, open the [S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) console in each target region/account that contains a stack instance, view the bucket properties, and confirm the new tag `Status: Active` is present.

<Frame>
  <img alt="Screenshot of the Amazon S3 console showing the Tags panel for a bucket. It lists four tags, including Status: Active, aws:cloudformation:logical-id (MyBucket), and a cloudformation stack-id ARN." />
</Frame>

If you inspect other stack instances (different regions or accounts) you should see the same tag there — confirming the StackSet update was applied across instances.

<Callout icon="warning">
  StackSet updates can modify resources across multiple accounts and regions. Ensure you have valid backups or change control in place, and that you have the necessary permissions to update all target accounts/regions. A failed update may trigger rollbacks depending on your deployment settings.
</Callout>

Summary

* Modify the CloudFormation template (add or change resources/tags).
* Upload the updated template to the existing StackSet.
* Confirm accounts/regions and deployment options, then submit.
* Monitor the update and verify resource changes in each target region/account.

Links and references

* [AWS CloudFormation StackSets documentation](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-is-stacksets.html)
* [AWS CloudFormation documentation](https://docs.aws.amazon.com/cloudformation/)
* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/)
* [CloudFormation template anatomy](https://docs.aws.amazon.[SECRET_REDACTED]-anatomy.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/13ed2c0a-3a8a-45b0-870a-6c267c392190/lesson/41f5fcbd-9cd0-4c00-8460-b341e974efa6" />
</CardGroup>
