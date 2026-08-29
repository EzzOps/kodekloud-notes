# Define the base image
FROM ubuntu:jammy

# Install packages that we want to make available at run time
RUN apt-get update && \
    apt-get install -y xz-utils ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create user and group
ARG cnb_uid=1000
ARG cnb_gid=1000
RUN groupadd cnb --gid ${cnb_gid} && \
    useradd --uid ${cnb_uid} --gid ${cnb_gid} -m -s /bin/bash cnb
```

### Updated Dockerfile (Ubuntu Focal)

```dockerfile theme={null}
# Define the base image
FROM ubuntu:focal

# Install packages that we want to make available at run time
RUN apt-get update && \
    apt-get install -y xz-utils ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create user and group
ARG cnb_uid=1000
ARG cnb_gid=1000
RUN groupadd cnb --gid ${cnb_gid} && \
    useradd --uid ${cnb_uid} --gid ${cnb_gid} -m -s /bin/bash cnb
```

## Step 3: Build the New Base Image

Before building, verify that your containers are running correctly by checking them with:

```bash theme={null}
docker ps
```

Now, navigate to the appropriate directory (for example, the "builder" directory) and build the new base image:

```bash theme={null}
docker build -t run-base:v2 .
```

<Callout icon="lightbulb">
  Ensure you are in the correct directory containing the updated Dockerfile before running the build command.
</Callout>

## Step 4: Rebase the Application Image

After successfully building the new base image (`run-base:v2`), update the application image using rebasing with the following command:

```bash theme={null}
pack rebase myapp --run-image run-base:v2
```

This command replaces the original runtime image with `run-base:v2` without rebuilding the other layers of your image.

## Step 5: Verify the Updated Base Image

To confirm that rebasing was successful, inspect your application image again:

```bash theme={null}
pack inspect myapp
```

You should see output reflecting the updated base image, similar to:

```terminal theme={null}
Inspecting image: myapp

REMOTE:
  (not present)

LOCAL:
Stack:
  Base Image:
    Reference: d5f7d132c2f196de58bb1ca4fb041fa9a5829587f3cb9c01aed442f79d9b8e
    Top Layer: sha256:8460bddda3ad232a2e8af998246486378f5c3df30c499a08b58a89fb71

  Run Images:
    run-base:v21
Rebasable: true

Buildpacks:
  ID                      VERSION  HOMEPAGE
  my-js-buildpack         0.0.1    https://github.com/buildpacks/samples/tree/main/buildpacks/hello-world
  samples/hello-world     0.0.1    https://github.com/buildpacks/samples/tree/main/buildpacks/hello-world
  samples/hello-moon      0.0.1    https://github.com/buildpacks/samples/tree/main/buildpacks/hello-moon
```

This demonstrates that only the base image layer was replaced, while the application layer remains unchanged.

<Callout icon="lightbulb">
  Rebasing provides an efficient workflow for updating critical components like the operating system layer without incurring the overhead of a full image rebuild.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/d2170747-7a07-4648-b449-958edfff954b/lesson/317cbaf3-9d6e-4e9c-8bdd-329d9147533f" />
</CardGroup>


# Rebase

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Buildpacks-Basics/Rebase/page

This guide explores the rebase functionality of Buildpacks for efficiently updating application base images without rebuilding all layers.

In this guide, we'll explore the rebase functionality offered by Buildpacks. Rebasing enables you to update the base image of an already built application without the need to rebuild all subsequent layers, resulting in a more efficient and faster update process.

## How Rebasing Works

When using a traditional Dockerfile, the first layer of an image is typically the base image, followed by additional layers that include application dependencies and source code. Any change to the base image—such as an operating system update, applying a hotfix, addressing a security vulnerability, or adding new dependencies—requires rebuilding every layer above it. This process can be resource-intensive and inefficient.

Buildpacks streamline this process. When you rebase an image with an updated base image, only the base layer is replaced, while the higher-level layers remain unchanged. This targeted replacement minimizes rebuild time and data transfer during the image update process.

<Frame>
  ![The image compares the effects of rebasing with Dockerfiles and Buildpacks, showing that Dockerfiles cause all layers to change, while Buildpacks only change the specific layer, resulting in less data transfer and faster rebuilds.](../../../../images/kodekloud.com/kk-media/image/upload/v1752871961/notes-assets/images/Cloud-Native-Buildpacks-Rebase/rebasing-dockerfiles-buildpacks-comparison.jpg)
</Frame>

<Callout icon="lightbulb">
  Rebasing significantly improves your build performance by only updating the necessary layer. This makes it an ideal approach when you need to apply minor changes or security fixes.
</Callout>

## Inspecting the Image

Before proceeding with a rebase operation, you can inspect the current image details using the Pack CLI. Run the following command:

```bash theme={null}
pack inspect my-image
```

A sample output might appear as follows:

```plaintext theme={null}
Inspecting image: my-image

