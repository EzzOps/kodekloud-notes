# => envconsul v0.11.0
```

<Callout icon="lightbulb">
  Make sure to update the version number in the URL if a newer release is available.
</Callout>

## 2. Fetch and Export KV Data

Use `envconsul` to pull all keys under the `apps/ecommerce` prefix and convert them to uppercase environment variables:

```bash theme={null}
envconsul \
  -prefix="apps/ecommerce" \
  -uppercase \
  -- printenv
```

Sample output:

```bash theme={null}
DATABASE_HOST=customer-db
DATABASE=billing
CONNECTION_STRING=Server=customer-db;Database=billing;User Id=...
```

### Common Flags

| Flag         | Description                                        |
| ------------ | -------------------------------------------------- |
| `-prefix`    | Consul KV path to fetch                            |
| `-uppercase` | Convert all keys to uppercase environment variable |
| `--`         | Separator before the command to execute            |

## 3. Launch Your Application with envconsul

To ensure your application picks up the variables at startup and on any KV change:

```bash theme={null}
envconsul \
  -prefix="apps/ecommerce" \
  -uppercase \
  -- ./start-your-app.sh
```

<Callout icon="triangle-alert">
  If your app requires a Consul ACL token, set `CONSUL_HTTP_TOKEN` in the environment or pass `-token` to `envconsul`.
</Callout>

## Summary

In this demo, you:

1. Installed `envconsul` on a Linux server.
2. Retrieved KV pairs from Consul and exposed them as environment variables.
3. Launched your application to inherit and watch for configuration updates automatically.

By integrating `envconsul`, your service maintains up-to-date settings without manual polling or restarts.

## Links and References

* [envconsul Releases][1]
* [Consul KV Documentation](https://www.consul.io/docs/kv)
* [HashiCorp envconsul Overview](https://www.hashicorp.com/products/envconsul)

[1]: https://releases.hashicorp.com/envconsul/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/70a7eb0f-aec7-41aa-b417-398c341698b6/lesson/ffc95153-fa8e-41ed-a1c8-3f2e71794713" />
</CardGroup>


# Demo Working with the Consul KV

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Access-the-Consul-KeyValue-KV/Demo-Working-with-the-Consul-KV/page

Learn to manage key/value pairs in HashiCorp Consul’s K/V store using the web UI, CLI, and HTTP API with practical examples.

In this hands-on tutorial, you’ll learn how to manage key/value pairs in HashiCorp Consul’s K/V store using three methods: the web UI, the CLI, and the HTTP API. We'll cover adding, querying, and deleting entries, plus best practices for decoding API responses.

***

## 1. Prerequisites

* SSH access to one of your Consul server nodes
* Consul UI open in your browser (defaults to [http://127.0.0.1:8500/ui](http://127.0.0.1:8500/ui))

When you first open the UI, the **Key/Value** section should be empty.

***

## 2. Adding Data via the CLI

Use the `consul kv put` command to insert entries under the `apps/eCommerce` prefix.

```bash theme={null}
