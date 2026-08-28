# Add Falco GPG key and repository
curl -s https://falco.org/repo/falcosecurity-36728A8F.asc | apt-key add -
echo "deb https://download.falco.org/packages/deb stable main" \
  | tee /etc/apt/sources.list.d/falcosecurity.list

# Update and install dependencies
apt-get update -y
apt-get install -y linux-headers-$(uname -r)

# Install Falco
apt-get install -y falco
```

<Callout icon="lightbulb">
  Installing kernel headers is required for the Falco DKMS module to build against your running kernel.
</Callout>

After installation, you should see output similar to:

```text theme={null}
Unpacking falco (0.29.0) ...
Setting up falco (0.29.0) ...
Loading new falco-… DKMS files...
Building initial module for <your-kernel-version>
Installing to /lib/modules/<your-kernel-version>/updates/dkms/
depmod...
DKMS: install completed.
```

## 2. Verify the Installation

1. **Check Falco service status**
   ```bash theme={null}
   systemctl status falco
   ```
   Falco may run as a daemon or via a container, depending on your setup.

2. **Inspect the configuration directory**
   ```bash theme={null}
   ls -l /etc/falco
   ```
   You should see:
   | File/Directory          | Description                           |
   | ----------------------- | ------------------------------------- |
   | falco\_rules.yaml       | Default rule definitions              |
   | falco\_rules.local.yaml | Local overrides for custom rules      |
   | k8s\_audit\_rules.yaml  | Kubernetes audit-event rules          |
   | rules.available/        | Available community-contributed rules |
   | rules.d/                | Custom rule fragments                 |

3. **Stream Falco logs**
   ```bash theme={null}
   journalctl -u falco -f
   ```

## 3. Generate a Kubernetes Alert

Open two terminal windows:

* **Terminal A**: Stream Falco logs
  ```bash theme={null}
  journalctl -u falco -f
  ```

* **Terminal B**: Trigger an alert
  ```bash theme={null}
  # Create an nginx pod named 'n1'
  kubectl run n1 --image=nginx

  # Confirm the pod is running
  kubectl get pod n1

  # Exec into the container to spawn a shell
  kubectl exec -it n1 -- bash

  # Inside the container, exit to complete the session
  root@n1:/# exit
  ```

As soon as the shell spawns inside the container, Falco will emit a notice:

```text theme={null}
20:15:32.123456 Notice A shell was spawned in a container with an attached terminal (command="bash" user=root container=n1 pod=n1 namespace=default image="nginx:latest")
```

This alert output references dynamic fields such as `%proc.cmdline`, `%user.name`, `%container.name`, `%k8s.pod.name`, `%k8s.ns.name`, and `%container.image`.

## 4. Inspect the Alert Rule

Falco’s built-in rules are defined in `falco_rules.yaml`. To view the rule that detects terminal shells in containers:

```bash theme={null}
grep -A15 -i "A shell was spawned in a container with an attached terminal" /etc/falco/falco_rules.yaml
```

Example snippet:

```yaml theme={null}
- rule: Terminal shell in container
  desc: Detect when a shell is spawned in a container with an attached terminal
  condition: spawned_process and container.id != host
    and proc.name in (bash, sh, csh, ksh, tcsh, zsh, dash)
    and fd.is_tty=true
  output: >
    A shell was spawned in a container with an attached terminal
    (command=%proc.cmdline user=%user.name container=%container.name
     pod=%k8s.pod.name namespace=%k8s.ns.name image=%container.image)
  priority: NOTICE
  tags: [container, shell]
```

Macros like `in_container` and lists such as `shell_binaries` are defined elsewhere in the configuration. For full details on writing and customizing rules, see the [Falco documentation](https://falco.org/docs/).

## 5. Next Steps

We recommend integrating Falco with a centralized dashboard or SIEM to manage alerts at scale. In the next tutorial, we’ll cover:

* Deploying Falco Manager and Falco Plugins.
* Sending alerts to a web UI (e.g., Grafana, Kibana).
* Custom rule authoring for advanced threat detection.

***

## Links and References

* [Falco Official Website](https://falco.org/)
* [Falco Quickstart Guide](https://falco.org/docs/quickstart/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [DKMS Kernel Module Guide](https://wiki.ubuntu.com/Kernel/ModuleBuild)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/3564410e-9c54-47f0-8c1b-d2bcf3ca454b" />
</CardGroup>


# Demo Falco Slack Notifications

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Demo-Falco-Slack-Notifications/page

Learn to send Falco security alerts to a Slack channel using Falco Sidekick and Slack Incoming Webhooks.

Learn how to send real-time Falco security alerts into a Slack channel using **Falco Sidekick** and Slack Incoming Webhooks. This guide walks you through creating a Slack channel, configuring a webhook, installing Sidekick via Helm, and testing alerts.

## Prerequisites

* A running Kubernetes cluster with Falco installed via Helm
* A Slack workspace with permission to create channels and apps
* `helm` and `kubectl` CLI tools configured for your cluster

## 1. Create a Slack Channel

Create a dedicated channel (for example, `#falco`) to receive Falco alerts.

