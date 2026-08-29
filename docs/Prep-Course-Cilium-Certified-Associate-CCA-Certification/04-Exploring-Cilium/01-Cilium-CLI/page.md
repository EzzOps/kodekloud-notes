# Cilium CLI

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Exploring-Cilium/Cilium-CLI/page

Explains cilium-cli commands to view and modify Cilium configuration, enable and disable debug logging, and verify pod restarts and logs for troubleshooting on Kubernetes.

In this lesson we cover two essential cilium-cli commands for administering Cilium on a Kubernetes cluster: how to view the active Cilium configuration and how to enable debug-level logging for troubleshooting. These commands read from and modify the `cilium-config` ConfigMap and (when needed) trigger a restart of Cilium agents so changes take effect.

<Frame>
  <img alt="A simple presentation slide with the title &#x22;Cilium CLI&#x22; centered on a blue-to-teal gradient background. In the bottom-left corner is a small &#x22;© Copyright KodeKloud&#x22; notice." />
</Frame>

Why these commands are useful:

* Inspect current runtime and configuration values.
* Temporarily increase logging detail to diagnose networking, policy, or datapath issues.
* Apply and revert settings without editing ConfigMaps manually.

## Quick command reference

|                                             Command | Purpose                                                                       | Example                                             |
| --------------------------------------------------: | ----------------------------------------------------------------------------- | --------------------------------------------------- |
|                                `cilium config view` | Display the active Cilium configuration (from the `cilium-config` ConfigMap). | `cilium config view`                                |
|                      `cilium config set debug true` | Enable debug logging (patches the ConfigMap and restarts Cilium pods).        | `cilium config set debug true`                      |
|                     `cilium config set debug false` | Disable debug logging (revert to default logging level).                      | `cilium config set debug false`                     |
| `kubectl -n kube-system get pods -l k8s-app=cilium` | Verify Cilium pods and check for restarts after config changes.               | `kubectl -n kube-system get pods -l k8s-app=cilium` |
|     `kubectl -n kube-system logs <cilium-pod-name>` | Inspect Cilium pod logs (useful when debug is enabled).                       | `kubectl -n kube-system logs cilium-abcde`          |

## View the current Cilium configuration

Use this to quickly inspect values stored in the `cilium-config` ConfigMap and confirm how Cilium is configured in the cluster:

```bash theme={null}
cilium config view
```

If you prefer to inspect the raw ConfigMap with kubectl:

```bash theme={null}
kubectl -n kube-system get configmap cilium-config -o yaml
```

This is helpful when you want to see timestamps, annotations, or any fields not surfaced by the `cilium` CLI output.

## Enable debug logging (toggle)

Enabling debug logging increases log verbosity from Cilium agents, which is useful when isolating issues in datapath, agent communication, or policy enforcement. The cilium CLI patches the `cilium-config` ConfigMap and restarts Cilium pods so agents pick up the change.

Enable debug logging:

```bash theme={null}
cilium config set debug true
```

Typical CLI output after enabling debug:

```text theme={null}
Patching ConfigMap cilium-config with debug=true...
Restarted Cilium pods
```

To revert debug logging back to normal (disable verbose logs):

```bash theme={null}
cilium config set debug false
```

## Verify pods and inspect logs

After toggling debug, confirm the pods restarted and examine logs:

```bash theme={null}
