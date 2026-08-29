# Raise a Merge Request amp Use rules at Job level

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Raise-a-Merge-Request-amp-Use-rules-at-Job-level/page

Learn to restrict GitLab CI/CD jobs to run only for merge request events using predefined variables and the rules keyword.

In this lesson, you’ll learn how to restrict a GitLab CI/CD job so that it only runs for merge request events. We will explore predefined pipeline variables and apply the `rules` keyword at the job level to include or exclude jobs based on `CI_PIPELINE_SOURCE`.

## 1. Define Jobs in `.gitlab-ci.yml`

First, declare two test jobs in your pipeline:

1. **generic\_predefined\_variables** – prints general CI/CD variables
2. **merge\_request\_predefined\_variables** – prints merge request–specific variables

```yaml theme={null}
