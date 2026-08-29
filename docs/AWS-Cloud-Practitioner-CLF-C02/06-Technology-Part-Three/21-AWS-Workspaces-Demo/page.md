# Load the autoreload extension
%load_ext autoreload
%autoreload 2

# Python Built-Ins:
import json
import time

# External Dependencies:
import boto3  # AWS SDK for Python
import numpy as np  # For numerical and matrix operations
import pandas as pd  # Utilities for tabular data
import sagemaker  # High-level SDK for Amazon SageMaker
from sagemaker.automl.automl import AutoMLEstimator
from sagemaker.feature_store.feature_group import FeatureGroup

# Local Helper Functions:
import util

# Setting up SageMaker parameters
sgmk_session = sagemaker.Session()  # Connect to SageMaker APIs
region = sgmk_session.boto_session.region_name  # AWS Region (e.g., 'ap-southeast-1')
bucket_name = sgmk_session.default_bucket()  # Default Amazon S3 bucket
bucket_prefix = "sme101/direct-marketing"  # S3 path for file storage
sgmk_role = sagemaker.get_execution_role()  # IAM role with necessary permissions

print(f"s3://{bucket_name}/{bucket_prefix}")
print(sgmk_role)
```

This script initializes your connection with AWS services by setting parameters like the AWS region, S3 bucket name, bucket prefix, and execution role.

If you'd like to verify the instance, check the notebook instances section in the SageMaker interface or the corresponding section in Studio.

![The image shows the Amazon SageMaker interface, highlighting features like Studio Notebooks, One-click Training, and Deployment options for machine learning workflows.](https://kodekloud.com/kk-media/image/upload/v1752862053/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_320.jpg)

> **lightbulb** Once the kernel is up and running, click the play button on each cell to execute the code.

## Importing Libraries and Configuring S3

After setting up the environment, the subsequent cell imports essential libraries and finalizes connections. The refined code is shown below:

```python theme={null}
# Python Built-Ins:
import json
import time

# External Dependencies:
import boto3  # AWS SDK for Python
import numpy as np  # Numerical and matrix processing
import pandas as pd  # Utilities for tabular data
import sagemaker  # AWS SDK for Amazon SageMaker
from sagemaker.automl.automl import AutoMLEstimator
from sagemaker.feature_store.feature_group import FeatureGroup

# Local Helper Functions:
import util

# Setting up SageMaker parameters
sgmk_session = sagemaker.Session()  # Connect to SageMaker APIs
region = sgmk_session.boto_session.region_name  # AWS Region (e.g., 'ap-southeast-1')
bucket_name = sgmk_session.default_bucket()  # Default S3 bucket for SageMaker
bucket_prefix = "sml01/direct-marketing"  # File path in the S3 bucket to store files
sgmk_role = sagemaker.get_execution_role()  # IAM Execution Role for required permissions

print(f"{bucket_name}/{bucket_prefix}")
print(sgmk_role)
```

Executing this cell confirms that your S3 bucket and IAM role are properly configured.

## Uploading Sample Data and Loading It into the Feature Store

In the next step, the notebook demonstrates how to fetch sample data, upload it to S3, and load the CSV file into the SageMaker Feature Store. The code below outlines these steps:

```python theme={null}
# Fetch the sample data using a helper function
raw_data_path = util.data.fetch_sample_data()
print(f"Got: {raw_data_path}\n")

print("Uploading raw dataset to Amazon S3:")
raw_data_s3_uri = f"s3://{bucket_name}/{bucket_prefix}/raw.csv"
!aws s3 cp {raw_data_path} {raw_data_s3_uri}

