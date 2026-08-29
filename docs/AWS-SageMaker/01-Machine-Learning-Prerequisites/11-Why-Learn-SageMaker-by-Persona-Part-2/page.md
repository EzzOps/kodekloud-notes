# Define a list of numbers
numbers = [1, 2, 3, 4, 5]

# Define a variable to hold the sum of even numbers
sum_of_evens = 0

# Iterate over the list
for number in numbers:
    # Check if the number is even
    if number % 2 == 0:
        sum_of_evens += number  # Add even numbers to the sum

# Output the result to the console
print("The sum of even numbers is:", sum_of_evens)
```

Why this example is relevant:

* `number % 2 == 0` identifies even numbers.
* The loop accumulates even numbers into `sum_of_evens`.
* `print(...)` displays the result — a simple I/O pattern you’ll use when inspecting model outputs or debugging data transforms.

If you can read and understand the code above, you have sufficient Python to complete the course. We will introduce helper functions and third-party packages (NumPy, pandas, scikit-learn, and SageMaker SDK) as they become necessary.

## AWS basics we expect

You should be comfortable with:

* Having an AWS account and signing in to the AWS Management Console.
* Uploading and downloading files (for example, CSVs) to/from an Amazon S3 bucket using the Console. This basic S3 interaction is sufficient to run the hands-on labs.
* Being aware of other AWS compute and networking services (EC2, ECS, Route 53) is helpful for context but not required.

<Frame>
  <img alt="A slide titled &#x22;AWS Basics&#x22; with three numbered boxes. They list prerequisites: must have used the AWS Management Console; can upload/download files to an S3 bucket; and awareness of EC2, ECS, Route53 is helpful but not required." />
</Frame>

> **lightbulb** If you haven't used Amazon S3 before, practice by creating a bucket in the Console, uploading a small CSV, then downloading it back to confirm access. This hands-on step removes a common friction point when training models on SageMaker.

## Machine learning awareness (high-level)

This course is designed for beginners. You don't need deep ML theory up front, but it's useful to understand the typical ML pipeline at a conceptual level:

* Source data (e.g., tabular house-price dataset).
* Select a candidate algorithm (we'll demo linear learning; other choices include XGBoost, LightGBM, etc.).
* Create and run a training job to let the algorithm learn patterns from the data.
* Training produces a model artifact (e.g., model.tar.gz) that contains learned parameters.
* Host the model on compute (a VM, container, or a managed service) to serve predictions (inference). In this course we'll use SageMaker hosted endpoints for inference requests.

<Frame>
  <img alt="A flowchart titled &#x22;ML Awareness&#x22; showing a machine learning pipeline from source data through algorithm and training to a trained model. The trained model is then hosted for inference, producing a final prediction." />
</Frame>

In short: ML is about teaching a model to generalize relationships between input features (bedrooms, bathrooms, square footage, area) and a target (house price). After training, the model predicts outcomes for unseen inputs.

## Prerequisite checklist (quick reference)

| Category      | What you should know                                               | Example task                                                 |
| ------------- | ------------------------------------------------------------------ | ------------------------------------------------------------ |
| Python basics | Functions, lists, loops, conditionals, printing                    | Read and modify a small script that transforms CSV data      |
| AWS & S3      | AWS account, Console, upload/download to S3                        | Create an S3 bucket and upload a sample CSV                  |
| ML workflow   | High-level pipeline: data → training → model → hosting → inference | Run a training job and call a hosted endpoint for prediction |

## What you'll learn in this course

* Choose an appropriate algorithm for a problem and data type.
* Create and run a SageMaker training job.
* Register, package, and host your trained model on a SageMaker endpoint.
* Send inference requests to the hosted model and interpret predictions.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; with two points: (1) basic Python and ML concepts are sufficient to get started, and (2) familiarity with AWS and its services enhances the learning experience. The slide has a dark left panel and teal numbered markers for each point." />
</Frame>

## Summary

If you understand basic Python (lists, loops, conditionals, print) and the high-level ML workflow (data → training → model artifact → hosting → inference), you’re ready to begin. Familiarity with AWS and S3 will make the hands-on portions smoother, while knowledge of EC2, ECS, or Route 53 is optional background.

This completes the short prerequisites lesson. In the next lesson we'll cover key machine learning fundamentals to give you a clear view of what happens during training and inference.

## Links and references

* [AWS SageMaker documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
* [Amazon S3 documentation](https://aws.amazon.com/s3/)
* [Amazon EC2 documentation](https://aws.amazon.com/ec2/)
* [Amazon ECS documentation](https://aws.amazon.com/ecs/)
* [Route 53 documentation](https://aws.amazon.com/route53/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/40da1d46-e900-4426-973b-a9a38c3e505d/lesson/c3d6f898-d27f-4dd4-9368-bd4a9b2ab75c)


# Why Learn SageMaker by Persona Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Machine-Learning-Prerequisites/Why-Learn-SageMaker-by-Persona-Part-2/page

Explains how data scientists perform exploratory data analysis, feature engineering, model training and iteration while leveraging managed ML platforms such as SageMaker

Let's focus on the Data Scientist persona and how their day-to-day activities map to tooling and managed ML platform features like Amazon SageMaker.

## Data exploration and interactive analysis

Data scientists start by getting to know the dataset: understand features and targets, spot correlations and outliers, and identify columns to drop. This phase is highly interactive — you run small code cells, inspect outputs, create visualizations, and document reasoning for reproducibility.

Jupyter Notebooks or JupyterLab are the default environment for this iterative workflow: run Python cells, visualize inline, and annotate with Markdown to capture findings that can be shared or re-run.

<Frame>
  <img alt="The slide titled &#x22;Data Scientist&#x22; shows a user icon connected to a &#x22;Data Exploration&#x22; box, which leads to three tasks: analyzes dataset, visualizes data, and identifies useful features. Each task is shown as a colored horizontal bar with a small icon on a dark background." />
</Frame>

Typical exploration workflow:

* Load tabular data into a pandas DataFrame for inspection and manipulation.
* Use NumPy for fast vectorized numerical ops when required.
* Visualize distributions, correlations, and model diagnostics with Matplotlib/Seaborn.
* Use scikit-learn for quick baseline models and common preprocessing (imputation, scaling, encoding) to validate ideas.

Quick examples (common patterns):

```python theme={null}
