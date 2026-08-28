# Create our model instance
model = FakeNet()
print(model)
```

***

## Creating a Fake Dataset and Training the Model

For demonstration purposes, we generate a synthetic dataset using random tensors and perform a simple training loop. We'll use the Mean Squared Error (MSE) loss function together with the SGD optimizer.

```python theme={null}
import torch
from torch.utils.data import Dataset, DataLoader

class FakeDataset(Dataset):
    def __init__(self, num_samples=1000):
        self.num_samples = num_samples

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # Generate random input data with 10 features and a random target value
        x = torch.randn(10)
        y = torch.randn(1)
        return x, y

# Create the dataset and data loader
dataset = FakeDataset(num_samples=1000)
data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Define loss function and optimizer
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
```

Train the model for five epochs:

```python theme={null}
# Train the model for 5 epochs
N_EPOCHS = 5

for epoch in range(N_EPOCHS):
    running_loss = 0.0
    for i, (inputs, targets) in enumerate(data_loader):
        optimizer.zero_grad()  # Zero the parameter gradients
        outputs = model(inputs)  # Forward pass
        loss = criterion(outputs, targets)
        loss.backward()        # Backward pass and optimize
        optimizer.step()
        running_loss += loss.item()
```

***

## Saving and Loading the Model Using state\_dict

PyTorch recommends saving only the model parameters with the state dictionary. This includes the model's weights, biases, and optimizer hyperparameters.

<Callout icon="lightbulb">
  It is generally recommended to save only the state\_dict to allow flexibility when modifying the model architecture or optimizer in the future.
</Callout>

Print the state dictionaries for inspection and then save them:

```python theme={null}
# Print model state_dict and optimizer state_dict
print(model.state_dict())
for k, v in model.state_dict().items():
    print(f"Layer Name: {k} Parameters: {v.size()}")

print(optimizer.state_dict())

# Save the state_dicts (using .pt extension for the model)
import torch
torch.save(model.state_dict(), "model_state_dict.pt")
torch.save(optimizer.state_dict(), "optimizer")
```

Later, you can reload the parameters for inference by initializing a new model instance and loading the saved state dictionary:

```python theme={null}
# Initialize a new model instance for inference
new_model = FakeNet()

# Print initial state for comparison
for k, v in new_model.state_dict().items():
    print(f"Layer Name: {k} Parameters: {v}")

# Load the parameters into the new model
new_model.load_state_dict(torch.load("model_state_dict.pt"))

# Verify that the parameters have updated after loading
for k, v in new_model.state_dict().items():
    print(f"Layer Name: {k} Parameters: {v}")
```

Perform inference by setting the model to evaluation mode and passing an example input:

```python theme={null}
# Create a sample input: a batch of one sample with 10 features
sample_input = torch.randn(1, 10)
print(sample_input)

# Set model to evaluation mode and perform inference
new_model.eval()
output = new_model(sample_input)
print(output)
```

***

## Saving and Loading the Entire Model

Another approach is to save the full model object as a Python pickle. Although convenient, this method requires the same class definitions when reloading.

```python theme={null}
# Save the full model object
torch.save(model, "model_full.pt")

# Load the full model
new_modelL = torch.load("model_full.pt")
print(new_modelL)

# Verify inference using the loaded full model
new_modelL.eval()
output = new_modelL(sample_input)
print(output)
```

***

## Creating and Using Checkpoints

Checkpoints allow you to save the full training state, including the model, optimizer, current epoch, and loss. This is essential for resuming training with minimal disruption.

### Saving a Checkpoint

```python theme={null}
import torch

# Dummy epoch and loss for checkpoint demonstration
epoch = 5
loss = 0.05

# Save a checkpoint (using a .tar extension)
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, f'{epoch}_checkpoint.tar')
```

### Loading from a Checkpoint

Reload the model, optimizer, and training state from a checkpoint:

```python theme={null}
# Re-initialize your model (using the same FakeNet definition)
model = FakeNet()
print(model)

# Load the checkpoint
checkpoint = torch.load('5_checkpoint.tar')
print(checkpoint)  # This displays the checkpoint dictionary contents

# Restore the model and optimizer states from the checkpoint
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

# Optionally, retrieve the saved loss and epoch values
loss = checkpoint['loss']
epoch = checkpoint['epoch']
print(loss, epoch)
```

Integrate checkpointing into the training loop by saving at specified intervals. For example, save a checkpoint every two epochs:

```python theme={null}
N_EPOCHS = 10

