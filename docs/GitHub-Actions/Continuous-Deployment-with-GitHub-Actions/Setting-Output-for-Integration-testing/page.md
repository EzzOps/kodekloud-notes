# NAME           READY   UP-TO-DATE   AVAILABLE   AGE
kubectl -n development get pods
# NAME                                  READY   STATUS    RESTARTS   AGE
# solar-system-6db5dfbrf8c-96qcz        1/1     Running   0          26m
# solar-system-6db5dfbrf8c-psbxx        1/1     Running   0          26m
```

You should see two replicas running (`2/2`). Now we’ll update the `dev-deploy` job in `.github/workflows/solar-system.yml`.

## Adding the `environment` Block

Within a GitHub Actions job:

* `env:` defines environment variables for all steps.
* `environment:` applies GitHub environment protection rules and can display a URL in the Actions UI.

### Step 1: Basic `environment` Definition

Replace or augment the `env:` block with:

```yaml theme={null}
jobs:
  dev-deploy:
    needs: docker
    runs-on: ubuntu-latest

    # Variables for all steps:
    env:
      APP_INGRESS_URL: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}

    # Enforce your GitHub environment rules:
    environment:
      name: development
      url: https://
    
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4
      - name: Install kubectl CLI
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.26.0'
      - name: Set Kubeconfig file
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
```

### Step 2: Populate the `url:` Field

Use the output of your `set-ingress-host-address` step so that Actions shows a direct link to the deployed service:

```yaml theme={null}
jobs:
  dev-deploy:
    needs: docker
    runs-on: ubuntu-latest

    environment:
      name: development
      url: https://${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}

    outputs:
      APP_INGRESS_URL: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}

    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4
      - name: Install kubectl CLI
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.26.0'
      - name: Set Kubeconfig file
        uses: azure/k8s-set-context@v3
```

### Step 3: Full Workflow Snippet

Below is the relevant section from `.github/workflows/solar-system.yml` after adding `environment`:

```yaml theme={null}
.github/workflows/solar-system.yml:
  jobs:
    unit-testing: {}
    code-coverage: {}
    docker: {}
    dev-deploy:
      needs: docker
      runs-on: ubuntu-latest

      environment:
        name: development
        url: https://${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}

      outputs:
        APP_INGRESS_URL: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}

      steps:
        - name: Checkout Repo
          uses: actions/checkout@v4
        - name: Install kubectl CLI
          uses: azure/setup-kubectl@v3
          with:
            version: 'v1.26.0'
        - name: Set Kubeconfig file
          uses: azure/k8s-set-context@v3
```

## Observing the Protection Rule in Action

When you push these changes, the **dev-deploy** job will pause at the `environment` step, waiting out the protection rule’s timer:

<Frame>
  ![The image shows a GitHub Actions workflow interface with a series of jobs including unit testing, code coverage, and containerization, currently in progress. The workflow is triggered by a push to a specific branch.](https://kodekloud.com/kk-media/image/upload/v1752876455/notes-assets/images/GitHub-Actions-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-actions-workflow-jobs-in-progress.jpg)
</Frame>

Clicking on the paused job reveals the wait timer and any bypass options available to admins:

<Frame>
  ![The image shows a GitHub Actions interface with a confirmation dialog for deploying to a development environment, including a comment box for manual override.](https://kodekloud.com/kk-media/image/upload/v1752876456/notes-assets/images/GitHub-Actions-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-actions-deployment-confirmation-dialog.jpg)
</Frame>

<Callout icon="lightbulb">
  Only HTTP/S URLs are supported in the `environment.url` field.
</Callout>

Once approved, the summary displays the environment URL for easy access.

## Tracking Deployments Across Environments (Public Beta)

GitHub’s public beta for deployment tracking shows a history of every deployment per environment under **Actions → Deployments**. You can review commit details, branch names, timestamps, and durations in one interface.

<Frame>
  ![The image shows a GitHub blog post announcing a public beta for a new deployment tracking feature across environments, with a list of capabilities for developers and DevOps managers.](https://kodekloud.com/kk-media/image/upload/v1752876457/notes-assets/images/GitHub-Actions-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-blog-public-beta-deployment-feature.jpg)
</Frame>

Developers and managers can:

* Inspect past deployments
* Compare changes
* Sign off on releases

***

## Quick Reference Table

| Field      | Description                                                     |
| ---------- | --------------------------------------------------------------- |
| name       | The GitHub environment name (e.g., `development`, `staging`)    |
| url        | The HTTP/S link displayed in the Actions UI for quick access    |
| protection | Rules such as required reviewers, wait timers, or secrets usage |

## Scope and Precedence of Variables

| Scope       | Precedence | Example `REPLICAS` Value |
| ----------- | ---------- | ------------------------ |
| Environment | High       | `1`                      |
| Repository  | Low        | `2`                      |

***

## Key Snippet for `dev-deploy`

```yaml theme={null}
dev-deploy:
  needs: docker
  runs-on: ubuntu-latest
  environment:
    name: development
    url: https://${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
  outputs:
    APP_INGRESS_URL: ${{ steps.set-ingress-host-address.outputs.APP_INGRESS_HOST }}
