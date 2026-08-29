# Managing Consul Service Mesh Intentions

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Register-a-Service-Proxy/Managing-Consul-Service-Mesh-Intentions/page

This article explains how to define and manage Consul Service Mesh intentions using various interfaces for consistent policy enforcement.

In this lesson, you’ll discover how to define and manage Consul Service Mesh intentions using the Config Entry API, HTTP API, CLI, and UI. Intentions created in one interface instantly appear in all others, ensuring consistent policies across your cluster.

## Defining Intentions with a Service-Intentions Config Entry

The recommended approach for declaring service intentions is to use a `service-intentions` config entry. This keeps your intentions version-controlled and declarative.

```hcl theme={null}
kind = "service-intentions"
name = "db-01"

sources = [
  {
    name   = "web-01"
    action = "deny"
  },
]
```

* `kind`: Must be `service-intentions`.
* `name`: The upstream service (here, `db-01`).
* `sources`: List of downstream services and their actions (`allow` or `deny`).

> **lightbulb** Modifying an existing intention only impacts **new** connections. Established sessions continue under the old policy until they’re restarted.

## Viewing and Managing Intentions in the UI

1. Log in to the Consul UI.
2. Click the **Intentions** tab in the sidebar to see all configured intentions.

![The image shows a guide on managing Consul Service Mesh intentions using a user interface, highlighting how to create, view, and manage intentions in the "Intentions" tab and within affected services.](https://kodekloud.com/kk-media/image/upload/v1752877934/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Managing-Consul-Service-Mesh-Intentions/consul-service-mesh-intentions-guide.jpg)

Example mappings in the UI:

| Source Service                    | Destination Service | Action |
| --------------------------------- | ------------------- | ------ |
| API service                       | prod customer DB    | allow  |
| Web app 01                        | customer DB         | allow  |
| API service, front-end e-commerce | dev MySQL           | deny   |

To inspect intentions for a single service:

1. Select the service (e.g., **front-end e-commerce**).
2. Open its **Intentions** tab.
3. Delete or modify any intention directly.

## Managing Intentions with the HTTP API

Consul’s HTTP API enables programmatic creation, retrieval, and deletion of intentions. Note that the `/v1/connect/intents` endpoint was deprecated in v1.9.0 in favor of `/v1/connect/intentions/exact`.

> **triangle-alert** The `/v1/connect/intents` path is deprecated as of Consul v1.9.0. Always use `/v1/connect/intentions/exact`.

### Create or Update an Intention

Allow `web-01` to communicate with `db-01`:

1. Create a `payload.json`:

   ```json theme={null}
   {
     "SourceType": "consul",
     "Action": "allow"
   }
   ```

2. Send the PUT request:

   ```bash theme={null}
   curl --request PUT \
     --data @payload.json \
     https://consul.example.com:8500/v1/connect/intentions/exact?source=web-01&destination=db-01
   ```

A successful call returns:

```json theme={null}
true
```

### List and Delete

| Operation | HTTP Method & Endpoint                                         |
| --------- | -------------------------------------------------------------- |
| List      | GET  `/v1/connect/intentions`                                  |
| Get       | GET  `/v1/connect/intentions/exact?source=<>&destination=<>`   |
| Delete    | DELETE `/v1/connect/intentions/exact?source=<>&destination=<>` |

## Managing Intentions via CLI

The `consul intention` command provides a full suite of subcommands to create, list, inspect, and remove intentions.

```bash theme={null}
