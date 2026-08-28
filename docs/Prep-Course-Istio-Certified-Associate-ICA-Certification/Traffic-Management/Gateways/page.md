# Gateways

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Gateways/page

Istio Gateways manage ingress and egress traffic, perform TLS termination, and use VirtualServices and DestinationRules to route and control traffic at the service mesh boundary

A Gateway is an entry point that controls traffic between the outside world and the Istio service mesh. Gateways are optional: if your workloads don't need external exposure, you can rely on VirtualServices alone. Use the Istio Operator to enable or disable gateway components as needed.

<Callout icon="lightbulb">
  Gateways are used only when you need to control ingress or egress traffic at the mesh boundary. Inside the mesh, VirtualServices and DestinationRules control routing and subsets.
</Callout>

## Types of Gateways

There are two primary Istio gateway types:

* Ingress Gateway — manages incoming traffic from outside the cluster into the Istio mesh.
* Egress Gateway — controls outgoing traffic from workloads inside the mesh to external services.

<Frame>
  <img alt="The image illustrates the architecture of an Ingress Gateway used to manage incoming traffic in a Kubernetes environment, showing components like Service, Replica Set, and Pods with containers." />
</Frame>

<Frame>
  <img alt="The image illustrates the concept of an Egress Gateway in Kubernetes, showing how outgoing traffic from pods within a namespace is managed and directed to external resources via the gateway." />
</Frame>

Istio installs ingress and (optionally) egress gateway components. For example, different Istio installation profiles (default, demo, minimal, etc.) include or exclude specific core components:

<Frame>
  <img alt="The image is a table showing Istio Profile Core Components across different profiles such as default, demo, minimal, remote, empty, preview, and ambient, with checkmarks indicating component inclusion." />
</Frame>

To verify installed gateway pods:

```bash theme={null}
