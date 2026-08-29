# 1. Create an App Service plan (Linux, B1 SKU)
az appservice plan create \
  --resource-group MY_RESOURCE_GROUP \
  --name MY_PLAN_NAME \
  --is-linux \
  --sku B1

# 2. Create a Web App with Node.js runtime
az webapp create \
  --resource-group MY_RESOURCE_GROUP \
  --plan MY_PLAN_NAME \
  --name MY_WEBAPP_NAME \
  --runtime "NODE|14-lts"

# 3. Retrieve publish profile XML (for GitHub Secrets)
az webapp deployment list-publishing-profiles \
  --name MY_WEBAPP_NAME \
  --resource-group MY_RESOURCE_GROUP \
  --xml
```

> **lightbulb** Store the XML output as a GitHub Secret named `AZURE_WEBAPP_PUBLISH_PROFILE` for seamless deployment.

***

## Quick CI/CD Workflow Overview

Your GitHub Actions workflow typically defines two jobs:

| Job    | Purpose                                         | Key Actions                                  |
| ------ | ----------------------------------------------- | -------------------------------------------- |
| build  | Prepare application artifact                    | Checkout → Setup Node.js → Test → Zip        |
| deploy | Publish the build artifact to Azure App Service | Download → Unzip → `azure/webapps-deploy@v2` |

Here’s a minimal example (`.github/workflows/azure-nodejs.yml`):

```yaml theme={null}
name: Build and Deploy to Azure Web App

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with: { node-version: '20.x' }
      - name: Install & Test
        run: |
          npm install
          npm run build --if-present
          npm run test --if-present
      - name: Package App
        run: zip release.zip . -r
      - uses: actions/upload-artifact@v3
        with: { name: node-app, path: release.zip }

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: production
      url: ${{ steps.deploy.outputs.webapp-url }}
    steps:
      - uses: actions/download-artifact@v3
        with: { name: node-app }
      - name: Unzip Artifact
        run: unzip release.zip
      - id: deploy
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: .
```

***

## Step 1: Create App Service in Azure Portal

1. Navigate to **App Services** → **Create**.
2. Select your Subscription and Resource Group.
3. Configure instance details (Runtime: Node.js, OS: Linux).

![The image shows a configuration screen for setting up an Azure App Service, including options for subscription, resource group, instance details, runtime stack, operating system, and region.](https://kodekloud.com/kk-media/image/upload/v1752875884/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/azure-app-service-configuration-screen.jpg)

4. Choose a pricing plan (e.g., Basic B1).

![The image shows a table listing various computing options with details such as ACU/vCPU, vCPU, memory, remote storage, and scale. A "Basic B1" option is selected, highlighting its specifications.](https://kodekloud.com/kk-media/image/upload/v1752875885/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/computing-options-table-basic-b1.jpg)

5. Under **Deployment**, enable **GitHub Actions** and authenticate.

***

## Step 2: Authorize GitHub Access

When prompted, grant Azure permission to your GitHub account and repository:

![The image shows a Microsoft Azure portal screen for creating a web app, with a pop-up window for authorizing Azure App Service to access a GitHub account. The pop-up includes options to authorize access to repositories and update GitHub Action workflow files.](https://kodekloud.com/kk-media/image/upload/v1752875887/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/azure-portal-web-app-github-access.jpg)

* Select Organization
* Choose Repository (e.g., **GA Cloud Deploy Demo**)
* Pick Branch (**main**)
* Preview & Confirm

***

## Step 3: Secure GitHub Environment

1. In GitHub, go to **Settings** → **Environments**.
2. Create an environment named `production`.
3. (Optional) Add protection rules or required reviewers.

![The image shows a GitHub repository settings page, specifically the "Environments" section for configuring production deployment protection rules. It includes options for required reviewers, wait timers, and custom rules with GitHub Apps.](https://kodekloud.com/kk-media/image/upload/v1752875888/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/github-repo-settings-environments-deployment.jpg)

***

## Step 4: Automatic Workflow Commit

Azure provisions the resources and commits a workflow file to `.github/workflows/`:

![The image shows a Microsoft Azure portal page indicating that a web app deployment is complete, with details about the resources and their status.](https://kodekloud.com/kk-media/image/upload/v1752875890/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/azure-portal-web-app-deployment-complete.jpg)

***

## Step 5: Inspect GitHub Changes

* **Secrets**: A new `AZURE_WEBAPP_PUBLISH_PROFILE` appears under **Settings** → **Secrets**.
* **Workflow**: `.github/workflows/main_<webapp>.yaml` is added.
* **Actions**: View your first run.

![The image shows a GitHub Actions workflow summary for building and deploying a Node.js app to Azure Web App. The workflow was successful, with separate build and deploy steps, and includes warnings about deprecated Node.js actions.](https://kodekloud.com/kk-media/image/upload/v1752875891/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/github-actions-nodejs-azure-deploy.jpg)

***

## Step 6: View Your Live App

GitHub Actions outputs the application URL after deployment. Click the link to verify your app:

![The image shows a digital representation of the solar system with planets orbiting the sun, accompanied by a description and interactive elements for exploring the planets.](https://kodekloud.com/kk-media/image/upload/v1752875892/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/solar-system-planets-orbiting-sun.jpg)

***

## Step 7: Review Deployment Logs

* **Build Job**: Checkout, Node.js setup, install, build, test, and packaging.
* **Deploy Job**: Artifact download, unzip, and Azure webapp zip-deploy.

![The image shows a GitHub Actions page where a Node.js app is being deployed to an Azure Web App. The deployment process is complete, as indicated by the success message.](https://kodekloud.com/kk-media/image/upload/v1752875893/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/github-actions-nodejs-azure-deployment-2.jpg)

***

## Sample Node.js Application Code

Below is a simple Express app. **Do not** hardcode credentials in production—use GitHub Secrets and environment variables.

```javascript theme={null}
// app.js
const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '/')));
app.use(cors());