# Timing the operation and preparing the feature group
%time
feature_group_name = "sm101-direct-marketing"
print("Loading data to SageMaker Feature Store")
util.data.load_sample_data(
    raw_data_path,
    f"{raw_data_s3_uri.split('/raw.csv')[0]}/feature-store",
    feature_group_name=feature_group_name,
    ignore_columns=[
        "duration", "emp.var.rate", "cons.conf.idx", "euribor3m", "nr.employed"
    ],
)
```

This cell performs the following tasks:

* Fetches the sample CSV file.
* Uploads the CSV to a specified S3 path.
* Loads the data into the Feature Store while excluding certain columns.

After running this cell, check the SageMaker Feature Store in Studio to confirm that the data has loaded successfully.

![The image shows Amazon SageMaker Studio with a Jupyter notebook open, displaying code and instructions related to data processing and feature store setup.](https://kodekloud.com/kk-media/image/upload/v1752862054/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_460.jpg)

![The image shows the Amazon SageMaker Studio interface, specifically the Feature Store section, displaying a feature group catalog with details like name, description, and status.](https://kodekloud.com/kk-media/image/upload/v1752862056/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_470.jpg)

## Running Autopilot for Tabular Data Problems

With the feature store populated, the notebook now showcases SageMaker Autopilot—an AutoML tool that automates data preparation and model training for tabular data problems.

To create an Autopilot experiment, you can follow the Studio GUI or execute the following code to run the job manually:

```python theme={null}
autopilot = AutoMLEstimator(
    role=sgmk_role,
    target_attribute_name="y",
    max_candidates=20,
    base_job_name="sm101-autopilot",
    output_path=f"s3://{bucket_name}/{bucket_prefix}/autopilot"
)
autopilot.fit(raw_data_s3_uri, wait=False)
```

You can also experiment with specific algorithms like XGBoost. Retrieve the appropriate container image for XGBoost with the following code:

```python theme={null}
image_uri = sagemaker.image_uris.retrieve("xgboost", region=region, version="1.5-1")
print(image_uri)
```

This portion of the demo underlines SageMaker Studio’s support for a wide range of machine learning workflows—from basic model training to advanced AutoML experiments.

![The image shows the Amazon SageMaker Studio interface with a file explorer, terminal, and a notebook open, discussing starting with SageMaker Autopilot for machine learning tasks.](https://kodekloud.com/kk-media/image/upload/v1752862057/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_500.jpg)

## Querying the Feature Store

The final part of the notebook demonstrates how to extract a snapshot from the SageMaker Feature Store using an Athena query. The following code snippet shows how to perform this query:

```python theme={null}
feature_group = FeatureGroup(feature_group_name, sagemaker_session=sgmk_session)
query = feature_group.athena_query()
table_name = query.table_name

data_extract_s3_uri = f"s3://{bucket_name}/{bucket_prefix}/data-extract"
!aws s3 rm --quiet --recursive {data_extract_s3_uri}  # Clear previous data extracts
print(f"Querying feature store to extract snapshot at:\n{data_extract_s3_uri}")

query.run("""
SELECT *
FROM (
    SELECT
        ROW_NUMBER() OVER (
            PARTITION BY "customer_id"
            ORDER BY "event_time" DESC, api_invocation_time DESC, write_time DESC
        ) AS row_number,
        *
    FROM "{table_name}"
    WHERE "event_time" = {time.time()}
) t
WHERE row_number = 1 AND NOT is_deleted;
""", output_location=data_extract_s3_uri)
query.wait()

