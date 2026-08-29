# Sample installation output
Install  1 Package

Total download size: 67 k
Installed size: 230
Is this ok [y/N]: y
Downloading Packages:
podman-docker-4.0.2-1.module_el8.7.0+1106+45480 208 kB/s | 67 kB     00:00    
----------------------------------------------------------
Total                                         94 kB/s | 67 kB     00:00    
Running transaction check.
Transaction check succeeded.
Running transaction test.
Transaction test succeeded.
Running transaction
  Preparing   :                                            
  Installing   : podman-docker-2:4.0.2-1.module_el8.7.0+1106+45480ee0       1/1 
  Verifying   : podman-docker-2:4.0.2-1.module_el8.7.0+1106+45480ee0       1/1 

Installed:
  podman-docker-2:4.0.2-1.module_el8.7.0+1106+45480ee0.noarch

Complete!
[aaron@LFCS-CentOS ~]$
```

***

## Configuring Podman’s Default Registry

Podman’s configuration file is located at `/etc/containers/registries.conf`. Open it using your preferred text editor (for example, vim):

```bash theme={null}
sudo vim /etc/containers/registries.conf
```

Find the line that configures unqualified search registries:

```plaintext theme={null}
unqualified-search-registries = ["registry.fedoraproject.org", "registry.access.redhat.com", "registry.centos.org", "docker.io"]
```

<Callout icon="lightbulb">
  Comment out the above line and add the following to set `docker.io` as the default registry:
</Callout>

```plaintext theme={null}
# unqualified-search-registries = ["registry.fedoraproject.org", "registry.access.redhat.com", "registry.centos.org", "docker.io"]
unqualified-search-registries = ["docker.io"]
```

If you receive a message about emulating the Docker CLI with Podman, you can disable this behavior by creating a specific file:

```bash theme={null}
sudo touch /etc/containers/no-docker
```

***

## Working with Images

### Searching for an Image

For this guide, we will use the popular Nginx web server as an example. To locate available Nginx images, run:

```bash theme={null}
docker search nginx
```

The output may include entries such as:

```plaintext theme={null}
docker.io/rancher/nginx
docker.io/vmware/nginx-photon
docker.io/ibmcom/nginx-ingress-controller-ppc64le    Docker Image for IBM Cloud Private-CE (Community Edition) ppc64le ingress controller component
...
```

The official image, often referred to as `docker.io/library/nginx`, is well-supported and highly rated.

### Pulling an Image

To pull the official Nginx image, use its fully qualified name:

```bash theme={null}
docker pull docker.io/library/nginx
```

For convenience, you can also use the short form:

```bash theme={null}
docker pull nginx
```

To pull a specific version (for instance, version 1.20.2), run:

```bash theme={null}
docker pull nginx:1.20.2
```

After pulling an image, you can list the available images with:

```bash theme={null}
docker images
```

Example output:

```plaintext theme={null}
REPOSITORY                 TAG       IMAGE ID       CREATED         SIZE
docker.io/library/nginx    1.20.2    8f34c303855f   17 hours ago    146 MB
docker.io/library/nginx    latest    12766a6745ee   17 hours ago    146 MB
```

If you wish to remove a specific version, execute:

```bash theme={null}
docker rmi nginx:1.20.2
```

Images can also be referenced by their IMAGE ID, using just enough characters to uniquely identify them.

***

## Running and Managing Containers

### Creating and Attaching to a Container

To create and run a new container using the Nginx image, use:

```bash theme={null}
docker run nginx
```

This command creates a container and attaches your terminal to its output. If you find that the container’s logs (for example, startup messages from `/docker-entrypoint.sh`) continuously appear, press Ctrl+C to detach and terminate the container.

To run the container in detached mode, use the `-d` option:

```bash theme={null}
docker run -d nginx
```

This command returns a hexadecimal container ID and allows the container to run in the background.

### Listing, Stopping, and Removing Containers

To list active containers, run:

```bash theme={null}
docker ps
```

For a complete list of containers (including those that have exited), use:

```bash theme={null}
docker ps --all
```

To stop a container, specify its container ID or assigned name. For example, to stop a container named `interesting_mcclintock`:

```bash theme={null}
docker stop interesting_mcclintock
```

After stopping the container, remove it with:

```bash theme={null}
docker rm interesting_mcclintock
```

If the container is running and you wish to force its removal, use:

```bash theme={null}
docker rm --force interesting_mcclintock
```

### Removing Images

If you try to remove an image that is currently in use, Docker will produce an error:

```bash theme={null}
docker rmi nginx
```

Example error message:

```plaintext theme={null}
Error: image used by [SECRET_REDACTED]: image is in use by a container
```

To force the removal of an image (this will stop and remove any dependent containers), add the `--force` option:

```bash theme={null}
docker rmi --force nginx
```

***

## Advanced: Naming Containers and Port Mapping

For improved container management, you can assign custom names and set up port mapping between the host and container. To run Nginx in a container named `mywebserver` with host port 8080 mapped to container port 80, use:

```bash theme={null}
docker run -d -p 8080:80 --name mywebserver nginx
```

This configuration directs any connection to port 8080 on your machine to port 80 inside the container. To test the setup, you can use netcat:

```bash theme={null}
nc localhost 8080
```

After connecting, type the following command:

```HTTP theme={null}
GET /
```

Then press Enter. This simulates a browser request to Nginx, displaying the default HTML page. Press Ctrl+C to exit the netcat session.

Note: Mapping to privileged ports (ports below 1024) requires root privileges. For example, to map host port 80 to container port 80, use:

```bash theme={null}
sudo docker run -d -p 80:80 --name mywebserver nginx
```

***

## Getting Help

For detailed information about any Docker command, append the `--help` option. For example:

```bash theme={null}
docker container --help
```

Or to get help for a specific command like `docker rm`:

```bash theme={null}
docker rm --help
```

Below is an example of help output for Podman’s container removal command:

```plaintext theme={null}
podman rm [options] CONTAINER [CONTAINER...]
Examples:
  podman rm imageID
  podman rm mywebserver myflaskserver 860a4b23
  podman rm --force --all
  podman rm -f c684f0d469f2
