# Deploy to a cloud provider using a GitHub Actions workflow

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Deployment-with-GitHub-Actions/Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/page

Learn to automate CI/CD for Node.js applications using GitHub Actions and Azure App Service.

Learn how to automate a complete CI/CD pipeline for your Node.js application using GitHub Actions and Azure App Service. In this guide, you’ll:

* Prepare Azure resources with the CLI or Portal
* Configure GitHub Actions workflows
* Securely connect GitHub to Azure
* Verify deployments in Azure and GitHub
* Optionally download a publish profile for manual setup

## Prerequisites

* A GitHub repository with your Node.js application
* An active [Azure subscription](https://azure.microsoft.com/free/)
* Azure CLI installed and authenticated (`az login`)
* Basic knowledge of GitHub Actions and YAML workflows

***

## Official Deployment Docs & Resources

GitHub maintains comprehensive guides for CI/CD with Azure. For more examples and advanced configuration, refer to:

* [GitHub Actions Documentation: Deploy to Azure](https://docs.github.com/actions/deployment/targeting-infrastructure-as-code/deploying-to-azure)
* [Azure App Service Documentation](https://learn.microsoft.com/azure/app-service/)

<Frame>
  ![The image shows a GitHub documentation page about deploying a Node.js project to Azure App Service using GitHub Actions. It includes sections like Introduction and Prerequisites.](https://kodekloud.com/kk-media/image/upload/v1752875884/notes-assets/images/GitHub-Actions-Certification-Deploy-to-a-cloud-provider-using-a-GitHub-Actions-workflow/github-actions-nodejs-azure-deployment.jpg)
</Frame>

***

## Create Azure App Service via CLI

Use the Azure CLI to provision your App Service plan and web app quickly.

```bash theme={null}
