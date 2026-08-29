# Nginx official image
CMD ["nginx"]

# MySQL official image
ENTRYPOINT ["/entrypoint.sh"]
CMD ["mysqld"]
```

A combined snippet illustrating both setups:

```dockerfile theme={null}
# ───── Nginx Setup ─────
RUN add-apt-repository -y ppa:nginx/stable \
  && apt-get update \
  && apt-get install -y nginx \
  && rm -rf /var/lib/apt/lists/* \
  && echo "\ndaemon off;" >> /etc/nginx/nginx.conf \
  && chown -R www-data:www-data /var/lib/nginx

VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs"]
WORKDIR /etc/nginx
CMD ["nginx"]

# ───── MySQL Setup ─────
RUN rpmkeys --import https://repo.mysql.com/RPM-GPG-KEY-mysql \
  && yum install -y $MYSQL_SERVER_PACKAGE_URL $MYSQL_SHELL_PACKAGE_URL libpwquality \
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

> **lightbulb** Use the JSON array form for `CMD` and `ENTRYPOINT` to avoid shell string parsing.

***

## 3. Overriding the Default Command at Runtime

Append a new command to `docker run` to replace the `CMD` entirely:

```bash theme={null}
docker run ubuntu sleep 5
```

Here, the container runs `sleep 5` instead of Bash, pauses for 5 seconds, then exits.

***

## 4. Baking Your Custom Command into a New Image

To make the override permanent, author a custom `Dockerfile`:

```dockerfile theme={null}
FROM ubuntu
# Shell form
CMD sleep 5

# Or JSON form
# CMD ["sleep", "5"]
```

Build and run:

```bash theme={null}
docker build -t ubuntu-sleeper .
docker run ubuntu-sleeper   # sleeps for 5 seconds
```

***

## 5. ENTRYPOINT vs. CMD

| Instruction | Purpose                              | Runtime Override     |
| ----------- | ------------------------------------ | -------------------- |
| CMD         | Sets a default command and arguments | Fully replaceable    |
| ENTRYPOINT  | Configures the primary executable    | Appends runtime args |

* **CMD**: default command, easily swapped by arguments you supply.
* **ENTRYPOINT**: fixed executable; any extra args in `docker run` are appended.

***

## 6. Combining `ENTRYPOINT` with Default `CMD` Arguments

Define both to set defaults that users can override:

```dockerfile theme={null}
FROM ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```

* `docker run ubuntu-sleeper` → runs `sleep 5`
* `docker run ubuntu-sleeper 10` → runs `sleep 10`

***

## 7. Replacing the Entrypoint at Runtime

Use `--entrypoint` to swap out the image’s entrypoint completely:

```bash theme={null}
docker run --entrypoint sleep ubuntu-sleeper 2.0 10
# Executes: sleep 2.0 10
```

***

## Links and References

* [Dockerfile reference: CMD](https://docs.docker.com/engine/reference/builder/#cmd)
* [Dockerfile reference: ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint)
* [docker run reference](https://docs.docker.com/engine/reference/commandline/run/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/15bcc1fb-cee6-46ac-89e7-549dbab427a2)


# Commands and Arguments in Kubernetes

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Commands-and-Arguments-in-Kubernetes/page

This tutorial explains how to configure commands and arguments in a Kubernetes Pod using the ubuntu-sleeper image.

In this tutorial, you’ll learn how to configure **commands** and **arguments** in a Kubernetes Pod. We’ll use a simple `ubuntu-sleeper` image that demonstrates how `ENTRYPOINT` and `CMD` from a Dockerfile map to the `command` and `args` fields in a Pod spec.

***

## Table of Contents

1. [Recap: ubuntu-sleeper Docker Image](#recap-ubuntu-sleeper-docker-image)
2. [Create a Pod with the Default Command](#create-a-pod-with-the-default-command)
3. [Override CMD with `args`](#override-cmd-with-args)
4. [Override ENTRYPOINT with `command`](#override-entrypoint-with-command)
5. [Summary & Mapping Table](#summary--mapping-table)
6. [References](#references)

***

## Recap: ubuntu-sleeper Docker Image

We built a minimal Docker image called **ubuntu-sleeper**:

```dockerfile theme={null}
FROM ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```

* Running without extra arguments uses the default sleep duration (5 seconds):
  ```bash theme={null}
  docker run --name ubuntu-sleeper ubuntu-sleeper
  ```
* Providing an argument overrides `CMD` (for example, sleep 10):
  ```bash theme={null}
  docker run --name ubuntu-sleeper ubuntu-sleeper 10
  ```

In Docker CLI, anything after the image name replaces the `CMD` instruction.

***

## Create a Pod with the Default Command

Here’s the simplest Pod manifest that runs `sleep 5` by default:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper-pod
spec:
  containers:
    - name: ubuntu-sleeper
      image: ubuntu-sleeper
```

Apply the Pod:

```bash theme={null}
kubectl create -f pod-definition.yml
```

By default, Kubernetes uses the image’s `ENTRYPOINT` + `CMD` (`sleep 5`), and the container will exit after 5 seconds.

***

## Override CMD with `args`

To change the sleep duration without touching the entrypoint, specify an `args` array in your Pod spec:

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

This runs `sleep 10`. Update the Pod:

```bash theme={null}
kubectl apply -f pod-definition.yml
```

> **lightbulb** The `args` field in Kubernetes corresponds directly to the Dockerfile `CMD`. Any elements you list here will override the default `CMD` values.

***

## Override ENTRYPOINT with `command`

If you need to override both the entrypoint and its arguments, use the `command` field for the entrypoint and `args` for its parameters:

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

* `command` replaces the Dockerfile `ENTRYPOINT`.
* `args` replaces the Dockerfile `CMD`.

Apply this configuration:

```bash theme={null}
kubectl create -f pod-definition.yml
```

> **triangle-alert** If you override the `command` field, make sure the specified executable exists in the container filesystem. Otherwise, the Pod will fail to start.

***

## Summary & Mapping Table

The table below summarizes how Dockerfile instructions map to Kubernetes Pod spec fields:

| Dockerfile Instruction | Kubernetes Pod Spec Field | Purpose                               |
| ---------------------- | ------------------------- | ------------------------------------- |
| ENTRYPOINT             | command                   | Defines the executable to run         |
| CMD                    | args                      | Provides default parameters/arguments |

Use these fields to precisely control the process invoked inside your containers.

***

## References

* [Kubernetes Official Documentation](https://kubernetes.io/docs/)
* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [Managing Containers in Pods](https://kubernetes.io/docs/concepts/workloads/pods/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/2c5416fe-a10c-42cc-8427-f776a2489163)
