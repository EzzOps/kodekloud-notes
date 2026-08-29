# Demo Navigating the UI

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-User-Interface/Demo-Navigating-the-UI/page

Guide to navigating the Amazon SageMaker console and creating and using legacy managed notebook instances, locating processing, training, models, endpoints, and using Jupyter and JupyterLab

In this lesson we walk through the Amazon SageMaker console and the legacy managed notebook instance experience. This hands-on demo shows:

* How to create legacy Jupyter Notebook instances (managed notebook instances).
* Where to find Processing jobs, Training jobs, Models, and Endpoints in the console.
* How to open and use both Jupyter Notebook and JupyterLab on a notebook instance.
* A brief comparison between legacy notebook instances and SageMaker Studio.

<Frame>
  <img alt="A slide titled &#x22;Demo Steps&#x22; listing six numbered demo items in two columns. The items cover creating notebook instances, data processing and training jobs, showing endpoints and models, and accessing Jupyter notebook vs lab." />
</Frame>

## Accessing the SageMaker console

Start at the AWS Management Console. If Amazon SageMaker is not visible in your recently visited services, type "SageMaker" into the search bar. Console labels may vary (for example: "Amazon SageMaker", "SageMaker", or "SageMaker AI") depending on console updates. In this lesson we focus on the legacy SageMaker notebook instance experience (managed notebook instances), not SageMaker Studio.

<Frame>
  <img alt="A screenshot of the AWS web console showing search results with a dark sidebar highlighting &#x22;Amazon SageMaker&#x22; (cursor pointing at it) and related features like SageMaker Studio. The right pane shows the account dashboard with a &#x22;Create application&#x22; button and a cost/usage chart." />
</Frame>

> **lightbulb** Tip: Console labels and navigation can change. Use the search bar to quickly locate SageMaker if it isn’t visible in your recently used services.

## Console navigation — where core resources appear

Once inside the SageMaker console, the left navigation shows categories such as Applications & IDEs, Processing, Training, and Inference. New accounts will show empty lists until jobs and resources are created. Below are examples of the resource pages you’ll use most often.

Processing jobs (data cleaning, feature engineering, batch transforms) appear under Processing. The console lists each job’s name, ARN, creation time, runtime duration, and status.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker console showing a &#x22;Processing jobs&#x22; list with job names, ARNs, creation times, durations and status indicators. The left navigation pane displays sections like Admin configurations, JumpStart and Processing." />
</Frame>

Training jobs launched from the SageMaker SDK (Estimator APIs) or other tooling appear under Training → Training jobs. The console shows creation time, duration, and completion status for each run.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker console showing the &#x22;Training jobs&#x22; page with a list of training job names, creation times, durations and &#x22;Completed&#x22; job statuses. The left sidebar shows SageMaker menu items like Admin configurations, JumpStart, Training and Inference." />
</Frame>

Models are listed under Inference → Models. A model entry references the model artifact or container that can be deployed to an endpoint for real-time inference.

<Frame>
  <img alt="A browser screenshot of the Amazon SageMaker console showing the &#x22;Models&#x22; page with a list of model entries (e.g., Model-hLy..., linear-learner..., house-prices) and the left-hand navigation menu. A large pointer/cursor is hovering over the &#x22;house-prices&#x22; model." />
</Frame>

If you deploy a model, the deployment appears under Endpoints. Endpoints are managed inference endpoints for real-time predictions; without a running endpoint you cannot perform real-time inference.

## Quick reference: console sections

| Console section    | Purpose                                                   | Example                                     |
| ------------------ | --------------------------------------------------------- | ------------------------------------------- |
| Processing         | Batch data processing, feature engineering, preprocessing | Data cleaning jobs, Spark jobs              |
| Training           | Model training runs                                       | Estimator / Training jobs launched from SDK |
| Inference → Models | Registered model artifacts for deployment                 | Model containers and S3 model.tar.gz        |
| Endpoints          | Deployed real-time inference endpoints                    | Multi-AZ endpoint for production            |

## Notebooks — legacy managed notebook instances vs Studio