```

## Links and References

* [GitHub Actions Environments](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment)
* [Kubernetes `kubectl` Overview](https://kubernetes.io/docs/reference/kubectl/overview/)
* [azure/setup-kubectl GitHub Action](https://github.com/azure/setup-kubectl)
* [azure/k8s-set-context GitHub Action](https://github.com/azure/k8s-set-context)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/92928734-1d5a-462d-9414-2d3865f5ef79/lesson/e0cdd818-d14b-4bae-8b1e-ef00cb924bc9" />
</CardGroup>


# Setting Output for Integration testing

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Deployment-with-GitHub-Actions/Setting-Output-for-Integration-testing/page

This guide explains how to set up integration testing in GitHub Actions by capturing and using dynamic Ingress host URLs.

Extend your GitHub Actions workflow with an **integration test** that automatically picks up your application’s dynamic Ingress host URL. This guide shows you how to:

* Deploy manifests to a Kubernetes cluster
* Capture the Ingress hostname as a workflow output
* Consume that output in a downstream integration-testing job

## Adding the Integration Test Job

After your `dev-deploy` job completes, add an `integration-testing` job that references the URL output:

```yaml theme={null}
jobs:
  integration-testing:
    name: Dev Integration Testing
    needs: [dev-deploy]
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

<Callout icon="lightbulb">
  The `curl` and `jq` utilities are pre-installed on the `ubuntu-latest` runner.
</Callout>

<Callout icon="triangle-alert">
  Using `curl -k` skips TLS verification. Only use this in non-production or trusted test environments.
</Callout>

## Retrieving the Ingress Host URL

To surface the Ingress host from Kubernetes into your workflow:

1. Invoke `kubectl` in the deploy job to read the host via JSONPath.
2. Write that hostname to `GITHUB_OUTPUT`.
3. Expose it as a job-level output.

### 1. Modify the Deploy Job

In your `dev-deploy` job, after applying the manifests, add a step with an ID to capture the host:

```yaml theme={null}
jobs:
  dev-deploy:
    needs: docker
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Install kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: '1.26.0'

      - name: Configure Kubeconfig
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBECONFIG }}

      - name: Deploy to Development
        run: kubectl apply -f kubernetes/development

      - id: set-ingress-host
        name: Set App Ingress Host URL
        run: |
          echo "APP_INGRESS_HOST=$(kubectl -n ${{ vars.NAMESPACE }} \
            get ingress -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')" \
            >> "$GITHUB_OUTPUT"
```

#### Kubernetes Ingress Example

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: solar-system
  namespace: development
spec:
  rules:
    - host: solar-system-{{ .Namespace }}.{{ .Ingress.IP }}.nip.io
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: solar-system
                port:
                  number: 3000
  tls:
    - hosts:
        - solar-system-{{ .Namespace }}.{{ .Ingress.IP }}.nip.io
      secretName: solar-system
```

### 2. Extract the Ingress Host via CLI

Run these commands locally or in a step to confirm your JSONPath:

| Command                                                                             | Description                                       |
| ----------------------------------------------------------------------------------- | ------------------------------------------------- |
| `kubectl -n development get ingress`                                                | List all ingresses in the `development` namespace |
| `kubectl -n development get ingress -o jsonpath='{.items[0].spec.tls[0].hosts[0]}'` | Extract the first TLS host from the ingress       |

```bash theme={null}
kubectl -n development get ingress
