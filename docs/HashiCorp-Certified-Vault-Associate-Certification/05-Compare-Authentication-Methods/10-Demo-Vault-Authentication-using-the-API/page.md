# Demo Vault Authentication using the API

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-Authentication-Methods/Demo-Vault-Authentication-using-the-API/page

This guide explains how to authenticate to HashiCorp Vault via Okta and retrieve secrets using curl.

In this guide, we’ll walk through how to authenticate to HashiCorp Vault via Okta and retrieve secrets using `curl`. The same pattern applies for other auth methods (e.g., GitHub, LDAP, AWS).

## Prerequisites

| Requirement   | Purpose                                    |
| ------------- | ------------------------------------------ |
| Vault server  | Running locally at `http://127.0.0.1:8200` |
| curl          | Issue HTTP requests                        |
| jq (optional) | Pretty-print JSON                          |

<Callout icon="lightbulb">
  Installing `jq` is optional but recommended for readable JSON outputs.
</Callout>

***

## 1. Authenticate via Okta

First, create a JSON file named `password.json` containing your Okta password:

```json theme={null}
{
  "password": "YourOktaPassword"
}
```

Next, send a login request. Replace `you@example.com` with your Okta username:

```bash theme={null}
curl --request POST \
     --data @password.json \
     http://127.0.0.1:8200/v1/auth/okta/login/you@example.com
```

A successful login returns a `client_token` in the `auth` block:

```json theme={null}
{
  "auth": {
    "client_token": "s.yuA7WdiZFMr9ArIjtYX0VMY",
    "policies": ["default","your-policy"],
    "metadata": {"username":"you@example.com"},
    "lease_duration":2764800,
    "renewable":true
  },
  "lease_id":"",
  "request_id":"05a0e2e2-879a-9d37-530c-aceedb831cd2"
}
```

For readable JSON, pipe the output to `jq`:

```bash theme={null}
curl --request POST \
     --data @password.json \
     http://127.0.0.1:8200/v1/auth/okta/login/you@example.com \
  | jq
```

Scroll to locate the `client_token` value.

***

## 2. Read a Secret from the KV Store

With your `client_token`, you can query Vault’s KV store. In this example, we read from `secret/data/app01` (KV version 2):

```bash theme={null}
curl --header "X-Vault-Token: s.yuA7WdiZFMr9ArIjtYX0VMY" \
     http://127.0.0.1:8200/v1/secret/data/app01
```

A typical raw response looks like this:

```json theme={null}
{
  "request_id":"9608f10d-2cb7-146e-4d28-c17bbbb92f07",
  "data":{
    "data":{"password":"Password1!"},
    "metadata":{
      "created_time":"2021-06-14T19:09:08.588706Z",
      "version":1
    }
  }
}
```

For formatted output:

```bash theme={null}
curl --header "X-Vault-Token: s.yuA7WdiZFMr9ArIjtYX0VMY" \
     http://127.0.0.1:8200/v1/secret/data/app01 \
  | jq
```

Which yields:

```json theme={null}
{
  "request_id":"f30d4e94-8bb7-3336-c1b0-ccc46644153d",
  "data":{
    "data":{"password":"Password1!"},
    "metadata":{
      "created_time":"2021-06-14T19:09:08.5887067Z",
      "version":1
    }
  }
}
```

<Callout icon="triangle-alert">
  Never expose your `client_token` in shared scripts or logs. Treat it like a password.
</Callout>

***

## 3. Summary of Endpoints

| Endpoint             | Description            | HTTP Method |
| -------------------- | ---------------------- | ----------- |
| /v1/auth/okta/login/ | Authenticate via Okta  | POST        |
| /v1/secret/data/     | Read secret from KV v2 | GET         |

***

## Conclusion

You have now:

1. Authenticated to Vault using the Okta auth method.
2. Extracted the `client_token` from the API response.
3. Retrieved a secret from the KV secrets engine.

Reuse this pattern to create, update, or delete secrets and to interact with other Vault API endpoints.

***

## Links and References

* [Vault HTTP API Documentation](https://www.vaultproject.io/api-docs)
* [Okta Auth Method (Vault)](https://www.vaultproject.io/docs/auth/okta)
* [Installing jq](https://stedolan.github.io/jq/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/eebfb593-8885-43b0-a9ba-9f88af87092e/lesson/975fea9a-ea13-45d2-b158-5d56e3b6ec4f" />
</CardGroup>
