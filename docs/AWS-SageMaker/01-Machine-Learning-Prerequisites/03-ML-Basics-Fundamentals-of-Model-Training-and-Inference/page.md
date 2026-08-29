# Linear model (symbolic)
# f(x) = w1*x1 + w2*x2 + w3*x3 + w4*x4 + w5*x5 + b
```

## Training objective and loop

Training optimizes parameters (w1…w5 and b) to minimize a loss function. For regression, the mean squared error (MSE) or sum of squared errors is common. For a single sample:

```python theme={null}
# Squared error for a single example
# error = (f(x) - y) ** 2
```

Training proceeds iteratively:

1. Initialize parameters (randomly or with sensible defaults).
2. Compute predictions f(x) for training samples.
3. Compute the loss (how far predictions differ from targets).
4. Adjust parameters to reduce the loss (gradient descent or another optimizer).
5. Repeat until convergence or another stopping condition.

The following diagram summarizes prediction, error computation, and parameter updates in a loop.

<Frame>
  <img alt="A diagram titled &#x22;Training Process&#x22; showing three steps: the model makes predictions (using weights w1…w5 and bias b), you compare the prediction to the actual value (error = (f(x)−y)^2), and you adjust parameters to minimize the error. A looped arrow and the caption &#x22;Repeat process&#x22; indicate iterating these steps." />
</Frame>

Gradient descent intuition: imagine the loss surface as a valley — at each step compute the slope (gradient) and move the parameters downhill until you reach a (local) minimum.

## Numeric example

Here’s an example showing trained parameters and a prediction (mileage scaled to thousands):

```python theme={null}
# Example trained model parameters (numeric). Mileage scaled to thousands.
w1, w2, w3, w4, w5 = -1.1, 0.4, 1.1, -0.8, 0.2
b = 25.0  # baseline price in thousands

# Example feature vector (x1..x5). Mileage expressed in thousands (20.0 => 20,000 miles).
x = [5.0, 2.0, 1.0, 20.0, 0.0]  # age, encoded color, sunroof, mileage (thousands), alarm

