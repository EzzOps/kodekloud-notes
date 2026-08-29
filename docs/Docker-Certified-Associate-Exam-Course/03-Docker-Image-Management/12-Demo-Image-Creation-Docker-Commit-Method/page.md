# README.md  Dockerfile
```

***

## Reviewing the Dockerfile

Below is the complete `Dockerfile`. It installs OpenJDK 8, downloads Tomcat into `/opt/tomcat`, sets permissions, and deploys a sample WAR file.

```dockerfile theme={null}
FROM centos:7

# Define a build-time variable for Tomcat version
ARG tomcat_version=8.5.6

# Install prerequisites
RUN yum install -y epel-release java-1.8.0-openjdk.x86_64 wget

# Create tomcat group and home directory
RUN groupadd tomcat && mkdir -p /opt/tomcat

# Create non-interactive tomcat user
RUN useradd -s /bin/nologin -g tomcat -d /opt/tomcat tomcat

# Download and extract Tomcat
WORKDIR /
RUN wget https://archive.apache.org/dist/tomcat/tomcat-8/v${tomcat_version}/bin/apache-tomcat-${tomcat_version}.tar.gz \
 && tar -zxvf apache-tomcat-${tomcat_version}.tar.gz -C /opt/tomcat --strip-components=1

# Set ownership and permissions
RUN cd /opt/tomcat \
 && chgrp -R tomcat conf bin lib logs temp webapps work \
 && chmod g+rx conf \
 && chmod g+r conf/* \
 && chown -R tomcat tomcat logs temp webapps work \
 && chmod g+r bin/*

# Deploy sample application
WORKDIR /opt/tomcat/webapps
RUN wget https://tomcat.apache.org/tomcat-7.0-doc/appdev/sample/sample.war

# Expose port and define startup command
EXPOSE 8080
CMD ["/opt/tomcat/bin/catalina.sh","run"]
```

***

## Dockerfile Instruction Reference

| Instruction | Description                                        | Example                                  |
| ----------- | -------------------------------------------------- | ---------------------------------------- |
| `FROM`      | Base image                                         | `centos:7`                               |
| `ARG`       | Build-time variable; default Tomcat version        | `ARG tomcat_version=8.5.6`               |
| `RUN`       | Execute shell commands (install, create, download) | `yum install -y java-1.8.0-openjdk wget` |
| `WORKDIR`   | Set working directory                              | `/opt/tomcat/webapps`                    |
| `EXPOSE`    | Document container port                            | `8080`                                   |
| `CMD`       | Default command when container starts              | `["/opt/tomcat/bin/catalina.sh","run"]`  |

***

## Building and Running the Default Image

Build with the default Tomcat version (`8.5.6`):

```bash theme={null}
docker build -t yogeshraheja/tomcatone:v1 .
```

Expected output:

```bash theme={null}
Successfully built <IMAGE_ID>
Successfully tagged yogeshraheja/tomcatone:v1
```

Run the container, mapping host port 84 to container port 8080:

```bash theme={null}
docker run -d --name tomcat_default -p 84:8080 yogeshraheja/tomcatone:v1
```

Now visit `http://<host>:84` in your browser. You should see the Tomcat welcome page for version 8.5.6.

***

## Building with a Custom Tomcat Version

You can override `tomcat_version` at build time to use any release from the [Apache Tomcat Archive](https://archive.apache.org/dist/tomcat/):

```bash theme={null}
docker build \
  --build-arg tomcat_version=8.5.8 \
  -t yogeshraheja/tomcatone:v2 .
```

Sample output:

```bash theme={null}
Successfully built <NEW_IMAGE_ID>
Successfully tagged yogeshraheja/tomcatone:v2
```

Verify both images:

```bash theme={null}
docker image ls yogeshraheja/tomcatone
# REPOSITORY             TAG    IMAGE ID       SIZE
# yogeshraheja/tomcatone  v2     <NEW_IMAGE_ID> 497MB
# yogeshraheja/tomcatone  v1     <OLD_IMAGE_ID> 497MB
```

Run the new container on port 86:

```bash theme={null}
docker run -d --name tomcat_custom -p 86:8080 yogeshraheja/tomcatone:v2
```

Now open `http://<host>:86` to confirm you’re running Tomcat version 8.5.8.

> **triangle-alert** Always verify that the Tomcat version you specify in `--build-arg` exists in the archive. Incorrect versions will cause the build to fail.

***

## Links and References

* [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
* [Apache Tomcat Archive](https://archive.apache.org/dist/tomcat/)
* [Docker Documentation](https://docs.docker.com/)
* [GitHub: dockertomcat](https://github.com/yogeshraheja/dockertomcat)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/d931f184-8e2f-4ad6-8108-5f32da353b5d)


# Demo Image Creation Docker Commit Method

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Demo-Image-Creation-Docker-Commit-Method/page

This tutorial teaches how to build a custom HTTPD webserver image using the Docker commit method on a CentOS 7 base image.

In this tutorial, you’ll learn how to build an HTTPD webserver image on top of a CentOS 7 base image using the Docker commit method. By the end, you’ll have a reusable image that includes your custom Apache configuration and index page.

## 1. Pull the CentOS 7 Base Image

Start by pulling the official CentOS 7 image from Docker Hub:

```bash theme={null}
docker image pull centos:7
```

You should see output like:

```bash theme={null}
7: Pulling from library/centos
75f829a71a1c: Pull complete
Digest: sha256:19a79828ca2505eae0ff38c2f39901f4826737295157cc5212b7a372cd2b
Status: Downloaded newer image for centos:7
docker.io/library/centos:7
```

Verify it’s available locally:

```bash theme={null}
docker image ls
```

Example:

```bash theme={null}
REPOSITORY   TAG   IMAGE ID       CREATED        SIZE
centos       7     7e6257c9f8d8   2 months ago   203MB
```

## 2. Create and Start a Container

1. Create a container named `test` from the CentOS 7 image:
   ```bash theme={null}
   docker container create --name test centos:7
   ```
2. Start it:
   ```bash theme={null}
   docker container start test
   ```
3. Attach an interactive shell:
   ```bash theme={null}
   docker container exec -it test /bin/bash
   ```

## 3. Install HTTPD and Customize the Web Page

Inside the container shell:

```bash theme={null}
yum -y update
yum install -y httpd
echo "<h1>Hello from KodeKloud</h1>" > /var/www/html/index.html
```

This installs Apache HTTPD and replaces the default index page.

> **lightbulb** You can test the Apache service within the container before committing:

  ```bash theme={null}
  httpd -k start
  curl http://localhost
  httpd -k stop
  ```

## 4. Commit the Container to a New Image

1. Exit and stop the container:

   ```bash theme={null}
   exit
   docker container stop test
   ```

2. Review container status:

   ```bash theme={null}
   docker container ls -l
   ```

3. Commit with metadata and a default `CMD`. Here’s an overview of common flags:

| Flag | Description                              | Example                                |
| ---- | ---------------------------------------- | -------------------------------------- |
| -a   | Specify the author                       | `-a "Yogesh Raheja"`                   |
| -m   | Add a commit message                     | `-m "Add HTTPD and custom index"`      |
| -c   | Set a Dockerfile instruction (e.g., CMD) | `-c 'CMD ["httpd","-D","FOREGROUND"]'` |

4. Run `docker commit`:

   ```bash theme={null}
   docker container commit \
     -a "Yogesh Raheja" \
     -m "Add HTTPD and custom index" \
     -c 'CMD ["httpd", "-D", "FOREGROUND"]' \
     test webtest:v1
   ```

You’ll get a new image ID, for example:

```bash theme={null}
sha256:9cd11553a2e7...
```

Verify the image list:

```bash theme={null}
docker image ls
```

Expected:

```bash theme={null}
REPOSITORY   TAG   IMAGE ID       CREATED         SIZE
webtest      v1    9cd11553a2e7   30 seconds ago  328MB
centos       7     7e6257c9f8d8   2 months ago    203MB
```

## 5. Test Your Custom Image

Launch a container from `webtest:v1`, mapping port 80:

```bash theme={null}
docker container run -d --name webtesting -p 80:80 webtest:v1
```

Confirm it’s running:

```bash theme={null}
docker container ls -l
```

Open `http://<DockerHostIP>` in your browser. You should see:

```text theme={null}
Hello from KodeKloud
```

This verifies that your HTTPD configuration and custom index page are baked into the image.

## 6. Tag and Push to Docker Hub

1. Tag the image for your repository (replace `<your-dockerhub-username>`):

   ```bash theme={null}
   docker image tag webtest:v1 <your-dockerhub-username>/codekloud-webtest:v1
   ```

2. Log in to Docker Hub:

   ```bash theme={null}
   docker login
   ```

3. Push the tagged image:

   ```bash theme={null}
   docker push <your-dockerhub-username>/codekloud-webtest:v1
   ```

Visit your [Docker Hub](https://hub.docker.com/) repository to confirm the `v1` tag is published.

***

Congratulations! You’ve successfully created and published a custom Docker image using the `docker commit` method.

## References

* [Docker Commit Documentation](https://docs.docker.com/engine/reference/commandline/commit/)
* [Docker Image Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* [CentOS on Docker Hub](https://hub.docker.com/_/centos/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/2b07cbde-a382-448a-b4f0-0c7be474526d)
