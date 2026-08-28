# Starter pipeline
trigger:
- none

pool:
  vmImage: 'ubuntu-latest'

steps:
- script: echo Hello, world!
  displayName: 'One-line script'

- script: |
    echo Add build, test, and deploy tasks here.
    echo See https://aka.ms/yaml
  displayName: 'Multi-line script'
```

## 5. Linking Key Vault Secrets in a Variable Group

1. In Azure DevOps, navigate to **Pipelines** → **Library** → **+ Variable group**.
2. Name it `KeyVaultSecrets`.
3. Toggle on **Link secrets from an Azure key vault as variables**.
4. Select your `KodeKloud Key Vault Connection` and choose the vault `KodeKloudKeyVault123`.
5. Add the secret **DBPassword** and click **Save**.

<Frame>
  ![The image shows an Azure DevOps interface for configuring a variable group named "KeyVaultSecrets," with options to link secrets from an Azure key vault. A warning message indicates the need for secret management permissions.](https://kodekloud.com/kk-media/image/upload/v1752867928/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-Azure-Pipelines-Secrets-with-Azure-Key-Vault/azure-devops-variable-group-keyvault-secrets.jpg)
</Frame>

## 6. Retrieving and Using the Secret in a Pipeline

Extend your YAML to reference the variable group and add the Azure Key Vault task:

```yaml theme={null}
pool:
  vmImage: 'ubuntu-latest'

variables:
- group: KeyVaultSecrets

steps:
- script: echo Hello, world!
  displayName: 'One-line script'

- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'KodeKloud Key Vault Connection'
    KeyVaultName: 'KodeKloudKeyVault123'
    SecretsFilter: 'DBPassword'
    RunAsPreJob: false

- script: echo "Using database password: $(DBPassword)"
  displayName: 'Use the secret'
```

Run the pipeline and, when prompted, grant permission for the service connection to read Key Vault secrets.

<Frame>
  ![The image shows an Azure DevOps pipeline interface where a permission request is needed to access a resource, with options to permit or cancel the action.](https://kodekloud.com/kk-media/image/upload/v1752867929/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-Azure-Pipelines-Secrets-with-Azure-Key-Vault/azure-devops-pipeline-permission-request.jpg)
</Frame>

Upon successful execution, you’ll see the retrieval step complete with the password masked in the logs:

```bash theme={null}
echo "Using database password: ***"
```

## Additional Examples

Below are common scenarios for using Key Vault in pipelines.

| Scenario                        | Task                                                |
| ------------------------------- | --------------------------------------------------- |
| .NET Core build                 | Fetch `DatabasePassword` then run `DotNetCoreCLI@2` |
| Web App deployment with API key | Fetch `ApiKey` then run `AzureWebApp@1`             |

```yaml theme={null}
# .NET Core build using Key Vault secret
steps:
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'MyKeyVaultConnection'
    KeyVaultName: 'MyDemoKeyVault'
    SecretsFilter: 'DatabasePassword'

- task: DotNetCoreCLI@2
  inputs:
    command: 'build'
    projects: '**/*.csproj'
  env:
    ConnectionString: "Server=myserver;Database=mydb;User Id=admin;Password=$(DatabasePassword)"
```

```yaml theme={null}
# Deploy to Azure Web App with Key Vault API Key
steps:
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'MyKeyVaultConnection'
    KeyVaultName: 'MyDemoKeyVault'
    SecretsFilter: 'ApiKey'

- task: AzureWebApp@1
  inputs:
    azureSubscription: 'MyAzureSubscription'
    appName: 'MyWebApp'
    deployToSlotOrASE: true
    resourceGroupName: 'MyResourceGroup'
    slotName: 'production'
    appSettings: '-ApiKey $(ApiKey)'
