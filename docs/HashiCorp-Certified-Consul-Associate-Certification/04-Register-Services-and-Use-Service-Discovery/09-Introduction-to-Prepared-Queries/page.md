# Open the service definition file
ec2-user@ip-10-0-101-177:~$ vi service.json

# Register the service
ec2-user@ip-10-0-101-177:~$ consul services register service.json
Registered service: front-end-eCommerce
```

Simulate a service restart to see how Consul handles temporary outages:

```bash theme={null}
ec2-user@ip-10-0-101-177:~$ sudo systemctl stop httpd
ec2-user@ip-10-0-101-177:~$ sudo systemctl start httpd
```

When you’re done, deregister the service:

```bash theme={null}
ec2-user@ip-10-0-101-177:~$ consul services deregister service.json
Deregistered service: web-server-01
```

> **lightbulb** The basic service definition offers no health checks, so Consul assumes it is always healthy.

***

## Adding a TCP Health Check

To ensure only healthy instances are returned by service discovery, update the definition to include a TCP health check on port 80. Save the following as `service-with-health.json`:

```json theme={null}
{
  "node_name": "web-server-01",
  "service": {
    "id": "web-server-01",
    "name": "front-end-eCommerce",
    "tags": ["v7.05", "production"],
    "address": "10.0.101.177",
    "port": 80,
    "check": {
      "id": "web",
      "name": "Check web on port 80",
      "tcp": "localhost:80",
      "interval": "10s",
      "timeout": "1s"
    }
  }
}
```

Register the enhanced service:

```bash theme={null}
ec2-user@ip-10-0-101-177:~$ consul services register service-with-health.json
Registered service: front-end-eCommerce
```

> **triangle-alert** Until the first TCP check passes, Consul marks the service as **failing** and will not return it in discovery queries.

***

## Observing Health Check Status

1. Open the [Consul UI](http://localhost:8500/ui).
2. Look for the **front-end-eCommerce** entry under **Services**.
3. If the check is still pending or failing, you’ll see a red “X” icon.

After approximately 10 seconds, Consul performs the TCP check against `localhost:80`. A successful connection flips the status to passing, indicated by a green checkmark.

### Simulating Failure and Recovery

To test Consul’s failure detection:

```bash theme={null}
ec2-user@ip-10-0-101-177:~$ sudo systemctl stop httpd
```

Within the next interval, the Consul UI shows the failure details:

| Check Name           | Status  | Output                                             |
| -------------------- | ------- | -------------------------------------------------- |
| Check web on port 80 | failed  | dial tcp 127.0.0.1:80: connect: connection refused |
| Serf Health Status   | passing | Agent alive and reachable                          |

Restart Apache to restore health:

```bash theme={null}
ec2-user@ip-10-0-101-177:~$ sudo systemctl start httpd
```

After the next 10-second interval, the TCP check passes and Consul marks the service as healthy again.

***

## Service Definition Comparison

| Feature                 | Basic Definition | With TCP Health Check                     |
| ----------------------- | ---------------- | ----------------------------------------- |
| `check` block           | Not present      | Present with `tcp`, `interval`, `timeout` |
| Initial health status   | Always passing   | Marked failing until first check          |
| Service discoverability | Immediate        | Delayed until healthy                     |

***

## Links and References

* [Consul Health Checks Documentation](https://www.consul.io/docs/health-checks)
* [Service Discovery with Consul](https://www.consul.io/docs/discovery)
* [Consul CLI Reference](https://www.consul.io/docs/commands)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/c93b029c-49ea-4720-b869-60ee503c5fce/lesson/4c363349-582a-4758-b624-557be75cc4c8)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/c93b029c-49ea-4720-b869-60ee503c5fce/lesson/eca5f924-71a3-45a5-961a-eb2184cfac93)


# Introduction to Prepared Queries

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Register-Services-and-Use-Service-Discovery/Introduction-to-Prepared-Queries/page

Prepared Queries in Consul enable advanced service discovery by filtering instances based on various criteria for reusable query execution.

Prepared Queries in [Consul](https://www.consul.io/) enable advanced service discovery by filtering instances based on health status, version tags, datacenter location, and more. Unlike basic DNS lookups, prepared queries let you define reusable query objects at the datacenter level and execute them via HTTP or DNS.

![The image is a slide titled "Introduction to Prepared Query," explaining the benefits and creation of complex service queries, with a pixelated design on the right side.](https://kodekloud.com/kk-media/image/upload/v1752877897/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Prepared-Queries/introduction-to-prepared-query-slide.jpg)

## Defining and Executing a Prepared Query

Prepared Queries are stored in Consul’s catalog by calling the `/v1/query` API endpoint:

```bash theme={null}
curl --request PUT \
     --data @my-query.json \
     http://localhost:8500/v1/query
