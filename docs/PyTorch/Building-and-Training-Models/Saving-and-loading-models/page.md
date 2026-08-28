# Training Loop
for epoch in range(N_EPOCHS):
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch: {epoch} Loss: {running_loss / len(train_loader)}")

# Test Loop
model.eval()  # Set the model to evaluation mode
with torch.no_grad():  # Disable gradient computation
    for i, data in enumerate(test_loader, 0):
        inputs, labels = data
        outputs = model(inputs)
        _, preds = torch.max(outputs.data, 1)

# Metric calculation
print("metric calculation:")
```

In the test loop, the separate `test_loader` dataset is used to evaluate the model on unseen data. The use of `torch.no_grad()` is crucial as it temporarily disables gradient tracking during inference, significantly reducing memory consumption.

## Inference Paradigms

There are two primary paradigms for model inference:

* **Batch Inference:** This approach processes predictions on a group of inputs at once, making it ideal for non-time-sensitive tasks like generating weekly reports or analyzing historical data. It allows for efficient processing of large datasets.

* **Real-Time Inference:** In this scenario, predictions are generated instantly as individual inputs arrive. This method is critical for time-sensitive applications such as chatbots, fraud detection systems, or self-driving cars.

<Frame>
  ![The image compares batch inference and real-time inference, highlighting their uses and ideal applications. Batch inference is suited for non-time-sensitive tasks, while real-time inference is for time-sensitive applications.](https://kodekloud.com/kk-media/image/upload/v1752883157/notes-assets/images/PyTorch-Model-Evaluation/batch-vs-real-time-inference.jpg)
</Frame>

## Integrating TorchMetrics for Evaluation

For more efficient metric computation in our test loop, we can integrate the TorchMetrics library. TorchMetrics simplifies tracking of key performance metrics in PyTorch. It provides pre-built functions for metrics such as accuracy, precision, recall, and F1 score, and is compatible with both CPU and GPU. You can also define custom metrics if needed.

<Frame>
  ![The image is an informational graphic about "Torchmetrics," a Python library for calculating and tracking machine learning metrics, highlighting features like prebuilt metrics, PyTorch integration, and CPU/GPU support.](https://kodekloud.com/kk-media/image/upload/v1752883158/notes-assets/images/PyTorch-Model-Evaluation/torchmetrics-python-library-graphic.jpg)
</Frame>

Below is an example of how to use TorchMetrics within a test loop:

```python theme={null}
import torchmetrics

# Initialize the accuracy metric for multiclass classification
accuracy_metric = torchmetrics.Accuracy(task="multiclass", num_classes=N)

# Test Loop
model.eval()  # Set model to evaluation mode
with torch.no_grad():  # Disable gradient computation
    for i, data in enumerate(test_loader, 0):
        inputs, labels = data
        outputs = model(inputs)
        _, preds = torch.max(outputs.data, 1)
        # Update the accuracy metric with predictions and true labels
        accuracy_metric.update(preds, labels)

