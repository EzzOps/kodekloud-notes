# ML Training Process

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/ML-Training-Process/page

Overview of machine learning training processes, including data splitting, training loops, loss functions, optimizers, gradient descent variants, and common terminology for model development and evaluation

Machine learning (ML) is the process of teaching a model to discover patterns in data and map inputs to outputs. In supervised learning, training teaches a model how to map an input `x` (a feature or data point) through a function `f(x)` to produce a prediction `y_hat` that approximates the true label `y`. Training adjusts model parameters so predictions align with real outcomes.

Key components of a training loop include labeled training data, a learning algorithm to adjust parameters, a loss function to quantify error, and an optimizer to update parameters using gradients computed from the loss.

<Frame>
  <img alt="The image is a diagram explaining machine learning (ML) training. It illustrates the flow between input, a learning model, a learning algorithm, and output, highlighting parameter updates and error functions." />
</Frame>

Core inputs required to start training:

* A training dataset (features + labels).
* A validation dataset (and ideally a separate test dataset) for evaluation.
* A chosen model architecture (e.g., XGBoost, CNN).
* A loss function that quantifies prediction error.
* An optimizer to update model parameters.
* Hyperparameters such as learning rate, batch size, and number of epochs.

These building blocks define the training environment and determine how effectively a model learns.

<Frame>
  <img alt="The image illustrates key inputs in a training process, including elements like training and validation datasets, model architecture, optimizer, loss function, and hyperparameters." />
</Frame>

## Data splitting and validation

To evaluate generalization, datasets are typically partitioned into training and validation/test sets. A common heuristic is to allocate roughly 80% of data to training and 20% to validation/testing; however, the exact split depends on dataset size and domain constraints. Cross-validation is another common strategy to make efficient use of limited data.

<Frame>
  <img alt="The image illustrates the division of raw data into a training dataset (80%) and a validation dataset." />
</Frame>

## Training loop: forward and backward passes

A typical training iteration performs the following steps:

1. Input `X` — the features or data points.
2. Forward pass through the model `f(x)` to produce predictions `y_hat`.
3. Compare predictions with true labels `y`.
4. Compute the loss using a chosen loss function.
5. Compute gradients of the loss with respect to model parameters (backpropagation).
6. Optimizer updates parameters using the gradients.
7. Repeat across batches and epochs until convergence or stopping criteria are met.

The forward pass simply computes predictions and the loss—no parameters are changed. The backward pass computes gradients of the loss and is where learning happens via parameter updates.

<Frame>
  <img alt="The image is a flowchart depicting the backward pass in machine learning training, showing steps from input to model output, error calculation, gradient computation, and weight updates." />
</Frame>

## Loss functions — measuring prediction error

Loss functions quantify how far predictions are from true values and guide parameter updates. Choose a loss that matches your task (regression vs classification) and the sensitivity you want to outliers.

Common regression losses:

* Absolute Error for a single data point: `|y_hat - y|`
* Mean Absolute Error (MAE) for `n` points:
  ```text theme={null}
  MAE = (1/n) * sum_i |y_hat_i - y_i|
  ```

<Frame>
  <img alt="The image explains loss functions, showing formulas for Absolute Error and Mean Absolute Error in a mathematical context." />
</Frame>

To penalize large errors more strongly, use squared differences:

* Mean Squared Error (MSE):
  ```text theme={null}
  MSE = (1/n) * sum_i (y_hat_i - y_i)^2
  ```

Squaring amplifies large deviations and thus places greater emphasis on outliers during training.

<Frame>
  <img alt="The image shows the formula for the Mean Squared Error (MSE) as a loss function, explaining it penalizes large errors by squaring the differences. It highlights the use of squaring instead of taking the absolute value." />
</Frame>

Classification losses:

* Binary Cross-Entropy (log loss) for binary classification: penalizes confident but incorrect probability estimates.
* Categorical Cross-Entropy (paired with softmax) for multi-class classification: generalizes binary cross-entropy to multiple classes.

<Frame>
  <img alt="The image shows the formula for a loss function, which is used to penalize wrong predictions in machine learning." />
</Frame>

