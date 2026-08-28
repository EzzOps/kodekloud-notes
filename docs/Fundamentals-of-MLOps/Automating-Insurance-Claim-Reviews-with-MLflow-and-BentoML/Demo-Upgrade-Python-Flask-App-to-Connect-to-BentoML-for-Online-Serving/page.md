# Assume 'data' and 'num_samples' are defined previously in your project
df = pd.DataFrame(data)

# Introduce some anomalies (e.g., very high claim amounts)
num_anomalies = 50
anomalies = {
    'claim_id': np.arange(num_samples + 1, num_samples + num_anomalies + 1),
    'claim_amount': np.random.randint(10000, 25000, num_anomalies),  # Much higher amounts
    'patient_age': np.random.randint(18, 90, num_anomalies),
    'provider_id': np.random.randint(1, 50, num_anomalies),
    'days_since_last_claim': np.random.randint(0, 365, num_anomalies)
}

df_anomalies = pd.DataFrame(anomalies)

# Combine normal data with anomalies
df = pd.concat([df, df_anomalies]).reset_index(drop=True)

# Shuffle the dataset
df = df.sample(frac=1).reset_index(drop=True)

# Save the data to CSV
df.to_csv('synthetic_health_claims.csv', index=False)
```

Run the script using the following command:

```bash theme={null}
python3 synthetic_health_claims.py
```

Upon execution, you should see an output confirming that the synthetic data was generated and saved. The console output will also show that the MLflow UI is running, along with relevant log messages.

***

## 3. Creating and Running the ML Experiment

In this section, you'll train an ML model to perform anomaly detection using the Isolation Forest algorithm and log experiment details to the MLflow server.

### Step 3.1: Model Training Script

Create a file named `isolation_model.py` with the following content:

```python theme={null}
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn

# Load the synthetic data
df = pd.read_csv('synthetic_health_claims.csv')

# Set the MLflow tracking URI
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Define the features for the model. Note that 'claim_id' is not used.
features = ['claim_amount', 'num_services', 'patient_age', 'provider_id', 'days_since_last_claim']

# Split the data into training and test sets
X_train, X_test = train_test_split(df[features], test_size=0.2, random_state=42)

# Create (or set) the experiment in MLflow
mlflow.set_experiment("Health Insurance Claim Anomaly Detection")

with mlflow.start_run():
    # Train the Isolation Forest model
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X_train)

    # Predict anomalies on training and test sets
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Calculate the percentage of detected anomalies
    train_anomaly_percentage = (y_pred_train == -1).mean() * 100
    test_anomaly_percentage = (y_pred_test == -1).mean() * 100

    # Log model parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("contamination", 0.05)

    # Log computed metrics
    mlflow.log_metric("train_anomaly_percentage", train_anomaly_percentage)
    mlflow.log_metric("test_anomaly_percentage", test_anomaly_percentage)

    # Log the model artifact to MLflow
    mlflow.sklearn.log_model(model, "model")

    print(f"Train Anomaly Percentage: {train_anomaly_percentage:.2f}%")
    print(f"Test Anomaly Percentage: {test_anomaly_percentage:.2f}%")
    print("Model and metrics logged to MLflow.")