// Connect to MongoDB
mongoose.connect('mongodb+srv://cluster.mongodb.net/superData', {
  user: 'superuser',
  pass: 'SuperPassword',
  useNewUrlParser: true,
  useUnifiedTopology: true
}, err => {
  if (err) console.error('MongoDB connection error:', err);
});

// Define Schema
const Schema = mongoose.Schema;
const dataSchema = new Schema({
  name: String,
  id: Number,
  description: String,
  image: String,
  velocity: String
});

// ...routes and server startup...
```

> **triangle-alert** Never commit secrets or plaintext credentials to your repository. Always leverage [GitHub Secrets](/docs/actions/security-guides/encrypted-secrets).

***

## Manual Publish Profile Download

If you prefer a manual setup:

1. In the Azure portal, select your Web App → **Get publish profile**.
2. Download the XML and save it as `AZURE_WEBAPP_PUBLISH_PROFILE` in GitHub Secrets.

![The image shows the Microsoft Azure portal interface for a web app named "ga-solar-system-demo," displaying its overview, properties, and deployment details. It includes information about the resource group, status, location, and associated GitHub project.](https://kodekloud.com/kk-media/image/upload/v1752875894/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/azure-portal-ga-solar-system-demo.jpg)

```xml theme={null}
<publishData>
  <publishProfile
    profileName="ga-solar-system-demo - Web Deploy"
    publishMethod="MSDeploy"
    publishUrl="ga-solar-system-demo.scm.azurewebsites.net:443"
    msdeploySite="ga-solar-system-demo"
    userName="$ga-solar-system-demo"
    userPWD="YOUR_PASSWORD"
    destinationAppUrl="https://ga-solar-system-demo.azurewebsites.net/">
    <!-- ... -->
  </publishProfile>
</publishData>
```

***

Congratulations! You’ve now set up a full CI/CD pipeline to build, test, and deploy your Node.js app to Azure App Service with GitHub Actions.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/b6687abe-8094-4750-910b-5daa8bc710b1/lesson/93f4e3b3-416c-4e9a-bfd3-4f13499e9a53)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/github-actions-certification/module/b6687abe-8094-4750-910b-5daa8bc710b1/lesson/8fdd90c2-c547-44dc-b6c5-c0ee11ab5ff4)


# If Expressions and Pull Request

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Deployment-with-GitHub-Actions/If-Expressions-and-Pull-Request/page

This guide explains setting up a GitHub Actions CI/CD workflow using conditional expressions for deploying applications based on branch types and pull request reviews.

In this guide, we’ll set up a GitHub Actions CI/CD workflow that uses conditional `if` expressions to deploy an application to development on feature branches and to production only from the `main` branch. Pull requests will gate production releases behind review and environment protection rules.

## Table of Contents

* [Environment Variables](#environment-variables)
* [Job Overview](#job-overview)
* [Dev Deploy Job](#dev-deploy-job)
* [Dev Integration Testing Job](#dev-integration-testing-job)
* [Prod Deploy Job](#prod-deploy-job)
* [Prod Integration Testing Job](#prod-integration-testing-job)
* [Workflow Execution & Pull Request Flow](#workflow-execution--pull-request-flow)
* [Links and References](#links-and-references)

## Environment Variables

Define shared environment variables at the top of your workflow file:

```yaml theme={null}
env:
  MONGO_URI: 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: ${{ vars.MONGO_USERNAME }}
  MONGO_PASSWORD: ${{ secrets.MONGO_PASSWORD }}
