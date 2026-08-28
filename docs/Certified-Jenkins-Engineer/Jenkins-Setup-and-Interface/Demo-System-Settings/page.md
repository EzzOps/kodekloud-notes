# Confirm the download
ls -lh jenkins.war
# -rw-r--r-- 1 root root 92M Jan  8 16:34 jenkins.war
```

***

## 3. Launching Jenkins with Custom Parameters

By default, `java -jar jenkins.war` binds to port 8080—which conflicts with the apt-installed service. Override this with:

```bash theme={null}
java -jar jenkins.war --httpPort=7777 --prefix=/dasher-technologies
```

After a few seconds, you’ll see Jetty start up and the initial setup wizard prompt:

```text theme={null}
2025-02-05 18:09:12.026+0000 [id=1]  INFO  org.eclipse.jetty.server.Server#doStart: Started Server@19c65cdc{STARTING}[12.0.16,sto=0] @1525ms
...
***********************************************************************
Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:
456e352c1ea424f9bfc923315957c2
This may also be found at: /root/.jenkins/secrets/initialAdminPassword
***********************************************************************
```

<Callout icon="lightbulb">
  Save the generated password. You can always retrieve it later from `/root/.jenkins/secrets/initialAdminPassword`.
</Callout>

***

## 4. Unlocking Jenkins and Installing Plugins

Open your browser at:

```text theme={null}
http://localhost:7777/dasher-technologies
```

Enter the admin password when prompted. The setup wizard will then let you:

* Install **Suggested Plugins**
* **Select Plugins** to customize your install

<Frame>
  ![The image shows a Jenkins setup wizard screen with options to "Install suggested plugins" or "Select plugins to install."](https://kodekloud.com/kk-media/image/upload/v1752870848/notes-assets/images/Certified-Jenkins-Engineer-Demo-Running-the-Jenkins-WAR-as-a-standalone-application/jenkins-setup-wizard-plugins.jpg)
</Frame>

***

## 5. Common Startup Options

Jenkins supports various JVM and server flags. Below are frequently used HTTP/HTTPS settings:

| Option                        | Description                                     | Example                        |
| ----------------------------- | ----------------------------------------------- | ------------------------------ |
| `--httpPort=<port>`           | Bind HTTP server to this port                   | `--httpPort=7777`              |
| `--httpListenAddress=<addr>`  | Set HTTP bind address                           | `--httpListenAddress=0.0.0.0`  |
| `--httpsPort=<port>`          | Enable HTTPS on this port (use `-1` to disable) | `--httpsPort=8443`             |
| `--httpsListenAddress=<addr>` | Set HTTPS bind address                          | `--httpsListenAddress=0.0.0.0` |
| `--prefix=<context-path>`     | Specify the URL prefix (context path)           | `--prefix=/custom-path`        |
| `--sessionTimeout=<minutes>`  | Define session timeout in minutes               | `--sessionTimeout=30`          |
| `--httpsKeyStore=<path>`      | Path to your Java keystore for HTTPS            | `/path/to/keystore`            |
| `--httpsKeyStorePassword=`    | Password for the HTTPS keystore                 | `YourPassword`                 |

For the complete list of server options, see [Jenkins HTTP Server Options].

***

## 6. Verifying Multiple Jenkins Instances

In another terminal, confirm both the `apt`-installed and standalone WAR instances are running:

```bash theme={null}
ps aux | grep -i jenkins
```

```text theme={null}
jenkins   27173  5.4  8.8 10874592 1435160 ?     Ssl  17:52   1.02 /usr/bin/java -Xms1G -Xmx1G -jar /usr/share/java/jenkins.war --webroot=/var/cache/jenkins/war --httpPort=8080
root      31980 19.6  5.6 13983116  912304 pts/6 Sl+  18:09   0.21 java -jar jenkins.war --httpPort=7777 --prefix=/dasher-technologies
root      32769  0.0  0.0   4088   1960 pts/8 S+   18:11   0.00 grep --color=auto -i jenkins
```

You now have two independent Jenkins servers running:

* Port **8080** via `apt`
* Port **7777** with custom context `/dasher-technologies`

Thank you for following this demo!

***

## Links and References

* [Jenkins HTTP Server Options]
* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Get Jenkins WAR](https://get.jenkins.io/war/)

[Jenkins HTTP Server Options]: https://www.jenkins.io/doc/book/managing/system-properties/#http-server-options

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7ab00946-0edd-4a13-b5c8-1b5001779f1c/lesson/666ff7c7-bedf-439d-ba84-6843b594b096" />
</CardGroup>


# Demo System Settings

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Setup-and-Interface/Demo-System-Settings/page

This article covers configuring key settings in Jenkins, including node parameters, Jenkins URL, and system administrator email for notifications.

In this lesson, we explore the key sections under **Manage Jenkins → Configure System**. You’ll learn how to adjust node parameters, set your Jenkins URL, and specify the system administrator email for notifications.

## Node Configuration

On the **Configure System** page, the primary node settings include:

| Setting             | Description                                                   | Default/Example                   |
| ------------------- | ------------------------------------------------------------- | --------------------------------- |
| Home directory      | Filesystem path where Jenkins stores all data                 | `/var/jenkins_home`               |
| System message      | Custom text displayed at the top of the dashboard             | —                                 |
| Number of executors | How many concurrent builds this node can run                  | 2                                 |
| Labels              | Identifiers for targeting this node in jobs                   | none                              |
| Usage               | Scheduling policy (e.g., “Use this node as much as possible”) | Use this node as much as possible |

<Frame>
  ![The image shows a Jenkins system configuration page in a web browser, with options for setting the number of executors, usage preferences, and other settings.](https://kodekloud.com/kk-media/image/upload/v1752870849/notes-assets/images/Certified-Jenkins-Engineer-Demo-System-Settings/jenkins-system-configuration-page.jpg)
</Frame>

<Callout icon="lightbulb">
  You can enforce naming conventions by defining patterns under the **Item naming** section. This practice improves consistency across jobs.
</Callout>

## Jenkins Location

Accurately setting the Jenkins URL is critical for links, webhooks, and notifications. Keep these best practices in mind:

* Choose a memorable hostname, for example, `jenkins.example.com`.
* Always use **HTTPS** to secure traffic.
* Avoid exposing internal hostnames or overly complex domains.

<Callout icon="triangle-alert">
  Configuring `localhost` as your Jenkins URL in production will trigger warnings and prevent external integrations from working correctly.
</Callout>

<Frame>
  ![The image shows a Jenkins system configuration page in a web browser, where the Jenkins URL is being set, and a warning message indicates the need for a valid host name instead of "localhost."](https://kodekloud.com/kk-media/image/upload/v1752870851/notes-assets/images/Certified-Jenkins-Engineer-Demo-System-Settings/jenkins-system-configuration-warning.jpg)
</Frame>

In this local demo, we’ll revert to:

```text theme={null}
http://localhost:8080
```

but be sure to replace it with your HTTPS address in a real deployment.

## System Admin Email

Specify the system administrator’s email address to receive critical alerts and build-failure notifications. This field integrates with your email notification settings, ensuring you’re alerted to issues in real time.

## Links and References

* [Jenkins System Configuration](https://www.jenkins.io/doc/book/managing/system-configuration/)
* [Jenkins Location Section](https://www.jenkins.io/doc/book/managing/system-configuration/#jenkins-location)
* [Configuring Email Notifications](https://www.jenkins.io/doc/pipeline/steps/mail/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7ab00946-0edd-4a13-b5c8-1b5001779f1c/lesson/884b6ecc-181f-4a26-92b1-f3fdc2194e1e" />
</CardGroup>
