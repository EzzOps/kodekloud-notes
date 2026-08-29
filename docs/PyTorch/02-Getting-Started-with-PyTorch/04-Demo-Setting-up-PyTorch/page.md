# Create a simple 1D tensor from a list and print it
simple_tensor = torch.tensor([1, 2, 3])
print(simple_tensor)
print(simple_tensor.shape)

# Create a 2D tensor from two lists and print its shape
two_dim_simple_tensor = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(two_dim_simple_tensor.shape)

# Create a 1D tensor with random values and print its contents and shape
random_tensor = torch.rand(3)
print(random_tensor)
print(random_tensor.shape)
```

For a more advanced example, here is how to create a three-dimensional tensor with dimensions 3 x 4 x 5 filled with random values:

```python theme={null}
# Create a 3D tensor with random values (dimensions: 3 x 4 x 5)
another_random_tensor = torch.rand(3, 4, 5)
print(another_random_tensor)
print(another_random_tensor.shape)
```

<Callout icon="lightbulb">
  If you're unsure about the structure of your tensor, use the visualize\_tensor() helper function to better understand its layers, rows, and columns.
</Callout>

***

## Tensors Filled with Zeros and Ones

PyTorch provides convenient functions to generate tensors pre-filled with zeros or ones, which can be extremely useful when initializing models or setting up placeholders.

```python theme={null}
# Create a tensor filled with zeros (dimensions: 2 x 4) and print it
zero_tensor = torch.zeros((2, 4))
print(zero_tensor)

# Create a tensor filled with ones (dimensions: 2 x 4) and print it
ones_tensor = torch.ones((2, 4))
print(ones_tensor)
```

***

## Tensor Indexing and Concatenation

This section covers how to access individual elements within a tensor using indexing, as well as how to concatenate tensors along specific dimensions.

### Indexing

Consider the following 3x3 tensor and learn how to access its rows and individual elements.

```python theme={null}
# Create a 3x3 tensor
tensor_a = torch.tensor([[10, 20, 30],
                         [40, 50, 60],
                         [70, 80, 90]])
print(tensor_a)

# Access the first row (index 0)
first_row = tensor_a[0]
print(first_row)

# Access the second row (index 1)
second_row = tensor_a[1]
print(second_row)

# Access the first value of the second row using two different methods
second_row_first_value = tensor_a[1, 0]
print(second_row_first_value)
```

### Concatenation

You can join tensors along an axis using PyTorch’s concatenation function. Note that concatenating tensors requires matching dimensions in the other axes.

```python theme={null}
# Create a new 2D tensor
tensor_b = torch.tensor([[1, 2, 3],
                         [4, 5, 6]])
print(tensor_b)

# Concatenate tensor_a and tensor_b along the first dimension (rows)
concat_tensor = torch.cat((tensor_a, tensor_b), dim=0)
print(concat_tensor)

# Attempting concatenation along dimension 1 (columns) when dimensions do not match will raise an error
# Uncommenting the following lines will throw a RuntimeError:
# concat_tensor = torch.cat((tensor_a, tensor_b), dim=1)
# print(concat_tensor)
```

<Callout icon="triangle-alert">
  Ensure that when concatenating tensors, all dimensions except the one being concatenated must match. Otherwise, PyTorch will raise a RuntimeError.
</Callout>

***

## Transforming Images into Tensors

In real-world applications, such as building an image classifier, transforming images into tensors is essential. The PyTorch torchvision library simplifies this process by providing image transforms.

Below is an example that uses the Pillow library (PIL) to open an image file and convert it into a tensor using torchvision.transforms. Replace "path\_to\_image.jpg" with the actual path to your image file.

```python theme={null}
from PIL import Image
import torchvision.transforms as transforms

# Load an image from the file system (replace 'path_to_image.jpg' with the actual image path)
image = Image.open("path_to_image.jpg")

# Define a transform to convert the image to a tensor
transform = transforms.ToTensor()

# Apply the transform to the image
image_tensor = transform(image)

