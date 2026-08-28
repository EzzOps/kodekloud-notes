# Retrieve the user’s desired Node.js version from the build plan
node_js_version=$(cat "$CNB_BP_PLAN_PATH" | .metadata.version | jq -r '.entries[] | select(.name == "node-js")')
echo "nodejs version: ${node_js_version}"

# Get the currently cached Node.js version
cached_nodejs_version=$(cat "${CNB_LAYERS_DIR}/node-js.toml" 2>/dev/null | yj -t | jq -r '.metadata.nodejs_version' 2>/dev/null || echo "NOT FOUND")
echo "cached version: ${cached_nodejs_version}"

# If the desired Node.js version differs from the cached version or the cache is missing,
# download and extract Node.js; otherwise, reuse the cached version.
if [[ "${node_js_version}" != *"${cached_nodejs_version}"* ]] || [[ ! -d "${node_js_layer}" ]]; then
    echo "---> Downloading and extracting NodeJS"
    wget -q -O "${node_js_url}" | tar -xJf - --strip-components 1 -C "${node_js_layer}"
else
    echo "---> Reusing NodeJS"
fi

# Make Node.js available during launch and mark the layer as cacheable.
cat > "${CNB_LAYERS_DIR}/node-js.toml" << EOL
[types]
build = false
launch = true
cache = true
[metadata]
nodejs_version = "${node_js_version}"
EOL
```

<Callout icon="lightbulb">
  This script first reads the user-specified Node.js version and then checks the cache for an existing version. If the versions mismatch or if the cache is absent, it downloads and extracts Node.js accordingly.
</Callout>

***

## Caching the node\_modules Layer

Caching application dependencies is handled by comparing the hash of the `package-lock.json` file. Since this file specifies exact versions of dependencies, any change in its content indicates that the dependencies have been updated. The following script manages the caching logic for the node\_modules layer:

```bash theme={null}
# Get the hash of the current package-lock.json file
pkg_lock_hash=$(sha256sum "package-lock.json" | cut -d ' ' -f 1)
prev_hash=""

# Retrieve the cached package-lock hash if available
if [ -f "${node_modules_layer}.toml" ]; then
    prev_hash=$(cat "${node_modules_layer}.toml" | grep "package_lock_hash" || true)
fi

# Install dependencies if the cache is invalid:
# either the node_modules directory does not exist or the hashes differ.
if [ ! -d "${node_modules_layer}/node_modules" ] || [[ "${prev_hash}" != *"${pkg_lock_hash}"* ]]; then
    echo "---> Installing node modules"
    # Copy package.json and package-lock.json to the layer
    cp package*.json "${node_modules_layer}/"
    # Install dependencies in the layer
    cd "${node_modules_layer}"
    npm ci
    cd "$workdir"
else
    echo "---> Reusing node modules from cache"
fi

# Create a symbolic link to make the node_modules layer available in the working directory
ln -s "${node_modules_layer}/node_modules" "/workspace/node_modules"

