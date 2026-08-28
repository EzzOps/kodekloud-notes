# Ingress Networking

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Services-Networking/Ingress-Networking/page

This lesson covers Ingress networking in Kubernetes, explaining its functionality, advantages over traditional services, and how to deploy and configure it effectively.

Welcome to this lesson on Ingress networking in Kubernetes. In this guide, you will learn how Ingress works, how it differs from traditional service exposure, and when to use each approach. We will start by reviewing services and then show how Ingress offers a consolidated, efficient way to manage external access to your applications.

## Traditional Service Exposure

Imagine deploying an online store application accessible via "myonlinestore.com". Your application is containerized in Docker and deployed as a Pod within a Deployment on your Kubernetes cluster. Additionally, your architecture includes a MySQL database deployed as a Pod and exposed internally using a ClusterIP service for secure communication with your application.

To allow external access, you initially create a service of type NodePort. For instance, assigning port 38080 to your application enables users to access it by visiting:

http\://\[Node-IP]:38080

<Frame>
  ![The image illustrates a Kubernetes architecture with a NodePort service for "wear" pods and a ClusterIP service for a MySQL database.](https://kodekloud.com/kk-media/image/upload/v1752871298/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Ingress-Networking/frame_90.jpg)
</Frame>

As traffic increases, you simply scale up by increasing the replica count, and the service load-balances requests among the Pods.

For improved user experience, you would typically update your DNS to map to your node IPs, allowing access via myonlinestore.com:38080. However, requiring users to remember a port number is not ideal.

To simplify this, you can introduce a proxy server between your DNS and cluster that forwards HTTP traffic on port 80 to port 38080. With DNS pointing to the proxy server, users can then simply access your application using myonlinestore.com.

If you are leveraging public cloud platforms like Google Cloud Platform (GCP), you can opt for a LoadBalancer service instead of NodePort. When a LoadBalancer service is created, Kubernetes provisions a high port and triggers GCP to set up a network load balancer, assigning an external IP for DNS configuration. Users can then seamlessly access your application via myonlinestore.com.

## Scaling with Multiple Services

As your business expands, you may introduce additional services. For example, suppose you add a video streaming service accessible via myonlinestore.com/watch, while keeping your original application available at myonlinestore.com/wear. In this case, you might deploy them as separate Deployments in the same cluster. A service named "video-service" of type LoadBalancer could be created, and Kubernetes would provision a separate external port (such as 38082) along with a dedicated GCP load balancer for that service.

<Frame>
  ![The image illustrates a network architecture with a GCP load balancer directing traffic to "wear" and "video" services, each with multiple instances.](https://kodekloud.com/kk-media/image/upload/v1752871299/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Ingress-Networking/frame_310.jpg)
</Frame>

However, managing multiple load balancers increases both costs and administrative overhead, often requiring separate SSL configurations, firewall rules, and more.

## Enter Ingress

Ingress provides a streamlined solution by offering a single externally accessible URL that can handle SSL, authentication, and URL-based routing. Think of Ingress as a layer-seven load balancer running within your Kubernetes cluster, and it is configured with native Kubernetes objects. Although you still require an external exposure mechanism (via a NodePort or cloud LoadBalancer), all advanced load balancing and routing rules are managed centrally by the Ingress controller.

<Frame>
  ![The image illustrates a Google Cloud Platform ingress architecture with load balancing for "wear" and "video" services.](https://kodekloud.com/kk-media/image/upload/v1752871300/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Ingress-Networking/frame_440.jpg)
</Frame>

Without Ingress, you would have to manually configure reverse proxies or load balancers such as NGINX, HAProxy, or Traefik. Ingress automates these tasks by monitoring Kubernetes for new or updated Ingress resources.

## Ingress Controllers

Ingress requires two key components to function effectively:

1. **Ingress Controller:** A specialized implementation (for example, NGINX, HAProxy, or Traefik) that actively manages the underlying load balancing.
2. **Ingress Resources:** Kubernetes YAML definitions that specify routing rules for directing incoming traffic.

<Callout icon="lightbulb">
  Remember that a Kubernetes cluster does not include an Ingress controller by default – you must deploy one. In this lesson, we use NGINX as our example.
</Callout>

### Deploying an NGINX Ingress Controller

Below is an example of a Deployment configuration for the NGINX Ingress controller. This configuration creates a single replica of the NGINX controller with appropriate labels:

```yaml theme={null}
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-ingress-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      name: nginx-ingress
  template:
    metadata:
      labels:
        name: nginx-ingress
    spec:
      containers:
        - name: nginx-ingress-controller
          image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0
          args:
            - /nginx-ingress-controller
```

Next, create a ConfigMap to manage NGINX configurations. An initially empty ConfigMap allows you to modify settings later without the need to change configuration files on the container image:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configuration
```

A Service of type NodePort is then used to expose the Ingress controller to external traffic:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: nginx-ingress
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
      name: http
    - port: 443
      targetPort: 443
      protocol: TCP
      name: https
  selector:
    name: nginx-ingress
```

The following Deployment configuration further enhances the setup by including environment variables and explicit port definitions:

```yaml theme={null}
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-ingress-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      name: nginx-ingress
  template:
    metadata:
      labels:
        name: nginx-ingress
    spec:
      containers:
        - name: nginx-ingress-controller
          image: quay.io/kubernetes-ingress-nginx/controller
          args:
            - /nginx-ingress-controller
            - --configmap=$(POD_NAMESPACE)/nginx-configuration
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          ports:
            - name: http
              containerPort: 80
            - name: https
              containerPort: 443
```

Finally, create a ServiceAccount for the Ingress controller to manage access to the Kubernetes API:

```yaml theme={null}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress-serviceaccount
```

<Callout icon="lightbulb">
  Deploying an Ingress controller involves:

  * A Deployment for the NGINX Ingress controller.
  * A Service to expose it externally using NodePort.
  * A ConfigMap to manage controller configurations.
  * A ServiceAccount to authenticate and authorize the controller’s operations.
</Callout>

## Ingress Resources

An Ingress resource defines the rules that instruct the Ingress controller on routing incoming requests. There are three common scenarios:

1. **Default Backend:** Routes all traffic to a single backend service.
2. **Path-Based Routing:** Directs traffic based on URL path segments.
3. **Host-Based Routing:** Routes traffic according to the domain name in the request.

### Default Backend Example

The following Ingress resource routes all incoming traffic to the "wear-service" on port 80:

```yaml theme={null}
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-wear
spec:
  backend:
    serviceName: wear-service
    servicePort: 80
```

After applying this configuration, you can create and verify it using:

```bash theme={null}
kubectl create -f Ingress-wear.yaml
ingress.extensions/ingress-wear created

kubectl get ingress
NAME           HOSTS    ADDRESS    PORTS   AGE
ingress-wear   *        <none>     80      2s
```

### Path-Based Routing Example

For services accessible via specific URL paths (e.g., "/wear" and "/watch"), define an Ingress resource with multiple path rules:

```yaml theme={null}
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
  - http:
      paths:
      - path: /wear
        backend:
          serviceName: wear-service
          servicePort: 80
      - path: /watch
        backend:
          serviceName: watch-service
          servicePort: 80
```

Verify the configuration with the command below:

```bash theme={null}
kubectl describe ingress ingress-wear-watch
```

### Host-Based Routing Example

For routing based on domain names, specify the host field in your Ingress resource. The following example directs traffic for "wear.my-online-store.com" and "watch.my-online-store.com" to separate backend services:

```yaml theme={null}
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-host-based
spec:
  rules:
  - host: wear.my-online-store.com
    http:
      paths:
      - backend:
          serviceName: wear-service
          servicePort: 80
  - host: watch.my-online-store.com
    http:
      paths:
      - backend:
          serviceName: watch-service
          servicePort: 80
```

If the host field is omitted, the rule will match traffic from any host.

### Handling Unmatched Traffic

For requests that do not match any defined rules (for example, if a user navigates to myonlinestore.com/listen), it is recommended to set up a default backend. This backend can serve a custom 404 Not Found page or any other appropriate response.

## Summary

* **Services** (ClusterIP, NodePort, LoadBalancer) provide various ways to expose your applications.
* **Ingress** consolidates external access through a single URL, simplifying SSL termination, load balancing, and routing.
* Deploy an **Ingress Controller** (e.g., NGINX) to continuously monitor and update configurations based on Ingress resources.
* Define **Ingress Resources** with specific routing rules to direct incoming traffic to the correct backend services.

<Frame>
  ![The image illustrates deploying and configuring ingress controllers like NGINX, HAProxy, and Traefik, highlighting the steps: "Deploy Ingress Controller" and "Configure Ingress Resources."](https://kodekloud.com/kk-media/image/upload/v1752871301/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Ingress-Networking/frame_520.jpg)
</Frame>

<Frame>
  ![The image lists various ingress controllers: GCP HTTP(S) Load Balancer, NGINX, Contour, HAProxy, Traefik, and Istio.](https://kodekloud.com/kk-media/image/upload/v1752871302/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Ingress-Networking/frame_560.jpg)
</Frame>

In this lesson, we have explored different approaches to expose your application in Kubernetes and demonstrated how Ingress simplifies the management of external access. By using Ingress, you benefit from centralized load balancing, SSL termination, and efficient URL-based routing.

## Next Steps

In the practice test section, you will engage with two types of labs:

1. An environment where an Ingress controller, corresponding resources, and applications are already deployed. In this lab, you will explore existing configurations, gather important data, and answer relevant questions.
2. A more challenging lab where you will deploy an Ingress controller and configure Ingress resources from scratch.

Good luck, and enjoy your hands-on learning experience!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/58deb166-bc85-48c7-98d0-696f1f536fb6/lesson/0d9a96f1-daff-4449-9347-c5c67874870d" />
</CardGroup>