# Print the tensor and its attributes (size, data type, and device)
print(image_tensor)
print(image_tensor.size(), image_tensor.dtype, image_tensor.device)
```

When you convert an image to a tensor, the first dimension typically represents the number of channels (for example, 3 channels for an RGB image), the second dimension represents the height, and the third dimension represents the width.

***

## Working with GPUs in PyTorch

PyTorch supports GPU acceleration, enabling faster computation for deep learning tasks. This section demonstrates how to check for GPU availability and move tensors to a GPU if one is available.

```python theme={null}
# Check if GPU is available
print(torch.cuda.is_available())

# Set the device to 'cuda' if GPU is available, otherwise 'cpu'
if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

# Create a tensor on the selected device and print the device attribute
tensor_device = torch.tensor([1, 2, 3], device=device)
print(tensor_device.device)

# Attempt to move a tensor from CPU to GPU
try:
    tensor_cuda = tensor_device.to('cuda')
    print("Tensor moved to GPU:", tensor_cuda.device)
except RuntimeError as e:
    print(e)
```

<Callout icon="lightbulb">
  On a machine without an NVIDIA GPU or proper drivers, attempting to move a tensor to 'cuda' will raise a runtime error. Always check for GPU availability before transferring data.
</Callout>

***

## Conclusion

This lesson provided a comprehensive introduction to working with PyTorch Tensors. We covered:

* Creating and initializing tensors of various dimensions and data types
* Generating tensors with zeros and ones
* Indexing and concatenating tensors
* Transforming images into tensors for computer vision tasks
* Leveraging GPU acceleration for tensor computations

By mastering these fundamental concepts, you will be well-equipped to build and train deep learning models.

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/5a59db15-2490-4be0-a894-4b3d3cc78fac/lesson/9a291e1f-8cd2-49f0-a4bf-e0ca16e0f3f7" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/pytorch/module/5a59db15-2490-4be0-a894-4b3d3cc78fac/lesson/16e0587e-3aba-47cb-a4b2-8ef26befd39e" />
</CardGroup>


# Demo Setting up PyTorch

Source: https://notes.kodekloud.com/docs/PyTorch/Getting-Started-with-PyTorch/Demo-Setting-up-PyTorch/page

This guide covers setting up a PyTorch development environment on Ubuntu, including installation and verification steps.

Welcome to this comprehensive guide on configuring a PyTorch development environment. In this tutorial, you'll learn how to create an isolated Python virtual environment on an Ubuntu machine, install all required dependencies (including PyTorch, TorchVision, and TorchAudio), and verify the installation. This step-by-step approach ensures that your environment is reproducible for collaboration or deployment.

Before you start, visit the [PyTorch “Get Started” page](https://pytorch.org/get-started/) to choose your operating system, package manager, and CUDA version. The page dynamically generates the installation commands. For instance, for a nightly CPU build you may receive:

```bash theme={null}
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

Alternatively, if you prefer Conda with CUDA 11.8 support, you might run:

```bash theme={null}
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

For a typical installation using CUDA 11.8, the command is:

```bash theme={null}
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

In the following sections, we detail how to set up your PyTorch environment on an Ubuntu system.

***

## Step 1: Update Your System and Verify Python Installation

Begin by updating your package list to ensure that you have the latest versions of available packages:

