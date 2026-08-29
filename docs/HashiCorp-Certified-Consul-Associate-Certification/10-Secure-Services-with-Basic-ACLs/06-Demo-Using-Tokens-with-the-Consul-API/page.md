# Demo Using Tokens with the Consul API

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Secure-Services-with-Basic-ACLs/Demo-Using-Tokens-with-the-Consul-API/page

This article demonstrates how to use an ACL token to authenticate HTTP requests with the Consul Key/Value store.

Welcome to the final lab of this guide. Here you’ll leverage an existing bootstrap ACL token to authenticate HTTP requests against the Consul Key/Value (K/V) store. This demonstration covers:

1. Loading the token from a file
2. Creating or recreating an ACL policy
3. Retrieving K/V entries via `curl` and `jq`
4. Two authentication methods for the Consul API

<Callout icon="lightbulb">
  Before proceeding, ensure Consul is running and you have access to the `consul` binary. For more details, see the [Consul documentation](https://www.consul.io/docs).
</Callout>

## 1. Export the ACL Token

Set the `CONSUL_HTTP_TOKEN_FILE` environment variable to read your token from `token.txt`:

```bash theme={null}
export CONSUL_HTTP_TOKEN_FILE=token.txt
```

<Callout icon="triangle-alert">
  Keep your token file secure. Avoid committing it to version control or sharing it publicly.
</Callout>

## 2. Create (or Recreate) an ACL Policy

Use `consul acl policy create` to define a policy with the required rules. If the policy name already exists, choose a new one:

```bash theme={null}
consul acl policy create -name "test123" -rules @rules.hcl