```

Once registered, a query named `my-query` is available as:

* **DNS**: `my-query.query.consul`
* **HTTP API**: `GET /v1/query/<QueryID>/execute`

> **lightbulb** DNS queries to `*.query.consul` support standard A/AAAA record lookups and SRV records for service resolution.

## Filtering Services: A Dealership Analogy

Imagine you visit a car dealership with thousands of vehicles. You only want:

1. A car (not a truck)
2. Painted red
3. The latest model

By applying these filters, you narrow down the lot to your perfect match.

![The image is an illustration titled "Introduction to Prepared Query," showing a person saying "I need to connect to a service" with a service catalog containing various web apps and services.](https://kodekloud.com/kk-media/image/upload/v1752877898/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Prepared-Queries/introduction-to-prepared-query-illustration.jpg)

Similarly, a Consul client can request service instances and then filter by:

* **Health**: only passing health checks
* **Service**: e.g., `web-app`
* **Tags**: e.g., `v6.4`

### Example: `web-app-v64` Prepared Query

Save the following JSON to `web-app-v64-query.json`:

```json theme={null}
{
  "Name": "web-app-v64",
  "Service": {
    "Service": "web-app",
    "Tags": ["v6.4"],
    "OnlyPassing": true
  }
}
```

Register it:

```bash theme={null}
curl --request PUT \
     --data @web-app-v64-query.json \
     http://localhost:8500/v1/query
```

Now you can resolve `web-app-v64.query.consul` or call:

```bash theme={null}
GET /v1/query/<QueryID>/execute
```

## Multi-Datacenter Failover Policies

In federated environments, you may want your queries to automatically fail over to other datacenters if no local instances are healthy.

![The image illustrates a failover policy example involving cloud services like Azure and AWS, with various software icons and a character representing a user. It includes a diagram showing connections between different components and services.](https://kodekloud.com/kk-media/image/upload/v1752877900/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Prepared-Queries/failover-policy-cloud-services-diagram.jpg)

### Failover Policy Types

| Policy Type | Behavior                                                          | Key Configuration         |
| ----------- | ----------------------------------------------------------------- | ------------------------- |
| Static      | Try a fixed list of datacenters in order                          | `Datacenters`             |
| Dynamic     | Automatically select the nearest N datacenters by round-trip time | `NearestN`                |
| Hybrid      | First nearest N, then fallback to a static list                   | `NearestN`, `Datacenters` |

![The image describes different types of failover policies: Static, Dynamic, and Hybrid, each with specific configurations for handling service failovers. It also notes that failover policies prioritize returning a local service before using a federated data center.](https://kodekloud.com/kk-media/image/upload/v1752877901/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Prepared-Queries/failover-policies-static-dynamic-hybrid.jpg)

#### Static Failover Policy

```json theme={null}
{
  "Name": "web-app-v64",
  "Service": {
    "Service": "web-app",
    "Tags": ["v6.4"],
    "OnlyPassing": true,
    "Failover": {
      "Datacenters": ["dc2", "dc3"]
    }
  }
}
```

> Consul tries the local datacenter first, then `dc2`, then `dc3`.

#### Dynamic Failover Policy

```json theme={null}
{
  "Name": "web-app-v64",
  "Service": {
    "Service": "web-app",
    "Tags": ["v6.4"],
    "OnlyPassing": true,
    "Failover": {
      "NearestN": 2
    }
  }
}
```

> Consul measures round-trip time and queries the two nearest datacenters if the local ones have no healthy instances.

#### Hybrid Failover Policy

```json theme={null}
{
  "Name": "web-app-v64",
  "Service": {
    "Service": "web-app",
    "Tags": ["v6.4"],
    "OnlyPassing": true,
    "Failover": {
      "NearestN": 2,
      "Datacenters": ["dc2", "dc3"]
    }
  }
}
```

> **lightbulb** In a hybrid policy, each datacenter is queried at most once per execution.

## Comparing Service Discovery Methods

Consul supports three main ways to locate services:

| Method                         | Advantages                                      | Limitations                               |
| ------------------------------ | ----------------------------------------------- | ----------------------------------------- |
| DNS                            | Built-in, simple round-robin                    | No health or metadata filtering           |
| Prepared Queries               | Filter by tags, health, metadata                | Local datacenter only                     |
| Prepared Queries with Failover | All prepared query benefits + cross-DC failover | Requires federated topology configuration |

![The image compares options for querying services, highlighting DNS as simple but not flexible, Prepared Query as dynamic but local, and Failover Policy as ideal for multi-cloud apps. It features colorful arrows and a pixelated design at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752877902/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Prepared-Queries/querying-services-comparison-dns-prepared.jpg)

## References

* [Consul Prepared Queries](https://www.consul.io/docs/discovery/prepared-queries)
* [Consul HTTP API](https://www.consul.io/api-docs)
* [Service Discovery Concepts](https://www.consul.io/docs/intro/concepts)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/c93b029c-49ea-4720-b869-60ee503c5fce/lesson/057f639c-9fa3-4c67-951e-baf8f85f15c5)
