# Optimizing the Training Process with Automation

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Scientist/Optimizing-the-Training-Process-with-Automation/page

How to use Amazon SageMaker Autopilot to automate preprocessing, model selection, hyperparameter tuning, and deployment for faster prototyping and cost controlled iterative tabular model training

In this lesson we show how to use automation in Amazon SageMaker to speed up model development and reduce the cost of iterative training experiments. We'll explain the manual pain points, how SageMaker AutoML (Autopilot) addresses them, and how to run Autopilot programmatically with the SageMaker SDK.

What we'll cover:

* Why manual model training can be costly and slow.
* What SageMaker AutoML / Autopilot automates.
* How to run Autopilot from the SageMaker SDK, inspect candidates, and deploy the best model.
* Best practices and when to use Autopilot vs. custom training.

Why manual model training gets expensive

* Managing dataset versions, feature processing, algorithm selection, and hyperparameter permutations creates a large combinatorial search space.
* Running every permutation is time-consuming and costly even with experiment tracking.
* Data scientists often reduce the search space using domain knowledge, but that still requires many training runs.

Example (illustrative) hyperparameter trials you might run manually:

```python theme={null}