Under Applications & IDEs → Notebooks you’ll see the legacy "Notebook instances" panel and a banner encouraging JupyterLab in SageMaker Studio (the newer, preferred environment). This demo shows the legacy managed notebook instances (the older experience) and how to open Jupyter and JupyterLab on them. SageMaker Studio and Domains offer a more integrated, multi-user environment and are outside this lesson’s scope.

<Frame>
  <img alt="A screenshot of the Amazon SageMaker console on the &#x22;Notebooks and Git repos&#x22; page with a large banner promoting JupyterLab in SageMaker Studio. The Notebook instances panel is shown (empty) along with a left-side navigation for Applications, IDEs, and admin configurations." />
</Frame>

## Create a legacy notebook instance (managed)

To create a legacy notebook instance, click "Create notebook instance" and provide a name. In the demo we use a recognizably named instance (for example: kodekloud-legacy-jupyter) to highlight that it’s a managed, legacy notebook. A notebook instance runs on an EC2-based managed virtual machine with a Jupyter server preinstalled — you don’t need to install Jupyter yourself.

Choose an instance type from the dropdown. For example, ml.t3.medium is a burstable CPU instance (commonly 2 vCPUs and 4 GiB RAM). For more CPU and memory, choose a larger instance (for example, a compute-optimized C5 family instance).

<Frame>
  <img alt="A screenshot of the Amazon SageMaker &#x22;Create notebook instance&#x22; page showing the Notebook instance settings with the instance type dropdown open and &#x22;ml.t3.medium&#x22; selected. The Notebook instance name field contains &#x22;kodekloud-legacy-jupyter.&#x22;" />
</Frame>

If you need to check instance specs, AWS documentation or third-party viewers show details and pricing for each family.

<Frame>
  <img alt="A webpage screenshot showing specifications and pricing for the AWS t3.medium EC2 instance. It lists details like 2 vCPUs, 4 GiB memory, clock speed, networking/storage info, and hourly prices." />
</Frame>

<Frame>
  <img alt="A webpage screenshot for the c5.xlarge AWS EC2 instance showing pricing and family sizes on the left and a detailed specs table on the right (4 vCPUs, 8 GiB memory, clock speed, networking and storage info). The page appears to be from a Vantage instance/pricing viewer." />
</Frame>

### Instance-type selection (quick comparison)

| Instance type | Use case                                           | Typical vCPU / RAM   |
| ------------- | -------------------------------------------------- | -------------------- |
| ml.t3.medium  | Small experiments, lightweight notebooks           | \~2 vCPUs, 4 GiB RAM |
| ml.c5.xlarge  | Compute-heavy preprocessing or small training jobs | \~4 vCPUs, 8 GiB RAM |

## IAM role and S3 access

Next pick the JupyterLab image/version and configure the IAM execution role for the notebook. The IAM role attached to the notebook instance defines what AWS resources (for example S3 buckets) the notebooks can access. For demos you might select "Any S3 bucket" to simplify access, but in production you should limit permissions to only the required resources and follow least-privilege principles.

<Frame>
  <img alt="A screenshot of the AWS SageMaker &#x22;Create notebook instance&#x22; page with a modal dialog titled &#x22;Create an IAM role&#x22; listing S3 access options. A large cursor is pointing at the &#x22;Any S3 bucket&#x22; option in the dialog." />
</Frame>

After creating the notebook instance, it will show a pending status while AWS provisions the managed EC2 instance. When the instance state reaches "InService" it is running and will continue to incur charges until stopped or deleted — remember to stop instances you’re not actively using.

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the Amazon SageMaker &#x22;Create notebook instance&#x22; page, focused on the Permissions and encryption section with a green success message about an IAM role. A large cursor is over the orange &#x22;Create notebook instance&#x22; button." />
</Frame>

When the notebook is InService, select the actions menu and choose "Open Jupyter" or "Open JupyterLab".

<Frame>
  <img alt="A screenshot of the Amazon SageMaker console showing the Notebook instances page with a green success banner and one notebook instance (kodekloud-legacy-jupyter) listed as InService. A hand-shaped cursor is hovering over the &#x22;Open Jupyter&#x22; action for that instance." />
</Frame>

## Using Jupyter Notebook and JupyterLab on managed instances

Opening "Jupyter" launches the classic Jupyter Notebook interface. You can create a new notebook and run simple Python cells:

```python theme={null}
