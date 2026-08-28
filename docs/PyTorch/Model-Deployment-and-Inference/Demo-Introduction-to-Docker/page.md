# Install the required modules
!pip install onnx onnxruntime
```

Console output:

```plaintext theme={null}
Requirement already satisfied: onnx in /root/venv/lib/python3.11/site-packages (1.17.0)
Requirement already satisfied: onnxruntime in /root/venv/lib/python3.11/site-packages (1.20.1)
Requirement already satisfied: numpy>=1.20 in /root/venv/lib/python3.11/site-packages (from onnx) (2.1.1)
Requirement already satisfied: protobuf>=3.20.2 in /root/venv/lib/python3.11/site-packages (from onnx) (5.29.3)
Requirement already satisfied: coloredlogs in /root/venv/lib/python3.11/site-packages (from onnxruntime) (15.0.1)
Requirement already satisfied: flatbuffers in /root/venv/lib/python3.11/site-packages (from onnxruntime) (24.12.23)
Requirement already satisfied: packaging in /root/venv/lib/python3.11/site-packages (from onnxruntime) (24.2)
Requirement already satisfied: sympy in /root/venv/lib/python3.11/site-packages (from onnxruntime) (1.13.3)
Requirement already satisfied: humanfriendly>=9.1 in /root/venv/lib/python3.11/site-packages (from coloredlogs->onnxruntime) (10.0)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in /root/venv/lib/python3.11/site-packages (from sympy->onnxruntime) (1.3.0)
```

Since all packages are present, we can proceed with the demonstration.

***

## Loading and Modifying the Model

In this section, we import the necessary modules from PyTorch and TorchVision to load and modify a MobileNet V3 Large model. After loading the model with pretrained weights, we adjust the classifier's final layer to output two classes. We then load a checkpoint to restore the model's state.

```python theme={null}
# Import modules
import torch
import torch.nn as nn
from torchvision import models

# Load the mobilenet_v3_large model with default weights
model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT)

# Modify the last layer for 2 output classes
model.classifier[-1] = nn.Linear(1280, 2)

# Load the model from checkpoint
checkpoint = torch.load('mobilenet_checkpoint.tar', weights_only=True)
```

Next, we load the state from the checkpoint into the model:

```python theme={null}
# Load the parameters from the checkpoint
model.load_state_dict(checkpoint['model_state_dict'])
```

These steps ensure that MobileNet V3 is updated for our classification task with two classes and that the weights are successfully restored.

***

## Exporting the Model to ONNX

PyTorch offers built-in support to export models to the ONNX format. By using the export function, we define the model's input signature and create an ONNX file. Start by displaying the documentation for torch.onnx.export for available options:

```python theme={null}
# Import the ONNX export module from PyTorch
import torch.onnx

# Display documentation for torch.onnx.export to see available options
help(torch.onnx.export)

# Create an example input tensor
example_input = torch.randn(1, 3, 224, 224)

# Export the model to an ONNX file
torch.onnx.export(model, example_input, "image_classifier.onnx")
```

After exporting, verify the correctness of the model by loading and checking the ONNX file:

```python theme={null}
import onnx

# Load the exported ONNX model
onnx_model = onnx.load("image_classifier.onnx")

# Check the model consistency
print(onnx.checker.check_model(onnx_model))
```

The export process leverages a dummy input to define the model's signature and generates the "image\_classifier.onnx" file for further use.

***

## Examining the Export Process

For clarity, the following example reiterates the export process: preparing an example input, exporting the model, and verifying the exported ONNX model.

```python theme={null}
# Create an example input
example_input = torch.randn(1, 3, 224, 224)

# Export the model
torch.onnx.export(model, example_input, "image_classifier.onnx")

# Load the model with ONNX and check for consistency
import onnx
onnx_model = onnx.load("image_classifier.onnx")
print(onnx.checker.check_model(onnx_model))
```

This check confirms that the model is export-consistent and ready for deployment.

***

## Preparing an Image for Inference

Before running inference on the ONNX model, the input image must be preprocessed. This involves resizing, normalizing, and converting the image to a tensor using Pillow and TorchVision transformations. The transformed image is then reshaped to include a batch dimension.

```python theme={null}
# Import necessary modules for image processing
from PIL import Image
from torchvision.transforms import v2
import torch

transform = v2.Compose([
    v2.Resize((224, 224)),
    v2.ToImage(),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406],
                 std=[0.229, 0.224, 0.225])
])

# Open the image using Pillow
image_path = 'sample-input.jpg'
image = Image.open(image_path)

# Apply the transformation to the image
transformed_image = transform(image)
print(transformed_image.shape)

# Add batch dimension: [batch_size, channels, height, width]
transformed_image = transformed_image.unsqueeze(0)
print(transformed_image.shape)
```

After transforming the image, convert it into a NumPy array to match the input requirements of ONNX Runtime:

```python theme={null}
import numpy as np

# Convert the transformed image to a NumPy array with type float32
image_np = np.array(transformed_image, dtype=np.float32)
```

***

## Running Inference with ONNX Runtime

With the ONNX model prepared and the input image transformed, we can perform inference using ONNX Runtime. The process involves loading the model, creating an inference session, and using an input dictionary for the session run.

```python theme={null}
# Import ONNX Runtime and load the model
import onnxruntime as ort
import onnx

onnx_model = onnx.load("image_classifier.onnx")

# Start an ONNX inference session
session = ort.InferenceSession("image_classifier.onnx")

