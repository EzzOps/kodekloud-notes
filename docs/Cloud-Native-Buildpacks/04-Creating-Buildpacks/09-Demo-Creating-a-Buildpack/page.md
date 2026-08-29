# Define the Node.js layer directory within the CNB layers directory
node_js_layer="${CNB_LAYERS_DIR}/node-js"
mkdir -p "${node_js_layer}"

default_node_js_version="18.18.0"

# Retrieve the desired Node.js version from the build plan or use the default version.
node_js_version=$(cat "${CNB_BP_PLAN_PATH}" | yj -t | jq -r '.entries[] | select(.name == "node-js") | .metadata.version' || echo "${default_node_js_version}")
echo "Node.js version specified: ${node_js_version}"

# Establish the download URL based on the desired Node.js version.
node_js_url="https://nodejs.org/dist/v${node_js_version}/node-v${node_js_version}-linux-x64.tar.xz"

# Retrieve the cached Node.js version from the layer metadata (if it exists).
cached_nodejs_version=$(cat "${CNB_LAYERS_DIR}/node-js.toml" 2>/dev/null | yj -t | jq -r .metadata.nodejs_version 2>/dev/null || echo 'NOT FOUND')
echo "Cached Node.js version: ${cached_nodejs_version}"

# <Callout icon="lightbulb" color="#1CB2FE">
# If the desired version differs from the cached version or if the layer is missing, the script downloads and extracts Node.js.
#
</Callout>
if [[ "${node_js_version}" != "${cached_nodejs_version}" ]] || [[ ! -d "${node_js_layer}" ]]; then
    echo "-----> Downloading and extracting Node.js"
    wget -q -O - "${node_js_url}" | tar -xJf - --strip-components 1 -C "${node_js_layer}"
else
    echo "-----> Reusing Node.js from cache"
fi

# Write layer metadata to indicate that Node.js is available for launch and caching, recording the version.
cat > "${CNB_LAYERS_DIR}/node-js.toml" << EOL
[types]
build = false
launch = true
cache = true
[metadata]
nodejs_version = "${node_js_version}"
EOL

# Update the PATH to include the node-js layer binaries.
export PATH="${node_js_layer}/bin:$PATH"
pwd
```

### How the Node.js Layer Caching Works

1. **Directory Preparation and Version Detection:**\
   The script creates the runtime layer directory and determines the desired Node.js version from the build plan, defaulting to version 18.18.0 if not specified.

2. **URL Construction and Cache Verification:**\
   It sets up the download URL for the specified version and compares it with the cached version stored in the metadata file. If there is a mismatch or the layer is absent, Node.js is downloaded and extracted.

3. **Metadata Update:**\
   The script updates the layer metadata (`node-js.toml`), ensuring that the build engine knows that Node.js is available for both launch and caching, and finally updates the PATH.

***

## Caching the node\_modules Layer

Caching the node\_modules layer is accomplished using a hash of the `package-lock.json` file. This hash-based approach guarantees that if dependencies have not changed, your cached node\_modules directory can be efficiently reused.

Below is the enhanced script for the node\_modules layer caching:

```bash theme={null}
#!/bin/bash
set -euo pipefail

# Calculate the SHA-256 hash of package-lock.json to detect changes in dependencies.
pkg_lock_hash=$(sha256sum "package-lock.json" | cut -d ' ' -f 1)

workdir=$(pwd)
# Define the node_modules layer directory.
node_modules_layer="${CNB_LAYERS_DIR}/node-dependencies"
mkdir -p "${node_modules_layer}"

# Retrieve the previously cached package-lock.json hash (if available).
prev_hash=$(cat "${node_modules_layer}.toml" 2>/dev/null | yj -t | jq -r .metadata.package_lock_hash 2>/dev/null || echo "NOT_FOUND")
echo "Current package-lock hash: ${pkg_lock_hash}"
echo "Previously cached hash: ${prev_hash}"

# <Callout icon="lightbulb" color="#1CB2FE">
# If the node_modules folder is absent or if the hash has changed (implying that dependencies have been updated), reinstall the modules.
#
</Callout>
if [ ! -d "${node_modules_layer}/node_modules" ] || [[ "${prev_hash}" != "${pkg_lock_hash}" ]]; then
    echo "---> Installing node modules"
    cp package*.json "${node_modules_layer}"
    cd "${node_modules_layer}"
    npm ci
    cd "$workdir"
else
    echo "---> Reusing node modules from cache"
fi

# Create a symlink in the workspace so that node_modules is directly accessible.
ln -sf "${node_modules_layer}/node_modules" "/workspace/node_modules"

# Write the current package-lock hash into the layer metadata.
cat > "${node_modules_layer}.toml" << EOL
[types]
build = false
launch = true
cache = true
[metadata]
package_lock_hash = "${pkg_lock_hash}"
EOL

# Write the launch configuration.
cat > "${CNB_LAYERS_DIR}/launch.toml" << EOL
[processes]
type = "web"
command = ["node", "index.js"]
default = true
EOL