REMOTE:
  (not present)

LOCAL:
Stack:

Base Image:
  Reference: 36862ffaa256b69f1c92251e433dbe12c522f8d6d1476e792599f20c9fcb532c
  Top Layer: sha256:130264b17d64b99aa2091e0664a5e0dbf6ead305d43cd674073311917390ed48

Run Images:
  run-base:v1

Rebasable: true

Buildpacks:
  ID                     VERSION   HOMEPAGE
  my-js-buildpack       0.0.1     -
  samples/hello-world   0.0.1     https://github.com/buildpacks/samples/tree/main/buildpacks/hello-world
  samples/hello-moon    0.0.1     https://github.com/buildpacks/samples/tree/main/buildpacks/hello-moon

Processes:
  TYPE          SHELL      COMMAND        ARGS       WORK DIR
  web (default) node       index.js       /workspace
```

In this output, note the **Run Images** field, which displays the current base image (run-base:v1).

## Rebasing the Image

If you need to update the base image—whether to apply a hotfix, address security vulnerabilities, or add new dependencies—and have created an updated base image (for example, run-base:v2), you can perform a rebase with the following command:

```bash theme={null}
pack rebase my-image --run-image run-base:v2
```

This command substitutes the old base image (run-base:v1) with the new one (run-base:v2) without rebuilding the remaining layers.

<Callout icon="triangle-alert">
  Ensure that your updated base image has been thoroughly tested before performing the rebase in production. This helps avoid any unexpected issues.
</Callout>

## Verifying the Rebase

After executing the rebase command, verify that the image now uses the updated base by inspecting it again:

```bash theme={null}
pack inspect my-image
```

An updated output should indicate the change as shown below:

```plaintext theme={null}
Inspecting image: my-image

REMOTE:
  (not present)

LOCAL:
Stack:
  Base Image:
    Reference: 36862ffaa256b69f1c92251e433dbe12c522f8d6d1476e792599f20c9fcb532c
    Top Layer: sha256:130264b17d64b99aa2091ee0664a5e0dbf6ead305d43cd67407331191739e0d48

Run Images:
  run-base:v2

Rebasable: true

Buildpacks:
  ID                      VERSION  HOMEPAGE
  my-js-buildpack        0.0.1    -
  samples/hello-world    0.0.1    https://github.com/buildpacks/samples/tree/main/buildpacks/hello-world
  samples/hello-moon     0.0.1    https://github.com/buildpacks/samples/tree/main/buildpacks/hello-moon
```

This confirms that the new base image (run-base:v2) is now active, highlighting the efficiency and convenience of using Buildpacks for rebasing.

For more detailed information on Buildpacks and image creation, consider reviewing these resources:

* [Buildpacks Documentation](https://buildpacks.io/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/d2170747-7a07-4648-b449-958edfff954b/lesson/591825b0-5ed8-4a09-82f4-6da6c8b68c3e" />
</CardGroup>