# Convert the transformed image to a numpy array (if not already done)
import numpy as np
image_np = np.array(transformed_image, dtype=np.float32)
```

Prepare the input dictionary using the session's first input name and run the inference:

```python theme={null}
# Prepare the input dictionary for the model
inputs = {session.get_inputs()[0].name: image_np}

# Run the inference on the ONNX model
outputs = session.run(None, inputs)
print(outputs)  # Raw outputs (logits) from the final model layer

# Determine the predicted class by identifying the index with the highest logit
predicted = outputs[0][0].argmax(0)
print(predicted)
```

The raw outputs represent logits, and applying argmax on these logits provides the index of the predicted class.

***

## Mapping the Prediction to a Label

To present the inference result in a human-friendly format, we associate the numerical prediction with a corresponding class label. Here, the two classes are defined as "malignant" (0) and "benign" (1).

```python theme={null}
# Get the predicted class index
predicted = outputs[0][0].argmax(0)
print(predicted)

# Define label encoding for the dataset
label_encoding = {"malignant": 0, "benign": 1}

# Create a reverse mapping from indices to labels
index_to_class_map = {v: k for k, v in label_encoding.items()}
print(f"Predicted Class: {index_to_class_map[predicted.item()]}")
```

Console output:

```plaintext theme={null}
Predicted Class: benign
```

This mapping step translates the model’s output into a readable class label.

***

<Frame>
  ![The image shows a Jupyter Notebook interface with Python code related to exporting a model using the torch.onnx.export function. The help documentation for this function is displayed, detailing its usage and arguments.](https://kodekloud.com/kk-media/image/upload/v1752883211/notes-assets/images/PyTorch-Demo-Deployment-Options/jupyter-notebook-torch-export-function.jpg)
</Frame>

***

## Conclusion

In this demo, we explored the end-to-end process of working with ONNX and ONNX Runtime. We covered the following steps:

| Step                            | Description                                                                                     |
| ------------------------------- | ----------------------------------------------------------------------------------------------- |
| Installing Dependencies         | Using pip to install ONNX and ONNX Runtime.                                                     |
| Loading and Modifying the Model | Loading a MobileNet V3 model, adjusting its classifier, and loading a checkpoint.               |
| Exporting to ONNX               | Exporting the model with a sample input and verifying model consistency.                        |
| Preparing Input                 | Preprocessing an image with Pillow and TorchVision transformations.                             |
| Running Inference               | Deploying the ONNX model with ONNX Runtime and determining the predicted class from raw logits. |
| Mapping Predictions             | Converting numerical predictions to human-readable class labels.                                |

<Callout icon="lightbulb">
  This guide provides a solid foundation for integrating ONNX models in a variety of deployment environments. For additional information, explore the [ONNX Documentation](https://onnx.ai/).
</Callout>

Thank you for reading this demonstration on exporting and using ONNX models for inference in real-world applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/a958efa1-845c-4cdf-9261-7688050bd96c/lesson/35e334ea-9ad5-4570-b988-6562dd95a5a8" />
</CardGroup>


# Demo Introduction to Docker

Source: https://notes.kodekloud.com/docs/PyTorch/Model-Deployment-and-Inference/Demo-Introduction-to-Docker/page

This lesson guides you in using Docker to deploy a Flask application, covering installation, image building, container running, and pushing to Docker Hub.

In this lesson, we guide you through using Docker to deploy a Flask application as part of a model deployment process. You will learn how to install Docker on an Ubuntu server, build a container image for your Flask app, verify the installation, run the container, test the application, and finally push the image to Docker Hub.

***

## Installing Docker on Ubuntu

Docker runs on Linux, Windows, and macOS, but in this example we focus on an Ubuntu server. The following instructions are adapted from the official Docker documentation.

<Callout icon="lightbulb">
  Before starting the installation, update your package index to ensure you have the latest information from the repositories.
</Callout>

### Step 1: Prerequisites

Update your package index and install the required packages:

```bash theme={null}
apt-get update
apt-get install ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
```

### Step 2: Add the Docker Repository

Add the Docker repository to your system. This command automatically determines your system’s version codename:

```bash theme={null}
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Step 3: Install Docker Engine

Update the package list again and install the Docker Engine, CLI, containerd, and additional required packages. This process may take a few moments:

```bash theme={null}
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

You should see output similar to the following, indicating that Docker and its dependencies have been installed:

```bash theme={null}
Get:2 https://download.docker.com/linux/ubuntu lunar/stable amd64 Packages [16.1 kB]
Hit:3 http://old-releases.ubuntu.com/ubuntu lunar InRelease
...
Fetched 64.9 kB in 1s (96.1 kB)
...
The following NEW packages will be installed: apparmor, containerd.io, docker-ce, docker-ce-cli, docker-buildx-plugin, docker-compose-plugin, ...
```

After installation, open a terminal to start and enable the Docker service.

***

## Verifying the Docker Installation

To confirm that Docker has been installed correctly, check the version:

```bash theme={null}
docker version
```

Next, run Docker’s official "Hello World" container to verify that both the client and daemon are functioning properly:

```bash theme={null}
docker run hello-world
```

A successful run will produce output like:

```text theme={null}
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c1ec31eb5944: Pull complete
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

***

## Building a Docker Image for the Flask App

This section walks you through containerizing a Flask application by creating a Dockerfile that outlines the necessary build steps.

### Dockerfile Explanation

The Dockerfile below uses a slim official Python image and installs the CPU version of PyTorch to minimize the image size. It then installs Python dependencies, copies your Flask app, and sets up a non-root user for enhanced security.

```dockerfile theme={null}
