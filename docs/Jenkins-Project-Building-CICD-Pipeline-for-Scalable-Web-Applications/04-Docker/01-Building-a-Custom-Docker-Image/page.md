# Building a Custom Docker Image

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Docker/Building-a-Custom-Docker-Image/page

Learn to build a custom Docker image for a Flask application and push it to Docker Hub.

In this guide, you'll learn how to build a custom Docker image for a Flask application and push it to [Docker Hub](https://hub.docker.com). We will containerize a simple Flask app that manages tasks and walk through creating the Dockerfile, building the image, and deploying it.

## Application Overview

Our sample Flask application (app.py) manages tasks with basic operations. Below is an excerpt of the code:

```python theme={null}
from flask import Flask, render_template, request

app = Flask(__name__)
