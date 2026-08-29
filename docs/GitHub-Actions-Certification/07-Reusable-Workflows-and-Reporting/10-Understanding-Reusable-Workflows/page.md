# shell: /usr/bin/bash -e {0}
# env:
#   MONGO_URI: mongodb+srv://...
URL: [
Error: Process completed with exit code 1.
```

The root cause is that `APP_INGRESS_URL` isn’t available to the test job. To fix this, we need to define and export `outputs` in our reusable workflow.

## 1. Define Workflow-Level Outputs

Edit `.github/workflows/reuse-deployment.yml` and add an `outputs` section under `on.workflow_call`:

```yaml theme={null}
name: Deployment - Reusable Workflow
on:
  workflow_call:
    inputs:
      environment:
        description: Deployment environment (dev or prod)
        required: true
        default: dev
        type: string
      mongodb-uri:
        description: MongoDB connection URI
        required: true
        type: string
      k8s-manifest-dir:
        description: Path to Kubernetes manifests
        required: true
        type: string
      kubectl-version:
        description: kubectl version
        required: false
        default: v1.24.0
        type: string
    secrets:
      k8s-kubeconfig:
        required: true
      mongodb-password:
        required: true
    outputs:
      application-url:
        description: The application ingress URL
        value: ${{ jobs.reuse-deploy.outputs.APP_INGRESS_URL }}
```

## 2. Map Job Outputs to Workflow Outputs

Inside the `reuse-deploy` job, expose the ingress host address:

```yaml theme={null}
jobs:
  reuse-deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.environment }}
      url: https://${{ steps.set-ingress-host.outputs.ingress_host }}
    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host.outputs.ingress_host }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: ${{ inputs.kubectl-version }}

      - name: Configure kubeconfig
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.k8s-kubeconfig }}

      - name: Deploy manifests
        run: |
          kubectl apply -f ${{ inputs.k8s-manifest-dir }}
          echo "Deployment complete."

      - name: Extract ingress host
        id: set-ingress-host
        run: |
          host=$(kubectl get ingress \
            -n ${{ inputs.environment }} \
            -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
          echo "ingress_host=$host" >> $GITHUB_OUTPUT
```

<Callout icon="lightbulb">
  Make sure the `id` in the step (here: `set-ingress-host`) matches when you reference `steps.<id>.outputs`.
</Callout>

## 3. Consume Outputs in the Caller Workflow

In your main workflow (e.g., `.github/workflows/ci.yml`), invoke the reusable workflow and pass its outputs to integration tests:

```yaml theme={null}
jobs:
  docker:
    runs-on: ubuntu-latest
    # Build and push image
    steps: …

  dev-deploy:
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    with:
      mongodb-uri: ${{ vars.MONGO_URI }}
      environment: development
      k8s-manifest-dir: kubernetes/development
    secrets:
      k8s-kubeconfig: ${{ secrets.KUBECONFIG }}
      mongodb-password: ${{ secrets.MONGO_PASSWORD }}

  dev-integration-testing:
    needs: dev-deploy
    runs-on: ubuntu-latest
    steps:
      - name: Run integration tests
        env:
          URL: ${{ needs.dev-deploy.outputs.application-url }}
        run: |
          echo "Testing $URL"
          curl -s -k https://$URL/live | jq -r '.status' | grep -qi live

  prod-deploy:
    if: github.ref == 'refs/heads/main'
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    with:
      mongodb-uri: ${{ vars.MONGO_URI }}
      environment: production
      k8s-manifest-dir: kubernetes/production
    secrets:
      k8s-kubeconfig: ${{ secrets.KUBECONFIG }}
      mongodb-password: ${{ secrets.MONGO_PASSWORD }}

  prod-integration-testing:
    if: github.ref == 'refs/heads/main'
    needs: prod-deploy
    runs-on: ubuntu-latest
    steps:
      - name: Validate production URL
        env:
          URL: ${{ needs.prod-deploy.outputs.application-url }}
        run: |
          echo "Production URL: $URL"
          curl -s -k https://$URL/live | jq -r '.status' | grep -qi live
```

| Job                      | Consumes Output                                         |
| ------------------------ | ------------------------------------------------------- |
| dev-deploy               | Generates `application-url` via reusable wf             |
| dev-integration-testing  | Uses `${{ needs.dev-deploy.outputs.application-url }}`  |
| prod-deploy              | Generates `application-url` for production              |
| prod-integration-testing | Uses `${{ needs.prod-deploy.outputs.application-url }}` |

## 4. Verify the Workflow Summary

After committing and pushing, the GitHub Actions summary will show all jobs passing, including the integration tests with the correct URLs.

<Frame>
  ![The image shows a GitHub Actions workflow summary for a project, indicating successful completion of various jobs like unit testing, code coverage, and deployment. The workflow is titled "Solar System Workflow" and includes details such as the trigger, status, and duration.](../../../../images/kodekloud.com/kk-media/image/upload/v1752876355/notes-assets/images/GitHub-Actions-Certification-Step-4-Using-Outputs-in-Reusable-Workflow/github-actions-solar-system-workflow-summary.jpg)
</Frame>

A snippet from **dev-integration-testing** logs confirms the URL is passed correctly:

```bash theme={null}
# env: URL: solar-system-development.172.232.87.200.nip.io
# Testing solar-system-development.172.232.87.200.nip.io
curl -s -k https://solar-system-development.172.232.87.200.nip.io/live | jq -r '.status'…
```

With this setup, your workflows remain modular, DRY, and easy to manage by:

* Defining inputs, secrets, and outputs in a reusable workflow.
* Mapping job-level outputs to workflow-level outputs.
* Accessing those outputs in downstream jobs.

## Links and References

* [GitHub Actions: Reusable Workflows](https://docs.github.com/actions/learn-github-actions/reusing-workflows)
* [workflow\_call event](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows#workflow_call)
* [GitHub Actions Outputs](https://docs.github.com/actions/using-workflows/workflow-outputs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/da8706ee-24ab-41a1-916d-da8232ca028e/lesson/93d520dd-bf81-4fcb-b445-d3879f5fd4c3" />
</CardGroup>


# Understanding Reusable Workflows

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Reusable-Workflows-and-Reporting/Understanding-Reusable-Workflows/page

This guide explains how to create and use reusable workflows in GitHub Actions to streamline deployment processes.

By centralizing common jobs—like deployment—into standalone workflows, you can reduce duplication, simplify updates, and enforce best practices across all your repositories. This guide shows you how to extract deployment logic into a reusable workflow and invoke it from language-specific CI pipelines.

## Sample CI Workflow for a Node.js App

Here’s an example `.github/workflows/ci-testing.yml` that runs tests, coverage, dependency scanning, build, and deployments in sequence:

```yaml theme={null}
name: CI Workflow
on: push

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [macos-latest, ubuntu-latest, windows-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: npm install
      - name: Run unit tests
        run: npm test

  code-coverage:
    needs: unit-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate coverage report
        run: npm run coverage

  dependency-scan:
    needs: code-coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Scan for vulnerabilities
        run: npm audit

  build:
    needs: dependency-scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build application
        run: npm run build

  deploy-dev:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '14'
      - name: Authenticate to DEV
        run: echo "Authenticating to DEV"
      - name: Deploy to development
        run: echo "Deploying to development environment"
      - name: Notify team
        run: echo "Development deployment complete"

  deploy-prod:
    needs: deploy-dev
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '14'
      - name: Authenticate to PROD
        run: echo "Authenticating to PROD"
      - name: Deploy to production
        run: echo "Deploying to production environment"
      - name: Notify team
        run: echo "Production deployment complete"
```

<Callout icon="triangle-alert">
  Copy-pasting deployment steps across multiple workflows leads to fragmented updates and higher maintenance costs. A single change requires edits in every file.
</Callout>

## Why Use Reusable Workflows?

A **reusable workflow** is a YAML file that other workflows can invoke via `workflow_call`. Benefits include:

| Benefit              | Description                                              |
| -------------------- | -------------------------------------------------------- |
| Avoid duplication    | Define deployment logic once and reuse everywhere.       |
| Simplify maintenance | Update a single file to apply changes organization-wide. |
| Enforce standards    | Share audited, best-practice workflows across teams.     |

## Example Repository Layout

Assume the following structure in your `XYZ/nodejs-app-repo`:

* `.github/workflows/awesome-app.yaml`
* `.github/workflows/reusable-workflow.yaml`

### Original Workflow: awesome-app.yaml

This caller workflow builds the app, runs tests, and then invokes the reusable deployment job:

```yaml theme={null}
name: My Awesome App
on: push

jobs:
  unit-testing:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm test

  code-coverage:
    needs: unit-testing
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm run coverage

  build:
    needs: code-coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm run build

  dev-deploy:
    needs: build
    uses: ./.github/workflows/reusable-workflow.yaml
    with:
      environment: development
    secrets:
      DEPLOY_TOKEN: ${{ secrets.DEV_DEPLOY_TOKEN }}
```

### Reusable Workflow: reusable-workflow\.yaml

By declaring `on.workflow_call`, you expose inputs, secrets, and jobs that any caller workflow can use:

```yaml theme={null}
name: Reusable Deployment
on:
  workflow_call:
    inputs:
      environment:
        type: string
        required: true
    secrets:
      DEPLOY_TOKEN:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '14'

      - name: Authenticate with cloud
        run: echo "Authenticating for ${{ inputs.environment }} using ${{ secrets.DEPLOY_TOKEN }}"

      - name: Deploy to ${{ inputs.environment }}
        run: echo "Deploying to ${{ inputs.environment }} environment"

      - name: Notify team
        run: echo "${{ inputs.environment }} deployment complete"
```

## Invoking the Reusable Workflow

You can call this reusable workflow from *any* repository or branch:

```yaml theme={null}
dev-deploy:
  needs: build
  uses: ./.github/workflows/reusable-workflow.yaml
  with:
    environment: development
  secrets:
    DEPLOY_TOKEN: ${{ secrets.DEV_DEPLOY_TOKEN }}

prod-deploy:
  needs: dev-deploy
  uses: ./.github/workflows/reusable-workflow.yaml
  with:
    environment: production
  secrets:
    DEPLOY_TOKEN: ${{ secrets.PROD_DEPLOY_TOKEN }}
```

<Callout icon="lightbulb">
  Inputs and secrets are strongly typed. Ensure that every `workflow_call` declaration and invocation matches the expected names and types.
</Callout>

## Key Terminology

* **Caller workflow**: The YAML file that uses `uses:` to invoke a reusable workflow.
* **Called workflow**: The reusable workflow that declares `on.workflow_call`.

## Links and References

* [GitHub Actions: Reusing workflows](https://docs.github.com/actions/learn-github-actions/reusing-workflows)
* [GitHub Actions: Workflow syntax](https://docs.github.com/actions/reference/workflow-syntax-for-github-actions)
* [actions/checkout](https://github.com/actions/checkout)
* [actions/setup-node](https://github.com/actions/setup-node)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/da8706ee-24ab-41a1-916d-da8232ca028e/lesson/0e2de6f2-1dde-44bc-b811-26879e55f770" />
</CardGroup>
