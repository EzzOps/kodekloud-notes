# Automating Jenkins using CLI and APIs

Source: https://notes.kodekloud.com/docs/Jenkins-For-Beginners/Automation-and-Security/Automating-Jenkins-using-CLI-and-APIs/page

This guide explores automating Jenkins tasks using the Command-Line Interface and REST API for efficient management of jobs and plugins.

Jenkins offers powerful automation capabilities that can significantly improve your continuous integration and continuous delivery workflows. In this guide, we explore two primary methods to automate Jenkins tasks: the Jenkins Command-Line Interface (CLI) and the Jenkins REST API. Whether you prefer to interact with Jenkins via SSH or HTTP, these methods enable efficient management of jobs, plugins, and much more.

***

## Jenkins CLI via SSH

The Jenkins CLI allows both users and administrators to interact directly with Jenkins from a shell or script, streamlining daily tasks and integrations. You can access the CLI over SSH or via a downloadable Java-based client. When using SSH, note that the SSH service is disabled by default. Jenkins will select a random port for SSH connections, so you need to determine the port number first.

<Callout icon="lightbulb">
  Ensure that the SSH service is enabled and your public key is added to the Jenkins user configuration before attempting SSH-based sessions.
</Callout>

### Retrieve the SSH Port

Run the following command to obtain the SSH port used by Jenkins:

```bash theme={null}
curl -Lv https://JENKINS_URL/login 2>&1 | grep -i 'x-ssh-endpoint'
