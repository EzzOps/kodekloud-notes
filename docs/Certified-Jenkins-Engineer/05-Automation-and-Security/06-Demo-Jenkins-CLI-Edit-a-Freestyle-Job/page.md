# Switch to home directory and download the CLI JAR
cd ~
wget http://139.84.159.194:8080/jnlpJars/jenkins-cli.jar
```

Verify the download:

```bash theme={null}
ls
# docker-compose.yml  gitea  jenkins-cli.jar
```

## 2. Explore Available CLI Commands

List all CLI commands and options:

```bash theme={null}
java -jar jenkins-cli.jar -s http://139.84.159.194:8080/ help
```

Check your current identity:

```bash theme={null}
java -jar jenkins-cli.jar -s http://139.84.159.194:8080/ who-am-i
```

```text theme={null}
Authenticated as: anonymous
Authorities:
  anonymous
```

Attempting to list jobs without proper credentials results in:

```bash theme={null}
java -jar jenkins-cli.jar -s http://139.84.159.194:8080/ list-jobs
```

```text theme={null}
ERROR: anonymous is missing the Overall/Read permission
```

## 3. Authenticate with Username and Password

Use `-auth USER:SECRET` to provide credentials. For example:

```bash theme={null}
java -jar jenkins-cli.jar -s http://139.84.159.194:8080/ \
  -auth admin:password \
  list-jobs
```

```text theme={null}
ascii-build-job
ascii-deploy-job
ascii-test-job
Generate ASCII Artwork
hello-world-pipeline
jenkins-hello-world
parameterized-pipeline-job
```

Confirm your authenticated identity:

```bash theme={null}
java -jar jenkins-cli.jar -s http://139.84.159.194:8080/ \
  -auth admin:password \
  who-am-i
```

```text theme={null}
Authenticated as: admin
Authorities:
  authenticated
```

> **triangle-alert** Avoid embedding plaintext passwords in scripts. Use [Jenkins API tokens](https://www.jenkins.io/doc/book/security/managing-tokens/) or SSH key authentication for better security.

## 4. Build Command and Flags

The `build` command accepts several useful flags:

| Flag         | Description                                |
| ------------ | ------------------------------------------ |
| -f           | Follow the live build output               |
| -p KEY=VALUE | Pass one or more build parameters          |
| -s           | Wait until the build completes             |
| -v           | Include the full console log in the output |
| -w           | Wait until the build starts                |

## 5. Triggering a Parameterized Job

To trigger `parameterized-pipeline-job` with a `BRANCH_NAME` parameter:

```bash theme={null}
java -jar jenkins-cli.jar -s http://139.84.159.194:8080/ \
  -auth admin:password \
  build parameterized-pipeline-job -f -p BRANCH_NAME=test
```

```text theme={null}
Started parameterized-pipeline-job #4
Completed parameterized-pipeline-job #4 : SUCCESS
```

## 6. View Job Status in Jenkins UI

After running the CLI command, you can monitor the build status and trends in the Jenkins dashboard:

![The image shows a Jenkins dashboard displaying the status of a parameterized pipeline job, with a test result trend graph and a detailed pipeline execution timeline.](https://kodekloud.com/kk-media/image/upload/v1752870387/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-CLI-Build-a-job/jenkins-dashboard-pipeline-job-status.jpg)

## 7. Include Full Console Output

If you need detailed logs in your terminal, add the `-v` flag:

```bash theme={null}
java -jar jenkins-cli.jar -s http://139.84.159.194:8080/ \
  -auth admin:password \
  build parameterized-pipeline-job -f -v -p BRANCH_NAME=test
```

```text theme={null}
[Pipeline] Start of Pipeline
...
[INFO] Total time:  3.452 s
[INFO] Finished at: 2024-08-19T19:42:29Z
...
[Pipeline] End of Pipeline
Finished: SUCCESS
Completed parameterized-pipeline-job #5 : SUCCESS
```

***

You can automate these steps in shell scripts or integrate them into your CI/CD pipelines. Beyond building jobs, the Jenkins CLI lets you manage views, plugins, credentials, and more.

## Links and References

* [Jenkins CLI Documentation](https://www.jenkins.io/doc/book/managing/cli/)
* [Jenkins Security: Managing API Tokens](https://www.jenkins.io/doc/book/security/managing-tokens/)
* [Jenkins User Handbook](https://www.jenkins.io/user-handbook.pdf)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/4d6d1f39-307c-4fdb-8d2b-834c1650e792/lesson/fcc53022-d54d-46d0-b364-23f76bd91201)


# Demo Jenkins CLI Edit a Freestyle Job

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Automation-and-Security/Demo-Jenkins-CLI-Edit-a-Freestyle-Job/page

This tutorial explains how to edit a Freestyle job in Jenkins using the Jenkins CLI.

In this tutorial, you’ll learn how to fetch, modify, and update a Freestyle job (`npm-version-test`) on Jenkins using the [Jenkins CLI](https://www.jenkins.io/doc/book/managing/cli/). The job prints the installed [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) versions. We’ll download its XML configuration, adjust the build steps, and push the changes back.

## Prerequisites

* Jenkins server accessible at `http://localhost:8080/`
* `jenkins-cli.jar` downloaded locally
* CLI access via SSH; for example:
  ```bash theme={null}
  ssh -l <user> -p <port> localhost
  ```

