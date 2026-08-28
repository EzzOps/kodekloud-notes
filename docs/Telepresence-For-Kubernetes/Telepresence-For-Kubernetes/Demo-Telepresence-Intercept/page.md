# 1. Download Telepresence (~50 MB)
Invoke-WebRequest `
  https://app.getambassador.[AWS_SECRET_ACCESS_KEY].20.0/telepresence-windows-amd64.zip `
  -OutFile telepresence.zip

# 2. Extract and remove archive
Expand-Archive -Path telepresence.zip -DestinationPath telepresenceInstaller/telepresence
Remove-Item telepresence.zip
cd telepresenceInstaller/telepresence

# 3. Run installer script
powershell.exe -ExecutionPolicy Bypass -File .\install-telepresence.ps1

# 4. Cleanup
cd ../..
Remove-Item telepresenceInstaller -Recurse -Force

# 5. Verify installation
telepresence --help
```

***

## 5. Deploying the Telepresence Traffic Manager

Telepresence uses [Helm](https://helm.sh/) to install its Traffic Manager. Simply run:

```bash theme={null}
telepresence helm install
```

This creates the `ambassador` namespace and deploys the traffic manager pods.

```bash theme={null}
kubectl get ns
# ...       
kubectl get pods -n ambassador
# traffic-manager-xxxxx  1/1  Running
```

***

## 6. Connecting to the Cluster

Establish a VPN-like tunnel between your laptop and the Kubernetes cluster:

```bash theme={null}
telepresence connect
```

Check connection status:

```bash theme={null}
telepresence status
```

You’ll see details on:

* Connection status
* Active Kubernetes context & namespace
* Routes for service and pod CIDRs
* DNS proxy configuration
* Traffic Manager health

<Callout icon="lightbulb">
  Ensure you have cluster-wide permissions to deploy the Traffic Manager via Helm. You may need a cluster-admin role.
</Callout>

***

## 7. Reviewing Cluster Services Locally

With Telepresence active, your laptop now behaves like a pod:

```bash theme={null}
kubectl get svc
```

Example output:

```plaintext theme={null}
NAME                TYPE           CLUSTER-IP      EXTERNAL-IP                                           PORT(S)
auth-service        ClusterIP      10.100.10.52    <none>                                                3000/TCP
inventory-service   ClusterIP      10.100.246.69   <none>                                                3000/TCP
products-service    LoadBalancer   10.100.169.75   a4519082e1ab846e38b3d9760c9e3b9-515600148.us-east-1.elb.amazonaws.com   3000:30782/TCP
kubernetes          ClusterIP      10.100.0.1      <none>                                                443/TCP
```

***

## 8. Testing DNS Resolution

Verify Kubernetes DNS from your laptop:

```bash theme={null}
nslookup auth-service
```

```plaintext theme={null}
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   auth-service.default.svc.cluster.local
Address: 10.100.10.52
```

***

## 9. Curling Services Locally

### Auth Service

```bash theme={null}
curl http://auth-service:3000
```

```json theme={null}
{"message":"this is the auth service"}
```

### Products Service

```bash theme={null}
curl "http://products-service:3000?product_ids=1,2,3"
```

```json theme={null}
{
  "data": [
    {"id":1,"name":"iPhone 14","price":900,"category":"electronics","onSale":false,"inventoryCount":893},
    {"id":2,"name":"Samsung 40in TV","price":500,"category":"electronics","onSale":true,"inventoryCount":902},
    {"id":3,"name":"Apple MacbookPro","price":2500,"category":"electronics","onSale":false,"inventoryCount":444}
  ]
}
```

***

## 10. Accessing a Pod by IP

1. List pods with IPs:

   ```bash theme={null}
   kubectl get pod -o wide
   ```

2. Curl the pod directly:

   ```bash theme={null}
   curl http://192.168.32.69:3000
   ```

   ```json theme={null}
   {"message":"this is the auth service"}
   ```

***

## 11. Disconnecting Telepresence

When you’ve finished testing, terminate the connection:

```bash theme={null}
telepresence quit
```

Confirm disconnection:

```bash theme={null}
telepresence status
# Status: Disconnected
```

***

## Links and References

* Telepresence: [https://www.telepresence.io/](https://www.telepresence.io/)
* Kubernetes Basics: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* Helm: [https://helm.sh/](https://helm.sh/)
* AWS EKS: [https://aws.amazon.com/eks/](https://aws.amazon.com/eks/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/telepresence-for-kubernetes/module/0eb5dcb6-2e2a-40d9-9caa-bd3149741aeb/lesson/d76ac3de-46c7-464e-8da6-43d4e332c65d" />
</CardGroup>


# Demo Telepresence Intercept

Source: https://notes.kodekloud.com/docs/Telepresence-For-Kubernetes/Telepresence-For-Kubernetes/Demo-Telepresence-Intercept/page

Learn to use Telepresence for intercepting Kubernetes service traffic and running workloads locally for efficient debugging.

In this lesson, you’ll learn how to use Telepresence to intercept traffic from a Kubernetes service and run the workload locally for fast, iterative debugging.

<Frame>
  ![The image shows a Visual Studio Code interface with a terminal open, displaying a command prompt connected via SSH. The file explorer on the left lists several project files and directories.](https://kodekloud.com/kk-media/image/upload/v1752884089/notes-assets/images/Telepresence-For-Kubernetes-Demo-Telepresence-Intercept/vscode-terminal-ssh-file-explorer.jpg)
</Frame>

## Prerequisites

* A Kubernetes cluster and `kubectl` configured to the correct context
* Telepresence CLI installed (`brew install telepresence` or see the [official docs](https://www.telepresence.io/docs/))
* Node.js (v14+) and npm

<Callout icon="lightbulb">
  Make sure your Kubernetes context is set to the target namespace, and you have permissions to create interceptions.
</Callout>

## 1. List Your Deployments

Identify the deployment you want to intercept:

```bash theme={null}
kubectl get deployment
