# Find the Jenkins java process
ps aux | grep -i jenkins.war

# Kill the process (replace PID with the actual PID shown)
kill -9 1048864

# Check systemd status
systemctl status jenkins
```

On restart, console output typically shows the build resuming, for example:

```text theme={null}
Resuming build at Sun Nov 10 17:22:47 UTC 2024 after Jenkins restart
No need to sleep any longer
Ready to run at Sun Nov 10 17:22:48 UTC 2024
[Pipeline] sh
+ echo 40
[Pipeline] sleep
Sleeping for 1 sec
[Pipeline] sh
+ echo 41
```

Because `MAX_SURVIVABILITY` was selected, the Pipeline persisted the necessary FlowNode state and continued after the restart.

Run the same job with PERFORMANCE\_OPTIMIZED

Switch the job's durability to `PERFORMANCE_OPTIMIZED` and run it again. If Jenkins is killed and not shut down cleanly, the Pipeline will likely not be resumable. You may see output like:

```text theme={null}
Creating placeholder flownodes because failed loading originals.

ERROR: Cannot resume build because FlowNode 42 for FlowHead 1 could not be loaded. This is expected to happen when using the PERFORMANCE_OPTIMIZED durability setting and Jenkins is not shut down cleanly. Consider investigating to understand if Jenkins was not shut down cleanly or switching to the MAX_SURVIVABILITY durability setting which should prevent this issue in most cases.
[Gitea] do not publish assets due to build being non-Successfully
Finished: FAILURE
```

This demonstrates the trade-off: `PERFORMANCE_OPTIMIZED` improves throughput but risks losing resumability after unclean restarts.

> **warning** If your Pipeline performs critical operations (production deploys, database migrations, infrastructure changes), prefer `MAX_SURVIVABILITY`. For ephemeral or highly parallel workloads where throughput matters more than resuming after crashes, `PERFORMANCE_OPTIMIZED` may be appropriate.

Summary

* Use `MAX_SURVIVABILITY` for critical, long-running, or deployment Pipelines where resumability is important.
* Use `PERFORMANCE_OPTIMIZED` for high-throughput Pipelines where occasional loss on unclean restarts is acceptable.
* `SURVIVABLE_NON_ATOMIC` is a compromise between the two.
* Configure durability at the global level, per-pipeline, or per-branch for multibranch projects depending on your operational needs.

Links and references

* [Jenkins: Pipeline Basics and Documentation](https://www.jenkins.io/doc/)
* [Jenkins Pipeline Plugin](https://plugins.jenkins.io/workflow-aggregator/)
* Jenkins durability settings are configurable at: Manage Jenkins → System → Pipeline Speed / Durability

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/6f55f1ac-064a-4aec-a91a-450caaf82d63/lesson/924187c9-803d-49ab-bcb3-3efac19fca28)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/6f55f1ac-064a-4aec-a91a-450caaf82d63/lesson/c86f887d-7907-409f-9d79-9e057abda40c)


# Use JCasC create jobs

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Backup-and-Configuration-Management/Use-JCasC-create-jobs/page

Guide to using Jenkins Configuration as Code to declaratively create pipeline jobs, configure tools like Node.js, handle Job DSL dependency, apply YAML and verify created jobs and tools

In this lesson you'll learn how to use the Jenkins Configuration as Code (JCasC) plugin to declaratively create pipeline jobs and configure tools (for example, Node.js). We cover:

* Where to find JCasC demo YAML and examples
* How to add tool and job definitions to your JCasC YAML
* How to resolve a common "No configurator for jobs" error (installing the Job DSL plugin)
* How to apply the configuration and verify created jobs and tools

JCasC has many example configurations in the plugin repository demos directory. These demos are helpful starting points for configuring authentication, clouds, tools, jobs, views, and more.

<Frame>
  <img alt="A dark-themed GitHub repository view showing the &#x22;configuration-as-code-plugin&#x22; demos directory with a list of demo subfolders and recent commit messages on the right. A file tree and navigation sidebar are visible on the left." />
</Frame>

## Example snippets from the demos

Below are representative YAML fragments you will commonly use or adapt when authoring your `jenkins-casc.yaml`.

Example: set Jenkins location (unclassified section)

```yaml theme={null}
unclassified:
  location:
    url: http://jenkins/
```

Example: Kubernetes cloud configuration (relevant fields)

```yaml theme={null}
jenkins:
  clouds:
    - kubernetes:
        name: "advanced-k8s-config"
        serverUrl: "https://advanced-k8s-config:443"
        serverCertificate: "serverCertificate"
        skipTlsVerify: true
        credentialsId: "advanced-k8s-credentials"
        namespace: "default"
        jenkinsUrl: "http://jenkins/"
        jenkinsTunnel: "jenkinsTunnel"
        containerCapStr: 42
        maxRequestsPerHostStr: 64
        retentionTimeout: 5
        connectTimeout: 10
```

Example: declare a Node.js tool installation via JCasC

```yaml theme={null}
tool:
  nodejs:
    installations:
      - name: "NodeJS Latest"
        home: "" # required until nodejs-1.3.4 release (JENKINS-57508)
        properties:
          - installSource:
              installers:
                - nodeJSInstaller:
                    id: "12.11.1"
    npmPackagesRefreshHours: 48 # default is 72
