# Introduction to PyTorch Tensors

Source: https://notes.kodekloud.com/docs/PyTorch/Getting-Started-with-PyTorch/Introduction-to-PyTorch-Tensors/page

This article introduces PyTorch tensors, covering their creation, attributes, operations, and GPU utilization for efficient data processing in deep learning.

In this lesson, we explore one of PyTorch's fundamental concepts: Tensors. Serving as the cornerstone for model building and training, tensors provide an efficient method for storing and processing data in multiple dimensions—from simple scalars to complex multi-dimensional arrays.

## Understanding Tensors

A tensor is a versatile container for data, similar to a list or table, but with enhanced capabilities. It can hold data across several dimensions:

* A scalar is the simplest tensor, representing a single number (a zero-dimensional tensor).
* A vector is a one-dimensional tensor, akin to a list of numbers.
* A matrix is a two-dimensional tensor, organized in rows and columns.

![The image is an introduction to tensors, highlighting their ability to organize data in different dimensions, act as containers for complex data, and hold more data than lists or arrays.](https://kodekloud.com/kk-media/image/upload/v1752883173/notes-assets/images/PyTorch-Introduction-to-PyTorch-Tensors/introduction-to-tensors-data-organization.jpg)

![The image is an introduction to tensors, showing examples of a scalar, a vector, and a matrix. The scalar is a single number, the vector is a one-dimensional array, and the matrix is a two-dimensional array.](https://kodekloud.com/kk-media/image/upload/v1752883174/notes-assets/images/PyTorch-Introduction-to-PyTorch-Tensors/introduction-to-tensors-scalar-vector-matrix.jpg)

Tensors can also manage more complex data. For example, an image is typically stored as a three-dimensional tensor—with dimensions representing height, width, and color channels. Similarly, video data is commonly stored as a four-dimensional tensor, where the extra dimension corresponds to time.

![The image shows a series of colored matrices stacked together, labeled with numbers 1 to 4, under the title "Tensor – Introduction."](https://kodekloud.com/kk-media/image/upload/v1752883175/notes-assets/images/PyTorch-Introduction-to-PyTorch-Tensors/tensor-introduction-colored-matrices.jpg)

In PyTorch, tensors are not only used to store data but also to perform a wide range of mathematical operations.

![The image is an introduction to tensors, highlighting three key features: storing data and performing math operations, flexibility for all data types, and handling simple numbers to complex data.](https://kodekloud.com/kk-media/image/upload/v1752883177/notes-assets/images/PyTorch-Introduction-to-PyTorch-Tensors/introduction-to-tensors-features.jpg)

## Creating Tensors

PyTorch offers several convenient methods to create tensors, depending on your requirements:

1. **From Lists or Arrays:** Convert a list, tuple, or NumPy array to a tensor using the `torch.tensor()` function.

   ```python theme={null}
   # Creating a tensor from a list
   tensor_from_list = torch.tensor([1, 2, 3])
   ```

2. **With Specific Values:** Create tensors filled with zeros or ones using `torch.zeros()` or `torch.ones()`.

   ```python theme={null}
   # Tensor filled with zeros
   zeros_tensor = torch.zeros(3, 3)
   ```

3. **Randomly Initialized Tensors:** Use `torch.rand()` for tensors populated with random numbers between 0 and 1—ideal for initializing model weights.

4. **Uninitialized Tensors:** Use `torch.empty()` for creating a tensor with uninitialized values (contents are based on the current memory state).

   ```python theme={null}
   # Uninitialized tensor
   empty_tensor = torch.empty(2, 3)
   ```

## Key Tensor Attributes

Every PyTorch tensor carries attributes that describe its structure and storage location:

* **Shape:** Indicates the dimensions (e.g., rows and columns).
* **dtype:** Specifies the data type (e.g., `float32`, `int64`).
* **Device:** Shows where the tensor is stored, such as the CPU or GPU.

For example:

```python theme={null}
import torch

t = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
print(t.shape, t.dtype, t.device)
