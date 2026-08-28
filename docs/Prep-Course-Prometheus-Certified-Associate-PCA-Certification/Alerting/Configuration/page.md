# Example: replace <url-to-alertmanager-tarball> with the copied URL
$ wget <url-to-alertmanager-tarball>
$ tar xvf alertmanager-*.tar.gz
$ cd alertmanager-*/
```

3. Inspect the extracted files:

| File / Directory   | Purpose                                                      |
| ------------------ | ------------------------------------------------------------ |
| `alertmanager`     | The Alertmanager executable (binary)                         |
| `alertmanager.yml` | Default configuration file (routing, receivers, etc.)        |
| `amtool`           | Command-line utility for interacting with Alertmanager       |
| `data/`            | Storage for silences, notification states, and cluster state |

<Frame>
  <img alt="The image displays a download page for Prometheus, showing downloadable files for different components like Prometheus, Alertmanager, and Blackbox Exporter, with details such as version, operating system, architecture, and file size." />
</Frame>

<Callout icon="lightbulb">
  You can run Alertmanager from the extracted folder. By default it looks for `alertmanager.yml` in the current working directory and stores runtime state under `data/`. Use `--config.file` and `--storage.path` to override these locations.
</Callout>

## Start Alertmanager

From the extracted directory, start Alertmanager:

```bash theme={null}
$ ./alertmanager
```

You should see logs similar to this, indicating successful startup and the listening address:

```bash theme={null}
ts=2022-10-04T20:57:44.014Z caller=cluster.go:680 level=info component=cluster msg="Waiting for gossip to settle..." interval=2s
ts=2022-10-04T20:57:44.065Z caller=coordinator.go:113 level=info component=configuration msg="Loading configuration file" file=alertmanager.yml
ts=2022-10-04T20:57:44.065Z caller=coordinator.go:126 level=info component=configuration msg="Completed loading of configuration file" file=alertmanager.yml
ts=2022-10-04T20:57:44.068Z caller=main.go:535 level=info msg="Listening address=:9093"
ts=2022-10-04T20:57:44.068Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2=false
ts=2022-10-04T20:57:46.014 caller=cluster.go:705 level=info component=cluster msg="gossip not settled" polls=0 before=0 now=1 elapsed=2.000253818s
ts=2022-10-04T20:57:51.017 caller=cluster.go:697 level=info component=cluster msg="gossip settled; proceeding"
```

By default Alertmanager listens on port 9093. Open a browser to `http://localhost:9093/` (or replace `localhost` with the server IP) to access the Alertmanager web UI.

<Callout icon="warning">
  If exposing Alertmanager to the public internet, secure the interface with a reverse proxy and TLS, or restrict access via firewall rules. Alertmanager can contain sensitive routing and receiver details.
</Callout>

## Configure Prometheus to Use Alertmanager

After Alertmanager is running, add it to your Prometheus configuration under the `alerting` section. Below is an example `prometheus.yml` snippet showing how to point Prometheus to one or more Alertmanager instances:

```yaml theme={null}
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager1:9093
          - alertmanager2:9093

rule_files:
  - "rules.yml"

scrape_configs:
  # ... your scrape jobs ...
```

* Replace `alertmanager1` / `alertmanager2` with hostnames or IP addresses reachable from your Prometheus server.
* Prometheus sends alerts to these targets via the Alertmanager API on port 9093.

## Quick Troubleshooting

* If logs show "gossip not settled", this is expected for clustered Alertmanager nodes until they discover each other.
* If Prometheus can’t reach Alertmanager, confirm network reachability and that Alertmanager is listening on port 9093 (`ss -lntp | grep 9093`).
* Use `amtool` for local inspection and to manage silences from the command line.

## References

