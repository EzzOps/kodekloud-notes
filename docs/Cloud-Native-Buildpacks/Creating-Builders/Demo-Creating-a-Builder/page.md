# Define the base image
FROM ubuntu:jammy

# Install packages available at build time
RUN apt-get update && \
    apt-get install -y xz-utils ca-certificates jq wget curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -Lo yj https://github.com/sclevine/yj/releases/download/v5.1.0/yj-linux-amd64 && \
    chmod +x yj && mv yj /usr/local/bin/

# Set required CNB user information
ARG cnb_uid=1000
ARG cnb_gid=1000
ENV CNB_USER_ID=${cnb_uid}
ENV CNB_GROUP_ID=${cnb_gid}

# Create user and group
RUN groupadd cnb --gid ${CNB_GROUP_ID} && \
    useradd --uid ${CNB_USER_ID} --gid ${CNB_GROUP_ID} -m -s /bin/bash cnb

# Use the specified user and group
USER ${CNB_USER_ID}:${CNB_GROUP_ID}

# Set metadata about the build image base
LABEL io.buildpacks.base.distro.name="ubuntu"
LABEL io.buildpacks.base.distro.version="22.04"
```

Once you have saved this Dockerfile (commonly as `build-base.Dockerfile`), build the image using:

```bash theme={null}
docker build -t build-base:v1 -f build-base.Dockerfile .
```

***

## 2. Creating the Runtime Image

The runtime image is the foundation for your final application container and only includes packages necessary for running your application. The Dockerfile below illustrates how to build a minimalist runtime environment based on Ubuntu Jammy:

```dockerfile theme={null}
# Define the base image
FROM ubuntu:jammy

# Install packages available at runtime
RUN apt-get update && \
    apt-get install -y xz-utils ca-certificates && \
    rm -rf /var/lib/apt/lists/*
  
# Create user and group for runtime
ARG cnb_uid=1000
ARG cnb_gid=1000
RUN groupadd cnb --gid ${cnb_gid} && \
    useradd --uid ${cnb_uid} --gid ${cnb_gid} -m -s /bin/bash cnb

# Use the specified user and group
USER ${cnb_uid}:${cnb_gid}

# Set metadata about the runtime image base
LABEL io.buildpacks.base.distro.name="ubuntu"
LABEL io.buildpacks.base.distro.version="22.04"
```

To build this runtime image (commonly stored in a file named `run-base.Dockerfile`), use:

```bash theme={null}
docker build -t run-base:v1 -f run-base.Dockerfile .
```

***

## 3. Configuring the Builder

The next step is to define the buildpacks and their order in a configuration file named `builder.toml`. This file specifies the base images (build and run images) as well as an ordered list of buildpacks that the builder will use.

Below is an example configuration:

```toml theme={null}
# Buildpacks to include in the builder
[[buildpacks]]
uri = "docker://sanjeevkt720/my-js-buildpack"

[[buildpacks]]
uri = "docker://cnbs/sample-package:hello-universe"

# Order used for detection
[[order]]
  [[order.group]]
    id = "my-js-buildpack"
  [[order.group]]
    id = "samples/hello-universe"

# Base images used to create the builder
[build]
image = "build-base:v1"

[run]
[[run.images]]
image = "run-base:v1"
arch = "amd64"
```

<Callout icon="lightbulb">
  Ensure that the IDs listed in the order section match those defined in each buildpack's own `buildpack.toml` file. You can inspect a buildpack’s metadata with the command `pack inspect-buildpack <buildpack-uri>`.
</Callout>

***

<Frame>
  ![The image is a diagram titled "Creating a Builder," showing components of a builder including "Node Buildpack," "Go Buildpack," "Build Image," and "Run Image."](https://kodekloud.com/kk-media/image/upload/v1752871975/notes-assets/images/Cloud-Native-Buildpacks-Creating-a-Builder/creating-a-builder-diagram.jpg)
</Frame>

***

## 4. Creating and Using Your Builder

With both the build and runtime images, along with the configuration file in place, you can create your custom builder. Run the following command to create the builder using your configured settings:

```bash theme={null}
pack builder create my-builder --config ./builder.toml
```

Once the builder is successfully created, build your application image. For instance, if your application source is located in the `nodejs-app/` directory, use:

```bash theme={null}
pack build my-image --path nodejs-app/ --builder my-builder
```

This command directs the pack CLI to generate your final application image using the custom builder, which includes your build and runtime images as well as the designated buildpacks.

***

By following these steps, you now have a complete setup for creating and using your own builder with Cloud Native Buildpacks, streamlining the process to build and run your cloud-native applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/94f2e47e-b25f-4e0c-8073-694c188e7cab/lesson/cf3b5aa0-c4af-49d5-81d3-33ebfa7e8b62" />
</CardGroup>


# Demo Creating a Builder

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Creating-Builders/Demo-Creating-a-Builder/page

This guide teaches how to create a custom builder by assembling files and configuring them step by step.

In this guide, you'll learn how to create your own builder by assembling the necessary files and configuring them step by step. We will begin by creating a folder named "builder" to hold all the essential files for your custom builder.

─────────────────────────────

## Creating the Base Image

The first step is to establish the base image used during the build stage. This image is crucial as it defines the environment for processing buildpacks and ultimately creating the final runtime image.

### Dockerfile: build-base.Dockerfile

Create a Dockerfile named **build-base.Dockerfile** with the following content. This file uses Ubuntu Jammy as the base image, installs required utilities (including xz-utils, ca-certificates, jq, wget, and curl), and adds the YJ tool. It also configures the CNB user and group information.

```dockerfile theme={null}