Options:
  -a, --all                         Remove all containers
  --cidfile stringArray             Read the container ID from the file
  --depend                          Remove container and all containers that depend on the selected container
  -f, --force                       Force removal of a running or unusable container
  -i, --ignore                      Ignore errors when a specified container is missing
  -l, --latest                      Act on the latest container podman is aware of
  -t, --time uint                   Not supported with the "--remote" flag
                                   Seconds to wait for stop before killing the container
  -v, --volumes                     Remove anonymous volumes associated with the container
```

***

## Conclusion

This guide demonstrated the key steps in managing and configuring containers on Linux using Docker and Podman. We covered installing Podman, configuring its default registry, working with images, running containers in both attached and detached modes, and advanced topics like port mapping and naming containers. Continue exploring these concepts to elevate your container management skills.

Happy containerizing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/141c7a78-21ef-4dd8-86a3-fb0ef5037a8d/lesson/a54da927-4c31-4c14-94ab-a7dcdf0304b2" />
</CardGroup>


# Perform container management using commands such as podman and skopeo

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Manage-Containers/Perform-container-management-using-commands-such-as-podman-and-skopeo/page

This guide explains how to manage container images using Skopeo alongside Podman, covering installation, inspection, copying, deleting, and synchronizing images.

In this guide, you'll learn how to efficiently handle container images using Skopeo—a powerful command-line utility that complements Podman. With Skopeo, you can manage container images and repositories directly without needing to download them onto your local disk.

## Installing Skopeo

Before you begin, ensure that Skopeo is installed on your system. If it's not already installed, you can set it up using YUM. This command installs Skopeo along with all its necessary dependencies:

```bash theme={null}
$ sudo yum install skopeo
```

<Callout icon="lightbulb">
  For other package managers and installation options, refer to the [official Skopeo documentation](https://github.com/containers/skopeo/blob/main/install.md).
</Callout>

## Inspecting Container Repositories

Skopeo allows you to examine remote container repositories without using local disk space. The `skopeo inspect` command retrieves a JSON output containing various details such as repository tags, creation date, Docker version, and system architecture.

For example, to inspect a Fedora image hosted on the Fedora registry, run:

```bash theme={null}
$ skopeo inspect docker://registry.fedoraproject.org/fedora:latest
```

The output will include information similar to:

```json theme={null}
{
  "Name": "registry.fedoraproject.org/fedora",
  "Digest": "sha256:[SECRET_REDACTED]",
  "RepoTags": [
    "24",
    "25",
    "26-modular"
  ],
  "Created": "2020-04-29T06:48:16Z",
  "DockerVersion": "1.10.1",
  "Labels": {
    "license": "MIT",
    "name": "fedora",
    "vendor": "Fedora Project",
    "version": "32"
  },
  "Architecture": "amd64",
  "OS": "linux",
  "Layers": [
    "sha256:[SECRET_REDACTED]"
  ],
  "Env": [
    "DISTTAG=f32container",
    "FGC=f32",
    "container=oci"
  ]
}
```

## Inspecting Container Configurations

Beyond repository details, Skopeo can also inspect the configuration of a container image. By using the `--config` flag with `skopeo inspect`, and piping the result through `jq`, you can view neatly formatted configuration details. For instance:

```bash theme={null}
$ skopeo inspect --config docker://registry.fedoraproject.org/fedora:latest | jq
```

This command outputs a detailed JSON summary of the container's configuration, including environmental variables, command information, and more:

```json theme={null}
{
  "created": "2020-04-29T06:48:16Z",
  "architecture": "amd64",
  "os": "linux",
  "config": {
    "Env": [
      "DISTTAG=f32container",
      "FGC=f32"
    ],
    "cmd": [
      "/bin/bash"
    ]
  },
  "Labels": {
    "license": "MIT",
    "name": "fedora",
    "vendor": "Fedora Project",
    "version": "32"
  },
  "rootfs": {
    "type": "layers",
    "diff_ids": [
      "sha256:[SECRET_REDACTED]"
    ]
  },
  "history": [
    {
      "created": "2020-04-29T06:48:16Z",
      "comment": "Created by Image Factory"
    }
  ]
}
```

## Copying Container Images

Skopeo is not just for inspection—it also enables you to transfer container images across different storage mechanisms. Whether you're dealing with remote registries, local container storage backends, or OCI directories, Skopeo simplifies the process.

### Copying Between Registries

To transfer an image from a public repository to an internal enterprise registry, use the following command:

```bash theme={null}
$ skopeo copy docker://quay.io/buildah/stable docker://registry.kodekloud.com/buildah
```

### Copying from an OCI Layout Directory

If you need to copy an image from a local OCI layout directory to another local directory, this command will do the trick:

```bash theme={null}
$ skopeo copy oci:busybox_ocilayout:latest dir:myemptydirectory
```

## Deleting Container Images

Removing an image from a repository is straightforward with Skopeo’s `delete` command. Simply specify the image address to delete it:

```bash theme={null}
$ skopeo delete docker://localhost:5000/imagename:latest
```

<Callout icon="triangle-alert">
  Deleting images is irreversible. Ensure you have backups or are certain before executing the delete command.
</Callout>

## Synchronizing Registries

For maintaining consistency between registries, Skopeo offers a synchronization feature. This is especially beneficial when managing a local container registry that mirrors a remote repository. For example, to sync a remote registry with a local directory, run:

```bash theme={null}
$ skopeo sync --src docker --dest dir registry.kodekloud.com/busybox /media/usb
```

## Accessing Skopeo Man Pages

For comprehensive details about Skopeo and its various commands, the manual pages are an excellent resource. Use the `man` command to explore them.

To access the general Skopeo manual, run:

```bash theme={null}
$ man skopeo
```

This displays the manual which covers the tool’s overview, usage, and options. Here is an excerpt:

SKOPEO(1)                          August 2016                         SKOPEO(1)

NAME\
skopeo -- Command line utility used to interact with local and remote container images and container image registries

SYNOPSIS\
skopeo \[global options] command \[command options]

DESCRIPTION\
skopeo is a command line utility providing various operations with container images and container image registries.

Similarly, for information on specific commands such as copying images, inspect the dedicated man page:

```bash theme={null}
$ man skopeo-copy
```

This command details how to execute the `skopeo copy` operation, including its options and usage.

## Summary

Skopeo is a versatile tool that enhances container management by providing streamlined ways to inspect, copy, delete, and synchronize container images across various platforms. With seamless integration alongside Podman, managing container workflows becomes more efficient and flexible.

For further reading and advanced usage, consider exploring more resources:

* [Skopeo GitHub Repository](https://github.com/containers/skopeo)
* [Podman Documentation](https://podman.io/documentation)

By following the steps outlined in this guide, you can improve your container management strategies and streamline operations in your containerized environments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/141c7a78-21ef-4dd8-86a3-fb0ef5037a8d/lesson/dc468105-88e9-4dba-8cf3-e98fc676e572" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/141c7a78-21ef-4dd8-86a3-fb0ef5037a8d/lesson/1b588fdb-14cc-461a-93fb-81551aefbe35" />
</CardGroup>
