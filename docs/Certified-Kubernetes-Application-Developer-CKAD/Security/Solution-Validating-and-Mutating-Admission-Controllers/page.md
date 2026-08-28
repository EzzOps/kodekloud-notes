# Solution Validating and Mutating Admission Controllers

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Security/Solution-Validating-and-Mutating-Admission-Controllers/page

This article provides a hands-on guide for validating and mutating admission controllers in Kubernetes, covering namespace creation, TLS secret management, and webhook server deployment.

In this lesson, we walk through the lab on validating and mutating admission controllers. You'll gain hands-on experience with namespace creation, TLS secret management, deploying webhook servers, and testing pod security contexts.

<Frame>
  ![KodeKloud practice test interface showing a terminal and a multiple-choice question about mutating and validating admission controllers.](https://kodekloud.com/kk-media/image/upload/v1752871293/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Solution-Validating-and-Mutating-Admission-Controllers/frame_0.jpg)
</Frame>

The lab begins with a multiple-choice question asking which combination is correct for mutating and validating admission controllers. The key observation is that the namespace auto-provision admission controller performs a mutation by automatically creating or altering a namespace. On the other hand, the namespace existence check is strictly a validation step. Therefore, the correct combination is to treat namespace auto-provisioning as mutating and namespace existence checking as validating.

<Frame>
  ![KodeKloud practice test interface showing a terminal and a question regarding the flow of invocation of admission controllers.](https://kodekloud.com/kk-media/image/upload/v1752871294/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Solution-Validating-and-Mutating-Admission-Controllers/frame_50.jpg)
</Frame>

## Step 1: Create the Namespace

First, create a namespace named "webhook-demo" to serve as the environment for the webhook operations.

```bash theme={null}
kubectl create ns webhook-demo
```

After executing the command, verify that the namespace is created by listing all namespaces:

```bash theme={null}
kubectl get ns
```

You should see the "webhook-demo" namespace included in the output.

## Step 2: Create a TLS Secret

For secure webhook communication, create a TLS secret named "webhook-server-tls" in the "webhook-demo" namespace. Ensure you substitute the correct file paths for the certificate and key:

```bash theme={null}
kubectl -n webhook-demo create secret tls webhook-server-tls \
  --cert "/root/keys/webhook-server-tls.crt" \
  --key "/root/keys/webhook-server-tls.key"
```

A successful creation message will confirm that the TLS secret has been established.

## Step 3: Deploy the Webhook Server

Review the webhook server deployment definition provided in the file `webhook-deployment.yaml`:

```bash theme={null}
cat webhook-deployment.yaml
```

Deploy the webhook server with the following command:

```bash theme={null}
kubectl apply -f webhook-deployment.yaml
```

## Step 4: Create the Webhook Service

Create a service for the webhook server using the configuration in `webhook-service.yaml`:

```bash theme={null}
kubectl apply -f webhook-service.yaml
```

## Step 5: Apply the Mutating Webhook Configuration

Next, apply the mutating webhook configuration defined in `webhook-configuration.yaml`. This file includes rules under the "rules" section to intercept "CREATE" operations for pods.

```bash theme={null}
kubectl apply -f webhook-configuration.yaml
```

<Callout icon="triangle-alert">
  When applying the webhook configuration, you might receive a deprecation warning indicating that admissionregistration.k8s.io/v1beta1 is deprecated in favor of v1. Despite the warning, the configuration will still perform its intended function by denying pod creation requests that attempt to run as root when no security context is provided.
</Callout>

In our lab, if no explicit value is given for "runAsNonRoot", a default value of `true` is applied, and the user ID is defaulted to `1234` unless overridden.

## Step 6: Test the Webhook by Deploying Pods

### Pod with Default Security Context

The next stage involves deploying a pod that does not specify any security context so that the webhook can mutate the configuration. The YAML file `pod-with-defaults.yaml` contains the following configuration:

```yaml theme={null}
