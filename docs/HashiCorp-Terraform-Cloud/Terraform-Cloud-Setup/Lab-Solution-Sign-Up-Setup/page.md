# (Paste your token here)
```

Terraform will store the credentials for subsequent CLI operations.

## 6. Interacting with Terraform Cloud via API

First, export your token as an environment variable:

```bash theme={null}
export TERRAFORM_TOKEN="YOUR_TOKEN"
```

Then request your organization’s details:

```bash theme={null}
curl \
  --header "Authorization: Bearer $TERRAFORM_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  https://app.terraform.io/api/v2/organizations/Mastering-Terraform-Cloud
```

A successful response returns your organization’s metadata in JSON:

```json theme={null}
{
  "data": {
    "id": "Mastering-Terraform-Cloud",
    "type": "organizations",
    "attributes": {
      "external-id": "org-tsVGG3U6yVQPMxxJ",
      "created-at": "2022-08-18T16:34:58.952Z",
      "email": "gabe@maentz.net",
      "session-timeout": null,
      "session-remember": null,
      "collaborator-auth-policy": "password",
      "plan-identifier": "free",
      "allow-force-delete-workspaces": true,
      "name": "Mastering-Terraform-Cloud",
      "permissions": {
        "can-update": true,
        "can-destroy": true,
        "can-access-via-teams": true
      }
    }
  }
}
```

For full API details, see the [Terraform Cloud API Reference](https://developer.hashicorp.com/terraform/cloud/api-docs).

## 7. Terraform Cloud API Token Types

Terraform Cloud supports these token types:

| Token Type         | Scope                                            | Use Case                          |
| ------------------ | ------------------------------------------------ | --------------------------------- |
| User Token         | Individual user permissions                      | Personal CLI & API access         |
| Team Token         | Specific team privileges                         | Automation with team-level access |
| Organization Token | Organization-wide management (teams, workspaces) | Scripts managing org resources    |

<Frame>
  ![The image shows a web interface for managing API tokens in Terraform Cloud, with options to create a new token and a list of existing tokens.](https://kodekloud.com/kk-media/image/upload/v1752878838/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/terraform-cloud-api-tokens-management.jpg)
</Frame>

<Frame>
  ![The image shows a webpage from Terraform Cloud's settings, specifically the API Tokens section, detailing user, team, and organization tokens. It includes navigation options on the left and a button to create an organization token.](https://kodekloud.com/kk-media/image/upload/v1752878839/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/terraform-cloud-api-tokens-settings.jpg)
</Frame>

***

This concludes our demonstration of web UI, CLI, and API authentication with Terraform Cloud.

<Frame>
  ![The image shows a settings page for authentication in a web application, detailing user session timeout and two-factor authentication options. It includes fields for setting session timeout and reauthentication intervals, with an option to require two-factor authentication for organization members.](https://kodekloud.com/kk-media/image/upload/v1752878840/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/authentication-settings-page-user-session-timeout.jpg)
</Frame>

## Links and References

* [Terraform Cloud Documentation](https://developer.hashicorp.com/terraform/cloud)
* [Terraform CLI Guide](https://developer.hashicorp.com/terraform/cli)
* [Terraform Cloud API Reference](https://developer.hashicorp.com/terraform/cloud/api-docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/f0c13760-a79c-42c2-a089-44f1c0a59bee/lesson/afdfcd55-1df4-4678-a4ba-2ce1b91a2837" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/f0c13760-a79c-42c2-a089-44f1c0a59bee/lesson/a3ac255f-5847-4bee-9737-9cfb17072145" />
</CardGroup>


# Lab Solution Sign Up Setup

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Terraform-Cloud-Setup/Lab-Solution-Sign-Up-Setup/page

This hands-on lab guides you through signing up for Terraform Cloud and integrating it with the Terraform CLI.

Welcome to this hands-on lab. In this guide, you’ll sign up for Terraform Cloud, create your first organization, and integrate the Terraform CLI with Terraform Cloud. By the end, you’ll be ready to manage infrastructure seamlessly across any cloud.

<Frame>
  ![The image shows a webpage from KodeKloud about Terraform Cloud signup and setup, with a terminal interface on the right side.](https://kodekloud.com/kk-media/image/upload/v1752878842/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Sign-Up-Setup/kodekloud-terraform-cloud-signup-setup.jpg)
</Frame>

***

## Table of Contents

* [Task 1: Sign Up for Terraform Cloud](#task-1-sign-up-for-terraform-cloud)
* [Task 2: Create a Terraform Cloud Organization](#task-2-create-a-terraform-cloud-organization)
* [Task 3: Authenticate via the CLI](#task-3-authenticate-via-the-cli)
* [Summary of Tasks](#summary-of-tasks)
* [Links and References](#links-and-references)

***

## Task 1: Sign Up for Terraform Cloud

Begin by navigating to the Terraform website:

1. Go to terraform.io and click **Try Terraform Cloud**.
2. On the signup form, enter your desired **Username**, **Email**, and **Password**, then submit.

<Frame>
  ![The image shows a webpage for HashiCorp Terraform, highlighting options for automating infrastructure on any cloud with links to download the open-source version or try Terraform Cloud.](https://kodekloud.com/kk-media/image/upload/v1752878843/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Sign-Up-Setup/hashicorp-terraform-automation-webpage.jpg)
</Frame>

<Frame>
  ![The image shows a Terraform Cloud account creation page with fields for username, email, and password, alongside a section highlighting the benefits of using Terraform Cloud.](https://kodekloud.com/kk-media/image/upload/v1752878844/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Sign-Up-Setup/terraform-cloud-account-creation-page.jpg)
</Frame>

<Callout icon="lightbulb">
  If you already have an account, click **Sign In** instead of creating a new one.
</Callout>

***

## Task 2: Create a Terraform Cloud Organization

Once you’re logged in, Terraform Cloud prompts you to create a new organization if none exists. Organization names must be unique across all Terraform Cloud users.

1. Enter a globally unique **Organization Name**.
2. Confirm your email address.
3. Click **Create organization**.

<Frame>
  ![The image shows a webpage for creating a new organization in Terraform Cloud, with fields for organization name and email address. There is a button labeled "Create organization" at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878845/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Sign-Up-Setup/terraform-cloud-create-organization-page.jpg)
</Frame>

In this lab, our example org is named **Mastering Terraform Cloud**. You’ll see the new organization dashboard, ready for workspace and settings configuration.

***

## Task 3: Authenticate via the CLI

To link your local Terraform CLI to Terraform Cloud, generate an API token:

1. Run the login command in your terminal:
   ```bash theme={null}
   terraform login
   ```
2. When prompted, confirm by typing `yes`:
   ```text theme={null}
   Do you want to proceed?
   Only 'yes' will be accepted to confirm.
   Enter a value: yes
   ```
3. Terraform opens a browser window to the tokens page:
   ```text theme={null}
   Open the following URL to access the tokens page for app.terraform.io:
   https://app.terraform.io/app/settings/tokens?source=terraform-login
   ```
4. On the Terraform Cloud website, create a new token (e.g., **Terraform login – Mastering Terraform Cloud**) and copy it.

<Frame>
  ![The image shows a web page with a pop-up window displaying a newly created API token for Terraform Cloud. The token is shown with an option to copy it, and there is a "Done" button at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878846/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Sign-Up-Setup/terraform-cloud-api-token-popup.jpg)
</Frame>

5. Paste the token back into the CLI (it will be hidden as you type):
   ```bash theme={null}
   Token for app.terraform.io:
   Enter a value: <paste-your-token>
   ```

Upon successful authentication, you’ll see a confirmation message:

```plaintext theme={null}
Retrieved token for user <your_username>
Welcome to Terraform Cloud!
Documentation: terraform.io/docs/cloud
New to TFC? Follow these steps to instantly apply an example configuration:
  $ git clone https://github.com/hashicorp/tfc-getting-started.git
  $ cd tfc-getting-started
  $ scripts/setup.sh
```

<Callout icon="triangle-alert">
  Your API token is stored in plain text at `~/.terraform.d/credentials.tfrc.json`. To remove it, run:

  ```bash theme={null}
  terraform logout
  ```
</Callout>

***

## Summary of Tasks

| Task                            | Description                                            |
| ------------------------------- | ------------------------------------------------------ |
| 1. Sign Up for Terraform Cloud  | Create your free Terraform Cloud account               |
| 2. Create a Terraform Cloud Org | Choose a unique name and confirm your email            |
| 3. Authenticate via the CLI     | Generate and store an API token for `app.terraform.io` |

***

## Links and References

* [Terraform Cloud Documentation](https://www.terraform.io/docs/cloud)
* [Terraform CLI Reference](https://www.terraform.io/docs/cli)
* [Terraform Getting Started Examples](https://github.com/hashicorp/tfc-getting-started)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/f0c13760-a79c-42c2-a089-44f1c0a59bee/lesson/6e792ad8-1137-42a2-a8fb-22241d2ae73e" />
</CardGroup>
