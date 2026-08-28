# Step 1 Configure new Reusable Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Reusable-Workflows-and-Reporting/Step-1-Configure-new-Reusable-Workflow/page

This article explains how to configure and use reusable workflows in GitHub Actions to avoid duplication in CI/CD processes.

GitHub Actions lets you **reuse common CI/CD logic** across multiple workflows and repositories. Instead of duplicating identical deployment steps in both `dev-deploy` and `prod-deploy`, extract them into a single reusable workflow.

## Why Avoid Duplication?

A typical “Solar System Workflow” might look like this:

```yaml theme={null}
