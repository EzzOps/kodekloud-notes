# Enable managed identities

Source: https://notes.kodekloud.com/docs/Microsoft-Azure-Security-Technologies-AZ-500/App-Security/Enable-managed-identities/page

Learn to enable managed identities for secure SQL database connections without exposing credentials in plain text.

In this article, you will learn how to enable managed identities to securely connect to a SQL database without exposing credentials in plain text. Managed identities allow an Azure resource (such as a Function App) to authenticate with Azure Active Directory (Azure AD) and access other resources that support Azure AD authentication.

<Callout icon="lightbulb">
  Avoid hardcoding credentials in your source code. Instead, leverage managed identities to improve your security posture.
</Callout>

## Using Plain Text Credentials

Initially, consider a Python script that connects to a SQL database by hardcoding the username and password. Hardcoding credentials is a major vulnerability since anyone with access to the code can see the sensitive data.

```python theme={null}
import pyodbc

server = 'mykodekloud.database.windows.net'
database = 'products'
username = 'dbAdmin'
password = 'VeryStrongPassword#889'
driver = '{ODBC Driver 17 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchone()
        while row:
            print(str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()
```

Using this method exposes your database to unauthorized access. While storing the connection string in [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/) is an option, a more secure alternative is to utilize managed identities.

## Using Managed Identity for Azure AD Authentication

Managed identities enable your code to authenticate with Azure AD by obtaining a token. Azure SQL Database then uses this token for authentication without the need for a username and password. The following Python example shows the modifications needed to use Azure AD authentication via a managed identity:

```python theme={null}
import pyodbc
import struct

server = 'mykodekloud.database.windows.net'
database = 'products'
driver = '{ODBC Driver 17 for SQL Server}'
connection_string = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+database
