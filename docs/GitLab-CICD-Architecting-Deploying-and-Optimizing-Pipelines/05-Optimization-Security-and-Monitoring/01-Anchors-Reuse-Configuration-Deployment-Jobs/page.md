# Anchors Reuse Configuration Deployment Jobs

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Anchors-Reuse-Configuration-Deployment-Jobs/page

Learn to use YAML anchors in GitLab CI/CD for reusable deployment job templates, reducing redundancy and simplifying pipeline maintenance.

In this tutorial, you’ll learn how to leverage YAML anchors in GitLab CI/CD to DRY (Don’t Repeat Yourself) up your pipeline, creating reusable templates for deployment jobs. By defining anchors once and merging them across multiple jobs, you avoid boilerplate and simplify maintenance.

## What Are YAML Anchors?

YAML anchors let you define a named block of configuration that can be duplicated or inherited later. In GitLab CI/CD, you typically combine anchors with **hidden jobs** (names starting with a dot) to build templates.

<Callout icon="lightbulb">
  Hidden jobs are not executed directly. They serve as templates when you use the `<<:` merge key to inherit their configuration.
</Callout>

### Basic Anchor Example

```yaml theme={null}
