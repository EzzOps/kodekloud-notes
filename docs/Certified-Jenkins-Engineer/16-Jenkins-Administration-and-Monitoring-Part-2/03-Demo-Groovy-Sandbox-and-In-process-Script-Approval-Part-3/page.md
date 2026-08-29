# Demo Groovy Sandbox and In process Script Approval Part 3

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-2/Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/page

This demo explains how Jenkins Groovy Sandbox enforces security through whitelisting and blacklisting methods, and how to approve blocked signatures.

Welcome to the third installment of our Jenkins Groovy Sandbox series. In this demo you’ll learn how the sandbox enforces security by whitelisting and blacklisting Groovy methods, and how administrators can approve blocked signatures via **In-process Script Approval**.

***

## Table of Contents

1. [Understanding Whitelists & Blacklists](#understanding-whitelists--blacklists)
2. [Inspecting the Whitelist](#inspecting-the-whitelist)
3. [Inspecting the Blacklist](#inspecting-the-blacklist)
4. [Adding Blacklisted Calls to a Pipeline](#adding-blacklisted-calls-to-a-pipeline)
5. [First Build: `getInstance` Blocked](#first-build-getinstance-blocked)
6. [Approving Signatures in Jenkins](#approving-signatures-in-jenkins)
7. [Second Build: `getProperty` Blocked](#second-build-getproperty-blocked)
8. [Final Build: Success!](#final-build-success)
9. [References](#references)

***

## Understanding Whitelists & Blacklists

Jenkins uses the [script-security plugin](https://github.com/jenkinsci/script-security-plugin) to sandbox Groovy scripts.\
Under `src/main/resources/org/jenkinsci/plugins/scriptsecurity/sandbox/whitelists` you’ll find files that list allowed methods. The same folder contains a `blacklist` file defining methods that are blocked by default and require admin approval.

| List Type | Purpose                                             | Sample Entry                                 |
| --------- | --------------------------------------------------- | -------------------------------------------- |
| Whitelist | API methods and signatures allowed in sandbox       | `method hudson.model.Run getFullDisplayName` |
| Blacklist | Methods blocked unless approved via Script Approval | `method java.io.Reader read`                 |

***

## Inspecting the Whitelist

Browse the [Jenkins script-security-plugin repository on GitHub](https://github.com/jenkinsci/script-security-plugin) and open the `whitelists` folder:

![The image shows a GitHub repository page for the "script-security-plugin" by "jenkinsci," displaying a file named "jenkins-whitelist" with a list of Jenkins API methods. The interface includes navigation options and a code viewer.](https://kodekloud.com/kk-media/image/upload/v1752870686/notes-assets/images/Certified-Jenkins-Engineer-Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/github-repo-script-security-plugin.jpg)

An excerpt from `jenkins-whitelist`:

```plaintext theme={null}
staticField hudson.model.Result ABORTED
staticField hudson.model.Result FAILURE
staticMethod hudson.model.Result fromString java.lang.String
method hudson.model.Run getFullDisplayName
method hudson.model.User getId
...
staticField jenkins.model.Jenkins VERSION
```

***

## Inspecting the Blacklist

The `blacklist` file in the same directory lists methods that are disallowed by default:

```plaintext theme={null}
method groovy.lang.Closure ncurry int java.lang.Object
new java.io.PrintWriter java.lang.String
method java.io.Reader read char[] int int
...
staticMethod groovy.xml.XmlUtil escapeXml java.lang.String
```

![The image shows a GitHub repository page displaying a file named "blacklist" from the "script-security-plugin" project. The file contains a list of Java methods and classes related to security restrictions in Jenkins.](https://kodekloud.com/kk-media/image/upload/v1752870688/notes-assets/images/Certified-Jenkins-Engineer-Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/github-repo-script-security-blacklist.jpg)

Any invocation of these methods in a sandboxed pipeline will be rejected unless approved.

***

## Adding Blacklisted Calls to a Pipeline

Let’s modify a declarative pipeline to call two blacklisted methods:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('Topic') {
      steps {
        echo 'Exploring Groovy Sandbox'
      }
    }
    stage('Get Hudson Instance') {
      steps {
        script {
          // This staticMethod is blacklisted by default
          def hudson = hudson.model.Hudson.getInstance()
          println "Hudson Instance: ${hudson}"
        }
      }
    }
    stage('Get System Property') {
      steps {
        script {
          // This method is also blacklisted by default
          def userName = java.lang.System.getProperty("user.name")
          println "System Property: ${userName}"
        }
      }
    }
  }
}
```

> **lightbulb** Make sure **Use Groovy Sandbox** is checked in your pipeline configuration before running the build.

![The image shows a configuration screen for a Jenkins pipeline, displaying a Groovy script with stages to get a Hudson instance and a system property. There are options to approve the script and use the Groovy sandbox.](https://kodekloud.com/kk-media/image/upload/v1752870689/notes-assets/images/Certified-Jenkins-Engineer-Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/jenkins-pipeline-configuration-groovy.jpg)

***

## First Build: getInstance Blocked

The **Topic** stage will pass, but **Get Hudson Instance** fails due to the blacklist:

![The image shows a Jenkins dashboard displaying the status of a pipeline named "groovy-sandbox-test," with various stages and their completion statuses.](https://kodekloud.com/kk-media/image/upload/v1752870690/notes-assets/images/Certified-Jenkins-Engineer-Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/jenkins-dashboard-groovy-sandbox-test.jpg)

Console output:

![The image shows a Jenkins console output with a Groovy script execution, highlighting a permission error related to using a static method. The sidebar includes options like "Open Blue Ocean" and "Pipeline Overview."](https://kodekloud.com/kk-media/image/upload/v1752870690/notes-assets/images/Certified-Jenkins-Engineer-Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/jenkins-console-groovy-permission-error.jpg)

```plaintext theme={null}
Scripts not permitted to use staticMethod hudson.model.Hudson getInstance
```

***

## Approving Signatures in Jenkins

Click the error link or navigate to **Manage Jenkins → In-process Script Approval** to review pending signatures:

![The image shows a Jenkins script approval interface with options to approve or deny script signatures, and a warning about potential security vulnerabilities.](https://kodekloud.com/kk-media/image/upload/v1752870691/notes-assets/images/Certified-Jenkins-Engineer-Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/jenkins-script-approval-interface.jpg)

> **triangle-alert** Approving method signatures grants scripts additional privileges. Review each request carefully.

Approve the `hudson.model.Hudson getInstance` signature, then rerun the build.

***

## Second Build: getProperty Blocked

After approving, **Get Hudson Instance** now succeeds but **Get System Property** fails:

![The image shows a Jenkins console output with a script error message indicating that a script is not permitted to use a specific Java method. It suggests that administrators can decide whether to approve or reject the signature.](https://kodekloud.com/kk-media/image/upload/v1752870692/notes-assets/images/Certified-Jenkins-Engineer-Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/jenkins-console-output-script-error.jpg)

Return to Script Approval and approve the `java.lang.System getProperty` signature:

![The image shows a Jenkins interface on the "Script Approval" page, displaying no pending script approvals and a list of already approved signatures.](https://kodekloud.com/kk-media/image/upload/v1752870693/notes-assets/images/Certified-Jenkins-Engineer-Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/jenkins-script-approval-interface-2.jpg)

***

## Final Build: Success!

Run the pipeline one last time. All stages should complete without errors:

![The image shows a Jenkins console interface with a dropdown menu open, displaying options like "Configure" and "Delete Pipeline." The console output includes a script error message related to permission issues with Java methods.](https://kodekloud.com/kk-media/image/upload/v1752870695/notes-assets/images/Certified-Jenkins-Engineer-Demo-Groovy-Sandbox-and-In-process-Script-Approval-Part-3/jenkins-console-interface-dropdown-error.jpg)

```plaintext theme={null}
Running on Jenkins in /var/lib/jenkins/workspace/groovy-sandbox-test
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Topic)
[Pipeline] echo
Exploring Groovy Sandbox
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Get Hudson Instance)
[Pipeline] script
[Pipeline] {
[Pipeline] echo
Hudson Instance: hudson.model.Hudson@623e629d
[Pipeline] }
[Pipeline] // script
[Pipeline] stage
[Pipeline] { (Get System Property)
[Pipeline] script
[Pipeline] {
[Pipeline] echo
System Property: jenkins
[Pipeline] }
[Pipeline] // script
```

***

## References

* [script-security Plugin on GitHub](https://github.com/jenkinsci/script-security-plugin)
* [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
* [In-process Script Approval](https://www.jenkins.io/doc/book/managing/script-approval/)
* [Jenkins Official Site](https://www.jenkins.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/90da5b24-e8f2-455a-9756-9d69f4a7ce8e/lesson/3e29de2e-dcbf-4331-965b-1fc67fe1bbae)
