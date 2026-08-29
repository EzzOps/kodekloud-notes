# List Istio system pods (example output)
$ kubectl get pods -n istio-system
NAME                                   READY   STATUS    RESTARTS   AGE
istio-egress-cfcd9bc96-p6nsg          1/1     Running   0          19s
istio-ingress-6cf77d4858-725nz        1/1     Running   0          23s
istiod-5fcb7d9676-vwfxj               1/1     Running   0          35s

# Inspect a specific ingress pod (labels may vary)
$ kubectl get pod -n istio-system istio-ingress-6cf77d4858-725nz -o wide
NAME                                   READY   STATUS    RESTARTS   AGE
istio-ingress-6cf77d4858-725nz        1/1     Running   0          113s
```

<Callout icon="warning">
  Gateway selector labels matter. The Gateway `spec.selector` must match the labels on the gateway pods (e.g., `istio=ingress`, `istio=ingressgateway`, or `istio=egress`). If the selector is wrong, traffic will not be handled by the intended Envoy pods.
</Callout>

## TLS termination and protocol support

Gateways are commonly used for TLS termination: the Envoy proxy at the mesh edge can decrypt incoming TLS traffic and forward plaintext traffic inside the mesh, or vice versa for egress. Gateways also support multiple protocols:

* HTTP / HTTPS
* TCP
* gRPC

<Frame>
  <img alt="The image illustrates a TLS termination process in a Kubernetes environment, highlighting the encryption and decryption of traffic at an ingress gateway and the flow within Kubernetes components like services, deployments, replica sets, and pods." />
</Frame>

<Frame>
  <img alt="The image illustrates three types of protocols: HTTP/S, TCP, and gRPC, each responsible for routing different types of traffic." />
</Frame>

## Example: VirtualService and DestinationRule (traffic splitting)

A VirtualService routes requests to one or more destinations. A DestinationRule defines subsets (versions) used by the VirtualService for traffic splitting.

VirtualService (50/50 split between `v1` and `v2`):

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ingress-app-vs
  namespace: frontend
spec:
  hosts:
    - app-svc
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: app-svc.frontend.svc.cluster.local
            port:
              number: 80
          subset: v1
          weight: 50
        - destination:
            host: app-svc.frontend.svc.cluster.local
            port:
              number: 80
          subset: v2
          weight: 50
```

DestinationRule defining subsets:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: app-ds
  namespace: frontend
spec:
  host: app-svc
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

## Exposing the app with an Ingress Gateway

To expose the frontend application externally you need a Gateway resource. The Gateway configures ports, protocols, and hostnames that the ingress Envoy pods will accept.

Example Ingress Gateway:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: ingress-app-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingress        # must match the gateway pod label exactly
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - app.example.com
```

Notes:

* The `selector` must match the labels on your ingress gateway pods (e.g., `istio: ingress` or `istio: ingressgateway`).
* In production, you will typically use port `443` and `HTTPS` with TLS settings, not port `80`.

To allow both internal and external access, add the gateway reference and external host to your VirtualService:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ingress-app-vs
  namespace: istio-system
spec:
  hosts:
    - app-svc
    - "app.example.com"
  gateways:
    - ingress-app-gateway
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: app-svc.frontend.svc.cluster.local
            port:
              number: 80
          subset: v1
          weight: 50
        - destination:
            host: app-svc.frontend.svc.cluster.local
            port:
              number: 80
          subset: v2
          weight: 50
```

* When workloads inside the mesh call `app-svc.frontend.svc.cluster.local`, the VirtualService applies the 50/50 split internally.
* When external users access `app.example.com`, the Gateway matches the host and the same VirtualService routes the request through the ingress gateway into the mesh.

### Incoming traffic flow

1. External client sends HTTP/HTTPS to the Ingress Gateway public IP (DNS: `app.example.com`).
2. Envoy (ingress pod) receives and decrypts if required.
3. Envoy consults the Gateway configuration to determine applicable ports/protocols.
4. The Gateway references a VirtualService to select the route based on host and path.
5. Envoy forwards to the Kubernetes Service and workload; response returns to client.

<Frame>
  <img alt="The image shows a diagram of an incoming traffic flow in a network system, detailing the process from an external HTTP/HTTPS request to the final response. It includes steps involving an ingress gateway, envoy proxy verification, consultation of a virtual service, and forwarding to a workload service." />
</Frame>

<Callout icon="lightbulb">
  Remember: An ingress Gateway requires a VirtualService to route traffic into the mesh. A VirtualService can operate independently for internal routing without a Gateway.
</Callout>

## Egress Gateway

An egress gateway centralizes outbound traffic from the mesh, letting you enforce policies, monitor exits, or lock outbound hosts.

Example Egress Gateway listening on 80 and 443:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: egress-app-gateway
  namespace: istio-system
spec:
  selector:
    istio: egress
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "*"
    - port:
        number: 443
        name: https
        protocol: HTTPS
      hosts:
        - "*"
```

* Using `"*"` (wildcard) allows all outgoing hosts through the egress gateway.
* Alternatively, list specific hosts to restrict egress to approved external endpoints.

VirtualService forcing traffic through the egress gateway (example for `api.example.com` on port 443):

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: egress-app-vs
  namespace: frontend
spec:
  hosts:
    - api.example.com
  gateways:
    - egress-app-gateway
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: api.example.com
            port:
              number: 443
```

* Workloads in the `frontend` namespace that want to call `api.example.com` will be required to go through the egress gateway and use HTTPS on port 443.

