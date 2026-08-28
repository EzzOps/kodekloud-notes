# Step 4 Using Outputs in Reusable Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Reusable-Workflows-and-Reporting/Step-4-Using-Outputs-in-Reusable-Workflow/page

This article explains how to expose and use outputs from a reusable GitHub Actions workflow for downstream jobs.

In this lesson, we’ll walk through exposing outputs from a reusable workflow so downstream jobs—in this case, **dev-integration-testing**—can access the application URL generated during deployment.

## Troubleshooting the Integration Test Failure

When **dev-integration-testing** runs without the exposed URL, you might see:

```bash theme={null}
echo $URL
