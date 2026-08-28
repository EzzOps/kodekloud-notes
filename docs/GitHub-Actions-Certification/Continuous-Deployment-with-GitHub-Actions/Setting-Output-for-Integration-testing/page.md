# NAME           READY   UP-TO-DATE   AVAILABLE   AGE
kubectl -n development get pods
# NAME                                        READY   STATUS    RESTARTS   AGE
# solar-system-6db5d5dfb8c-96qcz             1/1     Running   0          26m
# solar-system-6db5d5dfb8c-psbxx             1/1     Running   0          26m
```

Currently, the `solar-system` deployment uses two replicas (from the repository variable). We want to switch this to the environment variable value (`1` replica) by invoking the `development` environment in our workflow.

## Update the Workflow

To enforce environment protections and show the deployment URL in the workflow summary, add an `environment` block under the `dev-deploy` job:

```yaml theme={null}
env:
  MONGO_URI: mongodb+srv://supercluster.d83ji.mongodb.net/superData
  MONGO_USERNAME: ${{ vars.MONGO_USERNAME }}
  MONGO_PASSWORD: ${{ secrets.MONGO_PASSWORD }}

jobs:
  unit-testing:
    # ...

  code-coverage:
    # ...

  docker:
    # ...

  dev-deploy:
    needs: docker
    environment:
      name: development
      url: https://${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install kubectl CLI
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.26.0'

      - name: Set kubeconfig context
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig

      # ... additional deployment steps ...
```

Commit and push these changes to trigger a new workflow run.

<Callout icon="triangle-alert">
  After this change, the `dev-deploy` job will pend if the environment has protection rules (e.g., a wait timer or approval). Administrators must review and approve to proceed.
</Callout>

## Approving the Pending Deployment

Once the workflow hits the `dev-deploy` job, you’ll see it pending due to environment protection:

<Frame>
  ![The image shows a GitHub Actions workflow interface with a series of jobs including unit testing, code coverage, and containerization. The workflow is in progress, triggered by a recent push to a repository.](https://kodekloud.com/kk-media/image/upload/v1752875907/notes-assets/images/GitHub-Actions-Certification-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-actions-workflow-jobs-progress.jpg)
</Frame>

Click the pending job to reveal the protection rule and remaining wait time. Administrators can bypass the wait by adding a comment:

<Frame>
  ![The image shows a GitHub Actions interface with a confirmation dialog for deploying to a development environment, requiring administrator privileges and a comment for manual override.](https://kodekloud.com/kk-media/image/upload/v1752875908/notes-assets/images/GitHub-Actions-Certification-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-actions-deploy-confirmation-dialog.jpg)
</Frame>

After approval, the `dev-deploy` job runs. Upon success, the deployment URL appears in the workflow summary:

<Frame>
  ![The image shows a GitHub Actions workflow summary for a project, displaying successful completion of various jobs like unit testing, containerization, and deployment.](https://kodekloud.com/kk-media/image/upload/v1752875909/notes-assets/images/GitHub-Actions-Certification-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-actions-workflow-summary-success.jpg)
</Frame>

By clicking this URL, stakeholders can quickly verify the live application.

## View Deployments Across Environments

GitHub’s public beta for deployment tracking offers a centralized overview of deployments across all environments. Access it via **Actions > Deployments** in your repository:

<Frame>
  ![The image shows a GitHub Actions page displaying a list of workflow runs for a project called "Solar System Workflow." Each entry includes details like commit messages, status, and timestamps.](https://kodekloud.com/kk-media/image/upload/v1752875910/notes-assets/images/GitHub-Actions-Certification-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-actions-solar-system-workflow.jpg)
</Frame>

This dashboard displays each deployment event along with environment name, branch, commit, and duration. Learn more on the [GitHub blog announcement][gh-deploy-tracking].

<Frame>
  ![The image shows a GitHub blog post announcing the public beta of a new feature for tracking deployments across environments, with a list of capabilities for developers and DevOps managers. There is also a screenshot of a dashboard displaying deployment information.](https://kodekloud.com/kk-media/image/upload/v1752875910/notes-assets/images/GitHub-Actions-Certification-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-blog-post-deployment-tracking-beta.jpg)
</Frame>

***

With environments configured in your GitHub Actions workflow, you can enforce rules, manage scoped secrets and variables, and prominently display deployment URLs for fast verification.

## Links and References

* [GitHub Environments](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment)
* [Azure/setup-kubectl Action](https://github.com/Azure/setup-kubectl)
* [GitHub Actions Deployment Tracking][gh-deploy-tracking]

[gh-deploy-tracking]: https://github.blog/2023-07-26-github-actions-deployment-tracking/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/b6687abe-8094-4750-910b-5daa8bc710b1/lesson/8e8d11a8-60fc-42ac-bc13-5d364c24507c" />
</CardGroup>


# Setting Output for Integration testing

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Deployment-with-GitHub-Actions/Setting-Output-for-Integration-testing/page

This guide explains how to fetch and use Kubernetes Ingress host URLs in GitHub Actions for integration testing.

This guide shows you how to dynamically fetch your Kubernetes Ingress host, expose it as a job output in a `dev-deploy` job, and consume that output in an `integration-testing` job to verify your `/live` endpoint. By the end, you’ll have a seamless flow where the Ingress URL travels between jobs in the same workflow.

## Overview

* Capture the Ingress host URL after deployment
* Export it as a job output
* Use the output in a downstream integration test

## 1. Deploying to Dev and Capturing the Ingress URL

In the `dev-deploy` job, we apply Kubernetes manifests and query the Ingress host name. We then write it to `$GITHUB_OUTPUT` so it becomes available to other jobs.

```yaml theme={null}
jobs:
  dev-deploy:
    needs: docker
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Install kubectl CLI
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.26.0'

      - name: Configure kubeconfig
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBECONFIG }}

      - name: Deploy to Dev Environment
        run: kubectl apply -f kubernetes/development

      - name: Set App Ingress Host URL
        id: set-ingress-host-address
        run: |
          HOST=$(kubectl -n ${{ vars.NAMESPACE }} \
            get ingress -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')
          echo "APP_INGRESS_URL=$HOST" >> "$GITHUB_OUTPUT"

    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_URL }}
