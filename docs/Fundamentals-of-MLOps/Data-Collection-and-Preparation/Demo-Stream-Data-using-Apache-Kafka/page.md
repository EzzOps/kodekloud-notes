# Load the CSV file into a DataFrame
df = pd.read_csv("mock_data.csv")

# Display the first few rows
df.head()
```

### Inspecting Data Types and Missing Values

Check the DataFrame summary to inspect data types and count non-null entries:

```python theme={null}
# Display DataFrame summary and missing value counts
df.info()
df.isnull().sum()
```

Notice that columns like "hire date," "profile," and "department" might have null values, while numeric columns such as 'salary' are stored as float64.

For a statistical summary (which includes non-numeric columns), run:

```python theme={null}
df.describe(include='all')
```

<Frame>
  ![The image shows a Jupyter Notebook interface displaying Python code and output, including a summary of missing values and a statistical summary of a dataset's numeric columns using Pandas.](https://kodekloud.com/kk-media/image/upload/v1752875035/notes-assets/images/Fundamentals-of-MLOps-Demo-Small-to-Medium-Datasets-Data-Transformation-Pandas-Polars/jupyter-notebook-python-pandas-summary.jpg)
</Frame>

### Analyzing Categorical Data

To better understand categorical properties, inspect the unique values in the 'department' column:

```python theme={null}
df['department'].unique()
```

The output may look like:

```python theme={null}
array(['Marketing', 'HR', nan, 'IT', 'Finance'], dtype=object)
```

Notice the `NaN` value, which indicates missing data that could affect grouping and analysis later.

***

## 2. Data Cleaning

Cleaning your dataset is a vital step before modeling. You'll address missing numeric values and categorical inconsistencies.

### Handling Missing Numeric Values

Identify rows with missing numeric values such as 'age' or 'salary':

```python theme={null}
# Identify and display records with missing age and salary
print("Records with missing age:")
print(df[df['age'].isnull()][['age', 'salary', 'department']])
print("\nRecords with missing salary:")
print(df[df['salary'].isnull()][['age', 'salary', 'department']])
```

A common strategy is to fill missing values with the median value:

```python theme={null}
# Calculate median values for age and salary
age_median = df['age'].median()
salary_median = df['salary'].median()

print("\nMedian values used:")
print(f"Age median: {age_median}")
print(f"Salary median: {salary_median}")

# Fill missing numeric values with the median
df['age'] = df['age'].fillna(age_median)
df['salary'] = df['salary'].fillna(salary_median)
```

Confirm the imputation:

```python theme={null}
print("\nMissing values after numeric cleaning:")
print(df.isnull().sum())
```

### Handling Categorical Data

For categorical columns such as 'department', replace missing values with a default placeholder:

```python theme={null}
df['department'] = df['department'].fillna('Unknown')
print("\nMissing values after handling department:")
print(df.isnull().sum())
```

To get a quick overview of your cleaned DataFrame:

```python theme={null}
print("Cleaned DataFrame overview:")
print(df.head(), "\n")
print("Missing values in each column:")
print(df.isnull().sum(), "\n")
```

***

## 3. Transforming Complex JSON Data from the "profile" Column

The "profile" column contains JSON strings with structured details like address, phone number, and email. Transform these into Python dictionaries and extract the individual fields as separate columns.

### Converting JSON Strings

First, import the JSON module:

```python theme={null}
import json
```

Then, convert the JSON strings in the "profile" column:

```python theme={null}
df['profile'] = df['profile'].apply(lambda x: json.loads(x) if pd.notnull(x) else {})
```

### Extracting Information from JSON

Extract specific fields from the JSON data:

```python theme={null}
df['address'] = df['profile'].apply(lambda x: x.get('address', None))
df['phone']   = df['profile'].apply(lambda x: x.get('phone', None))
df['email']   = df['profile'].apply(lambda x: x.get('email', None))
```

Review the newly created columns:

```python theme={null}
print("\nSample extracted data:")
print(df[['address', 'phone', 'email']].head())
```

If the original "profile" column is no longer needed, drop it:

```python theme={null}
df.drop(columns=['profile'], inplace=True)

