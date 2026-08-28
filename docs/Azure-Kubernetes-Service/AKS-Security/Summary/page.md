# Create a resource group
az group create -l southeastasia -n kodekloud-osmdemo-rg

# Create AKS cluster with the OSM add-on
az aks create \
  -g kodekloud-osmdemo-rg \
  -n kk-aks-osmdemo \
  --enable-addons open-service-mesh
```

### 2. Configure kubectl Context

```bash theme={null}
# Fetch AKS credentials
az aks get-credentials -g kodekloud-osmdemo-rg -n kk-aks-osmdemo

# Confirm the current context
kubectl config current-context
```

### 3. Create Namespaces and Onboard to OSM

```bash theme={null}
# Create application namespaces
kubectl create ns bookbuyer bookstore bookwarehouse

# Add namespaces to the mesh
osm namespace add bookbuyer bookstore bookwarehouse
```

### 4. Deploy Sample Applications

```bash theme={null}
# Deploy the Book Buyer client
kubectl apply -f https://raw.githubusercontent.com/openservicemesh/osm/release-v0.11/docs/example/manifests/apps/bookbuyer.yaml

# Deploy Bookstore V1
kubectl apply -f https://raw.githubusercontent.com/openservicemesh/osm/release-v0.11/docs/example/manifests/apps/bookstore.yaml

# Deploy the Book Warehouse
kubectl apply -f https://raw.githubusercontent.com/openservicemesh/osm/release-v0.11/docs/example/manifests/apps/bookwarehouse.yaml
```

Wait for the Book Buyer pod:

```bash theme={null}
kubectl get pods -n bookbuyer -w
```

### 5. Port-Forward and Verify Default Traffic

```bash theme={null}
# Retrieve the Book Buyer pod name
POD=$(kubectl get pod -n bookbuyer -l app=bookbuyer -o jsonpath='{.items[0].metadata.name}')

# Forward local port 8081 to the sidecar port
kubectl port-forward -n bookbuyer $POD 8081:14001
```

Open `http://localhost:8081` to see Book Buyer successfully fetching from Bookstore V1 under OSM’s permissive policy.

<Callout icon="lightbulb">
  Permissive mode allows all services in the mesh to communicate without explicit SMI traffic policies.
</Callout>

### 6. Disable Permissive Traffic Policy

In the Azure Portal under **AKS → Open Service Mesh → Configuration**, update:

```yaml theme={null}
traffic:
  enableEgress: true
  enablePermissiveTrafficPolicyMode: false
```

After saving, Book Buyer will fail to reach Bookstore V1.

```bash theme={null}
kubectl logs -n bookbuyer $POD
# Look for denied request errors.
```

<Callout icon="triangle-alert">
  Disabling permissive mode without defining traffic policies will block all inter-service communication.
</Callout>

### 7. Apply Explicit Allow Traffic Policy

```bash theme={null}
kubectl apply -f https://raw.githubusercontent.com/openservicemesh/osm-docs/release-v1.2/manifests/access/traffic-access-v1.yaml
```

This SMI policy permits Book Buyer to call Bookstore. Reload `http://localhost:8081` to confirm connectivity.

### 8. Demonstrate Traffic Splitting

Create `traffic-split.yaml`:

```yaml theme={null}
apiVersion: split.smi-spec.io/v1alpha2
kind: TrafficSplit
metadata:
  name: bookstore-split
  namespace: bookstore
spec:
  service: bookstore
  backends:
    - service: bookstore-v1
      weight: 500m
    - service: bookstore-v2
      weight: 500m
```

Apply the split:

```bash theme={null}
kubectl apply -f traffic-split.yaml
```

Refresh the Book Buyer page—traffic should now be distributed evenly between V1 and V2. Adjust the `weight` values to shift more traffic to a particular version.

<Frame>
  ![The image shows a webpage titled "Bookbuyer" displaying the total number of books bought (567), with 520 from bookstore V1 and 47 from bookstore V2. The current time is also shown at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752869447/notes-assets/images/Azure-Kubernetes-Service-Open-Service-Mesh/bookbuyer-total-books-bought-webpage.jpg)
</Frame>

***

## References

* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Open Service Mesh (OSM) Documentation](https://openservicemesh.io/docs/)
* [SMI Specifications](https://smi-spec.io/)

## Further Reading

* [Azure Kubernetes Service Documentation](https://docs.microsoft.com/azure/aks/)
* [Envoy Proxy](https://www.envoyproxy.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/d229c32e-4ff2-47ce-8be7-3dd99d62753f/lesson/772dadb6-bef5-485f-ae96-551e351cb395" />
</CardGroup>


# Summary

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/AKS-Security/Summary/page

This module dives into the core components and best practices for strengthening the security posture of your AKS cluster.

<Callout icon="lightbulb">
  This module dives into the core components and best practices for strengthening the security posture of your AKS cluster.
</Callout>

1. **Azure Networking Fundamentals**
   * Design and configure Virtual Networks (VNets), subnets, and [Network Security Groups (NSGs)](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview)
   * Leverage private clusters and service endpoints to isolate AKS control plane and workloads

2. **AKS Networking Modes**
   * Kubernetes’ built-in kube-proxy with basic networking
   * Azure Container Networking Interface (CNI) for advanced IP management and VNet integration

3. **Network Policies**
   * Apply Calico or Azure-native policies for granular pod-to-pod and namespace traffic control
   * Enforce egress and ingress rules to limit attack surfaces

4. **Service Mesh Integration**
   * Implement Istio or [Open Service Mesh (OSM)](https://learn.microsoft.com/azure/aks/open-service-mesh-overview)
   * Gain mutual TLS, traffic encryption, observability, and policy enforcement

5. **Identity and Access Management (IAM)**
   * Integrate Azure Active Directory (AAD) for user and service principal authentication
   * Define Role-Based Access Control (RBAC) for least-privilege permissions
   * Secure the Kubernetes API with Azure Private Link and Managed Identities

6. **Azure Defender for Containers**
   * Enable threat protection to detect anomalous behavior and suspicious activity
   * Monitor vulnerabilities in container images and running workloads via Microsoft Defender

7. **Azure Policy for AKS Governance**
   * Enforce compliance rules on resource configurations, container image sources, and network settings
   * Implement policy initiatives for audit, deny, or append actions on non-conforming resources

<Callout icon="triangle-alert">
  CI/CD pipelines for AKS will be covered in the upcoming module. Plan your DevSecOps workflows to automate security checks and deployments.
</Callout>

## Links and References

* [Azure Virtual Network Documentation](https://learn.microsoft.com/azure/virtual-network/)
* [AKS Networking Overview](https://learn.microsoft.com/azure/aks/concepts-network)
* [Network Policies in Kubernetes](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Azure Defender for Containers](https://learn.microsoft.com/azure/defender-for-cloud/containers-introduction)
* [Azure Policy Overview](https://learn.microsoft.com/azure/governance/policy/overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/d229c32e-4ff2-47ce-8be7-3dd99d62753f/lesson/c7e36228-f57b-4188-82dc-e050b89dde88" />
</CardGroup>
