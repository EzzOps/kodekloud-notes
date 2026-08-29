# Archive test reports for review
```

> **lightbulb** Use `npm ci` in CI environments for a clean, deterministic install.

***

## 3. Code Coverage

Run coverage in parallel with unit tests. We ignore coverage thresholds to avoid pipeline failures but still collect the reports.

```bash theme={null}
npm ci
npm run coverage || echo "Coverage errors ignored"
# Archive coverage reports for metrics
```

> **lightbulb** Storing coverage artifacts helps you track trends over time, even if errors are ignored.

***

## 4. Containerization

Build your Docker image, perform a quick smoke test inside a container, and push it to your Docker registry.

```bash theme={null}
docker build -t $REGISTRY/$REPO:$TAG .
docker run --rm $REGISTRY/$REPO:$TAG npm test
docker push $REGISTRY/$REPO:$TAG
```

***

## 5. Deploy to Development Cluster

Apply Kubernetes manifests to your development cluster and capture the Ingress hostname.

```bash theme={null}
kubectl apply -f k8s/
DEV_HOST=$(kubectl get ingress app-ingress \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "Development URL: https://$DEV_HOST"
```

***

## 6. Integration Testing on Dev

Verify that the application is live on the development endpoint.

```bash theme={null}
curl -f https://$DEV_HOST/live
```

***

## 7. Manual Approval

Pause the workflow until a reviewer manually approves the release. On rejection, the pipeline stops.

> **triangle-alert** Ensure that the reviewer has access to both the GitHub repo and any relevant sprint boards before approving.

***

## 8. Deploy to Production Cluster

Once approved, deploy the same manifests to your production context.

```bash theme={null}
kubectl apply -f k8s/ --context=prod
PROD_HOST=$(kubectl get ingress app-ingress \
  --context=prod \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "Production URL: https://$PROD_HOST"
```

***

## 9. Post-Deployment Integration Tests

Perform final checks against the production endpoint to validate a successful release.

```bash theme={null}
curl -f https://$PROD_HOST/live
```

***

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions/module/6136c7b5-8fe0-4a84-ae77-0274623512d5/lesson/4a8b6d38-0341-43fb-acd5-fa2866f89217)


# Workflow Configure Unit Testing

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/Workflow-Configure-Unit-Testing/page

This guide explains how to set up automated unit tests for a Solar System application using GitHub Actions.

In this guide, we’ll set up automated unit tests for our Solar System application using GitHub Actions. You’ll learn how to:

* Create and configure a workflow file
* Install Node.js dependencies
* Securely manage environment variables
* Trigger the workflow on feature branches

## 1. Create a Feature Branch

First, clone the repository and switch to a new feature branch to keep `main` stable:

```bash theme={null}
git clone https://github.com/your-org/solar-system.git
cd solar-system
git checkout -b feature/unit-testing-workflow main
```

Open the project in your editor to get started.

![The image shows a GitHub repository page for a project named "solar-system," displaying the file structure and recent commits. The repository is public and has no stars or forks.](https://kodekloud.com/kk-media/image/upload/v1752876533/notes-assets/images/GitHub-Actions-Workflow-Configure-Unit-Testing/github-repo-solar-system-structure.jpg)

## 2. Open in Visual Studio Code

You can launch VS Code locally or use the GitHub.dev web editor by appending `.dev` to the repo URL.

![The image shows a code editor with a file named "solar-system.yml" open, displaying a directory structure on the left. The interface suggests it's a GitHub repository being viewed in a development environment.](https://kodekloud.com/kk-media/image/upload/v1752876534/notes-assets/images/GitHub-Actions-Workflow-Configure-Unit-Testing/code-editor-solar-system-github-repo.jpg)

Make sure the GitHub Actions extension is installed for syntax highlighting and workflow previews.

![The image shows a Visual Studio Code interface with the GitHub Actions extension page open, displaying details about the extension and a file explorer on the left.](https://kodekloud.com/kk-media/image/upload/v1752876534/notes-assets/images/GitHub-Actions-Workflow-Configure-Unit-Testing/vscode-github-actions-extension-interface.jpg)

## 3. Define the Workflow File

Create a new file at `.github/workflows/solar-system.yml` with the following contents:

```yaml theme={null}
name: Solar System Workflow

on:
  workflow_dispatch:
  push:
    branches:
      - main
      - 'feature/*'

jobs:
  unit-testing:
    name: Unit Testing
    runs-on: ubuntu-latest
    env:
      MONGO_URI: 'mongodb+srv://supercluster.d3jj.mongodb.net/superData'
      MONGO_USERNAME: ${{ vars.MONGO_USERNAME }}
      MONGO_PASSWORD: ${{ secrets.MONGO_PASSWORD }}
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Node.js Environment
        uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'

      - name: Install Dependencies
        run: npm install

      - name: Run Unit Tests
        run: npm test
```

This workflow:

* Triggers on manual dispatch and pushes to `main` or `feature/*`
* Runs on `ubuntu-latest`
* Checks out the code, sets up Node.js v18, installs dependencies, and runs `npm test`

> **triangle-alert** Do not store sensitive credentials directly in the workflow. Use [repository secrets](https://docs.github.com/actions/security-guides/encrypted-secrets) and variables for any sensitive data.

![The image shows a GitHub page for the "setup-node" action, detailing its functionality and usage for managing Node.js versions in GitHub Actions. It includes a code snippet for configuring the action.](https://kodekloud.com/kk-media/image/upload/v1752876535/notes-assets/images/GitHub-Actions-Workflow-Configure-Unit-Testing/github-setup-node-action-usage.jpg)

## 4. Enable GitHub Actions Tab

If you cannot see the **Actions** tab:

1. Go to **Settings > Actions > General**
2. Select **Allow all actions and reusable workflows**
3. Click **Save**

![The image shows the settings page of a GitHub repository, specifically focusing on actions permissions and artifact log retention options. The "Disable actions" option is selected.](https://kodekloud.com/kk-media/image/upload/v1752876536/notes-assets/images/GitHub-Actions-Workflow-Configure-Unit-Testing/github-repo-settings-actions-permissions.jpg)

Once enabled, the Actions tab will appear in your repository.

![The image shows a GitHub Actions setup page with options to configure workflows like Docker image, Node.js package publishing, and Jekyll using Docker.](https://kodekloud.com/kk-media/image/upload/v1752876537/notes-assets/images/GitHub-Actions-Workflow-Configure-Unit-Testing/github-actions-workflows-setup-docker.jpg)

## 5. Commit and Push

Commit your new workflow and push to the feature branch:

```bash theme={null}
git add .github/workflows/solar-system.yml
git commit -m "Add unit testing workflow"
git push origin feature/unit-testing-workflow
```

Pushing this branch automatically triggers the workflow run.

## 6. Inspect Workflow Run

Visit the **Actions** tab to monitor progress. If a unit test fails, you might see an error like:

```text theme={null}
MongooseError: The 'uri' parameter to 'openUri' must be a string, got "undefined"...
```

![The image shows a GitHub Actions workflow interface with a failed unit testing job. It includes details of the setup process and logs related to the failure.](https://kodekloud.com/kk-media/image/upload/v1752876538/notes-assets/images/GitHub-Actions-Workflow-Configure-Unit-Testing/github-actions-workflow-failed-job.jpg)

## 7. Provide Environment Variables

Our `app.js` connects to MongoDB using environment variables:

```javascript theme={null}
// app.js (excerpt)
mongoose.connect(process.env.MONGO_URI, {
  user: process.env.MONGO_USERNAME,
  pass: process.env.MONGO_PASSWORD,
  useNewUrlParser: true,
  useUnifiedTopology: true
});
```

At the workflow level (shown in Step 3), we reference:

| Variable        | Type                 | Usage                        |
| --------------- | -------------------- | ---------------------------- |
| MONGO\_URI      | Hardcoded (for demo) | MongoDB connection string    |
| MONGO\_USERNAME | Repository variable  | MongoDB username (`vars`)    |
| MONGO\_PASSWORD | Repository secret    | MongoDB password (`secrets`) |

> **lightbulb** Best practice is to store connection strings and credentials in secrets and variables. Rotate secrets regularly and grant least-privilege access.

Add these via **Settings > Secrets and variables > Actions**:

1. **Name**: `MONGO_PASSWORD` (Secret)\
   **Value**: `SuperPassword`

![The image shows a GitHub repository settings page where a new secret named "MONGO\_PASSWORD" with the value "SuperPassword" is being added.](https://kodekloud.com/kk-media/image/upload/v1752876538/notes-assets/images/GitHub-Actions-Workflow-Configure-Unit-Testing/github-repo-settings-add-mongo-password.jpg)

2. **Name**: `MONGO_USERNAME` (Variable)\
   **Value**: `superuser`

![The image shows a GitHub settings page where a new action variable is being added, with the name "MONGO\_USERNAME" and the value "superuser."](https://kodekloud.com/kk-media/image/upload/v1752876539/notes-assets/images/GitHub-Actions-Workflow-Configure-Unit-Testing/github-settings-new-action-variable.jpg)

## 8. Re-run the Workflow

After adding secrets and variables, commit any remaining changes:

```bash theme={null}
git add .github/workflows/solar-system.yml
git commit -m "Configure environment variables for MongoDB"
git push origin feature/unit-testing-workflow
```

Your workflow should now succeed, connecting to MongoDB and executing all tests.

## Next Steps

Next, we’ll explore how to upload test artifacts so you can review detailed test reports after your runner completes.

***

## Links and References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [actions/setup-node](https://github.com/actions/setup-node)
* [Encrypted Secrets in GitHub Actions](https://docs.github.com/actions/security-guides/encrypted-secrets)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions/module/6136c7b5-8fe0-4a84-ae77-0274623512d5/lesson/c21be618-a76a-4930-97b0-7bcc5961e53c)
