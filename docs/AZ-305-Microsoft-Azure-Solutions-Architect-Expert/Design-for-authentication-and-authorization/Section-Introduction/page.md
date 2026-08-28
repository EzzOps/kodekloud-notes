# Establish a connection using ActiveDirectoryMsi authentication.
_conn = pyodbc.connect(connection_string + ";Authentication=ActiveDirectoryMsi")

# Assume 'exptoken' is a byte string containing the access token obtained from Azure AD.
# The following constructs the token structure required by pyodbc.
tokenstruct = struct.pack("=I", len(exptoken)) + exptoken

# Create a connection using the token
conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: tokenstruct})

with conn.cursor() as cursor:
    cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
    row = cursor.fetchone()
    while row:
        print(row[0], row[1])
        row = cursor.fetchone()
```

By using managed identity authentication, there is no need to hard-code a username or password. Instead, Azure AD returns a token for the managed identity, ensuring secure and streamlined access to your SQL database or any other service that supports Azure AD authentication.

## Use Cases for Managed Identities

Managed identities can be used in various scenarios where secure resource authentication is required. They are supported by several Azure resources, including:

* Virtual Machines
* Web Apps
* Azure Kubernetes Service (AKS)
* Function Apps
* Load Balancers

<Callout icon="lightbulb">
  Managed identities are only available for resources deployed in Azure. They cannot be used with on-premises applications.
</Callout>

Using managed identities eliminates the need for constant credential rotations or certificate management, as the identity is maintained automatically by Azure AD. This significantly enhances the security and manageability of your applications.

## Types of Managed Identities

There are two types of managed identities in Azure:

1. **System-Assigned Managed Identity:**\
   This identity is automatically created for an Azure resource (e.g., a virtual machine). The identity's lifecycle is tied to the resource; if the resource is deleted, the identity is also removed.

2. **User-Assigned Managed Identity:**\
   This is a standalone identity resource that you create in Azure. It can be assigned to multiple Azure resources, making it ideal for scenarios where different instances of your application require a common identity.

Below is a diagram comparing the two types of managed identities:

<Frame>
  ![The image is a comparison table of system-assigned and user-assigned managed identities in Azure, detailing their alignment, lifecycle, sharing capabilities, and use cases.](https://kodekloud.com/kk-media/image/upload/v1752867242/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-managed-identities/azure-managed-identities-comparison-table.jpg)
</Frame>

### Key Differences Between Managed Identity Types

* **Lifecycle:**\
  • System-assigned identities are deleted automatically with their resource.\
  • User-assigned identities exist independently of the resources that use them.

* **Sharing:**\
  • System-assigned identities are dedicated to a single resource (one-to-one relationship).\
  • User-assigned identities can be shared across multiple resources.

* **Use Cases:**\
  • Choose system-assigned identities for workloads confined to a single resource.\
  • Choose user-assigned identities when multiple resources require a shared identity.

Demo scenarios include a virtual machine connecting to a database, a web app accessing data, or an application gateway retrieving an SSL certificate from Key Vault. In each case, managed identities offer a secure and maintainable method of authentication.

## Integration with Azure Key Vault

Next, we explore how Azure Key Vault integrates with managed identities to further enhance your security management by providing secure storage and access to certificates, secrets, and keys.

For more information on Azure AD and role-based access control, please visit the following resources:

* [Azure Active Directory Documentation](https://docs.microsoft.com/en-us/azure/active-directory/)
* [Azure Key Vault Documentation](https://docs.microsoft.com/en-us/azure/key-vault/)

By leveraging managed identities and Azure AD, you can significantly reduce the risk associated with credential management, ensuring your applications remain secure and compliant with modern security standards.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-305-microsoft-azure-solutions-architect-expert/module/37d1f5fb-99a1-4513-a856-4587651d9a60/lesson/fbc8aaa4-4728-495b-bf78-deed5a6c43df" />
</CardGroup>


# Section Introduction

Source: https://notes.kodekloud.com/docs/AZ-305-Microsoft-Azure-Solutions-Architect-Expert/Design-for-authentication-and-authorization/Section-Introduction/page

This lesson discusses design requirements for authentication and authorization in applications, focusing on Azure AD and identity management solutions for a real-world customer scenario.

In this lesson, we begin by discussing the key design requirements for authentication and authorization in modern applications. Our discussion will cover essential components such as Azure AD, Azure AD B2B, Azure AD B2C, and Conditional Access. We will also explore identity governance, access reviews, managed identities, and their application in securing access to KeyVault.

Given that the [AZ-305: Microsoft Azure Solutions Architect Expert](https://learn.kodekloud.com/user/courses/az-305-microsoft-azure-solutions-architect-expert) exam emphasizes solution design, this lesson is structured around a real-world customer scenario.

<Callout icon="lightbulb">
  Vendata Corp plans to leverage Azure AD for their identity and access management needs. Their solution requirements are as follows:

  * Collaborate with external partners without managing individual usernames and passwords.
  * Allow application users to access their e-commerce website using Apple, Google, and Microsoft email accounts.
  * Restrict access to corporate applications to the specific IP range 52.11.11.0/27.
  * Enforce multi-factor authentication for users accessing corporate applications from external networks.
  * Mitigate risks associated with leaked passwords and compromised accounts.
  * Provide administrators with a weekly report of role assignments to verify and review access rights.
  * Manage several HTTPS applications requiring secure storage of SSL certificates.
  * Securely store credentials for multiple application users who rely on an SQL backend, thus eliminating the need to hardcode encrypted credentials.
</Callout>

<Frame>
  ![The image is a scenario description from KodeKloud for Vendetta Corp, detailing requirements for using Azure AD as their identity and access management solution, including collaboration, app access, network restrictions, and security measures.](https://kodekloud.com/kk-media/image/upload/v1752867243/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Section-Introduction/azure-ad-vendetta-corp-scenario.jpg)
</Frame>

With these requirements clearly defined, we now proceed to the first section of this module, which focuses on identity and access management. Explore how to architect a secure and scalable solution that meets modern enterprise needs while maintaining compliance with industry standards.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-305-microsoft-azure-solutions-architect-expert/module/37d1f5fb-99a1-4513-a856-4587651d9a60/lesson/f5063197-aec3-488d-8b09-06308f48bd9d" />
</CardGroup>
