# Install Nginx.
RUN \
    add-apt-repository -y ppa:nginx/stable && \
    apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/* && \
    echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
    chown -R www-data:www-data /var/lib/nginx

# Define mountable directories.
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs"]

# Define working directory.
WORKDIR /etc/nginx

# Define default command.
CMD ["nginx"]

# Install server
RUN rpmmkeys --import https://repo.mysql.com/RPM-GPG-KEY-mysql \
    && yum install -y $MYSQL_SERVER_PACKAGE_URL $MYSQL_SHELL_PACKAGE_URL libpqquality \
    && yum clean all \
    && mkdir /docker-entrypoint-initdb.d

VOLUME /var/lib/mysql

COPY docker-entrypoint.sh /entrypoint.sh
COPY healthcheck.sh /healthcheck.sh
ENTRYPOINT ["/entrypoint.sh"]
HEALTHCHECK CMD /healthcheck.sh
EXPOSE 3306 33060
CMD ["mysqld"]
```

Another common example is a Dockerfile for an Ubuntu image that sets bash as the default command:

```dockerfile theme={null}
# Pull base image.
FROM ubuntu:14.04

# Install.
RUN \
    sed -i 's/#\(.*multiverse\)$/\1/' /etc/apt/sources.list && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y build-essential && \
    apt-get install -y software-properties-common && \
    apt-get install -y byobu curl git htop man unzip vim wget && \
    rm -rf /var/lib/apt/lists/*

# Add files.
ADD root/.bashrc /root/.bashrc
ADD root/.gitconfig /root/.gitconfig
ADD root/.scripts /root/.scripts

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root

# Define default command.
CMD ["bash"]
```

Because bash is a shell that waits for terminal input, if Docker does not attach a terminal at runtime, the container exits immediately when no input is provided.

## Overriding the Default Command

You can override the default command defined in the Docker image by appending a different command to the Docker run command. For instance, if you want the container to run a sleep command for five seconds instead of starting bash, execute:

```bash theme={null}
docker run ubuntu sleep 5
```

This approach temporarily replaces the default CMD from the image. To make a permanent change, create a new Docker image based on the Ubuntu image with a custom CMD. For example:

```dockerfile theme={null}
FROM ubuntu
CMD ["sleep", "5"]
```

Build and run your new image with the following commands:

```bash theme={null}
docker build -t ubuntu-sleeper .
docker run ubuntu-sleeper
```

The container will now always sleep for five seconds before exiting.

## Using ENTRYPOINT to Combine Commands and Arguments

What if you want to pass a variable argument, such as the number of seconds, when running the container without specifying the command every time? This is where the ENTRYPOINT instruction proves useful.

ENTRYPOINT sets the default executable that runs when the container starts. Any command-line arguments provided at runtime are appended to the ENTRYPOINT. Consider this Dockerfile:

```dockerfile theme={null}
FROM ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```

With this configuration:

* Running the container without additional arguments:

  ```bash theme={null}
  docker run ubuntu-sleeper
  ```

  Executes the command:

  Command at Startup: sleep 5

* Running the container with an extra argument:

  ```bash theme={null}
  docker run ubuntu-sleeper 10
  ```

  Executes the command:

  Command at Startup: sleep 10

<Callout icon="triangle-alert">
  If the necessary argument is missing (for example, if the ENTRYPOINT command expects an argument and none is provided), the container will fail to run and display an error.
</Callout>

To temporarily override the ENTRYPOINT and run a different command (for example, switching from sleep to sleep2.0), you can use the --entrypoint flag:

```bash theme={null}
docker run --entrypoint sleep2.0 ubuntu-sleeper 10
```

This command will execute:

Command at Startup: sleep2.0 10

This example clearly illustrates the difference between CMD and ENTRYPOINT. CMD's parameters can be completely overridden by command-line arguments, whereas ENTRYPOINT ensures that its predefined executable is always run, appending any supplied arguments.

***

That concludes our lesson on managing commands and arguments in Docker. By mastering these concepts, you can create more flexible and powerful containerized applications. Happy containerizing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/c11b6336-739d-4891-9e9e-8b46a1986cdd" />
</CardGroup>


# Commands and Arguments in Kubernetes

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Configuration/Commands-and-Arguments-in-Kubernetes/page

This lesson covers customizing container behavior in Kubernetes by overriding commands and arguments defined in Docker images.

Welcome to this lesson on handling commands and arguments within a Kubernetes pod. In this guide, you'll learn how to customize container behavior by overriding default settings defined in your Docker image. Previously, we built a simple Docker image called "ubuntu-sleeper" that pauses execution (sleeps) for a specified number of seconds. By default, running:

```bash theme={null}
docker run ubuntu-sleeper
```

makes the container sleep for five seconds. However, you can change this behavior by providing a command-line argument. For example, running:

```bash theme={null}
docker run --name ubuntu-sleeper ubuntu-sleeper 10
```

will cause the container to sleep for 10 seconds.

## Overriding Default Arguments in a Pod Definition

Kubernetes allows you to replicate the Docker behavior of passing command-line arguments by using the `args` field in a pod definition. When you specify additional arguments in a Kubernetes pod, they are supplied as an array.

Consider this pod definition template. In the example below, the pod runs the "ubuntu-sleeper" container and overrides the default sleep duration by setting the `args` field to `["10"]`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper-pod
spec:
  containers:
    - name: ubuntu-sleeper
      image: ubuntu-sleeper
      args: ["10"]
```

To create the pod, execute:

```bash theme={null}
kubectl create -f pod-definition.yml
```

When the pod starts, it creates a container from the specified image. The `args` field in the Kubernetes definition effectively overrides the default CMD instruction defined in the Dockerfile.

<Callout icon="lightbulb">
  In Kubernetes, you can manipulate container behavior at startup by tweaking the pod specification. Always ensure your YAML syntax is valid to avoid deployment issues.
</Callout>

## Overriding the Entrypoint

In our Dockerfile, we defined an entry point and a CMD instruction as follows:

```dockerfile theme={null}
FROM ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```

Typically, when you run the container, the entry point `sleep` is combined with the CMD default `5`. To override the entry point in Docker, you would use the `--entrypoint` flag, for instance:

```bash theme={null}
docker run --name ubuntu-sleeper --entrypoint sleep2.0 ubuntu-sleeper 10
```

In Kubernetes, you achieve the same result by using the `command` field in the pod definition. Specifically, the `command` field replaces the ENTRYPOINT from the Dockerfile, and the `args` field continues to override the CMD instruction. Below is an example demonstrating how to set both fields:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper-pod
spec:
  containers:
    - name: ubuntu-sleeper
      image: ubuntu-sleeper
      command: ["sleep2.0"]
      args: ["10"]
```

To deploy this pod, run:

```bash theme={null}
kubectl create -f pod-definition.yml
```

<Callout icon="lightbulb">
  Using the `command` and `args` fields in tandem gives you full control over the container's startup process, allowing you to override both the ENTRYPOINT and CMD as needed.
</Callout>

## Summary

There are two primary fields in a Kubernetes pod definition that correspond to your Dockerfile settings:

| Field   | Dockerfile Equivalent | Purpose                                                  |
| ------- | --------------------- | -------------------------------------------------------- |
| command | ENTRYPOINT            | Overrides the default entry point of the image           |
| args    | CMD                   | Replaces the default arguments passed to the entry point |

By correctly configuring these fields, you can modify the startup parameters of your container dynamically. This capability is particularly useful for customizing application behavior in different environments.

Review the provided exercises to practice configuring and troubleshooting commands and arguments in Kubernetes, and enhance your deployment strategies effectively.

For additional resources, refer to [Kubernetes Documentation](https://kubernetes.io/docs/) and [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/a7fb1078-b411-40ed-b2a3-100e46be9c70" />
</CardGroup>