for epoch in range(N_EPOCHS):
    running_loss = 0.0
    for i, (inputs, targets) in enumerate(data_loader):
        optimizer.zero_grad()   # Zero the parameter gradients
        outputs = model(inputs)   # Forward pass
        loss = criterion(outputs, targets)
        loss.backward()         # Backward pass and optimize
        optimizer.step()
        running_loss += loss.item()
    
    # Save a checkpoint every 2 epochs
    if epoch % 2 == 0:
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
        }, f'training_checkpoint_{epoch}.tar')

# Save the final checkpoint after the last epoch
torch.save({
    'epoch': N_EPOCHS,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss
}, 'training_checkpoint_final.tar')

# Example command to list all checkpoint files on Unix-like systems:
# ls -l training_checkpoint*
```

***

## Warm Starting (Transfer Learning)

Warm starting involves initializing a new model with parameters from a previously trained model. This is particularly useful for transfer learning, where you reuse learned features to speed up convergence on a new task.

```python theme={null}
# Load pre-trained model parameters into a new model instance
new_model.load_state_dict(torch.load('model_state_dict.pt'), strict=False)
print(new_model.state_dict())
```

The `strict=False` parameter ensures that only matching layers are loaded, allowing flexibility when the architectures differ slightly.

***

## Saving and Loading Across Different Devices

PyTorch makes it simple to load models trained on one device (e.g., GPU) onto another (e.g., CPU) by using the `map_location` argument.

```python theme={null}
# Load a model on CPU that was saved on GPU
import torch
model_cpu = torch.load('model_state_dict.pt', map_location='cpu')

# Alternatively, load directly to a GPU device (if available)
model_gpu = torch.load('model_state_dict.pt', map_location='cuda:0')
model_gpu.to('cuda')  # Ensure the model is moved to GPU
model_gpu.eval()

# During inference, both the model and inputs must be on the same device
sample_input = torch.randn(1, 10)
output_gpu = model_gpu(sample_input.to('cuda'))
print(output_gpu)

