# => Failed to create new policy: Unexpected response code: 403 (Permission denied)
```

<Callout icon="lightbulb">
  Using `CONSUL_HTTP_TOKEN` is convenient for CI/CD pipelines and local development shells.
</Callout>

***

## 3. Using the `-token-file` Flag

Store your token in a file (e.g., `token.txt`) and point the CLI at it:

```bash theme={null}
cat token.txt
consul acl policy create \
  -token-file token.txt \
  -name "test-policy" \
  -rules @rules.hcl
```

This approach keeps tokens out of your command history.

***

## 4. Using the `CONSUL_HTTP_TOKEN_FILE` Environment Variable

Combine file-based tokens with environment variables to centralize configuration:

```bash theme={null}
export CONSUL_HTTP_TOKEN_FILE=token.txt

consul acl policy create \
  -name "test-policy" \
  -rules @rules.hcl
# => failed to create new policy: Unexpected response code: 500 (Invalid Policy: A Policy with Name "test-policy" already exists)
```

<Callout icon="lightbulb">
  Ensure the token file has restrictive permissions (`chmod 600 token.txt`) to prevent unauthorized access.
</Callout>

***

## Summary

Consul CLI supports ACL tokens via:

* `-token` flag
* `CONSUL_HTTP_TOKEN` environment variable
* `-token-file` flag
* `CONSUL_HTTP_TOKEN_FILE` environment variable

Choose the method that best fits your workflow. For interactive use or automation, environment variables often offer the cleanest experience.

***

## Links and References

* [Consul ACL Overview](https://www.consul.io/docs/security/acl)
* [Consul CLI Documentation](https://www.consul.io/docs/commands)
* [HashiCorp Best Practices](https://learn.hashicorp.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/77c34744-e0fe-450e-82ea-c699ae223d45/lesson/e8c04e13-6d06-40f4-80cc-c8928f2fb107" />
</CardGroup>


# Demo Using Tokens with the Consul UI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Secure-Services-with-Basic-ACLs/Demo-Using-Tokens-with-the-Consul-UI/page

This tutorial explains how to authenticate to the Consul UI using an ACL token for managing access control.

In this tutorial, you’ll learn how to authenticate to the HashiCorp Consul UI with an ACL token. Once logged in, you can perform write operations—such as creating or modifying tokens, roles, and policies—directly from the interface.

## Overview

By default, the Consul UI provides read-only access to services, nodes, the Key/Value store, and cluster status. To enable write operations—like managing ACLs and service intentions—you must turn on ACL enforcement and log in with a valid token. This demo walks you through using the bootstrap (master) token to unlock full ACL management capabilities in the UI.

<Callout icon="lightbulb">
  * A running Consul cluster with ACL enforcement enabled
  * A valid bootstrap (master) token
  * Browser access to the Consul UI (usually http\://\<consul-server>:8500/ui/)
</Callout>

## 1. Logging In with an ACL Token

1. Navigate to the Consul UI in your browser.
2. Select the **ACL** tab. If you’re not authenticated, you’ll see:

   **You are not authorized. You must be granted permissions to access this data.**
3. Click **Login**. When prompted, paste your bootstrap token and submit.
4. After successful authentication, the ACL management interface loads:

<Frame>
  ![The image shows a web interface for managing access controls, specifically displaying a list of tokens with details such as their scope and description. The interface includes tabs for Tokens, Roles, and Policies.](https://kodekloud.com/kk-media/image/upload/v1752877954/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Using-Tokens-with-the-Consul-UI/access-control-web-interface-tokens.jpg)
</Frame>

<Callout icon="triangle-alert">
  Treat your bootstrap token like a root credential. Avoid sharing it or embedding it in scripts. Always store tokens in a secure vault or use a short-lived token for day-to-day operations.
</Callout>

## 2. Managing ACL Entities

Once logged in, the **ACL** section exposes three main entities:

| Entity   | Description                                 | UI Actions                |
| -------- | ------------------------------------------- | ------------------------- |
| Tokens   | Create, revoke, and modify ACL tokens       | New Token, Revoke, Edit   |
| Roles    | Group multiple policies under a single role | New Role, Assign Policies |
| Policies | Define fine-grained permission rules        | New Policy, Edit, Clone   |

### Creating and Editing

* To **create** a token or role, click **New Token** or **New Role** in the corresponding tab.
* To **edit** an existing policy (e.g., `e-commerce`), switch to **Policies**, select the policy, and update its HCL or JSON definitions.

## 3. Example: Editing a Policy

1. Click the **Policies** tab.
2. Select the `e-commerce` policy from the list.
3. Modify the rules in the editor pane and click **Save**.
4. Verify changes by assigning the policy to a role or creating a token scoped to it.

## Conclusion

In this lesson, you authenticated to the Consul UI using a bootstrap token and explored how to manage ACL tokens, roles, and policies directly from the interface. With these capabilities, you can enforce robust security policies and streamline access control operations.

## Links and References

* [Consul UI Guide](https://www.consul.io/docs/ui)
* [Access Control List (ACL) Overview](https://www.consul.io/docs/security/acl)
* [Official Consul Documentation](https://www.consul.io/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/77c34744-e0fe-450e-82ea-c699ae223d45/lesson/79ac0c03-da03-4fb1-9fd2-fdb601c51952" />
</CardGroup>
