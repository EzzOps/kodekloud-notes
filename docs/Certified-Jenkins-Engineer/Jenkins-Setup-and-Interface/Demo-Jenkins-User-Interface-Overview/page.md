# Command 'java' not found
```

<Callout icon="triangle-alert">
  Jenkins requires a supported Java runtime to start. Installing or configuring Java is mandatory.
</Callout>

## 6. Install Java 17

Jenkins LTS supports **Java 17** per the [Java Support Policy][java-support].

<Frame>
  ![The image shows a webpage from Jenkins' documentation detailing the Java Support Policy, including supported Java versions and their corresponding long-term support and weekly release versions.](https://kodekloud.com/kk-media/image/upload/v1752870826/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Installation/jenkins-java-support-policy-docs.jpg)
</Frame>

Install OpenJDK 17 and fontconfig:

```bash theme={null}
sudo apt update
sudo apt install -y openjdk-17-jre fontconfig
java -version
```

Expected output:

```plaintext theme={null}
openjdk version "17.0.8" 2023-07-18
OpenJDK Runtime Environment (build 17.0.8+7-Debian-1deb12u1)
OpenJDK 64-Bit Server VM (build 17.0.8+7-Debian-1deb12u1, mixed mode)
```

## 7. Start Jenkins

Restart and check status:

```bash theme={null}
sudo systemctl restart jenkins
sudo systemctl status jenkins
```

You should see:

```plaintext theme={null}
● jenkins.service - Jenkins Continuous Integration Server
   Active: active (running) since Mon 2024-08-19 08:03:40 UTC; 10s ago
 Main PID: 34102 (java)
    CGroup: /system.slice/jenkins.service
           └─34102 /usr/bin/java -Djava.awt.headless=true -jar /usr/share/java/jenkins.war ...
```

## 8. Retrieve Initial Admin Password

Find the initial admin password in the logs:

```bash theme={null}
sudo journalctl -u jenkins | grep 'initialAdminPassword'
```

Or directly read the file:

```bash theme={null}
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Inspect the Jenkins home directory:

```bash theme={null}
ls /var/lib/jenkins
# config.xml  plugins  secrets  updates  users  jobs  ...
```

## 9. Complete Setup Wizard

1. Open `http://<YOUR_VM_IP>:8080` in your browser.
2. **Unlock Jenkins** with the admin password from `/var/lib/jenkins/secrets/initialAdminPassword`.
3. **Select Plugins**
   * Choose **Suggested Plugins** or pick specific ones.