### Outgoing traffic flow

1. Workload sends outbound traffic; sidecar Envoy intercepts.
2. Envoy routes outbound traffic to the egress gateway (based on VirtualService).
3. Egress gateway applies policies, monitoring, and any TLS egress behavior.
4. Egress gateway forwards to external destination; responses return through the gateway to the originating workload.

<Frame>
  <img alt="The image is a diagram showing an outgoing traffic flow involving Envoy Proxy intercepting outbound traffic, routing it to an Egress Gateway, processing the request, and handling responses from external clients." />
</Frame>

Egress gateways are less commonly used in many organizations because networking stacks (VPCs, firewalls, NATs) already provide egress control. However, an Istio egress gateway is useful for centralized visibility, policy enforcement, or strict regulatory environments.

## Gateway capabilities and options

Gateways can configure:

* Ports and protocols (HTTP, HTTPS, TCP, gRPC).
* TLS modes and certificate handling (TLS termination / passthrough / mutual TLS).
* Host matching and SNI routing.
* Per-server TLS settings and redirects.

Refer to the official Gateway reference for details and examples:

* Reference: [https://istio.io/latest/docs/reference/config/networking/gateway/](https://istio.io/latest/docs/reference/config/networking/gateway/)

<Frame>
  <img alt="The image shows a diagram of &#x22;Gateway Options&#x22; related to server configurations, including sections on TLS mode, port, and server TLS settings, each with descriptive fields. It appears to be a reference guide from KodeKloud." />
</Frame>

<Callout icon="lightbulb">
  Study the Gateway options and examples in the Istio docs—this topic appears on the Istio Certified Associate exam. Practice creating Gateways and the related VirtualServices/DestinationRules in a lab environment.
</Callout>

## Quick reference table

| Resource Type   |                                                            Purpose | Example                                                                    |
| --------------- | -----------------------------------------------------------------: | -------------------------------------------------------------------------- |
| Gateway         |              Configure edge Envoy listeners and host/port bindings | `apiVersion: networking.istio.io/v1` Gateway YAML (see above)              |
| VirtualService  | Routing rules for requests (host/path matching, traffic splitting) | `apiVersion: networking.istio.io/v1alpha3` VirtualService YAML (see above) |
| DestinationRule |                   Define subsets and traffic policies for services | `apiVersion: networking.istio.io/v1` DestinationRule YAML (see above)      |

Links and references:

* Istio Gateway docs: [https://istio.io/latest/docs/reference/config/networking/gateway/](https://istio.io/latest/docs/reference/config/networking/gateway/)
* VirtualService docs: [https://istio.io/latest/docs/reference/config/networking/virtual-service/](https://istio.io/latest/docs/reference/config/networking/virtual-service/)
* DestinationRule docs: [https://istio.io/latest/docs/reference/config/networking/destination-rule/](https://istio.io/latest/docs/reference/config/networking/destination-rule/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/0ebb40cd-28de-4216-9dc7-9aa26eb3640d" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Introduction/page

Overview of Istio traffic management concepts and exam-focused module covering sidecars, virtual services, destination rules, ingress/egress, resilience techniques, traffic routing, mirroring, and ambient mode

This is the most important module and the longest, so let's dive

into what we're going to cover in this module.

This module examines sidecars, focusing on the resource and its default behavior.

Virtual services, possibly the most important resource in the Istio service mesh.

I would say that around 30 to 35% of all the questions

you're going to get in the ICA

exam will involve a virtual service.

And if we're talking about importance, I guess second

on the list would be DestinationRules.

This is a must-know for the ICA exam.

<Frame>
  <img alt="The image outlines three objectives: discussing sidecar resource configuration and behavior, understanding traffic routing using Virtual Services, and demonstrating subsets and load balancing with Destination Rules." />
</Frame>

This is where splitting traffic is configured.

We'll talk about exposing applications to the public using ingress gateways and

also outgoing traffic using egress gateways.

We'll talk about how we can introduce external services, something like a

database or a web app, and bring it

into the service mesh using ServiceEntries.

We'll talk about the pros and cons to various release methods and

show you a better way called Istio traffic mirroring or A/B testing.

We'll be talking about the issues that can happen in a microservices

stack and how they can be avoided using circuit breaking.

We'll look at how we can prevent

cascading failures when those bottlenecks happen.

Resilience isn't just about avoiding issues, but more about being prepared

for them when they do happen.

And fault injection is the answer.

We'll look at intentionally implementing delays and aborts

to see how the application behaves.

We're going to be using timeouts and retries as

a safety measure for those errors.

And finally, after we talked about all of these different Istio resources,

we'll have a look at how to set up ambient mode and

<Frame>
  <img alt="The image lists objectives numbered 09 to 11, including simulating delays, using timeouts and retries, and Istio’s new Ambient Mode. The text is placed alongside a gradient blue sidebar labeled &#x22;Objectives.&#x22;" />
</Frame>

go over a demo on how to use layer 4 traffic using

ztunnels and layer 7 traffic using the waypoint proxies, using HTTPRoutes.

Although I should mention again that none of this is going to

be in the actual ICA exam.

And by this, I mean the actual ambient mode.

So we're not going to deep dive

into, you know, HTTPRoutes and EnvoyFilters.

We are going to cover ambient mode, but the exam

does not go in too deep.

So we're not going to go in too deep into ambient mode.

And, you know, there's a lot to cover in this module.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/893af7d0-5bba-4293-a566-6f825e03196e" />
</CardGroup>