| Authentication Method | Command Example                                            |
| --------------------- | ---------------------------------------------------------- |
| HTTP                  | `java -jar jenkins-cli.jar -s http://localhost:8080/ help` |
| SSH                   | `ssh -l siddharth -p 41397 localhost help`                 |

## 1. Check Installed Node.js & npm

First, verify your local Node.js and npm versions:

```bash theme={null}
node -v
npm -v
```

## 2. Download the Job Configuration

Fetch the existing job’s XML to a local file.

### 2.1 Using HTTP

```bash theme={null}
java -jar jenkins-cli.jar -s http://localhost:8080/ get-job npm-version-test > npm-job.xml
```

### 2.2 Using SSH

```bash theme={null}
ssh -l siddharth -p 41397 localhost get-job npm-version-test > npm-job.xml
```

> **lightbulb** Always back up your existing XML before editing. You can keep a copy:

  ```bash theme={null}
  cp npm-job.xml npm-job.xml.bak
  ```

## 3. Inspect the Current Configuration

Open `npm-job.xml` and locate the `<builders>` section. It should resemble:

```xml theme={null}
<project>
  ...
  <builders>
    <hudson.tasks.Shell>
      <command>node -v</command>
      <configuredLocalRules/>
    </hudson.tasks.Shell>
  </builders>
  ...
</project>
```

## 4. Update the Build Steps

Modify `npm-job.xml` so the shell step echoes a message and invokes both Node.js and npm versions. Replace the `<builders>` section with:

```xml theme={null}
<project>
  ...
  <builders>
    <hudson.tasks.Shell>
      <command>
        echo "Updating job config using Jenkins CLI"
        node -v
        npm -v
      </command>
      <configuredLocalRules/>
    </hudson.tasks.Shell>
  </builders>
  ...
  <buildWrappers>
    <jenkins.plugins.timestamper.TimestamperBuildWrapper plugin="timestamper@1.27"/>
    <jenkins.plugins.nodejs.NodeJSBuildWrapper plugin="nodejs@1.6.2">
      <nodeJSInstallationName>nodejs-22-6-0</nodeJSInstallationName>
      <cacheLocationStrategy class="jenkins.plugins.nodejs.cache.DefaultCacheLocationLocator"/>
    </jenkins.plugins.nodejs.NodeJSBuildWrapper>
  </buildWrappers>
</project>
```

Save your edits to `npm-job.xml`.

## 5. Push the Updated Configuration

Send the modified XML back to Jenkins:

### 5.1 Via SSH

```bash theme={null}
ssh -l siddharth -p 41397 localhost update-job npm-version-test < npm-job.xml
```

### 5.2 Via HTTP

```bash theme={null}
java -jar jenkins-cli.jar -s http://localhost:8080/ update-job npm-version-test < npm-job.xml
```

A successful update returns no output.

## 6. Verify Your Changes

1. In the Jenkins UI, open **npm-version-test**.
2. Check that the build step now shows:
   ```bash theme={null}
   echo "Updating job config using Jenkins CLI"
   node -v
   npm -v
   ```
3. Trigger a new build. The console log should display something like:

   ```text theme={null}
   Started by user siddharth
   Building on the built-in node in workspace /var/lib/jenkins/workspace/npm-version-test
   + echo Updating job config using Jenkins CLI
   Updating job config using Jenkins CLI
   + node -v
   v22.6.0
   + npm -v
   10.8.2
   Finished: SUCCESS
   ```

That’s it! You’ve successfully edited a Freestyle job’s configuration and updated it in Jenkins using the CLI.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/4d6d1f39-307c-4fdb-8d2b-834c1650e792/lesson/0574086d-2d1d-427d-a91c-d1cb8780c9d6)
