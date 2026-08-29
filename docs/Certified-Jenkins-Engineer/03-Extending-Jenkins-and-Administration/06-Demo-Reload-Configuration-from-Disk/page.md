# Demo Reload Configuration from Disk

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Extending-Jenkins-and-Administration/Demo-Reload-Configuration-from-Disk/page

Reloading configuration from disk allows Jenkins to apply filesystem changes without a full restart, useful for editing settings or moving jobs.

Reloading configuration from disk allows Jenkins to pick up changes made directly to its filesystem without requiring a full restart. This is useful when you’ve edited `config.xml`, moved or renamed jobs via CLI, or updated your Jenkins home directory externally.

## When to Use “Reload Configuration from Disk”

Use this feature to apply external changes immediately:

| Scenario                          | Description                                                    | Command / UI Path                                          |
| --------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------- |
| Update `config.xml`               | Edit system settings or messages                               | `vi $JENKINS_HOME/config.xml`                              |
| Rename or move jobs               | Relocate job folders in the filesystem                         | `mv $JENKINS_HOME/jobs/old-job $JENKINS_HOME/jobs/new-job` |
| Adjust security or plugin configs | Change security realm, authorization strategy, or plugin files | N/A                                                        |

> **lightbulb** Reloading configuration does not apply plugin installations or upgrades. For plugin changes, use **Manage Plugins** and restart if required.

## 1. Update Configuration via the Jenkins UI

1. Navigate to **Dashboard** → **Manage Jenkins** → **Configure System**.
2. Find the **System Message** field.
3. Enter a new message (e.g., “Welcome to KodeKloud”) and click **Save**.
4. Verify the dashboard shows your updated system message.

## 2. Edit Configuration on the Filesystem

1. SSH into your Jenkins server and switch to the Jenkins home directory:
   ```bash theme={null}
   cd $JENKINS_HOME
   ```
2. Open the main configuration file in your preferred editor:
   ```bash theme={null}
   vi config.xml
   ```
3. Locate the `<systemMessage>` tag. Example before change:
   ```xml theme={null}
   <systemMessage>Welcome to coded.ku</systemMessage>
   ```
4. Update it to your desired text:
   ```xml theme={null}
   <systemMessage>Welcome to Dasher Technologies</systemMessage>
   ```
5. Save and exit the editor.
6. Confirm the change:
   ```bash theme={null}
   grep -i systemMessage config.xml
   ```
   Output should be:
   ```XML theme={null}
   <systemMessage>Welcome to Dasher Technologies</systemMessage>
   ```

At this point, the Jenkins UI still displays the old message, since the configuration hasn’t been reloaded.

## 3. Reload Configuration from Disk

1. In Jenkins, go to **Dashboard** → **Manage Jenkins**.
2. Scroll to **Tools and Actions** and click **Reload Configuration from Disk**.
3. Confirm the prompt to proceed. Jenkins will re-import all configuration files.

After a few seconds, your dashboard’s **System Message** updates to “Welcome to Dasher Technologies.”

> **triangle-alert** Performing a reload can briefly impact running jobs. Avoid frequent reloads during peak build activity.

## Benefits of Reloading from Disk

* Instant application of file-based edits
* No need for a full Jenkins restart
* Applies to jobs, system settings, security, and folder configurations

## References

* [Jenkins Configuration as Code](https://www.jenkins.io/projects/jcasc/)
* [Jenkins CLI Documentation](https://www.jenkins.io/doc/book/managing/cli/)
* [Manage Jenkins – Official Guide](https://www.jenkins.io/doc/book/managing/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/6113113b-7852-401b-9c41-c5bc8242ad99/lesson/86da24b3-dff4-4f1d-9076-5216d2122618)
