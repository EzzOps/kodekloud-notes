# Workflow Docker Push

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/Workflow-Docker-Push/page

This lesson extends GitHub Actions CI workflow to publish a Docker image to Docker Hub, including building, testing, and pushing the image.

In this lesson, you’ll extend your GitHub Actions CI workflow to publish a Docker image to [Docker Hub](https://hub.docker.com/). We’ll build the image for testing, verify it runs correctly, and then push it to your Docker Hub registry—all within a single workflow file.

<Callout icon="lightbulb">
  Ensure you’ve configured the following GitHub repository secrets:

  * `DOCKERHUB_USERNAME`
  * `DOCKERHUB_TOKEN`
  * `MONGO_URI`, `MONGO_USERNAME`, `MONGO_PASSWORD`
</Callout>

## Updated Workflow Snippet

Add these three steps to your `.github/workflows/ci.yml`:

```yaml theme={null}
