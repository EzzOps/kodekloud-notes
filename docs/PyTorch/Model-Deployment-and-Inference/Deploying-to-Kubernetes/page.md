# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables or secrets
MY_SECRET = os.getenv('SECRET')

# Load the MobileNetV3 Large pre-trained model before starting the app
try:
    logger.info("Loading MobileNetV3 Large pre-trained model...")
    model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT)
    model.eval()  # Switch to evaluation mode
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise RuntimeError("Failed to load the model.") from e
```

<Callout icon="lightbulb">
  Make sure that all required modules are imported and logging is correctly configured. The model must be loaded before any request is processed to avoid runtime errors.
</Callout>

***

## Creating Endpoints

### Prediction Endpoint

The `/predict` endpoint handles POST requests. It accepts a JSON payload that contains an image encoded in Base64. This endpoint decodes the image, preprocesses it, performs inference using the model, and returns the prediction in JSON format.

```python theme={null}
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract Base64 string from the incoming JSON request
        data = request.json
        if not data or 'image' not in data:
            logger.warning("No image provided in the request.")
            return jsonify({'error': 'No image provided'}), 400

        # Decode the Base64 image string
        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Preprocess the image and add the batch dimension if required
        transformed_img = preprocess(image).unsqueeze(0)

        # Perform inference in a no_grad context to save memory
        with torch.no_grad():
            logger.info("Performing inference...")
            output = model(transformed_img)
            _, predicted = torch.max(output.data, 1)
            logger.info(f"Inference complete. Predicted class: {predicted.item()}")

        # Return the prediction as a JSON response
        response = {'prediction': predicted.item()}
        logger.info(f"Response for /predict: {response}")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        response = {'error': str(e)}
        logger.info(f"Response for /predict: {response}")
        return jsonify(response), 500
