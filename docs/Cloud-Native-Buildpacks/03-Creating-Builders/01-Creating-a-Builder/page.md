# Creating a Builder

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Creating-Builders/Creating-a-Builder/page

Learn to create a custom builder using Cloud Native Buildpacks, including build and runtime images, and configuration for buildpacks.

In this guide, you'll learn how to create your own builder using Cloud Native Buildpacks. A builder is composed of three essential components:

* A build image for compiling your application.
* A runtime image for executing your application.
* An ordered list of buildpacks that perform detection and build processes.

***

## 1. Creating the Build Image

The build image provides the environment where all your buildpacks operate. It includes all the tools and packages necessary during the build process. The following Dockerfile example uses Ubuntu Jammy as the base image, installs essential utilities (such as xz-utils, ca-certificates, jq, wget, and curl), and sets up the required user and group for Cloud Native Buildpacks (CNB).

```dockerfile theme={null}
