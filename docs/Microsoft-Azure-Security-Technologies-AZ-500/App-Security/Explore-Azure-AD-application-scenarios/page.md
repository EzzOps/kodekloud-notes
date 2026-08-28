# Authentication using Azure AD Managed Identity
# Note: Ensure that 'Active DirectoryMsi' is formatted correctly as per driver support.
conn = pyodbc.connect(connection_string + ';Authentication=Active DirectoryMsi')
tokenstruct = struct.pack("=I", len(extoken)) + exptoken
conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: tokenstruct})

with conn.cursor() as cursor:
    cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()
```

In this code, the managed identity of the resource is used to securely retrieve authentication details from Azure AD without exposing any credentials.

## Managed Identity with Key Vault and Function Apps

Another approach is to configure your Function App to use a managed identity for accessing a Key Vault. The Function App obtains an access token from Azure AD, retrieves the connection string stored in the Key Vault, and uses it to connect securely to the SQL database.

### Infrastructure Deployment with PowerShell

The following PowerShell script deploys the infrastructure by creating a SQL server with a preloaded sample database (AdventureWorksLT), a Key Vault to securely store the connection string, and two Function Apps—one using a plain text connection string and the other using a managed identity:

```powershell theme={null}
# Create firewall rules
Write-Host "Configuring SQL server firewall" -ForegroundColor Green
$serverFirewallRule = New-AzSqlServerFirewallRule -ResourceGroupName $rg `
    -ServerName $serverName `
    -FirewallRuleName "AllowedIPs" -StartIpAddress $startIp -EndIpAddress $endIp
Write-Host "Created rule - $($serverFirewallRule.FirewallRuleName) for ($($server.ServerName))" -ForegroundColor Green

Write-Host "Creating database" -ForegroundColor Green
$database = New-AzSqlDatabase -ResourceGroupName $rg `
    -ServerName $serverName `
    -DatabaseName $databaseName `
    -Edition Basic `
    -SampleName "AdventureWorksLT"
Write-Host "Created database - $($database.DatabaseName) for ($($server.ServerName))" -ForegroundColor Green

$connectionString = "Server=tcp:$($serverName).database.windows.net,1433;Initial Catalog=$databaseName;Persist Security Info=False;User ID=$adminLogin;Password=$plainPassword;MultipleActiveResultSets=False"

# Key Vault creation
Write-Host "Creating Key Vault" -ForegroundColor Green
$kv = New-AzKeyVault -ResourceGroupName $rg `
    -Name $keyVaultName `
    -Location $location `
    -Sku Standard
Write-Host "Granting access policy to user to write connection string" -ForegroundColor Green
$AzKeyVaultAccessPolicy = New-AzKeyVaultAccessPolicy `
    -VaultName $kv.VaultName `
    -UserPrincipalName $signedInUser `
    -PermissionsToSecrets get,set,delete
Write-Host "Creating Key Vault secret" -ForegroundColor Green
New-AzKeyVaultSecret -VaultName $kv.VaultName -Name "sql" -SecretValue $secret

# Creating Function App
Write-Host "Creating Function App" -ForegroundColor Green
$storageAccount = New-AzStorageAccount -ResourceGroupName $rg -Name "stfn$(Get-Random)" -Location $location -SkuName "Standard_LRS" -AllowBlobPublicAccess $true
New-AzFunctionApp -ResourceGroupName $rg `
    -StorageAccount $storageAccount.StorageAccountName `
    -Location $location `
    -Runtime PowerShell `
    -Version 1.0 `
    -OsType Windows
```

### Function Code Samples

Below are two function examples—one with a plain text connection string, and the other using a managed identity to access Key Vault.

#### Function Using Plain Text Connection String

This function demonstrates the risk of using a hardcoded connection string:

```powershell theme={null}
# Input bindings are provided via the param block.
param('$Request', $TriggerMetadata)

# Connection string stored in plain text
$connectionString = "Server=tcp:sql-server-1668970856.database.windows.net,1433;Initial Catalog=db-adv-works;Persist Security Info=False;User ID=kodek"

# Create a SQL connection
$connection = New-Object System.Data.SqlClient.SqlConnection
$connection.ConnectionString = $connectionString

# Open the connection
$connection.Open()

# Create a SQL command to fetch table names
$command = $connection.CreateCommand()
$command.CommandText = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"

# Execute the command and fetch results
$reader = $command.ExecuteReader()
$tables = @()
while ($reader.Read()) {
    $tables += $reader["TABLE_NAME"]
}

# Close the connection
$connection.Close()

# Return table names as the response
$body = @{ tables = $tables } | ConvertTo-Json

Push-OutputBinding -Name Response -Value @{
    status = 200
    body = $body
}
```

#### Function Using Managed Identity to Access Key Vault

