# (No running container will appear.)
docker ps -a
# (The container will be shown in an "exited" state.)
```

When you run these commands, Docker creates a container from the Ubuntu image and launches it. However, because the container’s default process (typically `bash`) expects a terminal, it exits immediately when no terminal is attached. Unlike virtual machines, containers are designed to run a specific task or process (e.g., hosting a web server, application server, or database). Once that task completes or the process crashes, the container stops running.

<Callout icon="lightbulb">
  Containers are meant to run specific tasks rather than continuously running processes. The default behavior of many images reflects this design philosophy.
</Callout>

## Defining the Default Process in a Dockerfile

Most Docker images use the CMD instruction in their Dockerfile to specify the process that should run inside the container. For example:

* **Nginx image:** Uses `CMD ["nginx"]` to start the Nginx server.
* **MySQL image:** Uses `CMD ["mysqld"]` to launch the MySQL daemon.

Consider this excerpt from a Dockerfile that installs both Nginx and MySQL:

```dockerfile theme={null}
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

# Install MySQL server.
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

The Ubuntu image Dockerfile is structured similarly:

```dockerfile theme={null}
# Pull base image.
FROM ubuntu:14.04

# Install dependencies.
RUN \
    sed -i 's/# \(.*multiverse\)/\1/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y build-essential software-properties-common && \
    apt-get install -y byobu curl git htop man unzip vim wget && \
    rm -rf /var/lib/apt/lists/*

# Add custom files.
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

In this Ubuntu example, Docker launches `bash` as the default command. However, since Docker does not attach a terminal by default, the shell exits immediately, and the container stops.

## Overriding the Default Command

You can override the default CMD by appending a new command to the `docker run` command. For example, running the Ubuntu container with the `sleep` command:

```bash theme={null}
docker run ubuntu sleep 5
```

Here, the container runs the `sleep` program for 5 seconds before exiting.

### Making the Change Permanent

If you prefer that your image always executes the `sleep` command when started, you can create a new image based on Ubuntu with an updated CMD:

```dockerfile theme={null}
FROM ubuntu
CMD ["sleep", "5"]
```

After building the image:

```bash theme={null}
docker build -t ubuntu-sleeper .
docker run ubuntu-sleeper
```

The container runs `sleep 5` each time it starts. However, if you want the flexibility to change the sleep duration without rebranding the image, you can override the CMD at runtime:

```bash theme={null}
docker run ubuntu-sleeper sleep 10
```

While this works, the image name (`ubuntu-sleeper`) might misleadingly imply that the container always runs `sleep`.

## Using ENTRYPOINT with CMD for Flexibility

The ENTRYPOINT instruction allows you to fix the executable while still providing flexibility for command-line arguments to override or extend the CMD settings. With ENTRYPOINT, any command-line arguments are appended to the entrypoint command.

For example:

```dockerfile theme={null}
FROM ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```

When you run the container without additional arguments:

```bash theme={null}
docker run ubuntu-sleeper
```

The container executes `sleep 5`. If you run:

```bash theme={null}
docker run ubuntu-sleeper 10
```

Docker executes `sleep 10`, replacing the default operand defined in CMD with the provided one.

<Callout icon="triangle-alert">
  If you define only ENTRYPOINT without a default CMD, the container may fail to execute properly if no command-line arguments are provided. For instance, removing CMD can result in errors like "sleep: missing operand".
</Callout>

## Overriding Entrypoint at Runtime

If you need to change the entrypoint entirely—say, switching from `sleep` to a different executable like `sleep2.0`—you can override it at runtime using the `--entrypoint` option:

```bash theme={null}
docker run --entrypoint sleep2.0 ubuntu-sleeper 10
```

In this case, the container executes `sleep2.0 10`.

## Summary of Docker Commands and Dockerfile Configurations

Below is a summary table of key commands and their effects:

| Command/Configuration              | Description                                                                   | Example                                              |
| ---------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------- |
| Default CMD in Ubuntu container    | Executes `bash` but exits when no terminal is attached                        | `docker run ubuntu`                                  |
| Overridden CMD at runtime          | Replaces default command with a specified one (e.g., `sleep 5`)               | `docker run ubuntu sleep 5`                          |
| Permanent CMD update in Dockerfile | Builds an image with a permanent command change                               | `CMD ["sleep", "5"]`                                 |
| Using ENTRYPOINT with CMD          | Fixes the executable while allowing dynamic command-line argument replacement | `ENTRYPOINT ["sleep"]` & `CMD ["5"]`                 |
| Override ENTRYPOINT at runtime     | Replaces the image's fixed executable with an alternative one                 | `docker run --entrypoint sleep2.0 ubuntu-sleeper 10` |

### Consolidated Dockerfile Example

Below is the consolidated Dockerfile example using both ENTRYPOINT and CMD:

```dockerfile theme={null}
# Dockerfile for Ubuntu sleeper image with ENTRYPOINT and CMD
FROM ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```

After building the image:

```bash theme={null}
docker build -t ubuntu-sleeper .
```

* Running without additional parameters:

  ```bash theme={null}
  docker run ubuntu-sleeper
  ```

  Executes the command: `sleep 5`

* Overriding the sleep duration:

  ```bash theme={null}
  docker run ubuntu-sleeper 10
  ```

  Executes the command: `sleep 10`

* Overriding the entrypoint and the sleep duration:

  ```bash theme={null}
  docker run --entrypoint sleep2.0 ubuntu-sleeper 10
  ```

  Executes the command: `sleep2.0 10`

That concludes our exploration of Docker's CMD versus ENTRYPOINT. Happy containerizing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner/module/26faab43-a0ea-4355-9a94-f0bac957b507/lesson/b9bc7112-845b-4706-ab56-d47cb1435fbd" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner/module/26faab43-a0ea-4355-9a94-f0bac957b507/lesson/d3a90d5f-f354-4574-b8cc-97935f3374e8" />
</CardGroup>


# Demo Creating a new Docker Image

Source: https://notes.kodekloud.com/docs/Docker-Training-Course-for-the-Absolute-Beginner/Docker-Images/Demo-Creating-a-new-Docker-Image/page

This guide explains how to build a custom Docker image for a Python Flask web application and push it to Docker Hub.

Welcome to this detailed guide on building a custom Docker image for a simple Python Flask web application. In this tutorial, you'll learn how to set up the application, manually run it, containerize it using Docker, and finally push your image to Docker Hub. The complete project is available on my [GitHub page](https://github.com).

***

## Application Overview

Our web application comprises a single file, `app.py`, which defines two routes:

* The default route (`/`) displays a welcome message.
* The `/how are you` route returns the response "I am good, how about you?".

Below is the complete source code for `app.py`:

```python theme={null}
import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