```

<Callout icon="lightbulb">
  Ensure your Kubernetes context and namespace (`${{ vars.NAMESPACE }}`) are correctly configured before running `kubectl`.
</Callout>

## 2. Defining the Integration Testing Job

After `dev-deploy` completes, `integration-testing` retrieves the `APP_INGRESS_URL` output and calls the `/live` endpoint using `curl` and `jq`.

```yaml theme={null}
  integration-testing:
    name: Dev Integration Testing
    needs: dev-deploy
    runs-on: ubuntu-latest
    steps:
      - name: Test `/live` Endpoint
        env:
          URL: ${{ needs.dev-deploy.outputs.APP_INGRESS_URL }}
        run: |
          echo "Testing endpoint: https://$URL/live"
          curl https://$URL/live -s -k | jq -r .status | grep -iq live
```

<Callout icon="lightbulb">
  The Ubuntu runner includes both `curl` and `jq` by default. If you use a custom runner, install these tools before running the test.
</Callout>

## 3. Passing Values Between Jobs

GitHub Actions lets you map step outputs to job outputs and then reference them in downstream jobs via the `needs` context.

| Level       | Syntax                                  | Example                                                  |
| ----------- | --------------------------------------- | -------------------------------------------------------- |
| Step output | `steps.<step_id>.outputs.<output_name>` | `steps.set-ingress-host-address.outputs.APP_INGRESS_URL` |
| Job output  | `needs.<job_id>.outputs.<output_name>`  | `needs.dev-deploy.outputs.APP_INGRESS_URL`               |

<Frame>
  ![The image shows a GitHub Docs page about passing values between steps and jobs in a workflow, with information on using environment variables and job outputs.](https://kodekloud.com/kk-media/image/upload/v1752875912/notes-assets/images/GitHub-Actions-Certification-Setting-Output-for-Integration-testing/github-docs-passing-values-workflow.jpg)
</Frame>

For more details, see the [GitHub Actions contexts documentation](https://docs.github.com/actions/learn-github-actions/contexts#needs-context).

## 4. Complete Workflow Example

Here’s how the full `.github/workflows/solar-system.yml` might look with both jobs defined:

```yaml theme={null}
name: Deploy and Test

on:
  push:
    branches: [ main ]

jobs:
  dev-deploy:
    needs: docker
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Install kubectl CLI
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.26.0'

      - name: Configure kubeconfig
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBECONFIG }}

      - name: Deploy to Dev Environment
        run: kubectl apply -f kubernetes/development

      - name: Set App Ingress Host URL
        id: set-ingress-host-address
        run: |
          HOST=$(kubectl -n ${{ vars.NAMESPACE }} \
            get ingress -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')
          echo "APP_INGRESS_URL=$HOST" >> "$GITHUB_OUTPUT"

    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_URL }}

  integration-testing:
    name: Dev Integration Testing
    needs: dev-deploy
    runs-on: ubuntu-latest
    steps:
      - name: Test `/live` Endpoint
        env:
          URL: ${{ needs.dev-deploy.outputs.APP_INGRESS_URL }}
        run: |
          echo "Testing endpoint: https://$URL/live"
          curl https://$URL/live -s -k | jq -r .status | grep -iq live
```

<Frame>
  ![The image shows a GitHub Actions workflow summary for a project, indicating successful completion of various jobs such as unit testing, code coverage, and deployment. The workflow is named "solar-system.yml" and includes steps like containerization and integration testing.](https://kodekloud.com/kk-media/image/upload/v1752875913/notes-assets/images/GitHub-Actions-Certification-Setting-Output-for-Integration-testing/github-actions-workflow-summary-solar-system.jpg)
</Frame>

## References

* [GitHub Actions Contexts: needs](https://docs.github.com/actions/learn-github-actions/contexts#needs-context)
* [GitHub Actions: workflow syntax for GitHub Actions](https://docs.github.com/actions/reference/workflow-syntax-for-github-actions)
* [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/b6687abe-8094-4750-910b-5daa8bc710b1/lesson/2022a468-e925-43e2-be48-90eb5e6ffff2" />
</CardGroup>