This function uses a system-assigned managed identity to request an access token. It then retrieves the connection string from Key Vault and connects to the SQL database:

```powershell theme={null}
# Input bindings are provided via the param block.
param($Request, $TriggerMetadata)
$keyVaultUrl = $env:AKV
$resourceUri = 'https://vault.azure.net'
$tokenAuthUri = $env:MSI_ENDPOINT + '?resource=' + $resourceUri + '&api-version=2017-09-01'
$tokenResponse = Invoke-RestMethod -Uri $tokenAuthUri -Headers @{ "Secret" = "$env:MSI_SECRET" } -Method GET
$token = $tokenResponse.access_token

$connectionString = (Invoke-RestMethod -Method GET -Headers @{ "Authorization" = "Bearer $token" } -Uri "$keyVaultUrl/secrets/sql?api-version=7.1").value

# Create a SQL connection
$connection = New-Object System.Data.SqlClient.SqlConnection
$connection.ConnectionString = $connectionString

# Open the connection
$connection.Open()

# Create a SQL command to fetch table names
$command = $connection.CreateCommand()
$command.CommandText = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"

# Execute the command and fetch results
$reader = $command.ExecuteReader()
$tables = @()
while ($reader.Read()) {
    $tables += $reader["TABLE_NAME"]
}

# Close the connection
$connection.Close()

# Return table names as the response
$body = @{ tables = $tables } | ConvertTo-Json

Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
    StatusCode = [System.Net.HttpStatusCode]::OK
    Body = $body
})
```

After configuring both functions, deploy the Function App. The deployment script creates the functions "GetDatabaseTables" (using a plain text connection string) and "GetDatabaseTablesMSI" (using managed identity):

```powershell theme={null}
Set-AzWebApp -ResourceGroupName $rg -Name $functionAppName -AppSettings $envVariables | Out-Null
Write-Host "Creating functions" -ForegroundColor Green
func new function --name "GetDatabaseTables" --template "HTTP trigger" --authLevel "function" --worker-runtime PowerShell
func new function --name "GetDatabaseTablesMSI" --template "HTTP trigger" --authLevel "function" --worker-runtime PowerShell
Set-Content -Path .\function\GetDatabaseTables\run.ps1 -Value $code
Set-Content -Path .\function\GetDatabaseTablesMSI\run.ps1 -Value $codeMsi
Write-Host "Publishing function" -ForegroundColor Green
func azure functionapp publish $functionAppName
```