<Frame>
  ![The image shows a Jenkins setup wizard interface with options for selecting plugins related to organization, administration, and build features. The user can choose from various plugins to install.](https://kodekloud.com/kk-media/image/upload/v1752870828/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Installation/jenkins-setup-wizard-plugins.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins setup wizard interface, specifically the "Pipelines and Continuous Delivery" section, where various plugins related to pipelines are listed for selection.](https://kodekloud.com/kk-media/image/upload/v1752870829/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Installation/jenkins-pipelines-setup-wizard.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins setup wizard interface with options for configuring plugins related to source code management, distributed builds, and user management and security. The interface includes checkboxes for selecting specific plugins to install.](https://kodekloud.com/kk-media/image/upload/v1752870830/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Installation/jenkins-setup-wizard-plugins-interface.jpg)
</Frame>

4. **Choose Appearance**\
   Pick your UI theme (e.g., Dark Theme):

<Frame>
  ![The image shows a Jenkins setup wizard interface with options for configuring notifications, appearance, and languages. The "Dark Theme" option is selected under the Appearance section.](https://kodekloud.com/kk-media/image/upload/v1752870834/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Installation/jenkins-setup-wizard-dark-theme.jpg)
</Frame>

5. **Create First Admin User**\
   Fill in credentials:

<Frame>
  ![The image shows a web page for creating the first admin user in a setup wizard, with fields for username, password, full name, and email address.](https://kodekloud.com/kk-media/image/upload/v1752870835/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Installation/admin-user-setup-wizard-page.jpg)
</Frame>

6. **Configure Jenkins URL**\
   Confirm or edit the root URL, then **Save and Finish**:

<Frame>
  ![The image shows a Jenkins setup wizard screen for instance configuration, prompting the user to enter a Jenkins URL. There are options to "Save and Finish" or "Not now."](https://kodekloud.com/kk-media/image/upload/v1752870837/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Installation/jenkins-setup-wizard-url-config.jpg)
</Frame>

Once done, Jenkins will be ready to use. Start creating your first build pipeline!

## 10. References

* [Jenkins Download & Setup][download]
* [Linux Prerequisites for Jenkins][prereq]
* [Jenkins Java Support Policy][java-support]
* [Jenkins Official Documentation][jenkins-docs]

[download]: https://www.jenkins.io/download/

[prereq]: https://www.jenkins.io/doc/book/installing/#prerequisites

[java-support]: https://www.jenkins.io/doc/book/system-administration/java/

[jenkins-docs]: https://www.jenkins.io/doc/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7ab00946-0edd-4a13-b5c8-1b5001779f1c/lesson/07cb1d74-2ff6-492e-8f56-1d08525cd038" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7ab00946-0edd-4a13-b5c8-1b5001779f1c/lesson/aeaa6095-8d5d-4470-9c89-33bfa2014677" />
</CardGroup>


# Demo Jenkins User Interface Overview

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Setup-and-Interface/Demo-Jenkins-User-Interface-Overview/page

This lesson explores the core components of the Jenkins user interface, including version checking, login, and managing system settings and plugins.

In this lesson, we’ll explore the core components of the Jenkins user interface—from checking your version and logging in to managing system settings, plugins, and themes. By the end, you’ll be comfortable navigating Jenkins’ dashboard and administering your CI/CD environment.

## About Jenkins Version

Before logging in, you can verify the exact Jenkins release and view its dependencies:

1. On the login page, click the Jenkins icon in the bottom-right corner.
2. The **About Jenkins** dialog displays your version (e.g., 2.462.1), open-source capabilities, and a list of Mavenized dependencies with license links.

<Frame>
  ![The image shows the "About Jenkins" page from a Jenkins server, displaying version 2.462.1 and information about its open-source automation capabilities. It includes a list of Mavenized dependencies with their licenses.](https://kodekloud.com/kk-media/image/upload/v1752870838/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-User-Interface-Overview/about-jenkins-version-2-462-1.jpg)
</Frame>

<Callout icon="lightbulb">
  Each dependency link takes you to more information about the library’s purpose and license. This helps you stay compliant with open-source requirements.
</Callout>

## Jenkins Login

Authenticate with your configured credentials on the default login screen:

<Frame>
  ![The image shows a Jenkins login page with fields for username and password, alongside the Jenkins logo on a colorful background.](https://kodekloud.com/kk-media/image/upload/v1752870839/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-User-Interface-Overview/jenkins-login-page-username-password.jpg)
</Frame>

1. Enter your **Username** and **Password**.
2. Click **Sign in** to access the Jenkins dashboard.

## Dashboard & Manage Jenkins

Once logged in, you land on the Jenkins dashboard. To adjust system-wide settings:

1. Click **Manage Jenkins** in the left-hand menu.
2. Review any security warnings at the top (for example, running the master and build node together).

<Frame>
  ![The image shows the "Manage Jenkins" dashboard, displaying various configuration options and a security warning about using the built-in node.](https://kodekloud.com/kk-media/image/upload/v1752870840/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-User-Interface-Overview/manage-jenkins-dashboard-configuration.jpg)
</Frame>

<Callout icon="triangle-alert">
  Running both the master and build node on the same server is not recommended for production workloads. Consider separating build agents to improve security and reliability.
</Callout>

### Manage Jenkins: Configuration Categories

| Category             | Description                                                          |
| -------------------- | -------------------------------------------------------------------- |
| System Configuration | Home directory, executors, labels, URLs, admin email, global message |
| Security             | Configure authentication, authorization, and access control          |
| System Information   | JVM properties, environment variables, and system details            |
| Troubleshooting      | Logs, system logs, and diagnostic tools                              |
| Tools                | Global tool installations (e.g., JDK, Maven, Git)                    |
| Actions              | Reload configuration, safe restart, script console                   |

> Additional sections appear here when you install plugins (e.g., Credentials, Global Pipeline Libraries).

## System Configuration

Under **System Configuration**, you can set critical system parameters:

* **Jenkins Home Directory**
  ```bash theme={null}
  /var/lib/jenkins
  ```
* **Global System Message**
* **Number of Executors** (parallel build slots)
* **Agent Labels**
* **Jenkins URL**
* **System Admin E-mail Address**

Hover over the question-mark icon next to each field to view context-sensitive help. For example:

```text theme={null}
Jenkins URL: http://139.84.159.194:8080/
System Admin E-mail address: nobody@nowhere
```

After editing, click **Apply** (save and stay) or **Save** (save and return to dashboard).

<Frame>
  ![The image shows a Jenkins system configuration page where a system message is being set to "Welcome to Dasher CI Organization," with options to save or apply changes.](https://kodekloud.com/kk-media/image/upload/v1752870841/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-User-Interface-Overview/jenkins-system-configuration-dasher-ci.jpg)
</Frame>

<Callout icon="lightbulb">
  Use the **Global System Message** to broadcast maintenance windows or announcements directly on the dashboard.
</Callout>

## System Information & Plugins

### System Information

* View JVM properties, environment variables, and classpath entries.
* Inspect memory usage, file descriptors, and real-time performance graphs.

### Plugin Manager

* Review installed plugins, versions, and enable/disable status.
* Common plugins include Pipeline, [Parameterized Trigger](https://plugins.jenkins.io/parameterized-trigger/), Git, and Blue Ocean.

<Frame>
  ![The image shows a Jenkins system information page displaying a list of installed plugins, their versions, and their enabled status. The interface includes navigation options and a search bar.](https://kodekloud.com/kk-media/image/upload/v1752870842/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-User-Interface-Overview/jenkins-plugins-info-page.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins dashboard displaying system information, specifically focusing on memory usage over time. The interface includes navigation options and a graph illustrating memory data.](https://kodekloud.com/kk-media/image/upload/v1752870843/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-User-Interface-Overview/jenkins-dashboard-memory-usage-graph.jpg)
</Frame>

## System Logs

Quickly troubleshoot by viewing logs in the UI:

* Navigate to **Manage Jenkins > System Log**.
* Or, on the server use `journalctl` or inspect `$JENKINS_HOME/logs/jenkins.log`.

For more details, see the [journalctl documentation](https://www.freedesktop.org/software/systemd/man/journalctl.html).

## Appearance & Themes

Customize the look and feel with plugins such as [Dark Theme](https://plugins.jenkins.io/dark-theme/):

1. Install **Dark Theme**.
2. Select **Manage Jenkins > Configure Global Security** (or similar).
3. Enable **Dark Theme** and additional options (e.g., pipeline graphs on job pages).
4. Click **Save**.

***

## Links and References

* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)
* [Parameterized Trigger Plugin](https://plugins.jenkins.io/parameterized-trigger/)
* [Dark Theme Plugin](https://plugins.jenkins.io/dark-theme/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7ab00946-0edd-4a13-b5c8-1b5001779f1c/lesson/4bbf41e6-d736-425f-b5b3-b9d5a54f8856" />
</CardGroup>
