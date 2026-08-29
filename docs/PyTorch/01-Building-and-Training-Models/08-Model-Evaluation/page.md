# Model Evaluation

Source: https://notes.kodekloud.com/docs/PyTorch/Building-and-Training-Models/Model-Evaluation/page

This article discusses the process and importance of model evaluation in machine learning, including metrics, overfitting, and practical implementation techniques.

In this lesson, we trained three distinct models: a custom model from scratch and two models leveraging transfer learning. Now, we need to select the best candidate for deployment in production. Before making that decision, a thorough model evaluation must be performed.

<Frame>
  ![The image is a flowchart comparing three models: "Custom Model from Scratch," "Transfer Learning Model 1," and "Transfer Learning Model 2," with the latter being selected for model evaluation and deployment.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883143/notes-assets/images/PyTorch-Model-Evaluation/model-comparison-flowchart-transfer-learning.jpg)
</Frame>

Model evaluation is the process of assessing a machine learning model's performance on unseen data. It verifies whether the model has effectively captured the underlying patterns in the training data and can generalize to new examples. Think of it as administering a test to the model using questions it hasn't seen before.

To perform the evaluation, we use a separate dataset—commonly known as the test dataset—which is not used during the training phase. By comparing the model's predictions with the true labels, we can determine its effectiveness.

<Frame>
  ![The image is a slide titled "Introduction to Model Evaluation," highlighting two key points: assessing model performance on unseen data and ensuring effective pattern learning and generalization.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883144/notes-assets/images/PyTorch-Model-Evaluation/introduction-to-model-evaluation.jpg)
</Frame>

<Frame>
  ![The image is a flowchart titled "Introduction to Model Evaluation," showing the process from "Test Data" to "ML Model" to "Predictions."](../../../../images/kodekloud.com/kk-media/image/upload/v1752883145/notes-assets/images/PyTorch-Model-Evaluation/introduction-to-model-evaluation-flowchart.jpg)
</Frame>

This evaluation process enables us to compute metrics such as accuracy—which reflects how many predictions are correct—as well as precision and recall, which provide more detailed insights especially when dealing with imbalanced datasets.

<Frame>
  ![The image is an introduction to model evaluation, showing a flow between predictions and correct answers, and explaining that accuracy shows correct predictions while precision and recall assess detection of specific events.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883147/notes-assets/images/PyTorch-Model-Evaluation/model-evaluation-introduction-flow.jpg)
</Frame>

Evaluating a model is crucial because a model that performs exceptionally well on training data might still fail in real-world scenarios due to overfitting. Overfitting happens when the model memorizes the training data rather than learning generalizable patterns. By rigorously testing on unseen data, we can detect such issues and choose the model that best meets our operational requirements.

<Frame>
  ![The image outlines the importance of model evaluation, highlighting three points: ensuring models generalize beyond training data, detecting overfitting and genuine learning, and comparing models to find the best fit.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883148/notes-assets/images/PyTorch-Model-Evaluation/model-evaluation-importance-diagram.jpg)
</Frame>

It also helps pinpoint weaknesses, such as difficulty handling specific input types, thereby allowing us to make necessary improvements before deployment.

## Training vs. Validation Loss

During model training, we compute two key loss metrics: training loss and validation loss. These metrics provide insights into how well the model learns from the provided data.

* **Training Loss:** This metric measures error on the training dataset, which the model uses to iterate and optimize its parameters through methods like gradient descent. A low training loss indicates that the model is learning from the training data, but it doesn't guarantee good generalization.

* **Validation Loss:** This loss is computed on an unseen validation dataset after each training epoch (without updating the model parameters). A large discrepancy between training and validation loss is a strong indicator of overfitting.

Monitoring these metrics together helps in deciding when to stop the training process. If training loss decreases continually while validation loss increases, it signifies that the model is overfitting.

<Frame>
  ![The image shows a graph comparing training and validation loss over epochs, illustrating overfitting, along with three key points about monitoring these losses during model training.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883149/notes-assets/images/PyTorch-Model-Evaluation/training-validation-loss-graph.jpg)
