# Why Buildpacks

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Buildpacks-Basics/Why-Buildpacks/page

This article explores the advantages of CloudNative Buildpacks over traditional Dockerfiles in simplifying container image creation and addressing related challenges.

In this lesson, we explore why buildpacks exist, the challenges they address with traditional Dockerfiles, and how they simplify the process of creating container images. We begin by examining how a typical application is containerized using a Dockerfile.

***

## Containerizing an Application with Dockerfiles

When containerizing an application, developers typically write a Dockerfile—a sequence of instructions that details how to build the application's container image. Take, for example, a Node.js application. The following Dockerfile uses a trusted base image, creates a non-root user, sets up the working directory, installs production dependencies, copies the application source code, and finally exposes a port with the command to run the application.

<Frame>
  ![The image illustrates the process of containerizing an application, showing a developer creating a Dockerfile.](https://kodekloud.com/kk-media/image/upload/v1752871962/notes-assets/images/Cloud-Native-Buildpacks-Why-Buildpacks/containerizing-application-dockerfile.jpg)
</Frame>

```dockerfile theme={null}
