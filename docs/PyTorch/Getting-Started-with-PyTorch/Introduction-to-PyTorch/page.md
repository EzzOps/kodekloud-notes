# Expected Output:
# torch.Size([2, 2]) torch.float32 cpu
```

<Callout icon="lightbulb">
  Knowing these attributes helps you manage tensor operations efficiently and debug your deep learning models.
</Callout>

## Common Tensor Operations

PyTorch supports over 100 tensor operations. Here are several commonly used ones:

1. **Indexing and Slicing:** Extract specific elements or sections of a tensor. For instance, you can select certain rows or columns in a 2D tensor.

<Frame>
  ![The image is a slide titled "Tensor Operations" focusing on "Indexing and Slicing," explaining that these operations select elements or portions of a tensor and retrieve specific rows or columns in a 2D tensor.](https://kodekloud.com/kk-media/image/upload/v1752883178/notes-assets/images/PyTorch-Introduction-to-PyTorch-Tensors/tensor-operations-indexing-slicing.jpg)
</Frame>

2. **Joining Tensors:** Concatenate tensors along a specific dimension (row-wise or column-wise) using functions like `torch.cat()`.

<Frame>
  ![The image is a slide titled "Tensor Operations" focusing on "Joining Tensors," explaining that tensors can be combined using torch.cat() either row-wise or column-wise.](https://kodekloud.com/kk-media/image/upload/v1752883179/notes-assets/images/PyTorch-Introduction-to-PyTorch-Tensors/tensor-operations-joining-tensors.jpg)
</Frame>

3. **Reshaping Tensors:** Adjust the dimensions of a tensor (e.g., flatten a 2D matrix into a 1D vector) with the `torch.reshape()` function.

<Frame>
  ![The image is a slide titled "Tensor Operations" focusing on "Reshaping Tensors," explaining how tensors can be reshaped using torch.reshape() and its usefulness in flattening a 2D matrix into a 1D vector.](https://kodekloud.com/kk-media/image/upload/v1752883180/notes-assets/images/PyTorch-Introduction-to-PyTorch-Tensors/tensor-operations-reshaping-tensors.jpg)
</Frame>

Below is an example that compares common indexing approaches in both PyTorch and NumPy:

```python theme={null}
import torch
import numpy as np

# Create a 2D tensor (3x3 matrix) in PyTorch
tensor = torch.tensor([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]])

# Indexing operations in PyTorch
row_2 = tensor[1, :]
print("Second row (PyTorch):", row_2)

slice_2 = tensor[1, 0:2]
print("First two columns of the second row (PyTorch):", slice_2)

element = tensor[2, 1]
print("Element at (3rd row, 2nd column) (PyTorch):", element)

# Create a 2D array (3x3 matrix) in NumPy
array = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# Indexing operations in NumPy
row_2_np = array[1, :]
print("Second row (NumPy):", row_2_np)

slice_2_np = array[1, 0:2]
print("First two columns of the second row (NumPy):", slice_2_np)

element_np = array[2, 1]
print("Element at (3rd row, 2nd column) (NumPy):", element_np)
```

Both PyTorch tensors and NumPy arrays utilize similar syntax for indexing, making it easier to transition your skills from NumPy to PyTorch.

## Converting Images to Tensors

Converting images into tensors is a frequent task in machine learning. Typically, the Pillow library is used to open images, and TorchVision—via the `transforms.ToTensor()` function—converts them into tensors.

```python theme={null}
from PIL import Image
from torchvision import transforms

img = Image.open('image.jpg')
transform = transforms.ToTensor()
img_tensor = transform(img)
print(img_tensor)
```

After conversion, the image is represented as a 3D tensor with normalized RGB channel values between 0 and 1. To inspect this tensor's attributes, use:

```python theme={null}
print(img_tensor.shape, img_tensor.dtype, img_tensor.device)
# Expected Output:
# torch.Size([4, 144, 144]) torch.float32 cpu
```

This output indicates that the image tensor contains 4 channels (possibly RGBA) with dimensions of 144x144 pixels, stored on the CPU.

## Leveraging GPUs with PyTorch

PyTorch's strong GPU support significantly boosts deep learning performance. GPUs specialize in handling parallel computations, making them ideal for the heavy matrix operations found in deep learning.

<Frame>
  ![The image outlines the benefits of using a Graphics Processing Unit (GPU) for deep learning, including faster training, parallel computations, suitability for large datasets, reduced training time, and optimization for PyTorch.](https://kodekloud.com/kk-media/image/upload/v1752883182/notes-assets/images/PyTorch-Introduction-to-PyTorch-Tensors/gpu-deep-learning-benefits.jpg)
</Frame>

PyTorch utilizes NVIDIA’s CUDA (Compute Unified Device Architecture) to enable GPUs to handle tasks beyond rendering graphics, such as scientific computations and model training.

<Frame>
  ![The image is a presentation slide about NVIDIA's Compute Unified Device Architecture (CUDA), highlighting its use in scientific computing, machine learning, and leveraging GPU power for deep learning.](https://kodekloud.com/kk-media/image/upload/v1752883183/notes-assets/images/PyTorch-Introduction-to-PyTorch-Tensors/nvidia-cuda-scientific-computing-slide.jpg)
</Frame>

Check for GPU availability and move tensors as follows:

```python theme={null}
# Check if GPU is available
if torch.cuda.is_available():
    print("GPU is available")
