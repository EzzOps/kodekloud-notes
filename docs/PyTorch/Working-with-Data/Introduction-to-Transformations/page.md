# Load the image using Pillow
original_image = Image.open('images/cat/cat-1.jpg')
print(original_image)

# Display the loaded image
display_images(original_image=original_image)
```

<Frame>
  ![The image shows a Jupyter Notebook interface with text discussing improving model accuracy and pipelines using PyTorch transformations. It includes a conclusion and a note about using transformations for image classification models.](https://kodekloud.com/kk-media/image/upload/v1752883304/notes-assets/images/PyTorch-Demo-Introduction-to-Transformations/jupyter-notebook-pytorch-transformations.jpg)
</Frame>

***

## Resizing an Image

Resizing ensures consistent image dimensions across your dataset. In the example below, we resize the image to 50×25 pixels using the PyTorch v2 API.

```python theme={null}
# Using v2 Resize transform to set image dimensions to 50x25 pixels
resize_transform = v2.Resize((50, 25))
resized_image = resize_transform(original_image)

# Display the resized image
display_images(original_image=original_image, new_image=resized_image, new_image_name="Resized Image")
```

For those who prefer the v1 API, the same operation can be implemented as follows:

```python theme={null}
# Using v1 transforms.Resize for the identical operation
resize_transform = transforms.Resize((50, 25))
resized_image = resize_transform(original_image)
display_images(original_image=original_image, new_image=resized_image, new_image_name="Resized Image")
```

***

## Random Horizontal Flip

Random horizontal flips augment your dataset by mirroring images randomly. In this demonstration, we set the flip probability to 100% (p=1) for clarity.

```python theme={null}
# Random horizontal flip with 100% probability
rh_transform = v2.RandomHorizontalFlip(p=1)
rhf_image = rh_transform(original_image)
display_images(original_image=original_image, new_image=rhf_image, new_image_name="Random Horizontal Flip")
```

<Callout icon="lightbulb">
  For real-world applications, consider using a probability less than 1 (e.g., p=0.5) to introduce randomness in augmentation.
</Callout>

***

## Converting Images to Tensors

Before feeding images into a PyTorch model, they must be converted into tensors. This transformation scales pixel intensity values appropriately for model consumption.

```python theme={null}
from torchvision.transforms import ToTensor

# Convert image to tensor
tensor_transform = ToTensor()
tensor_image = tensor_transform(original_image)

print(f"Original Image: {original_image}")
print(f"Tensor Image: \n{tensor_image}")
```

***

## Normalizing Tensor Images

Normalization adjusts pixel intensity values to a standardized range, which is crucial for faster model convergence. Here, we normalize the tensor with a mean and standard deviation of (0.5, 0.5, 0.5).

```python theme={null}
# Normalize the tensor image
normalize_transform = v2.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
normalized_image = normalize_transform(tensor_image)

# Display normalized tensor along with the original tensor for comparison
print(normalized_image)
print(tensor_image)
```

<Callout icon="lightbulb">
  Normalization typically shifts the pixel values to a range between -1 and 1, promoting efficient model training.
</Callout>

***

## Random Cropping

Random cropping extracts a fixed-size region from an image, which is useful for data augmentation. In this example, we extract a 100×100 pixel patch.

```python theme={null}
# Randomly crop a 100x100 pixel region from the image
rc_transform = v2.RandomCrop(size=(100, 100))
rc_image = rc_transform(original_image)
display_images(original_image=original_image, new_image=rc_image, new_image_name="Random Crop")
```

Running the transformation multiple times yields crops from different parts of the image.

<Frame>
  ![The image shows two side-by-side pictures of a cat on a black background. The left is labeled "Original Image," and the right is labeled "Random Crop," showing a slightly different framing of the cat.](https://kodekloud.com/kk-media/image/upload/v1752883305/notes-assets/images/PyTorch-Demo-Introduction-to-Transformations/cat-original-random-crop.jpg)
</Frame>

***

## Random Photometric Distortion

Photometric distortion augments images by adjusting brightness, contrast, saturation, and hue. This increases the variation in lighting conditions, helping to improve model generalization.

```python theme={null}
# Create a photometric distortion transform with specified parameter ranges
rpd_transform = v2.RandomPhotometricDistort(
    brightness=(0.875, 1.125),
    contrast=(0.5, 1.5),
    saturation=(0.5, 1.5),
    hue=(-0.05, 0.05),
    p=1
)

# Apply photometric distortion
rpd_image = rpd_transform(original_image)
display_images(original_image=original_image, new_image=rpd_image, new_image_name="Random Photometric Distort")
```

<Callout icon="lightbulb">
  Try changing the parameter ranges to see how variations in brightness and saturation impact the overall image appearance.
</Callout>

***

## Random Resize

Random resizing applies variable scaling to images, introducing additional diversity into the dataset. Here, the image is randomly resized to a pixel size between 100 and 200.

```python theme={null}
# Randomly resize the image between 100 and 200 pixels
rr_transform = v2.RandomResize(min_size=100, max_size=200)
rr_image = rr_transform(original_image)
display_images(original_image=original_image, new_image=rr_image, new_image_name="Random Resize")
```

<Frame>
  ![The image shows two side-by-side pictures of a cat against a black background. The left is labeled "Original Image," and the right is labeled "Random Resize."](https://kodekloud.com/kk-media/image/upload/v1752883306/notes-assets/images/PyTorch-Demo-Introduction-to-Transformations/cat-original-random-resize.jpg)
</Frame>

***

## Building Transformation Pipelines with Compose

The Compose class enables you to chain multiple transformations together into a single, streamlined pipeline. This approach ensures that every image undergoes the same sequence of augmentations.

```python theme={null}
# Build a transformation pipeline combining several augmentations
transforms_pipeline = v2.Compose([
    v2.RandomCrop(size=(100, 100)),
    v2.RandomPhotometricDistort(
        brightness=(0.875, 1.125),
        contrast=(0.5, 1.5),
        saturation=(0.5, 1.5),
        hue=(-0.05, 0.05),
        p=1,
    ),
    v2.RandomResize(min_size=75, max_size=150),
    v2.RandomHorizontalFlip(p=1)
])