</Frame>

A balanced training approach will yield similar training and validation loss values over time.

## Overfitting vs. Underfitting

Two common challenges during model training are overfitting and underfitting:

* **Underfitting:** Occurs when the model is too simple to capture the underlying trends in the data, resulting in poor performance on both training and test datasets.

* **Overfitting:** Happens when a model is overly complex and starts to memorize the training data instead of learning generalizable patterns. Even though it might perform excellently on the training set, its performance on new, unseen data deteriorates.

<Frame>
  ![The image compares underfitting and overfitting in machine learning models, highlighting their characteristics and effects on data performance.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883150/notes-assets/images/PyTorch-Model-Evaluation/underfitting-overfitting-machine-learning-comparison.jpg)
</Frame>

The goal is to strike a balance where the model can generalize well without falling into the traps of underfitting or overfitting.

## Evaluation Metrics

Model evaluation employs several metrics to quantify performance:

* **Accuracy:** Represents the ratio of correctly predicted instances to the total predictions. While accuracy is easy to compute, it can be misleading for imbalanced datasets.

<Frame>
  ![The image is a slide titled "Metrics" listing four metrics: Accuracy, Precision, Recall, and F1 Score, with a focus on Accuracy, explaining it as the ratio of correct predictions to total predictions, noting it's easy to calculate but can be misleading for imbalanced datasets.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883151/notes-assets/images/PyTorch-Model-Evaluation/metrics-accuracy-precision-recall-f1.jpg)
</Frame>

* **Precision:** Indicates the ratio of true positive predictions to all positive predictions made by the model. This metric is vital in scenarios where false positives carry a high cost, such as spam detection or medical diagnosis.

* **Recall:** Denotes the ratio of true positive predictions to all actual positive cases, focusing on the model's ability to identify all positive instances. It is especially important in fields like disease detection and fraud monitoring.

<Frame>
  ![The image shows a list of metrics including Accuracy, Precision, Recall, and F1 Score, with a focus on Recall, explaining its importance in minimizing false positives and its application in fields like disease and fraud detection.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883153/notes-assets/images/PyTorch-Model-Evaluation/recall-metrics-importance-diagram.jpg)
</Frame>

* **F1 Score:** This is the harmonic mean of precision and recall. It provides a single metric that balances both false positives and false negatives, making it useful when you need a balance between precision and recall.

<Frame>
  ![The image shows a list of metrics including Accuracy, Precision, Recall, and F1 Score, with a focus on F1 Score, described as the harmonic mean of Precision and Recall, balancing both.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883154/notes-assets/images/PyTorch-Model-Evaluation/f1-score-precision-recall-metrics.jpg)
</Frame>

## The Confusion Matrix

A confusion matrix is an essential tool for evaluating classification models. It offers a detailed breakdown by comparing actual labels with the model’s predictions and categorizing them as follows:

* **True Positives:** Both predicted and actual labels are positive (e.g., both are "dog").
* **True Negatives:** Both predicted and actual labels are negative.
* **False Positives:** The model predicts positive while the actual label is negative.
* **False Negatives:** The model predicts negative while the actual label is positive.

<Frame>
  ![The image is a confusion matrix illustrating predictions of "Dog" and "Not Dog" with categories for true positives, false positives, and true negatives.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883155/notes-assets/images/PyTorch-Model-Evaluation/confusion-matrix-dog-predictions.jpg)
</Frame>

This matrix is the foundation for computing metrics like accuracy, precision, and recall.

<Frame>
  ![The image is a diagram explaining a confusion matrix, detailing the concepts of accuracy, precision, and recall with their respective formulas.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883156/notes-assets/images/PyTorch-Model-Evaluation/confusion-matrix-accuracy-precision-recall.jpg)
</Frame>

## Model Evaluation in Practice

Evaluating a model often mirrors the approach used during training, but with key distinctions. In evaluation, we use a test loop where gradient computation is disabled using PyTorch’s `no_grad` function. This approach reduces memory usage and enhances computational speed.

Below is an example showcasing both a training loop (for context) and a test loop used for evaluation:

```python theme={null}