# Mark the modules layer as available during build and launch, and enable caching
cat > "${node_modules_layer}.toml" << EOL
[types]
build = true
launch = true
cache = true
[metadata]
package_lock_hash = "${pkg_lock_hash}"
EOL
```

This caching process works as follows:

1. A SHA-256 hash is generated for the current `package-lock.json`.
2. The script checks if there is a previously cached hash.
3. If the node\_modules directory is missing or the hashes do not match (indicating updated dependencies), the script copies the `package.json` and `package-lock.json` to the layer, runs `npm ci` to install dependencies, and updates the cache.
4. A symbolic link is created, making the node\_modules layer accessible from the working directory.
5. Finally, metadata is saved to ensure the layer remains cacheable for future builds.

<Callout icon="lightbulb">
  Using caching not only speeds up the build process but also ensures that builds are consistent by reusing the exact versions of dependencies from previous builds.
</Callout>

***

Implementing caching logic with both the Node.js runtime and the node\_modules layers optimizes the build process. By reusing these layers, subsequent builds can avoid unnecessary downloads, leading to improved efficiency and faster deployment times.

For more details on related topics, refer to the following resources:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/0e306774-3067-4e23-9115-f3185d2ffa28/lesson/0b8f3100-2342-40d7-bdc6-bcb066bd47a1" />
</CardGroup>


# Creating a Buildpack

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Creating-Buildpacks/Creating-a-Buildpack/page

This guide teaches how to create a custom buildpack for JavaScript or Node.js applications, covering application structure and essential buildpack files.

In this lesson, you will learn how to create a custom buildpack tailored for JavaScript or Node.js applications. This buildpack activates only when it detects that the application is built with JavaScript or Node.js. Before diving into the buildpack creation process, let’s review the structure of a typical JavaScript application to ensure you have the necessary context.

## Overview of a JavaScript Application

A standard JavaScript application consists of several key components:

1. **Entry Point (index.js):**\
   This file contains the main source code of your application. In our example, all the logic is contained in a single file, although larger projects may distribute the code across multiple files. The entry point is conventionally named `index.js` or `app.js`. To run the application, execute the following command:

   ```bash theme={null}
   node index.js
   ```

   Below is a simple example using the Express framework:

   ```javascript theme={null}
   const express = require('express');
   const app = express();
   const PORT = process.env.PORT || 8080;

   // Define a route for the root URL
   app.get('/', (req, res) => {
     res.send('Hello, World!');
   });

   // Start the server
   app.listen(PORT, () => {
     console.log(`Server is running on http://localhost:${PORT}`);
   });
   ```

2. **Package Configuration (package.json):**\
   The `package.json` file contains essential metadata about your project, including its dependencies. For instance, when using Express and UUID, your configuration might look like this:

   ```json theme={null}
   {
     "name": "example-application",
     "version": "1.0.0",
     "main": "index.js",
     "scripts": {
       "test": "echo \"Error: no test specified\" && exit 1"
     },
     "author": "",
     "license": "ISC",
     "description": "",
     "engines": {
       "node": "23.1.0"
     },
     "dependencies": {
       "express": "^4.21.1",
       "uuid": "^11.0.2"
     }
   }
   ```

   This file not only lists the dependencies but also specifies the required Node.js version for your application.

3. **Lock File (package-lock.json):**\
   The `package-lock.json` locks dependencies to specific versions, ensuring consistency across development, CI/CD pipelines, and production environments. The buildpack later uses this file to detect any changes in dependency versions between builds.

4. **Dependencies Folder (node\_modules):**\
   After installing dependencies (for example, using npm), the `node_modules` folder contains the installed packages. A typical JavaScript project usually includes the entry point (`index.js` or `app.js`), the package configuration (`package.json`), and the `node_modules` directory.

<Frame>
  ![The image illustrates the basics of a JavaScript application, showing a project directory structure with files like index.js, package.json, and a node\_modules folder containing various modules.](https://kodekloud.com/kk-media/image/upload/v1752871983/notes-assets/images/Cloud-Native-Buildpacks-Creating-a-Buildpack/javascript-application-directory-structure.jpg)
</Frame>

## Buildpack Files Overview

A buildpack requires only a few fundamental files. In our example, these include:

1. **buildpack.toml:**\
   This configuration file defines metadata for your buildpack, such as the API version, buildpack ID, version, and target platform.

   ```toml theme={null}
   api = "0.10"

   [buildpack]
     id = "my-js-buildpack"
     version = "0.0.1"

   [[targets]]
     os = "linux"
     arch = "amd64"
   ```

2. **Detect Script (bin/detect):**\
   This executable script determines whether the buildpack should run. For a JavaScript buildpack, it checks for the presence of a `package.json` file. If the file is missing, the script exits with a status code of 100; otherwise, it allows the build process to continue.

   ```bash theme={null}
   #!/usr/bin/env bash
   set -eo pipefail
   if [[ ! -f package.json ]]; then
     exit 100
   fi
   ```

<Callout icon="lightbulb">
  The detect script ensures that your buildpack is executed only for JavaScript applications by checking for the existence of a `package.json` file.
</Callout>

3. **Build Script (bin/build):**\
   This executable script transforms your application source code into a Docker (or OCI-compliant) image. Its tasks include setting environment variables, installing dependencies, compiling source code (if necessary), and configuring the application's entry point.

   The Pack CLI offers a shortcut to generate this boilerplate. The following command creates a directory (in this example, `js-buildpack`) containing the `buildpack.toml` file and a `bin` folder with the detect and build scripts:

   ```bash theme={null}
   pack buildpack new my-js-buildpack --api 0.10 --path js-buildpack --version 0.0.1
   ```

   The generated `buildpack.toml` will resemble:

   ```toml theme={null}
   api = "0.10"

   [buildpack]
     id = "my-js-buildpack"
     version = "0.0.1"

   [[targets]]
     os = "linux"
     arch = "amd64"
   ```

## Detailed Look at the Detect Script

The detect script, located within the `bin` folder, is responsible for ensuring that the buildpack is applied only to JavaScript applications. It does so by verifying the presence of the `package.json` file:

```bash theme={null}
#!/usr/bin/env bash
set -eo pipefail
if [[ ! -f package.json ]]; then
  exit 100
