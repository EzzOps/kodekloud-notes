# Using Kustomize with a pipe:
$ kustomize build k8s/ | kubectl apply -f -
service/nginx-loadbalancer-service created
deployment.apps/nginx-deployment created

# Using kubectl directly with the -k flag:
$ kubectl apply -k k8s/
service/nginx-loadbalancer-service created
deployment.apps/nginx-deployment created
```

## Removing Configurations

Deleting the deployed resources follows a process similar to deployment. Simply replace the `apply` keyword with `delete`. The first method pipes the output of the Kustomize build command directly into `kubectl delete`:

```bash theme={null}
$ kustomize build k8s/ | kubectl delete -f -
service "nginx-loadbalancer-service" deleted
deployment.apps "nginx-deployment" deleted
```

Alternatively, use the native method with the `-k` flag:

```bash theme={null}
$ kubectl delete -k k8s/
service "nginx-loadbalancer-service" deleted
deployment.apps "nginx-deployment" deleted
```

<Callout icon="lightbulb">
  Always verify that the correct configurations are being applied or deleted by reviewing the Kustomize output before proceeding. This helps in avoiding accidental misconfigurations.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/b2ed246e-9cf4-484f-b1e0-8fad82d87034" />
</CardGroup>


# Kustomize vs Helm

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/Kustomize-vs-Helm/page

This article offers a comparison between Helm and Kustomize for modifying Kubernetes manifests across different environments.

This article offers a high-level comparison between Helm and Kustomize for modifying Kubernetes manifests across different environments. Understanding both tools is crucial when selecting the best fit for your project.

## Helm's Templating Approach

Helm uses Go templating syntax to inject variable values into Kubernetes manifests. Rather than hard coding values, Helm defines placeholders that can be dynamically replaced with environment-specific configurations. Consider the following example:

```yaml theme={null}
