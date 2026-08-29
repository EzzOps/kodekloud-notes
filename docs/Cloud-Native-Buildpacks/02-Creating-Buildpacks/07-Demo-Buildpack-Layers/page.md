# Demo Buildpack Layers

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Creating-Buildpacks/Demo-Buildpack-Layers/page

This guide demonstrates separating the Node.js runtime and Node modules into dedicated layers to improve build performance and caching.

In this guide, we demonstrate how to separate the Node.js runtime and Node modules installation into dedicated layers. Separating these components not only clarifies the build process but also leverages caching and boosts launch performance.

Below is a comprehensive step-by-step walkthrough with clearly structured code blocks.

***

## Creating the Node.js Runtime Layer

In this section, we create a dedicated layer for the Node.js runtime. Here, we download and extract Node.js into a specified directory. The runtime layer’s metadata is configured in a TOML file to ensure it is available at launch.

```bash theme={null}
#!/usr/bin/env bash
set -euo pipefail

echo "Building image using my-js-buildpack buildpack"