fi
```

If `package.json` is found, the script exits with a zero status code, allowing the build process to proceed to the build script.

## Detailed Look at the Build Script

The build script is pivotal in transforming your application's source code into a containerized image. It performs several key operations:

1. **Installing Node.js:**\
   The script downloads and extracts Node.js from its official distribution URL.

2. **Installing Application Dependencies:**\
   It then uses either `npm ci` or `npm install` to install all dependencies specified in both `package.json` and `package-lock.json`.

3. **Configuring the Application Entry Point:**\
   The script creates a `launch.toml` file in the directory defined by the `CNB_LAYERS_DIR` environment variable. This file specifies the command that will run when the container is started.

Below is the complete build script:

```bash theme={null}
#!/usr/bin/env bash
set -eo pipefail

echo "---> Building image using my-js-buildpack buildpack"
node_js_url=https://nodejs.org/dist/v18.18.1/node-v18.18.1-linux-x64.tar.xz
wget -q -O - "$node_js_url" | tar -xJf - --strip-components 1

export PATH="./bin:$PATH"

echo "---> Installing Application Dependencies"
npm ci

cat > "${CNB_LAYERS_DIR}/launch.toml" << EOL
[[processes]]
type = "web"
command = ["bin/node", "index.js"]
default = true
EOL
```

This build script executes several critical tasks: it downloads and extracts Node.js, updates the environment PATH, installs the application dependencies using npm, and generates a launch configuration (`launch.toml`) that sets the default process for running your application.

<Frame>
  ![The image illustrates a build process using a buildpack, showing the transformation from source code to a Docker image, with steps to install Node.js, application dependencies, and configure the application entry point.](https://kodekloud.com/kk-media/image/upload/v1752871984/notes-assets/images/Cloud-Native-Buildpacks-Creating-a-Buildpack/buildpack-docker-image-process.jpg)
</Frame>

## Building the Application Image

With the detect and build scripts in place, you can now create your application image using the following command:

```bash theme={null}
pack build myapp --path ./nodejs/ --buildpack ./js-buildpack/ --builder cnbs/sample-builder:jamm
```

In this command:

* `myapp` represents the name of the generated image.
* `--path ./nodejs/` specifies the directory containing your application’s source code.
* `--buildpack ./js-buildpack/` points to the folder containing your custom buildpack.
* `--builder cnbs/sample-builder:jamm` indicates which builder to use (note that the builder will override its default buildpacks with the buildpack you specified).

After executing this command, the buildpack will detect your JavaScript application, download and install Node.js along with the required dependencies, and configure the startup process as defined in the `launch.toml` file.

<Callout icon="lightbulb">
  This guide walks you through creating a custom JavaScript/Node.js buildpack, from understanding a typical application structure to crafting both the detect and build scripts, culminating in successfully building a containerized image.
</Callout>

Enjoy building your applications with your custom buildpack!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/0e306774-3067-4e23-9115-f3185d2ffa28/lesson/5a80f5e8-1bef-4853-9c36-8b3ad7baebc6" />
</CardGroup>