else:
    print("GPU is not available")
```

To move a tensor to a GPU:

```python theme={null}
# Check tensor device before and after moving to GPU
print(tensor.device)  # Expected Output: cpu

# Move tensor to GPU
tensor = tensor.to('cuda')
print(tensor.device)  # Expected Output: cuda
```

For portability, dynamically select the device:

```python theme={null}
# Select device based on GPU availability
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Create tensor on the selected device
tensor = torch.tensor([1, 2, 3], device=device)
print(tensor.device)
```

<Callout icon="lightbulb">
  Using dynamic device selection ensures that your code runs efficiently on both GPUs and CPUs.
</Callout>

## Conclusion

This lesson established a strong foundation for understanding and working with PyTorch tensors. We covered how to create tensors, utilize their powerful operations, convert images to tensors, and leverage GPU acceleration for performance gains. In the upcoming demo, we will further explore these concepts on our development machine.

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/5a59db15-2490-4be0-a894-4b3d3cc78fac/lesson/22db0214-825f-4f68-b444-49e0bc1f7713" />
</CardGroup>


# Introduction to PyTorch

Source: https://notes.kodekloud.com/docs/PyTorch/Getting-Started-with-PyTorch/Introduction-to-PyTorch/page

This article introduces PyTorch, its applications, advantages, and ecosystem in the context of artificial intelligence and machine learning.

Artificial intelligence and machine learning are not mere buzzwords—they are transformative forces reshaping industries, enhancing daily lives, and pushing the boundaries of technology. Frameworks like PyTorch power these advancements by enabling developers and researchers to build and experiment with deep learning models efficiently.

<Frame>
  ![The image illustrates AI and machine learning's impact on various sectors, featuring icons of a car, house, chat, and gear connected to a central AI symbol. The text reads "AI and Machine Learning – Transforming the Future."](https://kodekloud.com/kk-media/image/upload/v1752883184/notes-assets/images/PyTorch-Introduction-to-PyTorch/ai-machine-learning-impact-icons.jpg)
</Frame>

From powering virtual assistants and delivering personalized recommendations to enabling autonomous vehicles and driving medical breakthroughs, these transformative technologies are redefining the future.

<Frame>
  ![The image illustrates four applications of AI and machine learning: powering virtual assistants, personalized recommendations, enabling autonomous vehicles, and driving medical breakthroughs.](https://kodekloud.com/kk-media/image/upload/v1752883186/notes-assets/images/PyTorch-Introduction-to-PyTorch/ai-machine-learning-applications.jpg)
</Frame>

At the heart of many of these innovations is the PyTorch framework, developed by Facebook's AI Research Lab in 2016. As an open-source machine learning library written in Python, PyTorch is celebrated for its ease of use, flexibility, and high performance. Its dynamic computation graph allows developers to modify model architectures on the fly, making it especially popular for research and experimental projects.

## Applications of PyTorch

PyTorch is widely applied in various machine learning domains. Its strength in deep learning is evident in the construction of convolutional neural networks (CNNs) and recurrent neural networks (RNNs). Furthermore, PyTorch is highly effective for natural language processing tasks—such as machine translation, sentiment analysis, and language generation—as well as for computer vision tasks including image classification, object detection, and image segmentation when paired with the TorchVision library.

<Frame>
  ![The image is a diagram titled "PyTorch – Applications," showing three categories: Deep Learning (with CNNs and RNNs), NLP (with Machine Translation, Sentiment Analysis, and Language Generation), and Computer Vision (with Image Classification, Object Detection, and Image Segmentation).](https://kodekloud.com/kk-media/image/upload/v1752883187/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-applications-deep-learning-nlp-computer-vision.jpg)
</Frame>

When compared to other frameworks such as TensorFlow and Keras, PyTorch distinguishes itself with an intuitive Pythonic syntax and a dynamic approach to computation. While TensorFlow is known for its expansive ecosystem and benefits in production-scale projects, its static graph structure can be less flexible. Similarly, Keras, serving as a high-level API for TensorFlow, does not offer the same level of low-level control available in PyTorch.

<Frame>
  ![The image compares PyTorch, TensorFlow, and Keras, highlighting their key features and differences. PyTorch is noted for being intuitive and using dynamic graphs, TensorFlow for its larger ecosystem and production-scale projects, and Keras as a high-level API for TensorFlow with less low-level control.](https://kodekloud.com/kk-media/image/upload/v1752883188/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-tensorflow-keras-comparison.jpg)
</Frame>

PyTorch also boasts native GPU support and seamless integration with the Python ecosystem, making it a versatile option for both academic research and industrial applications.

## Key Advantages of PyTorch

One of the standout features of PyTorch is its dynamic computation graph, enabling eager execution. This means that operations are computed immediately, which simplifies debugging and accelerates iterative experimentation. Its highly Pythonic design ensures a smooth integration with existing Python libraries, easing the learning curve for new users.

<Frame>
  ![The image is a slide titled "PyTorch – Advantages" highlighting the "Pythonic Nature" of PyTorch, noting it integrates seamlessly with Python.](https://kodekloud.com/kk-media/image/upload/v1752883190/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-advantages-pythonic-nature.jpg)
</Frame>

The extensive PyTorch ecosystem further enhances its functionality:

* **PyTorch Lightning:** Simplifies the training process and reduces boilerplate code.
* **TorchServe:** Eases the deployment of trained models into production environments.
* **TorchAudio:** Optimizes audio data processing.
* **TorchVision:** Provides utilities and pre-trained models for computer vision tasks.

<Frame>
  ![The image lists PyTorch tools, including PyTorch Lightning, TorchServe, Torchaudio, and Torchvision, with a note that Torchvision focuses on computer vision tasks.](https://kodekloud.com/kk-media/image/upload/v1752883191/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-tools-lightning-serve-audio-vision.jpg)
</Frame>

Additionally, support for both CPU and GPU acceleration, combined with a dynamic and active community, ensures that PyTorch continues to evolve and deliver comprehensive support and improvements.

<Frame>
  ![The image outlines the advantages of PyTorch, highlighting strong community support, suitability for research and production, and a large ecosystem with many resources.](https://kodekloud.com/kk-media/image/upload/v1752883192/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-advantages-community-support.jpg)
</Frame>

## PyTorch Tensors

A fundamental component of PyTorch is the Tensor, akin to a NumPy array but optimized for GPU acceleration and enhanced computations. Tensors are versatile data containers capable of representing everything from single values to complex multi-dimensional arrays. This flexibility is essential for deep learning applications where efficient data manipulation is critical.

<Frame>
  ![The image explains PyTorch tensors, showing vectors as simple lists of numbers, matrices as grids of numbers, and tensors as multi-dimensional data. It highlights tensors as the core data structure in PyTorch, optimized with GPU acceleration.](https://kodekloud.com/kk-media/image/upload/v1752883193/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-tensors-vectors-matrices.jpg)
</Frame>

With operations ranging from element-wise addition and multiplication to matrix-level computations, PyTorch Tensors can be reshaped, sliced, and manipulated effortlessly. For example, image data stored in a tensor may need reshaping to fit the input specifications of a neural network—a process that PyTorch handles efficiently.

<Frame>
  ![The image describes PyTorch Tensors, highlighting their versatile operations like addition and multiplication, and their flexible manipulation capabilities such as reshaping and slicing.](https://kodekloud.com/kk-media/image/upload/v1752883194/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-tensors-operations-manipulation.jpg)
</Frame>

<Callout icon="lightbulb">
  For an in-depth exploration of tensors and their operations, look out for our detailed guide on PyTorch Tensors in the upcoming sections.
</Callout>

## Autograd: Automatic Differentiation

A pivotal feature of PyTorch is its Autograd library for automatic differentiation. Autograd tracks all operations performed on tensors and automatically computes the gradients required to optimize machine learning models. This process simplifies backpropagation, streamlining the training process and reducing common errors associated with manual gradient computation.

<Frame>
  ![The image describes PyTorch's autograd as an automatic differentiation library essential for training machine learning models, with a flowchart showing the process involving AccumulateGrad, PowBackward0, and AddBackward0.](https://kodekloud.com/kk-media/image/upload/v1752883195/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-autograd-differentiation-flowchart.jpg)
</Frame>

<Callout icon="lightbulb">
  Keep an eye on upcoming sections where we delve deeper into Autograd and its critical role in model training and optimization.
</Callout>

## Building Neural Networks with PyTorch

PyTorch simplifies the creation of neural networks—computational models inspired by the human brain that process data through interconnected layers. Its torch.nn module provides an array of pre-built components, including layers, activation functions, and loss functions, which enable developers to build and train neural networks with ease.

<Frame>
  ![The image illustrates a neural network diagram inside a silhouette of a head, showing input, hidden, and output layers.](https://kodekloud.com/kk-media/image/upload/v1752883196/notes-assets/images/PyTorch-Introduction-to-PyTorch/neural-network-diagram-silhouette-head.jpg)
</Frame>

Using torch.nn, developers can construct simple feedforward networks by stacking layers and selecting appropriate activation functions and loss metrics. This modular approach allows for the creation of both simple and sophisticated network architectures.

<Frame>
  ![The image describes PyTorch's torch.nn module, highlighting its components: Layers, Activation Functions, and Loss Functions, which are used for building and training neural networks.](https://kodekloud.com/kk-media/image/upload/v1752883198/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-torch-nn-module-components.jpg)
</Frame>

## The PyTorch Ecosystem

Beyond the core framework, PyTorch features a vibrant ecosystem of libraries and tools that address specialized tasks:

| Library           | Purpose                                                    | Example Use                                 |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------- |
| TorchVision       | Pre-trained models and utilities for computer vision tasks | Image classification and object detection   |
| TorchAudio        | Tools for efficient audio processing                       | Speech recognition and sound classification |
| PyTorch Lightning | High-level interface to streamline model training          | Simplifying complex training procedures     |
| TorchServe        | Deploying trained models into production                   | Serving models in production environments   |

<Frame>
  ![The image shows a diagram of the PyTorch ecosystem of libraries, including Torchvision, Torchaudio, PyTorch Lightning, and TorchServe, with a focus on "Vision tasks" under Torchvision.](https://kodekloud.com/kk-media/image/upload/v1752883198/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-ecosystem-vision-tasks-diagram.jpg)
</Frame>

These libraries, among others, extend PyTorch’s functionality and make it a comprehensive solution for tasks ranging from research to deployment.

## Adoption and Community Support

PyTorch is trusted by major companies and academic institutions alike. Some notable adopters include:

* **Meta (Facebook):** Utilizing PyTorch for advanced AI research and development.
* **Tesla:** Leveraging the framework for designing deep learning models for autopilot systems and self-driving technology.
* **Stanford University:** Employing PyTorch in cutting-edge research projects.
* **Uber:** Applying PyTorch in predictive modeling and autonomous driving research.

<Frame>
  ![The image shows logos of organizations that use PyTorch, including Meta, Stanford University, and Tesla.](https://kodekloud.com/kk-media/image/upload/v1752883200/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-logos-meta-stanford-tesla.jpg)
</Frame>

The PyTorch Foundation, established in 2022 under the guidance of the Linux Foundation, plays a crucial role in fostering community development and supporting the ecosystem’s growth. A robust open-source community, active forums, and continuous contributions further ensure that PyTorch remains on the cutting edge of technological innovation.

<Frame>
  ![The image outlines the PyTorch Foundation and Community, highlighting its open-source project, active community forums, and participation in major AI conferences.](https://kodekloud.com/kk-media/image/upload/v1752883200/notes-assets/images/PyTorch-Introduction-to-PyTorch/pytorch-foundation-community-overview.jpg)
</Frame>

## Summary

In this article, we introduced the core components and advantages of PyTorch—from dynamic tensors and automatic differentiation with Autograd to powerful neural network modules and an extensive ecosystem. Whether you are a researcher or an industry practitioner, understanding these fundamental concepts will serve as a solid foundation as you dive deeper into machine learning with PyTorch.

<Callout icon="lightbulb">
  Explore our upcoming tutorials for detailed insights into PyTorch’s tensor operations, model building, and optimization techniques.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/5a59db15-2490-4be0-a894-4b3d3cc78fac/lesson/b649ab9a-901e-440f-8499-2cfaf7629d3d" />
</CardGroup>