```

This endpoint performs the following steps:

* Parses the request payload and verifies the presence of an `"image"` key.
* Decodes the Base64-encoded image and converts it into an RGB image.
* Applies image preprocessing before passing the tensor to the model.
* Retrieves and returns the prediction using Flask’s `jsonify` method.

### Health Endpoint

The `/health` endpoint is a simple GET endpoint used to verify that the server is running correctly. It returns a JSON response with a health status.

```python theme={null}
@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint to confirm the app is running.
    """
    response = {'status': 'healthy'}
    logger.info(f"Response for /health: {response}")
    return jsonify(response), 200
```

***

## Testing the Flask Application

### Running the App Directly

To start the Flask application, run the following command from your terminal:

```bash theme={null}
python app.py
```

This command initializes the app, loads the model, and starts a development server, typically accessible at `http://127.0.0.1:5000`.

Example terminal output:

```bash theme={null}
root@pytorch demos/040-040-introduction-to-flask/flask_app on  [] main [!?] via 🐍 v3.11.4 (venv) → python app.py
2025-01-15 01:36:46,774 - INFO - Loading MobileNetV3 Large pre-trained model...
2025-01-15 01:36:46,912 - INFO - Model loaded successfully.
* Serving Flask app 'app'
* Debug mode: on
2025-01-15 01:36:46,919 - INFO - WARNING: This is a development server. Do not use it in a production deployment.
* Running on http://127.0.0.1:5000
2025-01-15 01:36:46,919 - INFO - Press CTRL+C to quit
```

<Callout icon="triangle-alert">
  Do not use the Flask development server in a production environment. For production deployments, consider using a WSGI server such as Gunicorn.
</Callout>

### Sending Test Requests

You can use the Python `requests` library to test your endpoints. Begin by creating a Base64-encoded string from an image (for example, "dog-1.jpg"):

```python theme={null}
import base64

with open('dog-1.jpg', 'rb') as img_file:
    base64_string = base64.b64encode(img_file.read()).decode('utf-8')
print(base64_string)
```

Next, test the prediction endpoint:

```python theme={null}
import requests

# JSON payload containing the Base64 encoded image
payload = {
    "image": base64_string
}

# Set the appropriate headers
headers = {
    "Content-Type": "application/json"
}

# Send a POST request to the /predict endpoint
response = requests.post("http://127.0.0.1:5000/predict",
                         json=payload,
                         headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())

# Verify the /health endpoint
health_response = requests.get("http://127.0.0.1:5000/health")
print("Health Status Code:", health_response.status_code)
print("Health Response JSON:", health_response.json())
```

A successful prediction response might look like:

```plaintext theme={null}
Status Code: 200
Response JSON: {'prediction': 207}
```

And the health check output:

```plaintext theme={null}
Health Status Code: 200
Health Response JSON: {'status': 'healthy'}
```

### Testing Error Handling

Test error handling by sending requests without the required payload or using an incorrect key:

```python theme={null}
# Test without sending any payload
error_response = requests.post("http://127.0.0.1:5000/predict", headers=headers)
print("Status Code:", error_response.status_code)
print("Response JSON:", error_response.json())

# Test with an incorrectly formatted payload
error_response = requests.post("http://127.0.0.1:5000/predict",
                               json={"video": base64_string},
                               headers=headers)
print("Status Code:", error_response.status_code)
print("Response JSON:", error_response.json())
```

The first case should return a 500 error (e.g., failure to decode JSON), while the second returns a 400 status with a message indicating that no image was provided.

***

## Running the App with Gunicorn

For production deployments, use a robust WSGI server like Gunicorn. Start the Gunicorn server with the following command:

```bash theme={null}
gunicorn -w 2 -b 0.0.0.0:8080 app:app
```

Test the application on port 8080:

```python theme={null}
# Send a POST request using Gunicorn on port 8080
response = requests.post("http://127.0.0.1:8080/predict",
                         json=payload,
                         headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
```

Terminal logs should display messages similar to:

```plaintext theme={null}
2025-01-15 01:36:46,774 - INFO - Loading MobileNetV3 Large pre-trained model...
2025-01-15 01:36:46,912 - INFO - Model loaded successfully.
...
2025-01-15 01:36:49,478 - INFO - * Debugger PIN: 808-753-342
2025-01-15 01:39:17,671 - INFO - Response for /predict: {'prediction': 207}
```

***

## Interpreting the Model Prediction

To convert the numeric prediction (e.g., 207) into a human-readable class label, use a mapping file (labels.json) available from Hugging Face. The labels file can be downloaded from:

[Imagenet 1K Labels](https://huggingface.co/datasets/huggingface/label-files/blob/main/imagenet-1k-id2label.json)

After downloading the file, use the following code to interpret the prediction:

```python theme={null}
import json

with open("labels.json", "r") as f:
    imagenet_classes = json.load(f)

# Retrieve the class name for the predicted class
class_label = imagenet_classes['207']
print(class_label)
```

If, for instance, the prediction corresponds to a golden retriever, the output should confirm the image class as "golden retriever"—an ideal match if your input image depicts a golden retriever puppy.

***

This concludes our introduction to Flask and model deployment. With Flask, you can quickly set up HTTP endpoints to serve machine learning models, complete with robust error handling and logging. Happy coding!

## Additional Resources

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Gunicorn Documentation](https://docs.gunicorn.org/)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-845c-4cdf-9261-7688050bd96c/lesson/02473255-a571-4ed3-8795-84db13733d23" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-845c-4cdf-9261-7688050bd96c/lesson/c6f37a93-7ced-4b01-b1d3-de98ad5bef74" />
</CardGroup>


# Deploying to Kubernetes

Source: https://notes.kodekloud.com/docs/PyTorch/Model-Deployment-and-Inference/Deploying-to-Kubernetes/page

This guide explores the advantages and best practices of deploying machine learning models using Kubernetes.

Kubernetes has rapidly become the de facto standard for deploying scalable, resilient applications, including machine learning (ML) models. Its robust architecture, which has scaled the internet among other applications, now plays a critical role in modern AI/ML initiatives.

<Frame>
  ![The image illustrates Kubernetes as a central component, highlighting its features such as seamless deployment, AI/ML support, and scalable architecture.](https://kodekloud.com/kk-media/image/upload/v1752883212/notes-assets/images/PyTorch-Deploying-to-Kubernetes/kubernetes-features-deployment-ai-ml.jpg)
</Frame>

In this guide, we explore why Kubernetes is ideal for model deployment. We assume you already have a basic understanding of Kubernetes, so our focus will be on its advantages and best practices for deploying ML models rather than a comprehensive platform overview.

We'll start by discussing the key benefits of using Kubernetes for model deployment. Then, we demonstrate how to leverage Kubernetes to handle specialized workloads, outline the complete deployment workflow for ML models, share best practices, and review popular ML serving frameworks.

<Frame>
  ![The image shows an agenda for a presentation on Kubernetes, covering topics like its role in model deployment, key benefits, specialized workloads, deployment workflow, best practices, and ML serving frameworks.](https://kodekloud.com/kk-media/image/upload/v1752883213/notes-assets/images/PyTorch-Deploying-to-Kubernetes/kubernetes-presentation-agenda-topics.jpg)
</Frame>

## What is Kubernetes?

Kubernetes is an open-source platform for automating the deployment, scaling, and management of containerized applications.

<Frame>
  ![The image is a slide titled "Kubernetes for Model Deployment" featuring the Kubernetes logo and a description of it as an open-source platform for automating deployment, scaling, and management of containerized applications.](https://kodekloud.com/kk-media/image/upload/v1752883214/notes-assets/images/PyTorch-Deploying-to-Kubernetes/kubernetes-model-deployment-slide.jpg)
</Frame>

Rather than rehash its general capabilities, let’s dive into why Kubernetes is particularly well-suited for ML model deployment.

## Why Use Kubernetes for Model Deployment?

Kubernetes offers several compelling benefits when deploying machine learning models:

* **High-Volume Request Handling:** Designed to manage a high volume of simultaneous requests, making it ideal for production environments where model traffic can fluctuate.
* **Seamless Scalability:** Its inherent scalability allows your application to grow without requiring extensive modifications to your deployment configuration.
* **Efficient Resource Utilization:** Kubernetes optimally allocates limited resources like GPUs, ensuring cost-effective operations for resource-heavy AI workloads.
* **Versatile Deployment Scenarios:** Whether deploying for real-time data inference or batch processing of historical data, Kubernetes adapts easily to various deployment scenarios.
* **Automated Resource Management:** It automates critical processes such as scaling during peak demand and adjusting resources during low-demand periods, while continuously monitoring system health for high availability and reliability.

Overall, Kubernetes streamlines the complex process of deploying and managing ML models, making it a powerful tool for modern AI applications.

## Handling Specialized Workloads

ML and AI tasks often require specific hardware configurations. Kubernetes enables precise resource allocation and workload scheduling by using node affinity, node selectors, taints & tolerations, and resource requests and limits.

### Node Affinity

Node affinity allows you to define which nodes should execute particular workloads. For instance, if a node is labeled with `gpu=true`, you can ensure that your ML tasks run specifically on these GPU-enabled nodes.

<Frame>
  ![The image is a slide titled "Specialized Workloads" focusing on "Node Affinity," explaining how to define node preferences for pods using labels and affinity rules, with an example of assigning GPU nodes for model inference tasks.](https://kodekloud.com/kk-media/image/upload/v1752883215/notes-assets/images/PyTorch-Deploying-to-Kubernetes/specialized-workloads-node-affinity.jpg)
</Frame>

Below is an example deployment manifest that uses node affinity to target nodes labeled with `gpu="true"`:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpu-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gpu-app
  template:
    metadata:
      labels:
        app: gpu-app
    spec:
      containers:
        - name: gpu-container
          image: my-ml-model:latest
      affinity:
        nodeAffinity:
          [SECRET_REDACTED]:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: gpu
                    operator: In
                    values:
                      - "true"
```

### Node Selector

Alternatively, you can use a node selector to ensure pods are scheduled on nodes with a specific label. Consider the following example, where pods are assigned to nodes labeled `cpu=high-performance`:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cpu-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cpu-app
  template:
    metadata:
      labels:
        app: cpu-app
    spec:
      nodeSelector:
        cpu: "high-performance"
      containers:
        - name: cpu-container
          image: my-cpu-intensive-app:latest
```

### Taints and Tolerations

Taints prevent pods from being scheduled on certain nodes unless they expressly tolerate them. This is useful for dedicating nodes exclusively to ML workloads.

<Frame>
  ![The image is a slide titled "Specialized Workloads" discussing "Taints and Tolerations" in Kubernetes, explaining how to prevent general-purpose pods from running on specialized nodes, with an example of allowing only ML-specific pods on GPU-enabled nodes.](https://kodekloud.com/kk-media/image/upload/v1752883216/notes-assets/images/PyTorch-Deploying-to-Kubernetes/specialized-workloads-taints-tolerations.jpg)
</Frame>

First, taint the node using the following command:

```bash theme={null}
