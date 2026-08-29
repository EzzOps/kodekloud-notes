# .github/workflows/awesome-app.yml
name: My Awesome App
on: push

jobs:
  unit-testing:
    # ... unit test definitions ...
  code-coverage:
    # ... code coverage definitions ...
  build:
    # ... build definitions ...
  dev-deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Step 1
        # ...
      - name: Step 2
        # ...
      - name: Step 3
        # ...
      - name: Step 4
        # ...
      - name: Step 5
        # ...
```

To DRY-up your CI/CD, move the `dev-deploy` job into its own reusable workflow file:

```yaml theme={null}
# .github/workflows/reusable-dev-deploy.yml
name: Reusable Dev-Deploy Workflow
on:
  workflow_call:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Step 1
        # ...
      - name: Step 2
        # ...
      - name: Step 3
        # ...
      - name: Step 4
        # ...
      - name: Step 5
        # ...
```

<Callout icon="lightbulb">
  The `on: workflow_call` trigger makes this workflow callable from other workflows. You can also define `inputs`, `outputs`, and `secrets` under `workflow_call` for advanced parameterization.
</Callout>

***

## 2. Calling a Reusable Workflow

Back in `awesome-app.yml`, replace the inline `dev-deploy` job with a reference to the reusable workflow:

```yaml theme={null}
# .github/workflows/awesome-app.yml
name: My Awesome App
on: push

jobs:
  unit-testing:
    # ...
  code-coverage:
    # ...
  build:
    # ...
  dev-deploy:
    needs: build
    uses: ./.github/workflows/reusable-dev-deploy.yml
```

If the reusable workflow lives in another repository, reference it by `{owner}/{repo}/{path}@ref`:

```yaml theme={null}
jobs:
  dev-deploy:
    needs: build
    uses: my-org/common-workflows/.github/workflows/reusable-dev-deploy.yml@main
```

<Callout icon="triangle-alert">
  When calling workflows in private repositories, ensure the caller has appropriate permissions and that any required `secrets:` are declared in the called workflow’s `workflow_call` section.
</Callout>

***

## 3. Inputs, Outputs, and Secrets

To make your reusable workflows more flexible:

* **Inputs** allow callers to pass parameters (e.g., environment name, version tag).
* **Outputs** let callers consume results (e.g., artifact URLs, deployment IDs).
* **Secrets** ensure sensitive data—like cloud credentials—are never exposed.

Example of declaring inputs and secrets in a reusable workflow:

```yaml theme={null}
# .github/workflows/reusable-dev-deploy.yml
on:
  workflow_call:
    inputs:
      env-name:
        description: 'Deployment environment'
        required: true
        type: string
    secrets:
      API_TOKEN:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ${{ inputs.env-name }}
        env:
          TOKEN: ${{ secrets.API_TOKEN }}
        # ...
```

***

## Benefits of Modular CI/CD with Reusable Workflows

* **Consistency:** Enforce the same deployment steps across all services.
* **Maintainability:** Update a single workflow file to propagate changes everywhere.
* **Scalability:** Easily onboard new projects by referencing prebuilt workflows.
* **Security:** Centralize and manage secrets in one place.

***

## Links and References

* [GitHub Actions: Reusing workflows](https://docs.github.com/actions/using-workflows/reusing-workflows)
* [GitHub Actions: Workflow syntax for GitHub Actions](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
* [GitHub Actions: Workflow commands](https://docs.github.com/actions/using-workflows/workflow-commands-for-github-actions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/57481ffd-2f40-4d62-af84-5f992f6c92dc/lesson/6c328588-e2d3-465c-a245-ac854f3e5393" />
</CardGroup>


# Uploading Reports to AWS S3 Storage

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Reusable-Workflows-and-Reporting/Uploading-Reports-to-AWS-S3-Storage/page

Automate publishing test and coverage reports to Amazon S3 using the jakejarvis/s3-sync-action in your GitHub Actions workflow.

Automate publishing your test and coverage reports to an Amazon S3 bucket by swapping out a manual upload step with the prebuilt **jakejarvis/s3-sync-action** in your GitHub Actions workflow.

## 1. Current Workflow: Placeholder Upload

Your existing `reports-s3` job runs after `unit-testing` and `code-coverage`, downloads artifacts, merges them, and uses a placeholder `echo` command:

```yaml theme={null}
jobs:
  reports-s3:
    needs: [unit-testing, code-coverage]
    name: AWS S3 - Upload Reports
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - name: Download Mocha Test Artifact
        uses: actions/download-artifact@v3
        with:
          name: Mocha-Test-Result

      - name: Download Code Coverage Artifact
        uses: actions/download-artifact@v3
        with:
          name: Code-Coverage-Result

      - name: Merge Test Files
        run: |
          ls -ltr
          mkdir reports-${{ github.sha }}
          mv cobertura-coverage.xml reports-${{ github.sha }}/
          mv test-results.xml reports-${{ github.sha }}/
          ls -ltr reports-${{ github.sha }}/

      - name: Upload to AWS S3
        run: echo "uploading..."