Once deployed, you can review the created resources in the [Azure portal](https://portal.azure.com).

<Frame>
  ![The image illustrates the concept of Managed Identities, showing various source icons accessing a target that supports Azure AD authentication.](https://kodekloud.com/kk-media/image/upload/v1752881617/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-managed-identities/managed-identities-azure-ad-authentication.jpg)
</Frame>

## Overview of Managed Identities

Managed identities ensure that only Azure resources can authenticate using credentials stored in Azure AD. Since the source must be an Azure resource, on-premises solutions cannot directly use managed identities.

There are two types of managed identities:

* **System-assigned Managed Identity:** Tied directly to a single Azure resource, this identity is deleted if the resource is removed.
* **User-assigned Managed Identity:** A separate Azure resource that can be associated with multiple resources and remains even if one resource is deleted.

### Comparison of Managed Identity Types

| Feature       | System-assigned Managed Identity                                          | User-assigned Managed Identity                                        |
| ------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Alignment** | Identity of a single resource                                             | Standalone identity that can be shared                                |
| **Lifecycle** | Deleted with the resource                                                 | Remains even if associated resources are deleted                      |
| **Sharing**   | Not shareable                                                             | Can be mapped to multiple resources                                   |
| **Use Cases** | Ideal for individual workloads (e.g., a Function App accessing Key Vault) | Best for scenarios where multiple resources require a common identity |

<Frame>
  ![The image is a comparison table of system-assigned and user-assigned managed identities in Azure, highlighting differences in alignment, lifecycle, sharing, and use cases.](https://kodekloud.com/kk-media/image/upload/v1752881618/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-managed-identities/azure-managed-identities-comparison-table.jpg)
</Frame>

## Configuring Managed Identity in the Azure Portal

To enable a system-assigned managed identity for a Function App in the Azure portal:

1. Navigate to the Function App’s Configuration.
2. Under the Identity section, toggle the system-assigned managed identity to “On.”
3. Save the settings. The identity is now registered with Azure AD.

<Frame>
  ![The image shows the configuration settings page of a Microsoft Azure Function App, displaying application settings with options to view, edit, or delete them. The interface includes a sidebar with various settings and deployment options.](https://kodekloud.com/kk-media/image/upload/v1752881620/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-managed-identities/azure-function-app-settings-page.jpg)
</Frame>

For shared identity requirements across multiple functions, consider creating and assigning a user-assigned managed identity manually.

<Frame>
  ![The image shows a Microsoft Azure portal screen where a user is prompted to enable a system-assigned managed identity for a function app. The status toggle is set to "On."](https://kodekloud.com/kk-media/image/upload/v1752881620/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-managed-identities/azure-portal-managed-identity-toggle.jpg)
</Frame>

After enabling the managed identity, verify its status in the Identity section of the Function App:

<Frame>
  ![The image shows a Microsoft Azure portal interface, specifically the Identity section for a function app, with options for managing system-assigned identities.](https://kodekloud.com/kk-media/image/upload/v1752881621/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-managed-identities/azure-portal-identity-function-app.jpg)
</Frame>

## Testing the Functions

After deployment, navigate to your Function App in the Azure portal to test the functions:

* **Plain Text Function:**\
  This function returns a list of table names from the SQL database using a hardcoded connection string.

* **Managed Identity Function:**\
  This function leverages a managed identity to authenticate with Azure AD, retrieve the connection string from Key Vault, and connect securely to the SQL database. If you encounter an error, it may be due to missing permissions for the Function App’s managed identity in Key Vault.

<Callout icon="triangle-alert">
  Ensure you configure the Key Vault access policy to grant the Function App's managed identity permission to read secrets. Without this permission, the managed identity function will fail.
</Callout>

To add the required access policy:

1. In the Azure portal, navigate to the Key Vault's Access Policies.
2. Add an access policy that grants the Function App's managed identity permission to read secrets.
3. Save your changes.

<Frame>
  ![The image shows a Microsoft Azure portal interface displaying details of a Key Vault named "akv982393682," including its essentials, settings, and monitoring options.](https://kodekloud.com/kk-media/image/upload/v1752881623/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Enable-managed-identities/azure-portal-key-vault-akv982393682.jpg)
</Frame>

Once the access policy is properly configured, the managed identity function will retrieve the connection string from the Key Vault and display the SQL table names. A typical JSON response might look like:

```json theme={null}
{
  "tables": [
    "Customer",
    "ProductModel",
    "ProductDescription",
    "Product",
    "ProductModelProductDescription",
    "ProductCategory",
    "BuildVersion",
    "ErrorLog",
    "Address",
    "CustomerAddress",
    "SalesOrderDetail",
    "SalesOrderHeader"
  ]
}
```

Both functions return the same results, but the managed identity function does so without exposing sensitive credentials.

## Summary

Managed identities provide a secure way for Azure resources to authenticate with other resources via Azure AD. In this article, we explored two approaches:

* Using a plain text connection string (an insecure method)
* Using a system-assigned managed identity to retrieve secrets from Azure Key Vault

This approach is applicable not only to PowerShell but also to other languages like C#, Python, or Java, whether you are using an official SDK or making direct REST API calls.

Now, let’s move on to securing web applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500/module/c93091f0-246d-47cc-a399-0e33ad87ee7f/lesson/102c5454-b260-4ea5-bbdf-58b261e435f3" />
</CardGroup>


# Explore Azure AD application scenarios

Source: https://notes.kodekloud.com/docs/Microsoft-Azure-Security-Technologies-AZ-500/App-Security/Explore-Azure-AD-application-scenarios/page

This lesson explores various Azure Active Directory application scenarios and integration processes for different application types.

This lesson dives into several Azure Active Directory (Azure AD) application scenarios. Azure AD, now rebranded as Microsoft Entra ID, is Microsoft’s cloud-based identity and access management service. Although you might still see “Azure AD” mentioned throughout the portal and older documentation, the features and capabilities remain unchanged.

Azure AD offers a powerful platform for developers to integrate robust identity services into web, mobile, desktop, and other application types. Its flexible design supports a wide range of scenarios—from single-page applications (SPAs) running in a browser to automated background services operating without human intervention. In this lesson, we detail the key stages, including app registration, token validation, permission configuration, and more.

Below is a technical walkthrough on integrating Azure AD with various application types:

***

## Single-Page Applications (SPA)

For instance, consider a lightweight React application used as an internal company dashboard. A typical SPA integration workflow involves:

1. **App Registration and Kickstart**\
   Register the SPA with Azure AD and configure the authentication flows to get started.

2. **Authentication Flow Implementation**\
   Implement the OAuth2/OpenID Connect flow so that users can sign in and obtain tokens. These tokens are usually stored in local or session storage, with the storage strategy selected based on token expiration and security considerations.

3. **API Permissions**\
   Grant the SPA the necessary permissions to access APIs such as the Microsoft Graph API for retrieving user profile data for the dashboard.

***

## Web Applications

Consider a .NET Core web application designed for a cloud-based document management system. The process includes:

1. **Registration and Setup**\
   Register the web application in Azure AD and integrate with OpenID Connect middleware to support user sign-in.

2. **Token Validation**\
   Upon successful authentication, validate the received ID token to ensure its integrity.

3. **Secrets, Certificates, and API Permissions**
   * Secure any secrets and certificates using services like Azure Key Vault.
   * Configure API permissions (for instance, granting access to the SharePoint API).

4. **Access Control**\
   Implement role-based access control (RBAC) within the application to manage user privileges.

5. **Token Storage**\
   Cache tokens using session stores or distributed caches to enhance application scalability.

***

## Web APIs

For a RESTful API built with Node.js serving data to a mobile application, the Azure AD integration process is as follows:

1. **App Registration**\
   Register the API with Azure AD to ensure proper identification.

2. **Integration Code**\
   Use sample code from Azure documentation as a foundation for implementing token-based authentication.

3. **Access Token Validation**\
   Validate access tokens provided by API consumers before processing any data, ensuring only authorized requests are served.

4. **Secrets and Certificates**\
   Store required secrets securely (e.g., in Azure Key Vault) and configure necessary API permissions such as for Microsoft Graph API.

5. **Authorization**\
   Utilize RBAC or similar mechanisms to protect sensitive endpoints.

6. **Token Storage**\
   Cache validated tokens as needed for efficiency in subsequent requests.

***

## Background Processes and Automation (Daemons)

For background processes, such as a Python script scheduled to sync data between an on-premises and a cloud database, follow these integration steps:

1. **App Registration**\
   Begin by registering the background process with Azure AD.

2. **Authentication Configuration**\
   Configure your Python script using the appropriate authentication flow. Azure documentation provides sample code to simplify this setup.

3. **Secrets and Certificates Management**\
   Use Azure Key Vault or a similar solution to manage secrets and certificates securely.

4. **API Permissions**\
   Configure the necessary permissions to allow your process to access required APIs or databases.

5. **Token Storage**\
   Securely cache tokens and reuse them based on your scheduling and refresh logic.

***

## Mobile Applications

A mobile app—whether on iOS or Android—like an employee meeting room booking system, follows a comparable integration process:

1. **Registration and Kickstart**\
   Register the mobile application with Azure AD to establish its configuration.

2. **API Permissions Configuration**\
   Define API permissions for the mobile app to access services like the Microsoft Booking API or any custom internal API.

3. **Token Acquisition and Caching**\
   After authentication, acquire a token and cache it appropriately for future API calls.

***

## Desktop Console Applications

Desktop applications, such as a .NET Core console application for system administrators managing user roles, involve these steps:

1. **App Registration**\
   Register the desktop app in Azure AD to initiate its setup.

2. **Workflow Options**
   * **Silent Flow**: For domain-joined machines, implement a silent flow using Windows authentication or Kerberos for automatic token acquisition.
   * **Interactive Sign-In**: Alternatively, prompt the user for sign-in if silent authentication isn’t available.

3. **API Permissions and Token Handling**\
   Grant permissions (e.g., to Microsoft Graph API) and store the tokens securely for reuse.

***

## Overall Workflow and Diagram

Across all these application types, the common integration steps include:

1. App Registration
2. Code Configuration and Implementation
3. Token Validation
4. Secrets and Certificate Management
5. API Permissions and Access Control
6. Token Caching/Storage

<Callout icon="lightbulb">
  These standardized steps ensure a consistent authentication and authorization process across SPAs, web apps, web APIs, background processes, mobile apps, and desktop applications.
</Callout>

<Frame>
  ![The image is a flowchart illustrating different Azure AD application scenarios, detailing steps for building various types of apps such as Single-Page Apps, Web Apps, Web APIs, Background Processes, Mobile Apps, and Desktop Console Apps. Each scenario includes steps like app registration, configuration, and token management.](https://kodekloud.com/kk-media/image/upload/v1752881624/notes-assets/images/Microsoft-Azure-Security-Technologies-AZ-500-Explore-Azure-AD-application-scenarios/azure-ad-application-flowchart.jpg)
</Frame>

The diagram above shows the authentication workflow and outlines the multi-stage process required before deploying an application to production. Each module—from initial registration, through setting up security policies, testing, and finally, production deployment—follows a structured approach, with slight adaptations for different application types.

***

## Registering an Application

In every scenario, application registration is the first and most critical step. Up next, we will explore how to register an application with Azure AD (now Microsoft Entra ID). This essential process lays the foundation for configuring identity services, token management, and permissions.

<Callout icon="lightbulb">
  By following the steps outlined in this lesson, you'll build a strong foundation in integrating Azure AD across diverse application architectures, ensuring secure authentication and effective authorization.
</Callout>

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500/module/c93091f0-246d-47cc-a399-0e33ad87ee7f/lesson/b7952160-b0e1-4db5-9fb5-0d7f8e25543b" />
</CardGroup>
