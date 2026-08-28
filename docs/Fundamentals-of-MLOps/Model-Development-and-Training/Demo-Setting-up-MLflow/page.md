# Set the MLflow tracking URI to the remote MLflow server
mlflow.set_tracking_uri("http://localhost:5000")

# Create synthetic data for regression
X, y = make_regression(n_samples=100, n_features=4, noise=0.1, random_state=42)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Set the experiment name in MLflow
mlflow.set_experiment("ML Model Experiment")

def log_model(model, model_name):
    with mlflow.start_run(run_name=model_name):
        # Train the model
        model.fit(X_train, y_train)
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Compute key metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        evs = explained_variance_score(y_test, y_pred)
        
        # Log metrics to MLflow
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("explained_variance", evs)
        
        # Log the model itself
        mlflow.sklearn.log_model(model, model_name)
        
        print(f"{model_name} - MSE: {mse}, RMSE: {rmse}, MAE: {mae}, R2: {r2}, Explained Variance: {evs}")

# Linear Regression Model
linear_model = LinearRegression()
log_model(linear_model, "Linear Regression")

# Decision Tree Regressor Model
tree_model = DecisionTreeRegressor()
log_model(tree_model, "Decision Tree Regressor")

# Random Forest Regressor Model
forest_model = RandomForestRegressor()
log_model(forest_model, "Random Forest Regressor")

