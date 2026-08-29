# Demo Cloud IAM Roles and Permissions

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Identity-and-Access-Management-IAM-in-GCP/Demo-Cloud-IAM-Roles-and-Permissions/page

Guide to creating a custom Google Cloud IAM role, assigning it to a service account, generating JSON keys, and verifying Cloud Storage read permissions.

Hello and welcome back.

In this lesson we create a custom IAM role in Google Cloud, attach it to a service account, and verify the permissions. The primary steps are:

* Create a custom IAM role with specific Cloud Storage read permissions.
* Create a service account and attach the custom role.
* Generate and download a service account key (JSON) for external use.
* Verify access from Cloud Shell or a local client.

> **lightbulb** This guide demonstrates the Console workflow and provides equivalent `gcloud` commands so you can automate or repeat the steps. Replace `PROJECT_ID`, `ROLE_ID`, `SA_NAME`, `SA_EMAIL`, `BUCKET`, and `OBJECT` with your actual values.

First, open the GCP Console and go to "IAM & Admin". You can reach it via the Quick access links or by searching the console search bar. Click the IAM entry to open the IAM page; this view shows principals and their assigned roles. Switch to the Roles tab to view custom and predefined roles.

<Frame>
  <img alt="A screenshot of the Google Cloud Console IAM page showing permissions for the project &#x22;KodeKloud-GCP-Training,&#x22; with tabs to view roles and options to grant or remove access. The roles listed include Cloud Data Fusion Runner, Dataproc Worker, Editor, kodekloud.storage.viewer, and Owner." />
</Frame>

## 1. Create a custom IAM role (Console)

* In the left-hand panel click **Roles**, then click **Create Role**.
* Enter a descriptive **Title** (example: `KodeKloudStorageViewer`), **Description** (example: `KodeKloudCustomRole for viewing storage bucket and object`), and an **ID** (lowercase, URL-safe string such as `kodekloudstoragerviewer1`) — the console may suggest an ID automatically.
* Choose the stage (e.g., General Availability) and proceed to add permissions.

When building a read-only storage role, add only the permissions required. For this demo we add these four read permissions:

| Permission             | Purpose                       |
| ---------------------- | ----------------------------- |
| `storage.buckets.list` | List buckets in a project     |
| `storage.buckets.get`  | Get bucket metadata           |
| `storage.objects.list` | List objects in a bucket      |
| `storage.objects.get`  | Read object data and metadata |

Search for each permission in the permissions selector and click **Add** for each.

<Frame>
  <img alt="A screenshot of the Google Cloud Console IAM &#x22;Create role&#x22; page with a custom role named &#x22;kodekloud.storage.viewer&#x22; being created. The form is populated and shows four selected storage permissions (storage.buckets.get, storage.buckets.list, storage.objects.get, storage.objects.list)." />
</Frame>

Important: these four permissions are read-only — they do not allow uploading, modifying, or deleting buckets or objects. For write or delete capabilities add `storage.objects.create`, `storage.objects.delete`, or `storage.buckets.create` as needed, or use a predefined role such as Storage Object Viewer / Storage Object Admin.

After adding permissions, click **Create**. If you previously created and deleted a similar role you may see multiple entries; ensure you pick the enabled role and use a unique ID when creating new roles.

<Frame>
  <img alt="A screenshot of the Google Cloud Console showing the IAM & Admin &#x22;Roles&#x22; page for the &#x22;KodeKloud-GCP-Training&#x22; project. It lists role names, where they're used, and their status (enabled/deleted) in a table." />
</Frame>

Alternative: create the same custom role with `gcloud` (example)

```bash theme={null}
gcloud iam roles create kodekloudstoragerviewer1 \
  --project=PROJECT_ID \
  --title="KodeKloudStorageViewer" \
  --description="KodeKloudCustomRole for viewing storage bucket and object" \
  --permissions="storage.buckets.list,storage.buckets.get,storage.objects.list,storage.objects.get" \
  --stage=GA
```

## 2. Attach the role to a user or service account

You can attach the custom role to a user via IAM -> Grant Access, or assign it to a service account. This demo creates a service account and assigns the custom role during creation.

* In the side panel select **Service Accounts** and click **Create Service Account**.
* Provide a **Name** (example: `kodekloud-test-sa`) — the Service account ID is auto-generated and editable — add a description, then click **Create and Continue**.
* On the Permissions step, search for your custom role (e.g., `kodekloud.storage.viewer` or your custom role ID) and assign it. If a role appears deleted or disabled you may get an error such as "Failed to add project roles" — choose the enabled version.

<Frame>
  <img alt="A Google Cloud Console screenshot of the &#x22;Create service account&#x22; IAM page showing the Permissions step with the role &#x22;kodekloud.storage.viewer&#x22; selected. A red warning reads &#x22;Failed to add project roles&#x22; and buttons like Continue and Done are visible." />
</Frame>

Finish creation and refresh the Service Accounts list — the new service account should now be visible.

<Frame>
  <img alt="A screenshot of the Google Cloud Console showing the IAM & Admin &#x22;Service accounts&#x22; page for the project &#x22;KodeKloud-GCP-Training.&#x22; It displays a table of service account emails, their statuses (Enabled), names, descriptions, and OAuth2 client IDs." />
</Frame>

Equivalent `gcloud` commands to create the SA and bind the custom role:

```bash theme={null}
