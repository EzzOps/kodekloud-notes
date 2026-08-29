# Update PATH during build-time so that npm and node are locatable.
export PATH="./bin:$PATH"

pwd
ls -la

echo "---> Installing Application Dependencies"
npm ci

echo "CNB_LAYERS_DIR: ${CNB_LAYERS_DIR}"

# Write the launch.toml to define the startup process for the container.
cat > "${CNB_LAYERS_DIR}/launch.toml" << EOL
[[processes]]
type = "web"
command = ["bin/node", "index.js"]
default = true
EOL
```

<Callout icon="lightbulb">
  When running build commands, environment variable changes (like modifications to PATH) only persist during the build process. At runtime, these changes do not apply. Hence, we reference the full path (`bin/node`) in the launch command.
</Callout>

With these modifications, the build script will:

* Download and extract Node.js into the current working directory.
* Update the PATH so that Node.js and npm are accessible during the build.
* Install application dependencies using `npm ci`.
* Generate a `launch.toml` file that defines a web process with the command `bin/node index.js`.

## Building the Image with the Custom Buildpack

With the updated detect and build scripts, you can now build the container image using your custom buildpack. For example, run:

```bash theme={null}
pack build myapp --path nodejs-app/ --builder cnbs/sample-builder:jammy --buildpack js-buildpack/
```

During the build process, you should see output similar to:

```plaintext theme={null}
==> ANALYZING
[analyzer] Image with name "myapp" not found
==> DETECTING
[detector] my-js-buildpack 0.0.1
[detector] detecting if my-js-buildpack should run
==> BUILDING
[builder] Building image using my-js-buildpack buildpack
[builder] ---> Downloading and extracting NodeJS
[builder] (Directory listing of /workspace ...)
[builder] ---> Installing Application Dependencies
...
[exporter] Setting default process type 'web'
[exporter] Saving myapp...
Successfully built image myapp
```

At this point, your image is successfully created. The generated `launch.toml` file instructs the lifecycle to execute `bin/node index.js` when the container starts.

## Running and Debugging the Container

To run your new image, you can use the following Docker command:

```bash theme={null}
docker run -d -p 8000:8080 myapp
```

If you encounter issues such as the container stopping unexpectedly, list all containers with:

```bash theme={null}
docker ps -a
```

You might see an error in the logs similar to:

```plaintext theme={null}
ERROR: failed to launch: path lookup: exec: "node": executable file not found in $PATH
```

This error indicates that the runtime environment cannot locate Node.js because PATH changes during the build process are not propagated. The solution is to reference the full executable path (i.e., using `"bin/node"` in the launch command).

Once the container is running with the correct launch command, test the application with:

```bash theme={null}
curl localhost:8000
```

If configured correctly, you should receive:

```plaintext theme={null}
Hello, World!
```

## Process Overview

Below is a summary table of actions performed by the buildpack:

| Step                           | Action                                            | Command/Result                                               |
| ------------------------------ | ------------------------------------------------- | ------------------------------------------------------------ |
| Generate Buildpack Boilerplate | Create a new buildpack with Pack CLI              | `pack buildpack new my-js-buildpack --...`                   |
| Enhance Detect Script          | Check for `package.json` to continue detection    | Exit with code 100 if missing                                |
| Update Build Script            | Download Node.js, install dependencies, and setup | Create `launch.toml` with `bin/node index.js`                |
| Build Image                    | Build an image using the custom buildpack         | `pack build myapp --...`                                     |
| Run Container                  | Start the container and test application          | `docker run -d -p 8000:8080 myapp` and `curl localhost:8000` |

## Conclusion

In this article, you learned how to create a custom Node.js buildpack that transforms source code into a runnable container image. We started by generating the buildpack boilerplate, modified the detect script to verify the presence of `package.json`, and enhanced the build script to:

• Download and extract Node.js\
• Install application dependencies via `npm ci`\
• Generate a `launch.toml` that specifies the startup process

While this example buildpack provides a basic setup, it can be extended and optimized further to adhere to advanced best practices. Future articles will delve into additional optimizations and buildpack features.

For more details on containerizing Node.js applications, check out the [official Node.js documentation](https://nodejs.org/en/docs/) and [Cloud Native Buildpacks documentation](https://buildpacks.io/docs/).

Happy building!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/0e306774-3067-4e23-9115-f3185d2ffa28/lesson/892e7d65-bc34-49a6-ac37-54e854f3e5bb" />
</CardGroup>


# Demo Packaging a Buildpack

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Creating-Buildpacks/Demo-Packaging-a-Buildpack/page

Learn to package your buildpack by creating a configuration file and using the pack tool to build and distribute your Docker image.

In this lesson, you will learn how to package your buildpack. The process starts by creating a configuration file named package.toml in the root directory of your project. This configuration file instructs the pack tool on where to locate your buildpack code.

## Step 1: Create the package.toml File

Begin by creating a file called package.toml in your project's root directory with the following content:

```toml theme={null}
[buildpack]
uri = "js-buildpack"
```

This configuration tells the pack tool that your buildpack resides in the folder named js-buildpack.

If your buildpack requires additional dependent buildpacks, you can include them in the package.toml file as demonstrated below:

```toml theme={null}
[buildpack]
uri = "js-buildpack"

