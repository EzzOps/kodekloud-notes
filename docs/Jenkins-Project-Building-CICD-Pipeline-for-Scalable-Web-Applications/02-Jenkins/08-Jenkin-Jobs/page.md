# Add changes to staging
git add

# Commit the changes with a descriptive message
git commit -m "made changes to index.html"

# Push changes to the main branch
git push origin main
```

Once the changes are pushed, Jenkins will automatically trigger a new build for the "Flask pipeline" job.

### Sample Console Output for the Auto-Triggered Build

```bash theme={null}
Started by GitHub push by sanjeevkt720
Running as SYSTEM
Building in workspace /var/lib/jenkins/workspace/Flask-pipeline
The recommended git tool is: NONE
No credentials specified
> /usr/bin/git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/Flask-pipeline/.git # timeout=10
Fetching changes from the remote Git repository
> /usr/bin/git config remote.origin.url https://github.com/kodeloudhub/jenkins-project # timeout=10
Fetching upstream changes from https://github.com/kodeloudhub/jenkins-project
> /usr/bin/git --version # timeout=10
> git --version # git version 2.40.1
> /usr/bin/git fetch --tags --force --progress https://github.com/kodeloudhub/jenkins-project +refs/heads/*:refs/remotes/origin/* # timeout=10
Checking out Revision 335e2031e167245b217bec9a5402a1c94ec5 (refs/remotes/origin/main)
> /usr/bin/git config core.sparsecheckout # timeout=10
> /usr/bin/git checkout -f 335e2031e167245b217bec9a5402a1c94ec5 # timeout=10
Commit message: "made changes to index.html"
> /usr/bin/git rev-list --no-walk bfc8489d5b1161bb14f565b0bea9e7d9 # timeout=10
[Flask-pipeline] $ /bin/sh -xe /tmp/jenkins34718612456724851020.sh
+ echo 'Hello from Jenkins'
Hello from Jenkins
Finished: SUCCESS
```

> **lightbulb** After each build (manual or auto-triggered), review the console output in Jenkins. This ensures that the repository is cloned correctly and the build steps, including the execution of the shell command, are completed successfully.

Now, every time changes are pushed to the `main` branch of your repository, Jenkins will automatically trigger a build using the GitHub webhook integration. For more information on Git and Jenkins integration, check out the [Jenkins Documentation](https://www.jenkins.io/doc/) and [GitHub Docs](https://docs.github.com/).

- [Watch Video](https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/4b025d4d-3ef9-479d-a483-3aa7a206a553/lesson/efdff7d4-fc12-414e-9a26-e287acdf5f2f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/4b025d4d-3ef9-479d-a483-3aa7a206a553/lesson/e502a22e-3b94-4ba5-af3d-9de2b764ec42)


# Jenkin Jobs

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Jenkins/Jenkin-Jobs/page

This article explores Jenkins jobs and their role in automating development and deployment tasks within CI/CD processes.

In this article, we dive into Jenkins jobs and explore their crucial role in automating various development and deployment tasks.

A Jenkins job is a predefined set of instructions that directs Jenkins on which actions to perform. While Jenkins itself is an automation engine, you must define the specific commands and steps it should execute. For example, to run pytest tests in a Python application, you need to create a Jenkins job that includes all the necessary commands for the task.

## Common Steps in a Jenkins Job

A typical Jenkins job can include a variety of stages such as:

* Compiling code
* Running automated tests
* Deploying to a staging environment (and eventually to production)
* Triggering third-party APIs
* Running linting, formatting, or other code quality checks

Each stage in the Jenkins job provides real-time feedback. After a successful code compilation, Jenkins logs the success of the compilation stage. If errors occur during the testing phase, Jenkins details the specific test failures, making it easier for developers to identify and address the issues.

![The image illustrates a Jenkins job workflow, showing stages like "Compile," "Test," "Deploy to Staging," and "Deploy to Production," with logs and developer interaction.](https://kodekloud.com/kk-media/image/upload/v1752879902/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Jenkin-Jobs/jenkins-job-workflow-stages-logs.jpg)

> **lightbulb** Jenkins jobs are central to continuous integration and continuous deployment (CI/CD) processes, ensuring that your code is built, tested, and deployed systematically.

## Types of Jenkins Jobs

Jenkins supports several types of jobs (often referred to as projects) to fit different automation needs:

* **Freestyle Project:**\
  The most basic job type where you can directly configure instructions through the Jenkins GUI.

* **Pipeline:**\
  A modern, code-centric configuration that allows you to define your job in a Jenkinsfile alongside your application code. This approach enables version control of your build configurations and ensures consistency.

* **Multi-Configuration Project:**\
  Ideal for running similar jobs with variable parameters. Use this when you need to test across multiple environments with slight configuration variations.

* **Folders:**\
  Organize multiple jobs into a hierarchical structure, keeping your Jenkins environment well-organized and manageable.

* **Multi-Branch Pipeline:**\
  Create different pipelines for various branches of your repository. This allows for branch-specific build and deployment processes, ensuring that each branch can have its tailored CI/CD pipeline.

## Summary

Jenkins jobs offer a flexible and robust framework for automating a wide range of tasks—from compiling code and running tests to deploying applications and integrating with external systems. By selecting the appropriate job type and configuration, you can optimize your continuous integration and deployment workflows, ultimately streamlining your development process.

For more detailed information on Jenkins and CI/CD practices, check out the [Jenkins Documentation](https://jenkins.io/doc/).

- [Watch Video](https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/4b025d4d-3ef9-479d-a483-3aa7a206a553/lesson/269028a5-63d3-44da-96dd-51fbfaa954ea)
