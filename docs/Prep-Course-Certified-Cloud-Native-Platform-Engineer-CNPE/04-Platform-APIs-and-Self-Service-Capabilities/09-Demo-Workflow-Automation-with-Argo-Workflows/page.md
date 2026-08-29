# /root/selfsigned-issuer.yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned-issuer
  namespace: operator-lab
spec:
  selfSigned: {}
```

Apply the Issuer and inspect its status:

```bash theme={null}
kubectl apply -f /root/selfsigned-issuer.yaml
kubectl describe issuer selfsigned-issuer -n operator-lab
```

Example output from creating and describing the Issuer:

```bash theme={null}
issuer.cert-manager.io/selfsigned-issuer created
```

```text theme={null}
Name:             selfsigned-issuer
Namespace:        operator-lab
API Version:      cert-manager.io/v1
Kind:             Issuer
Spec:
  Self Signed:    true
Status:
  Conditions:
    Last Transition Time:  2026-04-11T10:12:02Z
    Observed Generation:   1
    Reason:                IsReady
    Status:                True
  Type:                    Ready
Events:                   <none>
```

Notice the `Status` block and the `Conditions` entry reporting `Ready: True`. This indicates the operator successfully reconciled the Issuer.

## Create a Certificate that uses the Issuer

Next, create a `Certificate` that references the self-signed Issuer. Save this as `/root/test-certificate.yaml`:

```yaml theme={null}
# /root/test-certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: test-cert
  namespace: operator-lab
spec:
  secretName: test-cert-tls
  duration: 2160h       # 90 days
  renewBefore: 360h     # 15 days before expiry
  subject:
    organizations:
      - Example Corp
  commonName: test.example.com
  dnsNames:
    - test.example.com
    - www.test.example.com
  issuerRef:
    name: selfsigned-issuer
    kind: Issuer
```

Apply and check status:

```bash theme={null}
kubectl apply -f /root/test-certificate.yaml
kubectl get certificate -n operator-lab
kubectl describe certificate test-cert -n operator-lab
```

Expected results after applying:

```bash theme={null}
certificate.cert-manager.io/test-cert created
```

```bash theme={null}
kubectl get certificate -n operator-lab
NAME        READY   SECRET          AGE
test-cert   True    test-cert-tls   18s
```

Describing the Certificate reveals status conditions, validity times, renewal time, and related events:

```bash theme={null}
kubectl describe certificate test-cert -n operator-lab
```

Example excerpt:

```text theme={null}
Status:
  Conditions:
    Last Transition Time:  2026-04-11T00:13:33Z
    Message:               Certificate is up to date and has not expired
    Observed Generation:   1
    Reason:                Ready
    Status:                True
  Not After:              2026-04-11T00:13:33Z
  Not Before:             2026-04-11T00:13:33Z
  Renewal Time:           2026-06-25T10:13:33Z
  Revision:               1

Events:
  Normal  Issuing     65s  cert-manager-certificates-trigger         Issuing certificate as Secret does not exist
  Normal  Generated   65s  cert-manager-certificates-key-manager     Stored new private key in temporary Secret resource "test-cert-ktrpn"
  Normal  Issuing     64s  cert-manager-certificates-request-manager Created new CertificateRequest resource "test-cert-1"
  Normal  Issuing     63s  cert-manager-certificates-issuing         The certificate has been successfully issued
```

The `Message` and `Reason` fields provide the operator’s human-readable summary of the resource state. When troubleshooting, these are your primary starting points.

## Inspect the Secret created by the operator

cert-manager stores the issued certificate and private key in a Kubernetes Secret named as specified by `secretName` in the Certificate resource.

Check the Secret:

```bash theme={null}
kubectl get secret -n operator-lab
kubectl describe secret test-cert-tls -n operator-lab
```

Example output showing a TLS Secret with three keys:

```text theme={null}
NAME            TYPE                DATA  AGE
test-cert-tls   kubernetes.io/tls   3     113s
```

```text theme={null}
Type:  kubernetes.io/tls

Data
====
ca.crt:  1188 bytes
tls.crt: 1188 bytes
tls.key: 1675 bytes
```

These artifacts were created by cert-manager as a result of reconciling the `Certificate` resource.

## Demonstrate the reconciliation loop

To see reconciliation in action, delete the Secret and watch the operator recreate it:

```bash theme={null}
kubectl delete secret test-cert-tls -n operator-lab
kubectl get secret -n operator-lab
kubectl describe secret test-cert-tls -n operator-lab
```

Example interaction:

```bash theme={null}
secret "test-cert-tls" deleted from operator-lab

