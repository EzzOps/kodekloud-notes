# .github/workflows/reuse-deployment.yml
name: Deployment - Reusable Workflow

on:
  workflow_call:
    inputs:
      namespace:
        description: 'Kubernetes namespace'
        required: true
        type: string
      kubeconfig:
        description: 'Kubeconfig file contents'
        required: true
        type: string
    secrets:
      KUBECONFIG:
        description: 'Kubernetes kubeconfig secret'
        required: true

jobs:
  reuse-deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.namespace }}
      url: https://${{ steps.set-ingress-host.outputs.APP_INGRESS_URL }}
    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host.outputs.APP_INGRESS_URL }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: '1.26.0'

      - name: Set kubeconfig
        run: |
          echo "${{ secrets.KUBECONFIG }}" > kubeconfig
          export KUBECONFIG=$PWD/kubeconfig

      - name: Fetch cluster details
        run: |
          kubectl version --short
          echo "----------"
          kubectl get nodes

      - name: Replace tokens in manifests
        uses: cschleiden/replace-tokens@v1
        with:
          tokenPrefix: '_'
          tokenSuffix: '_'
          files: 'kubernetes/${{ inputs.namespace }}/*.yaml'
        env:
          NAMESPACE: ${{ inputs.namespace }}
          REPLICAS: ${{ vars.REPLICAS }}
          DOCKER_IMAGE: ${{ vars.DOCKER_IMAGE }}
          GITHUB_SHA: ${{ github.sha }}

      - name: Create MongoDB Secret
        run: |
          kubectl -n ${{ inputs.namespace }} create secret generic mongo-db-creds \
            --from-literal=MONGO_URI=${{ env.MONGO_URI }} \
            --from-literal=MONGO_USERNAME=${{ vars.MONGO_USERNAME }} \
            --from-literal=MONGO_PASSWORD=${{ secrets.MONGO_PASSWORD }} \
            --save-config \
            --dry-run=client \
            -o yaml | kubectl apply -f -

      - name: Deploy to ${{ inputs.namespace }}
        run: |
          kubectl apply -f kubernetes/${{ inputs.namespace }}

      - name: Set Ingress Host URL
        id: set-ingress-host
        run: |
          HOST=$(kubectl -n ${{ inputs.namespace }} get ingress \
            -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')
          echo "APP_INGRESS_URL=$HOST" >> $GITHUB_OUTPUT
```

This reusable workflow:

* Defines required `inputs` and `secrets`.
* Contains a single `reuse-deploy` job that checks out the code, configures `kubectl`, replaces tokens, creates secrets, deploys manifests, and outputs the ingress URL.

## 1.4 Invoke the Reusable Workflow

In your original workflow file (`.github/workflows/solar-system.yml`), replace the inline `dev-deploy` and `prod-deploy` jobs with calls to the reusable workflow:

```yaml theme={null}
# .github/workflows/solar-system.yml
name: Solar System Workflow

on:
  workflow_dispatch:
    branches:
      - main
      - 'feature/*'

env:
  MONGO_URI: 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
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
    if: contains(github.ref, 'feature/')
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    with:
      namespace: development
      kubeconfig: ${{ secrets.KUBECONFIG }}
    secrets:
      KUBECONFIG: ${{ secrets.KUBECONFIG }}

  dev-integration-testing:
    needs: dev-deploy
    # ...

  prod-deploy:
    if: github.ref == 'refs/heads/main'
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    with:
      namespace: production
      kubeconfig: ${{ secrets.KUBECONFIG }}
    secrets:
      KUBECONFIG: ${{ secrets.KUBECONFIG }}

  prod-integration-testing:
    needs: prod-deploy
    # ...
```

### Workflow Run Summary

After pushing these changes to a feature branch, the GitHub Actions UI will show the reusable workflow invocations:

![The image shows a GitHub Actions page displaying a list of workflow runs for a project named "solar-system," with various statuses and branches.](https://kodekloud.com/kk-media/image/upload/v1752876732/notes-assets/images/GitHub-Actions-Step-1-Configure-new-Reusable-Workflow/github-actions-solar-system-workflows.jpg)

Notice each deployment job now references `reuse-deployment.yml`.

### Job Names and Statuses

The UI prefixes the reusable-job name under `dev-deploy` and `prod-deploy` so you can easily identify the steps executed:

![The image shows a GitHub Actions workflow interface with a series of jobs and their statuses, including unit testing, code coverage, and deployment steps. The workflow is titled "modified path of reusable workflow" and is currently in a waiting state.](https://kodekloud.com/kk-media/image/upload/v1752876733/notes-assets/images/GitHub-Actions-Step-1-Configure-new-Reusable-Workflow/github-actions-workflow-jobs-status.jpg)

> **triangle-alert** If you forget to pass a required `input` or `secret`, the job will fail. For example, omitting `kubeconfig` will cause the `Set kubeconfig` step to error out:

  ![The image shows a GitHub Actions workflow run with several jobs, where the "dev-deploy" job has failed due to a missing "kubeconfig" input.](https://kodekloud.com/kk-media/image/upload/v1752876733/notes-assets/images/GitHub-Actions-Step-1-Configure-new-Reusable-Workflow/github-actions-workflow-dev-deploy-failed.jpg)

Always verify that every `input` and `secret` listed under `on.workflow_call` is provided when invoking the reusable workflow.

***

In the next lesson, we’ll cover advanced patterns for sharing secrets and artifacts across reusable workflows.

## Links and References

* [GitHub Actions: Reusing workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
* [Azure Setup Kubectl Action](https://github.com/Azure/setup-kubectl)
* [cschleiden/replace-tokens](https://github.com/cschleiden/replace-tokens)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions/module/57481ffd-2f40-4d62-af84-5f992f6c92dc/lesson/c25c7821-0b75-4404-bf62-43f3a056bb35)


# Step 2 Using Secrets in Reusable Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Reusable-Workflows-and-Reporting/Step-2-Using-Secrets-in-Reusable-Workflow/page

This guide demonstrates securely passing secrets to a reusable GitHub Actions workflow for improved maintainability and security.

In this guide, we’ll demonstrate how to securely pass `secrets` to a reusable GitHub Actions workflow. Centralizing deployment logic and managing sensitive data in one place improves maintainability and security.

## 1. Inspect the Existing Reusable Workflow

Open the reusable workflow file at `.github/workflows/reuse-deployment.yml`:

```yaml theme={null}
name: Deployment - Reusable Workflow

on:
  workflow_call:

jobs:
  reuse-deploy:
    environment:
      name: development
      url: http://example.com
    outputs:
      APP_INGRESS_HOST: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4

      - name: Install kubectl CLI
        uses: azure/setup-kubectl@v3
        with:
          version: '1.26.0'

      - name: Set Kubeconfig file
        uses: azure/k8s-set-context@v3
        with:
          # kubeconfig will be supplied via a secret

      - name: Create MongoDB Secret
        run: |
          kubectl -n ${{ vars.NAMESPACE }} create secret generic mongo-db-creds \
            --from-literal=MONGO_URI=${{ env.MONGO_URI }} \
            --from-literal=MONGO_USERNAME=${{ vars.MONGO_USERNAME }} \
            --from-literal=MONGO_PASSWORD=${{ secrets.MONGO_PASSWORD }} \
            --save-config \
            --dry-run=client -o yaml | kubectl apply -f -

      - name: Deploy to Dev Env
        run: |
          kubectl apply -f kubernetes/development

      - name: Set App Ingress Host URL
        id: set-ingress-host-address
        run: |
          echo "APP_INGRESS_HOST=$(kubectl -n ${{ vars.NAMESPACE }} get ingress \
            -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')" >> $GITHUB_OUTPUT
```

A quick review shows this workflow expects two secrets:

| Secret Name      | Required | Purpose                                             |
| ---------------- | -------- | --------------------------------------------------- |
| k8s-kubeconfig   | true     | Supplies the Kubernetes config to `k8s-set-context` |
| mongodb-password | true     | Password for MongoDB credentials secret             |

## 2. Declare Secrets in the Reusable Workflow

Extend the `on.workflow_call` section to require these secrets:

```yaml theme={null}
name: Deployment - Reusable Workflow

on:
  workflow_call:
    secrets:
      k8s-kubeconfig:
        required: true
      mongodb-password:
        required: true

jobs:
  reuse-deploy:
    environment:
      name: development
      url: https://${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
    outputs:
      APP_INGRESS_HOST: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4

      - name: Install kubectl CLI
        uses: azure/setup-kubectl@v3
        with:
          version: '1.26.0'

      - name: Set Kubeconfig file
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.k8s-kubeconfig }}

      - name: Create MongoDB Secret
        run: |
          kubectl -n ${{ vars.NAMESPACE }} create secret generic mongo-db-creds \
            --from-literal=MONGO_URI=${{ env.MONGO_URI }} \
            --from-literal=MONGO_USERNAME=${{ vars.MONGO_USERNAME }} \
            --from-literal=MONGO_PASSWORD=${{ secrets.mongodb-password }} \
            --save-config \
            --dry-run=client -o yaml | kubectl apply -f -

      - name: Deploy to Dev Env
        run: |
          kubectl apply -f kubernetes/development

      - name: Set App Ingress Host URL
        id: set-ingress-host-address
        run: |
          echo "APP_INGRESS_HOST=$(kubectl -n ${{ vars.NAMESPACE }} get ingress \
            -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')" >> $GITHUB_OUTPUT