```

We’ll replace the final step with the S3 Sync action.

## 2. Selecting the S3 Sync Action

### 2.1 Search GitHub Marketplace

In your repository’s [GitHub Marketplace](https://github.com/marketplace), search for **S3** and choose **jakejarvis/s3-sync-action**:

<Frame>
  ![The image shows a GitHub Marketplace page listing various actions related to AWS S3, including tools for caching, removing, deploying, and syncing files. Each action is accompanied by a brief description, star rating, and creator information.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876738/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/github-marketplace-aws-s3-actions.jpg)
</Frame>

### 2.2 Action Inputs

Inspect the action’s README for the inputs:

```yaml theme={null}
uses: jakejarvis/s3-sync-action@master
with:
  args: --acl public-read --follow-symlinks --delete
env:
  AWS_S3_BUCKET: ${{ secrets.AWS_S3_BUCKET }}
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  AWS_REGION: 'us-west-1'      # defaults to us-east-1
  SOURCE_DIR: 'public'         # defaults to repository root
  DEST_DIR: ''                 # optional destination path
```

| Variable                 | Description                     | Default / Required     |
| ------------------------ | ------------------------------- | ---------------------- |
| AWS\_S3\_BUCKET          | Target S3 bucket name           | Required               |
| AWS\_ACCESS\_KEY\_ID     | AWS IAM access key ID           | Required               |
| AWS\_SECRET\_ACCESS\_KEY | AWS IAM secret access key       | Required               |
| AWS\_REGION              | AWS region where bucket resides | Optional (`us-east-1`) |
| SOURCE\_DIR              | Directory to sync               | Optional (`.`)         |
| DEST\_DIR                | Path in bucket for uploads      | Optional (root)        |

<Callout icon="triangle-alert">
  Using the `--delete` flag will remove files in the bucket that are not present in your source directory. Double-check your `SOURCE_DIR` before enabling deletion.
</Callout>

## 3. Updated Workflow: S3 Sync Step

Replace the placeholder with the S3 Sync action. Here’s the complete `reports-s3` job:

```yaml theme={null}
jobs:
  reports-s3:
    needs: [unit-testing, code-coverage]
    name: AWS S3 - Upload Reports
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - name: Download Mocha Test Artifact
        uses: actions/download-artifact@v3
        with:
          name: Mocha-Test-Result

      - name: Download Code Coverage Artifact
        uses: actions/download-artifact@v3
        with:
          name: Code-Coverage-Result

      - name: Merge Test Files
        run: |
          ls -ltr
          mkdir reports-${{ github.sha }}
          mv cobertura-coverage.xml reports-${{ github.sha }}/
          mv test-results.xml reports-${{ github.sha }}/
          ls -ltr reports-${{ github.sha }}/

      - name: Upload to AWS S3
        uses: jakejarvis/s3-sync-action@master
        with:
          args: --follow-symlinks --delete
        env:
          AWS_S3_BUCKET: solar-system-reports-bucket
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: 'us-east-1'
          SOURCE_DIR: 'reports-${{ github.sha }}'
          DEST_DIR: 'reports-${{ github.sha }}'