* Prometheus downloads: [https://prometheus.io/download/](https://prometheus.io/download/)
* Alertmanager documentation: [https://prometheus.io/docs/alerting/latest/alertmanager/](https://prometheus.io/docs/alerting/latest/alertmanager/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/499d9ac5-c2e0-43fe-b000-f08f33fbf2dc/lesson/c0819c2f-69bb-4e1c-8a8a-cef901947f1d" />
</CardGroup>


# Configuration

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Alerting/Configuration/page

Guide to Alertmanager configuration explaining routing trees, matchers, receivers, grouping, and reload practices for delivering alerts to appropriate notification channels.

In this lesson we walk through an Alertmanager configuration file (`alertmanager.yml`) and explain how to route alerts to the right receivers. A typical Alertmanager configuration uses three primary sections:

* `global` — default settings applied across receivers (overridable).
* `route` — routing tree that maps alerts to receivers.
* `receivers` — notification destinations (Slack, email, SMS, webhooks, etc.).

Below is a compact, representative configuration that shows these sections together:

```yaml theme={null}
global:
  smtp_smarthost: 'mail.example.com:25'
  smtp_from: 'test@example.com'

route:
  receiver: staff
  group_by: ['alertname', 'job']
  routes:
    - match_re:
        job: "(node|windows)"
      receiver: infra-email

    - match:
        job: kubernetes
        severity: ticket
      receiver: k8s-slack

receivers:
  - name: 'k8s-slack'
    slack_configs:
      - channel: '#alerts'
        text: 'https://example.com/alerts/{{ .GroupLabels.app }}'
  - name: 'infra-email'
    email_configs:
      - to: 'infra@example.com'
  - name: 'staff'
    email_configs:
      - to: 'staff@example.com'
```

This sample illustrates the core concepts: defaults in `global`, a routing tree beginning at `route`, and concrete `receivers` that deliver notifications.

Callout for quick context:

<Callout icon="lightbulb">
  This guide focuses on Alertmanager routing: how alerts flow from the top-level route into nested routes, and how receivers and grouping control notification behavior.
</Callout>

## global

The `global` block sets defaults used by receiver configurations (for example, SMTP settings). Any receiver that lacks its own explicit setting will inherit values from `global`. Common uses include SMTP relay host, email `from` address, and generic webhook configuration defaults.

## route

The `route` section defines the routing tree that decides which alerts are sent to which receivers. At the top level, define a fallback receiver using the top-level `receiver` field. Alerts that do not match a more specific child route will continue to the fallback.

Example default/fallback route:

```yaml theme={null}
route:
  receiver: staff
  group_by: ['alertname', 'job']
  routes:
    - match_re:
        job: "(node|windows)"
      receiver: infra-email
    - match:
        job: kubernetes
      receiver: k8s-slack
```

Key route fields:

* `receiver` — the default receiver to send alerts to.
* `group_by` — labels used to group alerts into single notifications.
* `routes` — array of child routes, evaluated in order.

## Matcher types

Alertmanager supports three common matcher syntaxes. Use the one that best matches your routing needs.

| Matcher syntax | Use case                                                                      | Example                                                 |
| -------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------- |
| `match`        | Exact label equality (all listed pairs must match)                            | `match: { job: kubernetes, severity: ticket }`          |
| `match_re`     | Label values matched by regular expressions (useful to match multiple values) | `match_re: { job: "(node\|windows)" }`                  |
| `matchers`     | Array of expressions with operators and regex (`=`, `!=`, `=~`, `!~`)         | `matchers: ['severity="page"', 'env=~"prod\|staging"']` |

Example combining exact and regex matching:

```yaml theme={null}
route:
  routes:
    - match_re:
        job: "(node|windows)"
      receiver: infra-email

    - match:
        job: kubernetes
        severity: ticket
      receiver: k8s-slack
```

## Sub-routes (nested routes)

Routes can be nested to create parent → child relationships. Matching begins at the top-level route and then descends into child routes. A child route is only considered if its parent route matches.

Example: parent route matches `job: kubernetes`; a child route matches `severity: pager` and overrides the receiver:

```yaml theme={null}
route:
  receiver: k8s-email
  routes:
    - match:
        job: kubernetes
      receiver: k8s-email
      routes:
        - match:
            severity: pager
          receiver: k8s-pager
```

Behavior:

* Alerts with `job=kubernetes` and `severity=pager` will route to `k8s-pager`.
* Alerts with `job=kubernetes` but without `severity=pager` will use `k8s-email` (the parent route receiver).

## Example: multiple teams and sub-routes

Below is a practical layout for routing alerts to different teams (database and API), with sub-routes for severities and environments:

```yaml theme={null}
route:
  receiver: fallback-pager
  routes:
    # database team
    - match:
        team: database
      receiver: database-pager
      routes:
        - match:
            severity: page
          receiver: database-pager
        - match:
            severity: email
          receiver: database-email

    # api team
    - match:
        team: api
      receiver: api-pager
      routes:
        - match:
            severity: page
            env: dev
          receiver: api-ticket
        - match:
            severity: page
          receiver: api-pager
        - match:
            severity: ticket
          receiver: api-ticket
```

Notes on evaluation:

* The parent route (e.g., `team: database`) determines the initial receiver if no child route matches.
* Child routes are evaluated in order and can override the parent receiver if matched.

## Reloading configuration

Alertmanager does not automatically reload changes to `alertmanager.yml`. After editing the file you must apply the update using one of these methods:

* Restart the Alertmanager process (systemd example):
  * `sudo systemctl restart alertmanager`
* Send a SIGHUP to the process:
  * `sudo killall -HUP alertmanager`
* POST to the reload endpoint:
  * `curl -X POST http://localhost:9093/-/reload`

<Callout icon="warning">
  Always validate your YAML before reloading. A malformed configuration can prevent Alertmanager from starting or handling alerts correctly.
</Callout>

## Continue behavior (allowing multiple matches)

By default, route traversal stops when a route matches (first match wins). If you want an alert to match a route and then continue to later routes (so the same alert is delivered to multiple receivers), set `continue: true` on the route that should allow further evaluation.

Example — send every alert to `alert-logs`, and also to `k8s-email` for Kubernetes alerts:

```yaml theme={null}
route:
  routes:
    - receiver: alert-logs
      continue: true

    - match:
        job: kubernetes
      receiver: k8s-email
```

## Grouping alerts

Alertmanager groups alerts for a route into a single notification by default. Use `group_by` to control batching. Child routes inherit `group_by` from their parent unless they define their own.

Top-level grouping by team:

```yaml theme={null}
route:
  receiver: fallback-pager
  group_by: ['team']
  routes:
    - match:
        team: infra
      group_by: ['region', 'env']
      receiver: infra-email
      routes:
        - match:
            severity: page
          receiver: infra-pager
```

Behavior:

* Top-level: alerts are grouped by `team`. Alerts with the same `team` value are batched into single notifications.
* For the `infra` route: grouping refines to `region` and `env`. Alerts with the same `region` and `env` values are grouped together.

## Best practices and final reminders

* Keep `global`, `route`, and `receivers` sections well organized and consistent.
* Use:
  * `match` for exact label matches,
  * `match_re` for regex-based matching,
  * `matchers` for advanced matching expressions.
* Use `continue: true` on routes when you intentionally want an alert to be handled by multiple receivers.
* Validate YAML and reload Alertmanager after changes.
* Use meaningful `group_by` labels to avoid noisy notifications or overly coarse grouping.

## Links and references

* [Alertmanager Configuration](https://prometheus.io/docs/alerting/latest/configuration/) — official Prometheus Alertmanager docs
* [Alertmanager Routing](https://prometheus.io/docs/alerting/latest/alertmanager/#routing-tree) — routing tree and matcher details

If you need a sample repository or more advanced receiver examples (Slack webhooks, PagerDuty), check the official docs linked above for integration-specific fields and templates.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/499d9ac5-c2e0-43fe-b000-f08f33fbf2dc/lesson/31176c29-9994-4240-b2d0-6a8301945c3e" />
</CardGroup>
