# Demo Data Pipeline Orchestration

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Data-Collection-and-Preparation/Demo-Data-Pipeline-Orchestration/page

This article provides a guide on orchestrating data pipelines using Apache Airflow in a factory IoT setting.

Welcome to this comprehensive guide on data pipeline orchestration using Apache Airflow. In this lesson, you will explore a hands-on demo that illustrates how Airflow processes real-time data from an IoT device in a factory setting. Imagine a manufacturing facility where multiple machines are monitored through IoT devices collecting various metrics. Our objective is to process this data at scheduled intervals using Airflow’s scheduling feature and then share the processed results with maintenance technicians. Airflow streamlines task orchestration and simplifies troubleshooting for data engineers, data warehouse engineers, and MLOps professionals.

![The image illustrates a data pipeline orchestration process, showing data collection from a factory, processing through IoT, and task management with three tasks.](https://kodekloud.com/kk-media/image/upload/v1752875030/notes-assets/images/Fundamentals-of-MLOps-Demo-Data-Pipeline-Orchestration/data-pipeline-orchestration-iot-tasks.jpg)

In the sections below, we break down each component of the pipeline including Docker image initialization, Airflow configuration, and the creation of DAGs for ETL operations.

***

## Setting Up the Airflow Environment

In our KodeKloud playground, we start by creating a working directory for our orchestration example and then initialize Airflow using its official Docker image.

### Create the Working Directory

Begin by creating and navigating to your project directory:

```bash theme={null}
admin@docker-host:~$ mkdir example-orchestration
admin@docker-host:~$ cd example-orchestration/
admin@docker-host:~/example-orchestration$
```

### Download the Docker Compose File and Configure Folders

Download the required Docker Compose file and set up the necessary folder structure for DAGs, logs, plugins, and configuration:

```bash theme={null}
admin@docker-host:~/example-orchestrations$ mkdir example-orchestration
admin@docker-host:~/example-orchestrations$ cd example-orchestration
admin@docker-host:~/example-orchestrations$ curl -LLo 'https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml'
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
100 11342  100 11342    0 29307    0 --:-- --:-- --:-- 29307
admin@docker-host:~/example-orchestrations$ ls -lrt
total 12
-rw-r--r-- 1 admin admin 11342 Dec  8 07:09 docker-compose.yaml
admin@docker-host:~/example-orchestrations$ mkdir -p ./dags ./logs ./plugins ./config
admin@docker-host:~/example-orchestrations$ echo -e "AIRFLOW_UID=${id -u}" > .env
```

After configuring your environment, open the Docker Compose YAML file to review Airflow's settings. This file details the Airflow image, its environment variables, and services like Redis and Postgres.

> **lightbulb** Key components include setting the executor type, defining database connections, and mapping volumes for DAGs, logs, plugins, and configuration.

### Airflow Configuration Snippet

Below is a snippet from the Docker Compose file, highlighting the Airflow image and essential environment variables:

```yaml theme={null}
x-airflow-common:
  &airflow-common
  image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.10.2}
  environment:
    airflow-common-env:
      AIRFLOW_CORE_EXECUTOR: CeleryExecutor
      AIRFLOW_DATABASE_SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW_CELERY_RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
      AIRFLOW_CELERY_BROKER_URL: redis://redis:6379/0
      AIRFLOW_CORE_FERNET_KEY: ''
      AIRFLOW_CORE_DAGS_ARE_PAUSED_AT_CREATION: 'true'
      AIRFLOW_CORE_LOAD_EXAMPLES: 'true'
      AIRFLOW_API_AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session'
      AIRFLOW_SCHEDULER_ENABLE_HEALTH_CHECK: 'true'
      AIRFLOW_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}
      AIRFLOW_CONFIG: '/opt/airflow/config/airflow.cfg'
  volumes:
    - ${AIRFLOW_PROJ_DIR:-/}:/dags/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-/}:/logs/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-/}:/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-/}:/plugins:/opt/airflow/plugins
  user: '${AIRFLOW_UID:-50000}:0'
  depends_on:
    &airflow-common-depends-on
    redis:
      condition: service_healthy
    postgres:
```

Additional services such as Redis, the Airflow web server, scheduler, and worker are defined similarly. For example, the Redis service is configured as follows:

```yaml theme={null}
redis:
  image: redis:7.2-bookworm
  expose:
    - 6379
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 10s
    timeout: 30s
    retries: 50
    start_period: 30s
    restart: always
```

And the Airflow web server exposes port 8080 (mapped to your local port 8081):

```yaml theme={null}
airflow-webserver:
  <<: *airflow-common
  command: webserver
  ports:
    - "8081:8080"
  healthcheck:
    test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
    interval: 30s
    timeout: 10s
    retries: 5
    start_period: 30s
    restart: always
  depends_on:
    <<: *airflow-common-depends-on
    airflow-init:
      condition: service_completed_successfully
```

### Initializing Airflow

After reviewing the configuration, initialize Airflow with the following commands:

```bash theme={null}
admin@docker-host:~$ cd example-orchestration/
admin@docker-host:~/example-orchestration$ ls -lrt
total 12
-rw-rw-r-- 1 admin admin 11342 Dec  8 07:09 docker-compose.yaml
admin@docker-host:~/example-orchestration$ mkdir -p ./dags ./logs ./plugins ./config
admin@docker-host:~/example-orchestration$ echo -e "AIRFLOW_UID=${id -u}" > .env
admin@docker-host:~/example-orchestration$ vim docker-compose.yaml
admin@docker-host:~/example-orchestration$ docker compose up airflow-init
```

During initialization, Airflow downloads the necessary images and sets up database tables and user permissions. A successful initialization is indicated by a zero exit code in the logs.

Once initialization is complete, start all containers:

```bash theme={null}
admin@docker-host:~/example-orchestration$ docker compose up
```

You'll observe that containers for Redis, Postgres, airflow-init, airflow-scheduler, airflow-webserver, airflow-worker, and airflow-triggerer are created and started. The appearance of the Airflow logo in the logs confirms that the service is running.

***

## Accessing the Airflow Web Interface

After starting the containers (which might take 5–10 minutes), open your browser and navigate to [http://localhost:8081](http://localhost:8081). You will see the Airflow web interface.

Log in using the credentials:

* Username: Airflow
* Password: Airflow

In the UI, you'll find a list of DAGs (ETL workflows). Most example DAGs are initially paused; simply toggle them to activate. For example, the interface may display a tutorial DAG along with associated code details.

![The image shows an Apache Airflow web interface displaying details of a DAG named "tutorial," including task summaries and DAG details.](https://kodekloud.com/kk-media/image/upload/v1752875032/notes-assets/images/Fundamentals-of-MLOps-Demo-Data-Pipeline-Orchestration/apache-airflow-tutorial-dag-interface.jpg)

Clicking a DAG’s code button reveals its underlying implementation, offering further insights into the orchestration process.

***

## Example: Bash Operator DAG

The following example demonstrates how to use the BashOperator to run Linux commands as part of an ETL workflow. This DAG, titled "example\_bash\_operator," schedules tasks using a cron expression and utilizes dummy tasks to represent workflow steps.

```python theme={null}
from __future__ import annotations

import datetime
import pendulum

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="example_bash_operator",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dag_timeout=datetime.timedelta(minutes=60),
    tags=["example", "example2"],
    params={"example_key": "example_value"},
) as dag:
    run_this_last = EmptyOperator(
        task_id="run_this_last",
    )

    # [START howto_operator_bash]
    run_this = BashOperator(
        task_id="run_after_loop",
        bash_command="echo https://airflow.apache.org/",
    )
    # [END howto_operator_bash]

    run_this >> run_this_last

    for i in range(3):
        task = BashOperator(
            task_id=f"run_{i}",
            bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        )
        task >> run_this
```

Switch to the “Graph” view in the Airflow UI to visually inspect the DAG execution. Each box in the graph represents an individual task and the arrows depict task dependencies. Checking individual task logs can help diagnose any issues during execution.

![The image shows an Apache Airflow interface displaying a Directed Acyclic Graph (DAG) named "example\_bash\_operator," with various tasks like "runme\_0," "runme\_1," and "this\_will\_skip" visualized in a flowchart format.](https://kodekloud.com/kk-media/image/upload/v1752875033/notes-assets/images/Fundamentals-of-MLOps-Demo-Data-Pipeline-Orchestration/apache-airflow-dag-example-bash-operator.jpg)

***

## Creating a Custom IoT Data Pipeline DAG

In this section, you will create a custom DAG that simulates an IoT data pipeline. The DAG will perform three main functions:

1. Generate random IoT data.
2. Aggregate the collected data.
3. (Optionally) Send an email with the aggregated results.

### Create the DAG File

Open a new file named `iot_dag.py` within the `dags` folder:

```bash theme={null}
cd dags/
vim iot_dag.py
```

Paste the following code into `iot_dag.py`:

```python theme={null}
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
import random
import time
import datetime
