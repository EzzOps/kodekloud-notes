# Backstage Configuration

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Backstage-Basics/Backstage-Configuration/page

Guide to Backstage configuration files and layered environment-specific overrides for local and production using app-config.yaml, app-config.local.yaml and app-config.production.yaml

In this lesson we cover how to configure a Backstage instance and which files to modify to change Backstage behavior across environments (local development, production, etc.). This guide explains the layered configuration model used by Backstage and shows where to place environment-specific overrides.

A typical Backstage app repository contains configuration files such as `app-config.local.yaml`, `app-config.production.yaml`, `app-config.yaml`, `backstage.json`, and `catalog-info.yaml`, along with folders like `node_modules`, `packages`, and `plugins`.

<Frame>
  <img alt="A slide titled &#x22;Backstage Configuration&#x22; showing a directory tree of config files and folders. It lists files like app-config.local.yaml, app-config.production.yaml, app-config.yaml, backstage.json, catalog-info.yaml and folders such as node_modules, packages, plugins, etc." />
</Frame>

Key configuration files to know:

* `app-config.yaml` — base configuration shared across environments
* `app-config.local.yaml` — overrides for local development
* `app-config.production.yaml` — overrides for production deployments

Backstage supports layered configuration: the base `app-config.yaml` contains settings common to all environments, and environment-specific files merge on top of it to override values when present.

## How the config files work (layered configuration)

* Backstage loads `app-config.yaml` first as the canonical base.
* If present, `app-config.local.yaml` and `app-config.production.yaml` are merged on top of the base and replace any overlapping keys.
* Only include keys in the override files for properties that change between environments; unspecified keys remain as defined in the base file.

## app-config.yaml (base configuration)

Put values that are identical across environments here. This file should be committed to source control and serve as the canonical configuration for your Backstage instance.

```yaml theme={null}
app:
  title: Scaffolded Backstage App
  baseUrl: http://147.182.170.10:3000

organization:
  name: My Company

backend:
  baseUrl: http://147.182.170.10:7007
  listen:
    port: 7007
  cors:
    origin: http://147.182.170.10:3000
    methods: [GET, HEAD, PATCH, POST, PUT, DELETE]
    credentials: true
```

## app-config.local.yaml (local development overrides)

Use `app-config.local.yaml` to override only the values that differ for local development. Backstage merges this file on top of the base config, so you don’t need to repeat the entire configuration—only the keys you want to change.

<Frame>
  <img alt="A diagram showing that app-config.local.yaml (local development configuration) overrides the main app-config.yaml, with an arrow labeled &#x22;Override&#x22; from the local file to the main config." />
</Frame>

Example local overrides:

```yaml theme={null}
app:
  baseUrl: http://localhost:3000

backend:
  baseUrl: http://localhost:7007
  cors:
    origin: http://localhost:3000
```

> **warning** Do not commit `app-config.local.yaml` if it contains secrets (API keys, credentials) or machine-specific values. Keep it as a local-only configuration file and add it to `.gitignore` where appropriate.

## app-config.production.yaml (production overrides)

`app-config.production.yaml` works the same as the local override file but is intended for production deployments. Use environment-specific overrides here and avoid hard-coding secrets or machine-specific values in files stored in version control.

<Frame>
  <img alt="A diagram titled &#x22;App-config.production.yaml&#x22; showing a PROD server icon above two config-file icons (app-config.yaml on the left and app-config.production.yaml on the right) with a horizontal arrow labeled &#x22;Override&#x22; pointing from the production-specific file to the base config." />
</Frame>

Example: reference environment variables instead of committing secrets. The example below uses an environment variable for the host:

```yaml theme={null}
app:
  baseUrl: "https://${HOST}"
```

> **lightbulb** Use environment variables in production configs to avoid storing secrets in version control. The `HOST` environment variable in the example above will be substituted at runtime.

## Restarting Backstage after config changes

Backstage reads configuration files at startup. After editing any config file, restart your Backstage process so the new settings are applied.

```bash theme={null}