```

> **triangle-alert** Always store sensitive data such as database credentials and API keys in GitHub [Secrets](/docs/actions/security-guides/encrypted-secrets) or [Variables](/docs/actions/variables).

## Job Overview

Below is a summary of each job, its trigger condition, and dependencies:

| Job Name                   | Condition                          | Needs         | Description                                   |
| -------------------------- | ---------------------------------- | ------------- | --------------------------------------------- |
| `docker`                   | Always (push or PR)                | *none*        | Builds and pushes Docker image                |
| `dev-deploy`               | `contains(github.ref, 'feature/')` | `docker`      | Deploys to the development environment        |
| `dev-integration-testing`  | `contains(github.ref, 'feature/')` | `dev-deploy`  | Runs health checks against the dev deployment |
| `prod-deploy`              | `github.ref == 'refs/heads/main'`  | `docker`      | Deploys to the production environment         |
| `prod-integration-testing` | `github.ref == 'refs/heads/main'`  | `prod-deploy` | Validates the live production endpoint        |

## Dev Deploy Job

The `dev-deploy` job runs on any branch matching `feature/`. It depends on the `docker` job:

```yaml theme={null}
jobs:
  dev-deploy:
    if: contains(github.ref, 'feature/')
    needs: docker
    environment:
      name: development
      url: https://${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4

      # Add Kubernetes deployment steps here, for example:
      # - name: Apply Manifests
      #   run: kubectl apply -f kubernetes/development
```

> **lightbulb** The `contains` function evaluates whether the branch ref string includes `feature/`. See [GitHub Actions expressions](https://docs.github.com/en/actions/learn-github-actions/expressions#about-if-expressions) for more.

## Dev Integration Testing Job

After deployment to development, run integration tests to verify application health:

```yaml theme={null}
  dev-integration-testing:
    name: Dev Integration Testing
    if: contains(github.ref, 'feature/')
    needs: dev-deploy
    runs-on: ubuntu-latest
    steps:
      - name: Test Application Health
        run: |
          curl https://${{ needs.dev-deploy.outputs.APP_INGRESS_URL }}/health
```

## Prod Deploy Job

Production deployments trigger only on the `main` branch. This job also sets up Kubernetes credentials and applies manifests:

```yaml theme={null}
  prod-deploy:
    if: github.ref == 'refs/heads/main'
    needs: docker
    environment:
      name: production
      url: https://${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4

      - name: Set up Kubernetes Credentials
        uses: azure/setup-kubectl@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBECONFIG }}

      - name: Fetch Kubernetes Cluster Details
        run: |
          kubectl version --short
          kubectl get nodes

      - name: Save Nginx Ingress IP
        id: set-ingress-host
        run: |
          echo "APP_INGRESS_HOST=$(kubectl -n ingress-nginx get service ingress-nginx-controller \
            -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
          echo "::set-output name=APP_INGRESS_HOST::$APP_INGRESS_HOST"

      - name: Replace Tokens in Manifests
        uses: cscheidlen/replace-tokens@v1
        with:
          tokenPrefix: '_{'
          tokenSuffix: '}_'
          files: ["kubernetes/production/*.yaml"]
        env:
          NAMESPACE: ${{ vars.NAMESPACE }}
          REPLICAS: ${{ vars.REPLICAS }}
          IMAGE: ${{ secrets.DOCKERHUB_USERNAME }}/solar-system:${{ github.sha }}
          INGRESS_IP: ${{ steps.set-ingress-host.outputs.APP_INGRESS_HOST }}

      - name: Deploy to Production
        run: kubectl apply -f kubernetes/production
