# Register an application with App Registration

Source: https://notes.kodekloud.com/docs/Microsoft-Azure-Security-Technologies-AZ-500/App-Security/Register-an-application-with-App-Registration/page

Guide to registering applications in Microsoft Entra ID and obtaining access tokens using the OAuth2 client credentials flow.

Registering an application in Microsoft Entra ID (formerly Azure AD) is the essential first step for enabling authentication and authorization with Microsoft Identity Services. An app registration tells Entra ID that your application intends to use Microsoft identity and gives the app a unique Application (client) ID, credentials, and configuration used during authentication flows.

Why register an application? Core benefits:

* Centralized application management in Microsoft Entra ID.
* Secure user authentication using Entra ID authentication mechanisms.
* Fine-grained authorization via scopes and permissions.
* Integration with Azure services (Key Vault, Blob Storage, SQL, etc.).
* App-to-app authentication using client credentials (client secret or certificate).
* Cross-platform SDKs and developer tooling.
* Global scale and industry-standard security for authentication tokens.

<Frame>
  <img alt="A presentation slide titled &#x22;Register an Application With App Registration&#x22; showing a vertical row of colorful feature buttons (e.g., Centralized Application Management, Secure User Authentication) on the left. On the right is a rounded screenshot of the Microsoft identity/app registration portal with app details and a &#x22;Build your application with the Microsoft identity&#x22; section." />
</Frame>

Since app registrations are stored in Microsoft Entra ID, they inherit Entra ID's security, policy, and scalability capabilities.

This guide walks through the Azure portal steps to create an app registration and then requests an access token using the client credentials flow. The same registration details (client\_id, client\_secret/certificate, tenant) are used to authenticate and request tokens from the Microsoft Identity Platform.

Getting started: open the Azure portal and navigate to Microsoft Entra ID (the new name for Azure Active Directory).

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the Home dashboard with a left navigation menu open, service icons across the top, and a list of recent resources and their types in the main pane. The highlighted item is &#x22;Microsoft Entra ID&#x22; in the left menu." />
</Frame>

In the Microsoft Entra ID blade, open App registrations to create a new app.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal open to the &#x22;App registrations&#x22; page for a Kodekloud tenant. The left-hand navigation menu is visible and a banner about deprecation of ADAL/MSAL appears near the top." />
</Frame>

Click New registration, supply a Name (in this lesson we use "app-sec-reg"), and choose the Supported account types. Optionally add a Redirect URI for interactive web flows. For simple service-to-service (non-interactive) scenarios, Redirect URI is not required.

Account type guidance:

| Supported account type                                         | Use case                                  | When to choose                                         |
| -------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------ |
| Accounts in this organizational directory only (single tenant) | Internal apps used only within one tenant | Use for internal business apps                         |
| Accounts in any organizational directory (multi-tenant)        | Apps used by multiple organizations       | Use for B2B or ISV apps                                |
| Accounts in any org and personal Microsoft accounts            | Broad consumer + org access               | Use for apps targeting both work and personal accounts |
| Personal Microsoft accounts only                               | Consumer-only apps                        | Use for single-user consumer apps                      |

<Frame>
  <img alt="A screenshot of the Microsoft Azure &#x22;Register an application&#x22; page showing fields to create an app (Name, Supported account types, Redirect URI), with &#x22;app-sec-reg&#x22; entered and the single-tenant option selected. The page includes the Register button at the bottom." />
</Frame>

After clicking Register, the portal shows the app registration details. Copy the Application (client) ID and Directory (tenant) ID — you will use the client\_id (and tenant) when requesting tokens.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the App registrations page for an application named &#x22;app-sec-reg,&#x22; including its application/client ID, object and tenant IDs, and left-hand navigation options. A notification in the top-right confirms the app was successfully created." />
</Frame>

You can view endpoints for the Microsoft identity platform (authorize endpoints, token endpoints, OpenID configuration, etc.). For client credentials flows you will call the token endpoint.

Example endpoints (replace the tenant ID with your tenant ID):

```text theme={null}
OAuth 2.0 authorization endpoint (v2)
https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/oauth2/v2.0/authorize

OAuth 2.0 token endpoint (v2)
https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/oauth2/v2.0/token

OAuth 2.0 authorization endpoint (v1)
https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/oauth2/authorize

OAuth 2.0 token endpoint (v1)
https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/oauth2/token

OpenID Connect metadata document
https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/v2.0/.well-known/openid-configuration

Microsoft Graph API endpoint
https://graph.microsoft.com

Federation metadata document
https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/federationmetadata/2007-06/federationmetadata.xml

WS-Federation sign-on endpoint
https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/wsfed

SAML-P sign-on endpoint
https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/saml2

SAML-P sign-out endpoint
https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/saml2
```

For this tutorial we will request an access token from the v2 token endpoint.

