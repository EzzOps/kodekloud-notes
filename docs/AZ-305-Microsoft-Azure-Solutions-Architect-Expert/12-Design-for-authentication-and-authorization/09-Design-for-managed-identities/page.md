# Get token from Azure AD using client credentials
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("Content-Type", "application/x-www-form-urlencoded")
$body = "grant_type=client_credentials&client_id=<your-client-id>&client_secret=<your-client-secret>&resource=https://vault.azure.net/"
$tenantId = "<your-tenant-id>"
$url = "https://login.microsoftonline.com/$tenantId/oauth2/token"
$output = Invoke-RestMethod -Uri $url -Body $body -Method POST -Headers $headers
$accessToken = $output.access_token

# Access a secret from Azure Key Vault
$secretId = "https://yourkeyvaultname.vault.azure.net/secrets/your-secret-name?api-version=7.3"
$akvHeaders = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$akvHeaders.Add("Authorization", "Bearer $accessToken")
$secret = Invoke-RestMethod -Uri $secretId -Method GET -Headers $akvHeaders
$secret.value
```

When executed (for example, within an Automation Account runbook), this script retrieves and prints the secret value from Key Vault.

> **triangle-alert** Avoid hardcoding any credentials in your scripts. Instead, consider using managed identities to eliminate the risk of exposing sensitive information.

***

## Securing Access with Managed Identity

To enhance security and eliminate embedded credentials, you can enable a Managed Identity for your Automation Account. Managed Identity provides your application with a secure mechanism to acquire tokens without managing client IDs or secrets manually.

### Enabling Managed Identity

1. In your Automation Account within the Azure Portal, navigate to the **Identity** section.
2. Enable the system-assigned managed identity.
3. Once the identity is enabled, note its object ID. Use this ID to grant access in Key Vault by creating a dedicated access policy.

![The image shows a Microsoft Azure portal page for managing a system-assigned managed identity within an automation account. The status is set to "On," and a notification confirms successful registration with Azure Active Directory.](https://kodekloud.com/kk-media/image/upload/v1752867241/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-keyvault/azure-portal-managed-identity-status.jpg)

### Using Managed Identity with PowerShell

Below is an example PowerShell script demonstrating how to use Managed Identity to retrieve an access token and then access a secret from Key Vault without explicitly handling credentials.

```powershell theme={null}
# Get token from Managed Identity Service (MSI)
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$resource = "resource=https://vault.azure.net"
# The environment variable IDENTITY_HEADER contains the MSI endpoint URL
$url = $env:IDENTITY_HEADER + $resource
$headers.Add("X-IDENTITY-HEADER", $env:IDENTITY_HEADER)
$headers.Add("Metadata", "True")
$tokenResponse = Invoke-RestMethod -Uri $url -Method GET -Headers $headers
$accessToken = $tokenResponse.access_token

# Access the Key Vault secret using the MSI token
$secretId = "https://yourkeyvaultname.vault.azure.net/secrets/your-secret-name?api-version=7.3"
$akvHeaders = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$akvHeaders.Add("Authorization", "Bearer $accessToken")
$secret = Invoke-RestMethod -Uri $secretId -Method GET -Headers $akvHeaders
$secret.value
```

After updating Key Vault access policies to include your Automation Account’s managed identity, this script should successfully return the secret value without storing any credentials in your code.

***

## Final Remarks

By combining managed identities with Azure Key Vault, you can eliminate hard-coded credentials in your automation scripts and significantly improve your application’s secret management security. This guide has walked you through setting up Key Vault, configuring access policies, and building PowerShell scripts to retrieve secrets—first using client credentials and then leveraging a managed identity.

Evaluate these approaches carefully to meet your specific security and performance requirements as you build and secure your Azure environment.

Happy coding!

- [Watch Video](https://learn.kodekloud.com/user/courses/az-305-microsoft-azure-solutions-architect-expert/module/37d1f5fb-99a1-4513-a856-4587651d9a60/lesson/7832c1b7-34bb-4762-9eee-85aa25636261)


# Design for managed identities

Source: https://notes.kodekloud.com/docs/AZ-305-Microsoft-Azure-Solutions-Architect-Expert/Design-for-authentication-and-authorization/Design-for-managed-identities/page

This guide explains managed identities for Azure resources, demonstrating secure authentication methods without embedding credentials in code.

Managed identities provide a secure and efficient way for your Azure resources to authenticate with Azure Active Directory (Azure AD) and access other services without embedding credentials in your code. This guide explains how managed identities work and demonstrates connecting to an Azure SQL Database using both traditional credential-based authentication and managed identity authentication.

## Traditional Credential-Based Authentication

In a traditional setup, a Python web application running on Azure connects to an SQL Database using a username and password stored within the code. While this method may work, it exposes sensitive credentials that could be compromised if the code is accidentally pushed to a public repository.

```python theme={null}
import pyodbc

server = "mykodekloud.database.windows.net"
database = "products"
username = "dbadmin"
password = "VeryStrongPassword#889"
driver = "{ODBC Driver 17 for SQL Server}"

with pyodbc.connect(
    "DRIVER=" + driver +
    ";SERVER=tcp:" + server +
    ";PORT=1433;" +
    "DATABASE=" + database +
    ";UID=" + username +
    ";PWD=" + password
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchone()
        while row:
            print(str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()
```

> **triangle-alert** Storing clear-text credentials in your code is risky. If the repository is ever breached, sensitive information can be easily stolen.

## Managed Identity Authentication

Managed identities remove the need to store credentials in your code. Instead, your Azure resource is granted an identity in Azure AD, which can then obtain an authentication token to access services such as Azure SQL Database.

The following example demonstrates how to connect to an Azure SQL Database using a managed identity. Notice that the connection string uses Active Directory MSI (Managed Service Identity) and obtains a token from Azure AD for secure authentication.

```python theme={null}
import pyodbc
import struct

server = "mykodekloud.database.windows.net"
database = "products"
driver = "{ODBC Driver 17 for SQL Server}"
connection_string = (
    "DRIVER=" + driver +
    ";SERVER=" + server +
    ";DATABASE=" + database
)