```

## Where to place your JCasC file

Edit your controller’s JCasC YAML file. In this lesson the configuration file is:
`/var/lib/jenkins/JENKINS_BACKUP/jenkins-casc.yaml`

Your YAML may already contain many sections (credentials, views, plugin configs, etc.). For example, a credentials fragment might look like:

```yaml theme={null}
credentials:
  system:
    domainCredentials:
      - credentials:
          - usernamePassword:
              description: "Gitea Server Credentials"
              id: "gitea-server-creds"
              password: "{AQAAABAAAAAQA4e7WfYLRu0yZL9NsHsLaqohKKpJFtItDGTyKUsxqC0U=}"
              scope: GLOBAL
              username: "gitea-admin"
          - usernamePassword:
              description: "Credentials for MongoDB"
              id: "mongo-db-credentials"
              password: "{AQAAABAAAAAQFPgIHj2LB26zTPKnU+rDyr/G7Vm9oaLUK8x8Rpcp0iE0=}"
              scope: GLOBAL
              username: "superuser"
      - string:
          description: "Mongo Database Username"
          id: "mongo-db-username"
```

## Adding jobs via JCasC (requires Job DSL plugin)

JCasC delegates top-level `jobs:` configuration to the Job DSL configurator. This means your YAML can include embedded Job DSL scripts under a `jobs:` root. Example:

```yaml theme={null}
jobs:
  - script: >
      folder('testjobs')
  - script: >
      pipelineJob('testjobs/default-agent') {
        definition {
          cps {
            script("""
              pipeline {
                agent any
                stages {
                  stage('test') {
                    steps {
                      echo "hello"
                    }
                  }
                }
              }
            """.stripIndent())
          }
        }
      }
```

This configuration creates:

* a folder named `testjobs`
* a pipeline job `testjobs/default-agent` with a minimal pipeline that echoes "hello"

If you attempt to apply YAML containing `jobs:` before the Job DSL plugin is installed, JCasC will fail because the `jobs` configurator is not available.

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Configuration as Code&#x22; admin page showing the config source path (/var/lib/jenkins/JENKINS_BACKUP/jenkins-casc.yaml) and a red error: &#x22;No configurator for the following root elements: jobs.&#x22; The page also shows buttons to apply, reload, download, and view configuration." />
</Frame>

Here is the essential exception you may see:

```text theme={null}
io.jenkins.plugins.casc.UnknownConfiguratorException: No configurator for the following root elements: jobs
```

> **warning** If JCasC reports "No configurator for the following root elements: jobs", install the Job DSL plugin first. JCasC requires the Job DSL configurator to process any `jobs:` roots in your YAML.

## Installing the Job DSL plugin

To resolve the error, install the Job DSL plugin:

* Dashboard -> Manage Jenkins -> Manage Plugins -> Available -> search for "Job DSL" -> install.

The plugin UI looks like this:

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;Plugins&#x22; management page showing the &#x22;Available plugins&#x22; view with &#x22;Job DSL&#x22; selected. The plugin details (version, description and an adoption notice) and install controls are visible in the UI." />
</Frame>

After installing the Job DSL plugin, reload or re-apply your JCasC configuration so the new configurator is available and JCasC can process the `jobs:` root.

> **lightbulb** The Job DSL plugin must be installed before JCasC can apply job definitions under the `jobs:` root. If you add job definitions first, JCasC will report the "No configurator for ... jobs" error.

## Verify the applied configuration

After a successful apply/reload:

* Confirm a folder `testjobs` appears in the Jenkins dashboard.
* Inside it, confirm a pipeline job `default-agent` (full name `testjobs/default-agent`) exists.
* Open the job and verify the pipeline script matches the Job DSL-defined Groovy pipeline. For example:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('test') {
      steps {
        echo "hello"
      }
    }
  }
}
```

* Verify the Node.js tool under Manage Jenkins -> Global Tool Configuration: you should see `NodeJS Latest` with the declared version (e.g., `12.11.1`).

## Quick checklist

| Step | Action                                                                                                                                   |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Find demo YAML in the JCasC plugin demos: `https://github.com/jenkinsci/configuration-as-code-plugin/tree/master/demos`                  |
| 2    | Edit your `jenkins-casc.yaml` (e.g., `/var/lib/jenkins/JENKINS_BACKUP/jenkins-casc.yaml`) and add `tool:` and `jobs:` sections as needed |
| 3    | Ensure required plugins are installed (e.g., Job DSL for the `jobs:` root)                                                               |
| 4    | Apply or reload the JCasC configuration from Manage Jenkins -> Configuration as Code                                                     |
| 5    | Verify created folders, jobs, and tool installations in the Jenkins UI                                                                   |

## Troubleshooting tips

* If JCasC fails on unknown root elements, confirm the matching plugin that provides the configurator is installed (Job DSL for `jobs:`; other roots may require their own plugins).
* If a tool (like NodeJS) is not visible after applying JCasC, check the tool YAML for syntax errors and confirm the installer version ID is valid for your installed tool plugin.
* Check Manage Jenkins -> Configuration as Code for the current config source and any error messages; review controller logs for full stack traces.

## Links and references

* [Jenkins Configuration as Code (JCasC) plugin](https://plugins.jenkins.io/configuration-as-code/)
* [Job DSL plugin](https://plugins.jenkins.io/job-dsl/)
* [JCasC demos directory on GitHub](https://github.com/jenkinsci/configuration-as-code-plugin/tree/master/demos)
* [Kubernetes cloud docs (Jenkins)](https://www.jenkins.io/doc/book/clouds/kubernetes/)

That’s the basic flow for using JCasC to create jobs and configure tools.

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/6f55f1ac-064a-4aec-a91a-450caaf82d63/lesson/a393ebf1-51c1-4a3f-bfd1-605a5d8b31a0)