print("Experiment completed! Check the MLflow server for details.")
```

## Installing Required Packages

Make sure you have scikit-learn installed. Open a new terminal session and run the following command:

```bash theme={null}
$ pip install scikit-learn
```

You might see output similar to:

```bash theme={null}
Requirement already satisfied: scikit-learn in /home/codespace/.local/lib/python3.12/site-packages (1.5.2)
Requirement already satisfied: numpy>=1.19.5 in /home/codespace/.local/lib/python3.12/site-packages (1.21.1)
Requirement already satisfied: scipy>=1.1.0 in /home/codespace/.local/lib/python3.12/site-packages (1.14.1)
Requirement already satisfied: joblib>=1.0.0 in /home/codespace/.local/lib/python3.12/site-packages (1.4.2)
Requirement already satisfied: threadpoolctl>=2.0.0 in /home/codespace/.local/lib/python3.12/site-packages (3.5.0)
[notice] A new release of pip is available: 24.2 → 24.3.1
[notice] To update, run: python3 -m pip install --upgrade pip
```

Once installed, run the example file with:

```bash theme={null}
$ python3 example_mlflow.py
```

Remember: Your MLflow UI must be running (in a separate terminal) so that the experiment data logs correctly.

## Analyzing Experiment Results in MLflow

After the execution, open the MLflow UI and navigate to the experiments section to find a new experiment titled "ML Model Experiment". Here, you will see three runs corresponding to the following models:

* Linear Regression
* Decision Tree Regressor
* Random Forest Regressor

<Frame>
  ![The image shows an MLflow interface displaying an experiment with three model runs: Random Forest Regressor, Decision Tree Regressor, and Linear Regression, each with details like creation time, duration, and source.](https://kodekloud.com/kk-media/image/upload/v1752875167/notes-assets/images/Fundamentals-of-MLOps-Demo-Running-and-experiment-and-storing-the-result-on-MLflow/mlflow-experiment-model-runs.jpg)
</Frame>

By selecting this experiment, you can view details such as run duration and input data. Use the evaluation section and select all the model runs, then click "Compare" to analyze key metrics side by side.

<Frame>
  ![The image shows an MLflow interface comparing three runs from one experiment, with a focus on a parallel coordinates plot for RMSE metrics. It includes details of each run, such as run ID, name, start and end times, and duration.](https://kodekloud.com/kk-media/image/upload/v1752875168/notes-assets/images/Fundamentals-of-MLOps-Demo-Running-and-experiment-and-storing-the-result-on-MLflow/mlflow-compare-runs-parallel-coordinates.jpg)
</Frame>

This comparison view provides valuable insights into the performance metrics of each model.

Another useful visualization is the contour plot, which helps compare metrics like explained variance, mean absolute error (MAE), and mean squared error (MSE) across runs.

<Frame>
  ![The image shows a contour plot from an MLflow experiment comparing three runs, with axes labeled for explained variance, mean absolute error (mae), and mean squared error (mse). Below the plot, there are details of the runs, including IDs, names, start and end times, and durations.](https://kodekloud.com/kk-media/image/upload/v1752875169/notes-assets/images/Fundamentals-of-MLOps-Demo-Running-and-experiment-and-storing-the-result-on-MLflow/mlflow-experiment-contour-plot.jpg)
</Frame>

This interface is invaluable for data science experiments, as it simplifies the process of selecting the best model based on performance metrics.

## Next Steps

That concludes this lesson. In our next article, we will discuss how to store the model file in the model registry.

Thank you, and see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/898cf36a-be28-4be6-b6cf-c616c1a4798e/lesson/08fa2087-31aa-4efa-a900-12866a28ad9c" />
</CardGroup>


# Demo Setting up MLflow

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Model-Development-and-Training/Demo-Setting-up-MLflow/page

This guide explains how to set up an MLflow server in a local development environment using Visual Studio Code.

Welcome to this comprehensive guide on setting up an MLflow server for your local development environment using Visual Studio Code. Follow along step-by-step with your terminal while you watch the terminal pane in VS Code similar to the demonstration below.

## Step 1: Install MLflow

MLflow is available as a package on PyPI. To install MLflow, run the following command in your terminal:

```bash theme={null}
pip install mlflow
```

Upon executing this command, you should observe output similar to the example below:

```bash theme={null}
Requirement already satisfied: scipy>=2 in /home/codespace/.local/lib/python3.12/site-packages (from mlflow) (1.14.1)
Collecting sqlalchemy<3,>=1.4.0 (from mlflow)
Downloading SQLAlchemy-2.0.36-cp312-cp312-manylinux2014_x86_64.whl.metadata (9.7 kB)
Collecting gunicorn<24 (from mlflow)
Downloading gunicorn-23.0.0-py3-none-any.whl.metadata (4.4 kB)
Collecting click<9,>=7.0 (from mlflow)
Downloading click-8.1.3-py3-none-any.whl.metadata (0.7 kB)
Collecting cloudpickle<2,>=1.3 (from mlflow)
Downloading cloudpickle-2.1.0-py3-none-any.whl.metadata (7.2 kB)
Collecting databricks-sdk<0.8,>=0.7 (from mlflow)
Requirement already satisfied: gitpython>=3.1.0 in /home/codespace/.local/lib/python3.12/site-packages (from mlflow) (3.1.43)
Collecting importlib-metadata<5.0,>=1.0 (from mlflow)
Downloading importlib_metadata-4.13.0-py3-none-any.whl (20 kB)
Collecting opentelemetry-api<1.0,>=0.26b (from mlflow)
Downloading opentelemetry_api-1.17.2-py3-none-any.whl (24.1 kB)
Collecting opentelemetry-sdk<1.17,>=1.14 (from mlflow)
Downloading opentelemetry_sdk-1.17.2-py3-none-any.whl (6.0.2)
Requirement already satisfied: protobuf<=5.0.0,>=3.15.0 in /home/codespace/.local/lib/python3.12/site-packages (from mlflow) (5.3.0)
Collecting sparselib<0.4,>=0.3 (from mlflow)
Downloading Mako-1.2.4-py3-none-any.whl (36 kB)
```

Additionally, you may encounter more package download messages, like in the output below:

```bash theme={null}
Downloading blinker-1.8.2-py3-none-any.whl (9.5 kB)
Downloading cachetools-5.5.0-py3-none-any.whl (9.5 kB)
Downloading click-8.1.7-py3-none-any.whl (97 kB)
Downloading cloudpickle-2.1.0-py3-none-any.whl (22 kB)
Downloading databricks-sdk-0.6.0-py3-none-any.whl (569 kB)
Downloading graphlib_core-3.2.5-py3-none-any.whl (16 kB)
Downloading graphql-relay-3.2.0-py3-none-any.whl (613 kB)
Downloading greenlet-1.1.3-cp312-cp312-manylinux_2_28_x86_64.whl (88 kB)
Downloading idna-3.4-py3-none-any.whl (64 kB)
Downloading isthetag-2.2.0-py3-none-any.whl (116 kB)
Downloading opentelemetry-api-1.20.0-py3-none-any.whl (149 kB)
Downloading opentelemetry-sdk-1.20.0-py3-none-any.whl (316 kB)
Downloading werkzeug-2.2.3-py3-none-any.whl (232 kB)
Downloading deprecated-2.14.0-py3-none-any.whl (12 kB)
Downloading pyasn1_modules-0.2.8-py3-none-any.whl (83 kB)
Downloading pyjwt-2.4.0-py3-none-any.whl (18 kB)
Downloading marshmallow-3.19.1-py3-none-any.whl (43 kB)
Downloading markupsafe-2.1.1-cp39-cp39-manylinux_2_10_x86_64.whl (11 kB)
Downloading Markdown-3.4.3-py3-none-any.whl (97 kB)
Downloading Mako-1.1.5-py3-none-any.whl (64 kB)
Downloading werkzeug-2.2.2-py3-none-any.whl (228 kB)
Downloading requests-2.28.1-py3-none-any.whl (62 kB)
Downloading Flask-2.2.2-py3-none-any.whl (98 kB)
Downloading google-auth-2.16.1-py3-none-any.whl (171 kB)
Downloading google-auth-oauthlib-0.4.6-py3-none-any.whl (17 kB)
```

<Callout icon="lightbulb">
  If the installation process prompts any errors, ensure that your pip version is up-to-date and you are using a supported version of Python.
</Callout>

## Step 2: Start the MLflow Server

Once the installation is complete, launch the MLflow UI by running:

```bash theme={null}
mlflow ui
```

This command will start the MLflow server, which listens on the default port 5000. You should see terminal output that resembles this:

```bash theme={null}
[2024-11-05 18:33:22 +0000] [7842] [INFO] Starting gunicorn 23.0.0
[2024-11-05 18:33:22 +0000] [7842] [INFO] Listening at: http://127.0.0.1:5000 (7842)
[2024-11-05 18:33:22 +0000] [7842] [INFO] Using worker: sync
[2024-11-05 18:33:22 +0000] [7848] [INFO] Booting worker with pid: 7848
[2024-11-05 18:33:22 +0000] [7862] [INFO] Booting worker with pid: 7862
[2024-11-05 18:33:22 +0000] [7863] [INFO] Booting worker with pid: 7863
[2024-11-05 18:33:22 +0000] [7864] [INFO] Booting worker with pid: 7864
```

<Callout icon="lightbulb">
  Click on the provided link or manually navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to access the MLflow UI.
</Callout>

## Step 3: Explore the MLflow UI

When you open the MLflow UI in your browser, you will initially see a default experiment. If no experiments have been logged, the experiment section will appear empty.

<Frame>
  ![The image shows an MLflow interface with no logged runs in the "Experiments" section, displaying a message that no runs have been logged yet.](https://kodekloud.com/kk-media/image/upload/v1752875170/notes-assets/images/Fundamentals-of-MLOps-Demo-Setting-up-MLflow/mlflow-experiments-no-runs-logged.jpg)
</Frame>

The MLflow UI acts as a centralized hub where all experiments are recorded. Here, you can:

* Begin a new experiment with a custom name.
* View detailed logs and traces.
* Compare the performance of different runs.
* Access the dedicated models section, which serves as the MLflow model repository.

In this demonstration, MLflow version 2.17.2 was installed by default since no specific version was provided during installation.

<Frame>
  ![The image shows an MLflow interface with a "Registered Models" page, indicating no models are registered yet and offering an option to create a model.](https://kodekloud.com/kk-media/image/upload/v1752875171/notes-assets/images/Fundamentals-of-MLOps-Demo-Setting-up-MLflow/mlflow-registered-models-empty.jpg)
</Frame>

## Conclusion

This tutorial has demonstrated how to set up a basic MLflow service on a local system. This setup can also be applied to other environments such as virtual machines or Kubernetes clusters.

Thank you for following this guide. Stay tuned for more detailed tutorials on advanced MLflow functionalities and usage scenarios.

Happy experimenting!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/898cf36a-be28-4be6-b6cf-c616c1a4798e/lesson/6cb31353-e706-4e2f-b304-557fd63a92d1" />
</CardGroup>
