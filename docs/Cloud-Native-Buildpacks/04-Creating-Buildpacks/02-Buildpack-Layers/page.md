# Set a default version in case none is specified
default_version="18.18.1"

# Determine the Node.js version from package.json; if not available, use the default version
version=$(jq -r '.engines.node // empty' "./package.json")
version=${version:-$default_version}

# Write the build plan file using the CNB_BUILD_PLAN_PATH environment variable
cat > "${CNB_BUILD_PLAN_PATH}" << EOL
provides = [{ name = "node-js" }]
requires = [{ name = "node-js", metadata = { version = "$version" } }]
EOL
```

This script first verifies the existence of the package.json file. It then sets a default Node.js version (18.18.1) and uses the `jq` tool to extract the version from the "engines" section. If no version is found, the script falls back to the default version. Finally, it writes the build plan file with both "provides" and "requires" sections.

## Build Script

The build script leverages the information written by the detect script to download and install the correct version of Node.js. Here is the improved build script:

```bash theme={null}
#!/usr/bin/env bash
set -euo pipefail

echo "Building image using my-js-buildpack buildpack"

default_node_js_version="18.18.0"

# Retrieve the user's desired Node.js version from the build plan file.
# The build plan file is accessed via the CNB_BUILD_PLAN_PATH environment variable.
node_js_version=$(cat "$CNB_BUILD_PLAN_PATH" | yj -t | jq -r '.entries[] | select(.name == "node-js") | .metadata.version' || echo "${default_node_js_version}")
echo "Node.js version: ${node_js_version}"

node_js_url="https://nodejs.org/dist/v${node_js_version}/node-v${node_js_version}-linux-x64.tar.xz"
echo "---> Downloading and extracting NodeJS"
wget -q -O - "$node_js_url" | tar -xJf - --strip-components 1
```

In this script, a default Node.js version is defined, and then the build plan file (pointed to by CNB\_BUILD\_PLAN\_PATH) is read to extract the desired version using the tools `yj` (a YAML/JSON converter) and `jq`. Once the desired version is determined, the script dynamically constructs the URL for the corresponding Node.js archive, downloads, and extracts it.

<Callout icon="lightbulb">
  By using build plans to transfer version metadata from the detect script to the build script, the buildpack gains flexibility and scalability. This design enables multiple teams to seamlessly specify different Node.js versions without needing to modify hardcoded values in the build script.
</Callout>

This concludes our lesson on using buildpack build plans to dynamically configure runtime versions for Node.js applications.

***

For more details on buildpacks and deploying applications, check out:

* [Cloud Native Buildpacks](https://buildpacks.io/)
* [Node.js Official Downloads](https://nodejs.org/en/download/)
* [Using jq for JSON Processing](https://stedolan.github.io/jq/manual/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/0e306774-3067-4e23-9115-f3185d2ffa28/lesson/9f36cce8-caee-49cb-bcc6-ace554fa2331" />
</CardGroup>


# Buildpack Layers

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Creating-Buildpacks/Buildpack-Layers/page

This article explores how buildpack layers enhance build efficiency by optimizing Dockerfile commands and enabling faster, reusable build processes.

In this lesson, we explore how buildpack layers can create efficient, reusable build processes. By leveraging layers, you can optimize Dockerfile commands, speed up build times, and reduce redundant work.

## Understanding Layers in Dockerfiles

Each significant command in a Dockerfile produces a layer. Consider the following Dockerfile example:

```dockerfile theme={null}
