# Create a Shared Library for Slack Notification

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Shared-Libraries-in-Jenkins/Create-a-Shared-Library-for-Slack-Notification/page

How to create a Jenkins Shared Library to centralize and reuse Slack notification logic across pipelines for consistent, maintainable notifications.

In this lesson you'll centralize Slack notification logic into a Jenkins Shared Library so it can be reused across multiple pipelines. Moving custom Groovy notification code out of individual Jenkinsfiles and into a shared library improves maintainability, reduces duplication, and makes it easier to apply consistent notification behavior across projects.

Why use a Shared Library?

* Reuse the same notification logic across many repositories and jobs.
* Keep Jenkinsfiles small and focused on pipeline structure.
* Update notification behavior in one place rather than across dozens of Jenkinsfiles.

Example: inline notification function you might have inside a Jenkinsfile

```groovy theme={null}
// Example inline function in a Jenkinsfile
def slackNotificationMethod(String buildStatus = 'STARTED') {
    def color

    if (buildStatus == 'SUCCESS') {
        color = '#47ec05'
    } else if (buildStatus == 'UNSTABLE') {
        color = '#d5ee0d'
    } else {
        color = '#ec2805'
    }

    def msg = "${buildStatus}: ${env.JOB_NAME} #${env.BUILD_NUMBER}:\n${env.BUILD_URL}"

    slackSend(color: color, message: msg)
}
```

That works for a single repository. To reuse the function across many pipelines, create a Shared Library repository and expose the logic as a global step under `vars/`.

<Frame>
  <img alt="A dark-themed web screenshot of a &#x22;New Repository&#x22; form in a Git hosting UI (Gitea), showing an open Owner dropdown with options like &#x22;gitea-admin&#x22; and &#x22;dasher-org.&#x22; The form includes fields for repository name, visibility, description, .gitignore and license." />
</Frame>

Create a new Git repository in your organization (for example, `shared-libraries`). Initialize it and push an initial commit:

```bash theme={null}
