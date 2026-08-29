# Demo SageMaker Canvas Data Wrangler Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-Data-Engineer/Demo-SageMaker-Canvas-Data-Wrangler-Part-2/page

Guide showing how to export SageMaker Data Wrangler transformations to Canvas datasets, Amazon S3, or a Jupyter notebook plus .flow for reproducible Processing jobs, with step examples and tips

At this stage the data-flow transforms are already defined and ordered correctly: drop column → impute → scale values → ordinal encode → one-hot encode. The remaining step is to export the transformed dataset so it can be persisted and consumed later (for training, reporting, or downstream pipelines).

This guide shows three export targets and how to reproduce the same Data Wrangler flow as code:

* Export to a Canvas dataset (low-code, Canvas-managed)
* Export to Amazon S3 (for downstream processing or storage)
* Export a Jupyter Notebook + .flow file (reproducible Processing job)

Each section explains the steps and examples you can adapt for your environment.

## Export to a Canvas dataset

1. From the end of the Data Wrangler flow, click the plus sign → Export → Canvas dataset.
2. Give the dataset a clear, descriptive name (for example, "KodeKloud house price data").
3. Optionally choose whether to process a sample (fast iteration) or the entire dataset. For demos, a subset is fine.
4. Run the export. Data Wrangler will choose where to execute the transform:
   * If it fits within the Canvas managed instance limits, it runs locally there.
   * Otherwise Data Wrangler uses a managed Spark backend (for example, EMR).

Once created, you can view the dataset metadata on the SageMaker Datasets page (name, size, creation time, status).

<Frame>
  <img alt="Screenshot of a &#x22;Datasets&#x22; management screen showing a list of tabular datasets (name, source, files, cells, last updated, status). The dataset &#x22;kodekloud-houseprice-data&#x22; is selected with a hand cursor over its checkbox." />
</Frame>

Tip: Rename the flow to something readable (for example, "KodeKloud house price flow"). Timestamps and auto-generated IDs in flow names are often awkward when referenced in code.

## Export to Amazon S3

To export transformed data to S3:

1. Open your Data Wrangler flow and add a destination node: Export → Amazon S3.
2. Choose a descriptive dataset name (example: "KodeKloud dataset house price") and select an S3 bucket and path.
3. For production/full runs choose to process the entire dataset. Click Export and wait for the job to finish.

After the job completes, verify the output in the S3 bucket. If the Data Wrangler job used Spark, the output is typically partitioned files with prefixes like `part-00000-...` and an output prefix/directory created by the export job.

<Frame>
  <img alt="A screenshot of the Amazon S3 web console opened to the bucket &#x22;kodekloud-sagemaker-demystified,&#x22; showing two objects: a CSV file named something like &#x22;kaggle_london_house_price_data_sample...&#x22; and an output folder. The UI shows tabs for Objects/Properties/Permissions and action buttons (Copy S3 URI, Download, Delete, etc.)." />
</Frame>

If you open the export folder you will see one or more CSV objects produced by the job. Spark-style outputs use file names like `part-00000-...`.

<Frame>
  <img alt="A screenshot of the Amazon S3 web console showing the contents of a folder (output_98c77944-4798-46c7-9176-e19fce6c2fa6/) with a single CSV object named &#x22;part-00000-27898861-4dfd-4a64-8420-ef3fc80bd79b-c000.csv&#x22;. The file is 5.7 MB and was last modified on May 2, 2025, with the cursor hovering over the filename." />
</Frame>

## Export the flow as a Jupyter Notebook (and .flow)

Exporting the flow as a Jupyter Notebook gives a reproducible artifact that sets up a SageMaker Processing job to apply the same transformations. This is ideal for handing work to a developer or integrating into CI/CD.

From the Data Wrangler flow:

* Add Export → Jupyter Notebooks → Amazon S3 and choose an S3 destination.
* Data Wrangler will store a `.ipynb` and a `.flow` file in the chosen location. The notebook contains boilerplate code to create and run a SageMaker Processing job that uses the `.flow` file as the transformation spec.

When the export completes, you will see a confirmation in the Canvas UI.

<Frame>
  <img alt="A screenshot of an AWS Data Wrangler data-flow canvas titled &#x22;kk-house-price-flow.flow&#x22; showing a preprocessing pipeline (Source → Data types → Drop column → Impute → Scale values → Ordinal encode → One-hot encode → Destination). A validation-complete message and a &#x22;Successfully exported&#x22; notification are also visible." />
</Frame>

Best practice: Sign out of SageMaker Canvas when finished to stop the managed instance and avoid charges. Canvas will warn you if background jobs are still running.

## Open JupyterLab and copy exported files from S3

SageMaker Studio/JupyterLab does not show S3 objects directly in the file browser. Use the AWS CLI in a terminal to copy the exported notebook and `.flow` file into the Studio filesystem.

First, verify you can list buckets:

```console theme={null}
sagemaker-user@default:~$ aws s3 ls
```

Then copy the notebook and flow file (quote URIs that contain spaces):

```console theme={null}
sagemaker-user@default:~$ aws s3 cp "s3://kodekloud-sagemaker-demystified/output_1746186367/kk-house-price-flow.ipynb" sagemaker-demystified/
download: s3://kodekloud-sagemaker-demystified/output_1746186367/kk-house-price-flow.ipynb to sagemaker-demystified/kk-house-price-flow.ipynb

sagemaker-user@default:~$ aws s3 cp "s3://kodekloud-sagemaker-demystified/output_1746186367/kk-house-price-flow.flow" sagemaker-demystified/
download: s3://kodekloud-sagemaker-demystified/output_1746186367/kk-house-price-flow.flow to sagemaker-demystified/kk-house-price-flow.flow
```

You should now see both files in the JupyterLab file browser.

## Open the exported notebook

Launch the notebook in JupyterLab and select an appropriate Python kernel. The notebook includes:

* Markdown explaining the flow and export
* Code to configure and run a SageMaker Processing job that executes the `.flow` transformation
* References to the `.flow` file and input CSV(s)

<Frame>
  <img alt="A screenshot of a Jupyter/SageMaker notebook titled &#x22;Save to S3 with a SageMaker Processing Job,&#x22; showing a table of contents and an &#x22;Inputs and Outputs&#x22; section. A file browser with project files is visible in the left sidebar." />
</Frame>

## Notebook contents — core snippets

The exported notebook sets up ProcessingInput(s) for the flow and inputs, and ProcessingOutput(s) for S3. Below are representative snippets you will find (adapt as needed).

Typical imports used in the exported notebook:

```python theme={null}
