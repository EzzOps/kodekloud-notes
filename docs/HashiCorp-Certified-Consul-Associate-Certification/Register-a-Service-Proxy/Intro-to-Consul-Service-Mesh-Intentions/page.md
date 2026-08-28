# /etc/consul.d/config.hcl
log_level          = "INFO"
node_name          = "consul-node-a"
server             = true
ui                 = true
leave_on_terminate = true
data_dir           = "/etc/consul.d/data"
datacenter         = "us-east-1"
client_addr        = "0.0.0.0"
bind_addr          = "10.0.101.110"
advertise_addr     = "10.0.101.110"
retry_join         = ["10.0.101.248"]
bootstrap_expect   = 2
enable_syslog      = true

connect {
  enabled     = true
  performance {
    raft_multiplier = 1
  }
}
```

Save and restart Consul:

```bash theme={null}
sudo systemctl restart consul
```

Repeat on **consul-node-b**, adjusting `node_name`, `bind_addr`, `advertise_addr`, and `retry_join`. When both nodes are up, verify membership:

```bash theme={null}
consul members
```

<Frame>
  ![The image shows a computer screen with a terminal window open, displaying a command prompt, and a web browser tab showing a Consul services page with one service listed.](https://kodekloud.com/kk-media/image/upload/v1752877907/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/computer-terminal-command-prompt-consul-services.jpg)
</Frame>

## 2. Register and Configure Services

Now register the two application services on separate web servers:

| Service   | Node      | Port | Definition File |
| --------- | --------- | ---- | --------------- |
| counting  | counting  | 9003 | counting.hcl    |
| dashboard | dashboard | 9002 | dashboard.hcl   |

<Frame>
  ![The image shows a web interface for HashiCorp Consul, displaying a services page with one service named "consul" and two instances.](https://kodekloud.com/kk-media/image/upload/v1752877908/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/hashicorp-consul-services-page-instance.jpg)
</Frame>

### 2.1 Counting Service

On the **counting** server, create `counting.hcl`:

```hcl theme={null}
# counting.hcl
node_name = "counting"

service {
  name = "counting"
  id   = "counting-1"
  port = 9003

  connect {
    sidecar_service {}
  }

  check {
    id       = "counting-check"
    http     = "http://localhost:9003/health"
    method   = "GET"
    interval = "1s"
    timeout  = "1s"
  }
}
```

Register it:

```bash theme={null}
consul services register counting.hcl
```

### 2.2 Dashboard Service

On the **dashboard** server, create `dashboard.hcl`:

```hcl theme={null}
# dashboard.hcl
node_name = "dashboard"

service {
  name = "dashboard"
  port = 9002

  connect {
    sidecar_service {
      proxy {
        upstreams = [
          {
            destination_name = "counting"
            local_bind_port  = 5000
          }
        ]
      }
    }
  }

  check {
    id       = "dashboard-check"
    http     = "http://localhost:9002/health"
    method   = "GET"
    interval = "15s"
    timeout  = "1s"
  }
}
```

Register it:

```bash theme={null}
consul services register dashboard.hcl
```

<Callout icon="lightbulb">
  Services are registered immediately but not yet running—health checks will show “critical” until the application and proxy start.
</Callout>

## 3. Start Services and Sidecar Proxies

Launch each application and its sidecar proxy so traffic is routed via Consul Connect.

### 3.1 Counting Service & Proxy

On the **counting** server:

```bash theme={null}
export PORT=9003
./counting-service &

# Start Consul sidecar proxy for counting
consul connect proxy --sidecar-for counting-1 > counting-proxy.log &
```

Check the status in Consul’s UI:

<Frame>
  ![The image shows a Consul web interface displaying service details for "counting-1" on a node named "web-server-01," including health checks and status information.](https://kodekloud.com/kk-media/image/upload/v1752877910/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/consul-web-interface-counting-1-status.jpg)
</Frame>

### 3.2 Dashboard Service & Proxy

On the **dashboard** server:

```bash theme={null}
export PORT=9002
export COUNTING_SERVICE_URL="http://localhost:5000"
./dashboard-service &

# Start Consul sidecar proxy for dashboard
consul connect proxy --sidecar-for dashboard > dashboard-proxy.log &
```

Now both sidecars are active and enforce mTLS.

## 4. Verify Connectivity

Open your browser to `http://<dashboard-node-ip>:9002` and refresh the page. You should see the counter increment via the proxy:

