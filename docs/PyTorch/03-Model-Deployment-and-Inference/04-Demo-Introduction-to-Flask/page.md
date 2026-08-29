# Use the official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /opt/app

# Install CPU version of PyTorch
RUN pip install torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code
COPY ./flask_app .

# Create a user and group for running the app
RUN groupadd -r pytorch && useradd --no-log-init -r -g pytorch pytorch

# Change ownership of the app directory
RUN chown -R pytorch:pytorch /opt/app

# Switch to the created user
USER pytorch

# Expose the port that our Flask app is listening on
EXPOSE 8000

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
```

Place this Dockerfile in the same directory as your `requirements.txt` file and your Flask app. Then, build your Docker image with the following command:

```bash theme={null}
docker build -t mobilenetv3lg-flask:v1.0 .
```

During the build process, you will see steps that include loading the base image, copying files, installing Python packages via pip, and setting up a non-root user. After the build completes, verify the new image with:

```bash theme={null}
docker images
```

A sample output might look like this:

```text theme={null}
REPOSITORY              TAG       IMAGE ID       CREATED               SIZE
mobilenetv3lg-flask     v1.0      1734db15a849   About a minute ago    5.39GB
hello-world             latest    d2c94e258dc9   20 months ago         13.3kB
```

<Callout icon="lightbulb">
  After optimizing the image by including only CPU dependencies, you may notice a reduction in image size (e.g., from 5.39GB to 1.34GB).
</Callout>

***

## Running the Docker Container

Now that your Docker image is ready, you can run it as a container. The command below maps port 8000 in the container to port 8000 on your local machine:

```bash theme={null}
docker run -p 8000:8000 mobilenetv3lg-flask:v1.0
```

When the container starts, you may see log messages similar to the following:

```text theme={null}
2025-01-16 19:05:41,363 - INFO - Loading MobileNetV3 Large pre-trained model...
Downloading: "https://download.pytorch.org/models/mobilenet_v3_large-5c1a4163.pth" to /home/pytorch/.cache/torch/hub/checkpoints/mobilenet_v3_large-5c1a4163.pth
100.0%
2025-01-16 19:05:41,827 - INFO - Model loaded successfully.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:8000
...
```

For deploying the container in detached mode (running in the background), use the `-d` flag:

```bash theme={null}
docker run -d -p 8000:8000 mobilenetv3lg-flask:v1.0
```

You can monitor your containers with:

```bash theme={null}
docker ps
```

And view container logs with:

```bash theme={null}
docker logs <container_id>
```

***

## Testing the Flask Application Inside Docker

With your container running, test the Flask endpoint by sending a POST request with an image payload. The following Python script encodes an image in Base64, constructs a JSON payload, and sends it to the `/predict` endpoint:

```python theme={null}
import requests
import base64

# Open the image file and encode it to Base64
with open('dog-1.jpg', 'rb') as img_file:
    base64_string = base64.b64encode(img_file.read()).decode('utf-8')

# Construct the JSON payload
payload = { "image": base64_string }

# Specify the headers
headers = { "Content-Type": "application/json" }

# Send the POST request
response = requests.post("http://127.0.0.1:8000/predict", headers=headers, json=payload)

