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
```

### MySQL Dockerfile Excerpt

```dockerfile theme={null}
# Install server and dependencies
RUN rpmkeys --import https://repo.mysql.com/RPM-GPG-KEY-mysql \
    && yum install -y $MYSQL_SERVER_PACKAGE_URL $MYSQL_SHELL_PACKAGE_URL libpwquality \
    && yum clean all \
    && mkdir /docker-entrypoint-initdb.d

VOLUME /var/lib/mysql

COPY docker-entrypoint.sh /entrypoint.sh
COPY healthcheck.sh /healthcheck.sh

# Define entrypoint script.
ENTRYPOINT ["/entrypoint.sh"]

# Healthcheck.
HEALTHCHECK CMD /healthcheck.sh

EXPOSE 3306 33060

# Default command to start the server.
CMD ["mysqld"]
```

## The Default Ubuntu Container Runs Bash

The official Ubuntu image uses `bash` as its default command. Without an interactive TTY, Bash exits immediately:

```dockerfile theme={null}
FROM ubuntu:14.04

RUN \
    sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y build-essential software-properties-common \
                       byobu curl git htop man unzip vim wget && \
    rm -rf /var/lib/apt/lists/*

ADD root/.bashrc /root/.bashrc
ADD root/.gitconfig /root/.gitconfig
ADD root/.scripts /root/.scripts

ENV HOME /root
WORKDIR /root

CMD ["bash"]
```

Running `docker run ubuntu` without `-t` gives Bash no TTY, so it exits immediately—causing the container to stop.

## Overriding CMD at Runtime

You can override the default `CMD` by appending your own command in `docker run`:

```bash theme={null}
docker run ubuntu sleep 5
```

This runs `sleep 5`, keeps the container alive for 5 seconds, then exits.

## Making the Change Permanent with CMD

To bake a default command into your image, declare a new `CMD` in your Dockerfile:

```dockerfile theme={null}
FROM ubuntu
CMD ["sleep", "5"]
```

Build and run:

```bash theme={null}
docker build -t ubuntu-sleeper .
docker run ubuntu-sleeper    # sleeps 5 seconds and exits
```

### Shell Form vs Exec Form

CMD can use shell form:

```dockerfile theme={null}
CMD sleep 5
```

or exec form (JSON array):

```dockerfile theme={null}
CMD ["sleep", "5"]
```

With exec form, Docker does not invoke a shell, and the first element must be the executable.

## ENTRYPOINT vs CMD

Use `ENTRYPOINT` to fix the executable but allow arguments to vary:

```dockerfile theme={null}
FROM ubuntu
ENTRYPOINT ["sleep"]
```

Then:

```bash theme={null}
docker run ubuntu-sleeper 10    # runs: sleep 10
```

With only `CMD`, any arguments passed to `docker run` replace the entire command line.

> **lightbulb** `ENTRYPOINT` locks in your executable. Combine it with `CMD` to set default parameters.

## Combining ENTRYPOINT and CMD

To specify both a fixed executable and default arguments:

```dockerfile theme={null}
FROM ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```

* `docker run ubuntu-sleeper` runs `sleep 5`
* `docker run ubuntu-sleeper 10` runs `sleep 10`

> **triangle-alert** Always use the JSON array form for both `ENTRYPOINT` and `CMD` when combining them. This ensures proper argument handling.

### Quick Comparison

| Instruction | Purpose                        | Override Behavior                     |
| ----------- | ------------------------------ | ------------------------------------- |
| CMD         | Default command or parameters  | Replaced by arguments on `docker run` |
| ENTRYPOINT  | Fixed executable for the image | Overridable with `--entrypoint` flag  |

## Overriding ENTRYPOINT

You can also override `ENTRYPOINT` at runtime:

```bash theme={null}
docker run --entrypoint sleep2.0 ubuntu-sleeper 10
```

This runs `sleep2.0 10` instead of the original `sleep`.

## Links and References

* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [docker run reference](https://docs.docker.com/engine/reference/commandline/run/)
* [Docker Official Images](https://hub.docker.com/search?q=\&type=image)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/1e66d7ac-82f7-4c2f-bb21-7bf40934fed5)


# COPY vs ADD

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/COPY-vs-ADD/page

This guide compares the COPY and ADD directives in a Dockerfile, highlighting their differences and best practices for efficient image creation.

In this guide, we’ll compare the `COPY` and `ADD` directives in a Dockerfile, highlight their differences, and share best practices for keeping your images predictable and lean.

## Why It Matters

Both `COPY` and `ADD` bring files and directories from your build context into the container’s filesystem. However, `ADD` has two extra behaviors that can be surprising:

* Automatic extraction of local archives
* Remote URL download at build time

By understanding these differences, you can write clearer Dockerfiles and avoid unintended side effects.

## Feature Comparison

| Directive | Copies Local Files/Dirs | Extracts Local Archives | Downloads Remote URLs |
| --------- | ----------------------- | ----------------------- | --------------------- |
| `COPY`    | ✔️                      | ❌                       | ❌                     |
| `ADD`     | ✔️                      | ✔️                      | ✔️                    |

> **triangle-alert** Overusing `ADD` can introduce unexpected files or extra layers. If you only need to transfer files, prefer `COPY`.

***

## Simple Usage Examples

### 1. Using COPY

A straightforward copy of `testdir` from your context into the image:

```dockerfile theme={null}
FROM centos:7
COPY testdir /testdir
```

### 2. Using ADD for a Local Directory

Functionally identical to `COPY` when the source is a directory:

```dockerfile theme={null}
FROM centos:7
ADD testdir /testdir
```

### 3. ADD to Extract a Local Archive

Automatically unpack `app.tar.xz` into `/testdir`:

```dockerfile theme={null}
FROM centos:7
ADD app.tar.xz /testdir
```

***

## Consolidating Steps with RUN

Multiple `RUN` instructions add layers. Combine download, extraction, build, and cleanup in one `RUN` to keep images small:

```dockerfile theme={null}
FROM centos:7

RUN curl -fsSL http://example.com/app.tar.xz \
    | tar -xJ -C /testdir \
    && cd /testdir \
    && yarn build
```

This single-layer approach removes the archive stream in-flight, leaving no temporary files behind.

***

## When You Need ADD for Remote Files

If you prefer `ADD` to fetch a URL, then extract manually:

```dockerfile theme={null}
FROM centos:7