```

## Prod Integration Testing Job

Once production is deployed, run a final health check:

```yaml theme={null}
  prod-integration-testing:
    name: Prod Integration Testing
    if: github.ref == 'refs/heads/main'
    needs: prod-deploy
    runs-on: ubuntu-latest
    steps:
      - name: Validate Production Health
        env:
          URL: ${{ needs.prod-deploy.outputs.APP_INGRESS_URL }}
        run: |
          echo "Testing URL: $URL"
          curl https://$URL/live -s -k | jq -r .status | grep -i live
```

## Workflow Execution & Pull Request Flow

1. **Feature Branch Push**
   * `docker` builds and pushes the image.
   * `dev-deploy` and `dev-integration-testing` run automatically.
   * Production jobs are skipped on feature branches.

![The image shows a GitHub Actions workflow interface for a project named "solar-system," displaying a workflow in progress with steps like unit testing, containerization, and deployment.](https://kodekloud.com/kk-media/image/upload/v1752875896/notes-assets/images/GitHub-Actions-Certification-If-Expressions-and-Pull-Request/github-actions-solar-system-workflow.jpg)

2. **Review Feature Deployments**
   * The workflow summary marks all dev jobs as successful.

![The image shows a GitHub Actions workflow summary with various jobs like unit testing, containerization, and deployment, all marked as successful. It includes a visual representation of the workflow steps and deployment protection rules.](https://kodekloud.com/kk-media/image/upload/v1752875897/notes-assets/images/GitHub-Actions-Certification-If-Expressions-and-Pull-Request/github-actions-workflow-summary-successful.jpg)

3. **Open Pull Request**
   * Create a PR from `feature/*` into `main` to prepare a production release.

![The image shows a GitHub interface where a user is creating a pull request to merge changes from a feature branch into the main branch, with a description about adding GitHub Actions workflows for CI/CD automation.](https://kodekloud.com/kk-media/image/upload/v1752875898/notes-assets/images/GitHub-Actions-Certification-If-Expressions-and-Pull-Request/github-pull-request-feature-branch.jpg)

4. **Confirm Previous Deployments**
   * The PR page lists all commits and verifies the dev deployment.

![The image shows a GitHub pull request page with a list of commits, most of which are verified, and a notification that the branch was successfully deployed.](https://kodekloud.com/kk-media/image/upload/v1752875900/notes-assets/images/GitHub-Actions-Certification-If-Expressions-and-Pull-Request/github-pull-request-commits-deployed.jpg)

5. **Merge to Main**
   * Merging triggers a new workflow: dev jobs skip, prod job awaits manual approval or timer.

![The image shows a GitHub Actions workflow interface for a project named "solar-system," displaying the status of various jobs like unit testing, code coverage, and deployment processes. The workflow is waiting for a review to deploy to production.](https://kodekloud.com/kk-media/image/upload/v1752875901/notes-assets/images/GitHub-Actions-Certification-If-Expressions-and-Pull-Request/github-actions-solar-system-workflow-2.jpg)

6. **Approve or Reject**
   * A reviewer approves the production deployment via the Actions UI.

![The image shows a GitHub Actions interface with a pending deployment review for a production environment. There are options to reject or approve and deploy the changes.](https://kodekloud.com/kk-media/image/upload/v1752875902/notes-assets/images/GitHub-Actions-Certification-If-Expressions-and-Pull-Request/github-actions-pending-deployment-review.jpg)

7. **Production Deployment Complete**
   * Once approved, the production deployment proceeds and can be monitored in the Deployments UI.

![This image shows a GitHub deployment page for a project named "solar-system," displaying active deployments and a list of recent deployment activities.](https://kodekloud.com/kk-media/image/upload/v1752875903/notes-assets/images/GitHub-Actions-Certification-If-Expressions-and-Pull-Request/github-deployment-solar-system-activity.jpg)

By leveraging conditional `if` expressions, pull requests, and environment protection rules, you can build a robust, secure CI/CD pipeline that separates development and production deployments seamlessly.

## Links and References

* [GitHub Actions Expressions](https://docs.github.com/en/actions/learn-github-actions/expressions)
* [Using Environments for Deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
* [Encrypted Secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* [Protecting Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-protected-branches)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/b6687abe-8094-4750-910b-5daa8bc710b1/lesson/aeb2d582-56fc-4619-acf8-f8e35662fb86)
