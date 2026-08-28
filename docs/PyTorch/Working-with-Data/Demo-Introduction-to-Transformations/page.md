# Let's begin with preloaded audio files
import torchaudio.datasets

# Create a dataset using DR_VCTK (Device Recorded VCTK)
audio_dataset = torchaudio.datasets.DR_VCTK(root='./audio', subset='test', download=True)
```

Once the download is complete, you can inspect the `./audio` folder to explore the dataset.

***

## Preloaded Image Datasets

Next, we explore preloaded image datasets using TorchVision. In this example, we use the FashionMNIST classification dataset. A transformation is applied to convert images to tensors for further processing.

```python theme={null}
import torchvision.datasets
from torchvision.transforms import ToTensor

# Create a dataset from the FashionMNIST classification dataset
image_dataset = torchvision.datasets.FashionMNIST(
    root='./fashion',
    train=False,
    download=True,
    transform=ToTensor()
)
```

After downloading, the dataset is stored in the "fashion" directory. You can inspect the class labels and index mapping as shown below:

```python theme={null}
# Display dataset classes and their index mapping
print(image_dataset.classes)
print(image_dataset.class_to_idx)

# Create a reversed mapping for readability
class_to_index_map = image_dataset.class_to_idx
index_to_class_map = {v: k for k, v in class_to_index_map.items()}
print(index_to_class_map)
```

For FashionMNIST, the classes are:

```text theme={null}
['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
```

with indices ranging from 0 to 9.

### Visualizing the FashionMNIST Dataset

Visualizing a subset of the dataset helps to better understand the data. The following code randomly displays a grid of 9 images along with their labels:

```python theme={null}
import torch
import matplotlib.pyplot as plt

# Set up a plot for 9 random images
figure = plt.figure(figsize=(8, 8))
cols, rows = 3, 3
for i in range(1, cols * rows + 1):
    sample_idx = torch.randint(len(image_dataset), size=(1,)).item()
    img, label = image_dataset[sample_idx]
    figure.add_subplot(rows, cols, i)
    plt.title(index_to_class_map[label])
    plt.axis("off")
    plt.imshow(img.squeeze())
plt.show()
```

Alternatively, you can visualize the dataset with a different grid layout:

```python theme={null}
figure = plt.figure(figsize=(6, 8))
cols, rows = 3, 2
for i in range(1, cols * rows + 1):
    sample_idx = torch.randint(len(image_dataset), size=(1,)).item()
    img, label = image_dataset[sample_idx]
    figure.add_subplot(rows, cols, i)
    plt.title(index_to_class_map[label])
    plt.axis("off")
    plt.imshow(img.squeeze())
plt.show()
```

The grid maps numerical labels to human-friendly class names, making it easier to interpret the visualized data.

<Frame>
  ![The image shows a grid of heatmap-style visualizations of clothing items, including a dress, bag, T-shirt, and trousers, labeled accordingly. It appears to be part of a Jupyter Notebook interface, likely related to PyTorch DataLoaders.](https://kodekloud.com/kk-media/image/upload/v1752883302/notes-assets/images/PyTorch-Demo-Datasets-and-Dataloaders/clothing-heatmap-visualizations-jupyter.jpg)
</Frame>

***

## Working with DataLoaders

A DataLoader handles the batching and shuffling of your dataset during training. Below is an example that demonstrates how to create a DataLoader for the FashionMNIST dataset with a batch size of 64, ensuring that the data is shuffled during training.

```python theme={null}
from torch.utils.data import DataLoader

image_dataloader = DataLoader(
    dataset=image_dataset,
    batch_size=64,
    shuffle=True,
    num_workers=1
)
```

To evaluate a single batch, iterate over the DataLoader once:

```python theme={null}
# Retrieve one batch of images and labels
features, labels = next(iter(image_dataloader))
print(f"Features shape: {features.size()}")
print(f"Labels shape: {labels.size()}")
```

For example, the output might be:

```Python theme={null}
Features shape: torch.Size([64, 1, 28, 28])
Labels shape: torch.Size([64])
```

This confirms that each batch contains 64 grayscale images of size 28x28 along with their corresponding labels.

To further visualize a random image from the batch and display its human-readable label:

```python theme={null}
import random

# Select a random index from the batch
rand_idx = random.randint(0, labels.size(0) - 1)

# Extract the image and label
img = features[rand_idx].squeeze()
label = labels[rand_idx]

# Plot the image using a gray colormap for better clarity
plt.imshow(img, cmap='gray')
plt.show()

# Print the label and its corresponding class name
print(f"Label: {label} -> {index_to_class_map[label.item()]}")
```

Executing this code snippet repeatedly will display various images and their correct labels from the dataset.

***

## Creating a Custom Dataset

If you have your own image collection and corresponding labels, you can define a custom dataset using PyTorch’s Dataset class. In this example, we assume that image file paths and labels are stored in a CSV file named `labels.csv`.

<Callout icon="lightbulb">
  Ensure your CSV file is formatted correctly, as shown in the example below.
</Callout>

### Defining the Custom Dataset

Import the necessary modules and create a custom dataset class as follows:

```python theme={null}
from torch.utils.data import Dataset
import pandas as pd
from PIL import Image
from torchvision import transforms

class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, class_list):
        self.df = pd.read_csv(annotations_file)
        self.class_list = class_list

    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, index):
        image = Image.open(self.df.file_path[index])
        img_url = self.df.file_path[index]
        # Convert image to tensor
        convert_tensor = transforms.ToTensor()
        image = convert_tensor(image)
        label = self.class_list.index(self.df.label[index])
        return image, label, img_url
