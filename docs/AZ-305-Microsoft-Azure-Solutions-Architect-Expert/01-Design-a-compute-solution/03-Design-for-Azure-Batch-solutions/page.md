# Design for Azure Batch solutions

Source: https://notes.kodekloud.com/docs/AZ-305-Microsoft-Azure-Solutions-Architect-Expert/Design-a-compute-solution/Design-for-Azure-Batch-solutions/page

This lesson teaches how to select and implement Azure Batch solutions for managing compute-intensive tasks efficiently.

In this lesson, you will learn when and how to select an Azure Batch solution. Although Azure Batch is not part of our [AZ-104: Microsoft Azure Administrator](https://learn.kodekloud.com/user/courses/az-104-microsoft-azure-administrator) course, it is included in the [AZ-204: Developing Solutions for Microsoft Azure](https://learn.kodekloud.com/user/courses/az-204-developing-solutions-for-microsoft-azure) exam because it requires developer skills. With Azure Batch, you can create and manage jobs using Python, .NET, or any other supported language.

## When to Use Azure Batch

Azure Batch is ideal for High Performance Computing (HPC) workloads. In HPC scenarios, you typically have compute-intensive tasks that do not require deep management of the underlying infrastructure. Azure Batch simplifies job management by automatically scaling compute nodes and scheduling tasks.

<Frame>
  ![The image is a guide on when to select an Azure Batch solution, featuring a decision flowchart and explanations for HPC scenarios, managing jobs, and installing applications.](../../../../images/kodekloud.com/kk-media/image/upload/v1752866847/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-Batch-solutions/azure-batch-decision-guide-flowchart.jpg)
</Frame>

Azure Batch is best suited for scenarios where you:

1. Need to manage a large number of jobs.
2. Want to scale compute nodes automatically based on task intensity (e.g., running simulations that require multiple nodes).
3. Prefer to install and run your own application code rather than relying solely on built-in solutions. For example, you might process images stored in a storage account and then output the processed results.

## How Azure Batch Works

The diagram below illustrates the complete data processing workflow using Azure Batch. Imagine that you have an Azure Data Lake Storage account that holds your data (distinct from regular Azure Storage). A client uploads files—such as images or other data—to Azure Data Lake Storage. In parallel, code provisions the necessary compute resources and jobs. The process pulls data from storage, executes compute-intensive operations (like image processing or simulations), and then pushes the processed data back to storage for your client application to retrieve.

<Frame>
  ![The image is a flowchart illustrating the working process of Azure Batch, showing data movement between Azure Data Lake Storage, Azure Batch, and client applications. It includes steps like uploading files, creating compute pools, processing tasks, and downloading output files.](../../../../images/kodekloud.com/kk-media/image/upload/v1752866848/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-Batch-solutions/azure-batch-flowchart-data-movement.jpg)
</Frame>

Multiple SDKs, including Python and .NET, are available for Azure Batch, allowing you to choose the one that best fits your development needs.

<Callout icon="lightbulb">
  This lesson demonstrates Azure Batch setup using the Azure Portal and Azure CLI commands. Make sure you have the appropriate permissions and Azure CLI installed on your system.
</Callout>

***

## Step 1: Creating the Resource Group and Storage Account

Begin by creating a resource group in your desired location. Use the following command:

```bash theme={null}
az group create \
  --name QuickstartBatch-rg \
  --location eastus2
```

Next, create a storage account. Note that the storage account name must be unique:

```bash theme={null}
az storage account create \
  --resource-group QuickstartBatch-rg \
  --name mystorageaccount \
  --location eastus2 \
  --sku Standard_LRS
```

If you need a different unique name, update the command accordingly:

```bash theme={null}
az storage account create \
  --resource-group QuickstartBatch-rg \
  --name kodekoud \
  --location eastus2 \
  --sku Standard_LRS
```

<Callout icon="triangle-alert">
  If you encounter policy restrictions allowing deployments only in specific regions (e.g., East US and West US), update the location parameter to match an allowed region.
</Callout>

***

## Step 2: Creating the Batch Account

Create your batch account, which combines jobs, tasks, and compute pools. Replace parameters as needed:

```bash theme={null}
az batch account create \
  --name mybatchaccount \
  --storage-account mystorageaccount \
  --resource-group QuickstartBatch-rg \
  --location eastus
```

If you wish to modify the batch account name, use this alternative command:

```bash theme={null}
az batch account create \
  --name koddekloudbatch \
  --storage-account koddekloudbatch \
  --resource-group QuickstartBatch-rg \
  --location eastus
```

Wait until the batch account creation is complete.

***

## Step 3: Authenticating to the Batch Account

Before creating pools, jobs, and tasks, authenticate to your batch account with the following command:

```bash theme={null}
az batch account login -n kodekloudbatch -g QuickstartBatch-rg
```

This command uses the shared key for authentication. After a successful login, you can proceed with creating compute resources.

***

## Step 4: Creating the Compute Pool

Create a compute pool to provision the necessary virtual machines. In this example, the pool (named "kpool") uses a Standard\_A1\_v2 VM size, employs a canonical Ubuntu 18.04 image, and targets two dedicated nodes:

```bash theme={null}
az batch pool create --id kpool \
  --vm-size Standard_A1_v2 \
  --target-dedicated-nodes 2 \
  --image canonical:ubuntuserver:18.04-LTS \
  --node-agent-sku-id "batch.node.ubuntu 18.04"
```

After creating the pool, check its allocation state:

```bash theme={null}
az batch pool show --pool-id kpool --query "allocationState"
```

Initially, the allocation state might show "resizing." Once all nodes are provisioned, the state will change to "steady." You can also verify the pool status via the Azure Portal.

<Frame>
  ![The image shows a Microsoft Azure portal interface displaying details of a batch account named "kodekloudbatch." It includes information about resource groups, account status, and monitoring metrics like vCPU minutes and failed tasks.](../../../../images/kodekloud.com/kk-media/image/upload/v1752866849/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-Batch-solutions/azure-portal-kodekloudbatch-details.jpg)
</Frame>

***

## Step 5: Creating Jobs and Tasks

Once the compute pool is in a "steady" state, create a job that will run on the pool:

```bash theme={null}
az batch job create --id kjob --pool-id kpool
```

A job groups tasks that run on the provisioned compute nodes. Next, create tasks within your job—this example uses a loop to create four tasks. Each task prints environment variables (prefixed with AZ\_BATCH) and then sleeps for 90 seconds:

```bash theme={null}
for i in {1..4}
do
  az batch task create --task-id ktask$i --job-id kjob --command-line "/bin/bash -c 'printenv | grep AZ_BATCH; sleep 90s'"
done
```

After task creation, verify the status of a task using:

```bash theme={null}
az batch task show --task-id ktask1 --job-id kjob
```

Ensure that the exit code is zero to confirm successful execution. Additional details, such as the compute node on which the task ran, will also be available.

To view the task output files (e.g., standard output and standard error), list the files with:

```bash theme={null}
az batch task file list --task-id ktask1 --job-id kjob -o table
```

A sample output might include files like the working directory, stderr.txt, and stdout.txt. Download the standard output file to inspect the results:

```bash theme={null}
az batch task file download --job-id kjob --file-path stdout.txt --destination ./output.txt
```

Finally, review the contents of the downloaded file:

```bash theme={null}
cat output.txt
```

This file should display the environment variables starting with AZ\_BATCH, verifying the task executed correctly.

Alternatively, you can check task details directly in the Azure Portal. Navigate to your job "kjob" under the "kodekloudbatch" account, then click on a completed task (such as task four) to view its output.

<Frame>
  ![The image shows a Microsoft Azure portal interface displaying a list of completed tasks under a job named "kjob" in the "kodekloudbatchbatch" account. Each task is marked as completed with an exit code of 0.](../../../../images/kodekloud.com/kk-media/image/upload/v1752866850/notes-assets/images/AZ-305-Microsoft-Azure-Solutions-Architect-Expert-Design-for-Azure-Batch-solutions/azure-portal-kjob-tasks-completed.jpg)
</Frame>

***

## Summary

In this lesson, you learned how to create an Azure Batch solution by:

* Establishing a resource group and storage account.
* Creating and authenticating a batch account.
* Provisioning a compute pool.
* Setting up jobs and tasks for parallel execution.

This step-by-step example demonstrates basic parallel task execution. You can extend these concepts for more complex workloads by leveraging SDKs like .NET or Python.

Happy batching!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-305-microsoft-azure-solutions-architect-expert/module/bf1d18e5-9589-48cf-99af-4150d985241a/lesson/a9227ce1-87a3-44f2-9dc6-49619cac0270" />
</CardGroup>
