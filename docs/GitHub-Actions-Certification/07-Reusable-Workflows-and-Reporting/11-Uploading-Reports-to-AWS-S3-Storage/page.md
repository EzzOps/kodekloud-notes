# Uploading Reports to AWS S3 Storage

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Reusable-Workflows-and-Reporting/Uploading-Reports-to-AWS-S3-Storage/page

This guide automates uploading Mocha test results and code coverage reports to Amazon S3 using GitHub Actions and the `jakejarvis/s3-sync-action`.

In this guide, we’ll automate the upload of Mocha test results and code coverage reports to an Amazon S3 bucket using GitHub Actions. Instead of scripting AWS CLI commands manually, we’ll use the popular `jakejarvis/s3-sync-action` from the GitHub Marketplace.

## Prerequisites

* An existing S3 bucket (e.g., `solar-system-reports-bucket` in **us-east-1**).
* AWS credentials stored as **GitHub repository secrets**.
* A workflow that uploads test artifacts via `actions/upload-artifact`.

## 1. Initial Workflow Stub

Here’s our starting point. The `reports-s3` job currently downloads artifacts, merges them into a folder, then echoes a placeholder message:

```yaml theme={null}
reports-s3:
  needs: [code-coverage, unit-testing]
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
      run: echo "uploading......."
```

### Choosing a Marketplace Action

The GitHub Marketplace offers many AWS S3 actions for syncing, uploading, or deploying:

<Frame>
  ![The image shows a GitHub Marketplace page listing various actions related to AWS S3, including options for caching, deploying, syncing, and uploading files. Each action is accompanied by a brief description and star ratings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876356/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/github-marketplace-aws-s3-actions.jpg)
</Frame>

One of the most widely used is `jakejarvis/s3-sync-action`.

## 2. Sample Usage of `jakejarvis/s3-sync-action`

```yaml theme={null}
- name: Sync to S3
  uses: jakejarvis/s3-sync-action@master
  with:
    args: --acl public-read --follow-symlinks --delete
  env:
    AWS_S3_BUCKET: ${{ secrets.AWS_S3_BUCKET }}
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    AWS_REGION: 'us-west-1'   # Optional: defaults to us-east-1
    SOURCE_DIR: 'public'      # Optional: defaults to entire repo
```

### Environment Variables Reference

| Variable                 | Description                             | Default        |
| ------------------------ | --------------------------------------- | -------------- |
| AWS\_S3\_BUCKET          | Name of your S3 bucket                  | *none*         |
| AWS\_ACCESS\_KEY\_ID     | AWS access key stored in GitHub secrets | *none*         |
| AWS\_SECRET\_ACCESS\_KEY | AWS secret key stored in GitHub secrets | *none*         |
| AWS\_REGION              | AWS region for your bucket              | us-east-1      |
| SOURCE\_DIR              | Directory to sync                       | entire repo    |
| DEST\_DIR                | Destination path within the bucket      | root of bucket |

<Callout icon="lightbulb">
  Store your AWS credentials securely under **Settings → Secrets and variables** in your GitHub repository.
</Callout>

## 3. Integrate the Sync Action into `reports-s3`

Replace the placeholder step with the `s3-sync-action`. The final job looks like this:

```yaml theme={null}
jobs:
  reports-s3:
    needs: [code-coverage, unit-testing]
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
          AWS_REGION: us-east-1
          SOURCE_DIR: reports-${{ github.sha }}
          DEST_DIR: reports-${{ github.sha }}
```

## 4. Verify Your S3 Bucket and Secrets

Your bucket, `solar-system-reports-bucket`, is in US East (N. Virginia):

<Frame>
  ![The image shows an Amazon S3 console with a bucket named "solar-system-reports-bucket" in the US East (N. Virginia) region. The bucket's access is set to allow objects to be public, and it was created on October 22, 2023.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876358/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/amazon-s3-solar-system-bucket-console.jpg)
</Frame>

AWS credentials should appear in **Secrets and variables**:

<Frame>
  ![The image shows a GitHub repository settings page, specifically the "Secrets and variables" section for GitHub Actions, displaying environment and repository secrets.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876359/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/github-repo-settings-secrets-variables.jpg)
</Frame>

At first, the bucket will be empty:

<Frame>
  ![The image shows an Amazon S3 console interface displaying the "solar-system-reports-bucket" with options to manage objects, properties, permissions, and more. The objects section is currently loading, and various actions like copy, download, and delete are available.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876361/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/amazon-s3-console-solar-system-reports.jpg)
</Frame>

## 5. Trigger the Workflow

Commit and push your changes. After `unit-testing` and `code-coverage` finish, you’ll see the `reports-s3` job queued:

<Frame>
  ![The image shows a GitHub Actions workflow interface for a project named "solar-system," displaying a series of jobs including unit testing, code coverage, and AWS S3 upload reports. The workflow is triggered by a push and is currently queued.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876363/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/github-actions-solar-system-workflow.jpg)
</Frame>

You may notice an extra **build** step as it prepares the sync container:

<Frame>
  ![The image shows a GitHub page for the "S3 Sync" GitHub Action, which is used to sync a directory with an S3 bucket using the AWS CLI. It includes usage instructions and links to related resources.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876365/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/github-action-s3-sync-usage-instructions.jpg)
</Frame>

After the container is ready, the sync runs and uploads your reports:

<Frame>
  ![The image shows a GitHub Actions workflow interface with various jobs listed, including unit testing, code coverage, and AWS S3 upload reports, all marked as completed.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876366/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/github-actions-workflow-jobs-completed.jpg)
</Frame>

## 6. Confirm the Upload

Refresh the S3 console to see your XML report files:

<Frame>
  ![The image shows an Amazon S3 console with a bucket named "solar-system-reports-bucket" containing two XML files: "cobertura-coverage.xml" and "test-results.xml," both last modified on October 22, 2023.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876367/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/amazon-s3-solar-system-bucket-xmls.jpg)
</Frame>

## Next Steps

<Callout icon="lightbulb">
  Browse the [GitHub Marketplace](https://github.com/marketplace?type=actions) for actions to integrate with other cloud providers and CI/CD tools.
</Callout>

<Frame>
  ![The image shows a GitHub repository settings page, specifically the "Secrets and variables" section, where environment and repository secrets like AWS keys and passwords are managed.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876369/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/github-repo-settings-secrets-variables-2.jpg)
</Frame>

<Frame>
  ![The image shows the GitHub Marketplace page filtered to display "Actions," listing various automation tools for development workflows, such as setting up Node.js and Java JDK environments.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876371/notes-assets/images/GitHub-Actions-Certification-Uploading-Reports-to-AWS-S3-Storage/github-marketplace-actions-automation-tools.jpg)
</Frame>

That’s it! You’ve automated the upload of your test and coverage artifacts to AWS S3.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/da8706ee-24ab-41a1-916d-da8232ca028e/lesson/c76053fb-7d61-48ba-bda8-10dd427741a5" />
</CardGroup>
