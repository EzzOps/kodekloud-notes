# On error (name exists), try:
consul acl policy create -name "test456" -rules @rules.hcl
```

Sample output after creating `test456`:

```text theme={null}
ID:        51eff8b-4581-7009-2d44-78edf6f105da
Name:      test456
Namespace: default
Rules:
  node "web-server-01" {
    policy = "write"
  }
  key_prefix "apps/eCommerce" {
    policy = "write"
  }
  session_prefix "" {
    policy = "write"
  }
  service "eCommerce-Front-End" {
    policy = "write"
  }
```

## 3. Verify Your Token and List K/V Entries

Clear your terminal and display the token:

```bash theme={null}
clear
cat token.txt
# Example output:
# c7142d5a-aba1-78ba-f521-189971e29c24
```

Then list all keys in the K/V store:

```bash theme={null}
consul kv get -recurse
```

Expected output:

```text theme={null}
apps/eCommerce/database:billing
apps/eCommerce/database_host:customer_db
apps/eCommerce/environment:production
apps/eCommerce/version:4.5
apps/search/url:search.service.consul
apps/search/version:4
```

## 4. Authenticate API Requests

Now that you know the key (`apps/eCommerce/database_host`) and have your ACL token, you can fetch its value using the Consul HTTP API. Below are two supported methods:

| Header Type    | Description                  | Header Example                                |
| -------------- | ---------------------------- | --------------------------------------------- |
| X-Consul-Token | Consul-specific token header | `X-Consul-Token: c7142d5a-aba1-78ba-f521-...` |
| Authorization  | Standard HTTP Bearer token   | `Authorization: Bearer c7142d5a-aba1-78ba...` |

### Method 1: X-Consul-Token Header

```bash theme={null}
curl \
  --header "X-Consul-Token: c7142d5a-aba1-78ba-f521-189971e29c24" \
  http://127.0.0.1:8500/v1/kv/apps/eCommerce/database_host | jq
```

Response:

```json theme={null}
[
  {
    "LockIndex": 0,
    "Key": "apps/eCommerce/database_host",
    "Flags": 0,
    "Value": "Y3VzdG9tZXJzZGI=",
    "Namespace": "default",
    "CreateIndex": 2336,
    "ModifyIndex": 2336
  }
]
```

### Method 2: Authorization Bearer Header

```bash theme={null}
curl \
  --header "Authorization: Bearer c7142d5a-aba1-78ba-f521-189971e29c24" \
  http://127.0.0.1:8500/v1/kv/apps/eCommerce/database_host | jq
```

The JSON payload returned is identical to **Method 1**.

***

You’ve now learned how to authenticate Consul API requests using an ACL token—either via `X-Consul-Token` or the standard `Authorization: Bearer` header. For more information, refer to the [Consul API KV documentation](https://www.consul.io/api-docs/kv).

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/77c34744-e0fe-450e-82ea-c699ae223d45/lesson/3d7ed3e1-99f6-4e58-8317-2451357e5bbe)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/77c34744-e0fe-450e-82ea-c699ae223d45/lesson/dda060e9-3724-4bdf-8bb6-bc592d749b37)


# Demo Using Tokens with the Consul CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Secure-Services-with-Basic-ACLs/Demo-Using-Tokens-with-the-Consul-CLI/page

This guide explains four methods to provide an ACL token to the Consul CLI for authorized API access.

In this guide, you’ll learn four ways to provide an ACL token to the Consul CLI. ACL tokens control access to Consul’s API, ensuring your operations are authorized. You can supply your token through:

1. The `-token` flag
2. The `CONSUL_HTTP_TOKEN` environment variable
3. The `-token-file` flag
4. The `CONSUL_HTTP_TOKEN_FILE` environment variable

For demonstration, we’ll use the bootstrap/master token `c7142d25-a8b1-70ba-f521-189872e92c24`. Be sure to substitute your own token.

> **triangle-alert** Never expose your ACL tokens in public repositories or logs. Treat them like passwords.

## Quick Comparison

| Method                   | Configuration            | When to Use                                            |
| ------------------------ | ------------------------ | ------------------------------------------------------ |
| `-token` flag            | CLI argument             | One-off commands or scripts                            |
| `CONSUL_HTTP_TOKEN`      | Environment variable     | Frequent CLI use, avoids repetitive flags              |
| `-token-file` flag       | File containing token    | Centralized token management via file system           |
| `CONSUL_HTTP_TOKEN_FILE` | Env var pointing to file | Combine file management with environment configuration |

***

## 1. Using the `-token` Flag

Supply the ACL token directly on the command line with `-token`.

```bash theme={null}
consul acl policy create \
  -token c7142d25-a8b1-70ba-f521-189872e92c24 \
  -name "test-policy" \
  -rules @rules.hcl
```

This is ideal for ad-hoc operations or automation scripts where passing flags is acceptable.

***

## 2. Using the `CONSUL_HTTP_TOKEN` Environment Variable

Export the token once, then omit the `-token` flag in subsequent commands:

```bash theme={null}
export CONSUL_HTTP_TOKEN=c7142d25-a8b1-70ba-f521-189872e92c24
```

Now run the same policy creation without specifying the token:

```bash theme={null}
consul acl policy create \
  -name "test-policy" \
  -rules @rules.hcl
```

To verify permissions are enforced, unset the variable and rerun:

```bash theme={null}
unset CONSUL_HTTP_TOKEN

consul acl policy create \
  -name "test-policy" \
  -rules @rules.hcl
