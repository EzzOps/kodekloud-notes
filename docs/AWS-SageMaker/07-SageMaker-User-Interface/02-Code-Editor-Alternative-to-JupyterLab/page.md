# clean_data.py
import argparse
import boto3
import pandas as pd
from sklearn.preprocessing import StandardScaler

s3 = boto3.client("s3")

def upload_to_s3(local_path, bucket, key):
    """Upload a local file to S3."""
    s3.upload_file(local_path, bucket, key)

def process_data(input_path, output_path):
    """Perform data preprocessing: handle missing values and scale numeric columns."""
    df = pd.read_csv(input_path)

    # Fill missing values with median for numeric columns only
    df.fillna(df.median(numeric_only=True), inplace=True)

    # Standardize numeric columns
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    scaler = StandardScaler()
    if len(numeric_cols) > 0:
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # Save processed data
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV data and upload results to S3.")
    parser.add_argument("--input-bucket", type=str, required=True, help="S3 bucket containing input data")
    parser.add_argument("--input-key", type=str, required=True, help="S3 key for input data")
    parser.add_argument("--output-bucket", type=str, required=True, help="S3 bucket for processed data")
    parser.add_argument("--output-key", type=str, required=True, help="S3 key for processed data")
    args = parser.parse_args()

    # Example local paths derived from S3 keys (adjust as needed)
    input_path = "/tmp/input.csv"
    output_path = "/tmp/output.csv"

    # Download input from S3
    s3.download_file(args.input_bucket, args.input_key, input_path)

    # Process and upload
    process_data(input_path, output_path)
    upload_to_s3(output_path, args.output_bucket, args.output_key)
```

If you invoke the script without required CLI arguments, argparse will print a usage message and exit:

```text theme={null}
usage: clean_data.py [-h] --input-bucket INPUT_BUCKET --input-key INPUT_KEY --output-bucket OUTPUT_BUCKET --output-key OUTPUT_KEY
clean_data.py: error: the following arguments are required: --input-bucket, --input-key, --output-bucket, --output-key
```

When debugging in VS Code, set breakpoints (for example, inside process\_data), step into functions, and inspect variables like the DataFrame and the StandardScaler instance. This lets you reproduce and fix runtime exceptions that can be difficult to debug in notebook cells.

Note: VS Code supports notebooks, but its notebook experience typically lacks some of JupyterLab’s richer interactive visualization and exploratory tools. For interactive visual exploration, JupyterLab is usually superior.

Here is a small example demonstrating raw tabular data with missing values loaded into pandas:

```python theme={null}
import pandas as pd

data = {
    "Bedrooms": [2, 3, 4, None],
    "Price": [200000, 250000, None, 150000],
    "Neighborhood": ["Downtown", None, "Suburb", "Rural"]
}

