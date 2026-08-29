# Import PyTorch vision models
from torchvision import models

# List available models and print the count
print(models.list_models())
print(f"Number available: {len(models.list_models())}")

# Load a pre-trained VGG19 model (old API)
model = models.vgg19(pretrained=True)

# Load with weights argument (new API)
model = models.vgg19(weights=models.VGG19_Weights.DEFAULT)

# Display the model parameters
print(model.state_dict())
```

As demonstrated, the models module downloads the required weights to your local directory. The updated API offers the flexibility of choosing specific pre-trained weights for your models.

──────────────────────────────

## Modifying the Model Output

Pre-trained models are typically configured for 1,000 classes. When working on a custom task with a different number of classes, you must adjust the output layer accordingly. The following example shows how to modify the final classifier layer of the VGG19 model to output 20 classes:

```python theme={null}
# Display the classifier layers
print(model.classifier)

import torch.nn as nn

# Modify the output layer (for 20 classes)
model.classifier[6] = nn.Linear(4096, 20)

# Verify the updated classifier
print(model.classifier)
```

<Callout icon="lightbulb">
  Modifying the output layer is crucial for adapting a pre-trained model to new tasks and datasets.
</Callout>

──────────────────────────────

## Using the PyTorch Hub to Share and Load Models

The PyTorch Hub provides a seamless way to list, download, and share models from GitHub repositories. It also supports loading pre-trained weights effortlessly. For instance, the following snippet demonstrates how to list available models from the PyTorch Vision repository on GitHub:

```python theme={null}
from torch import hub

# List models from a specific version of torchvision (v0.10.0)
hub.list('pytorch/vision:v0.10.0')
```

Similarly, to explore models like YOLOv5 from Ultralytics:

```python theme={null}
# List available YOLOv5 models
hub.list('ultralytics/yolov5')
```

To load a model from the hub, you can use the code below:

```python theme={null}
from torch import hub

# Load the YOLOv5s model
model = hub.load('ultralytics/yolov5', 'yolov5s')

# Provide a batch of images for inference
imgs = ['cat1.jpg', 'zidane.jpg']
results = model(imgs)

# Print the inference results
results.print()
```

Additionally, here’s how to load a ResNet-50 model with pre-trained weights from the PyTorch Vision GitHub repository:

```python theme={null}
# Load model weights and the model using the hub
weights = hub.load("pytorch/vision", "get_model_weights", name="resnet50")
model = hub.load("pytorch/vision", "resnet50", weights=weights.DEFAULT)
```

──────────────────────────────

## Sharing Your Own Model via PyTorch Hub

You can easily share your custom models using a GitHub repository by including a hub configuration file (typically named `hub-conf.py`). This file defines dependencies, model URLs, and entry points. Below is an excerpt from a typical `hub-conf.py` that specifies a simple neural network model called FakeNet:

```python theme={null}
# Define dependencies
dependencies = ['torch']
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.hub import load_state_dict_from_url

# Dictionary mapping model names to URLs containing the state dict
models_url = {
    'fake_model': 'https://github.[AWS_SECRET_ACCESS_KEY]main/section_3/demos/030-105-additional-training-methods/model_state_dict'
}

# Define the model class
class FakeNet(nn.Module):
    def __init__(self):
        super(FakeNet, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.batch_norm = nn.BatchNorm1d(50)
        self.fc2 = nn.Linear(50, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.batch_norm(x)
        x = self.fc2(x)
        return x

# Entry point for the fake_model
def fake_model(pretrained=False, **kwargs):
    """
    FakeNet model
    pretrained (bool): Load pretrained weights if True.
    """
    model = FakeNet(**kwargs)
    if pretrained:
        model.load_state_dict(load_state_dict_from_url(models_url['fake_model'], progress=True))
    return model
```

Once hosted on GitHub, users can load your model with the following code:

```python theme={null}
import torch

# Load the fake_model with pretrained parameters
model = torch.hub.load('kodekloudhub/PyTorch', 'fake_model', pretrained=True)
print(model.state_dict())

# List available models in the repo and get help about the fake_model
print(torch.hub.list('kodekloudhub/PyTorch'))
torch.hub.help('kodekloudhub/PyTorch', 'fake_model')
```

To load the model without pre-trained weights and modify it for a custom task:

```python theme={null}
import torch

model = torch.hub.load('kodekloudhub/PyTorch', 'fake_model', pretrained=False)
print(model)

# Modify the network output to have two outputs instead of one
import torch.nn as nn
model.fc2 = nn.Linear(50, 2)
print(model)
```

──────────────────────────────

## Learning Rate Schedulers

Learning rate schedulers are pivotal in adjusting the learning rate during training, ensuring efficient convergence and preventing overshooting. PyTorch optimizers support several schedulers. Here are some examples:

```python theme={null}
import torch.optim as optim

# Define an optimizer for the model parameters
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Create a StepLR scheduler: reduce the learning rate by 0.1 every 5 epochs
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

# Create an ExponentialLR scheduler: decay the learning rate by multiplying with 0.1 every epoch
scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.1, last_epoch=-1)

# Create a ReduceLROnPlateau scheduler: reduce LR by 0.1 if no improvement for 2 epochs
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2)

