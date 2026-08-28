# Create a service account
gcloud iam service-accounts create kodekloud-test-sa \
  --display-name="KodeKloud Test Service Account" \
  --project=PROJECT_ID

# Grant the custom role to the service account
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:kodekloud-test-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="projects/PROJECT_ID/roles/kodekloudstoragerviewer1"
```

## 3. Create and download a service account key (JSON)

If you plan to use this service account from outside GCP (for local development, CI, or other systems), generate a key:

* Click the service account to open its details page.
* Select the **Keys** tab, click **Add Key -> Create new key**, choose **JSON**, and click **Create**.
* The JSON key will be downloaded to your machine.

<Frame>
  <img alt="A Google Cloud Console screenshot showing the IAM & Admin service accounts keys page with a popup saying &#x22;Private key saved to your computer&#x22; and a downloaded JSON key file. The page warns about security risks of service account keys and provides options to add keys." />
</Frame>

You can also create a key using `gcloud`:

```bash theme={null}
gcloud iam service-accounts keys create key.json \
  --iam-account=kodekloud-test-sa@PROJECT_ID.iam.gserviceaccount.com \
  --project=PROJECT_ID
```

<Callout icon="warning">
  Service account JSON keys are long-lived credentials that grant access to your project. Treat these files like secrets: store them securely, rotate them regularly, and avoid committing them to source control. When possible prefer Workload Identity (for GKE), Workload Identity Federation, or short-lived tokens instead of downloading keys.
</Callout>

## 4. Verify permissions (Cloud Shell or local client)

To authenticate using the downloaded JSON key:

```bash theme={null}
# Option A: Activate the service account for gcloud
gcloud auth activate-service-account --key-file=key.json

# Option B: Set GOOGLE_APPLICATION_CREDENTIALS for SDKs and client libraries
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

Test read-only access to Cloud Storage (examples):

```bash theme={null}
# List buckets (requires storage.buckets.list)
gsutil ls

# List objects in a bucket (requires storage.objects.list)
gsutil ls gs://BUCKET

# Read an object to stdout (requires storage.objects.get)
gsutil cat gs://BUCKET/OBJECT
```

If you attempt an action not covered by the custom role (for example, `gsutil cp` to upload or `gsutil rm` to delete), you'll receive an error indicating insufficient permissions. Use this to validate that the role is properly scoped as read-only.

## Wrap-up

You now have:

* A custom read-only Cloud Storage role,
* A service account with that role attached,
* A JSON key downloaded for external authentication,
* Commands to verify permissions locally or in Cloud Shell.

Next: test access in your application or CI environment using the JSON key or adopt Workload Identity / Workload Identity Federation for better security posture.

## Links and references