# Check which device is available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
```

<Callout icon="lightbulb">
  When using the `map_location` argument, always confirm that both your model and input data reside on the same device to avoid runtime errors.
</Callout>

***

## Summary

This lesson demonstrated various methods for saving and loading PyTorch models, including best practices for using state dictionaries, saving full models, checkpointing, warm starting for transfer learning, and managing device-specific loading. These techniques are fundamental for successful model training, deployment, and reuse.

For further reading, consider exploring:

* [PyTorch Documentation](https://pytorch.org/docs/)
* [Model Persistence in PyTorch](https://pytorch.org/tutorials/beginner/saving_loading_models.html)

Enhance your model management workflows by integrating these saving and loading strategies into your projects. Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-a284-41d1-8469-7e60705bbab8/lesson/34b3e0de-921b-4b2d-aad4-3467732ea1cf" />
</CardGroup>


# Introduction to Neural Networks

Source: https://notes.kodekloud.com/docs/PyTorch/Building-and-Training-Models/Introduction-to-Neural-Networks/page

Understanding neural networks is essential for model training with PyTorch, focusing on their structure, function, and applications in artificial intelligence.

Understanding neural networks is fundamental before diving into model training with PyTorch. These models, inspired by the human brain, are at the core of many modern artificial intelligence applications, including prediction, pattern recognition, and problem-solving.

Neural networks learn by analyzing data patterns, much like the human brain improves skills with practice. They excel at identifying hidden relationships within large datasets, which makes them essential for applications ranging from image classification to natural language processing.

<Callout icon="lightbulb">
  Neural networks consist of layers of interconnected neurons, where each neuron acts as a simple decision-making unit. As data moves through these layers, the network refines and interprets the information, ultimately leading to precise predictions.
</Callout>

## How Neural Networks Work

A neural network comprises multiple layers of neurons:

* **Input Layer:** Receives the raw data, such as images, text, or audio.
* **Hidden Layers:** Perform the majority of data analysis by identifying patterns and extracting features.
* **Output Layer:** Delivers the final predictions or decisions based on the processed information.

<Frame>
  ![The image explains the role of neurons in neural networks, highlighting their processes of information selection, activation, connection, and collaboration to make decisions.](https://kodekloud.com/kk-media/image/upload/v1752883136/notes-assets/images/PyTorch-Introduction-to-Neural-Networks/neurons-in-neural-networks-diagram.jpg)
</Frame>

The individual neurons collaborate by receiving input, processing it, and making decisions based on predefined rules. This collective operation allows the neural network to tackle complex tasks by breaking them down into simpler, manageable operations.

<Frame>
  ![The image illustrates the structure of a neural network, showing input, hidden, and output layers, along with their functions.](https://kodekloud.com/kk-media/image/upload/v1752883138/notes-assets/images/PyTorch-Introduction-to-Neural-Networks/neural-network-structure-layers-diagram.jpg)
</Frame>

### A Practical Example

Consider a network that classifies images as either dogs or cats:

1. **Input Stage:** The image is fed into the input layer.
2. **Feature Extraction:** Hidden layers extract and refine key features.
3. **Decision Making:** The output layer classifies the image based on the processed data.

## Activation Functions: The Neuron Gatekeepers

Activation functions determine whether a neuron should "activate" by processing the input data. They act as filters, allowing only relevant information to pass through. Common functions include:

* **Sigmoid:** Smooth curve used for binary activations.
* **ReLU (Rectified Linear Unit):** Popular in modern networks due to its simplicity and effectiveness of passing only positive values.

<Frame>
  ![The image explains the role of activation functions in neural networks, highlighting their functions in neuron activation, information flow control, and filtering useful information for the next layer.](https://kodekloud.com/kk-media/image/upload/v1752883138/notes-assets/images/PyTorch-Introduction-to-Neural-Networks/activation-functions-neural-networks.jpg)
</Frame>

## Learning and Training in Neural Networks

During training, neural networks make predictions based on the input data. When these predictions are incorrect, the network adjusts the connections (weights) between neurons. This iterative process helps the network improve over time, similar to learning from mistakes.

<Frame>
  ![The image illustrates the process of how neural networks learn through model training, showing steps like making a guess, comparing with actual results, adjusting weights, and improving over time.](https://kodekloud.com/kk-media/image/upload/v1752883139/notes-assets/images/PyTorch-Introduction-to-Neural-Networks/neural-networks-training-process.jpg)
</Frame>

### Backpropagation: Fine-Tuning the Model

Backpropagation is a critical technique where errors are propagated backwards through the network to update the weights. This feedback loop helps pinpoint the source of errors and refines the model with each iteration.

<Frame>
  ![The image illustrates the process of backpropagation in neural networks, showing input, hidden, and output layers with connections and weight adjustments.](https://kodekloud.com/kk-media/image/upload/v1752883141/notes-assets/images/PyTorch-Introduction-to-Neural-Networks/backpropagation-neural-networks-diagram.jpg)
</Frame>

## Types of Neural Networks

Neural networks come in various architectures, each tailored for specific types of tasks. Here is a quick overview:

| Type                               | Use Case                                       | Description                                               |
| ---------------------------------- | ---------------------------------------------- | --------------------------------------------------------- |
| Feed-Forward Neural Network        | Standard processing from input to output       | Data flows in one direction without looping               |
| Convolutional Neural Network (CNN) | Image analysis and pattern recognition         | Excels at processing grid-like topology such as images    |
| Recurrent Neural Network (RNN)     | Sequential data processing (e.g., text, audio) | Ideal for handling time-series or sequence-dependent data |

<Frame>
  ![The image lists three types of neural networks: Feedforward Neural Network, Convolutional Neural Network (CNN), and Recurrent Neural Network (RNN), each with a brief description of their functions.](https://kodekloud.com/kk-media/image/upload/v1752883142/notes-assets/images/PyTorch-Introduction-to-Neural-Networks/neural-networks-types-descriptions.jpg)
</Frame>

<Callout icon="lightbulb">
  * Neural networks draw inspiration from the human brain, leveraging interconnected neurons to recognize patterns and make predictions.
  * The layered structure — comprising input, hidden, and output layers — is critical for data processing.
  * Activation functions ensure that only valuable information is forwarded through the network.
  * Training involves iterative weight adjustments, with backpropagation playing a pivotal role in refining network accuracy.
  * Various architectures like CNNs and RNNs are optimized for tasks such as image recognition and sequential data processing.
</Callout>

<Frame>
  ![The image is a summary of key concepts about neural networks, including their inspiration from the human brain, structure, activation functions, training, and types like CNNs and RNNs.](https://kodekloud.com/kk-media/image/upload/v1752883142/notes-assets/images/PyTorch-Introduction-to-Neural-Networks/neural-networks-key-concepts-summary.jpg)
</Frame>

## Next Steps: Implementing Neural Networks with PyTorch

Now that you have a solid understanding of neural network fundamentals, you're ready to dive into implementing these models using PyTorch. In the upcoming sections, we will walk through the process of building and training neural networks with code examples, ensuring you can leverage PyTorch effectively for your projects.

For more detailed guidance on neural network implementations and advanced techniques, be sure to explore additional resources and documentation on [PyTorch's official site](https://pytorch.org/).

Happy coding and learning!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-a284-41d1-8469-7e60705bbab8/lesson/4d48093e-84ad-4187-894c-ed7ba631f898" />
</CardGroup>
