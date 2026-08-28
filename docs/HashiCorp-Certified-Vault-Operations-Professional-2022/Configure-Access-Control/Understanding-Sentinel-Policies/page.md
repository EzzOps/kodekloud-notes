# Understanding Sentinel Policies

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Configure-Access-Control/Understanding-Sentinel-Policies/page

This article explains Sentinel, HashiCorps policy-as-code framework for Vault, detailing its features, policy types, and creation process.

Sentinel is HashiCorp’s embedded policy-as-code framework, built directly into the Vault binary. It provides fine-grained, logic-based policy evaluation to permit or deny access to Vault paths and secrets based on dynamic conditions and external data.

With Sentinel you can:

* Treat policies like application code (version control, PR reviews, automated testing, CI/CD)
* Define condition-based rules (time, IP address, request path, MFA status, etc.)
* Pull in external data (current time, client IPs, request details)
* Enforce policies at three levels: advisory, soft mandatory, and hard mandatory
* Reuse the same policies across Terraform, Nomad, Vault, and Consul (enterprise editions)

<Callout icon="lightbulb">
  Sentinel is embedded in the Vault binary. No additional services or agents are required.
</Callout>

<Frame>
  ![The image is an infographic describing features of a policy management system, including "Policy as Code," "Fine Grained, Conditioned-Based," "Embedded," "Enforcement Levels," "External Information," and "Multi-Cloud Compatible." It uses icons and brief descriptions to explain each feature.](https://kodekloud.com/kk-media/image/upload/v1752878340/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Understanding-Sentinel-Policies/policy-management-system-infographic-features.jpg)
</Frame>

***

## Sentinel Across HashiCorp Enterprise Products

Sentinel isn’t limited to Vault. It’s part of HashiCorp’s enterprise offerings for:

* Terraform
* Nomad
* Vault
* Consul

Once you author a Sentinel policy, you can apply it across these platforms with minimal changes.

<Frame>
  ![The image highlights that Sentinel is not just a Vault feature and is available in the Enterprise versions of HashiCorp products like Terraform, Nomad, Vault, and Consul. It also features a Vault certification badge and a cartoon character at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878341/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Understanding-Sentinel-Policies/sentinel-enterprise-hashi-corp-products.jpg)
</Frame>

***

## Types of Sentinel Policies

Vault supports two main policy types:

|                         Policy Type | Scope                                     | Purpose                                                          |
| ----------------------------------: | ----------------------------------------- | ---------------------------------------------------------------- |
|     **Role Governing Policy (RGP)** | Tokens, identity entities, and groups     | Govern actions identities can perform based on role logic        |
| **Endpoint Governing Policy (EGP)** | Specific API paths (authenticated or not) | Enforce conditions (source IP, business hours, MFA) per endpoint |

<Frame>
  ![The image describes two types of Sentinel policies: Role Governing Policies (RGPs) tied to tokens and identity entities, and Endpoint Governing Policies (EGPs) tied to paths. It highlights their access controls and effects.](https://kodekloud.com/kk-media/image/upload/v1752878342/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Understanding-Sentinel-Policies/sentinel-policies-rgps-egps-access-controls.jpg)
</Frame>

*Example:* An EGP on `/dev/data` could deny all access outside business hours, regardless of token validity.

***

## Anatomy of a Sentinel Policy

Every Sentinel policy consists of:

1. **Imports**: Standard libraries—`base64`, `decimal`, `http`, `json`, `sockaddr`, `time`, `mfa`, etc.
2. **Variables & helper rules**: Reusable rule definitions.
3. **main rule**: The required entry point. Returns `true` to allow or `false` to deny.

Basic template:

```sentinel theme={null}
import "<library>"

helper_rule = rule {
  <condition>
}

main = rule {
  <condition>
}
```

<Frame>
  ![The image lists examples of imports that can be used with Sentinel, such as base64, decimal, http, json, and others, each with a brief description of their functions. It also includes a note about fine-grained controls over a Vault environment.](https://kodekloud.com/kk-media/image/upload/v1752878344/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Understanding-Sentinel-Policies/sentinel-imports-examples-functions-controls.jpg)
</Frame>

### Common Sentinel Imports

* `base64` – Encode/decode Base64 strings
* `decimal` – High-precision decimal arithmetic
* `http` – Perform HTTP requests within policies
* `json` – Parse and manipulate JSON data
* `sockaddr` – Handle IP addresses and CIDR blocks
* `time` – Load, compare, and parse timestamps
* `mfa` – Access the results of MFA methods
* `strings` – String manipulation functions

***

## Example RGP: Allow Specific Identities

This RGP grants access only to identities named “jeff” or members of the “sysops” group:

```sentinel theme={null}
main = rule {
  identity.entity.name is "jeff" or
  identity.entity.id is "fe2a5bfd-c483-9263-b0d4-f9d345efdf9f" or
  "sysops" in identity.groups.names or
  "14c0940a-5c07-4b97-81ec-0d423accb8e0" in keys(identity.groups.by-id)
}
```

Using the entity ID prevents bypass by deleting and recreating the user.

***

## Example EGP 1: Revoke Old Tokens

Apply to all paths (`*`) to deny tokens issued before a cutoff timestamp:

```sentinel theme={null}
import "time"

main = rule when not request.unauthenticated {
  time.parse(request.auth.token.creation_time).unix >
  time.parse("2022-12-25T00:00:01Z").unix
}
```

* `when not request.unauthenticated` ensures this only applies to authenticated requests.
* Denies any token created before **December 25, 2022**.

***

## Example EGP 2: LDAP Login with MFA and IP Check

This policy requires both an IP CIDR check and a Ping MFA challenge on `auth/ldap/login`:

```sentinel theme={null}
import "sockaddr"
import "mfa"
