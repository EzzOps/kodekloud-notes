# Expected output: consul-template v0.25.1
```

## 3. Create a Template File

Define your template with placeholders that map to the Consul K/V keys:

```bash theme={null}
cat << 'EOF' > config.json.tmpl
{
  "environment":   "{{ key "apps/eCommerce/environment" }}",
  "version":       "{{ key "apps/eCommerce/version" }}",
  "database_host": "{{ key "apps/eCommerce/database_host" }}",
  "database_name": "{{ key "apps/eCommerce/database" }}"
}
EOF
```

Each `{{ key "..." }}` snippet instructs Consul Template to fetch the corresponding value at render time.

## 4. Render the Template

Use the `-once` flag for a single render, or run without it to watch for changes:

```bash theme={null}
consul-template -template "config.json.tmpl:config.json" -once
```

<Callout icon="triangle-alert">
  Using `-once` renders the file a single time and then exits. Remove `-once` to keep watching for updates.
</Callout>

Verify the output:

```bash theme={null}
ls
cat config.json
```

```json theme={null}
{
  "environment": "production",
  "version":     "4.5",
  "database_host": "customer_db",
  "database_name": "billing"
}
```

## 5. Next Steps

In production, run Consul Template as a service or sidecar to continuously monitor your K/V store. This ensures that any update in Consul is immediately reflected in your application’s configuration.

***

## Links and References

* [Consul Template Documentation](https://www.consul.io/docs/agent/templates)
* [Consul K/V Store Overview](https://www.consul.io/docs/agent/kv)
* [HashiCorp Consul Template Releases](https://releases.hashicorp.com/consul-template/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/70a7eb0f-aec7-41aa-b417-398c341698b6/lesson/89c70441-5b19-4604-8e1e-340b8cf36803" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/70a7eb0f-aec7-41aa-b417-398c341698b6/lesson/8f6c68ef-cdcb-4abd-bbe1-552329ba0bfa" />
</CardGroup>


# Demo Using Envconsul to monitor Changes to Consul KV

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Access-the-Consul-KeyValue-KV/Demo-Using-Envconsul-to-monitor-Changes-to-Consul-KV/page

This tutorial explains how to install and use HashiCorp envconsul to monitor Consul KV changes and expose them as environment variables.

In this tutorial, you’ll learn how to install and run HashiCorp envconsul on an application server. Envconsul fetches key-value pairs from Consul and exposes them as environment variables, automatically watching for changes without manual intervention.

## Prerequisites

* A running Consul cluster with KV entries under `apps/ecommerce`
* SSH access to your application server
* (Optional) Consul ACL token if your cluster enforces ACLs

### Example KV Entries

| Consul KV Path                     | Value                                               |
| ---------------------------------- | --------------------------------------------------- |
| `apps/ecommerce/database_host`     | `"customer-db"`                                     |
| `apps/ecommerce/database`          | `"billing"`                                         |
| `apps/ecommerce/connection_string` | `"Server=customer-db;Database=billing;User Id=..."` |

## 1. Install envconsul

Download the latest Linux AMD64 binary from HashiCorp’s release archive:

```bash theme={null}
curl --silent -Lo /tmp/envconsul.zip \
  https://releases.hashicorp.com/envconsul/0.11.0/envconsul_0.11.0_linux_amd64.zip
```

Unzip and move the binary into your `PATH`:

```bash theme={null}
unzip /tmp/envconsul.zip -d /tmp
sudo mv /tmp/envconsul /usr/local/bin/
```

Verify the installation:

```bash theme={null}
envconsul --version