# Save the cleaned data to CSV for further processing
df.to_csv("cleaned_data.csv", index=False)
print("\nCleaned data saved to 'cleaned_data.csv'")
```

<Frame>
  ![The image shows a spreadsheet titled "mock\_data.csv" with columns for ID, name, age, salary, hire date, department, bonus, address, phone, and email. It contains various entries with corresponding data.](https://kodekloud.com/kk-media/image/upload/v1752875036/notes-assets/images/Fundamentals-of-MLOps-Demo-Small-to-Medium-Datasets-Data-Transformation-Pandas-Polars/mock-data-spreadsheet-columns.jpg)
</Frame>

***

## 4. Further Data Transformations

With your cleaned data saved, you can perform additional transformations by reloading the dataset.

### Adding Derived Columns

For instance, you can create a new column "address\_length" to verify that addresses meet a certain length requirement:

```python theme={null}
df = pd.read_csv("cleaned_data.csv")

# Calculate the length of each address
df['address_length'] = df['address'].apply(lambda x: len(str(x)))
print("Sample data after adding 'address_length':")
print(df[['address', 'address_length']].head(), "\n")
```

Next, categorize salaries into buckets such as low, medium, and high:

```python theme={null}
# Define salary bins and labels
bins = [0, 50000, 70000, 100000]
labels = ['low', 'medium', 'high']

# Create a new column for salary categorization
df['salary_category'] = pd.cut(df['salary'], bins=bins, labels=labels, include_lowest=True)
print("Sample data after adding 'salary_category':")
print(df[['salary', 'salary_category']].head(), "\n")
```

### Grouping and Aggregation

Aggregate key metrics by grouping data by the 'department' column:

```python theme={null}
# Group data by department and compute mean salary and age
summary_report = df.groupby('department').agg({
    'salary': 'mean',
    'age': 'mean'
}).reset_index()

