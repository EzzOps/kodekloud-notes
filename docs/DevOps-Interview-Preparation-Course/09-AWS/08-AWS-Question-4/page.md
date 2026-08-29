# AWS Question 4

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Preparation-Course/AWS/AWS-Question-4/page

Explains an AWS IAM policy, its allow and deny statements, resource scoping, practical implications, and interview-friendly explanations and improvements.

This article walks through a sample AWS IAM policy that you might be given in an interview: explain what it allows, what it denies, and the practical implications. Read the policy, then follow the step-by-step breakdown and interview-friendly summary.

Corrected policy (single consolidated copy):

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ListRead",
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:GetAccountPublicAccessBlock",
        "s3:ListAccessPoints",
        "s3:ListAllMyBuckets"
      ],
      "Resource": "arn:aws:s3:::*"
    },
    {
      "Sid": "AllowS3Self",
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::carlossalazar",
        "arn:aws:s3:::carlossalazar/*"
      ]
    },
    {
      "Sid": "DenyS3Logs",
      "Effect": "Deny",
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::*log*"
    }
  ]
}
```

## Quick summary table

| Sid               | Effect          | Actions                                                                                                | Resource(s)                                                  | Purpose                                                                                     |
| ----------------- | --------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| `AllowS3ListRead` | Allow           | `s3:GetBucketLocation`, `s3:GetAccountPublicAccessBlock`, `s3:ListAccessPoints`, `s3:ListAllMyBuckets` | `arn:aws:s3:::*`                                             | Permit listing/metadata reads across buckets (account-level listing)                        |
| `AllowS3Self`     | Allow           | `s3:*`                                                                                                 | `arn:aws:s3:::carlossalazar`, `arn:aws:s3:::carlossalazar/*` | Full S3 permissions scoped to the single bucket `carlossalazar` and its objects             |
| `DenyS3Logs`      | Deny (explicit) | `s3:*`                                                                                                 | `arn:aws:s3:::*log*`                                         | Explicitly deny all S3 actions on buckets whose names contain `log` (bucket-level ARN only) |

## Step-by-step explanation

1. Version

* `"Version": "2012-10-17"` specifies the policy language version. This is the standard policy version used for most IAM policies.

2. High-level structure

* `"Statement"` is an array of statements. Each statement includes a Sid (identifier), Effect, Action(s), and Resource(s). The policy contains three statements:
  * `AllowS3ListRead`
  * `AllowS3Self`
  * `DenyS3Logs`

3. Statement: AllowS3ListRead

* Effect: Allow
* Actions:
  * `s3:GetBucketLocation` — returns a bucket's AWS Region.
  * `s3:GetAccountPublicAccessBlock` — reads the account-level public access block configuration.
  * `s3:ListAccessPoints` — lists S3 Access Points.
  * `s3:ListAllMyBuckets` — lists all buckets in the account (commonly used by the AWS Console).
* Resource: `arn:aws:s3:::*` (bucket-level ARNs)
* Practical meaning: grants the principal permission to perform common listing and metadata read operations across buckets in the account.
* Important implementation note: some S3/listing actions (notably `s3:ListAllMyBuckets` and certain account-level APIs) do not support resource-level scoping and must use `"Resource": "*"`. Before deploying, verify each action's resource support in the AWS docs and adjust the Resource accordingly.

4. Statement: AllowS3Self

* Effect: Allow
* Action: `s3:*` (all S3 actions)
* Resource:
  * `arn:aws:s3:::carlossalazar` — bucket-level actions (e.g., bucket ACLs, policy)
  * `arn:aws:s3:::carlossalazar/*` — object-level actions inside the bucket
* Practical meaning: gives the principal full control over the specific bucket `carlossalazar` and its objects.
* Note: Some S3 APIs require bucket ARNs, some require object ARNs, and a few require both for a complete permission check. Including both ARNs covers typical API requirements for the bucket and its objects.

5. Statement: DenyS3Logs

* Effect: Deny (explicit deny)
* Action: `s3:*`
* Resource: `arn:aws:s3:::*log*` — matches bucket ARNs with `log` anywhere in the name
* Practical meaning: any bucket whose name contains the substring `log` will be denied all S3 actions at the bucket ARN level.
* Key caveat: the deny currently matches bucket ARNs only and does not match object ARNs (e.g., `arn:aws:s3:::my-log-bucket/object`). If the intention is to deny both bucket- and object-level actions for buckets containing `log`, the deny should include both `arn:aws:s3:::*log*` and `arn:aws:s3:::*log*/*`.
* Behavior: explicit denies always override allows. If an action and resource match both an Allow and this Deny, the Deny blocks the action.

## Key behaviors and implications

* Explicit Deny precedence: any explicit `Deny` matching an action and resource overrides `Allow` statements.
* Resource scoping: `arn:aws:s3:::bucket` vs `arn:aws:s3:::bucket/*` distinguishes bucket-level permissions from object-level permissions. Some S3 actions do not accept resource-level ARNs and must be given `"Resource": "*"`.
* Principle of least privilege: `s3:*` is broad and should be avoided unless necessary. Replace with a minimal set of actions to reduce risk.
* Pattern matching in ARNs: wildcard patterns like `*log*` match any bucket name containing `log` anywhere. Validate that this pattern reflects your intent and doesn't unintentionally match buckets like `catalog`.

## Interview-friendly concise answer

This policy has three statements: two allows and one explicit deny. The first Allow grants listing and metadata read permissions across buckets (verify whether some actions require `"Resource": "*"`, e.g., `s3:ListAllMyBuckets`). The second Allow grants full S3 permissions but only for the bucket `carlossalazar` and its objects. The Deny explicitly blocks all S3 actions on bucket ARNs that include `log` in the name—note it currently only covers bucket ARNs; to block object-level actions in those buckets, include `arn:aws:s3:::*log*/*`. Because explicit Deny overrides Allow, any matching Deny will prevent access even if an Allow would otherwise permit it.

## Suggested improvements and interview talking points

* Replace `s3:*` with the specific actions required (follow least-privilege).
* Add Conditions to narrow access (e.g., `aws:SourceIp`, `aws:MultiFactorAuthPresent`, or `aws:PrincipalIsAWSService`), if relevant.
* Confirm which S3 actions support resource-level scoping and adjust `Resource` values accordingly; some actions must use `"Resource": "*"`.
* If the Deny should block both bucket and object access for `*log*` buckets, add `arn:aws:s3:::*log*/*` in the Deny resource list.
* Validate wildcard patterns carefully to avoid accidental matches (e.g., `catalog` contains `log`).
* Explain explicit deny precedence and resource-level differences (bucket vs object) clearly during interviews.

<Callout icon="lightbulb">
  When walking through an IAM policy in an interview, systematically cover: Version, each Statement (Sid, Effect, Actions, Resources), resource scoping (bucket vs object vs service-level "\*"), explicit deny precedence, and least-privilege implications. Mention actionable improvements (narrow actions, add Conditions, correct resource scopes).
</Callout>

## References

* AWS IAM policy elements: [https://docs.aws.amazon.com/IAM/latest/UserGuide/access\_policies.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
* Amazon S3 actions, resources, and condition keys: [https://docs.aws.amazon.com/AmazonS3/latest/dev/using-with-s3-actions.html](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-with-s3-actions.html)

Understanding how to read and explain these policies is essential for diagnosing access issues and designing secure, least-privilege permissions in AWS.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-preparation-course/module/f1169a2e-23de-4377-bc4f-a07c136a11d6/lesson/b3e105db-c4f0-4634-bcb9-9d446891ee82" />
</CardGroup>
