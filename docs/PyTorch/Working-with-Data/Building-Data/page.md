# Install Flask via pip
pip install Flask
```

<Callout icon="lightbulb">
  Remember to manage your Python environments effectively using tools like virtualenv or conda to keep dependencies organized.
</Callout>

After installation, verify the proper setup of Flask by checking its version:

```bash theme={null}
# Check the version of Flask
python -m flask --version

# Expected Output
# Python 3.12.4
# Flask 3.1.0
# Werkzeug 3.1.3
```

## Setting Up a Flask Application

Establishing a well-organized project structure is key for maintainability. Create a primary folder for your application that contains an `app.py` file for your main logic, along with dedicated folders for models, static assets (CSS, images, JavaScript, etc.), templates, and tests.

Example project structure:

```text theme={null}
flask_app/
    app.py
    model/
        pytorch_model.pth
    static/
        style.css
    templates/
        index.html
        layout.html
    tests/
        test_app.py
        test_model.py
```

Within `app.py`, import Flask, set up an instance, and define routes with decorators. For example:

```python theme={null}
# Simple Flask App
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Flask!"

if __name__ == '__main__':
    app.run(debug=True)
```

When you navigate to the root URL, the application responds with "Welcome to Flask!" This simple setup establishes a foundation for further expansion.

## Integrating a PyTorch Model

To integrate a PyTorch model, load it into memory when the Flask app starts—this prevents redundant loading during inference. Use `torch.load` to import your model and set it to evaluation mode:

```python theme={null}
# Load a PyTorch model in Flask
import torch
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load model
model = torch.load('model/pytorch_model.pth')
model.eval()
```

Loading the model at startup ensures that it is ready to handle incoming requests efficiently.

### Creating an Inference Endpoint

Next, define an endpoint (e.g., `/predict`) that processes POST requests. This endpoint will accept JSON data, convert it to a PyTorch tensor, perform inference, and return the prediction as JSON. Consider the following example:

```python theme={null}
# Define an inference endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_tensor = torch.tensor(data['input'])
    output = model(input_tensor)
    return jsonify({'output': output.tolist()})
```

Example JSON request and response:

```json theme={null}
{
    "input": [1.0, 2.0, 3.0]
}
```

```json theme={null}
{
    "output": [0.85, 0.10, 0.05]
}
```

This endpoint processes the input, generates inferences, and returns the results in a structured JSON format.

## Running the Flask Server

After setting up your application, run the Flask development server locally by executing your Python file. For example, with `app.py` as your main file:

```bash theme={null}
# Run Flask application
python app.py

# Output
* Serving Flask app "app"
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

<Callout icon="triangle-alert">
  The built-in server is intended for development only. For production environments, consider using a production-ready WSGI server.
</Callout>

## Deploying with Gunicorn

For production deployments, use a WSGI server like Gunicorn. First, install Gunicorn:

```bash theme={null}
# Install Gunicorn
pip install gunicorn
```

Then, run your Flask application using Gunicorn:

```bash theme={null}
# Run Flask app with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app

# Output example:
# [2024-12-06 14:03:30 -0500] [96381] [INFO] Starting gunicorn 23.0.0
```

This command starts Gunicorn with four worker processes, binding to all network interfaces on port 8080. Here, `app:app` tells Gunicorn to locate the Flask instance named `app` within the `app.py` file.

## Best Practices for Flask Deployment

Adhering to best practices ensures your application is efficient, secure, and scalable:

1. **Prepare the Model:**
   * Load the model once at startup to avoid repetitive loading.
   * Set the model to evaluation mode for accurate predictions.

<Frame>
  ![The image provides best practices for preparing a model, suggesting to load the model once during start-up to avoid redundancy and to set the model to evaluation mode for inference.](https://kodekloud.com/kk-media/image/upload/v1752883265/notes-assets/images/PyTorch-Introduction-to-Flask/model-preparation-best-practices.jpg)
</Frame>

2. **Efficient Endpoint Design:**
   * Design clear and descriptive API endpoints.
   * Validate incoming data to meet model requirements.

<Frame>
  ![The image is a slide titled "Efficient Endpoint Design" with best practices for API design, including using descriptive endpoints and validating incoming data.](https://kodekloud.com/kk-media/image/upload/v1752883265/notes-assets/images/PyTorch-Introduction-to-Flask/efficient-endpoint-design-api-best-practices.jpg)
</Frame>

3. **Error Handling:**
   * Implement robust error handling to return clear messages and proper HTTP status codes for invalid requests.

4. **Security:**
   * Utilize HTTPS to secure data transmission.
   * Store sensitive details like API keys or credentials in environment variables instead of hard-coding them.

<Frame>
  ![The image is a slide titled "Best Practices" focusing on security, advising to use HTTPS for secure data transmission and to store sensitive information in environment variables.](https://kodekloud.com/kk-media/image/upload/v1752883267/notes-assets/images/PyTorch-Introduction-to-Flask/best-practices-security-https-env-vars.jpg)
</Frame>

5. **Monitoring and Logging:**
   * Log API usage, errors, and inference times to facilitate troubleshooting.
   * Consider implementing a health endpoint to continuously monitor application status.

These practices can help maintain a highly efficient, secure, and reliable Flask application.

## Summary

In summary, this article covered:

* An introduction to Flask and its benefits for deploying PyTorch models.
* Steps to install Flask and organize your project structure.
* How to integrate a PyTorch model and create an inference API endpoint.
* Instructions for running your application using Flask’s built-in server and deploying it with Gunicorn.
* Best practices for efficient model preparation, API design, error handling, security, and monitoring.

Let’s now move on to demoing a Flask application designed to serve a PyTorch model.

<Frame>
  ![The image is a summary slide about Flask, a Python microframework, covering its overview, benefits, setup instructions, and best practices.](https://kodekloud.com/kk-media/image/upload/v1752883268/notes-assets/images/PyTorch-Introduction-to-Flask/flask-python-microframework-summary.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-845c-4cdf-9261-7688050bd96c/lesson/94f6282a-76a1-47f1-a91f-37d38c086dff" />
</CardGroup>


# Building Data

Source: https://notes.kodekloud.com/docs/PyTorch/Working-with-Data/Building-Data/page

This article explains how to build custom data for training a model using PyTorch, covering data splitting, cleaning, versioning, and creating data transforms and loaders.

In this lesson, we explain how to build custom data for training a model using PyTorch. We cover data splitting, cleaning, versioning, and creating data transforms and loaders in a clear, step-by-step manner.

## Data Splitting

Data splitting divides your dataset into training, validation, and testing subsets. This is essential for ensuring that your model generalizes well and that performance metrics are reliable. For instance, you might use a 70/15/15 ratio for training, validation, and testing respectively, although you can adjust these percentages to meet your project requirements.

<Frame>
  ![The image illustrates data splitting for machine learning, showing percentages for training (70%), validation (15%), and testing (15%) datasets. Each section is described with its purpose: teaching the model, fine-tuning, and measuring final performance.](https://kodekloud.com/kk-media/image/upload/v1752883269/notes-assets/images/PyTorch-Building-Data/data-splitting-machine-learning-diagram.jpg)
</Frame>

PyTorch's `RandomSplit` utility from the `torch.utils.data` module can help automate this process by randomly dividing the dataset into the desired sizes. Here’s an example:

```python theme={null}
from torch.utils.data import random_split