# Prediction (price in thousands)
f_x = w1 * x[0] + w2 * x[1] + w3 * x[2] + w4 * x[3] + w5 * x[4] + b
```

Reminder: consistent scaling between training and inference is crucial — many teams scale features (e.g., divide mileage by 1,000) to keep weights interpretable and numerically stable.

## From training to hosting and inference

Training uses labeled data (inputs with known targets), enabling the model to compare predictions to ground truth and improve. After training, you deploy (host) the trained model on a compute platform (virtual machine, container, on-prem server, or managed service like SageMaker). The hosted model receives new input data (same features, without targets) and returns predictions by applying the learned function f(x).

<Frame>
  <img alt="A slide titled &#x22;Summary&#x22; that lists four ML inference steps: train a model with labeled data, host it for inference, use new data with the same features but no targets, and generate predictions. It mentions the model's learned function f(x)." />
</Frame>

## Key takeaways

* ML models learn numeric relationships between features and a target by tuning weights and biases.
* Encode categorical and boolean features numerically before training (prefer one-hot for unordered categories).
* Scale numerical features to keep weights at reasonable magnitudes and improve optimizer behavior.
* Training minimizes a loss function (e.g., squared error) using optimization methods such as gradient descent.
* Ensure the same preprocessing pipeline is applied to training and inference data to avoid serving errors.

> **lightbulb** Always ensure your training and inference data use the same feature format and preprocessing (encoding and scaling). Mismatches between training and serving preprocessing are a common source of errors.

## Further reading and references

* Amazon SageMaker — model training and hosting: [https://aws.amazon.com/sagemaker/](https://aws.amazon.com/sagemaker/)
* Scikit-learn preprocessing (one-hot, scaling): [https://scikit-learn.org/stable/modules/preprocessing.html](https://scikit-learn.org/stable/modules/preprocessing.html)
* Introduction to Gradient Descent (blog/notes): [https://developers.google.com/machine-learning/crash-course/gradient-descent](https://developers.google.com/machine-learning/crash-course/gradient-descent)

This completes the lesson. Future material will cover the full ML pipeline: ideation → data preparation → training → deployment → monitoring and inference.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/40da1d46-e900-4426-973b-a9a38c3e505d/lesson/9912fafc-2651-450f-9835-162242754b1a)


# ML Basics Fundamentals of Model Training and Inference

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Machine-Learning-Prerequisites/ML-Basics-Fundamentals-of-Model-Training-and-Inference/page

Introductory guide to model training and inference using London house prices, covering data requirements, linear regression math, optimization, algorithm choices, overfitting, and deployment.

This lesson explains core machine learning concepts and the fundamentals of model training and inference. We'll follow a practical example — a tabular dataset of London house prices — to show what happens during training, how simple models like linear regression work, how algorithms (for example, XGBoost or Linear Learner) interact with data, and how iterative optimization minimizes loss to produce a deployable model.

We cover:

* What training data must contain.
* How an algorithm creates a model artifact from data.
* How inference works on a hosted prediction endpoint.
* The math behind linear regression and loss minimization.
* How training generalizes to multiple features and the risk of overfitting.

To begin, supervised machine learning requires training examples that include both inputs (features) and the target value you want the model to predict.

Our running example is a CSV table of London house sales. Each row contains features such as number of bedrooms, number of bathrooms, square footage, and postcode/area. The sale price is the target (the value we want the model to predict). During training the algorithm learns how combinations of features map to the target so the trained model can predict sale prices for new, unseen properties.

> **lightbulb** Your training dataset must include the target value for each training example. Supervised learning cannot learn the input→output mapping without that target column.

After preparing data you pick an algorithm (for example, XGBoost, LightGBM, Linear models, k-NN). Algorithms are pre-built methods that extract patterns and produce a mathematical representation of the relationship between features and targets. Training runs the chosen algorithm against your labeled data and outputs a model artifact (for example, `model.tar.gz` or `model.tgz`) that encodes the learned parameters.

Once training completes, host the model artifact on a prediction platform (a server, virtual machine, or a managed service such as [AWS SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker)). An inference request provides the same input features used in training but omits the target; the model returns a predicted value (for example, "£320,000").

<Frame>
  <img alt="A flowchart titled &#x22;Machine Learning Basics&#x22; that outlines the pipeline from training data and an algorithm through the training process to produce a trained model. The model is hosted on a prediction platform which takes new (no-target) data to produce inference predictions." />
</Frame>

Although deep learning and LLMs receive a lot of attention, tabular problems (linear and logistic regression, tree-based models such as XGBoost) account for many industry use cases. Mastering them offers practical value for business forecasting, risk scoring, and many production ML roles.

Common ML applications:

* Classifying objects (e.g., fraudulent transaction vs. legitimate).
* Forecasting trends (e.g., next-month sales).
* Identifying non-obvious relationships for business intelligence and decision-making.

<Frame>
  <img alt="A presentation slide titled &#x22;Machine Learning Basics&#x22; showing three panels: &#x22;Classifying objects,&#x22; &#x22;Forecasting trends,&#x22; and &#x22;Identifying relationships.&#x22; Each panel has a simple icon (cube with magnifier, rising bar chart, and connected nodes) illustrating the task." />
</Frame>

Linear regression — building intuition

* We predict house price from a single input feature (for example, property size) to introduce the idea of fitting.
* Plot the (x, y) points (size vs. price). A line that approximates these points is the model: it gives a rule to predict `y` from a new `x`.

<Frame>
  <img alt="An educational slide titled &#x22;Linear Regression — Understanding the Math&#x22; showing a scatter plot with blue data points and an orange best-fit line. It also displays the formula f(x) = ax + b with a labeled as slope and b as the y-intercept." />
</Frame>

Mathematical form

* A line is commonly written as `f(x) = a x + b`. In ML we usually write `f(x) = w x + b` where:
  * `w` is the weight (coefficient) and controls the slope.
  * `b` is the bias (intercept) and shifts the line vertically.
* The line typically does not pass exactly through all points. The vertical distance from an observed point to the line is the residual (error).

To measure how well the line fits the data we square each residual and sum them across all training examples. This sum of squared residuals (ordinary least squares loss) prevents positive and negative residuals from canceling out. Training adjusts `w` and `b` to minimize this loss — searching for the line of best fit.

Training is an optimization procedure: the algorithm updates parameters, recomputes the loss, and repeats until it reaches a minimum (local or global).

<Frame>
  <img alt="A presentation slide titled &#x22;Role of Algorithm in Model Training&#x22; with a blue rounded box labeled &#x22;Algorithm&#x22; on the left and three colored bullet panels on the right. The panels list that algorithms extract patterns from data, enable accurate predictions on unseen data, and reduce error during training." />
</Frame>

Multivariate (multiple features)

* With several input features (for example, bedrooms, bathrooms, square footage, age), linear regression generalizes to a weighted sum:
  * `f(x) = w1*x1 + w2*x2 + ... + wn*xn + b`
* Each feature `xi` gets its own weight `wi`. As the number of features grows (tens to hundreds), the parameter space becomes high-dimensional.
* Larger models can capture more complexity but are more prone to overfitting (learning training set noise rather than general patterns). Practical training uses validation data and regularization to manage this trade-off.

<Frame>
  <img alt="A presentation slide titled &#x22;Role of Algorithm in Model Training&#x22; showing a scatter plot of car age (years) versus sale price with a fitted trend line and arrows indicating residuals for each data point. The chart illustrates how the model's predictions compare to actual sale prices over time." />
</Frame>

Glossary (compact)

| Term         | Meaning                            | Example                  |
| ------------ | ---------------------------------- | ------------------------ |
| Weight (`w`) | Coefficient applied to a feature   | In `y = 2x + 4`, `w = 2` |
| Bias (`b`)   | Intercept term, shifts predictions | In `y = x + 2`, `b = 2`  |

<Frame>
  <img alt="A presentation slide titled &#x22;Role of Algorithm in Model Training&#x22; that explains the linear model f(x) = wx + b with w, b, and x defined. To the right is a graph showing several example lines (y = x, y = 2x, y = 2x + 4, y = x + 2)." />
</Frame>

Optimization and practical training tips

* Many algorithms use gradient-based optimization (for example, gradient descent) which computes the gradient of the loss with respect to each parameter and updates parameters in the direction that reduces loss.
* The learning rate controls the update step size:
  * Too large → risk of overshooting minima and unstable training.
  * Too small → slow convergence and high compute cost.
* Stopping criteria: maximum number of iterations/epochs, minimum improvement threshold, or early stopping based on validation loss. These help prevent wasted compute and reduce overfitting.

Algorithm selection at a glance

| Algorithm family               | When to use                            | Typical strengths                    |
| ------------------------------ | -------------------------------------- | ------------------------------------ |
| Linear models                  | Simple relationships, interpretability | Fast, low variance                   |
| Tree-based (XGBoost, LightGBM) | Tabular data with mixed feature types  | High accuracy, handles heterogeneity |
| k-NN                           | Small datasets, non-parametric         | Simple, few assumptions              |
| Neural networks                | Complex interactions, large datasets   | High capacity, requires more data    |

> **warning** Be cautious with many features or overly long training runs: they increase the risk of overfitting and unnecessary compute costs. Use held-out validation data, regularization, and early stopping to monitor generalization.

Summary — common workflow

1. Prepare training data: include features and the target column for each example.
2. Choose an algorithm suitable for the problem and data modality (tabular, text, images).
3. Train iteratively to minimize a loss function (for regression, often sum of squared errors).
4. Validate and tune hyperparameters (learning rate, regularization, model complexity).
5. Export the trained model artifact and host it on a prediction platform to serve inference requests (new inputs without targets).
6. Monitor model performance in production and retrain as needed with new data.

Links and references

* [AWS SageMaker (course)](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* XGBoost: [https://xgboost.readthedocs.io/](https://xgboost.readthedocs.io/)
* Scikit-learn (linear models): [https://scikit-learn.org/stable/modules/linear\_model.html](https://scikit-learn.org/stable/modules/linear_model.html)

If you want, I can add a short worked example showing how to compute the sum of squared residuals and a simple gradient descent update for `w` and `b` using Python-style pseudocode.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/40da1d46-e900-4426-973b-a9a38c3e505d/lesson/77801f1e-44fb-4fc8-ae7e-bf504ebc7ad6)