```

> **lightbulb** Declaring secrets under `on.workflow_call` ensures GitHub Actions validates them before running any jobs.

## 3. Pass Secrets from the Caller Workflow

In your caller workflow (for example, `.github/workflows/solar-system.yml`), supply the required secrets under each job that invokes the reusable workflow:

```yaml theme={null}
jobs:
  dev-deploy:
    if: contains(github.ref, 'feature/')
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    secrets:
      k8s-kubeconfig: ${{ secrets.KUBECONFIG }}
      mongodb-password:    ${{ secrets.MONGO_PASSWORD }}

  prod-deploy:
    if: github.ref == 'refs/heads/main'
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    secrets:
      k8s-kubeconfig: ${{ secrets.KUBECONFIG }}
      mongodb-password:    ${{ secrets.MONGO_PASSWORD }}
```

## 4. Handle Missing Secrets Errors

> **triangle-alert** If you omit a required secret, GitHub Actions fails immediately with a validation error specifying the missing secret.

Ensure each job includes all declared secrets to prevent startup failures.

## 5. Verify Workflow Execution

After adding the secrets, the `dev-deploy` job should complete the Kubeconfig step successfully. If you still see empty environment variables in downstream jobs, like:

```bash theme={null}
echo $URL
Error: Process completed with exit code 1.
```

remember that GitHub Actions does not automatically propagate caller `env` variables into a reusable workflow’s outputs. You may need to explicitly map and return those variables.

## 6. Example Caller Workflow Environment

For context, here’s how global environment variables might be defined in the caller workflow:

```yaml theme={null}
name: Solar System Workflow

on:
  workflow_dispatch:
  push:
    branches:
      - main
      - 'feature/*'

env:
  MONGO_URI:      'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: ${{ vars.MONGO_USERNAME }}
  MONGO_PASSWORD: ${{ secrets.MONGO_PASSWORD }}

jobs:
  unit-testing: {}
  code-coverage: {}
  docker: {}
  dev-deploy:
    if: contains(github.ref, 'feature/')
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    secrets:
      k8s-kubeconfig: ${{ secrets.KUBECONFIG }}
      mongodb-password:    ${{ secrets.MONGO_PASSWORD }}
```

## Links and References

* [Reusing Workflows with workflow\_call](https://docs.github.com/en/actions/using-workflows/reusing-workflows#calling-a-reusable-workflow)
* [GitHub Actions Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* [azure/setup-kubectl Action](https://github.com/Azure/setup-kubectl)
* [azure/k8s-set-context Action](https://github.com/Azure/k8s-set-context)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions/module/57481ffd-2f40-4d62-af84-5f992f6c92dc/lesson/e75e577a-1c37-4703-bcf4-e6d3a26a8938)
