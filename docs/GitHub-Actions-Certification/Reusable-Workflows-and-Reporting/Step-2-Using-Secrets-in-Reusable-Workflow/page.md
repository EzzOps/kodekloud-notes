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
  unit-testing: …
  code-coverage: …
  docker: …
  dev-deploy: …
  dev-integration-testing: …
  prod-deploy: …
  prod-integration-testing: …
```

Maintaining nearly identical steps in `dev-deploy` and `prod-deploy` quickly becomes error-prone. Use [reusable workflows](https://docs.github.com/actions/learn-github-actions/reusing-workflows) to centralize your logic.

<Callout icon="lightbulb">
  See the official documentation for an overview of [reusing workflows in GitHub Actions](https://docs.github.com/actions/learn-github-actions/reusing-workflows).
</Callout>

<Frame>
  ![The image shows a GitHub Docs page about GitHub Actions, specifically focusing on the limitations of reusing workflows. It includes a navigation menu on the left and a list of related topics on the right.](https://kodekloud.com/kk-media/image/upload/v1752876347/notes-assets/images/GitHub-Actions-Certification-Step-1-Configure-new-Reusable-Workflow/github-actions-reusing-workflows-limitations.jpg)
</Frame>

***

## 1. Create the Reusable Workflow

1. **File location**: `.github/workflows/reuse-deployment.yml`
2. **Trigger**: replace `on: workflow_dispatch` with `on: workflow_call`.
3. **Inputs**: declare `kubeconfig` as a required string.

```yaml theme={null}
# .github/workflows/reuse-deployment.yml
name: Deployment – Reusable Workflow

on:
  workflow_call:
    inputs:
      kubeconfig:
        description: 'Kubernetes config for the target cluster'
        required: true
        type: string
```

### Full Workflow Definition

```yaml theme={null}
# .github/workflows/reuse-deployment.yml
name: Deployment – Reusable Workflow

on:
  workflow_call:
    inputs:
      kubeconfig:
        description: 'Kubernetes config for the target cluster'
        required: true
        type: string

jobs:
  reuse-deploy:
    runs-on: ubuntu-latest
    environment:
      name: development          # Can be overridden by caller
      url: https://${{ steps.set-ingress-host.outputs.APP_INGRESS_HOST }}
    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host.outputs.APP_INGRESS_HOST }}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install kubectl CLI
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.26.0'

      - name: Set Kubeconfig
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ inputs.kubeconfig }}

      - name: Fetch cluster details
        run: |
          kubectl version --short
          echo '---'
          kubectl get nodes

      - name: Save Nginx Ingress Controller IP to GITHUB_ENV
        run: |
          echo "INGRESS_IP=$(kubectl -n ingress-nginx \
            get svc ingress-nginx-controller \
            -o jsonpath='{.status.loadBalancer.ingress[0].ip}')" >> $GITHUB_ENV

      - name: Replace tokens in manifest files
        uses: cschleiden/replace-tokens@v1
        with:
          tokenPrefix: '_'
          tokenSuffix: '_'
          files: ['kubernetes/development/*.yaml']
        env:
          NAMESPACE: ${{ vars.NAMESPACE }}
          REPLICAS: ${{ vars.REPLICAS }}
          DOCKER_IMAGE: ${{ vars.DOCKER_IMAGE }}

      - name: Create MongoDB secret
        run: |
          kubectl -n ${{ vars.NAMESPACE }} create secret generic mongo-db-creds \
            --from-literal=MONGO_URI=${{ vars.MONGO_URI }} \
            --from-literal=MONGO_USERNAME=${{ vars.MONGO_USERNAME }} \
            --from-literal=MONGO_PASSWORD=${{ secrets.MONGO_PASSWORD }} \
            --save-config --dry-run=client -o yaml | kubectl apply -f -

      - name: Deploy to development
        run: |
          kubectl apply -f kubernetes/development

      - name: Set application ingress host URL
        id: set-ingress-host
        run: |
          echo "APP_INGRESS_HOST=$(kubectl -n ${{ vars.NAMESPACE }} \
            get ingress -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')" >> "$GITHUB_OUTPUT"
```

***

## 2. Call the Reusable Workflow

Replace the inline `dev-deploy` and `prod-deploy` jobs in your main pipeline:

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
  unit-testing: …
  code-coverage: …
  docker: …

  dev-deploy:
    if: contains(github.ref, 'feature/')
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    with:
      kubeconfig: ${{ secrets.KUBECONFIG }}

  dev-integration-testing: …

  prod-deploy:
    if: github.ref == 'refs/heads/main'
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    with:
      kubeconfig: ${{ secrets.KUBECONFIG }}

  prod-integration-testing: …
```

| Original Job  | Reusable Workflow Call                           |
| ------------- | ------------------------------------------------ |
| `dev-deploy`  | `uses: ./.github/workflows/reuse-deployment.yml` |
| `prod-deploy` | `uses: ./.github/workflows/reuse-deployment.yml` |