# Print the response from the server
print("Response JSON:", response.json())
```

A successful response might show:

```text theme={null}
Response JSON: {'prediction': 207}
```

This indicates that the inference request was processed correctly by your Flask application.

***

## Tagging and Pushing the Docker Image to Docker Hub

To share your Docker image, start by tagging it with your Docker Hub username:

```bash theme={null}
docker tag mobilenetv3lg-flask:v1.0 username/mobilenetv3lg-flask:v1.0
```

Next, log in to Docker Hub:

```bash theme={null}
docker login -u username
```

Enter your password when prompted. After logging in, push the tagged image to Docker Hub:

```bash theme={null}
docker push username/mobilenetv3lg-flask:v1.0
```

Once pushed, you can pull and run the image on another system with:

```bash theme={null}
docker pull username/mobilenetv3lg-flask:v1.0
docker run -p 8000:8000 username/mobilenetv3lg-flask:v1.0
```

The output during the push confirms that Docker has uploaded the image layers and generated a digest.

***

## Conclusion

In this lesson, you learned how to:

* Install Docker on an Ubuntu server.
* Build a Docker image using a Dockerfile that packages a Flask application along with CPU-based PyTorch dependencies.
* Run a Docker container and verify its operation by sending a test inference request.
* Tag and push the Docker image to Docker Hub for easy distribution and deployment.

With your Docker image now hosted on Docker Hub, you can seamlessly deploy and share your application across different environments. Next, we will explore containerizing a best-trained model in a lab exercise.

Happy containerizing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/a958efa1-845c-4cdf-9261-7688050bd96c/lesson/cd9074ad-839d-4206-b652-89620b04a816" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/pytorch/module/a958efa1-845c-4cdf-9261-7688050bd96c/lesson/a2426a0c-b7e8-4de8-9d0e-841003658a16" />
</CardGroup>


# Demo Introduction to Flask

Source: https://notes.kodekloud.com/docs/PyTorch/Model-Deployment-and-Inference/Demo-Introduction-to-Flask/page

This lesson explores Flask basics and demonstrates serving a machine learning model using Flask for model deployment.

In this lesson, we explore the basics of Flask and demonstrate how to serve a machine learning model using Flask. This guide combines content from a Jupyter Notebook and a standalone Flask application file, providing a comprehensive introduction to model deployment with Flask.

***

## Installing and Verifying Flask

Before building the application, ensure that Flask is installed. Run the following commands to install Flask, check its version, and inspect the directory structure of your Flask app:

```bash theme={null}
!pip install Flask
```

```bash theme={null}
bash
!python -m flask --version
```

```bash theme={null}
bash
!tree flask_app/
```

These commands not only install Flask but also verify that the essential files exist within the `flask_app/` directory, an important part of your model deployment workflow.

If Flask is already installed, you may see output indicating that the requirements are already satisfied, for example:

```plaintext theme={null}
!pip install Flask
```

```plaintext theme={null}
Requirement already satisfied: Flask in /root/venv/lib/python3.11/site-packages (3.1.0)
Requirement already satisfied: Werkzeug>=3.1 in /root/venv/lib/python3.11/site-packages (from Flask) (3.1.3)
Requirement already satisfied: Jinja2>=3.1.2 in /root/venv/lib/python3.11/site-packages (from Flask) (3.1.5)
Requirement already satisfied: itsdangerous>=2.2 in /root/venv/lib/python3.11/site-packages (from Flask) (2.2.0)
Requirement already satisfied: click>=8.1.3 in /root/venv/lib/python3.11/site-packages (from Flask) (8.1.8)
Requirement already satisfied: blinker>=1.9 in /root/venv/lib/python3.11/site-packages (from Flask) (1.9.0)
Requirement already satisfied: MarkupSafe>=2.0 in /root/venv/lib/python3.11/site-packages (from Jinja2>=3.1.2->Flask) (3.0.2)
```

You can also re-run the version command from within the Notebook:

```bash theme={null}
python -m flask --version
```

This command displays your Python version, Flask version (3.1.0), and Werkzeug version (3.1.3).

Next, verify the structure of your Flask app. Running:

```bash theme={null}
tree flask_app/
```

should produce an output similar to:

```plaintext theme={null}
flask_app
├── app.py
└── image_transformations.py
```

***

## Creating the Flask Application

Before starting the Flask server, initialize the app by loading any required environment variables and your machine learning model. In this example, we use the MobileNetV3 Large pre-trained model. It is essential that the model is loaded before the application processes any requests.

Below is an example of the initial setup with logging and error handling:

```python theme={null}
import os
import io
import base64
import json
import logging
from flask import Flask, request, jsonify
from torchvision import models
import torch
from PIL import Image
from image_transforms import preprocess  # Ensure this module is available