```

## Best Practices

* Never store secrets in source code or text files.
* Enforce the principle of least privilege on Key Vault access policies.
* Rotate and expire secrets routinely.
* Prefer Managed Identities over service principals when possible.
* Implement logging and auditing for all Key Vault operations.
* Maintain separate vaults for development, testing, and production.

## Links and References

* [Azure Key Vault Documentation](https://docs.microsoft.com/azure/key-vault/)
* [Azure Pipelines YAML Schema](https://docs.microsoft.com/azure/devops/pipelines/yaml-schema)
* [Azure DevOps Service Connections](https://docs.microsoft.com/azure/devops/pipelines/library/service-endpoints)
* [Managing Secrets with Azure Key Vault](https://docs.microsoft.com/azure/devops/pipelines/tasks/deploy/azure-key-vault)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/2f8974b7-9aa9-46b8-a562-d7ed568269af/lesson/84b2e01a-665b-40aa-a5e2-d2c583106b18" />
</CardGroup>


# Exploring GitHub Secrets

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-a-Strategy-for-Managing-Sensitive-Information-in-Automation/Exploring-GitHub-Secrets/page

This guide explains managing GitHub Secrets for secure automation, covering setup, usage in workflows, and best practices.

In this guide, you’ll learn how to manage encrypted variables in GitHub—commonly known as **GitHub Secrets**—to keep API keys, tokens, and credentials safe. We’ll cover what secrets are, how to set them up, use them in workflows, and follow best practices for secure automation.

## What Are GitHub Secrets?

GitHub Secrets are encrypted environment variables stored at the repository, environment, or organization level. They enable you to reference sensitive data in your Actions workflows without exposing them in code.

| Scope                | Description                                                  | Ideal for                  |
| -------------------- | ------------------------------------------------------------ | -------------------------- |
| Repository secrets   | Accessible only in a single repository                       | Project-specific API keys  |
| Environment secrets  | Scoped to named environments (e.g., `staging`, `production`) | Deployment credentials     |
| Organization secrets | Shared across multiple repositories within an organization   | Centralized service tokens |

### Viewing Secrets and Variables

To inspect secrets in a repository:

1. Navigate to **Settings** → **Secrets and variables**.
2. Choose **Actions**, **Codespaces**, or **Dependabot**.

<Frame>
  ![The image shows a GitHub repository settings page for "Actions secrets and variables," displaying a repository secret named "AZURE\_WEBAPP\_PUBLISH\_PROFILE."](https://kodekloud.com/kk-media/image/upload/v1752867930/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-GitHub-Secrets/github-repo-actions-secrets-variables.jpg)
</Frame>

#### Variables vs. Secrets

* **Secrets** are encrypted and masked in logs.
* **Variables** hold non-sensitive data (e.g., server names) and can be updated centrally.

<Frame>
  ![The image shows a GitHub repository settings page for "Actions secrets and variables," with options to manage secrets and variables. The "Variables" tab is selected, and there are no repository variables currently set.](https://kodekloud.com/kk-media/image/upload/v1752867931/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-GitHub-Secrets/github-repo-actions-secrets-variables-2.jpg)
</Frame>

## Creating and Updating Repository Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**.
2. Click **New repository secret**.
3. Enter a **Name** (e.g., `API_KEY`) and the secret **Value**.
4. Click **Add secret**.

<Frame>
  ![The image shows a GitHub interface where a user is adding a new secret under "Actions secrets" in the settings of a project. The fields for "Name" and "Secret" are being filled out.](https://kodekloud.com/kk-media/image/upload/v1752867932/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-GitHub-Secrets/github-actions-secrets-settings-interface.jpg)
</Frame>

Once created, the secret appears in the list—its value remains hidden:

<Frame>
  ![The image shows a GitHub repository settings page for managing "Actions secrets and variables," with an "API\_KEY" listed as a repository secret.](https://kodekloud.com/kk-media/image/upload/v1752867933/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-GitHub-Secrets/github-repo-settings-actions-secrets.jpg)
</Frame>

To update a secret, click **Edit**, provide a new value, and re-authenticate if prompted.

## Using Secrets in a Workflow

Add secrets to your workflow YAML to inject them at runtime. Create a file like `.github/workflows/hello.yml`:

```yaml theme={null}
on:
  workflow_dispatch:

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    steps:
      - name: Hello World Action
        run: |
          curl -H "Authorization: Bearer ${{ secrets.API_KEY }}" \
               https://en12e6i3tq18hk.x.pipedream.net