full_df = query.as_dataframe()
print(f"Got {len(full_df)} records")
```

In summary, this process:

* Executes an Athena query on the feature store table to extract the latest records for each customer.
* Stores results at a specified S3 URI.
* Loads the data into a pandas DataFrame for further analysis.

A similar version of the query is provided later in the notebook, featuring slight variations in syntax.

![The image shows the Amazon SageMaker Studio interface, focusing on setting up an AutoML experiment with input data from an S3 location.](https://kodekloud.com/kk-media/image/upload/v1752862058/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_650.jpg)

![The image shows the Amazon SageMaker Studio interface, focusing on setting up a machine learning experiment with target and feature selection options.](https://kodekloud.com/kk-media/image/upload/v1752862059/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_710.jpg)

![The image shows the Amazon SageMaker Studio interface for creating an Autopilot experiment, focusing on selecting training methods and algorithms.](https://kodekloud.com/kk-media/image/upload/v1752862060/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_780.jpg)

![The image shows the Amazon SageMaker Studio interface, specifically the "Create an Autopilot experiment" section with deployment settings and advanced options for machine learning.](https://kodekloud.com/kk-media/image/upload/v1752862062/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_800.jpg)

![The image shows the Amazon SageMaker Studio interface, specifically the "Create an Autopilot experiment" section, detailing experiment configuration and data input settings.](https://kodekloud.com/kk-media/image/upload/v1752862063/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-SageMaker-Demo/frame_820.jpg)

## Conclusion

In this lesson, we demonstrated how AWS SageMaker Studio streamlines machine learning model development. You learned how to:

* Navigate the SageMaker Studio interface
* Import essential libraries and set up your environment
* Upload sample data to S3 and load it into the Feature Store
* Run AutoML experiments with SageMaker Autopilot and test with XGBoost
* Query the Feature Store using Athena to extract data snapshots

By leveraging SageMaker, you focus on model development and experimentation while AWS handles the underlying infrastructure. We hope this demo has provided valuable insights into efficient machine learning workflows using AWS SageMaker. Happy modeling, and see you in the next lab!

> **lightbulb** For more information on AWS SageMaker and advanced machine learning workflows, visit the [AWS SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html).

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-practitioner-clf-c02/module/bc372a48-ec05-4d1c-a3ef-e6b3ac1caf48/lesson/56b16cb5-00a3-4ce6-860f-a04929b9a2b3)


# AWS Workspaces Demo

Source: https://notes.kodekloud.com/docs/AWS-Cloud-Practitioner-CLF-C02/Technology-Part-Three/AWS-Workspaces-Demo/page

This demo guides users through setting up and using Amazon WorkSpaces, an AWS service for persistent virtual desktops in the cloud.

Welcome, Cloud Practitioners! In this demo, we will guide you through the process of setting up and using Amazon WorkSpaces—an AWS end-user computing service that provides persistent virtual desktops within the cloud. You can access these desktops via a dedicated client or through a web interface.

***

## Region and Directory Setup

We start our demo in the Northern Virginia region as Amazon WorkSpaces is not supported in all regions (for example, Ohio). When you click "Create a new WorkSpace," you'll be guided through several configuration steps. One of the initial steps is selecting a directory. In this demo, a simple Active Directory—functionally similar to LDAP—is used. This directory is registered with multiple subnets (for instance, us-east-1a and us-east-1b) and includes subnet details with IDs ending in c6, b7, c6, 2, and e2.

All necessary features are active, such as WorkDocs, internet access, and local administrator rights. Additionally, web access and Linux client support are enabled. This directory was pre-configured for Active Directory management, which simplifies user administration.

![The image shows an AWS WorkSpaces directory summary page with details like directory type, organization name, status, VPC, subnets, and encryption settings.](https://kodekloud.com/kk-media/image/upload/v1752862064/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Workspaces-Demo/frame_60.jpg)

***

## Creating a Workspace

The next step is to select the appropriate directory containing your users and click **Next**. In this phase, an additional user is created specifically for the WorkSpace. For demonstration purposes, the user is named "Amazon Linux" (abbreviated as AL2) with the email "[Michael+AL2@KodeKloud.com](mailto:Michael+AL2@KodeKloud.com)". Note that many email providers ignore text after the plus sign, so the email still routes to [Michael@KodeKloud.com](mailto:Michael@KodeKloud.com).

![The image shows an AWS WorkSpaces interface for creating users, with fields for username, first name, last name, and email, alongside navigation and password management options.](https://kodekloud.com/kk-media/image/upload/v1752862066/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Workspaces-Demo/frame_120.jpg)

After creating the user, verify its presence along with other users (such as mForrester and Ubuntu) in the directory and then click **Next**.

![The image shows an AWS WorkSpaces interface for identifying users, listing usernames, names, and emails, with "amazonl2" selected. Steps for creating WorkSpaces are on the left.](https://kodekloud.com/kk-media/image/upload/v1752862067/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Workspaces-Demo/frame_150.jpg)

### Selecting a Bundle and Operating System

In the next phase of the configuration, you need to choose a system bundle. The available bundles include:

* **Value:** 1 CPU, 2 GB memory
* **Standard**
* **Performance**
* **Power:** 4 vCPUs, 16 GB memory (selected for this demo)
* **PowerPro:** 8 vCPUs, 32 GB memory
* **GPU-enabled options:** Various configurations, including one with 122 GB memory and a dedicated virtual GPU

For this demo, the "Power" bundle was chosen for its balanced performance. Although the user is named after Amazon Linux, the demo opts for the Ubuntu operating system. Additionally, the WorkSpace is configured to auto-stop after one hour, and tag configuration is skipped to streamline the setup.

![The image shows an AWS WorkSpaces interface for selecting a bundle, highlighting a "Power" option with 4 vCPU and 16 GB memory, suitable for software development and data processing.](https://kodekloud.com/kk-media/image/upload/v1752862069/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Workspaces-Demo/frame_160.jpg)

![The image shows an AWS WorkSpaces configuration screen, highlighting running mode options (AlwaysOn, AutoStop) and tag management, with navigation steps on the left sidebar.](https://kodekloud.com/kk-media/image/upload/v1752862070/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Workspaces-Demo/frame_230.jpg)

After reviewing the selected settings, click **Create**. Note that new WorkSpaces typically take around 20 minutes to become fully active. In this demo, two WorkSpaces were preloaded, providing immediate visual feedback without a long wait period.

***

## Workspace Status and Invitation

Once the WorkSpaces are created, you'll notice that one might be in an available state while another still shows as pending. For instance, the WorkSpace configured with Amazon Linux might remain pending for a short time, whereas another (such as one running Windows Server) may be available. Select an available WorkSpace to proceed with connecting.

![The image shows an AWS WorkSpaces management console with details of a specific workspace, including user information, connection state, and available actions like editing users.](https://kodekloud.com/kk-media/image/upload/v1752862071/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Workspaces-Demo/frame_300.jpg)

Next, click the **Invite Users** action. AWS provides a registration code that is needed to access the WorkSpace. Copy the code and note that the associated username is “Enforcer.”

![The image shows an Amazon WorkSpaces interface for inviting users, with instructions for downloading the client and registration details.](https://kodekloud.com/kk-media/image/upload/v1752862074/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Workspaces-Demo/frame_320.jpg)

Right-click the provided link and proceed with the invitation process. With the WorkSpaces client already installed, open the application and register your WorkSpace using the registration code. After confirming that the username “Enforcer” is correctly set and entering the correct credentials, the client establishes a connection.

Once connected, the WorkSpace applies personalized settings, logs you into the virtual desktop hosted on AWS, and allows you to install and run your applications as if you were using a local machine.

***

## Testing the Virtual Desktop

Inside the virtual desktop, launch Firefox to assess network performance. Running an internet speed test reveals that the connection speed significantly exceeds typical desktop network speeds. The results demonstrate speeds that are well above standard Ethernet limits, likely powered by high-speed network backplanes.

![The image shows an internet speed test in progress, displaying a download speed of 1213.0 Mbps on a computer screen.](https://kodekloud.com/kk-media/image/upload/v1752862075/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Workspaces-Demo/frame_470.jpg)

A subsequent test confirms similar results:

![A screenshot of an internet speed test result showing 1147 Mbps download and 1656 Mbps upload, with 1 ms latency, indicating a very fast connection.](https://kodekloud.com/kk-media/image/upload/v1752862076/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Workspaces-Demo/frame_490.jpg)

> **lightbulb** For a smooth user experience, remember to customize your virtual desktop settings and install only the necessary software, enhancing both security and performance.

This confirms that Amazon WorkSpaces delivers a powerful and responsive virtual desktop experience.

***

## Conclusion

This demo showcased the process of setting up and connecting to an Amazon WorkSpace—from configuring directories and creating users to selecting hardware bundles and testing network speeds. Once connected, you gain access to a full-featured virtual desktop in AWS where you can seamlessly install and run your applications.

For more information, explore the following resources:

* [AWS WorkSpaces Documentation](https://aws.amazon.com/workspaces/)
* [AWS End-User Computing](https://aws.amazon.com/end-user-computing/)

Thank you for reading, and we look forward to sharing more cloud computing insights in our next article.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-practitioner-clf-c02/module/bc372a48-ec05-4d1c-a3ef-e6b3ac1caf48/lesson/c75692dc-c4fd-493f-a28b-75236ae47806)
