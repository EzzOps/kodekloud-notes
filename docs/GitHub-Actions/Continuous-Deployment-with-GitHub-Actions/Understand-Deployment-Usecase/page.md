# OUTPUT:
# NAME           HOSTS                                           ADDRESS                       PORTS   AGE
# Extract only the host:
kubectl -n development get ingress \
  -o jsonpath='{.items[0].spec.tls[0].hosts[0]}'
# solar-system-development.172.232.87.200.nip.io
```

### 3. Expose the Step Output as a Job Output

Enable downstream jobs to consume the captured host by defining an `outputs` section:

```yaml theme={null}
jobs:
  dev-deploy:
    needs: docker
    runs-on: ubuntu-latest
    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host.outputs.APP_INGRESS_HOST }}
    steps:
      # ... (previous steps) ...
```

## Consuming the Output in Integration Testing

In the `integration-testing` job, map the job output to an environment variable:

```yaml theme={null}
jobs:
  integration-testing:
    name: Dev Integration Testing
    needs: dev-deploy
    runs-on: ubuntu-latest
    steps:
      - name: Test URL Output with curl and jq
        env:
          URL: ${{ needs.dev-deploy.outputs.APP_INGRESS_URL }}
        run: |
          echo "URL: $URL"
          echo "-----------------------------------------"
          curl https://$URL/live -s -k | jq -r .status | grep -i live
```

## Passing Values Between Jobs

<Frame>
  ![The image shows a GitHub Docs page about passing values between steps and jobs in a workflow, with navigation links and support options.](https://kodekloud.com/kk-media/image/upload/v1752876458/notes-assets/images/GitHub-Actions-Setting-Output-for-Integration-testing/github-docs-passing-values-workflow.jpg)
</Frame>

Learn more in the [GitHub Actions docs on passing values between jobs](https://docs.github.com/en/actions/using-workflows/passing-values-between-jobs).

### Official Example

```yaml theme={null}
jobs:
  job1:
    runs-on: ubuntu-latest
    outputs:
      output1: ${{ steps.step1.outputs.test }}
      output2: ${{ steps.step2.outputs.test }}
    steps:
      - id: step1
        run: echo "test=hello" >> "$GITHUB_OUTPUT"
      - id: step2
        run: echo "test=world" >> "$GITHUB_OUTPUT"

  job2:
    runs-on: ubuntu-latest
    needs: job1
    steps:
      - env:
          OUTPUT1: ${{ needs.job1.outputs.output1 }}
          OUTPUT2: ${{ needs.job1.outputs.output2 }}
        run: echo "$OUTPUT1 $OUTPUT2"
```

## Workflow Run Summary

<Frame>
  ![The image shows a GitHub Actions workflow summary for a project named "solar-system," indicating a successful run with various jobs like unit testing, code coverage, and containerization. The workflow was triggered by a push and completed in 2 minutes and 4 seconds.](https://kodekloud.com/kk-media/image/upload/v1752876459/notes-assets/images/GitHub-Actions-Setting-Output-for-Integration-testing/github-actions-solar-system-workflow-summary.jpg)
</Frame>

## Integration Testing Job Log

<Frame>
  ![The image shows a GitHub Actions workflow interface with a successful "Dev Integration Testing" job, displaying job setup and test output details.](https://kodekloud.com/kk-media/image/upload/v1752876461/notes-assets/images/GitHub-Actions-Setting-Output-for-Integration-testing/github-actions-dev-integration-testing.jpg)
</Frame>

This confirms that the dynamic Ingress host URL was successfully passed from the deploy job to the integration-testing job.

## References

* [GitHub Actions: Passing values between jobs](https://docs.github.com/en/actions/using-workflows/passing-values-between-jobs)
* [Kubernetes Ingress Documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/)
* [Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/92928734-1d5a-462d-9414-2d3865f5ef79/lesson/2513913d-b724-4b82-a580-1077f0c69453" />
</CardGroup>


# Understand Deployment Usecase

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Deployment-with-GitHub-Actions/Understand-Deployment-Usecase/page

This guide explains deploying a Dockerized application to Kubernetes clusters using a CI/CD pipeline.

In this guide, we’ll walk through our CI/CD pipeline stages and demonstrate how to deploy a Dockerized application to Kubernetes clusters. You’ll learn how to:

* Build and test your code
* Containerize with Docker
* Deploy to a development cluster
* Run integration tests
* Promote to production after manual approval

## Deployment Pipeline Overview

We’ve already completed:

| Stage                   | Purpose                                        |
| ----------------------- | ---------------------------------------------- |
| Unit Testing            | Validate code logic with `npm test`            |
| Code Coverage           | Measure test coverage using `npm run coverage` |
| Docker Containerization | Package the app into a Docker image            |

Next, the pipeline will:

1. Push the Docker image to a container registry
2. Deploy to a Kubernetes *development* environment
3. Execute integration tests against the dev cluster
4. Await manual approval
5. Promote the same deployment to the *production* environment

## Local Development Commands

Before diving into Kubernetes, run these commands locally to verify your application:

| Step        | Command                                 | Description                       |
| ----------- | --------------------------------------- | --------------------------------- |
| Install     | `npm install`                           | Install project dependencies      |
| Test        | `npm test`                              | Execute unit tests                |
| Coverage    | `npm run coverage`                      | Generate code coverage report     |
| Build Image | `docker build -t my-app:latest .`       | Create a Docker image             |
| Run Image   | `docker run -p 3000:3000 my-app:latest` | Launch the container on port 3000 |
| Push Image  | `docker push my-app:latest`             | Upload the image to your registry |

```bash theme={null}
