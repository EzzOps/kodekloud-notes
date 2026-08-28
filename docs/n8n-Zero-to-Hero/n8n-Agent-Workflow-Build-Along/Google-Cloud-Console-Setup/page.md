# Google Cloud Console Setup

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Agent-Workflow-Build-Along/Google-Cloud-Console-Setup/page

Step by step guide to configure Google Cloud Console OAuth so n8n can authenticate and reuse a single credential for Google services such as Drive Sheets Gmail and Docs

In this guide you'll set up Google Cloud Console so n8n can authenticate with Google services (Drive, Gmail, Sheets, Docs, etc.) using a single OAuth credential you can reuse across Google nodes. The OAuth flow is the same for all Google-based nodes, so we’ll use the Google Drive node as the example.

Open your Google Drive node in n8n and create a new credential to begin.

<Frame>
  <img alt="The image shows a Google Drive Trigger configuration screen in an application interface, with options for setting poll times and selecting folders. The right side of the image is an output section with placeholder text." />
</Frame>

Overview — what you’ll do:

* Create or select a Google Cloud project.
* Configure the OAuth consent screen.
* Create an OAuth 2.0 Client ID (web application).
* Add n8n’s OAuth redirect URL to the client.
* Copy Client ID and Client Secret into n8n.
* Enable required Google APIs (Drive, Sheets, Gmail, Docs).
* Authenticate from n8n and test the integration.

Step-by-step instructions

1. Open Google Cloud Console

* Go to `https://console.cloud.google.com` and sign in with the Google account you want to use for API access.

2. Create or select a project

* Click the project drop-down (top-left) and choose New Project.
* Give the project a name (for example `n8n-demo-kk`) and set Location to “No organization” if applicable. Click Create, then Select.

<Frame>
  <img alt="The image shows a Google Cloud interface where a project named &#x22;n8n-test&#x22; is selected, and a notification indicates that the client ID has been copied to the clipboard." />
</Frame>

3. Configure the OAuth consent screen

* In the left menu go to APIs & Services > OAuth consent screen.
* Click Get started if prompted.
* Enter an App name (you can reuse your project name) and choose a Support email.
* For User Type choose `External` unless you have a Google Workspace domain and want `Internal`.
* Save and continue through the required fields.

<Frame>
  <img alt="The image shows a Google Cloud dashboard offering $300 in free credits for new users, along with notifications related to project creation." />
</Frame>

4. Create the OAuth 2.0 Client ID

* Go to APIs & Services > Credentials and click Create Credentials > OAuth client ID.
* Select Application type: `Web application`.
* Give the OAuth client a Name (for example `n8n-demo-kk`).

<Frame>
  <img alt="The image shows a Google Cloud interface for creating an OAuth client ID, with fields for application type, name, and authorized JavaScript and redirect URIs. A notification indicates that the OAuth configuration has been created." />
</Frame>

5. Add an Authorized redirect URI

* In n8n, when creating the Google credential, copy the OAuth Redirect URL shown in the credential form.
* Paste that exact redirect URL into Authorized redirect URIs in the Google Cloud dialog, then click Create.

6. Copy the Client ID and Client Secret

* After creating the OAuth client, copy the Client ID and Client Secret from the Google Cloud dialog.
* Paste them into the corresponding fields in the n8n Google credential.

<Frame>
  <img alt="The image shows a Google Cloud interface where an OAuth client ID has been successfully created, along with options to download the associated JSON file." />
</Frame>

Before finishing the OAuth flow in n8n, complete these two important items in the Google Cloud Console:

* Branding and Authorized domains:
  * In the OAuth consent screen > Branding section, add any Authorized domains you will use.
  * For n8n Cloud users add `n8n.cloud`. For self-hosted n8n add your host domain (for example `example.com`).
  * The authorized domain must match the domain portion of the redirect URI you provided.