Next: create credentials for the application. For production use, a certificate is recommended. For quick testing you can create a client secret in Certificates & secrets.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;app-sec-reg | Certificates & secrets&#x22; page for an app registration, with one client secret listed. A toast notification in the corner indicates the application credentials were successfully updated." />
</Frame>

<Callout icon="lightbulb">
  After adding a client secret, copy its value immediately. You cannot retrieve the secret value later from the portal — if you lose it you must create a new secret.
</Callout>

Requesting a token (client credentials grant)

* Use grant\_type=client\_credentials for app-to-app (no user) authentication.
* For Microsoft Graph requests, use the scope value [https://graph.microsoft.com/.default](https://graph.microsoft.com/.default) to request the app's configured application permissions.

HTTP POST example (application/x-www-form-urlencoded) to the v2 token endpoint:

```http theme={null}
POST https://login.microsoftonline.com/1e0fa212-37dc-45f5-bb0f-b60687cac64b/oauth2/v2.0/token
Content-Type: application/x-www-form-urlencoded

client_id=5a683b67-8a0d-4834-8a45-fb8167003e2d
&client_secret=xWNBQ~7_W_xiJ0iWtGQYGcGctwgCxW83mV0enbLG
&grant_type=client_credentials
&scope=https://graph.microsoft.com/.default
```

(If using Postman: select Body → x-www-form-urlencoded and enter the key/value pairs, or use Bulk Edit to paste them.)

A successful response returns a JSON payload containing an access token:

```json theme={null}
{
  "token_type": "Bearer",
  "expires_in": 3599,
  "ext_expires_in": 3599,
  "access_token": "[SECRET_REDACTED]..."
}
```

Understanding and validating the token

* The access\_token is a JWT. You can inspect it (for example at [https://jwt.ms](https://jwt.ms)) to view header and payload claims.
* Typical claims include:
  * aud (audience): the resource the token is intended for (e.g., [https://graph.microsoft.com](https://graph.microsoft.com)).
  * iss (issuer): the token issuer (tenant-specific).
  * appid or azp: your application's client ID.
  * tid: tenant ID.
  * exp, iat: expiry and issued-at timestamps.

Sample decoded header:

```json theme={null}
{
  "typ": "JWT",
  "alg": "RS256",
  "x5t": "-KI3Q9nNR7bRofxmeZoXqbHZGew",
  "kid": "-KI3Q9nNR7bRofxmeZoXqbHZGew"
}
```

Sample decoded payload for an app token (abridged):

```json theme={null}
{
  "aud": "https://graph.microsoft.com",
  "iss": "https://sts.windows.net/1e0fa212-37dc-45f5-bb0f-b60687cac64b/",
  "iat": 1696666347,
  "nbf": 1696666347,
  "exp": 1696670247,
  "app_displayname": "app-sec-reg",
  "appid": "5a683b67-8a0d-4834-8a45-fb8167003e2d",
  "idtyp": "app",
  "tid": "1e0fa212-37dc-45f5-bb0f-b60687cac64b"
}
```

Token validation checklist (when your API receives a token):

* Verify the token signature using the issuer's public keys (from OpenID configuration).
* Verify the issuer (iss) matches expected issuer for the tenant.
* Verify the audience (aud) matches your API or Microsoft Graph.
* Verify token expiry (exp) and not-before (nbf).
* Verify required claims (appid, scopes/roles) are present.

How the token is issued

* The Microsoft Identity Platform issues tokens after authenticating the client (by client secret or certificate) and validating requested scopes/permissions. Your app then presents the token to APIs (Microsoft Graph or other resource APIs) to authenticate and authorize requests.

Calling Microsoft Graph with the token

1. Acquire the access\_token as shown above.
2. Add Authorization: Bearer \<access\_token> header to your HTTP requests.
3. Call Graph endpoints, for example:

GET [https://graph.microsoft.com/v1.0/users](https://graph.microsoft.com/v1.0/users)

Ensure your app registration has the appropriate application permissions in the Azure portal and that an admin has granted consent where required.

Further reading and references

* Microsoft Identity Platform documentation: [https://learn.microsoft.com/azure/active-directory/develop/](https://learn.microsoft.com/azure/active-directory/develop/)
* App registrations overview: [https://learn.microsoft.com/azure/active-directory/develop/app-objects-and-service-principals](https://learn.microsoft.com/azure/active-directory/develop/app-objects-and-service-principals)
* OAuth 2.0 client credentials flow: [https://learn.microsoft.com/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow](https://learn.microsoft.com/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow)
* Microsoft Graph docs: [https://learn.microsoft.com/graph/overview](https://learn.microsoft.com/graph/overview)

This completes the app registration and token issuance overview. Next, you can use the access token to call Microsoft Graph or other protected APIs and learn how to validate tokens in your application code.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/microsoft-azure-security-technologies-az-500/module/c93091f0-246d-47cc-a399-0e33ad87ee7f/lesson/3746d8ca-434f-4383-86d9-954ef1dbb6a3" />
</CardGroup>