[[dependencies]]
uri = "samples/buildpacks/hello-moon"

[[dependencies]]
uri = "docker://cnbs/sample-package:hello-world"
```

For this example, no additional dependencies are needed, so the initial simple configuration is sufficient.

## Step 2: Package the Buildpack

Next, package the buildpack by executing the following command. This command names your buildpack image "my-js-buildpack" and points the pack tool to the package.toml file located in your project root:

```bash theme={null}
pack buildpack package my-js-buildpack --config ./package.toml
```

After running the command, you should see an output similar to the following:

```plaintext theme={null}
[exporter] Reusing layer 'buildpacksio/lifecycle:process-types'
[exporter] Adding label 'io.buildpacks.lifecycle.metadata'
[exporter] Adding label 'io.buildpacks.build.metadata'
[exporter] Adding label 'io.buildpacks.project.metadata'
[exporter] Setting default process type 'web'
[exporter] Saving myapp...
[exporter] *** Images (826b95390a10):
[exporter] myapp
[exporter] Adding cache layer 'my-js-buildpack:node-dependencies'
[exporter] Reusing cache layer 'my-js-buildpack:node-js'
[exporter] Successfully built image myapp
```

<Callout icon="lightbulb">
  This output confirms that your buildpack has been successfully packaged into a Docker image.
</Callout>

## Step 3: Verify the Packaged Image

To confirm that the image has been created, list your Docker images by running:

```bash theme={null}
docker images
```

The output should include your newly packaged buildpack image, resembling the following:

```plaintext theme={null}
pack.local/builder/71796564636c657170e
<none>
<none>
<none>
pack.local/builder/7465747486977260570
pack.local/builder/787166d6717a63756579
<none>
my-js-buildpack
cnbs/sample-builder
<none>
myapp
latest    4217f3dcc8b  44 years ago  192MB
<none>    6abc728b2ef  44 years ago  243MB
<none>    0adf8920ef6  44 years ago  84.2MB
<none>    e2ab749ad5aa  44 years ago  192MB
<none>    ba1c5d8ad7df  44 years ago  243MB
<none>    7f0ca68075b3  44 years ago  192MB
<none>    04bf31c086fc  44 years ago  243MB
<none>    f8a9f9645d9  44 years ago 243MB
latest    04c8aa842a  44 years ago  3.52KB
latest    32c7fcb6fa  44 years ago  243MB
jammy     69b96b5c21  44 years ago  192MB
latest    82691b65db  44 years ago  243MB
<none>    593bd8d46dfe  44 years ago  243MB
```

## Step 4: Tag and Distribute the Buildpack Image

If you plan to distribute your buildpack image, you must tag the image with the proper repository identifier before pushing it to Docker Hub or another container registry. To tag the image, run:

```bash theme={null}
docker image tag my-js-buildpack sanjeevkt
```

After tagging your image, push it to the designated container registry using the appropriate Docker push command. This final step readies your buildpack for distribution.

Happy building!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-native-buildpacks/module/0e306774-3067-4e23-9115-f3185d2ffa28/lesson/3bf29623-0de4-4ad9-bcbf-f76e48b1c214" />
</CardGroup>