```

Run the script by executing:

```bash theme={null}
python3 isolation_model.py
```

The terminal will display detailed output regarding the experiment, including logged parameters and metrics. A typical output snippet might look like this:

```text theme={null}
2024/12/03 11:22:46 INFO mlflow.tracking.fluent: Experiment with name 'Health Insurance Claim Anomaly Detection' does not exist. Creating a new experiment.
2024/12/03 11:22:46 WARNING mlflow.models.model: Model logged without a signature and input example. Please set `input_example` parameter when logging the model to auto infer the model signature.
Train Anomaly Percentage: 5.20%
Test Anomaly Percentage: 4.29%
Model and metrics logged to MLflow.
View run: http://127.0.0.1:5000/e/experiments/199596116865516564
```

***

## 4. Validating the Experiment in MLflow

Once the script finishes running, refresh your browser where the MLflow UI is open. You should now see the "Health Insurance Claim Anomaly Detection" experiment, complete with parameters, metrics, and the model artifact.

<Frame>
  ![The image shows an MLflow experiment interface displaying details of a machine learning run, including parameters, metrics, and model information for an anomaly detection task.](https://kodekloud.com/kk-media/image/upload/v1752875005/notes-assets/images/Fundamentals-of-MLOps-Demo-Setup-MLflow-server-and-run-the-ML-Experiment/mlflow-anomaly-detection-experiment.jpg)
</Frame>

This UI confirms that your experiment has been successfully logged and is ready for further exploration or deployment.

***

## 5. Next Steps

In a production setting, your model may undergo multiple iterations and rigorous testing before deployment. For this demo, we directly use the output from this experiment. The logged model artifact, which might be stored as a pickle file or another format, can be downloaded from the MLflow UI and integrated further.

The next phase typically involves building a service around the model using frameworks like BentoML. For more detailed information on BentoML, refer to the [BentoML Documentation](https://docs.bentoml.org/).

***

Thank you for reading this guide on setting up the MLflow server and running your ML experiment. For additional resources, check out the following links:

* [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
* [scikit-learn Documentation](https://scikit-learn.org/stable/user_guide.html)
* [VS Code Documentation](https://code.visualstudio.com/docs)

Happy experimenting!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/e6813732-5ba7-496f-84db-2272a4c2b188/lesson/bc058c2d-4f52-457b-8847-bae2af2aa174" />
</CardGroup>


# Demo Upgrade Python Flask App to Connect to BentoML for Online Serving

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Automating-Insurance-Claim-Reviews-with-MLflow-and-BentoML/Demo-Upgrade-Python-Flask-App-to-Connect-to-BentoML-for-Online-Serving/page

This tutorial explains how to integrate a Flask app with BentoML for online prediction serving using CSV file uploads.

Welcome to this lesson on how to integrate a Flask application with BentoML for online prediction serving. In this tutorial, you will learn how to set up a simple Flask application that accepts CSV file uploads, processes the data, communicates with the BentoML predict endpoint, and then displays prediction results in an intuitive user interface.

Below is an overview of the steps covered in this tutorial:

***

## Step 1: Setting Up the Flask Application

Begin by launching your VS Code editor and opening a new terminal. Also, open a separate terminal window to start the BentoML service, which must be running to serve predictions.

Create a file named `flaskapp.py` and include the following code. This code establishes an endpoint that receives a POST request containing a Base64-encoded CSV file. The CSV content is decoded and converted into a DataFrame. Should the DataFrame include a `claim_id` column, it is temporarily separated from the rest of the data. The remaining data is then sent as JSON to the BentoML predict endpoint. Upon receiving the prediction results, they are merged back with the original DataFrame, and the results are rendered through an HTML template.

```python theme={null}
from flask import Flask, render_template, request
import pandas as pd
import requests
import base64
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file_data = request.form.get('file')
    # Decode the Base64 encoded CSV file content
    decoded_file = base64.b64decode(file_data.split(',')[1])
    # Read CSV content into a DataFrame
    df = pd.read_csv(io.StringIO(decoded_file.decode('utf-8')))
    
    # Separate the 'claim_id' column if it exists
    if 'claim_id' in df.columns:
        claim_ids = df['claim_id']
        df = df.drop(columns=['claim_id'])
    else:
        claim_ids = None
    
    # Send the DataFrame to the BentoML service as JSON
    response = requests.post(
        'http://127.0.0.1:3000/predict/',  # BentoML endpoint
        json=df.to_dict(orient='records')
    )
    
    # Retrieve predictions from the response
    predictions = response.json()['predictions']
    df['Prediction'] = predictions
    
    # Reattach the 'claim_id' column if it was present
    if claim_ids is not None:
        df['claim_id'] = claim_ids
    
    # Render the results in the results.html template
    return render_template('results.html', tables=[df.to_html(classes='data')])
    
if __name__ == '__main__':
    app.run(port=5005)
```

> **Note:** Ensure that both Flask and BentoML are installed in your Python environment to avoid import errors.

***

## Step 2: Creating HTML Templates

To provide a straightforward user interface, create a folder named `templates` in your project directory. Inside this folder, establish the following HTML templates:

### 1. index.html

This template displays the file upload interface for users. (Customize this file according to your design preferences.)

### 2. results.html

The `results.html` file displays prediction results formatted in a table. Below is an example template with basic table styling:

```html theme={null}
<html lang="en">
<head>
    <style>
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>Prediction Results</h1>

{{ table|safe }}

    <a href="/">Go Back</a>
