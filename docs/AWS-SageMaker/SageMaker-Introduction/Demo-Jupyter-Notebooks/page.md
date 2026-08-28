# 1) Create model resource
sagemaker.create_model(
    ModelName=model_name,
    PrimaryContainer={
        "Image": container_image,
        "ModelDataUrl": model_artifact_s3,
    },
    ExecutionRoleArn=role_arn,
)

# 2) Create endpoint configuration
endpoint_config_name = "house-price-endpoint-config-v1"
sagemaker.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[
        {
            "VariantName": "AllTraffic",
            "ModelName": model_name,
            "InitialInstanceCount": 1,
            "InstanceType": "ml.m5.large",
        }
    ],
)

# 3) Create endpoint
endpoint_name = "house-price-endpoint"
sagemaker.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=endpoint_config_name,
)

# Later: to deploy a new model, create a new Model + EndpointConfig then:
# sagemaker.update_endpoint(EndpointName=endpoint_name, EndpointConfigName="house-price-endpoint-config-v2")
```

<Callout icon="warning">
  Be mindful of costs: real-time endpoints incur charges while instances are running. For low-traffic or batch workloads, evaluate serverless, async, or Batch Transform to reduce costs.
</Callout>

Tip: The SageMaker Python SDK (sagemaker) provides higher-level abstractions (Model.deploy(), Pipeline deployments, etc.) that simplify many of the steps above and integrate well with CI/CD pipelines.

Final considerations and decision criteria

* Match hosting to requirements: latency, throughput, availability, cost, and operational capacity.
* Start simple with SageMaker Endpoints for predictable, low-latency inference on AWS; evolve to serverless or async patterns when appropriate.
* Design for model updates and automated deployment from the start — models drift and will require retraining and rotation into production.
* Monitor model performance, latency, and cost after deployment; automate rollback or traffic-shifting when necessary.

Further reading and references

* AWS SageMaker Endpoints documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/ex](https://docs.aws.amazon.com/sagemaker/latest/dg/ex) endpoints.html
* SageMaker Python SDK: [https://sagemaker.readthedocs.io/](https://sagemaker.readthedocs.io/)
* boto3 SageMaker client: [https://boto3.amazonaws.com/v1/documentation[AWS_SECRET_ACCESS_KEY].html](https://boto3.amazonaws.com/v1/documentation[AWS_SECRET_ACCESS_KEY].html)
* Kubernetes and container orchestration: [https://kubernetes.io/docs/home/](https://kubernetes.io/docs/home/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/772ec99e-54ee-4f4f-8b2a-08b5bc4d4a32/lesson/c63b171d-e654-4649-862d-6e9bfffbfa4c" />
</CardGroup>


# Demo Jupyter Notebooks

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-Introduction/Demo-Jupyter-Notebooks/page

Guide to install and run Jupyter Notebook and JupyterLab on an Ubuntu EC2 instance, covering virtual environments, connecting remotely, basic usage, and security considerations.

In this lesson you'll set up and use Jupyter Notebook (classic) and JupyterLab on a standalone Ubuntu VM (EC2 in this demo). This manual installation demonstrates how the pieces fit together; hosted services such as [AWS SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) provide managed environments if you prefer not to install manually.

We will:

* Install Python tooling and create an isolated virtual environment.
* Install and run the classic Jupyter Notebook server and connect from a browser.
* Create and run notebook code and markdown cells.
* Install and explore JupyterLab and its integrated features.
* Review security considerations for remote notebooks.

Let’s get started.

## 1. Launch and connect to the EC2 Ubuntu instance

In the AWS Management Console I launched a fresh Ubuntu EC2 instance and opened a shell from the console using Instance Connect.

<Frame>
  <img alt="Screenshot of the AWS EC2 &#x22;Connect to instance&#x22; page showing the EC2 Instance Connect tab with an instance ID, public IPv4 address, and the username set to &#x22;ubuntu.&#x22; A large cursor is visible on the left and a &#x22;Connect&#x22; button appears at the bottom right." />
</Frame>

Once you have an interactive shell on the instance, verify Python is available. On modern Ubuntu releases the `python` command is not always present — use `python3`:

```bash theme={null}
