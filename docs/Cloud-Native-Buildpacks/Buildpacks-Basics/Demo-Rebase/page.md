# Expected output:
# 0.35.1
```

This output confirms that the Pack CLI has been successfully installed on your system. For further details and troubleshooting, refer to the official [Pack CLI Documentation](https://github.com/buildpacks/pack).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/d2170747-7a07-4648-b449-958edfff954b/lesson/e3e70583-011f-4fbb-93f7-fdc008cd73fc" />
</CardGroup>


# Demo Rebase

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Buildpacks-Basics/Demo-Rebase/page

This article demonstrates how to use rebasing to update the operating system base layer without rebuilding subsequent layers in Docker images.

In this lesson, we demonstrate how to use rebasing to update the operating system base layer without rebuilding the subsequent layers, including the application layer. This approach is especially useful when addressing security vulnerabilities, installing new libraries, or upgrading the underlying distribution—all without the overhead of a full rebuild.

## Step 1: Verify Your Application Image

Before rebasing, ensure that your application image is built and available in Docker. Run the following command to list your Docker images:

```bash theme={null}
docker image ls
```

To inspect the image details, including the buildpacks used and the runtime image, execute:

```bash theme={null}
pack inspect myapp
```

The output will include detailed information similar to:

```terminal theme={null}
Inspecting image: myapp

REMOTE:
  (not present)

LOCAL:
  Stack:
    Base Image:
      Reference: 36862ffaa256b69f1c92251e433dbe12c522f8d6d1476e792599f20c9fcb532c
      Top Layer: sha256:130264b1764b99aa2091ee0664a5e8dbf6ead305d43cd67407331191739e0d48

  Run Images:
    run-base:v1

  Rebasable: true

  Buildpacks:
    ID              VERSION   HOMEPAGE
    my-js-buildpack 0.0.1     -

  Processes:
    TYPE         SHELL   COMMAND   ARGS      WORK DIR
    web (default) node    index.js  /workspace
```

The output confirms that the current base (runtime) image is `run-base:v1`.

<Callout icon="lightbulb">
  The `pack inspect` command provides critical insight into your image’s structure. Verifying that your image is rebasable is an important prerequisite before proceeding.
</Callout>

## Step 2: Create a New Base Image

Suppose you need to update the base image—for instance, to switch from Ubuntu Jammy to Ubuntu Focal and install additional packages. First, modify your Dockerfile for the runtime image.

### Original Dockerfile (Ubuntu Jammy)

```dockerfile theme={null}
