# Dex Okta Connector

Source: https://notes.kodekloud.com/docs/GitOps-with-ArgoCD/ArgoCD-AdvancedAdmin/Dex-Okta-Connector/page

This article explains how to integrate DEX with Okta for authentication in ArgoCD using SAML.

In this article, we explain how ArgoCD leverages a DEX connector to delegate authentication to an external identity service such as Okta. ArgoCD includes DEX within its installation package, enabling seamless integration with third-party identity providers (IDPs) and enhancing your authentication strategy.

## Overview

DEX is an identity service that implements the OpenID Connect protocol to power authentication for various applications. When a user logs in via DEX, authentication is eventually validated by an external IDP. In essence, DEX acts as an intermediary between the client application (ArgoCD) and the external identity provider.

DEX supports a wide range of identity providers including Okta, Google, GitLab, GitHub, and OpenShift, as well as protocols such as SAML, OIDC, and LDAP. In this guide, we focus on configuring DEX to integrate with Okta using SAML.

## Configuring Okta for SAML

When using Okta, the following steps are required to set up a SAML application:

1. **Create a SAML Application in Okta:**\
   Provide the necessary configuration details in the Okta dashboard. For example, set the Single Sign-On (SSO) URL to your ArgoCD server URL with the `/api/dex/callback` suffix.

2. **Assign Application Access:**\
   Assign the SAML application to specific users or groups within Okta. In our example, the application is assigned to a user named Kiatim. All user and group management is handled by Okta.

3. **Obtain Integration Details:**\
   After configuration, Okta supplies an SSO URL along with an X.509 certificate. These values must be added to the ArgoCD ConfigMap to complete the integration with DEX.

> **lightbulb** By default, users authenticating via Okta do not have permission to make changes within ArgoCD. To allow full operations, you must update the ArgoCD RBAC configuration.

## Updating the ArgoCD Configuration

To integrate DEX with Okta, update the ArgoCD ConfigMap with the necessary connector configuration. Use the following command and configuration snippet:

```bash theme={null}
$ kubectl -n argocd edit configmap argocd-cm
...
dex.config: |
  connectors:
    - type: saml
      id: Okta
      name: Okta
      config:
        ssoURL: <okta-idp-sso-url>
        caData: <base64encoded X.509 Certificate>
        usernameAttr: name
        emailAttr: email
        groupsAttr: groups
```

This configuration informs ArgoCD’s embedded DEX where to find your Okta instance and provides the necessary details to complete SAML authentication.

## Updating RBAC for Okta Users

After updating the DEX configuration, refresh the ArgoCD UI. You should now see a new "Login via Okta" button on the login page. To grant authenticated Okta users the permissions required to modify applications, update the ArgoCD RBAC configuration using the following steps:

```bash theme={null}
$ kubectl -n argocd edit configmap argocd-rbac-cm
...
data:
  policy.csv: |
    p, role:crudApps, applications, *, kia-project/*, allow
    g, kia-team, role:crudApps
...
configmap/argocd-rbac-cm edited
```

In the RBAC policy above, notice that we have referenced a group named "kia-team" defined in Okta. This policy applies to all users within that group, granting them full permissions to perform operations on applications within the specified ArgoCD Kubernetes project.

> **triangle-alert** Ensure that the RBAC policies are correctly configured to avoid granting excessive permissions. Regularly review your RBAC settings to maintain a secure environment.

## Summary

By integrating DEX with an Okta SAML application, ArgoCD can seamlessly delegate authentication to an external IDP, streamlining user access management. Make sure to update both the DEX configuration and the RBAC policies to fully enable Okta authentication and provide the necessary permissions to your users.

For further reading, consider visiting the following resources:

* [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
* [Okta Developer Documentation](https://developer.okta.com/)
* [OpenID Connect Explained](https://openid.net/connect/)

Happy configuring!

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-argocd/module/ef6b6fef-0bd5-4fab-b437-b6d613fa74b4/lesson/b29644ee-7de2-4200-ae4c-86b7cdc9fa7b)