df = pd.DataFrame(data)
print(df)
```

Typical pandas output will represent missing numeric values as NaN:

Bedrooms     Price Neighborhood
0       2.0  200000.0     Downtown
1       3.0  250000.0          NaN
2       4.0       NaN       Suburb
3       NaN  150000.0        Rural

Why choose Code Editor vs JupyterLab

Use the Code Editor when your workflow emphasizes software engineering practices, productionization, and automation. Use JupyterLab for interactive exploration and visualization.

| Environment            | Best for                                                | Key benefits                                                                        |
| ---------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| JupyterLab / Notebooks | Early-stage exploration, visualization, ad-hoc analysis | Rich interactive plotting, cell-based experimentation, easy data inspection         |
| Code Editor (VS Code)  | Refactoring, production scripts, automation, CI/CD      | Powerful debugger, Git integration, multi-file editing, lightweight for large repos |

<Callout icon="lightbulb">
  Hybrid workflow recommendation: start with Jupyter Notebooks for exploration and prototyping, then refactor stable, reusable logic into modules and scripts in the Code Editor for productionization, testing, and automation.
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;Results: Productivity Gains&#x22; listing three numbered recommendations: use JupyterLab for early-stage exploration, transition to Code Editor for structured development, and use SageMaker Pipelines for custom processing jobs. The items are shown as horizontal colored bars on a dark blue background." />
</Frame>

When to refactor into scripts

As projects mature, move exploratory logic into well-tested, maintainable code:

* Extract reusable functions and modules from notebooks.
* Add robust error handling, input validation, and structured logging.
* Introduce unit tests and consider type hints for clearer interfaces.
* Use the Code Editor to refactor, debug, and integrate code into automation pipelines (SageMaker Pipelines, Step Functions, or Airflow).

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; listing four points: Code Editor is an alternative IDE within SageMaker Studio, ideal for VSCode users, offers better debugging than JupyterLab, and is best for general code development." />
</Frame>

Summary

* The Code Editor in [AWS SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) Studio provides a managed VS Code environment ideal for application development, refactoring, and building automation.
* JupyterLab remains the go-to environment for exploratory data analysis and interactive visualization.
* A hybrid approach is common: notebooks for experimentation, then refactor to scripts and develop in an IDE for production.
* For automation (SageMaker Pipelines, Step Functions, Apache Airflow), develop and test robust scripts in the Code Editor and integrate them into your CI/CD and MLOps workflows.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; with three numbered points. It outlines using Jupyter alongside a code editor, a hybrid approach for early development and deployment refactoring, and refactoring code into Python scripts for automation with SageMaker Pipelines, AWS Step Functions, or Apache Airflow." />
</Frame>

Further reading and references

* [AWS SageMaker documentation](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* [Amazon S3 developer guide](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [Amazon EC2 documentation](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)

This wraps up the lesson. A brief discussion of SageMaker Studio Classic—what it is and why it is no longer the preferred environment—is provided in a separate module.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b5e72234-012c-4793-ad8c-e1a7c6d3b8be/lesson/8904d5c1-da9d-4e8a-964a-26108d42138d" />
</CardGroup>


# Code Editor Alternative to JupyterLab

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-User-Interface/Code-Editor-Alternative-to-JupyterLab/page

Overview of SageMaker Studio Code Editor as a VS Code–based IDE alternative to JupyterLab for structured development, debugging, Git integration, and AWS resource support

In this lesson we introduce the Code Editor: a VS Code–based development interface available inside Amazon SageMaker Studio. It provides a familiar IDE experience for developers who prefer traditional editors (for example, Python IDLE, PyCharm, or Visual Studio Code) over notebook-centric workflows.

Many ML teams are proficient in Python but less familiar with JupyterLab. For those teams, exposing only Jupyter Notebooks can slow onboarding and reduce productivity. SageMaker’s Code Editor (based on VS Code OSS / code-server) runs in a managed environment and brings common IDE features—step-over/step-into debugging, variable watches, integrated terminal, linting/formatting extensions, and Git integration—into the Studio experience so developers can remain productive without context switching.

<Frame>
  <img alt="A slide titled &#x22;Preference for Regular IDEs Over JupyterLab&#x22; comparing Regular IDEs (left: step-over/step-into, familiar environment, enhanced productivity) with JupyterLab (right: slows productivity, limited debugging, no step-over/step-into). The ML team is shown in the center with the note &#x22;Skilled in Python, but unfamiliar with Jupyter.&#x22;" />
</Frame>

## Accessing Code Editor in SageMaker Studio

When you open SageMaker Studio, the Applications panel lists built-in tools you can launch (notebooks, IDEs, language tools, and ML workflow apps). The Code Editor appears in that list only if the application was enabled when the SageMaker user profile was created—this is controlled by the administrator who creates the user profile.

<Callout icon="lightbulb">
  If you don’t see Code Editor in the Applications panel, ask your SageMaker admin to enable it for your user profile.
</Callout>

Example of the managed environment shell prompt you might see inside Studio:

```bash theme={null}
sagemaker-user@default:~$
```

## What is the SageMaker Code Editor?

* It is a managed, hosted implementation of the open-source VS Code experience (VS Code OSS / code-server) inside SageMaker Studio.
* It provides a familiar VS Code–like interface running on managed compute provisioned by SageMaker.
* It supports editing Python scripts and Jupyter Notebooks, plus common configuration files such as JSON and YAML.
* Native VS Code extensions (some pre-enabled) are available, including the AWS Toolkit and Amazon Q for AWS resource browsing, code-completion, and generative assistance.

Code Editor is fully integrated into Studio and supports:

* AWS resource browsing (via the AWS Toolkit extension) for S3, training jobs, and other SageMaker resources.
* Git integration to clone repositories, create branches, commit, push, and perform basic merge workflows from the UI.
* Traditional debugging (step-in/step-over) that is more powerful than the limited debugging features in notebooks.
* Extensions and plugins; extension availability is managed by the hosted environment.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: SageMaker Code Editor&#x22; that lists eight numbered feature points. It highlights that the editor is Code‑OSS/VS Code–based, integrated with SageMaker Studio and AWS Toolkit, has built‑in Git, and is suited for scripts, pipelines and Jupyter notebooks." />
</Frame>

## When to use Code Editor vs Jupyter Notebooks

Choose the environment that best fits the task and stage of development:

* Use Jupyter Notebooks for interactive exploration and experimentation:
  * Inline outputs and markdown narrative are ideal for data exploration, plotting (Matplotlib, Seaborn), interactive visualizations, and ad hoc analysis.
  * Great for prototyping and experiment tracking where stepwise execution and rich cell output matter.

* Use the Code Editor for structured development, automation, and production workflows:
  * Best for writing maintainable Python scripts or packages, debugging with a step-through debugger, and multi-file navigation.
  * Use for code that will be invoked by schedulers, CI/CD pipelines, or orchestration services, or that needs to be version-controlled and tested.

Typical workflow:

* Early experimentation: perform interactive analysis and visualization in Jupyter Notebooks.
* Refactor for production: extract working code from notebooks into modular Python scripts or packages and continue development/debugging in Code Editor. This transition improves maintainability and suits pipeline or deployment workflows.

Code Editor also simplifies multi-file development: open multiple tabs, navigate across modules, and use integrated Git to manage changes without resorting to a terminal for basic operations.

## Comparison highlights

| Resource         | SageMaker Code Editor                                                    | Local VS Code                                                |
| ---------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------ |
| Use case         | Tailored for ML development and automation inside SageMaker              | General-purpose IDE for many languages and scenarios         |
| AWS integration  | Deep, out-of-the-box integration with SageMaker services and AWS Toolkit | Requires AWS Toolkit and local IAM credentials/configuration |
| Language support | Optimized for Python, JSON, YAML in the SageMaker context                | Wide language ecosystem and tooling                          |
| Extensibility    | Curated set of extensions due to managed environment                     | Nearly unlimited extension installation                      |
| Debugging        | Supports step-over/step-into debugging in a managed environment          | Richest and most extensible debugging capabilities           |
| Setup            | Launched from Studio Applications panel                                  | Requires local installation per machine                      |

<Frame>
  <img alt="A slide titled &#x22;Solution: SageMaker Code Editor&#x22; showing a comparison table between SageMaker Code Editor and VSCode. It lists categories like use case, AWS integration, language support, extensibility, debugging, and setup, noting SageMaker is ML-focused with deep AWS integration and limited extensibility while VSCode is general-purpose, highly extensible, and has full debugging tools." />
</Frame>

## Side-by-side: Code Editor vs JupyterLab

| Aspect                    | Code Editor                                                                 | JupyterLab                                                               |
| ------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Workspace model           | Private workspaces, per-user                                                | Can be configured for shared workspaces and collaborative editing        |
| Collaboration             | Git-based workflows (branching, PRs)                                        | Real-time collaborative editing (multi-user cursors) in many deployments |
| Inline outputs & plotting | Not focused on inline visualization; best for files and scripts             | Rich inline outputs, visualizations rendered beneath cells               |
| Debugging & logging       | Traditional debugger and structured logging—better for production debugging | Quick iterative debugging with cell-level outputs and prints             |
| Workflow focus            | Structured, single-invocation scripts for automation and pipelines          | Interactive, exploratory workflows and human-readable narratives         |

<Frame>
  <img alt="A slide titled &#x22;Solution: SageMaker Code Editor&#x22; showing a two-column comparison table that contrasts Code Editor (private spaces, requires Git, no inline visualizations, etc.) with JupyterLab (shared collaboration, inline outputs, debugging and plotting)." />
</Frame>

<Callout icon="lightbulb">
  Choose the environment based on the task: interactive analysis and visualization in Jupyter; structured, debuggable, and version-controlled code in the Code Editor.
</Callout>

## Summary

* SageMaker Code Editor delivers a VS Code–like IDE inside SageMaker Studio, optimized for writing scripts, pipelines, and production automation.
* Jupyter Notebooks remain the best tool for interactive exploration, visualization, and iterative experimentation.
* Use Jupyter for exploration and rapid prototyping; refactor to Code Editor when you need structured code, robust debugging, and CI/CD-friendly scripts.

## Links and References

* [Amazon SageMaker Studio documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)
* [VS Code OSS (code-server)](https://github.com/coder/code-server)
* [AWS Toolkit for Visual Studio Code](https://aws.amazon.com/visualstudiocode/)
* [JupyterLab documentation](https://jupyterlab.readthedocs.io/)
* [Best practices: transitioning notebooks to scripts and packages](https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b5e72234-012c-4793-ad8c-e1a7c6d3b8be/lesson/b9363b69-a825-4d3b-9d47-f99cf5c826e6" />
</CardGroup>
