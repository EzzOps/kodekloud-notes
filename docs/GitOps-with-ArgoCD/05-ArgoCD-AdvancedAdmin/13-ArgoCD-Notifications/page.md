# ArgoCD Notifications

Source: https://notes.kodekloud.com/docs/GitOps-with-ArgoCD/ArgoCD-AdvancedAdmin/ArgoCD-Notifications/page

This article explores configuring ArgoCD Notifications for Slack to receive alerts about changes in application state.

In this article, we explore ArgoCD Notifications—a powerful controller that enables you to receive alerts about changes in your ArgoCD application state. With support for multiple notification services including email, Telegram, webhooks, GitHub, and Slack, this guide specifically focuses on configuring notifications for Slack.

> **lightbulb** Ensure your Slack application is properly configured before proceeding with the integration.

## Configuring Slack Notifications

The Slack notification service requires an application token with the correct permissions to post messages. To obtain this token:

1. Create a new Slack application in your workspace.
2. Navigate to the OAuth section of your Slack app.
3. Add the necessary OAuth scopes, e.g., `chat:write` and `chat:write:customize`.
4. Install the app into your workspace and select the Slack channel where notifications should be sent.
5. Store the received OAuth token in the ArgoCD Notifications secret.

Next, update the Slack integration settings within the ArgoCD Notifications ConfigMap. Reference the token from the secret, and optionally override the default username and icon. Finally, patch your ArgoCD application or project with an annotation that enables notifications. In this example, we use the annotation `notifications.argoproj.io/subscribe.on-sync-succeeded.slack` along with the designated Slack channel name.

**Important:** Simply configuring these steps is not sufficient. ArgoCD sends notifications only after a trigger is defined and a corresponding message template is created.

## Understanding Triggers and Templates

A trigger defines the condition under which a notification is sent. Each trigger contains:

* A name
* A condition (e.g., `app.status.sync.status == 'Synced'`)
* A reference to a notification template

In this example, the trigger initiates a notification when the application sync status equals `Synced`, directly using the application object value. The trigger then calls the notification template `app-sync-succeeded-slack`, which formats the notification message.

A notification template is responsible for generating the message that is sent to Slack. These templates are defined in the ArgoCD Notifications ConfigMap, and you can reference the same template across multiple triggers to maintain consistency.

If additional details such as repository URL, author details, or commit messages should be included in the notification, consider leveraging Slack attachments by modifying the existing template.

## Example Configurations

Below are the configuration examples for setting up ArgoCD Notifications:

### Update the ConfigMap

```yaml theme={null}
$ kubectl edit configmap argocd-notifications-cm
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
data:
  service.slack: |
    token: $slack-token
    username: argocd-bot
    icon: ":rocket:"
  
  trigger.app-sync-succeeded: |
    when: app.status.sync.status == 'Synced'
    send: [app-sync-succeeded-slack]
  
  template.app-sync-succeeded-slack: |
    message: |
      Application {{.app.metadata.name}} sync is {{.app.status.sync.status}}.
```

### Configure the Secret

```yaml theme={null}
$ kubectl edit secret argocd-notifications-secret
apiVersion: v1
kind: Secret
metadata:
  name: argocd-notifications-secret
stringData:
  slack-token: xoxb-33238328357138-3839459687381...
