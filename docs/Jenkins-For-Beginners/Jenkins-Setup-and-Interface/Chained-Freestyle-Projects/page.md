# Chained Freestyle Projects

Source: https://notes.kodekloud.com/docs/Jenkins-For-Beginners/Jenkins-Setup-and-Interface/Chained-Freestyle-Projects/page

This article demonstrates how to break a multi-stage process into separate jobs by chaining Freestyle Projects in Jenkins.

This article demonstrates how to break a multi-stage process into separate jobs by chaining Freestyle Projects in Jenkins. Previously, we executed a job that generated ASCII artwork by performing build, test, and deploy stages. Now, we will separate these stages into individual projects and chain them so that the test job runs after the build job, and the deploy job runs only after both the build and test jobs complete.

Below is an example of the complete process originally executed in one job:

```bash theme={null}