* [IAM roles and permissions overview (Google Cloud)](https://cloud.google.com/iam/docs/understanding-roles)
* [Creating and managing custom roles](https://cloud.google.com/iam/docs/creating-custom-roles)
* [Service accounts overview](https://cloud.google.com/iam/docs/service-accounts)
* [Best practices for service accounts and keys](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys)
* gsutil documentation: [https://cloud.google.com/storage/docs/gsutil](https://cloud.google.com/storage/docs/gsutil)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9dd8e9-0075-430e-92db-757c9a6b738a/lesson/95badab2-e79b-40b1-a4fb-795d2df473e0" />
</CardGroup>


# Demo Using Service account in local editor

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Identity-and-Access-Management-IAM-in-GCP/Demo-Using-Service-account-in-local-editor/page

Guide to using a downloaded Google Cloud service account JSON key locally with gcloud CLI to authenticate, verify permissions, adjust roles, and clean up credentials.

Welcome back. In a previous lesson we created:

* a custom IAM role that allows listing Cloud Storage buckets and objects,
* a service account, and
* a service account key (JSON).

This article shows how to use that downloaded service account key locally so the gcloud CLI acts as the service account while you develop or test. Follow the steps below to authenticate, verify permissions, adjust role permissions if needed, and clean up local credentials.

<Callout icon="lightbulb">
  Service account keys are sensitive. Store them only on trusted machines, delete them when no longer needed, and rotate keys if they are exposed.
</Callout>

What the service account key looks like
Below is an example of the JSON key file you download from the Cloud Console. Your file will include the same fields; `private_key` is shortened here.

```json theme={null}
{
  "type": "service_account",
  "project_id": "kodekloud-gcp-training",
  "private_key_id": "79980d36ed10010b4098be95fcf3ccdbf36bc404",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC...\n-----END PRIVATE KEY-----\n",
  "client_email": "kodekloud-test-sa@kodekloud-gcp-training.iam.gserviceaccount.com",
  "client_id": "115919895903955568351",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kodekloud-test-sa%40kodekloud-gcp-training.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```

Prerequisite: gcloud CLI
Install and configure the gcloud CLI first: [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

On macOS, if you see Python-related errors (for example `ModuleNotFoundError: No module named 'imp'`), point the Cloud SDK to a compatible Python binary. Example:

```bash theme={null}
export CLOUDSDK_PYTHON=/opt/homebrew/bin/python3.11
```

Step 1 — Activate the service account locally
With the JSON key file in your working directory (here named `kodekloud-gcp-training-79980d36ed10.json`), run:

```bash theme={null}
gcloud auth activate-service-account --key-file=kodekloud-gcp-training-79980d36ed10.json
```

Expected response:

```text theme={null}
Activated service account credentials for: [kodekloud-test-sa@kodekloud-gcp-training.iam.gserviceaccount.com]
```

Step 2 — Set the active project
Set the project for subsequent gcloud commands. Permissions are evaluated against the project and resources in this context:

```bash theme={null}
gcloud config set project kodekloud-gcp-training
```

If you do not have access you might be prompted to confirm:

```text theme={null}
WARNING: You do not appear to have access to project [kodekloud-gcp-training] or it does not exist.
Are you sure you wish to set property [core/project] to kodekloud-gcp-training?

Do you want to continue (Y/n)? Y

Updated property [core/project].
```

Step 3 — Verify the service account permissions
Test an operation the custom role allows (list Cloud Storage buckets):

```bash theme={null}
gcloud storage ls
```

Example output (lists buckets visible to the service account):

```text theme={null}
gs://data-proc-demo-kodekloud/
gs://dataflow-staging-us-central1-240657367796/
...
gs://temp_data_kodekloud/
```

Now test an operation that the custom role does *not* include (list Compute Engine instances):

```bash theme={null}
gcloud compute instances list
```

If the service account lacks `compute.instances.list`, you'll see an error like:

```text theme={null}
ERROR: (gcloud.compute.instances.list) Some requests did not succeed:
 - Required 'compute.instances.list' permission for 'projects/kodekloud-gcp-training'
```

Step 4 — Add missing permission to the custom role (if needed)
If you require additional permissions, edit the custom role in the Cloud Console:

1. Go to IAM & Admin → Roles.
2. Open your custom role (e.g., `kodekloud.storage.viewer`).
3. Click Edit role → Add permissions.
4. Search for `compute.instances.list`, add it, and Update.

<Frame>
  <img alt="A Google Cloud Console screenshot showing the IAM & Admin &#x22;Edit role&#x22; page for a custom role (kodekloud.storage.viewer) with an &#x22;Add permissions&#x22; dialog open listing compute.instance permissions. The left side shows assigned storage permissions and role details." />
</Frame>

After updating the role, rerun:

```bash theme={null}
gcloud compute instances list
```

If the service account now has `compute.instances.list` but there are no instances in the project, the command returns:

```text theme={null}
Listed 0 items.
```

This confirms that local authentication and role permission changes are effective.

Step 5 — Cleaning up and revoking local credentials
When finished, list active accounts:

```bash theme={null}
gcloud auth list
```

Example output:

```text theme={null}
Credentialed Accounts

ACTIVE  ACCOUNT
*       kodekloud-test-sa@kodekloud-gcp-training.iam.gserviceaccount.com

To set the active account, run:
 $ gcloud config set account `ACCOUNT`
```

Revoke the service account credentials from your local gcloud auth store:

```bash theme={null}
gcloud auth revoke kodekloud-test-sa@kodekloud-gcp-training.iam.gserviceaccount.com
```

Warning: revoking a service account token only removes local credentials. Service account tokens cannot be force-revoked like user OAuth tokens; they will expire automatically. To immediately prevent key use, delete the specific service account key or disable/delete the parent service account.

<Callout icon="warning">
  Revoking local credentials does not expire the underlying service account key. If a key is compromised, delete the key (or disable/delete the service account) immediately.
</Callout>

To delete the key you created:

```bash theme={null}
gcloud iam service-accounts keys delete KEY_ID \
  --iam-account=kodekloud-test-sa@kodekloud-gcp-training.iam.gserviceaccount.com
```

Quick reference — common gcloud commands used here

| Action                                 | Command                                                                | Notes                                                                |
| -------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Activate service account with key file | `gcloud auth activate-service-account --key-file=KEY.json`             | Authenticates gcloud as the service account using the JSON key.      |
| Set active project                     | `gcloud config set project PROJECT_ID`                                 | Ensures commands target the desired GCP project.                     |
| List Cloud Storage buckets             | `gcloud storage ls`                                                    | Works only if the service account has storage list/view permissions. |
| List Compute Engine instances          | `gcloud compute instances list`                                        | Requires `compute.instances.list` permission.                        |
| List credentialed accounts             | `gcloud auth list`                                                     | Shows which account is active locally.                               |
| Revoke a local account                 | `gcloud auth revoke ACCOUNT`                                           | Removes local credentials from the gcloud auth store.                |
| Delete a service account key           | `gcloud iam service-accounts keys delete KEY_ID --iam-account=ACCOUNT` | Permanently removes the key so it can no longer be used.             |

Summary

* Use `gcloud auth activate-service-account --key-file=KEY.json` to authenticate locally with a service account key.
* Set the active project with `gcloud config set project PROJECT_ID`.
* Test allowed operations (e.g., `gcloud storage ls`) and confirm denied operations (e.g., `gcloud compute instances list`).
* Edit your custom role to add permissions if necessary, then re-run commands.
* Revoke local credentials and delete service account keys when finished to reduce risk.

Links and references

* gcloud CLI installation: [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
* IAM roles & permissions: [https://cloud.google.com/iam/docs/understanding-roles](https://cloud.google.com/iam/docs/understanding-roles)
* Service account keys best practices: [https://cloud.google.com/iam/docs/creating-managing-service-account-keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)

Thanks for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9dd8e9-0075-430e-92db-757c9a6b738a/lesson/2148c5c5-44c6-4df9-9755-1902c2a5e02a" />
</CardGroup>
