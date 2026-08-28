# Retrieve the Istio Ingress Gateway NodePort for port 80
PORT=$(kubectl -n istio-system get svc istio-ingressgateway -o json \
  | jq '.spec.ports[] | select(.port == 80) | .nodePort')

if [[ -z "$PORT" ]]; then
  echo "Error: Istio Ingress Gateway port 80 is not exposed as a NodePort."
  exit 1
fi

applicationURL="http://devsecops-demo.eastus.cloudapp.azure.com"
applicationURI="/increment/99"

echo "Using port: $PORT"
echo "Calling: $applicationURL:$PORT$applicationURI"

# Perform the increment test
response=$(curl -s "$applicationURL:$PORT$applicationURI")
http_code=$(curl -s -o /dev/null -w "%{http_code}" "$applicationURL:$PORT$applicationURI")

if [[ "$response" == "100" ]]; then
  echo "Increment Test Passed"
else
  echo "Increment Test Failed: expected '100', got '$response'"
  exit 1
fi

# Validate HTTP status code
if [[ "$http_code" == "200" ]]; then
  echo "HTTP Status Code Test Passed"
else
  echo "HTTP Status Code Test Failed: $http_code"
  exit 1
fi
```

## Complete Jenkins Pipeline Snippet

Here’s the full context showing how both the **K8S\_Deployment - PROD** and **Integration Tests - PROD** stages integrate into your Jenkinsfile:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('K8S_Deployment - PROD') {
      steps {
        parallel(
          "Apply Deployment": {
            withKubeConfig([credentialsId: 'kubeconfig']) {
              sh """
                sed -i 's#\\\${imageName}#${imageName}#g' k8s_PROD-deployment_service.yaml
                kubectl -n prod apply -f k8s_PROD-deployment_service.yaml
              """
            }
          },
          "Rollout Status": {
            withKubeConfig([credentialsId: 'kubeconfig']) {
              sh "bash k8s-PROD-deployment-rollout-status.sh"
            }
          }
        )
      }
    }

    stage('Integration Tests - PROD') {
      steps {
        script {
          try {
            withKubeConfig([credentialsId: 'kubeconfig']) {
              sh "bash integration-test-PROD.sh"
            }
          } catch (e) {
            withKubeConfig([credentialsId: 'kubeconfig']) {
              sh "kubectl -n prod rollout undo deploy ${deploymentName}"
            }
            error("Rolled back due to integration test failure.")
          }
        }
      }
    }
  }

  post {
    always {
      junit 'target/surefire-reports/*.xml'
      jacoco execPattern: 'target/jacoco.exec'
      pitmutation mutationStatsFile: '**/target/pit-reports/**/*mutations.xml'
      dependencyCheckPublisher pattern: 'target/dependency-check-report.xml'
      publishHTML(
        allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: 'owasp-zap-report',
        reportFiles: ''
      )
    }
  }
}
```

## Demo Run

Once pushed, the pipeline runs the integration script:

```bash theme={null}
$ bash integration-test-PROD.sh
32564
http://devsecops-demo.eastus.cloudapp.azure.com:32564/increment/99
Increment Test Passed
HTTP Status Code Test Passed
```

With this setup, you have a streamlined integration test step for your production deployments. To expand your testing strategy, integrate [JMeter](https://jmeter.apache.org/) for performance or other specialized tools.

## Links & References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Istio Gateway Concepts](https://istio.io/latest/docs/concepts/traffic-management/#gateways)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/28109bc8-356d-467a-bc46-3b072d3cfca3" />
</CardGroup>


# Demo Istio Ingress Gateway and Virtual Service

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Demo-Istio-Ingress-Gateway-and-Virtual-Service/page

Learn to use Istio’s Ingress Gateway and VirtualService to expose and control traffic for a Kubernetes-based DevSecOps application.

In this guide, you’ll learn how to use Istio’s **Ingress Gateway** and **VirtualService** to expose and control traffic for a Kubernetes-based DevSecOps application. We’ll define the necessary custom resources, apply them, and verify external access. Finally, you’ll see how Kiali can help you visualize and troubleshoot your service mesh configuration.

## Istio Ingress Gateway

An **Ingress Gateway** acts as an edge load balancer for your service mesh, handling incoming HTTP/TCP traffic. It exposes ports and protocols, but unlike Kubernetes Ingress, it does **not** include routing rules—that’s delegated to a VirtualService.

<Callout icon="lightbulb">
  A Gateway only configures the listener. Use a VirtualService to define how traffic is routed.
</Callout>

Here’s a minimal Gateway CRD:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: httpbin-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "httpbin.example.com"
```

Apply the Gateway:

```bash theme={null}
kubectl apply -f gateway.yaml
```

## Istio VirtualService

A **VirtualService** lets you define routing rules that map incoming requests (from a Gateway or internal service) to destinations in the mesh.

<Frame>
  ![The image shows a webpage from the Istio documentation, specifically discussing "Virtual services" and their role in traffic management. It includes sections on why virtual services are used, with a navigation sidebar on the right.](https://kodekloud.com/kk-media/image/upload/v1752873745/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Istio-Ingress-Gateway-and-Virtual-Service/istio-virtual-services-traffic-management.jpg)
</Frame>

Example: route all HTTP traffic for `httpbin.example.com` to the `httpbin` service on port 8000.

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: httpbin
spec:
  hosts:
  - "httpbin.example.com"
  http:
  - route:
    - destination:
        host: httpbin
        port:
          number: 8000
```

Apply it:

```bash theme={null}
kubectl apply -f virtualservice.yaml
```

## Exposing the DevSecOps Application

Our application `devsecops-svc` is currently a ClusterIP service on port 8080 in the `prod` namespace:

```bash theme={null}
kubectl -n prod get svc