* Enable the APIs you will use:
  * Search for and enable the Google APIs your workflows require (for example: Google Drive API, Gmail API, Google Sheets API, Google Docs API).

<Frame>
  <img alt="The image shows a configuration screen for connecting a Google Drive account using OAuth2 API, including fields for OAuth Redirect URL, Client ID, and Client Secret. There is also a &#x22;Sign in with Google&#x22; button visible." />
</Frame>

7. Set testing/publishing state

* In the OAuth consent screen, set the Publish status to `Testing` for development. For production you can submit the app for verification and publish it.
* Note: an unverified app will display a Google warning during sign-in; this is expected for development accounts.

<Callout icon="lightbulb">
  If you see a "Google hasn't verified this app" warning when signing in, that is expected for unverified apps. For development and testing you can proceed. To remove the warning for production, submit the app for verification through Google Cloud.
</Callout>

Optional — troubleshooting tip:

* If you receive redirect mismatch errors during sign-in, double-check the Authorized redirect URIs and Authorized domains in the OAuth consent screen. They must match the exact domain and path used in the n8n credential.

<Callout icon="warning">
  Ensure the redirect URI you add to Google Cloud exactly matches the OAuth Redirect URL shown in n8n (including protocol, domain, and path). A mismatch will cause Google sign-in to fail.
</Callout>

8. Authenticate from n8n

* Back in n8n’s Google credential dialog, click Sign in with Google.
* Choose the account and accept the requested permissions (scopes).
* Once authorized, n8n will display the account as connected.

9. Test the Google Drive trigger

* Configure the Google Drive Trigger node and choose the folder to watch.
* Click Fetch Test Event. If there’s no recent activity you may see “no data with the current filter.”
* Upload a file (for example an `.xlsx`) to the selected Drive folder, then click Fetch Test Event again. The node should receive the new file metadata and trigger.

<Frame>
  <img alt="The image shows a software interface for configuring a Google Drive Trigger, which includes parameters like poll times and folder selection. It also displays a button labeled &#x22;Fetch Test Event&#x22; and an area for executing or setting mock data." />
</Frame>

Repeat for other Google services

* After you enable an API in Google Cloud (Sheets, Gmail, Docs, etc.), you can use the same OAuth credential in n8n to connect those nodes. The OAuth client, redirect URI, and authorized domains remain the same — only enable the additional APIs you need.

Quick reference — common Google APIs to enable

| API               | Use case                                      | Docs                                                                                 |
| ----------------- | --------------------------------------------- | ------------------------------------------------------------------------------------ |
| Google Drive API  | File metadata, upload/download, watch folders | [https://developers.google.com/drive/api](https://developers.google.com/drive/api)   |
| Google Sheets API | Read/write Sheets data, append rows           | [https://developers.google.com/sheets/api](https://developers.google.com/sheets/api) |
| Gmail API         | Send and read emails                          | [https://developers.google.com/gmail/api](https://developers.google.com/gmail/api)   |
| Google Docs API   | Read and update Google Docs content           | [https://developers.google.com/docs/api](https://developers.google.com/docs/api)     |

Links and references

* Google Cloud Console: `https://console.cloud.google.com`
* n8n: [https://n8n.io/](https://n8n.io/)
* Google API docs:
  * Google Drive API — [https://developers.google.com/drive/api](https://developers.google.com/drive/api)
  * Google Sheets API — [https://developers.google.com/sheets/api](https://developers.google.com/sheets/api)
  * Gmail API — [https://developers.google.com/gmail/api](https://developers.google.com/gmail/api)
  * Google Docs API — [https://developers.google.com/docs/api](https://developers.google.com/docs/api)

That’s it — once the OAuth client and APIs are configured, you can connect Drive and any other Google services in n8n using the same OAuth credential and reuse it across nodes and workflows.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/6045516d-9973-433b-8ce3-99f78a1b3c15/lesson/b4e9cd1a-eb37-40bb-a525-4123655e1f7c" />
</CardGroup>
