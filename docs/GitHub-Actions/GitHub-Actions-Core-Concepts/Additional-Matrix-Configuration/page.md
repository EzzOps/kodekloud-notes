# Additional Matrix Configuration

Source: https://notes.kodekloud.com/docs/GitHub-Actions/GitHub-Actions-Core-Concepts/Additional-Matrix-Configuration/page

This guide explores advanced configurations for GitHub Actions matrix strategy, including excluding combinations, including custom pairs, and controlling job behavior.

In this guide, we’ll dive deeper into GitHub Actions’ matrix strategy. You’ll learn how to:

* Exclude unsupported combinations
* Include custom combinations
* Control failure behavior (`fail-fast`)
* Limit parallel jobs (`max-parallel`)

By default, if any matrix job fails, GitHub Actions cancels all in-progress or queued jobs. Also, all combinations run in parallel unless you configure otherwise.

<Frame>
  ![The image shows a GitHub Actions workflow summary with multiple deployment jobs, where most have succeeded except for one failure in the "windows-latest, alpine" deployment.](https://kodekloud.com/kk-media/image/upload/v1752876615/notes-assets/images/GitHub-Actions-Additional-Matrix-Configuration/github-actions-workflow-deployment-summary.jpg)
</Frame>

## 1. Excluding Specific Combinations

To prevent certain OS–image pairs (like Alpine on Windows) from running, use the `exclude` keyword under `strategy.matrix`:

```yaml theme={null}
