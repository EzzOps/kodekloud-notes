# Demo Creating a base IAM user

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/AWS-CloudFormation-Introduction/Demo-Creating-a-base-IAM-user/page

Guide to creating a base AWS IAM user with administrative permissions and MFA to get started with CloudFormation, with recommendations for least-privilege practices.

This demo shows how to create a base AWS IAM user with the permissions and settings needed to start using AWS CloudFormation. Follow the steps below in the AWS Management Console. These instructions focus on getting a working administrative user quickly — you should refine permissions later to follow least-privilege practices.

Why this matters: CloudFormation needs an IAM identity with sufficient permissions to create and manage resources in your account. Creating a dedicated IAM user for demos or CI/CD access helps isolate credentials from the root account.

Resources

* [AWS Identity and Access Management (IAM) documentation](https://docs.aws.amazon.com/iam/)
* [AWS CloudFormation documentation](https://docs.aws.amazon.com/cloudformation/)
* [AWS multi-factor authentication (MFA) guidance](https://docs.aws.amazon.com/iam/latest/UserGuide/id_credentials_mfa.html)

Steps

1. Open the AWS Management Console and go to IAM

* In the services search, type “IAM” and select the IAM service.

2. Create a new user

* In the IAM console navigation, choose Users → Create user.
* Enter a username (in this demo we use `mono-cfn`).
* Under “Select AWS access type,” enable AWS Management Console access.
* For Console password, choose “Custom password” and enter a secure password you will save.
  * If you do not want the user to be required to change the password on first sign-in, uncheck “Require password reset.”

3. Assign permissions

* Click Next to reach the Permissions step.
* You can attach policies directly to the user or create and use an IAM group (group-based permissions are recommended for production).
* For a quick start in this demo, attach the managed policy `AdministratorAccess` to the user so the account can run CloudFormation and related services. You should later replace this with a least-privilege policy tailored to your CloudFormation templates.

<Frame>
  <img alt="A screenshot of the AWS IAM console on the &#x22;Create user&#x22; page showing a list of policies to attach. The table shows AWS-managed policies with &#x22;AdministratorAccess&#x22; checked and pagination controls on the right." />
</Frame>

4. Create the user and save credentials

* Click Next, review the settings, then click Create user.
* Save the password or download the CSV from the console when prompted — you will need these credentials to sign in as the new user.
* After creation, choose Return to users list (or Continue) to view your users.

<Frame>
  <img alt="A screenshot of the AWS Identity and Access Management (IAM) Users page listing two users (arno and arno-cf) with columns for groups, last activity, MFA, and password age. The page header shows Create user and Delete buttons." />
</Frame>

5. Get the IAM user sign-in URL

* From the IAM dashboard, copy the “IAM user sign-in link” — it’s unique to your AWS account.
* Save or open this link in a new tab so you can sign in as the IAM user.

6. Sign in as the IAM user

* Sign out of the root account, then open the IAM user sign-in URL.
* Sign in with the IAM username (e.g., `mono-cfn`) and the password you saved.

<Frame>
  <img alt="A browser screenshot of the AWS IAM user sign-in page showing fields for account ID, IAM username (filled), a masked password, and a &#x22;Sign in&#x22; button. To the right is an Amazon Lightsail promotional banner with streaking light graphics and a simple robot illustration." />
</Frame>

7. Set your preferred region

* After signing in, set the AWS region in the console (top-right).
* For consistency across this tutorial, set the region to US East (N. Virginia). Using a single region avoids region-related differences in resource availability and pricing.

<Frame>
  <img alt="A screenshot of the AWS Management Console Home page with the region selector expanded, listing regions like N. Virginia, Ohio, Tokyo, and Mumbai. The main panel shows &#x22;No recently visited services,&#x22; and the Windows taskbar is visible along the bottom." />
</Frame>

8. Enable multi-factor authentication (MFA)

* For security, enable MFA on the IAM user from the IAM dashboard or the user’s Security credentials tab.
* Follow the console’s MFA setup flow (use a virtual MFA app such as Google Authenticator or Authy).

<Frame>
  <img alt="Screenshot of the AWS Identity and Access Management (IAM) dashboard. It shows security recommendations including that the root user has MFA, a prompt to &#x22;Add MFA for yourself,&#x22; and a note about user access key status." />
</Frame>

> **lightbulb** Best practice: use IAM groups for assigning permissions to multiple users, enable MFA for all privileged identities, and apply the principle of least privilege. AdministratorAccess is used here only to simplify getting started — tighten permissions before using this user for production workloads.

Quick reference table

| Setting          | Recommended value for demo       | Production guidance                                                                             |
| ---------------- | -------------------------------- | ----------------------------------------------------------------------------------------------- |
| Username         | mono-cfn (example)               | Use a descriptive, unique name (e.g., ci-cfn-deployer)                                          |
| Access type      | AWS Management Console           | Prefer IAM roles for automation; use IAM users or roles with programmatic keys only when needed |
| Console password | Custom password (saved securely) | Use strong password policy and rotate credentials                                               |
| Attached policy  | AdministratorAccess (demo)       | Create least-privilege IAM policies or use role-based access                                    |
| MFA              | Enable (virtual MFA app)         | Required for all privileged users                                                               |

What you have after completing these steps

* A dedicated IAM user capable of running CloudFormation with administrative permissions (for this demo).
* Console access via the account-specific IAM sign-in URL.
* MFA enabled to protect the account (if you completed step 8).

Next steps

* Replace AdministratorAccess with a least-privilege policy scoped to the CloudFormation templates and resources you will deploy.
* Consider creating an IAM group for CloudFormation operators and adding users to that group.
* For CI/CD systems, create an IAM role with narrowly scoped permissions and use temporary credentials.

Further reading

* [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
* [CloudFormation security and access control](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/security.html)

You should now have a base IAM user and be ready to continue with CloudFormation exercises.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/2ec6349c-f14b-48d2-8049-b313938d561e/lesson/e58b0250-efac-42f4-926c-70ed9b6fddde)