```bash theme={null}
root@ubuntu-host:~ ➜ apt-get update
Get:1 http://old-releases.ubuntu.com/ubuntu lunar InRelease [267 kB]
Get:2 http://old-releases.ubuntu.com/ubuntu lunar-updates InRelease [109 kB]
Get:3 http://old-releases.ubuntu.com/ubuntu lunar-backports InRelease [99.9 kB]
Get:4 http://old-releases.ubuntu.com/ubuntu lunar-security InRelease [109 kB]
Get:5 http://old-releases.ubuntu.com/ubuntu lunar/multiverse amd64 Packages [289 kB]
Get:6 http://old-releases.ubuntu.com/ubuntu lunar/main amd64 Packages [1,797 kB]
Get:7 http://old-releases.ubuntu.com/ubuntu lunar/universe amd64 Packages [18.7 MB]
Get:8 http://old-releases.ubuntu.com/ubuntu lunar/restricted amd64 Packages [181 kB]
Get:9 http://old-releases.ubuntu.com/ubuntu lunar-updates/restricted amd64 Packages [325 kB]
Get:10 http://old-releases.ubuntu.com/ubuntu lunar-updates/main amd64 Packages [531 kB]
Get:11 http://old-releases.ubuntu.com/ubuntu lunar-updates/multiverse amd64 Packages [11.6 kB]
Get:12 http://old-releases.ubuntu.com/ubuntu lunar-backports/universe amd64 Packages [4,203 B]
Get:13 http://old-releases.ubuntu.com/ubuntu lunar-security/universe amd64 Packages [1,017 kB]
Get:14 http://old-releases.ubuntu.com/ubuntu lunar-security/main amd64 Packages [429 kB]
Get:15 http://old-releases.ubuntu.com/ubuntu lunar-security/restricted amd64 Packages [8,203 B]
Fetched 25.3 MB in 4s (7,220 kB/s)
Reading package lists... Done
root@ubuntu-host:~ ➜
```

It appears that Python is not installed yet. Install Python 3 (version 3.11 in this guide) and verify the installation with:

```bash theme={null}
root@ubuntu-host:~ ⟶ python3 --version
Python 3.11.4

root@ubuntu-host:~ ⟶ which python3
/usr/bin/python3
```

***

## Step 2: Install pip and the venv Package

Pip is essential for managing Python packages. Install pip along with build dependencies:

```bash theme={null}
root@ubuntu-host:~ ⟶ apt-get install -y python3-pip python3-dev python3-venv
```

During the installation, you will encounter output similar to this:

```plaintext theme={null}
Setting up libgprofng0:amd64 (2.40-2ubuntu4.1) ...
Setting up python3-pip (23.0.1+dfsg-1ubuntu0.2) ...
...
root@ubuntu-host:~ #
```

Verify pip's installation:

```bash theme={null}
root@ubuntu-host:~ ⟶ pip3 --version
pip 23.0.1 from /usr/lib/python3/dist-packages/pip (python 3.11)
```

***

## Step 3: Create and Activate a Virtual Environment

Isolating your project in a virtual environment prevents conflicts between package versions. Create a new virtual environment named "venv":

```bash theme={null}
root@ubuntu-host:~ ⟶ python3 -m venv venv
```

Check that the `venv` directory has been created:

```bash theme={null}
root@ubuntu-host:~ ⟶ ls -l
total 4
drwxr-xr-x 5 root root 4096 Dec 18 14:12 venv
```

Inside the `venv` folder, you will find several subdirectories and files:

```bash theme={null}
root@ubuntu-host:~ ⟶ ls -l venv/
total 16
drwxr-xr-x 2 root root 4096 Dec 18 14:12 bin
drwxr-xr-x 2 root root 4096 Dec 18 14:12 include
drwxr-xr-x 3 root root 4096 Dec 18 14:12 lib
lrwxrwxrwx 1 root root   14 Dec 18 14:12 lib64 -> lib
-rw-r--r-- 1 root root  149 Dec 18 14:12 pyvenv.cfg
```

Activate the virtual environment with:

```bash theme={null}
root@ubuntu-host:~ ⟶ source venv/bin/activate
```

Your prompt should now indicate that you are working within the virtual environment. You can safely install packages using pip without affecting the global Python installation.

***

## Step 4: Install PyTorch, TorchVision, and TorchAudio

With the virtual environment activated, install PyTorch and its related libraries via pip. This command also pulls in necessary NVIDIA libraries if a GPU is detected:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 (venv) ➜ pip3 install torch torchvision torchaudio
```

The installation will display output similar to:

```plaintext theme={null}
Collecting torch
Downloading torch-2.5.1-cp311-cp311-manylinux1_x86_64.whl (906.5 MB)
Collecting torchvision
Downloading torchvision-0.20.1-cp311-cp311-manylinux1_x86_64.whl (7.2 MB)
Collecting torchaudio
Downloading torchaudio-2.5.1-cp311-cp311-manylinux1_x86_64.whl (3.4 MB)
...
```

This confirms that PyTorch along with TorchVision and TorchAudio (plus their dependencies) have been installed in your isolated environment.

***

## Step 5: Verify the Installation

To check that all packages installed correctly, list the installed packages using:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 (venv) ➜ pip3 list
```

