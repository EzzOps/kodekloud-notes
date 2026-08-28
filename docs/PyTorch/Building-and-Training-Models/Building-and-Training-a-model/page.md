# Load parameters from pre-trained models
resnet18 = models.resnet18(pretrained=True)
alexnet = models.alexnet(pretrained=True)
squeezenet = models.squeezenet1_0(pretrained=True)
vgg16 = models.vgg16(pretrained=True)
densenet = models.densenet161(pretrained=True)
inception = models.inception_v3(pretrained=True)
googlenet = models.googlenet(pretrained=True)
shufflenet = models.shufflenet_v2_x1_0(pretrained=True)
mobilenet_v2 = models.mobilenet_v2(pretrained=True)
mobilenet_v3_large = models.mobilenet_v3_large(pretrained=True)
mobilenet_v3_small = models.mobilenet_v3_small(pretrained=True)
resnext50_32x4d = models.resnext50_32x4d(pretrained=True)
wide_resnet50_2 = models.wide_resnet50_2(pretrained=True)
mnasnet = models.mnasnet1_0(pretrained=True)
```

### Modifying a Pre-Trained Model

The example below demonstrates how to adapt a pre-trained ResNet-18 model for a new task involving 10 output classes:

```python theme={null}
import torch.nn as nn
import torchvision.models as models

# Load the pre-trained ResNet-18 model
model = models.resnet18(pretrained=True)

# Get the number of features in the last fully connected layer
num_ftrs = model.fc.in_features

# Replace the fully connected layer for a new task with 10 classes
model.fc = nn.Linear(num_ftrs, 10)
```

Here, the final fully connected layer is replaced with a new one that outputs predictions for 10 classes. The number of input features is obtained from the original model's configuration.

<Callout icon="lightbulb">
  When modifying pre-trained models, remember to adjust the network's final layer to match the number of classes in your new task.
</Callout>

## PyTorch Hub

PyTorch Hub is a community-driven platform that provides access to a wide range of pre-trained models. It simplifies the process of exploring, downloading, and sharing models contributed by researchers around the world.

<Frame>
  ![The image shows a webpage from PyTorch Hub, highlighting its offering of a variety of pre-trained models for researchers.](https://kodekloud.com/kk-media/image/upload/v1752883119/notes-assets/images/PyTorch-Additional-Training-Methods/pytorch-hub-pretrained-models.jpg)
</Frame>

To browse available models, use the `torch.hub.list` function by specifying the GitHub repository. For example, to list vision models from the PyTorch/vision repository, execute:

```plaintext theme={null}
# List vision models available from the PyTorch/vision repository
torch.hub.list('pytorch/vision')
Downloading: "https://github.com/pytorch/vision/zipball/main" to .cache/torch/hub/main.zip
['alexnet', 'convnext_base', 'convnext_large', 'convnext_small', 'convnext_tiny',
 'deeplabv3_mobilenet_v3_large', 'deeplabv3_resnet50',
 'densenet121', 'densenet161', 'densenet169', 'densenet201', 'efficientnet_b0',
 'efficientnet_b1', 'efficientnet_b2', 'efficientnet_b3', 'efficientnet_b4',
 'efficientnet_b5', 'efficientnet_b6', 'efficientnet_b7', 'efficientnet_v2_l',
 'efficientnet_v2_m', 'efficientnet_v2_s', 'fcn_resnet101', 'fcn_resnet50',
 'get_model_weights', 'get_weight', 'googlenet', 'inception_v3',
 'lrappt_mobilenet_v3_large', 'maxvit_t', 'mc3_18', 'mnasnet0_5', 'mnasnet0_75',
 'mnasnet1_0', 'mnasnet1_3', 'mobilenet_v2', 'mobilenet_v3_large',
 'mobilenet_v3_small', 'mvit_v1_b', 'mvit_v2_s', 'r2plus1d_18', 'r3d_18',
 'raft_large', 'raft_small', 'regnet_x_16gf', 'regnet_x_1_6gf', 'regnet_x_32gf']
```

After identifying the desired model, load it using the `torch.hub.load` function. For example, to load the pre-trained VGG-16 model:

```python theme={null}
import torch

# Load pre-trained VGG-16 model
model = torch.hub.load('pytorch/vision', 'vgg16')
print(model)
```

PyTorch Hub also enables model deployment by facilitating model sharing. To share your model, create a file named `hubconf.py` in your repository. This file defines the entry point for your model. The following example illustrates how to set up a `hubconf.py` for a ResNet-18 model:

```python theme={null}
dependencies = ['torch']
from torchvision.models.resnet import resnet18 as resnet

def model(pretrained=False, **kwargs):
    """ResNet-18 model
    pretrained (bool): Load pretrained weights if True.
    """
    # Initialize the model with optional pretrained weights
    model = resnet(pretrained=pretrained, **kwargs)
    if pretrained:
        checkpoint = 'https://model-url.pth'
        state_dict = torch.hub.load_state_dict_from_url(checkpoint, progress=False)
        model.load_state_dict(state_dict)
    return model
