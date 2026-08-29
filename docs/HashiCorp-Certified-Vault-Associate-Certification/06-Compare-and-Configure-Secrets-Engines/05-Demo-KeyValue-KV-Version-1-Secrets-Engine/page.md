# Demo KeyValue KV Version 1 Secrets Engine

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-and-Configure-Secrets-Engines/Demo-KeyValue-KV-Version-1-Secrets-Engine/page

This guide explores enabling and managing the Key/Value version 1 secrets engine in HashiCorp Vault, including CRUD operations and JSON output filtering.

In this guide, you’ll explore how to enable and manage the Key/Value (KV) version 1 secrets engine in HashiCorp Vault. You will learn to list existing secrets engines, mount a new KV engine, perform CRUD operations on secrets, and filter JSON output with `jq`.

## 1. List Enabled Secrets Engines

Run the following command to see which secrets engines are mounted:

```bash theme={null}
vault secrets list
```

| Path       | Type      | Accessor            | Description                                         |
| ---------- | --------- | ------------------- | --------------------------------------------------- |
| cubbyhole/ | cubbyhole | cubbyhole\_9c6c2ca2 | Per-token private secret storage                    |
| identity/  | identity  | identity\_e55fbf01  | Identity store                                      |
| sys/       | system    | system\_ae43616e    | System endpoints for control, policy, and debugging |
| transit/   | transit   | transit\_5bb3af5e   | n/a                                                 |

## 2. Enable a KV Version 1 Secrets Engine

By default, `kv` enables version 1. Mount it at the path `training`:

```bash theme={null}
vault secrets enable -path=training kv
```

Success! You should see:

```bash theme={null}
Enabled the kv secrets engine at: training/
```

Verify the new mount:

```bash theme={null}
vault secrets list
```

| Path      | Type | Accessor     | Description |
| --------- | ---- | ------------ | ----------- |
| training/ | kv   | kv\_1d131683 | n/a         |
| …         | …    | …            | …           |

> **lightbulb** If you need KV version 2 (with versioning, metadata, and rollback), use `-version=2`.

## 3. Verify the Engine Version

Use `--detailed` to confirm the KV engine version:

```bash theme={null}
vault secrets list --detailed
```

Look for an empty `Options` map (`map[]`), which indicates KV v1:

```text theme={null}
Path        Plugin  Accessor       Options
----        ------  --------       -------
training/   kv      kv_1d131683    map[]
```

## 4. Write and Read Secrets

Write a secret at `training/apps/jenkins`:

```bash theme={null}
vault kv put training/apps/jenkins apikey=secret123
```

Read it back:

```bash theme={null}
vault kv get training/apps/jenkins
```

Output:

```text theme={null}
Key      Value
---      -----
apikey   secret123
```

## 5. Update Secrets

Writing to the same path replaces existing data:

```bash theme={null}
vault kv put training/apps/jenkins apikey=newsecret456
vault kv get training/apps/jenkins
```

Result:

```text theme={null}
Key      Value
---      -----
apikey   newsecret456
```

## 6. Write Multiple Key/Value Pairs

You can include several pairs in one command:

```bash theme={null}
vault kv put training/apps/jenkins apikey=secret789 user=vault-admin
vault kv get training/apps/jenkins
```

Result:

```text theme={null}
Key      Value
---      -----
apikey   secret789
user     vault-admin
```

## 7. Filter JSON Output with jq

Retrieve secret data in JSON:

```bash theme={null}
vault kv get -format=json training/apps/jenkins
```

Sample output:

```json theme={null}
{
  "request_id": "...",
  "data": {
    "apikey": "secret789",
    "user": "vault-admin"
  }
}
```

Extract fields:

```bash theme={null}
vault kv get -format=json training/apps/jenkins \
  | jq -r '.data.apikey'
vault kv get -format=json training/apps/jenkins \
  | jq -r '.data.user'