<Frame>
  ![The image shows a Slack interface with a "Create a channel" dialog open, where a user is entering details for a new channel named "#falco" with a description for Falco notifications. The background displays a conversation in the "#jenkins" channel.](https://kodekloud.com/kk-media/image/upload/v1752873736/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Falco-Slack-Notifications/slack-create-channel-falco-notifications.jpg)
</Frame>

## 2. Configure an Incoming Webhook

Follow these steps to set up an incoming webhook in Slack.

1. Open the [Slack Incoming Webhooks documentation](https://api.slack.com/messaging/webhooks).

<Frame>
  ![The image shows a webpage from the Slack API documentation, specifically about getting started with incoming webhooks. It includes instructions on creating a Slack app and enabling incoming webhooks.](https://kodekloud.com/kk-media/image/upload/v1752873737/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Falco-Slack-Notifications/slack-api-incoming-webhooks-guide.jpg)
</Frame>

2. Click **Create an app**, choose **From scratch**, and pick your workspace.

<Frame>
  ![The image shows a Slack API webpage with a pop-up window titled "Create an app," offering options to configure an app's scopes and settings either from scratch or using an app manifest. The browser has multiple tabs open, and a user profile picture is visible in the top right corner.](https://kodekloud.com/kk-media/image/upload/v1752873738/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Falco-Slack-Notifications/slack-api-create-app-popup.jpg)
</Frame>

3. Under **Features**, enable **Incoming Webhooks**.

<Frame>
  ![The image shows a Slack API settings page with options for configuring features like Incoming Webhooks, Slash Commands, and Bots. The interface includes navigation links and a section for managing app credentials.](https://kodekloud.com/kk-media/image/upload/v1752873739/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Falco-Slack-Notifications/slack-api-settings-incoming-webhooks-bots.jpg)
</Frame>

4. Click **Add New Webhook to Workspace**, select `#falco`, and authorize. Copy the generated URL:

   ```text theme={null}
   https://hooks.slack.[SECRET_REDACTED]
   ```

<Callout icon="triangle-alert">
  Treat your webhook URL like a password. Do not expose it in public repositories.
</Callout>

5. Verify the webhook with `curl`:

   ```bash theme={null}
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"Hello, Falco!"}' \
     https://hooks.slack.[SECRET_REDACTED]
   ```

You should see **“Hello, Falco!”** in the `#falco` channel.

## 3. Install Falco Sidekick with Slack Integration

Use Helm to enable Falco Sidekick and configure Slack:

```bash theme={null}
helm upgrade falco falcosecurity/falco \
  --set falcosidekick.enabled=true \
  --set falcosidekick.webui.enabled=true \
  --set falcosidekick.config.slack.webhookurl="https://hooks.slack.[SECRET_REDACTED]" \
  --set falcosidekick.config.customfields="environment:production,datacenter:paris" \
  -n falco
```

| Configuration Key                     | Description                     | Example                                     |
| ------------------------------------- | ------------------------------- | ------------------------------------------- |
| falcosidekick.enabled                 | Enable Falco Sidekick component | `true`                                      |
| falcosidekick.webui.enabled           | Sidekick Web UI                 | `true`                                      |
| falcosidekick.config.slack.webhookurl | Slack incoming webhook URL      | `"https://hooks.slack.com/services/…"`      |
| falcosidekick.config.customfields     | Custom metadata fields          | `"environment:production,datacenter:paris"` |

After upgrading, confirm the release and running pods:

```bash theme={null}
helm ls -n falco
kubectl get all -n falco
```

## 4. Trigger a Test Alert

Spawn a shell in a container to generate a Falco alert. Replace `n1` with your Pod name:

```bash theme={null}
kubectl exec -it n1 -- sh -c "touch /tmp/test && ls /tmp/test"
```

Falco detects the shell spawn and Sidekick forwards the alert to Slack.

<Frame>
  ![The image shows a Slack interface with a notification from the Falco Slack Application, indicating that a shell was spawned in a container with specific details about the container and process.](https://kodekloud.com/kk-media/image/upload/v1752873740/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Falco-Slack-Notifications/slack-notification-falco-container-shell.jpg)
</Frame>

The message includes rule name, priority, container details, pod/namespace, custom fields, timestamp, and process info.

## Conclusion

You've successfully integrated Falco with Slack for real-time monitoring. To extend this setup—sending alerts to Microsoft Teams, Discord, Elasticsearch, Datadog, and more—update the `falcosidekick.config` in your Helm command.

## Links and References

* [Falco Sidekick Repository](https://github.com/falcosecurity/falcosidekick)
* [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
* [Falco Documentation](https://falco.org/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/2e80d9a5-7416-4cc8-a9a0-c5db7e0fd736" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/7ac16b77-b5ad-4c8a-94b2-55e4fa77a4b0" />
</CardGroup>