# A short time later the controller recreates it:
kubectl get secret -n operator-lab
NAME            TYPE                DATA  AGE
test-cert-tls   kubernetes.io/tls   3     14s
```

Operators continuously watch their owned resources and reconcile until the observed state matches the desired state. Deleting side-effect resources (for example, Secrets or ConfigMaps created by an operator) does not permanently break the system — the operator will typically restore them.

<Callout icon="lightbulb">
  Always start troubleshooting custom resources by inspecting their `status.conditions`. Use `kubectl describe <kind> <name> -n <namespace>` (or `kubectl get <kind> <name> -n <namespace> -o yaml`) to see the operator-reported `Status`, `Reason`, human-readable `Message`, and related events.
</Callout>

## Key takeaways (exam & production)

1. Use `kubectl get` and `kubectl describe` on custom resources to read their status and conditions. The operator reports its view through the resource's `status`.
2. Operators continuously reconcile and will restore resources they manage. Deleting dependent resources (e.g., Secrets created by an operator) may result in them being recreated automatically.
3. If a resource is not in the desired state, `status.conditions` usually contains a `False` condition with a `Reason` and `Message` that help diagnose what went wrong. Always check events shown by `kubectl describe` as well.

## Links and references

* cert-manager documentation: [https://cert-manager.io/docs/](https://cert-manager.io/docs/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/33c8c726-73a9-4e4f-9b19-f426aa8cc191" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/208267db-ac21-46da-a59d-a686feee49f7" />
</CardGroup>


# Demo Workflow Automation with Argo Workflows

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-APIs-and-Self-Service-Capabilities/Demo-Workflow-Automation-with-Argo-Workflows/page

Guide demonstrating Argo Workflows usage in Kubernetes, including simple tasks, steps, DAGs, kubectl execution, parameters, templates, and RBAC considerations

Argo Workflows is a Kubernetes-native workflow orchestration engine for running complex, containerized job sequences (data pipelines, automation, kubectl, Python, Bash, etc.). It is often compared with other CNCF projects — here’s a quick comparison to clarify roles:

| Project        | Typical use case                       | Key focus                                                   |
| -------------- | -------------------------------------- | ----------------------------------------------------------- |
| Argo CD        | GitOps — sync cluster state to Git     | Continuous delivery / cluster reconciliation                |
| Tekton         | CI/CD pipelines                        | Build, test, and push artifacts                             |
| Argo Workflows | General-purpose workflow orchestration | Orchestrate multi-step tasks and dependencies in Kubernetes |

<Callout icon="lightbulb">
  This guide assumes Argo Workflows is already installed in your Kubernetes cluster. If you need installation instructions, refer to the official docs: [Argo Workflows installation](https://argoproj.github.io/argo-workflows/installation/).
</Callout>

In this article we build progressively more advanced workflows to demonstrate common Argo constructs:

* A simple container task
* Steps (sequential and parallel), with parameters
* DAG-based dependencies
* Running `kubectl` from inside a workflow (with RBAC considerations)

***

## 1) Simple “hello” workflow

Create `hello-workflow.yaml`. Notice `generateName` gives each submission a unique suffix:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: hello-world-
  namespace: argo
spec:
  entrypoint: hello
  templates:
  - name: hello
    container:
      image: alpine:3.18
      command: [echo]
      args: ["Hello from KodeKloud!"]
```

Submit and watch the run with the Argo CLI:

```bash theme={null}
argo submit hello-workflow.yaml -n argo --watch
```

Or inspect pods and logs with kubectl:

```bash theme={null}
kubectl get pods -n argo
kubectl logs <pod-name> -n argo
```

When the workflow completes you’ll see a generated name, `Succeeded` status, and the steps that ran.

<Frame>
  <img alt="The image shows a terminal displaying the status of a Kubernetes job named &#x22;hello-world-8pttw.&#x22; The job has successfully started, completed in 20 seconds, and is not currently running." />
</Frame>

Example `argo get` output (abridged):

```plaintext theme={null}
Name:               hello-world-8pttw
Namespace:          argo
ServiceAccount:     unset (will run with the default ServiceAccount)
Status:             Succeeded
Created:            Sat Apr 11 10:47:08 +0000 (20 seconds ago)
Finished:           Sat Apr 11 10:47:28 +0000 (now)
Duration:           20 seconds
Progress:           1/1

STEP                    TEMPLATE    PODNAME                    DURATION
✔ hello-world-8pttw     hello       hello-world-8pttw          10s
```

Example pod logs:

```bash theme={null}
kubectl logs hello-world-8pttw -n argo
time="2026-04-11T10:47:16.379Z" level=info msg="capturing logs" argo=true
Hello from KodeKloud!
time="2026-04-11T10:47:17.380Z" level=info msg="sub-process exited" argo=true error="<nil>"
```

***

## 2) Steps: sequential and parallel steps, with parameters

Use `steps` when you want ordered or grouped tasks. Steps are an array of arrays:

* Each inner array represents tasks that run in parallel.
* Outer array elements run sequentially.

Create `steps-workflow.yaml`. This example defines a reusable `print-message` template that accepts a `message` parameter, and a `pipeline` entrypoint that runs two sequential steps:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: steps-demo-
  namespace: argo
spec:
  entrypoint: pipeline
  templates:
  - name: pipeline
    steps:
    - - name: step-one
        template: print-message
        arguments:
          parameters:
          - name: message
            value: "Hello from KodeKloud!"
    - - name: step-two
        template: print-message
        arguments:
          parameters:
          - name: message
            value: "Hello from Nourhan!"
  - name: print-message
    inputs:
      parameters:
      - name: message
    container:
      image: alpine:3.18
      command: [echo]
      args: ["{{inputs.parameters.message}}"]
```

Submit:

```bash theme={null}
argo submit steps-workflow.yaml -n argo --watch
```

Notes:

* With the YAML above, `step-one` runs first, then `step-two`.
* To run `step-one` and `step-two` in parallel, place them in the same inner array (see the parallel example below).

Parallel example (only the `pipeline.steps` portion shown):

```yaml theme={null}
