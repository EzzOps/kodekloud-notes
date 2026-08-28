# Begin by importing the torch library
import torch

# Helper code to visualize tensors using matplotlib
import matplotlib.pyplot as plt

def visualize_tensor(tensor):
    num_layers = tensor.size(0)  # Number of layers (e.g., 4)
    height, width = tensor.size(1), tensor.size(2)
    
    fig, axes = plt.subplots(1, num_layers, figsize=(15, 5))
    
    if num_layers == 1:
        axes = [axes]
    # Further implementation as shown in Section 1...
```

After installing the Python extension, you have access to various features that streamline development, including debugging, snippet support, and intelligent code completion.

<Frame>
  ![The image shows the Visual Studio Code extensions marketplace with a focus on the Python extension, displaying details such as ratings, installation options, and support information.](https://kodekloud.com/kk-media/image/upload/v1752883173/notes-assets/images/PyTorch-Course-Structure/vscode-python-extension-marketplace.jpg)
</Frame>

***

## Section 3: Configuring Your Environment with Jupyter

To fully leverage Jupyter notebooks within VS Code, install the Jupyter extension from the marketplace. This extension allows you to run notebooks directly in VS Code and easily switch between different kernels to match your environment settings. In this section, you will also learn how to define dependencies and code a simple model class. Consider the following example:

```python theme={null}
# Define dependencies
dependencies = ['torch']
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.hub import load_state_dict_from_url

# Dictionary pointing to the URL of the models
models_url = {
    'fake_model': 'https://github.[AWS_SECRET_ACCESS_KEY]/main/'
}

# Model class definition
class FakeNet(nn.Module):
    def __init__(self):
        super(FakeNet, self).__init__()
        # Initialization code goes here

    def forward(self, x):
        # Define the forward pass
        return x
```

Ensure that you set the notebook kernel to match the environment where your dependencies are installed so that the demos and labs run smoothly.

***

## Section 4: Interactive Labs and Running Commands

The final section of the course introduces interactive labs. Here, you'll alternate between using your IDE and executing commands in the terminal. For instance, you might run a Python script using the terminal as shown below:

```python theme={null}
# Begin by importing the torch library
import torch
```

When you execute your script, you might encounter outputs similar to the following:

```bash theme={null}
/root/venv/bin/python3 /root/PyTorch/hubconf.py
[WARN] - (starship::utils): Executing command "git" timed out.
[WARN] - (starship::utils): You can set command_timeout in your config to a higher value to allow long-running commands to keep executing.
```

A successful run could display output like this:

```bash theme={null}
root@pytorch PyTorch on  🌳 main via 🐍 v3.11.4 (venv) ➔ /root/venv/bin/python3 /root/PyTorch/hubconf.py
root@pytorch PyTorch on  🚀 main [!]? via 🐍 v3.11.4 (venv) *
```

<Callout icon="lightbulb">
  Running your scripts both in the IDE and the terminal helps solidify your understanding of PyTorch operations across different environments.
</Callout>

***

## Conclusion

In this guide, we have detailed the course structure and demonstrated how to configure both Jupyter Notebook and Visual Studio Code for PyTorch development. By following these examples and experimenting with the provided code snippets, you will gain a robust understanding of PyTorch and its workflows.

Thank you for choosing this course—now is the time to dive in and start learning!

For further reading and more resources, check out the following:

* [PyTorch Documentation](https://pytorch.org/docs/)
* [Jupyter Notebook Documentation](https://jupyter.org/documentation)
* [Visual Studio Code Documentation](https://code.visualstudio.com/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-2490-4be0-a894-4b3d3cc78fac/lesson/c75e932d-fe2f-4f2d-874b-4bee72227c2f" />
</CardGroup>


# Demo Introduction to PyTorch Tensors

Source: https://notes.kodekloud.com/docs/PyTorch/Getting-Started-with-PyTorch/Demo-Introduction-to-PyTorch-Tensors/page

This lesson introduces PyTorch Tensors, covering creation, manipulation, and visualization techniques essential for deep learning and model training.

Hey everyone,

In this lesson, we'll dive into PyTorch Tensors—one of the core components for deep learning and model training. Tensors help you transform data into a format that is optimal for model training and inference. Throughout this guide, you will learn how to create, initialize, and manipulate tensors using various techniques.

Below is some helper code that imports PyTorch and matplotlib, and defines a function to visualize tensor layers. This visualization function displays each layer along with its corresponding index, which is particularly useful for understanding multi-dimensional tensor structures.

```python theme={null}
import torch
import matplotlib.pyplot as plt

def visualize_tensor(tensor):
    num_layers = tensor.size(0)  # Number of layers (e.g., 4 channels)
    height, width = tensor.size(1), tensor.size(2)  # Height and width (e.g., 82, 290)

    fig, axes = plt.subplots(1, num_layers, figsize=(15, 5))

    # If there is only one layer, ensure axes is iterable
    if num_layers == 1:
        axes = [axes]

    for i in range(num_layers):
        axes[i].imshow(tensor[i], cmap='gray', aspect='auto')
        axes[i].set_title(f'Layer {i+1}')

    plt.show()
```

***

## Creating and Initializing Tensors

In this section, we demonstrate how to create different types of tensors including simple one-dimensional, multi-dimensional, and random tensors.

### Simple and Multi-Dimensional Tensors

Let's start by creating a one-dimensional tensor from a list, then a two-dimensional tensor, followed by a tensor filled with random values.

```python theme={null}