# Rename columns for clarity
summary_report.rename(columns={'salary': 'average_salary', 'age': 'average_age'}, inplace=True)
print("Summary report by department:")
print(summary_report)
```

<Callout icon="lightbulb">
  Grouping and aggregation help in identifying trends and outliers within each department, which is critical for further ML model tuning.
</Callout>

***

## 5. Conclusion

In this tutorial, we covered the following steps to transform raw data into actionable insights for machine learning pipelines:

* Explored the dataset using Pandas functions such as `head()`, `info()`, `isnull()`, and `describe()`.
* Cleaned missing numeric values by imputing medians and handled missing categorical data with placeholders.
* Transformed a complex JSON column into separate, meaningful columns.
* Derived new columns, including address length and salary categories, to provide additional insights.
* Grouped and aggregated data by department to summarize key metrics.

These transformation practices are crucial when preparing your data for scalable ML models, especially in real-world scenarios with large datasets.

Thank you for following this guide. For more information on data transformation and ML pipeline best practices, explore additional resources such as [Pandas Documentation](https://pandas.pydata.org/docs/) and [Kaggle Learn](https://www.kaggle.com/learn).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/d72a3430-8b54-48d6-89ad-6a5f8b74f4ab/lesson/87ca9a04-612c-4647-a43d-99e6efff84cf" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/d72a3430-8b54-48d6-89ad-6a5f8b74f4ab/lesson/7a6fb098-18b6-4237-a449-8a606d42fe3e" />
</CardGroup>


# Demo Stream Data using Apache Kafka

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Data-Collection-and-Preparation/Demo-Stream-Data-using-Apache-Kafka/page

This article provides a hands-on demonstration of setting up Apache Kafka for real-time data streaming using Docker and Python.

Welcome to this hands-on demonstration on Apache Kafka. In this lesson, you will learn how to set up Apache Kafka as an event bus so that one program can publish messages while multiple programs consume them in real time. Kafka acts as a central hub where events from various producers are sent to designated topics. Consumers then subscribe to these topics to retrieve and process messages.

In this demonstration, we will:

* Create a simple Kafka environment using Docker Compose.
* Develop a Python-based Kafka producer that generates messages.
* Build a Kafka consumer to read and process those messages.

***

## Environment Setup

First, update your system and install the necessary packages for Python 3 and virtual environments. Run the following commands in your KodeKloud playground labs terminal:

```bash theme={null}
admin@docker-host:~$ sudo apt update
Get:1 https://download.docker.com/linux/ubuntu focal InRelease [57.7 kB]
Get:2 https://download.docker.com/linux/ubuntu focal/stable amd64 Packages [64.2 kB]
Get:3 http://security.ubuntu.com/ubuntu focal-security InRelease [128 kB]
Get:4 http://archive.ubuntu.com/ubuntu focal-updates InRelease [128 kB]
Get:5 http://archive.ubuntu.com/ubuntu focal-backports InRelease [128 kB]
Get:6 http://archive.ubuntu.com/ubuntu focal/main amd64 Packages [1,275 kB]
Get:7 http://archive.ubuntu.com/ubuntu focal/restricted amd64 Packages [33.4 kB]
Get:8 http://archive.ubuntu.com/ubuntu focal/universe amd64 Packages [11.3 MB]
Get:9 http://archive.ubuntu.com/ubuntu focal/multiverse amd64 Packages [177 kB]
Get:10 http://archive.ubuntu.com/ubuntu focal-updates/multiverse amd64 Packages [34.6 kB]
Get:11 http://archive.ubuntu.com/ubuntu focal-updates/restricted amd64 Packages [4,639 kB]
Get:12 http://archive.ubuntu.com/ubuntu focal-updates/universe amd64 Packages [1,587 kB]
Get:13 http://archive.ubuntu.com/ubuntu focal-updates/main amd64 Packages [4,426 kB]
Get:14 http://archive.ubuntu.com/ubuntu focal/universe amd64 Packages [4,157 kB]
Get:15 http://security.ubuntu.com/ubuntu focal-security amd64 Packages [4,157 kB]
Get:16 http://archive.ubuntu.com/ubuntu focal-backports/main amd64 Packages [55.2 kB]
Get:17 http://security.ubuntu.com/ubuntu focal-security/universe amd64 Packages [1,296 kB]
Get:18 http://security.ubuntu.com/ubuntu focal-security/multiverse amd64 Packages [30.9 kB]
Get:19 http://security.ubuntu.com/ubuntu focal-security/main amd64 Packages [4,639 kB]
Get:20 http://security.ubuntu.com/ubuntu focal-security/restricted amd64 Packages [4,227 kB]
Fetched 34.1 MB in 3s (13.5 MB/s)
Reading package lists... Done
Building dependency tree
Reading state information... Done
46 packages can be upgraded. Run 'apt list --upgradable' to see them.
admin@docker-host:~$ sudo apt install -y python3-pip python3-venv
```

After installation, clear your screen and create a Python virtual environment to isolate all Kafka-related dependencies:

```bash theme={null}
admin@docker-host:~$ python3 -m venv kafka_venv
admin@docker-host:~$ source kafka_venv/bin/activate
(kafka_venv) admin@docker-host:~$
```

<Callout icon="lightbulb">
  Creating a virtual environment helps prevent conflicts with system-wide packages and ensures a smooth dependency management experience.
</Callout>

***

## Setting Up Kafka with Docker Compose

Next, configure Kafka and Zookeeper using Docker Compose. Create a file named `docker-compose.yaml` and paste the content below. This configuration uses the Zookeeper image (required for managing the Kafka cluster) and the Confluent Kafka image that relies on Zookeeper.

Please note that a terminal view is provided in the image below for illustration. The file name and its content remain unchanged.

<Frame>
  ![The image shows a terminal window with a new file named "python-kafka-producer.py" open, displaying a blank screen with tilde symbols on the left.](https://kodekloud.com/kk-media/image/upload/v1752875038/notes-assets/images/Fundamentals-of-MLOps-Demo-Stream-Data-using-Apache-Kafka/terminal-python-kafka-producer-file.jpg)
</Frame>

```yaml theme={null}
version: '3'
services:
  zookeeper:
    image: confluentic/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"
  kafka:
    image: confluentic/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