<Frame>
  ![The image shows a GitHub Actions workflow interface with a series of jobs and their statuses, including unit testing, code coverage, and deployment steps. The workflow is titled "modified path of reusable workflow" and is currently in a waiting status.](https://kodekloud.com/kk-media/image/upload/v1752876349/notes-assets/images/GitHub-Actions-Certification-Step-1-Configure-new-Reusable-Workflow/github-actions-workflow-jobs-status.jpg)
</Frame>

***

## 3. Troubleshoot Missing Inputs

If your pipeline fails with:

```text theme={null}
Input required and not supplied: kubeconfig
```

it indicates that the caller did not pass the required `kubeconfig` input.

<Frame>
  ![The image shows a GitHub Actions workflow with a failed job in the "dev-deploy" stage due to a missing "kubeconfig" input. Other stages like unit testing and code coverage are marked as successful.](https://kodekloud.com/kk-media/image/upload/v1752876350/notes-assets/images/GitHub-Actions-Certification-Step-1-Configure-new-Reusable-Workflow/github-actions-failed-job-kubeconfig.jpg)
</Frame>

<Callout icon="triangle-alert">
  Always pass **all** required inputs when calling a reusable workflow:

  ```yaml theme={null}
  with:
    kubeconfig: ${{ secrets.KUBECONFIG }}
  ```
</Callout>

***

## References

* [Reusing workflows in GitHub Actions](https://docs.github.com/actions/learn-github-actions/reusing-workflows)
* [azure/setup-kubectl GitHub Action](https://github.com/Azure/setup-kubectl)
* [azure/k8s-set-context GitHub Action](https://github.com/Azure/k8s-set-context)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/da8706ee-24ab-41a1-916d-da8232ca028e/lesson/705ff718-165a-4638-8b0c-e9047a2a6c66" />
</CardGroup>


# Step 2 Using Secrets in Reusable Workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Reusable-Workflows-and-Reporting/Step-2-Using-Secrets-in-Reusable-Workflow/page

Learn to securely pass secrets into a reusable GitHub Actions workflow with various methods and common pitfalls.

In this lesson, you’ll learn how to securely pass secrets into a reusable GitHub Actions workflow. We’ll cover:

* Inspecting a reusable workflow to identify required secrets
* Two approaches for passing secrets
* A step-by-step guide to explicitly declare and pass secrets
* Common pitfalls and how to propagate environment variables

***

## Inspecting the Reusable Workflow

First, review the reusable workflow metadata to see which secrets it expects:

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
      APP_INGRESS_URL:
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
          # ...
```

A quick search shows this workflow requires two secrets:

| Secret Name        | Purpose                        |
| ------------------ | ------------------------------ |
| `k8s-kubeconfig`   | Kubernetes cluster credentials |
| `mongodb-password` | MongoDB database password      |

These must be supplied by the caller workflow (the “Solar System Workflow”).

***

## Caller Workflow Example

Here’s how you might create a Kubernetes secret and deploy in your caller workflow:

```yaml theme={null}
- name: Create MongoDB Secret
  run: |
    kubectl -n ${{ vars.NAMESPACE }} create secret generic mongo-db-creds \
      --from-literal=MONGO_URI=${{ env.MONGO_URI }} \
      --from-literal=MONGO_USERNAME=${{ vars.MONGO_USERNAME }} \
      --from-literal=MONGO_PASSWORD=${{ secrets.MONGO_PASSWORD }} \
      --save-config -o yaml | kubectl apply -f -

- name: Deploy to Dev Env
  run: |
    kubectl apply -f kubernetes/development

- name: Set App Ingress Host URL
  id: set-ingress-host-address
  run: |
    echo "APP_INGRESS_HOST=$(kubectl -n ${{ vars.NAMESPACE }} \
      get ingress -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')"
```

***

## Approaches to Passing Secrets

You have two main methods for forwarding secrets to a reusable workflow:

| Method                         | Description                                                                   |
| ------------------------------ | ----------------------------------------------------------------------------- |
| `secrets: inherit`             | Automatically inherits all organization-level secrets.                        |
| Explicit `secrets` declaration | You specify exactly which secrets to forward, improving clarity and security. |

<Callout icon="lightbulb">
  Using `secrets: inherit` is quick, but explicit declaration reduces blast radius by only passing the secrets you need.
</Callout>

***

## Step-by-Step: Explicitly Passing Secrets

Follow these steps to declare and forward secrets in your reusable workflow.

### 1. Declare Secrets in the Reusable Workflow

Add a `secrets` section under `workflow_call`:

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
            --save-config -o yaml | kubectl apply -f -

      - name: Deploy to Dev Env
        run: kubectl apply -f kubernetes/development

      - name: Set App Ingress Host URL
        id: set-ingress-host-address
        run: |
          echo "APP_INGRESS_HOST=$(kubectl -n ${{ vars.NAMESPACE }} \
            get ingress -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')"
```

### 2. Call the Reusable Workflow with Secrets

Reference the reusable workflow from your Solar System repo and pass the required secrets:

```yaml theme={null}
jobs:
  dev-deploy:
    if: contains(github.ref, 'feature/')
    needs: docker
    uses: ./.github/workflows/reuse-deployment.yml
    secrets:
      k8s-kubeconfig: ${{ secrets.KUBECONFIG }}
      mongodb-password: ${{ secrets.MONGO_PASSWORD }}
```

<Callout icon="triangle-alert">
  If a required secret is missing, the workflow will fail to start with an “invalid workflow file” error. Always verify secret names and availability before committing.
</Callout>

Successful execution will show:

```plaintext theme={null}
✔ Kubeconfig set
```

***

## Limitation: Environment Variables Aren’t Propagated

Note that environment variables (e.g., `MONGO_URI`) defined in the caller do *not* automatically flow into a reusable workflow:

```bash theme={null}
echo $URL
curl https://$URL/live -s -k | jq -r .status | grep -i live