```

Here, `${{ secrets.API_KEY }}` retrieves the value securely.

<Frame>
  ![The image shows a GitHub Actions setup page for a repository, offering options to configure workflows such as a simple workflow or deployment to various cloud services.](https://kodekloud.com/kk-media/image/upload/v1752867935/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-GitHub-Secrets/github-actions-workflow-setup-page.jpg)
</Frame>

Commit the workflow and trigger it manually or on push. GitHub masks the secret in logs, replacing characters with `***`, while your external endpoint receives the correct token.

<Frame>
  ![The image shows a GitHub Actions interface with a workflow file named main.yml and two recent workflow runs. The interface includes options for managing workflows and running them manually.](https://kodekloud.com/kk-media/image/upload/v1752867936/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-GitHub-Secrets/github-actions-workflow-main-yml.jpg)
</Frame>

<Callout icon="triangle-alert">
  Secrets are **not** exposed to workflows triggered by pull requests from forks. This prevents unauthorized access to your credentials.
</Callout>

## Advanced GitHub Secrets Usage

### Deploying to Azure with JSON Credentials

Store full JSON service principals in a secret and use them:

```yaml theme={null}
name: Deploy to Azure
on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

<Callout icon="lightbulb">
  GitHub automatically masks secrets in Action logs, so your credentials never appear in plaintext.
</Callout>

### Automating Secret Rotation

Use a scheduled workflow to rotate keys monthly:

```yaml theme={null}
name: Rotate API Key
on:
  schedule:
    - cron: '0 0 1 * *' # Monthly at midnight UTC

jobs:
  rotate-key:
    runs-on: ubuntu-latest
    steps:
      - name: Generate new API key
        run: |
          NEW_KEY=$(openssl rand -base64 32)
          echo "NEW_KEY=$NEW_KEY" >> $GITHUB_ENV

      - name: Update external service
        run: |
          curl -X POST https://api.example.com/rotate-key \
            -H "Authorization: Bearer ${{ secrets.CURRENT_API_KEY }}" \
            -d "{\"new_key\": \"$NEW_KEY\"}"

      - name: Update GitHub Secret
        uses: hmanzur/actions-set-secret@v2.0.0
        with:
          name: CURRENT_API_KEY
          value: $NEW_KEY
```

### Auditing Secret Usage

Log each secret access for compliance:

```yaml theme={null}
steps:
  - name: Log secret usage
    if: success() && contains(github.event.head_commit.message, 'DEPLOY_KEY')
    run: |
      echo "Secret DEPLOY_KEY used at $(date)" >> $GITHUB_WORKSPACE/secret_usage.log

  - name: Use secret
    env:
      DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
    run: ./deploy.sh
```

## Best Practices for GitHub Secrets

<Frame>
  ![The image shows a list of best practices for managing secrets in code, including limiting exposure, using short-lived tokens, and enabling secret scanning.](https://kodekloud.com/kk-media/image/upload/v1752867937/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Exploring-GitHub-Secrets/best-practices-managing-secrets-code.jpg)
</Frame>

* Limit access with fine-grained permissions.
* Use short-lived tokens or ephemeral credentials.
* Never commit secrets to code or configuration files.
* Require approvals for environment secrets in production.
* Rotate and audit secrets regularly.
* Enable [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning).
* Train your team on secure secret handling.

## References

* [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* [GitHub Actions Overview](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions)
* [Azure Login Action](https://github.com/Azure/login)
* [azure/webapps-deploy@v2](https://github.com/Azure/webapps-deploy)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/2f8974b7-9aa9-46b8-a562-d7ed568269af/lesson/9e18cfda-9382-45f4-b949-cf495175af5c" />
</CardGroup>
