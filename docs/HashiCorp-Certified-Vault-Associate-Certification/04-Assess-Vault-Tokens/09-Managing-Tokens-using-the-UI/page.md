# Renew by token ID
vault token renew s.12VNpg4OA9tTdCd4V60DuDRK

# Renew by accessor
vault token renew -accessor lMIaz4Tn1t57wKXdsfNv7vlm
```

Renewal output confirms the new TTL and policies:

```text theme={null}
Key             Value
---             -----
token           s.12VNpg4OA9tTdCd4V60DuDRK
token_duration  5m
renewable       true
policies        ["default" "training"]
```

***

## 4. Revoking a Token

To immediately invalidate a token, use:

```bash theme={null}
vault token revoke <token-or-accessor>
```

Example:

```bash theme={null}
vault token revoke s.12VNpg4OA9tTdCd4V60DuDRK
```

<Callout icon="triangle-alert">
  Revoking a token is irreversible. Any sessions or processes using that token will lose access immediately.
</Callout>

***

## 5. Checking Token Capabilities

Determine which operations a token can perform on a specific path:

```bash theme={null}
vault token capabilities <token> <path>
```

Example:

```bash theme={null}
vault token capabilities s.dhtIk8VsE3Mj61PuGP3ZfFrg kv/data/apps/webapp
```

Output:

```text theme={null}
create, list, read, sudo, update
```

This helps you audit and verify permissions for service accounts or automation tools.

***

## 6. References

* [Vault CLI Reference](https://www.vaultproject.io/docs/commands)
* [Authentication Methods](https://www.vaultproject.io/docs/auth)
* [Vault Token Authentication](https://www.vaultproject.io/docs/concepts/tokens)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/ffb53470-4115-4c47-aade-cb572b6b574f/lesson/b2c77d39-3dea-4fce-986c-393f8df33b0a" />
</CardGroup>


# Managing Tokens using the UI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Assess-Vault-Tokens/Managing-Tokens-using-the-UI/page

Learn to authenticate to HashiCorp Vault’s web interface using tokens and copy your active token for CLI or API use.

In this guide, you’ll learn how to authenticate to HashiCorp Vault’s web interface using tokens and how to copy your active token for CLI or API use. This workflow is essential for administrators and operators who need to manage secrets or automate Vault interactions without repeatedly entering credentials.

## Table of Contents

* [Overview of Token Authentication](#overview-of-token-authentication)
* [Logging In with a Token](#logging-in-with-a-token)
* [Copying Your Active Token](#copying-your-active-token)
* [Examples: CLI & API Usage](#examples-cli--api-usage)
* [References](#references)

## Overview of Token Authentication

Vault’s **Token** auth method is the simplest form of authentication. It’s most commonly used when:

* You have the initial root token after deploying a new Vault cluster.
* You generated a token via the Vault CLI or another auth method.

<Callout icon="triangle-alert">
  Treat Vault tokens like passwords. Never share them publicly or commit them to version control. Always store tokens securely (e.g., in a secrets manager).
</Callout>

## Logging In with a Token

Follow these steps to authenticate in the Vault UI using a token:

| Step | Action                                                             |
| ---- | ------------------------------------------------------------------ |
| 1    | Navigate to the Vault UI and click **Token** under “Authenticate”. |
| 2    | Paste your token into the input field.                             |
| 3    | Click **Sign In** to access the UI.                                |

Once authenticated, you’ll see the Vault dashboard and can begin managing secrets, policies, and more.

## Copying Your Active Token

After signing in (via Token, LDAP, Okta, OIDC, etc.), you can quickly retrieve your current token for use in scripts or API calls:

1. Click the user menu in the top-right corner of the Vault UI.
2. Select **Copy Token**.

This copies your active token to the clipboard.

<Callout icon="lightbulb">
  Copying the token from the UI is ideal for one-off CLI commands or testing API endpoints without re-authenticating.
</Callout>

## Examples: CLI & API Usage

Use the copied token to interact with Vault programmatically:

```shell theme={null}