# Compute and display the overall accuracy
accuracy = accuracy_metric.compute()
print(f"Accuracy: {accuracy!r}")
```

In this workflow, the accuracy metric keeps track of statistics over each batch, and after the evaluation loop completes, the overall accuracy is computed and displayed.

## Alternative Evaluation Methods

In addition to TorchMetrics, other evaluation libraries such as Scikit-learn offer robust solutions and additional metrics:

* **Accuracy Score:** For overall prediction accuracy.
* **Classification Report:** Provides a detailed report including precision, recall, and F1 score.
* **Confusion Matrix:** Offers a granular breakdown of true vs. predicted labels.

<Frame>
  ![The image is an overview of the scikit-learn library, highlighting three features: Accuracy Score for overall accuracy, Classification Report for precision, recall, and F1-score, and Confusion Matrix for analyzing true vs. predicted classifications. It notes that the library is widely used and easy to integrate.](https://kodekloud.com/kk-media/image/upload/v1752883160/notes-assets/images/PyTorch-Model-Evaluation/scikit-learn-overview-accuracy-report.jpg)
</Frame>

These alternative tools allow for flexible and comprehensive model evaluation tailored to specific needs.

## Summary

In summary, model evaluation is critical for ensuring that a machine learning model generalizes well to unseen data. Key takeaways include:

* Monitoring both training and validation losses to detect overfitting or underfitting.
* Utilizing diverse evaluation metrics such as accuracy, precision, recall, and F1 score.
* Leveraging tools like the confusion matrix for detailed analysis of the model's performance.
* Integrating libraries such as TorchMetrics or Scikit-learn to streamline the evaluation process.
* Understanding the distinction between batch and real-time inference based on application requirements.
* Using PyTorch’s `no_grad()` function during evaluation to optimize memory usage and speed up inference.

<Frame>
  ![The image is a summary slide outlining key concepts in model evaluation, including metrics like accuracy and precision, and concepts like overfitting and underfitting. It also mentions the use of a confusion matrix for detailed analysis.](https://kodekloud.com/kk-media/image/upload/v1752883160/notes-assets/images/PyTorch-Model-Evaluation/model-evaluation-summary-accuracy-precision.jpg)
</Frame>

<Frame>
  ![The image is a summary slide discussing model inference, tools like Torchmetrics and Scikit-learn, and efficiency tips for PyTorch.](https://kodekloud.com/kk-media/image/upload/v1752883161/notes-assets/images/PyTorch-Model-Evaluation/model-inference-torchmetrics-scikit-learn.jpg)
</Frame>

<Callout icon="lightbulb">
  For optimal model performance, always validate using multiple metrics and choose the evaluation strategy that aligns with your application's requirements.
</Callout>

This concludes our discussion on model evaluation. In the next demo, we will walk through the complete process—from running the test loop to computing the final metrics—to further solidify these concepts in practice.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/pytorch/module/b8cb82ae-a284-41d1-8469-7e60705bbab8/lesson/509a2f12-7aeb-44cc-991f-231471c819a2" />
</CardGroup>


# Saving and loading models

Source: https://notes.kodekloud.com/docs/PyTorch/Building-and-Training-Models/Saving-and-loading-models/page

This article covers saving and loading models in PyTorch, including core functions, techniques for model management, and handling device differences.

As you build and refine models, it's essential to understand how to save and reload them. Whether you want to preserve a model for future use, transfer it between devices, or resume training later, PyTorch provides flexible tools to accomplish these tasks. In this guide, we cover core functions available in PyTorch—saving models, loading saved parameters, and running inference—so you walk away with practical techniques for effective model management.

<Frame>
  ![The image shows an agenda with four points related to PyTorch, focusing on saving and reloading models, flexible tools, core functions, and practical techniques for model management.](https://kodekloud.com/kk-media/image/upload/v1752883163/notes-assets/images/PyTorch-Saving-and-loading-models/pytorch-agenda-model-management.jpg)
</Frame>

Let's dive into the details.

## Why Save Your Models?

Training a model can take hours or even days. Saving your model allows you to:

* Reuse it without retraining
* Share your work with collaborators
* Deploy it immediately for inference
* Resume training at a later time

PyTorch offers three main functions for model serialization:

* `torch.save`
* `torch.load`
* `load_state_dict`

<Frame>
  ![The image is an introduction slide about PyTorch, highlighting three functions for saving and loading models: torch.save, torch.load, and load\_state\_dict.](https://kodekloud.com/kk-media/image/upload/v1752883163/notes-assets/images/PyTorch-Saving-and-loading-models/pytorch-saving-loading-models-intro.jpg)
</Frame>

## Core Saving and Loading Functions

### 1. Saving and Loading with torch.save and torch.load

• **torch.save**: Serialize various PyTorch objects (e.g., models, tensors, dictionaries) to a file using Python's pickle module.

```python theme={null}
torch.save(x, "model.pt")
```

For example, use this function to save a model's parameters.

• **torch.load**: The inverse of `torch.save`, this function deserializes the saved data back into memory.

```python theme={null}
torch.load("model.pt")
```

### 2. Using load\_state\_dict

The `load_state_dict` function is used to load a model's learnable parameters (weights and biases) from a previously saved state dictionary. Typically, you initialize a new model with the same architecture and then load the saved parameters into it.

```python theme={null}
model.load_state_dict(torch.load("model.pt"))
```

## Understanding state\_dict

A `state_dict` in PyTorch is a dictionary that holds all learnable parameters of a model, such as weights and biases. When saving a model, you usually serialize its `state_dict` because it contains the key information needed to restore the model later. Note that only layers with learnable parameters (like convolutional or linear layers) are included; non-learnable layers such as dropout are omitted.

Optimizers in PyTorch also maintain a `state_dict` that includes both their state and hyperparameters. The following image illustrates how state dictionaries capture essential parameters:

<Frame>
  ![The image explains the concept of state\_dict in machine learning, highlighting that it includes learnable parameters like convolutional and linear layers, but excludes non-learnable layers like dropout. It also notes that optimizers have their own state\_dict for state and hyperparameters.](https://kodekloud.com/kk-media/image/upload/v1752883164/notes-assets/images/PyTorch-Saving-and-loading-models/statedict-machine-learning-parameters.jpg)
</Frame>

## Saving Models for Inference

Inference involves using a trained model to make predictions on new, unseen data. The recommended approach in PyTorch is to save the model’s `state_dict`, then load it and switch the model to evaluation mode.

```python theme={null}