echo "CNB_LAYERS_DIR: ${CNB_LAYERS_DIR}"
```

### How the node\_modules Layer Caching Works

1. **Dependency Change Detection:**\
   The script computes a SHA-256 hash for the `package-lock.json` file and compares it to the previous hash. This hash determines if dependencies have changed.

2. **Conditional Installation:**\
   If the `node_modules` folder does not exist or if the dependency hash differs, the necessary package configuration files are copied, and `npm ci` is executed to install the dependencies. Otherwise, the cache is reused.

3. **Workspace Integration and Metadata Update:**\
   A symlink is created to make the cached node\_modules folder accessible from the workspace. Finally, updated metadata (including the package-lock hash) is written to ensure proper caching and launch behavior.

***

## Testing the Caching Logic

After implementing the caching logic, you can build and run your application using the buildpack. Follow these steps:

1. **Build and Run the Application:**

   ```bash theme={null}
   docker run -d -p 8000:8080 myapp
   curl localhost:8000
   # Expected output:
   # Hello, World!
   ```

2. **Trigger a Build with Pack:**

   Remove any existing container and build your application with the sample builder and buildpack:

   ```bash theme={null}
   docker rm -f <container_id>
   pack build myapp --path nodejs-app/ --builder cnbs/sample-builder:jammy --buildpack js-buildpack/
   ```

   During the build process, you might see logs such as:

   * If the cached Node.js version matches the desired version:
     ```Node.js theme={null}
     [builder] Node.js version specified: 18.18.0
     [builder] Cached Node.js version: 18.18.0
     [builder] -----> Reusing Node.js from cache
     [builder] -----> Reusing node modules from cache
     ```
   * If the desired Node.js version changes (e.g., from 18.18.0 to 18.18.1):
     ```bash theme={null}
     [builder] Node.js version specified: 18.18.1
     [builder] Cached Node.js version: 18.18.0
     [builder] -----> Downloading and extracting Node.js
     [builder] -----> Reusing node modules from cache
     ```

3. **Handling Dependency Changes:**

   When modifications are made to the dependencies (reflected by changes in `package-lock.json`), the build logs will indicate:

   ```bash theme={null}
   [builder] -----> Installing node modules
   ```

   This confirms that the cache is being invalidated and refreshed as needed.

***

By comparing the desired state with the cached state—using both the Node.js version and the dependency hash—this caching mechanism optimizes build times and maintains consistency across builds.

For further reading, check out these resources:

* [Node.js Official Downloads](https://nodejs.org/en/download/)
* [npm Documentation](https://docs.npmjs.com/)
* [Cloud Native Buildpacks](https://buildpacks.io/)

<Callout icon="lightbulb">
  If you encounter any cache-related issues during your build process, double-check the metadata stored in the TOML files to confirm that the intended versions and hashes are correctly recorded.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/0e306774-3067-4e23-9115-f3185d2ffa28/lesson/9556709f-b988-4eaa-aded-13397536c16d" />
</CardGroup>


# Demo Creating a Buildpack

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Creating-Buildpacks/Demo-Creating-a-Buildpack/page

This guide teaches how to create a custom Node.js buildpack using the Pack CLI, covering boilerplate generation, detection logic, and build process enhancements.

In this guide, you will learn how to create a custom Node.js buildpack using the Pack CLI. We'll generate the starter boilerplate, update the detection logic to target Node.js projects, and enhance the build process to install Node.js and application dependencies. This article covers each step in detail to help you convert your source code into a container image with best practices.

## Creating the Buildpack

To get started, use the Pack CLI to create a new buildpack. In this example, the buildpack is named "my-js-buildpack", uses API version 0.10, and is stored in a folder called `js-buildpack` with an initial version of 0.0.1:

```bash theme={null}
pack buildpack new my-js-buildpack --api 0.10 --path js-buildpack --version 0.0.1
```

After running this command, you should see output similar to:

```plaintext theme={null}
create  buildpack.toml
create  bin/build
create  bin/detect
Successfully created my-js-buildpack
```

If you inspect the `js-buildpack` folder, you'll notice a `buildpack.toml` file containing metadata similar to:

```toml theme={null}
api = "0.10"

[buildpack]
  id = "my-js-buildpack"
  version = "0.0.1"

[[targets]]
  os = "linux"
  arch = "amd64"
```

The `bin` directory hosts two scripts: `detect` and `build`. The `detect` script determines if the buildpack applies to the application, while the `build` script handles the build logic.

## Understanding the Detect Script

The default `detect` script is as follows:

```bash theme={null}
#!/usr/bin/env bash

set -euo pipefail

layers_dir="$1"
env_dir="$2/env"
plan_path="$3"

exit 0
```

If the `detect` script exits with a status code of 0, the build process continues to the build stage. To control whether your buildpack should be activated, you can conditionally exit with a nonzero status code. For example, to explicitly fail detection, you might modify the script to:

```bash theme={null}
#!/usr/bin/env bash
set -eo pipefail

echo "detecting if my-js-buildpack should run"
exit 1
```

Exiting with status code 1 signals the builder that this buildpack should not be used. Since our buildpack is intended for Node.js applications, updating the detection logic to check for a `package.json` file makes it more robust:

```bash theme={null}
#!/usr/bin/env bash
set -eo pipefail

echo "detecting if my-js-buildpack should run"
if [[ ! -f package.json ]]; then
  exit 100
fi

exit 0
```

This change ensures that if the `package.json` file is absent, the buildpack exits with code 100, indicating that it does not apply.

## The Default Build Script

The default `build` script is minimal and only exits successfully:

```bash theme={null}
#!/usr/bin/env bash

set -eu pipefail

layers_dir="$1"
env_dir="$2/env"
plan_path="$3"

exit 0
```

For a Node.js application, the build process should perform the following tasks:

1. Download and install Node.js.
2. Install application dependencies using an `npm` command.
3. Create a `launch.toml` file (in the CNB layers directory) specifying the start command for the application.

### Updating the Build Script for Node.js

Enhance your `bin/build` script to download and install Node.js version 18.18.1, update the PATH during the build, install dependencies, and create a `launch.toml` file. Below is the updated script:

```bash theme={null}
#!/usr/bin/env bash
set -euo pipefail

echo "Building image using my-js-buildpack buildpack"

echo "---> Downloading and extracting NodeJS"
node_js_url="https://nodejs.org/dist/v18.18.1/node-v18.18.1-linux-x64.tar.xz"
wget -q -O - "${node_js_url}" | tar -xJf - --strip-components 1