```

Assume your `labels.csv` is structured as follows:

```csv theme={null}
file_path,label
images/cat/cat-1.jpg,cat
images/cat/cat-2.jpg,cat
images/cat/cat-3.jpg,cat
images/cat/cat-4.jpg,cat
images/dog/dog-1.jpg,dog
images/dog/dog-2.jpg,dog
images/dog/dog-3.jpg,dog
images/dog/dog-4.jpg,dog
images/dog/dog-5.jpg,dog
```

Create an instance of your custom dataset with:

```python theme={null}
class_list = ["cat", "dog"]

custom_dataset = CustomImageDataset(annotations_file='labels.csv', class_list=class_list)
print(custom_dataset)
```

To inspect the dataset details, use:

```python theme={null}
print(f"Annotations data: \n{custom_dataset.df}")
print(f"Classes: {custom_dataset.class_list}")
```

Since the custom dataset does not automatically generate a mapping from class names to indices, you can create one manually:

```python theme={null}
custom_class_labels_map = {0: 'cat', 1: 'dog'}
```

### Visualizing the Custom Dataset

The following code snippet visualizes 9 random images from your custom dataset:

```python theme={null}
import torch
import matplotlib.pyplot as plt
from PIL import Image

# Set up the plot grid
figure = plt.figure(figsize=(8, 8))
cols, rows = 3, 3
for i in range(1, cols * rows + 1):
    sample_idx = torch.randint(len(custom_dataset), size=(1,)).item()
    # Retrieve the image path and label
    img_path, label = custom_dataset[sample_idx][2], custom_dataset[sample_idx][1]
    img = Image.open(img_path)
    figure.add_subplot(rows, cols, i)
    plt.title(label)
    plt.axis("off")
    plt.imshow(img)
plt.show()
```

Each execution displays different images along with their labels (e.g., 0 for cat, 1 for dog).

## Custom Dataset DataLoader

Similar to preloaded datasets, you can create a DataLoader for your custom dataset. Even if the dataset contains fewer images than the specified batch size (64 in this example), the DataLoader will return all available samples.

```python theme={null}
custom_dataloader = DataLoader(dataset=custom_dataset, batch_size=64, shuffle=True)

# Retrieve a batch from the custom DataLoader
features, labels, urls = next(iter(custom_dataloader))
print(f"Features shape: {features.size()}")
print(f"Labels shape: {labels.size()}")
```

For example, the output might be:

```Python theme={null}
Features shape: torch.Size([10, 3, 224, 224])
Labels shape: torch.Size([10])
```

To visualize a random image from this batch with its corresponding label:

```python theme={null}
rand_idx = random.randint(0, labels.size(0) - 1)
img = features[rand_idx]
label = labels[rand_idx]

plt.imshow(img.permute(1, 2, 0))  # Permute dimensions from (C, H, W) to (H, W, C)
plt.show()

print(f"Label: {label} -> {custom_class_labels_map.get(label.item())}")
```

Running this snippet multiple times will help validate that your custom dataset and its label mapping work correctly.

***

## Using TorchVision's ImageFolder

An efficient alternative for organizing images is to use TorchVision’s ImageFolder. When your images are arranged such that each class has its own subdirectory, ImageFolder automatically assigns labels based on these subdirectory names.

```python theme={null}
import torchvision
from torchvision import transforms

