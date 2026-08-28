# Function to generate random IoT data
def generate_iot_data(**kwargs):
    data = []
    for _ in range(60):  # 60 readings (1 per second) over one minute
        data.append(random.choice([0, 1]))
        time.sleep(1)  # simulate a 1-second interval
    return data

# Function to aggregate the IoT data
def aggregate_machine_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='getting_iot_data')
    count_0 = data.count(0)
    count_1 = data.count(1)
    aggregated_data = {'count_0': count_0, 'count_1': count_1}
    return aggregated_data

# Email content generation
def create_email_content(**kwargs):
    ti = kwargs['ti']
    aggregated_data = ti.xcom_pull(task_ids='aggregate_machine_data')
    return (f"Aggregated IoT Data:\n"
            f"Count of 0: {aggregated_data['count_0']}\n"
            f"Count of 1: {aggregated_data['count_1']}")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    dag_id='iot_data_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    start_task = DummyOperator(task_id='start_task')

    getting_iot_data = PythonOperator(
        task_id='getting_iot_data',
        python_callable=generate_iot_data,
    )

    aggregate_machine_data = PythonOperator(
        task_id='aggregate_machine_data',
        python_callable=aggregate_machine_data,
    )

    # Optionally, use an EmailOperator to send the results
    send_email = EmailOperator(
        task_id='send_email',
        to='technician@example.com',
        subject='IoT Data Aggregation Results',
        html_content=create_email_content(),
    )

    end_task = DummyOperator(task_id='end_task')

    # Define the task dependencies
    start_task >> getting_iot_data >> aggregate_machine_data >> send_email >> end_task
```

Save the file. Airflow automatically detects new DAG definitions in the `dags` folder, and the "iot\_data\_pipeline" DAG will appear in the Airflow UI.

***

## Running and Monitoring the DAG

To run your new DAG:

1. Unpause "iot\_data\_pipeline" in the Airflow UI.
2. Trigger a manual run by clicking the run button.

The DAG executes the following tasks sequentially:

1. **start\_task**: Indicates the workflow start.
2. **getting\_iot\_data**: Generates simulated IoT data.
3. **aggregate\_machine\_data**: Aggregates the collected data.
4. **send\_email**: (Optional) Sends an email with the aggregated results.
5. **end\_task**: Marks the end of the pipeline.

Monitor the current state of each task (running, success, or failure) via the real-time UI. For detailed insights, click on a running task (e.g., "getting\_iot\_data") and check the logs.

<Frame>
  ![The image shows an Apache Airflow interface displaying a DAG named "iot\_data\_pipeline" with tasks in various states, including "start\_task," "getting\_iot\_data," "aggregate\_machine\_data," and "end\_task." The "getting\_iot\_data" task is currently running.](https://kodekloud.com/kk-media/image/upload/v1752875034/notes-assets/images/Fundamentals-of-MLOps-Demo-Data-Pipeline-Orchestration/apache-airflow-iot-data-pipeline.jpg)
</Frame>

After execution, the aggregated data might show, for example, 38 instances of “0” and 22 instances of “1”. In real-world applications, these counts could represent metrics such as successful operations versus machine errors, thereby aiding maintenance engineers in troubleshooting issues.

<Callout icon="lightbulb">
  This pipeline can be extended to write data to databases or data lakes, depending on your application needs.
</Callout>

***

## Conclusion

This lesson demonstrated how Apache Airflow simplifies the scheduling and orchestration of complex ETL workflows, replacing multiple cron jobs with a single, manageable system. With Airflow, you can efficiently set up pipelines to collect, process, and analyze data from IoT devices with minimal effort.

Thank you for following along, and happy orchestrating!

For more detailed information on Apache Airflow and data orchestration, consider visiting the [Apache Airflow Documentation](https://airflow.apache.org/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/d72a3430-8b54-48d6-89ad-6a5f8b74f4ab/lesson/6b5a2362-363e-4cfb-b2ed-ea65bce01abb" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/d72a3430-8b54-48d6-89ad-6a5f8b74f4ab/lesson/32cb866e-8452-4f35-9ede-3a79cd78100a" />
</CardGroup>


# Demo Small to Medium Datasets Data Transformation Pandas Polars

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Data-Collection-and-Preparation/Demo-Small-to-Medium-Datasets-Data-Transformation-Pandas-Polars/page

This hands-on tutorial demonstrates data transformation with Pandas, covering data import, quality checks, cleaning, and preparation for machine learning tasks.

Welcome to this hands-on tutorial demonstrating data transformation with Pandas. In this guide, you'll learn how to import a mock CSV dataset, perform data quality checks, handle missing values, and transform complex JSON data—all to prepare your dataset for downstream machine learning (ML) tasks.

***

## 1. Data Exploration and Quality Checks

Begin by launching your Jupyter Notebook and loading the mock CSV file into a DataFrame. This CSV dataset is destined for your ML model, but first, its quality must be verified.

<Callout icon="lightbulb">
  Before diving into transformations, always inspect your data using basic functions such as `head()`, `info()`, and `describe()`.
</Callout>

### Loading the Data

Start by importing Pandas and reading the CSV:

```python theme={null}
import pandas as pd