```

## 4. Setting Up AWS S3

### 4.1 Creating the Bucket

In the [AWS S3 console](https://console.aws.amazon.com/s3/home), create a bucket named `solar-system-reports-bucket` (or your preferred name) in the desired region:

<Frame>
  ![The image shows an Amazon S3 console with a bucket named "solar-system-reports-bucket" in the US East (N. Virginia) region, indicating that objects can be public.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876740/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/amazon-s3-console-solar-system-bucket.jpg)
</Frame>

## 5. Storing AWS Credentials as GitHub Secrets

Add your AWS keys under **Settings > Secrets and variables > Actions**:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

<Callout icon="lightbulb">
  Storing credentials in **GitHub Secrets** ensures they remain encrypted and aren’t exposed in your workflow logs.
</Callout>

<Frame>
  ![The image shows a GitHub repository settings page, specifically the "Secrets and variables" section, listing environment and repository secrets like AWS keys and passwords.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876742/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/github-repo-settings-secrets-variables.jpg)
</Frame>

## 6. Running the Workflow

Commit and push your changes. The `reports-s3` job will queue after `unit-testing` and `code-coverage` complete:

<Frame>
  ![The image shows a GitHub Actions workflow interface for a project named "solar-system," displaying the status of various jobs like unit testing, code coverage, and AWS S3 uploads. The workflow is currently queued and includes steps for containerization and deployment.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876743/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/github-actions-solar-system-workflow.jpg)
</Frame>

### 6.1 Merge Step Log

```bash theme={null}
Run ls -ltr
total 24
-rw-r--r-- 1 runner docker 3347 Oct 22 07:44 test-results.xml
-rw-r--r-- 1 runner docker 597 Oct 22 07:44 cobertura-coverage.xml
...
```

### 6.2 S3 Sync Step Log

```bash theme={null}
Run jakejarvis/s3-sync-action@master
/usr/bin/docker run --name e8d... \
  --workdir /github/workspace --rm ... \
  --follow-symlinks --delete
upload: reports-1374785c0a9719be70ed2e7ba3481dabd72429c6/test-results.xml to s3://solar-system-reports-bucket/reports-1374785c0a9719be70ed2e7ba3481dabd72429c6/test-results.xml
```

Once complete, the AWS S3 upload step shows success:

<Frame>
  ![The image shows a GitHub Actions workflow interface with a job titled "AWS S3 - Upload Reports" that has successfully completed. The sidebar lists various jobs, including unit testing and deployment tasks.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876744/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/github-actions-aws-s3-upload-reports.jpg)
</Frame>

## 7. Why the Extra “build” Step?

Because **jakejarvis/s3-sync-action** is a Docker-based custom action, GitHub builds the container at runtime. You’ll see this as an extra “build” step in the logs:

<Frame>
  ![The image shows a GitHub page for a GitHub Action called "S3 Sync," which is used to sync a directory with an AWS S3 bucket. It includes usage instructions and links for further information.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876745/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/github-action-s3-sync-instructions.jpg)
</Frame>

## 8. Verifying in S3

### 8.1 Inspect the Commit-SHA Folder

After syncing, refresh your bucket to see a folder named after the commit SHA:

<Frame>
  ![The image shows an Amazon S3 console with a bucket named "solar-system-reports-bucket" containing one folder named "reports-13f4785c0a9719be70ed2e7b34db4db7242c96".](../../../../images/kodekloud.com/kk-media/image/upload/v1752876746/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/amazon-s3-solar-system-reports-bucket.jpg)
</Frame>

### 8.2 Check Uploaded Files

Open the folder to confirm your XML reports are present:

<Frame>
  ![The image shows an Amazon S3 console with a bucket named "solar-system-reports-bucket" containing two XML files: "cobertura-coverage.xml" and "test-results.xml," both last modified on October 22, 2023.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876747/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/amazon-s3-solar-system-bucket-xml-files.jpg)
</Frame>

## 9. Next Steps & Alternatives

You can apply the same pattern to other cloud storage solutions like [Azure Blob Storage](https://learn.microsoft.com/azure/storage/blobs/storage-blobs-introduction). Always store credentials securely as GitHub Secrets:

<Frame>
  ![The image shows a GitHub repository settings page, specifically the "Secrets and variables" section under "Actions," displaying environment and repository secrets like AWS keys and passwords.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876748/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/github-repo-settings-secrets-variables-2.jpg)
</Frame>

Before building your own plugin, explore the [GitHub Marketplace](https://github.com/marketplace)—you may find a prebuilt action that meets your requirements:

<Frame>
  ![The image shows the GitHub Marketplace page filtered for "Actions," displaying various automation tools like "Setup Node.js environment" and "Setup Java JDK" with their descriptions and star ratings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876749/notes-assets/images/GitHub-Actions-Uploading-Reports-to-AWS-S3-Storage/github-marketplace-actions-automation-tools.jpg)
</Frame>

## Links and References

* [jakejarvis/s3-sync-action](https://github.com/jakejarvis/s3-sync-action)
* [GitHub Actions: Storing encrypted secrets](https://docs.github.com/actions/security-guides/encrypted-secrets)
* [AWS S3 Documentation](https://docs.aws.amazon.com/s3/index.html)
* [Azure Blob Storage Introduction](https://learn.microsoft.com/azure/storage/blobs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/57481ffd-2f40-4d62-af84-5f992f6c92dc/lesson/0fe80ffd-60a2-4991-86a5-1fc6ae7f8910" />
</CardGroup>