# Create a dataset using ImageFolder
image_folder_dataset = torchvision.datasets.ImageFolder(
    root="images",  # Directory containing class subdirectories
    transform=transforms.Compose([transforms.ToTensor()])
)
print(image_folder_dataset)
print(image_folder_dataset.classes)
print(image_folder_dataset.class_to_idx)
```

Load this dataset with a DataLoader:

```python theme={null}
image_folder_dataloader = DataLoader(image_folder_dataset, batch_size=64, shuffle=True)
```

To visualize a batch of images from the ImageFolder dataset:

```python theme={null}
# Retrieve one batch of images and labels
images, labels = next(iter(image_folder_dataloader))

fig, axes = plt.subplots(1, len(images), figsize=(8, 8))
for i, (img, label) in enumerate(zip(images, labels)):
    img = img.permute(1, 2, 0)  # Convert from (C, H, W) to (H, W, C)
    axes[i].imshow(img)
    axes[i].set_title(image_folder_dataset.classes[label])
    axes[i].axis("off")
plt.show()
```

This approach leverages the directory structure to automatically generate class labels, simplifying dataset creation when working with well-organized image folders.

<Frame>
  ![The image shows a grid of animal photos, including cats and dogs, with labels "0" and "1" above each image. It appears to be part of a dataset used in a coding environment.](https://kodekloud.com/kk-media/image/upload/v1752883303/notes-assets/images/PyTorch-Demo-Datasets-and-Dataloaders/animal-photos-dataset-grid.jpg)
</Frame>

***

## Conclusion

In this guide, we demonstrated techniques for working with preloaded datasets and DataLoaders in PyTorch, as well as methods for creating and visualizing custom datasets. These approaches help streamline data loading and preprocessing for model training, whether you’re using built-in libraries or your own data collections. Happy coding and exploring with PyTorch!

<Callout icon="lightbulb">
  For more details on PyTorch data handling, visit the [PyTorch Documentation](https://pytorch.org/docs/stable/index.html).
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/f9d4b50b-328e-4cf7-a22a-3b236bf0abcd/lesson/d5f6d294-6a83-4f19-8182-fa85c98fa487" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/pytorch/module/f9d4b50b-328e-4cf7-a22a-3b236bf0abcd/lesson/84df5a52-c34c-4810-8c04-4f5a504f88b7" />
</CardGroup>


# Demo Introduction to Transformations

Source: https://notes.kodekloud.com/docs/PyTorch/Working-with-Data/Demo-Introduction-to-Transformations/page

This article teaches PyTorch image transformations for data preprocessing and augmentation to enhance model performance and efficiency.

Welcome to this technical lesson on PyTorch image transformations. In this guide, you'll learn how to utilize PyTorch transformations for data preprocessing and augmentation to boost model performance and efficiency. PyTorch’s TorchVision library offers a comprehensive set of transformation classes that convert raw image data into formats that are optimized for model training and can augment your dataset by adding variability.

Below, we demonstrate various transformation techniques—including resizing, random horizontal flips, tensor conversion, normalization, random cropping, photometric distortions, random resizing, and building transformation pipelines with Compose—each explained with its corresponding code snippet.

***

## Helper Function to Display Images

We begin by defining a helper function to visualize the original image alongside its transformed version. This function is essential for comparing the effects of different transformations in real time.

```python theme={null}
import matplotlib.pyplot as plt

def display_images(original_image, new_image=None, new_image_name=None):
    """
    Helper function to display images.
    If a new image is provided, shows them side by side.
    """
    if new_image is not None:
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(original_image)
        axes[0].axis('on')  # Display axis for context
        axes[0].set_title('Original Image')
        axes[1].imshow(new_image)
        axes[1].axis('on')
        axes[1].set_title(new_image_name)
    else:
        plt.figure(figsize=(10, 5))
        plt.imshow(original_image)
        plt.axis('on')
    plt.show()
```

You can now use this function to visually compare the before and after images for every transformation applied.

***

## Loading an Image with Pillow and PyTorch Transforms

In this section, we load an image of a cat using the Pillow library while utilizing both version 2 and version 1 of the transform APIs.

```python theme={null}
from torchvision.transforms import v2
from torchvision import transforms
from PIL import Image
