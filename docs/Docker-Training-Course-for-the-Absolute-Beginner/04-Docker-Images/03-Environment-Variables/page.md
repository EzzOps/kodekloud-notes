# Environment Variables

Source: https://notes.kodekloud.com/docs/Docker-Training-Course-for-the-Absolute-Beginner/Docker-Images/Environment-Variables/page

Learn to configure a Python web application using environment variables for better management of application settings and deployment processes.

In this article, you'll learn how to configure a Python web application using environment variables. We’ll start by examining a basic Flask application that renders a web page with a background color. Initially, the background color is hardcoded in the application source code.

Below is the initial code snippet where the background color is set to "red":

```python theme={null}
import os
from flask import Flask, render_template

app = Flask(__name__)
color = "red"

@app.route("/")
def main():
    print(color)
    return render_template('hello.html', color=color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
```

In this version, any change to the background color requires direct modification of the source code. Best practices suggest externalizing configuration data, such as the background color, to keep your application logic independent from configuration changes.

> **lightbulb** Externalizing configuration values using environment variables allows you to change application settings without altering your code.

To implement this, we introduce an environment variable named APP\_COLOR. By reading the value of APP\_COLOR from the environment, you can easily update the background color without modifying the application's source code. Below is the updated version of the code:

```python theme={null}
import os
from flask import Flask, render_template

app = Flask(__name__)
color = os.environ.get('APP_COLOR')

@app.route("/")
def main():
    print(color)
    return render_template('hello.html', color=color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
```

## Running the Application with an Environment Variable

You can start the application with the desired background color by setting the environment variable inline. For example, to run the app with a blue background, use the following command:

```bash theme={null}
export APP_COLOR=blue; python app.py
```

## Deploying with Docker

When deploying your application as a Docker container, you can pass the environment variable at runtime using the Docker run command. For example, to run the container with the background color set to blue, execute:

```bash theme={null}
docker run -e APP_COLOR=blue simple-webapp-color
```

To deploy multiple containers with different background colors, you can run multiple containers with distinct values:

```bash theme={null}
docker run -e APP_COLOR=blue simple-webapp-color
docker run -e APP_COLOR=green simple-webapp-color
docker run -e APP_COLOR=pink simple-webapp-color
```

## Inspecting Environment Variables in a Running Container

To verify the environment variables set within a running container, use the Docker inspect command. The output will list the environment variables under the "Config" section. For example:

```bash theme={null}
docker inspect blissful_hopper
```

The output includes a section similar to the following:

```json theme={null}
[
  {
    "Id": "35505f7810d17291261a43391d4b6c0846594d415ce4f4d0a6ffbf9cc5109048",
    "State": {
      "Status": "running",
      "Running": true
    },
    "Mounts": [],
    "Config": {
      "Env": [
        "APP_COLOR=blue",
        "LANG=C.UTF-8",
        "GPG_KEY=0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D",
        "PYTHON_VERSION=3.6.6",
        "PYTHON_PIP_VERSION=18.1"
      ],
      "Entrypoint": [
        "python",
        "app.py"
      ]
    }
  }
]
```

This section demonstrates how the APP\_COLOR environment variable is configured in the container along with other system-level environment settings.

> **lightbulb** By using environment variables such as APP\_COLOR, you can easily manage configuration changes and streamline deployment processes without altering the application’s core logic.

That’s it for this article on using environment variables in Python web applications and Docker deployments for managing application settings.

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner/module/26faab43-a0ea-4355-9a94-f0bac957b507/lesson/eabfd75e-f974-48d7-884a-661142a04130)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner/module/26faab43-a0ea-4355-9a94-f0bac957b507/lesson/6eab379d-70cc-4ae7-871e-b861d5be6883)
