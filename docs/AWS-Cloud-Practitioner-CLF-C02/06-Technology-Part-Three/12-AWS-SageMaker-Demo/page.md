# AWS SageMaker Demo

Source: https://notes.kodekloud.com/docs/AWS-Cloud-Practitioner-CLF-C02/Technology-Part-Three/AWS-SageMaker-Demo/page

This article provides a comprehensive lesson on building, training, and deploying machine learning models using AWS SageMakers tools and features.

Welcome to this comprehensive lesson on AWS SageMaker. In this demo, you will explore how to build, train, and deploy machine learning models using SageMaker’s robust suite of tools. This article highlights key SageMaker subservices and walks you through the process of setting up and executing common machine learning tasks.

SageMaker includes several powerful features such as:

* **Edge Manager**
* **Augmented AI** (for human evaluation of data)
* **Inference** (for model predictions and testing)
* **Training and Data Processing**
* **Notebooks** (with integrated Jupyter notebooks and Git repository support)
* **Ground Truth** (for dataset labeling)
* Additional governance options and quick-start jumpstarts

![The image shows the Amazon SageMaker interface, highlighting features for building, training, and deploying machine learning models, with navigation options and setup guides.](https://kodekloud.com/kk-media/image/upload/v1752862049/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_20.jpg)

For this lesson, we focus on SageMaker Studio—an integrated development environment (IDE) designed to streamline access to all SageMaker functionalities. The demonstration environment has been pre-configured, and the necessary workshop materials are already downloaded.

![The image shows the Amazon SageMaker Studio interface, an integrated development environment for machine learning, with sections on features, pricing, and documentation.](https://kodekloud.com/kk-media/image/upload/v1752862051/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_80.jpg)

## Navigating SageMaker Studio and Opening a Notebook

Start by navigating to the folder named "built-in algorithm HPO tabular" and double-click on the first notebook titled "autopilot and XGBoost." This notebook contains step-by-step instructions and code cells for configuring your environment. You will be prompted to select the "medium" instance type when initializing the notebook kernel, which then launches an instance in the background.

To execute a code cell in the notebook, simply click the play button or use the shortcut Shift+Enter. This interactive approach is ideal for data scientists and ML engineers as it facilitates immediate feedback and iterative development.

![The image shows an Amazon SageMaker Studio interface, setting up a notebook environment with options for image, kernel, instance type, and startup script.](https://kodekloud.com/kk-media/image/upload/v1752862052/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_120.jpg)

## Setting Up the Environment

The notebook begins by importing essential libraries, configuring an S3 bucket, defining the IAM role, and establishing a connection to SageMaker services using the SageMaker SDK. Below is the initial setup code:

```python theme={null}
