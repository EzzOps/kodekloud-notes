# Authentication

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Security/Authentication/page

Overview of Kubernetes authentication methods for kube-apiserver, covering legacy static files, TLS client certificates, external identity providers, service accounts, and operational recommendations.

Welcome to this lesson on authentication in a Kubernetes cluster. Kubernetes clusters run on multiple nodes (physical or virtual) and include components that coordinate access to the control plane and workloads. Several types of principals interact with the cluster:

* Administrators who perform cluster-level operations.
* Developers who deploy and iterate on applications.
* End users who access applications (application-level auth is handled by the apps themselves and is out of scope here).
* Robots (processes, controllers, CI systems, and third-party services) that call the Kubernetes API programmatically.

<Frame>
  <img alt="A stylized system diagram showing a series of connected modules/cards linked by nodes and padlock icons to indicate protected stages. Icons for &#x22;Admins&#x22; and &#x22;Developers&#x22; appear on the left and &#x22;End Users&#x22; and &#x22;Bots&#x22; on the right." />
</Frame>

This lesson focuses on securing administrative access to the kube-apiserver — the central API endpoint that authenticates and authorizes all requests to the control plane. That includes access performed by humans (admins, developers) and machines (controllers, CI systems, operators).

Kubernetes does not manage regular user accounts natively: you cannot create or list standard user objects with kubectl. User identities are typically introduced to the cluster through external mechanisms, such as:

* static files (legacy),
* TLS client certificates,
* or an external identity provider (OIDC, LDAP, Kerberos, SAML, etc).

Service accounts, on the other hand, are a Kubernetes resource and are created/managed via the API. Example:

```bash theme={null}
