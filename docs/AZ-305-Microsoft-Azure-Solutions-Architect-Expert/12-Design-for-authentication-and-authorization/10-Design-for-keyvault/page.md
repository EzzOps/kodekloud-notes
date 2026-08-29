# Design for keyvault

Source: https://notes.kodekloud.com/docs/AZ-305-Microsoft-Azure-Solutions-Architect-Expert/Design-for-authentication-and-authorization/Design-for-keyvault/page

This article explains how to design, set up, and manage Azure Key Vault for secure storage of keys, secrets, and certificates.

Azure Key Vault is a secure vault designed to store and manage keys, secrets, and certificates for your applications. It offers three essential functions: key management, certificate management, and secret management.

![The image is a diagram titled "Design for Azure Key Vault" by KodeKloud, illustrating key management, secret management, and certificate management with corresponding icons.](https://kodekloud.com/kk-media/image/upload/v1752867230/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-key-vault-design-diagram.jpg)

***

## Why Use Azure Key Vault?

Storing sensitive data in Azure Key Vault eliminates the need to embed credentials or encryption keys directly in your code. Your application can securely retrieve these elements at runtime. Key Vault provides robust access control using Azure Role-Based Access Control (RBAC) alongside its own data plane access policies. Even with RBAC permissions, explicit access policies are required to modify or read stored data. This separation enhances security by centralizing auditing and logging for all operations, making it easier to detect credential leaks or unauthorized access.

Azure Key Vault also streamlines key generation within the cloud, reducing the challenges of on-premises key management. Multiple Key Vaults can be deployed to meet distinct access policies or to improve performance under high request volumes.

![The image is an infographic explaining the benefits of using Azure Key Vault, highlighting features like centralized storage, access control, logging, and key generation.](https://kodekloud.com/kk-media/image/upload/v1752867231/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-key-vault-benefits-infographic.jpg)

***

## Setting Up Azure Key Vault and Managing Identities on the Azure Portal

### Creating an App Registration

Begin by setting up an identity for your application through Azure Active Directory to securely access Key Vault.

1. Open the Azure Portal and navigate to **Azure Active Directory**.
2. Under **App Registrations**, create a new registration (for example, "KodeKloud").
3. After registration, copy the Application (client) ID and the Directory (tenant) ID for later use.
4. Go to the **Certificates & Secrets** section and create a new client secret. Remember to copy the secret value immediately, as it will be hidden later.

![The image shows the Microsoft Azure portal homepage, displaying various Azure services, resources, and navigation options. A cursor hovers over the "Azure Active Directory" service.](https://kodekloud.com/kk-media/image/upload/v1752867232/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-portal-homepage-active-directory.jpg)

![The image shows a Microsoft Azure portal page for app registrations, specifically for an application named "kodekloud." It includes details like application IDs, tenant IDs, and options for managing authentication and API permissions.](https://kodekloud.com/kk-media/image/upload/v1752867234/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-portal-app-registrations-kodekloud.jpg)

### Creating a Key Vault and Adding a Secret

1. In the Azure Portal, create a new Key Vault. Ensure the name is unique as it forms part of a public endpoint.
2. Configure additional settings such as soft delete and retention policies according to your needs.
3. After deployment, navigate to the Key Vault resource and select **Secrets**.
4. Create a new secret (for example, "SQL DB") by providing a secret value along with optional fields like activation and expiration dates.

![The image shows a Microsoft Azure portal interface for managing a key vault named "kodekloudakv," displaying options for managing keys, secrets, and certificates, along with access configuration and monitoring tools.](https://kodekloud.com/kk-media/image/upload/v1752867235/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-portal-key-vault-management.jpg)

![The image shows a Microsoft Azure portal interface for creating a secret, with fields for name, secret value, and options for setting activation and expiration dates. The "Create" button is visible at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752867236/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-portal-create-secret-interface.jpg)

### Configuring Access Policies

Even with RBAC management permissions, accessing secrets in Key Vault requires explicit data plane access policies.

1. In your Key Vault, navigate to **Access Policies**.
2. Click **Create** and select the appropriate permissions (for example, grant all secret permissions when working with secrets).
3. Search for and select the app registration (e.g., "KodeKloud") that you created earlier.
4. Confirm the settings and create the access policy.

![The image shows the Microsoft Azure portal displaying access policies for a key vault named "kodekloudakv." It lists a user with specific key, secret, and certificate permissions.](https://kodekloud.com/kk-media/image/upload/v1752867237/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-portal-key-vault-access-policies.jpg)

![The image shows a Microsoft Azure interface for creating an access policy, with options to configure key, secret, and certificate permissions. Various checkboxes are available for selecting specific management operations.](https://kodekloud.com/kk-media/image/upload/v1752867238/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-access-policy-configuration.jpg)

![The image shows the Microsoft Azure interface for creating an access policy, with various permissions and settings listed, and a "Create" button highlighted.](https://kodekloud.com/kk-media/image/upload/v1752867239/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-access-policy-interface.jpg)

> **lightbulb** For enhanced security, always review and regularly update your access policies to ensure only necessary permissions are granted.

***

## Development with Visual Studio Code

After completing the Key Vault setup and configuring access policies, you can write and test code to interact with Key Vault using Visual Studio Code. Its robust development features, such as autocomplete and an integrated terminal, facilitate this process.

![The image shows a split screen with Microsoft Azure's portal on the left, displaying access policies for a key vault, and Visual Studio Code on the right, with a PowerShell terminal open.](https://kodekloud.com/kk-media/image/upload/v1752867240/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-portal-key-vault-vscode.jpg)

***

## Retrieving a Token and Accessing Secrets Using PowerShell

The following PowerShell code snippet demonstrates how to retrieve an Azure AD token using client credentials and use that token to access a secret stored in Azure Key Vault.

```powershell theme={null}