# Apply the pipeline to the original image
pipeline_image = transforms_pipeline(original_image)
```

After applying the pipeline, you can view the transformed image as shown below:

```python theme={null}
display_images(original_image=original_image, new_image=pipeline_image, new_image_name="Pipeline Image")
```

<Callout icon="lightbulb">
  Using a transformation pipeline streamlines preprocessing and ensures consistency across your training data.
</Callout>

***

## Applying Transformations to a Dataset

Next, we integrate a transformation pipeline with a real dataset: the Fashion MNIST dataset from TorchVision.

```python theme={null}
import torchvision.datasets

# Create a FashionMNIST dataset without any transformation
original_image_dataset = torchvision.datasets.FashionMNIST(root='./fashion', train=False, download=True)

# Retrieve and display an image from the dataset
original_image, label = original_image_dataset[2]
display_images(original_image=original_image)
```

Now, we define a transformation pipeline tailored to the smaller dimensions of Fashion MNIST images:

```python theme={null}
# Construct a pipeline tailored to Fashion MNIST image size
transforms_pipeline = v2.Compose([
    v2.RandomCrop(size=(15, 15)),
    v2.RandomPhotometricDistort(
        brightness=(0.875, 1.125),
        contrast=(0.5, 1.5),
        saturation=(0.5, 1.5),
        hue=(-0.05, 0.05),
        p=1
    ),
    v2.RandomResize(min_size=10, max_size=15),
    v2.RandomHorizontalFlip(p=1)
])
```

You can integrate these transformations into the dataset by passing the pipeline as the `transform` argument:

```python theme={null}
# Create a new dataset where each image is augmented by the pipeline
transformed_image_dataset = torchvision.datasets.FashionMNIST(
    root='./fashion', train=False, download=True, transform=transforms_pipeline
)

# Retrieve a transformed image and display it alongside the original
transformed_image, label = transformed_image_dataset[2]
display_images(original_image=original_image, new_image=transformed_image, new_image_name="Transformed Fashion MNIST Image")
```

***

## Conclusion

In this lesson, we explored a variety of image transformation techniques using PyTorch’s TorchVision library. We covered resizing, flipping, cropping, photometric adjustments, normalization, and composing pipelines—all critical steps for effective image preprocessing and data augmentation. These techniques not only standardize your dataset but also improve model robustness and performance. Experiment with these transformations to optimize the augmentation strategies for your projects.

<Frame>
  ![The image shows two side-by-side visualizations labeled "Original Image" and "Pipeline Image," depicting a transformation process with color-coded pixel data.](https://kodekloud.com/kk-media/image/upload/v1752883307/notes-assets/images/PyTorch-Demo-Introduction-to-Transformations/original-pipeline-image-transformation.jpg)
</Frame>

Thank you for following along, and happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/f9d4b50b-328e-4cf7-a22a-3b236bf0abcd/lesson/be1aae10-5f0d-4206-8781-c7e3b18c9316" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/pytorch/module/f9d4b50b-328e-4cf7-a22a-3b236bf0abcd/lesson/94c8b52a-7e06-4689-a5c4-135c09a0e5c7" />
</CardGroup>


# Introduction to Transformations

Source: https://notes.kodekloud.com/docs/PyTorch/Working-with-Data/Introduction-to-Transformations/page

This lesson explores using transformations to prepare and enhance image data for training models in PyTorch, improving robustness and reducing overfitting.

In this lesson, we explore how to use transformations to prepare and enhance image data for training models in PyTorch. These techniques introduce variety into your dataset, allowing models to learn robust features and generalize effectively to new data. Transformations are a crucial preprocessing step that not only standardizes input images but also augments the dataset to reduce overfitting.

Transformations serve two primary purposes:

1. **Preprocessing:** Resize images to a uniform dimension and normalize pixel values to ensure consistency across the dataset.
2. **Data Augmentation:** Apply operations such as rotating, flipping, and cropping to generate multiple modified versions of each image. This variation helps the model perform well on unseen data by reducing the risk of overfitting.

<Callout icon="lightbulb">
  Benefits of data transformations include improved preprocessing, effective data augmentation, and enhanced generalization, which collectively reduce overfitting.
</Callout>

<Frame>
  ![The image explains the benefits of transforming data, highlighting preprocessing, data augmentation, improved learning, and preventing overfitting.](https://kodekloud.com/kk-media/image/upload/v1752883308/notes-assets/images/PyTorch-Introduction-to-Transformations/data-transformation-benefits-diagram.jpg)
</Frame>

Overfitting, which is discussed later in more detail, can be mitigated effectively using these augmentation techniques. The TorchVision Transforms module in PyTorch simplifies the application of these transformations, offering easy-to-use operations for resizing, converting images to tensors, normalizing pixel values, and applying various augmentation methods.

For example, here is a simple import statement to get started with TorchVision Transforms:

```python theme={null}