<Callout icon="lightbulb">
  Choose the loss function that matches your task (regression vs classification) and the scale/sensitivity you want for errors (e.g., `MAE` vs `MSE`). Consider robustness to outliers and the effect on gradient magnitudes when selecting a loss.
</Callout>

Loss functions summary

| Loss function             | Use case                   | Notes                                                            |
| ------------------------- | -------------------------- | ---------------------------------------------------------------- |
| `MAE`                     | Regression                 | Robust to outliers, linear penalty.                              |
| `MSE`                     | Regression                 | Penalizes large errors more heavily (sensitive to outliers).     |
| Binary Cross-Entropy      | Binary classification      | Works with sigmoid outputs; penalizes confident errors strongly. |
| Categorical Cross-Entropy | Multi-class classification | Use with softmax outputs for mutually exclusive classes.         |

## Optimizers — updating parameters

Optimizers use gradients from the loss to update model parameters and reduce error over training. Selection of an optimizer and its hyperparameters (e.g., learning rate) can greatly affect convergence speed and final performance.

Common optimizers:

* Stochastic Gradient Descent (SGD): simple, updates parameters using estimated gradients (often per batch); can be noisy but may generalize well.
* Momentum-based methods: accelerate convergence by accumulating past gradients (e.g., SGD with momentum).
* Adam: combines momentum and per-parameter adaptive learning rates for faster, often robust convergence.
* Adagrad, RMSprop: adaptive learning-rate methods suitable for sparse or non-stationary problems.

<Frame>
  <img alt="The image illustrates the process of optimization in machine learning, showing the flow from input to gradient computation and weight update, with common optimizers like SGD and Adam highlighted." />
</Frame>

Optimizers are mathematical procedures that decide how to change parameters after each training step using the gradient of the loss as guidance. Different optimizers adjust step size and direction in different ways, affecting stability and speed.

<Frame>
  <img alt="The image is a diagram explaining the process of optimization in machine learning, showing the flow from predicted and true outputs through loss functions and optimizers, culminating in updating the weights and repeating the process." />
</Frame>

Optimizers summary

| Optimizer             | Strengths                                   | Typical use                            |
| --------------------- | ------------------------------------------- | -------------------------------------- |
| `SGD`                 | Simple, good generalization                 | Baselines, large-scale training        |
| `SGD + Momentum`      | Faster convergence, smoother updates        | Deep networks where acceleration helps |
| `Adam`                | Adaptive per-parameter LR, fast convergence | Default for many deep-learning tasks   |
| `RMSprop` / `Adagrad` | Adaptive learning rates                     | Sparse gradients or specific tasks     |

## Gradient descent variants

Gradient descent is the foundation of most optimizers. Variants:

* Batch Gradient Descent: compute gradients over the whole dataset (stable but slow for large datasets).
* Stochastic Gradient Descent (SGD): update using one sample at a time (fast but noisy).
* Mini-batch Gradient Descent: compute gradients on small batches — most commonly used in practice.

Gradient descent update rule (single step):

```latex theme={null}
\[
\theta_{t+1} = \theta_{t} - \eta \cdot \nabla_{\theta} L(\theta_{t})
\]
```

Where `\theta_t` are parameters at step `t`, `\eta` is the learning rate, and `\nabla_{\theta} L` is the gradient of the loss with respect to parameters.

## Common training terms

* Epoch: one complete pass through the entire training dataset.
* Batch: a subset of the dataset processed together in one forward/backward pass.
* Iteration: one parameter update (i.e., processing one batch). Iterations per epoch = `dataset_size / batch_size`.

Example: a dataset of 10,000 samples with batch size 100 yields 100 iterations per epoch. Training for 100 epochs results in 10,000 total iterations.

<Callout icon="warning">
  Don't confuse iterations and epochs: an iteration performs one parameter update on a batch, while an epoch processes the entire dataset once (many iterations per epoch).
</Callout>

Further reading and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (useful for deploying models)
* [TensorFlow Guide](https://www.tensorflow.org/guide)
* [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
* [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/d05c8e28-4593-48a9-8e19-62d881d54373" />
</CardGroup>
