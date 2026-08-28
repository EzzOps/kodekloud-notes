# DEMO Alerts amp Providers

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Notification-Controller/DEMO-Alerts-amp-Providers/page

This tutorial configures the Flux Notification Controller to send GitOps alerts to a Slack channel.

In this tutorial, you'll configure the Flux Notification Controller to automatically send GitOps alerts to a Slack channel. By the end, you will have a working Slack App, Flux provider, and alert definitions driving real-time notifications.

***

## 1. Prepare Your Slack Workspace and Channel

If you don’t have a Slack workspace yet, create one by following [Slack’s Help Center instructions](https://slack.com/help/articles/218080037-Create-a-Slack-workspace):

<Frame>
  ![The image shows a Slack Help Center webpage with instructions on creating a workspace for a team, including steps for desktop, iOS, and Android.](https://kodekloud.com/kk-media/image/upload/v1752877673/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-help-center-create-workspace.jpg)
</Frame>

Once your workspace is ready, create a new channel (public or private) for Flux alerts. In this demo, we’ll use `flux-alerts-channel`:

<Frame>
  ![The image shows a Slack workspace with a private channel named "flux-alerts-channel" that has just been created. The interface displays the channel's name, a welcome message, and a user who joined the channel.](https://kodekloud.com/kk-media/image/upload/v1752877674/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-workspace-flux-alerts-channel.jpg)
</Frame>

If you need to customize the channel settings, use the channel-creation pop-up:

<Frame>
  ![The image shows a Slack interface with a pop-up window for creating a new channel, where you can enter a name, description, and set the channel to private.](https://kodekloud.com/kk-media/image/upload/v1752877675/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-new-channel-popup-interface.jpg)
</Frame>

***

## 2. Create and Configure a Slack App

### 2.1 Create the Slack App

1. Go to the [Slack API dashboard](https://api.slack.com/apps).
2. Click **Create an App**, give it a name (e.g., **Flux Alerts Application**), and select your workspace.

<Frame>
  ![The image shows a Slack API interface where a user is naming an app "Flux Alert" and choosing a workspace to develop it in. There are options to cancel or create the app.](https://kodekloud.com/kk-media/image/upload/v1752877677/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-api-flux-alert-app-creation.jpg)
</Frame>

### 2.2 Configure OAuth & Permissions

Under **Features → OAuth & Permissions**, add the following **Bot Token Scopes**:

| Scope                | Description                        |
| -------------------- | ---------------------------------- |
| chat:write           | Send messages as the app           |
| channels:read        | Read public channel information    |
| chat:write.customize | Send messages with a custom avatar |

<Frame>
  ![The image shows the Slack API interface, specifically the "OAuth & Permissions" section, where options for advanced token security and OAuth tokens for a workspace are displayed.](https://kodekloud.com/kk-media/image/upload/v1752877678/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-api-oauth-permissions-interface.jpg)
</Frame>

After adding the scopes, install the app:

<Frame>
  ![The image shows a Slack API settings page with a list of bot token scopes, including permissions like "chat:write" and "channels:read." There's a success message at the top indicating changes have been saved.](https://kodekloud.com/kk-media/image/upload/v1752877679/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-api-settings-bot-token-scopes.jpg)
</Frame>

On the authorization screen, click **Allow**:

<Frame>
  ![The image shows a Slack authorization page where the Flux Alerts Application is requesting permission to access the "mcd-level2" Slack workspace. It includes options to view content and perform actions in channels and conversations, with "Cancel" and "Allow" buttons.](https://kodekloud.com/kk-media/image/upload/v1752877680/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-authorization-flux-alerts-mcd-level2.jpg)
</Frame>

Once installed, copy the **Bot User OAuth Token** from the **OAuth & Permissions** page.

<Frame>
  ![The image shows a Slack API settings page focused on OAuth & Permissions, displaying options for token security and an OAuth token for a workspace.](https://kodekloud.com/kk-media/image/upload/v1752877681/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-api-oauth-permissions-settings.jpg)
</Frame>

<Callout icon="triangle-alert">
  Keep your Bot User OAuth Token secure. Treat it like any sensitive credential.
</Callout>

### 2.3 Invite the Bot to Your Alert Channel

If your alerts channel is private, you must add the app as a member:

<Frame>
  ![The image shows a Slack workspace interface with a private channel named "flux-alerts-channel" open. A dropdown menu is visible, offering options to notify everyone in the channel.](https://kodekloud.com/kk-media/image/upload/v1752877682/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-workspace-flux-alerts-channel-2.jpg)
</Frame>

Once invited, you’ll see a confirmation in the channel:

<Frame>
  ![The image shows a Slack workspace with a private channel named "flux-alerts-channel." It includes messages about a user joining the channel and an application being added.](https://kodekloud.com/kk-media/image/upload/v1752877683/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-workspace-flux-alerts-channel-3.jpg)
</Frame>

***

## 3. Configure Flux Notification Controller

### 3.1 Create the Slack Bot Token Secret

Store your Slack Bot Token in the `flux-system` namespace:

```bash theme={null}
kubectl -n flux-system create secret generic slack-bot-token \
  --from-literal=token=xoxb-xxxxxxxxxxxxxxxxxxxx
```

<Callout icon="lightbulb">
  Replace `xoxb-xxxxxxxxxxxxxxxxxxxx` with your actual Bot User OAuth Token.
</Callout>

### 3.2 Define the Slack Provider

Flux’s Provider API lets you specify how notifications are sent. See [Flux Notification Providers](https://kodekloud.com/kk-media/image/upload/v1752877685/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/flux-documentation-notification-providers.jpg):

<Frame>
  ![The image shows a webpage from the Flux documentation listing various notification providers such as Discord, GitHub, Google Chat, and Slack. The left sidebar contains navigation links for different components and guides.](https://kodekloud.com/kk-media/image/upload/v1752877685/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/flux-documentation-notification-providers.jpg)
</Frame>

**Option A: Apply a YAML manifest**\
Create `notification-provider-slack.yaml`:

```yaml theme={null}
apiVersion: notification.toolkit.fluxcd.io/v1beta2
kind: Provider
metadata:
  name: notification-provider-slack
  namespace: flux-system
spec:
  type: slack
  channel: flux-alerts-channel
  address: https://slack.com/api/chat.postMessage
  secretRef:
    name: slack-bot-token
  username: flux-bot
```

Apply it:

```bash theme={null}
kubectl -n flux-system apply -f notification-provider-slack.yaml
```

**Option B: Generate with the Flux CLI**

```bash theme={null}
flux create provider notification slack notification-provider-slack \
  --channel flux-alerts-channel \
  --username flux-bot \
  --secret-ref slack-bot-token \
  --address https://slack.com/api/chat.postMessage \
  --export > notification-provider-slack.yaml
```

***

### 3.3 Define an Alert

Alerts let you filter events by severity and resource type before sending them via your provider.

Create `notification-alert-slack.yaml`:

```yaml theme={null}
apiVersion: notification.toolkit.fluxcd.io/v1beta2
kind: Alert
metadata:
  name: notification-alert-slack
  namespace: flux-system
spec:
  eventSeverity: info
  eventSources:
    - kind: Kustomization; name: "*"
    - kind: GitRepository; name: "*"
    - kind: Bucket; name: "*"
    - kind: OCIRepository; name: "*"
    - kind: HelmChart; name: "*"
    - kind: HelmRepository; name: "*"
    - kind: HelmRelease; name: "*"
    - kind: ImageRepository; name: "*"
    - kind: ImagePolicy; name: "*"
    - kind: ImageUpdateAutomation; name: "*"
  providerRef:
    name: notification-provider-slack
```

Or generate with the Flux CLI:

```bash theme={null}
flux create alert notification-alert-slack \
  --event-severity info \
  --provider-ref notification-provider-slack \
  --event-source Kustomization/* \
  --event-source GitRepository/* \
  --event-source Bucket/* \
  --event-source OCIRepository/* \
  --event-source HelmChart/* \
  --event-source HelmRepository/* \
  --event-source HelmRelease/* \
  --event-source ImageRepository/* \
  --event-source ImagePolicy/* \
  --event-source ImageUpdateAutomation/* \
  --export > notification-alert-slack.yaml
```

Apply your Alert:

```bash theme={null}
kubectl -n flux-system apply -f notification-alert-slack.yaml
```

***

## 4. Confirm Setup

Make sure Flux picks up your changes and that both the provider and alert are `READY`:

```bash theme={null}
flux reconcile source git flux-system
flux get alert
flux get providers notification
```

***

## 5. Trigger and Observe Notifications

Change something in your Git repository—for example, reduce the replica count in your deployment:

```yaml theme={null}
