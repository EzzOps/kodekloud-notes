# Log in to Terraform Cloud or Enterprise
terraform login [hostname]

# Log out and remove your local credentials
terraform logout [hostname]
```

> **lightbulb** When you run `terraform login`, the CLI opens your browser to generate a user API token. Paste the token back into the terminal. Credentials are saved to `~/.terraform.d/credentials.tfrc.json`.

> **triangle-alert** To fully revoke a token, delete it from **User Settings** in the Terraform Cloud web UI. Running `terraform logout` only removes the token locally.

CLI authentication is required for commands like `terraform plan` and `terraform apply` when your state and configurations live in Terraform Cloud.

For more details, see [Terraform CLI Authentication](https://www.terraform.io/internals/terraform-cli#authentication).

***

## Terraform Cloud API

Use Terraform Cloud’s REST API for programmatic access. Every request must include a valid bearer token:

```bash theme={null}
curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request GET \
  https://app.terraform.io/api/v2/organizations?page[number]=1&page[size]=20
```

> **lightbulb** Replace `$TOKEN` with your user, team, or organization token. Ensure `Content-Type` is set to `application/vnd.api+json`.

All API endpoints require authentication and follow the [JSON:API](https://jsonapi.org/) specification.

***

## Token Types

![The image is an informational slide about token-based authentication, detailing user, team, and organization tokens, with links for further information. It includes cartoon characters at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878824/notes-assets/images/HashiCorp-Terraform-Cloud-Authenticate-to-Terraform-Cloud/token-based-authentication-info-slide.jpg)

Choose the appropriate token for your workflow:

| Token Type         | Permissions                             | Use Case                     | Management Location   |
| ------------------ | --------------------------------------- | ---------------------------- | --------------------- |
| User Token         | Matches your personal account           | Interactive CLI tasks        | User Settings         |
| Team Token         | Inherits team-level permissions         | Automated CI/CD pipelines    | Teams Page            |
| Organization Token | Full org management (teams, workspaces) | Organization-wide automation | Organization Settings |

***

## Managing Authentication

Organization owners can enforce additional security policies:

![The image is about "Managing Authentication" and features icons representing Multi-Factor Authentication, SSH Keys, and Session Duration.](https://kodekloud.com/kk-media/image/upload/v1752878826/notes-assets/images/HashiCorp-Terraform-Cloud-Authenticate-to-Terraform-Cloud/managing-authentication-mfa-ssh-keys.jpg)

* **Multi-Factor Authentication (MFA)**\
  Enforce two-factor authentication for all members.
* **Single Sign-On (SSO)**\
  Integrate with external identity providers (Business tier only).
* **SSH Keys**\
  Add private keys at the org level for workspaces that need access to private Git repositories.
* **Session Duration**\
  Configure inactivity timeouts and maximum session lengths to require periodic reauthentication.

> **triangle-alert** SSO is only available on the Business tier. Ensure your organization plan supports it before configuring.

***

In this module, we covered:

* Accessing Terraform Cloud via the web interface
* Authenticating with the Terraform CLI
* Using the Terraform Cloud REST API
* Understanding user, team, and organization tokens
* Enforcing organizational security policies (MFA, SSO, SSH keys, session timeouts)

With these authentication methods and policies in place, you can securely manage infrastructure at scale.

## Links and References

* [Terraform Cloud Authentication](https://www.terraform.io/cloud-docs/users-teams-organizations/authentication)
* [Terraform CLI Documentation](https://www.terraform.io/cli)
* [Terraform Cloud API Reference](https://www.terraform.io/cloud-docs/api)
* [JSON:API Specification](https://jsonapi.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/f0c13760-a79c-42c2-a089-44f1c0a59bee/lesson/093a8a00-ad16-4e00-b2bf-468de4cbbefd)


# Demo Interacting with Terraform Cloud

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Terraform-Cloud-Setup/Demo-Interacting-with-Terraform-Cloud/page

Learn to authenticate with Terraform Cloud using web UI, CLI, and API, covering security settings, SSH key management, and token types.

In this lesson, you’ll learn how to sign in and interact with Terraform Cloud through the web UI, CLI, and API. We’ll cover user and organization-level security settings, SSH key management, and token types.

## 1. Logging into Terraform Cloud Web UI

1. Navigate to the Terraform Cloud login page and enter your HCP account or username/email credentials.

![The image shows a login page for HashiCorp Terraform Cloud, with options to sign in using an HCP account or by entering a username or email. A dropdown menu suggests different email options for login.](https://kodekloud.com/kk-media/image/upload/v1752878827/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/terraform-cloud-login-page-options.jpg)

2. If you belong to multiple organizations, select the one you want to access.

![The image shows a webpage from Terraform Cloud where a user can choose from a list of organizations to access, including "Enterprise-Cloud," "Enterprise-DataCenter," and "Mastering-Terraform-Cloud."](https://kodekloud.com/kk-media/image/upload/v1752878829/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/terraform-cloud-organizations-selection-page.jpg)

## 2. Configuring User-Level Authentication

1. Click your user avatar and select **User Settings** → **Account Settings**.

![The image shows a Terraform Cloud interface with no workspaces created yet, and a user menu open displaying options like "User settings" and "Sign out."](https://kodekloud.com/kk-media/image/upload/v1752878830/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/terraform-cloud-interface-no-workspaces.jpg)

2. Under **Authentication**, enable Two-Factor Authentication (2FA). You can choose an authentication app or SMS.

![The image shows a webpage for setting up two-factor authentication, offering options for using an application or SMS for verification. It includes a field for entering a phone number and a button to enable 2FA.](https://kodekloud.com/kk-media/image/upload/v1752878832/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/two-factor-authentication-setup-webpage.jpg)

3. For app-based 2FA, scan the QR code and enter the generated one-time password.

![The image shows a webpage for verifying two-factor authentication, featuring a QR code and a field to enter an authentication code.](https://kodekloud.com/kk-media/image/upload/v1752878833/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/two-factor-authentication-verification-qr-code.jpg)

> **triangle-alert** Always save your backup codes in a secure location. Losing access to your 2FA device can lock you out of Terraform Cloud.

Once verified, 2FA is active on your account.

## 3. Organization-Level Security Policies

Switch to your organization (e.g., **Mastering Terraform Cloud**), then go to **Settings** → **Authentication**. Here you can:

* Require that all members enable 2FA
* Configure session inactivity timeouts
* Set reauthentication intervals

![The image shows a web interface for managing two-factor authentication settings, with options to disable 2FA and reveal backup codes. It includes a dropdown menu for selecting an organization.](https://kodekloud.com/kk-media/image/upload/v1752878834/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/two-factor-authentication-settings-interface.jpg)

![The image shows a settings page for authentication in Terraform Cloud, detailing user session timeout and two-factor authentication options. It includes fields for setting session timeout and reauthentication intervals, with options to update user sessions and require two-factor authentication.](https://kodekloud.com/kk-media/image/upload/v1752878835/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/terraform-cloud-authentication-settings-page.jpg)

> **lightbulb** Customizing session timeouts helps balance security and usability across your organization.

## 4. Managing SSH Keys for Git Operations

At the organization level, upload SSH private keys to enable Git-based operations. To generate an RSA key in PEM format:

```bash theme={null}
ssh-keygen -t rsa -m PEM
```

## 5. Authenticating with Terraform CLI

On your local machine with Terraform installed, run:

```bash theme={null}
terraform login
```

This command will open your browser to generate an API token, then return you to the CLI.

![The image shows a command-line interface prompting the user to generate and enter a token for Terraform, with instructions to open a web browser to obtain the token.](https://kodekloud.com/kk-media/image/upload/v1752878836/notes-assets/images/HashiCorp-Terraform-Cloud-Demo-Interacting-with-Terraform-Cloud/terraform-token-generation-command-line.jpg)

When prompted, paste your token (input is hidden):

```bash theme={null}