@app.route('/how are you')
def hello():
    return 'I am good, how about you?'

if __name__ == "__main__":
    app.run()
```

***

## Deploying the Application Manually

Before containerizing the application, you can deploy it manually on an Ubuntu host. Follow these steps:

### Installing Dependencies

Update your package lists and install Python along with required packages:

```bash theme={null}
apt-get update
apt-get install -y python python-setuptools python-dev build-essential python-pip python-mysqldb
```

Next, install Flask and its MySQL helper using pip:

```bash theme={null}
pip install flask
pip install flask-mysql
```

To run the application manually, execute the command below:

```bash theme={null}
FLASK_APP=app.py flask run --host=0.0.0.0
```

Once running, access the following URLs in your web browser:

* `http://<IP>:5000` – should display "Welcome!"
* `http://<IP>:5000/how%20are%20you` – should display "I am good, how about you?"

The console output will look similar to:

```plaintext theme={null}
=> Welcome
=> I am good, how about you?
```

***

## Running the Application Inside a Docker Container

Containerizing your application isolates the environment and simplifies dependency management.

### Starting an Ubuntu Container

Launch an interactive Ubuntu container with a bash shell:

```bash theme={null}
docker run -it ubuntu bash
```

Inside the container, update the package index and install Python:

```bash theme={null}
apt-get update
apt-get install -y python
```

<Callout icon="lightbulb">
  If you encounter errors while installing Python due to an outdated package index, make sure to run `apt-get update` before attempting the installation.
</Callout>

### Installing pip and Flask

If you receive a "pip: command not found" error, install pip:

```bash theme={null}
apt-get install python-pip
```

Then install Flask using pip:

```bash theme={null}
pip install flask
```

Successful installation will display messages confirming that Flask and its dependencies (itsdangerous, click, Werkzeug, Jinja2, MarkupSafe) have been installed.

### Running the Application

After copying your application code into the container (for example, place it in `/opt/app.py`), run the application with:

```bash theme={null}
FLASK_APP=app.py flask run --host=0.0.0.0
```

The expected output is:

```plaintext theme={null}
 * Serving Flask app "app"
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

You can now access the application using the container's IP on port 5000. Visiting the `/how%20are%20you` route should trigger a GET request and display the correct response.

***

## Recording the Steps

It's a good practice to record the commands executed for troubleshooting or later use. Below is an example command history:

```bash theme={null}
apt-get update
apt-get install -y python
apt-get install python-pip
pip install flask
cat > /opt/app.py
vi /opt/app.py
FLASK_APP=app.py flask run --host=0.0.0.0
history
```

Keep these steps handy as you move forward to Dockerize your application.

***

## Dockerizing the Application

After verifying your web application inside a Docker container, you can now create a Docker image.

### Creating a Dockerfile

Create a project directory (e.g., `my-simple-webapp`) and add a file named `Dockerfile` with the following content:

```Dockerfile theme={null}
FROM ubuntu