# Print the scheduler state
print(scheduler.state_dict())
```

Each scheduler has a specific use case. For example, StepLR decreases the learning rate at fixed intervals, while ReduceLROnPlateau monitors a validation metric and adjusts the learning rate when performance stalls.

──────────────────────────────

## Transfer Learning and Fine-tuning the Final Layer

Transfer learning allows you to leverage pre-trained models and fine-tune just the final layers for a specific task. This section illustrates how to adapt the VGG19 model for a 10-class problem using the CIFAR10 dataset. We begin by preparing the dataset and updating the model's output layer.

### Prepare the Dataset and Update the Model

Using image transformations and the CIFAR10 dataset (which includes classes like plane, car, bird, cat, deer, dog, frog, horse, ship, and truck), we update the classifier for our custom task:

```python theme={null}
import torch
import torchvision.transforms.v2 as v2
from torchvision import datasets

transform = v2.Compose([
    v2.RandomHorizontalFlip(),
    v2.ToImage(),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Important normalization
])

# CIFAR10 dataset
trainset = datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4, shuffle=True, num_workers=1)

import torch.nn as nn
from torchvision import models

# Load VGG19 with default weights
model = models.vgg19(weights=models.VGG19_Weights.DEFAULT)

# Update the final classifier layer for 10 classes
model.classifier[-1] = nn.Linear(4096, 10)
```

### Freezing and Unfreezing Layers

For effective feature extraction, freeze all layers except the final classifier. This ensures that during training, only the last layer's parameters are updated.

```python theme={null}
# Freeze all layers
for param in model.parameters():
    param.requires_grad = False

# Unfreeze only the final classifier layer
for param in model.classifier[-1].parameters():
    param.requires_grad = True

# Verify which layers are trainable
for name, param in model.named_parameters():
    print(f"Layer: {name}, requires_grad: {param.requires_grad}")
```

<Callout icon="lightbulb">
  Freezing layers prevents the alteration of pre-trained features, speeding up training when adapting models to new tasks.
</Callout>

### Training Loop with a Learning Rate Scheduler

The training loop below defines a loss function, optimizer (limited to the final classifier), and a learning rate scheduler. It also saves checkpoints periodically, including the state of the optimizer and scheduler.

```python theme={null}
import torch.optim as optim

# Define loss, optimizer, and scheduler
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.classifier[-1].parameters(), lr=0.001, momentum=0.9)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.1)

N_EPOCHS = 10
for epoch in range(N_EPOCHS):
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data
        
        # Zero the gradients
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    # Print the average loss for this epoch
    print(f"Epoch: {epoch} Loss: {running_loss / len(trainloader):.4f}")

    # Step the scheduler at the end of the epoch
    scheduler.step()

    # Save a checkpoint every 2 epochs
    if epoch % 2 == 0:
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'scheduler_state_dict': scheduler.state_dict(),
            'loss': loss,
        }, f'training_checkpoint_{epoch}.tar')

# Save the final checkpoint after the last epoch
torch.save({
    'epoch': N_EPOCHS,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'scheduler_state_dict': scheduler.state_dict(),
    'loss': loss,
}, 'training_checkpoint_final.tar')
```

This training approach demonstrates effective feature extraction by fine-tuning only the final layer over 10 epochs while preserving the state of training through periodic checkpointing.

──────────────────────────────

## Conclusion

In this article, we explored several advanced training techniques in PyTorch. We covered the process of loading and modifying pre-trained models, using PyTorch Hub for model sharing, setting up various learning rate schedulers, and implementing transfer learning by fine-tuning the model's final layer. These methodologies not only boost model performance but also streamline the training process. Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-a284-41d1-8469-7e60705bbab8/lesson/a25a1e8e-b979-44aa-8664-874046ddcb77" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-a284-41d1-8469-7e60705bbab8/lesson/4c364708-8045-4d80-9e1b-a22cbdd8dba6" />
</CardGroup>


# Demo Building and Training a model

Source: https://notes.kodekloud.com/docs/PyTorch/Building-and-Training-Models/Demo-Building-and-Training-a-model/page

This guide explores building and training a machine learning model using a simple neural network with PyTorch.

Congratulations on reaching this point! In this guide, we will explore how to build and train a machine learning model by constructing a simple neural network using PyTorch. We will cover the following topics:

* Building a neural network with PyTorch
* Passing data through network layers and observing changes in tensor dimensions
* Demonstrating the effect of ReLU activation
* Executing a full forward pass
* Inspecting model parameters
* Setting up loss functions and optimizers
* Preparing datasets and dataloaders
* Creating an image classification network
* Implementing training and validation loops

Let's dive in!

***

## Building a Simple Neural Network in PyTorch

In PyTorch, you can construct a neural network by defining a class that inherits from `nn.Module`. Typically, this class includes an `__init__` method to define the layers and a `forward` method that outlines how data flows through these layers.

Below is an example of a simple neural network class, `SimpleNeuralNetwork`. This model contains an input layer, a hidden layer, and an output layer, all implemented as linear layers. To introduce non-linearity, a ReLU activation is applied after the input and hidden layers.

```python theme={null}
import torch
import torch.nn as nn