For reproducibility, you can generate a requirements file:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 (venv) ➜ pip3 freeze > requirements.txt
```

Review the generated file:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 (venv) ➜ cat requirements.txt
```

The file should contain entries like:

```plaintext theme={null}
filelock==3.16.1
fsspec==2024.10.0
Jinja2==3.1.4
MarkupSafe==3.0.2
...
torch==2.5.1
torchaudio==2.5.1
torchvision==0.20.1
```

Next, validate that PyTorch operates as expected by opening a Python interpreter:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 (venv) ➜ python3
```

Inside the interactive shell, run:

```python theme={null}
import torch
print(torch.__version__)  # Expected output: 2.5.1+cu124 (or similar)
print(torch.rand(2, 4))   # Generates a random 2x4 tensor
```

Optionally, check for CUDA-enabled GPU availability:

```python theme={null}
print(torch.cuda.is_available())
```

This returns True if a CUDA device is available, else it returns False. Exit the interpreter by pressing Ctrl+D.

***

## Step 6: Deactivate the Virtual Environment

Once you've completed testing, deactivate the virtual environment to return to the global Python state:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 (venv) ➜ deactivate
```

Running `pip3 list` in the global environment will now display only basic packages (e.g., pip, setuptools, wheel) without the additional PyTorch and NVIDIA libraries.

To double-check, reactivate your virtual environment and list its installed packages:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 ➜ source venv/bin/activate
root@ubuntu-host:~ via 🐍 v3.11.4 (venv) ➜ pip3 list
```

***

## Step 7: Reproducing Your Virtual Environment

Reproducibility is key when collaborating or migrating between machines. First, create a new virtual environment (named "venv2"):

```bash theme={null}
root@ubuntu-host:~ via v3.11.4 ↣ python3 -m venv venv2
```

Verify both virtual environments exist:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 ➜ ls -l
total 12
-rw-r--r-- 1 root root   595 Dec 18 14:16 requirements.txt
drwxr-xr-x 6 root root  4096 Dec 18 14:14 venv
drwxr-xr-x 5 root root  4096 Dec 18 14:24 venv2
```

Activate the new environment:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 ➜ source venv2/bin/activate
```

Your new environment is minimal. Install all dependencies using the previously generated `requirements.txt`:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 (venv2) ➜ pip3 install -r requirements.txt
```

After installation, validate the PyTorch version by starting Python:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 (venv2) ➜ python3
```

Then execute:

```python theme={null}
import torch
print(torch.__version__)  # Expected output: 2.5.1+cu124 (or similar)
```

Exit the interpreter and deactivate the environment:

```bash theme={null}
root@ubuntu-host:~ via 🐍 v3.11.4 (venv2) ➜ deactivate
```

<Callout icon="lightbulb">
  Generating a `requirements.txt` file helps ensure your project’s environment can be perfectly replicated on another machine, thereby improving collaboration efficiency.
</Callout>

***

## Conclusion

In this guide, you learned how to:

* Update an Ubuntu system and verify Python installation.
* Install pip and create a Python virtual environment.
* Install PyTorch along with TorchVision and TorchAudio in an isolated environment.
* Verify the installation and generate a reproducible `requirements.txt` file.
* Reproduce the virtual environment on another instance.

By following these steps, you ensure that your development environment is consistent and easily shareable. Happy coding with PyTorch!

***

## Additional Resources

* [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
* [Python Virtual Environments Guide](https://docs.python.org/3/library/venv.html)
* [Understanding CUDA in PyTorch](https://pytorch.org/docs/stable/notes/cuda.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/5a59db15-2490-4be0-a894-4b3d3cc78fac/lesson/22b81745-1782-4121-8e27-2d1a632fda0f" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/pytorch/module/5a59db15-2490-4be0-a894-4b3d3cc78fac/lesson/c496c2d8-6495-4274-b1d9-53234081e334" />
</CardGroup>