```

Save the file, then bring up the Kafka environment using:

```bash theme={null}
(kafka_venv) admin@docker-host:~$ docker-compose up -d
```

This command pulls the necessary images and starts the containers for Zookeeper and Kafka in detached mode. Verify that the containers are running with:

```bash theme={null}
(kafka_venv) admin@docker-host:~$ docker container ls
```

***

## Creating and Validating Kafka Topics

With the Kafka cluster running, proceed to list the available topics:

```bash theme={null}
docker exec admin-kafka-1 kafka-topics --list --bootstrap-server localhost:9092
```

Since no topics exist initially, create a new topic named `sample-topic`:

```bash theme={null}
docker exec admin-kafka-1 kafka-topics --create --topic sample-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

Verify creation by listing the topics again:

```bash theme={null}
docker exec admin-kafka-1 kafka-topics --list --bootstrap-server localhost:9092
```

For detailed information about the topic, use:

```bash theme={null}
docker exec admin-kafka-1 kafka-topics --describe --topic sample-topic --bootstrap-server localhost:9092
```

<Callout icon="lightbulb">
  Adjust the number of partitions and the replication factor as needed. These parameters are critical for achieving higher throughput and ensuring fault tolerance in production environments.
</Callout>

***

## Producing Messages with a Kafka Producer

Now, let's create a Python script to produce sample events to our Kafka topic. Open a text editor (e.g., using `vim`) and create a file named `python-kafka-producer.py`.

An optional terminal screenshot is shown below for visual reference. Follow the written instructions to enter the code.

<Frame>
  ![The image shows a dark-themed terminal window with a text editor open, displaying a blank screen with a series of tilde (\~) symbols on the left. The status bar at the bottom indicates the editor is in "INSERT" mode.](https://kodekloud.com/kk-media/image/upload/v1752875038/notes-assets/images/Fundamentals-of-MLOps-Demo-Stream-Data-using-Apache-Kafka/dark-terminal-text-editor-insert.jpg)
</Frame>

Paste the following code into the file:

```python theme={null}
from kafka import KafkaProducer
import json
import time
from datetime import datetime

def create_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

def generate_message():
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'value': round(time.time() % 100, 2)
    }

def main():
    producer = create_producer()
    topic_name = 'sample-topic'
    try:
        while True:
            message = generate_message()
            producer.send(topic_name, value=message)
            print(f"Produced message: {message}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping producer...")
        producer.close()

if __name__ == "__main__":
    main()
```

Save the file and run the producer using:

```bash theme={null}
python3 python-kafka-producer.py
```

As the producer runs, it continuously generates messages—with each message containing a timestamp and a value—and sends them to the Kafka topic.

***

## Consuming Messages with a Kafka Consumer

In a separate terminal, activate the Python virtual environment and create a new file named `python-kafka-consumer.py`:

```bash theme={null}
admin@docker-host:~$ source kafka_venv/bin/activate
(kafka_venv) admin@docker-host:~$ vim python-kafka-consumer.py
```

Paste the following code into the file:

```python theme={null}
from kafka import KafkaConsumer
import json

def create_consumer():
    return KafkaConsumer(
        'sample-topic',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def main():
    consumer = create_consumer()
    try:
        for message in consumer:
            print(f"Received message: {message.value}")
    except KeyboardInterrupt:
        print("Stopping consumer...")
        consumer.close()

if __name__ == "__main__":
    main()
```

Save the file and then run the consumer:

```bash theme={null}
python3 python-kafka-consumer.py
```

The consumer will subscribe to the `sample-topic` and begin printing any messages it receives from Kafka.

***

## Demo Overview

In summary, this lesson demonstrated how to:

* Set up a Kafka cluster using Docker Compose.
* Create and validate Kafka topics.
* Develop Python scripts for both producing and consuming messages.

The producer continuously sends messages that include a timestamp and a random value, while the consumer retrieves and prints these messages in real time. This setup shows how Kafka can serve as the central nervous system for data streaming applications, efficiently handling data ingestion and distribution.

Happy coding and see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/d72a3430-8b54-48d6-89ad-6a5f8b74f4ab/lesson/6267c1eb-7af8-441a-9dc4-51e04649d0f9" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/d72a3430-8b54-48d6-89ad-6a5f8b74f4ab/lesson/ae1d4d98-2142-4870-a20e-5402cc29c0d8" />
</CardGroup>