</body>
</html>
```

### 3. Additional HTML for File Upload Handling

Below is a minimal HTML snippet that includes client-side logic for handling CSV file uploads. You can either incorporate this snippet within your `index.html` or save it as a separate file (for example, `visualize.html`):

```html theme={null}
<html lang="en">
<body>
<script>
function handleFile(file) {
    if (file && file.type === 'text/csv') {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            hiddenFileInput.value = reader.result;
            uploadForm.submit();
        };
    } else {
        alert('Please upload a valid CSV file.');
    }
}
</script>
</body>
</html>
```

These templates serve as a starting point for your application's user interface. In real-world projects, front-end engineers might further enhance or style these templates.

***

## Step 3: Running the Flask Application

After saving all your files, run your Flask application with the following command in your terminal:

```bash theme={null}
python3 flaskapp.py
```

The terminal output should resemble the following:

```plaintext theme={null}
* Serving Flask app "flaskapp"
* Debug mode: off
WARNING: This is a development server. Do not use it in production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5005/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 119-280-234
```

Open your browser and navigate to [http://127.0.0.1:5005/](http://127.0.0.1:5005/) to access the application.

***

## Step 4: Debugging Template Errors

If you encounter a `TemplateNotFound` error for `result.html` when uploading a CSV file, it indicates that Flask is attempting to render a template with an incorrect name. Verify that your template filenames are consistent with those being referenced in your Flask code. The correct file name should be `results.html` (plural), not `result.html`.

<Frame>
  ![The image shows a web page displaying a "TemplateNotFound" error from a Flask application, indicating that the "result.html" template is missing. It includes a traceback of the error in the code.](https://kodekloud.com/kk-media/image/upload/v1752875006/notes-assets/images/Fundamentals-of-MLOps-Demo-Upgrade-Python-Flask-App-to-Connect-to-BentoML-for-Online-Serving/flask-templatenotfound-error-traceback.jpg)
</Frame>

Review your project files in VS Code to confirm that the template folder contains the correctly named file:

<Frame>
  ![The image shows a Visual Studio Code interface with a project open, displaying an HTML file with some CSS styling and a terminal window below showing error logs related to a Python Flask application.](https://kodekloud.com/kk-media/image/upload/v1752875007/notes-assets/images/Fundamentals-of-MLOps-Demo-Upgrade-Python-Flask-App-to-Connect-to-BentoML-for-Online-Serving/vscode-html-css-flask-error-logs.jpg)
</Frame>

***

## Step 5: Testing the BentoML Integration

After resolving any template errors, refresh your page and drag-and-drop a CSV file containing claim data into the upload area. The application will then invoke the BentoML predict endpoint, and the ML model will process the claim data to return predictions.

For example, a prediction value of -1 may indicate that a claim requires further investigation, whereas a value of +1 suggests that the claim can be automatically approved. The prediction results are then rendered into a table displaying essential claim details, such as claim ID, amount, number of services, patient age, provider ID, days since the last claim, and the corresponding prediction value.

<Frame>
  ![The image shows a table titled "Prediction Results" with columns for claim details, including claim ID, amount, number of services, patient age, provider ID, days since last claim, and a prediction value.](https://kodekloud.com/kk-media/image/upload/v1752875009/notes-assets/images/Fundamentals-of-MLOps-Demo-Upgrade-Python-Flask-App-to-Connect-to-BentoML-for-Online-Serving/prediction-results-claim-details-table.jpg)
</Frame>

This organized presentation enables insurance agents to quickly pinpoint claims that require further review (i.e., those with a prediction of -1) while streamlining the approvals for other claims.

***

## Step 6: Architectural Overview

To summarize the entire workflow, consider the following steps:

1. Users submit claims through a dedicated portal.
2. The uploaded CSV file containing claim data is processed by the Flask app.
3. The processed data is sent as JSON to the BentoML predict endpoint.
4. The ML model hosted with BentoML analyzes the data and returns predictions.
5. Claims with a prediction of -1 are flagged for review, while those with +1 are automatically approved.
6. A Data Lake containing historical claim data supports the ML model training process, further enhancing prediction accuracy.

The complete architecture is illustrated in the following flowchart, which outlines the workflow from claim submission to final approval or review:

<Frame>
  ![The image is a flowchart illustrating an ML model designed to accelerate insurance claims processing, showing the steps from claim submission to approval and payout.](https://kodekloud.com/kk-media/image/upload/v1752875010/notes-assets/images/Fundamentals-of-MLOps-Demo-Upgrade-Python-Flask-App-to-Connect-to-BentoML-for-Online-Serving/ml-model-insurance-claims-flowchart.jpg)
</Frame>

***

## Conclusion

This end-to-end project demonstrates how to modernize the insurance claims process using an ML model served via BentoML, seamlessly integrated with a Flask-based user interface. By automating the detection of problematic claims and streamlining automatic approvals, this solution empowers insurance agents to focus on claims that genuinely require attention.

That concludes this lesson. See you in the next tutorial—thank you for joining us!

> **Note:** For additional details on Flask, BentoML, and integrating machine learning with web applications, visit the [Flask Documentation](https://flask.palletsprojects.com/) and [BentoML Docs](https://docs.bentoml.org/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/e6813732-5ba7-496f-84db-2272a4c2b188/lesson/4d1501a5-a355-4e62-bdf7-983fa207b988" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/e6813732-5ba7-496f-84db-2272a4c2b188/lesson/42386256-2f14-4178-8f7b-7f914547640d" />
</CardGroup>