```

Users can then load the shared model using:

```python theme={null}
# Load the model from a GitHub repository
model = torch.hub.load('username/repo_name', 'model', pretrained=True)
```

## Learning Rate Schedulers

Learning rate schedulers play a crucial role in training by adjusting the learning rate throughout the training process. This dynamic adjustment ensures that the model takes larger steps in the early stages and fine-tuned adjustments later, preventing issues like overshooting optimal parameters.

<Frame>
  ![The image explains the benefits of learning rate schedulers in model training, highlighting improved model convergence, prevention of overshooting, and faster convergence.](https://kodekloud.com/kk-media/image/upload/v1752883120/notes-assets/images/PyTorch-Additional-Training-Methods/learning-rate-schedulers-benefits.jpg)
</Frame>

PyTorch provides several built-in learning rate schedulers:

* **StepLR:** Decreases the learning rate by a fixed factor (gamma) after a set number of epochs.
* **ExponentialLR:** Applies an exponential decay to the learning rate.
* **ReduceLROnPlateau:** Lowers the learning rate when performance metrics stagnate.

<Frame>
  ![The image describes three common learning rate schedulers: StepLR, ExponentialLR, and ReduceLROnPlateau, each with a brief explanation of their function.](https://kodekloud.com/kk-media/image/upload/v1752883121/notes-assets/images/PyTorch-Additional-Training-Methods/learning-rate-schedulers-step-exponential-reduce.jpg)
</Frame>

To integrate a learning rate scheduler into your training loop, first define an optimizer, then configure the scheduler, and finally update it at the end of each epoch. For instance, to use a StepLR scheduler with an SGD optimizer:

```python theme={null}
import torch.optim as optim

# Define the optimizer with an initial learning rate
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Configure the StepLR scheduler to decay the learning rate every 10 epochs by a factor of 0.1
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

# Training loop
for epoch in range(50):
    # Insert your training logic here
    # ...

    # Update the learning rate at the end of the epoch
    scheduler.step()
```

## Summary

In summary, this article has covered several advanced training methods in PyTorch:

* **Transfer Learning:** Utilize pre-trained models to achieve faster convergence and reduce training time.
* **PyTorch Hub:** Access and share a wide range of pre-trained models through a community-driven platform.
* **Learning Rate Schedulers:** Dynamically adjust learning rates during training to avoid overshooting and ensure efficient convergence.

<Frame>
  ![The image is a summary slide listing five key points about PyTorch, including training methods, transfer learning, PyTorch Hub, learning rate schedulers, and specific schedulers like StepLR and ExponentialLR.](https://kodekloud.com/kk-media/image/upload/v1752883122/notes-assets/images/PyTorch-Additional-Training-Methods/pytorch-summary-training-methods-schedulers.jpg)
</Frame>

These techniques are invaluable for building complex models with enhanced accuracy and efficiency. Next, let's move on to the demonstration section to see these methods in action.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/b8cb82ae-a284-41d1-8469-7e60705bbab8/lesson/090bd418-7634-499a-bfd2-bf8bee0a8c46" />
</CardGroup>


# Building and Training a model

Source: https://notes.kodekloud.com/docs/PyTorch/Building-and-Training-Models/Building-and-Training-a-model/page

This article guides on building and training a neural network model using PyTorch, covering model definition, parameters, loss functions, optimizers, and effective training techniques.

Now that we have an understanding of neural networks and their role in PyTorch, we will walk through building and training a neural network model. In this guide, we cover how to define a neural network using PyTorch, explore model parameters, loss functions, and optimizers, and learn how to train your model effectively.

This is an exciting section where theory meets hands-on implementation.

***

## What Is a Model?

A model can be thought of as a blueprint or recipe that makes predictions based on input data. A popular type of model is a neural network, inspired by the human brain's structure and function.

<Frame>
  ![The image is a diagram titled "What Is a Model?" showing three sections labeled Blueprint, Recipe, and Instruction, with "Model" at the center.](https://kodekloud.com/kk-media/image/upload/v1752883123/notes-assets/images/PyTorch-Building-and-Training-a-model/what-is-a-model-diagram.jpg)
</Frame>

A neural network is composed of layers of neurons, which work together to learn patterns in data. In PyTorch, you create a structure where input data passes through these layers and produces an output—such as identifying objects in an image.

<Frame>
  ![The image shows a diagram of a neural network model with an input layer, hidden layers, and an output layer, connected by lines representing the flow of information.](https://kodekloud.com/kk-media/image/upload/v1752883124/notes-assets/images/PyTorch-Building-and-Training-a-model/neural-network-model-diagram.jpg)
</Frame>

PyTorch streamlines model creation by providing essential tools to define and link layers.

***

## Defining a Neural Network Model in PyTorch

To build a neural network in PyTorch, you create a class that inherits from `torch.nn.Module`. This class serves as a blueprint that defines the layers and the flow of data through them.

Below is an example of a simple neural network class:

```python theme={null}
import torch
import torch.nn as nn