<Frame>
  ![The image shows a computer screen displaying a dashboard with a large number "1" and an IP address. There are multiple browser tabs open, and a terminal window is visible in the background.](https://kodekloud.com/kk-media/image/upload/v1752877910/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/computer-dashboard-ip-address-browser-tabs.jpg)
</Frame>

In the Consul UI you’ll also see the service topology and traffic distribution:

<Frame>
  ![The image shows a Consul dashboard interface displaying a service topology with a connection between "dashboard" and "counting" services. The "counting" service has a load distribution of 75% and 25%.](https://kodekloud.com/kk-media/image/upload/v1752877912/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/consul-dashboard-service-topology-75-25.jpg)
</Frame>

Monitor overall health checks:

<Frame>
  ![The image shows a web interface displaying various service health checks, including details like service names, check IDs, types, and outputs. It appears to be part of a monitoring or management dashboard for network services.](https://kodekloud.com/kk-media/image/upload/v1752877913/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/service-health-checks-dashboard-interface.jpg)
</Frame>

## 5. Manage Intentions

By default, Consul permits all service-to-service calls. Use **intentions** to enforce allow/deny policies.

Create a new intention to allow **dashboard → counting**:

<Frame>
  ![The image shows a web interface for creating a new intention in a service management tool, with options to select source and destination services, and to allow or deny connections.](https://kodekloud.com/kk-media/image/upload/v1752877914/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/service-management-tool-intention-creation.jpg)
</Frame>

Once saved, you’ll see it in the UI:

<Frame>
  ![The image shows a web interface for managing service intentions in HashiCorp Consul, displaying a permission setting from "dashboard" to "counting" with an "Allow" action.](https://kodekloud.com/kk-media/image/upload/v1752877916/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/hashicorp-consul-service-intentions-dashboard.jpg)
</Frame>

To test a deny rule, switch the intention to **Deny**:

<Frame>
  ![The image shows a web interface for editing service intentions, with options to allow, deny, or set application-aware connections between a source and destination service. The user is about to save the configuration.](https://kodekloud.com/kk-media/image/upload/v1752877917/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Service-Mesh/web-interface-editing-service-intentions.jpg)
</Frame>

Save and refresh the dashboard—updates stop, confirming the proxy enforces your policy. Revert to **Allow** to resume traffic.

## Conclusion

You’ve successfully:

* Enabled **Consul Connect** for mutual TLS service mesh
* Registered services with sidecar proxies
* Started applications and proxies
* Verified secure communication
* Managed traffic via **intentions**

Consul’s service mesh lets you implement fine-grained security and traffic policies without modifying application code. Happy networking!

***

## Links and References

* [Consul Connect Documentation](https://www.consul.io/docs/connect)
* [Intentions in Consul](https://www.consul.io/docs/connect/intentions)
* [HashiCorp Learn: Service Mesh Tutorial](https://learn.hashicorp.com/tutorials/consul/service-mesh)
* [Consul CLI Reference](https://www.consul.io/docs/commands)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/be057676-1d98-4d78-89c8-b8be2a9c2967/lesson/2e25754f-8976-44e6-9108-94aa3e1768b7" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/be057676-1d98-4d78-89c8-b8be2a9c2967/lesson/88e0f50a-4cce-457e-bc5f-bf5fe2d298a8" />
</CardGroup>


# Intro to Consul Service Mesh Intentions

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Register-a-Service-Proxy/Intro-to-Consul-Service-Mesh-Intentions/page

This article explains how Intentions in a Consul service mesh control service communication and access through application layer enforcement.

In a Consul service mesh, **Intentions** govern which services can communicate by enforcing access control at the application layer. Using a service graph, Intentions ensure only permitted traffic flows between sidecar proxies or natively integrated applications.

<Frame>
  ![The image is a slide about "Consul Service Mesh - Intentions," explaining how intentions define access control for services and how they are enforced. It includes details on service graphs, inbound connections, proxy requests, and default ACL policy behavior.](https://kodekloud.com/kk-media/image/upload/v1752877918/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Intro-to-Consul-Service-Mesh-Intentions/consul-service-mesh-intentions-slide.jpg)
</Frame>

Intentions are enforced at the **destination** (the upstream or target service) during inbound connections:

* With a default ACL policy of **Allow All**, every service-to-service call succeeds unless you explicitly add a Deny Intention.
* With **Deny All**, no traffic is allowed until you create specific Allow Intentions.

<Callout icon="triangle-alert">
  If you switch to `Deny All`, all existing service calls will be blocked until you configure Allow Intentions.
</Callout>

When multiple Intentions match a communication path, Consul applies the **first** matching rule in a top-down evaluation. Only one Intention controls authorization at any time.

***

## Building Your Service Graph with Intentions

Every service registers in Consul’s catalog—usually alongside a Sidecar Proxy. As you define Intentions, Consul dynamically constructs a **service graph** illustrating permitted interactions.

Consider these common policies:

* **Allow the web application to call the Platform API**\
  Create an Allow Intention from `web-app` → `platform-api` for encrypted, authenticated traffic.
* **Allow the search service to query the database**\
  Define an Allow Intention from `search-service` → `database` so search can read data.
* **Deny Inventory service access to Identity service**\
  Add a Deny Intention from `inventory` → `identity` to block all inventory instances.

<Frame>
  ![The image illustrates a Consul Service Mesh with a focus on "Intentions," showing a service catalog and a service graph with connections between various applications and databases. It includes icons for web applications, microservices, databases, and other components, highlighting interactions and permissions.](https://kodekloud.com/kk-media/image/upload/v1752877919/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Intro-to-Consul-Service-Mesh-Intentions/consul-service-mesh-intentions-diagram.jpg)
</Frame>

Since Consul enforces **identity-based authorization**, you reference services by name—not IP address. Any number of instances (containers, VMs, etc.) of a service automatically share the same permissions.

<Frame>
  ![The image illustrates a Consul Service Mesh with a focus on "Intentions," showing a service catalog and a service graph with various applications and their interactions, including allowed and denied connections.](https://kodekloud.com/kk-media/image/upload/v1752877920/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Intro-to-Consul-Service-Mesh-Intentions/consul-service-mesh-intentions-diagram-2.jpg)
</Frame>

***

## Intentions Precedence and Match Order

Intentions are prioritized by a **precedence** value; higher numbers are evaluated first. Consul processes rules top-down and stops at the first match for both source and destination services.

<Frame>
  ![The image is a slide about "Consul Service Mesh - Intentions," explaining precedence and match order with a table showing rules and their precedence levels. It highlights a top-down ruleset using "Allow" or "Deny" intentions, with precedence that cannot be overridden.](https://kodekloud.com/kk-media/image/upload/v1752877922/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Intro-to-Consul-Service-Mesh-Intentions/consul-service-mesh-intentions-ruleset.jpg)
</Frame>

***

## Protocol Enforcement: Layer 4 vs. Layer 7

Consul supports two enforcement modes, depending on your proxy and application protocol:

| Enforcement Layer | Mechanism                  | Key Capabilities                                 |
| ----------------- | -------------------------- | ------------------------------------------------ |
| Layer 4 (L4)      | Consul’s built-in proxy    | Identity-based TCP allow/deny on new connections |
| Layer 7 (L7)      | Envoy or advanced sidecars | HTTP-aware policies (paths, headers, methods)    |

<Callout icon="lightbulb">
  To use Layer 7 Intentions, integrate [Envoy](https://www.envoyproxy.io) or another HTTP-aware proxy with Consul.
</Callout>

<Frame>
  ![The image is a slide about "Consul Service Mesh - Intentions," focusing on controlling authorization using L4 (identity-based) and L7 (application-aware) protocols. It includes a decorative pixelated design on the right and a cartoon character at the bottom right.](https://kodekloud.com/kk-media/image/upload/v1752877923/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Intro-to-Consul-Service-Mesh-Intentions/consul-service-mesh-intentions-slide-2.jpg)
</Frame>

***

## Further Reading

* [Consul Intentions Documentation](https://www.consul.io/docs/enterprise/connect/intentions)
* [Consul ACL Overview](https://www.consul.io/docs/security/acl)
* [Envoy Proxy Documentation](https://www.envoyproxy.io)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/be057676-1d98-4d78-89c8-b8be2a9c2967/lesson/cb709e82-467c-4dbf-98b5-37acfe5766b8" />
</CardGroup>
