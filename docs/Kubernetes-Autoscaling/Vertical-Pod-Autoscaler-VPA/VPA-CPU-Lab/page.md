# VPA CPU Lab

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Vertical-Pod-Autoscaler-VPA/VPA-CPU-Lab/page

Hands-on lab demonstrating CPU-focused Vertical Pod Autoscaler using a Flask app to monitor usage, generate VPA recommendations (updateMode Off), and validate recommendations under load

Welcome — this lab covers a CPU-focused Vertical Pod Autoscaler (VPA) workflow. The high-level flow mirrors the memory-focused lab but targets CPU:

* Deploy a sample application.
* Monitor CPU utilization.
* Apply a VPA that produces recommendations (no automatic updates).
* Run a CPU load test and validate VPA recommendations.

<Frame>
  <img alt="A slide titled &#x22;Lab Overview&#x22; listing three numbered steps: &#x22;Deploy sample application,&#x22; &#x22;Monitor application resource usage,&#x22; and &#x22;Apply VPA configuration and capture recommendations.&#x22; A stylized pink computer icon with a DNA-like symbol is shown on the left." />
</Frame>

What you'll deploy

* A simple Flask application will act as the CPU workload for this lab.
* Initially the app is idle and uses very little CPU (typically \~1m).
* A VPA will be created to produce CPU recommendations only (no automatic updates). The VPA will enforce a minimum of `100m` and a maximum of `1000m` CPU for the container and will be configured to control CPU only.

VPA manifest (vpa-cpu.yml)

```yaml theme={null}
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: flask-app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app-4
  updatePolicy:
    updateMode: "Off"  # Set to "Auto" for automatic updates
  resourcePolicy:
    containerPolicies:
      - containerName: '*'
        minAllowed:
          cpu: 100m
        maxAllowed:
          cpu: 1000m
        controlledResources: ["cpu"]
```

Quick explanation of the important fields

| Field                              | Purpose                                                  | Example / notes                                                                                |
| ---------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `targetRef`                        | Which Deployment the VPA should observe                  | `name: flask-app-4`                                                                            |
| `updatePolicy.updateMode`          | Whether the VPA should automatically change pod requests | `updateMode: "Off"` (recommendations only). Change to `"Auto"` to apply updates automatically. |
| `resourcePolicy.containerPolicies` | Per-container limits and controlled resources            | `minAllowed: cpu: 100m`, `maxAllowed: cpu: 1000m`, `controlledResources: ["cpu"]`              |

Apply the VPA

```bash theme={null}
kubectl apply -f vpa-cpu.yml
