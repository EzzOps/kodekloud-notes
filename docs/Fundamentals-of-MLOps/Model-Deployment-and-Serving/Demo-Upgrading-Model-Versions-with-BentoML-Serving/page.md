# Generate synthetic data for house price prediction
def generate_data():
    data = {
        'square_footage': [1000, 1500, 1800, 2000, 2300, 2500, 2700, 3000, 3200, 3500],
        'num_rooms': [3, 4, 4, 5, 6, 7, 7, 8, 8, 9],
        'price': [200000, 250000, 280000, 310000, 340000, 400000, 430000, 460000, 500000]
    }
    return pd.DataFrame(data)

# Load the data
df = generate_data()

# Define features and target
X = df[['square_footage', 'num_rooms']]
y = df['price']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

After training the model using linear regression, it is saved to the BentoML repository. To verify that the model has been saved, run:

```bash theme={null}
(bentoml-env) @learnwithraghu ~/workspaces/mLops-demo/Fundamentals-of-LLMops/04-bentoml (main) $ python3 model_train_v1.py
(bentoml-env) @learnwithraghu ~/workspaces/mLops-demo/Fundamentals-of-LLMops/04-bentoml (main) $ bentoml models list
Tag                          Module             Size      Creation Time
house_price_model:uyrh5n53xsoaan  bentoml.sklearn  1.23 KiB  2024-11-08 14:20:47
```

This output confirms that the house price model has been stored with a size of 1.23 KB and includes the associated creation timestamp.

***

## Serving the V1 Model

We now create an API endpoint to serve the trained model. The following code in `model_service_v1.py` loads the latest house price model from the repository, initializes a BentoML service, defines a Pydantic input schema, and registers the prediction endpoint:

```python theme={null}
import bentoml
from bentoml.io import JSON
from pydantic import BaseModel

# Load the model
model_ref = bentoml.sklearn.get("house_price_model:latest")
model_runner = model_ref.to_runner()

# Define the service
svc = bentoml.Service("house_price_predictor", runners=[model_runner])

# Input schema
class HouseInput(BaseModel):
    square_footage: float
    num_rooms: int

# API for prediction
@svc.api(input=JSON(pydantic_model=HouseInput), output=JSON())
async def predict_house_price(data: HouseInput):
    input_data = [[data.square_footage, data.num_rooms]]
    prediction = await model_runner.predict.async_run(input_data)
    return {"predicted_price": prediction[0]}
```

To serve the model, use the BentoML CLI with auto-reload enabled:

```bash theme={null}
(bentoml-env) ~/learnwithraghu ➜ /workspaces/mLops-demo/Fundamentals-of-LLMops/04-bentoml (main) $ bentoml serve model_service_v1.py --reload
```

Once the service has started, your default web browser may automatically open on the BentoML interface (typically running on port 3000), providing a user-friendly API documentation.

<Frame>
  ![The image shows a web interface for a machine learning service called "house\_price\_predictor:dev" created with BentoML, featuring API endpoints for predicting house prices and infrastructure observability.](https://kodekloud.com/kk-media/image/upload/v1752875133/notes-assets/images/Fundamentals-of-MLOps-Demo-Model-Serving-using-BentoML/house-price-predictor-bentoml-interface.jpg)
</Frame>

You can test the API using the "Try it out" feature on the UI or by sending a curl request:

```bash theme={null}
curl -X 'POST' 'https://vigilant-broccoli-664v5pjj97h5pg9-3000.app.github.dev/predict_house_price' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
  "square_footage": 2500,
  "num_rooms": 4
}'
```

Alternatively, test the service locally with:

```bash theme={null}
curl -X POST "http://127.0.0.1:3000/predict_house_price" \
-H "Content-Type: application/json" \
-d '{"square_footage": 2500, "num_rooms": 4}'
```

The service will return a JSON response with the predicted house price.

***

## Upgrading the Model (V2)

The second version of our model includes additional features that can enhance prediction accuracy. The upgraded model integrates parameters such as the number of bathrooms, house age, distance to the city center, and more. Below is the updated training script (`model_train_v2.py`):

```python theme={null}
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import bentoml

# Generate synthetic data for house price prediction with 10 features
def generate_data():
    data = {
        'square_footage': [1000, 1500, 1800, 2000, 2300, 2500, 2700, 3000, 3200, 3500],
        'num_rooms': [3, 4, 4, 5, 6, 6, 7, 7, 8, 9],
        'num_bathrooms': [1, 2, 1, 2, 2, 2, 3, 4, 4, 4],
        'house_age': [10, 5, 15, 20, 8, 25, 30, 35, 40, 45],
        'distance_to_city_center': [10, 15, 20, 5, 12, 18, 25, 30, 35, 40],
        'has_garage': [1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
        'has_garden': [1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
        'crime_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        'avg_school_rating': [4, 3, 5, 4, 3, 2, 1, 5, 3, 4],
        'country': ['USA', 'USA', 'USA', 'Canada', 'Canada', 'Canada', 'UK', 'UK', 'UK', 'Germany'],
        'price': [200000, 250000, 280000, 300000, 340000, 370000, 400000, 430000, 460000, 500000]
    }
    return pd.DataFrame(data)

# Load the data
df = generate_data()

# One-hot encode categorical features like 'country'
df = pd.get_dummies(df, columns=['country'], drop_first=True)

# Features and target
X = df.drop(columns=['price'])
y = df['price']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model with BentoML
bentoml.sklearn.save_model("house_price_model_v2", model)
```

After training, verify that the new model has been saved by running:

```bash theme={null}
(bentoml-env) @learnwithraghu ~/workspaces/mlops-demo/Fundamentals-of-LLMops/04-bentoml (main) $ python3 model_train_v2.py
(bentoml-env) @learnwithraghu ~/workspaces/mlops-demo/Fundamentals-of-LLMops/04-bentoml (main) $ bentoml models list
```

BentoML tags the most recent version as "latest" while retaining the previous model version. To serve the V2 model, create a new service file (e.g., `model_service_v2.py`) that incorporates the expanded input schema and then use the following commands:

```bash theme={null}
$ python3 model_train_v2.py
$ bentoml models list
$ bentoml serve model_service_v2.py --reload
```

You can test the upgraded API endpoint using the UI or by sending this curl request:

```bash theme={null}
curl -X POST "http://127.0.0.1:3000/predict_house_price" \
  -H "Content-Type: application/json" \
  -d '{
  "square_footage": 2500,
  "num_rooms": 5,
  "num_bathrooms": 3,
  "house_age": 10,
  "distance_to_city_center": 8,
  "has_garage": 1,
  "has_garden": 0,
  "crime_rate": 1,
  "avg_school_rating": 8,
  "country": "Germany"
}'
```

The expected JSON response should resemble:

```json theme={null}
{"predicted_price": 366760.9746143092}
```

***

## Recap

In this guide, we covered the following key steps:

| Step                  | Description                                                                           | Command/Example                                                              |
| --------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Environment Setup** | Created a virtual environment and installed dependencies                              | `python3 -m venv bento-ml-env`                                               |
| **Training V1 Model** | Built a linear regression model with synthetic data and saved it to BentoML           | `python3 model_train_v1.py`                                                  |
| **Serving V1 Model**  | Created an API endpoint using BentoML to serve the model                              | `bentoml serve model_service_v1.py --reload`                                 |
| **Upgrading to V2**   | Expanded the model with additional features and deployed using a new API service file | `python3 model_train_v2.py` and `bentoml serve model_service_v2.py --reload` |

<Callout icon="lightbulb">
  Integrating ML models with BentoML streamlines the deployment process, making it easy to serve and update models for real-time predictions.
</Callout>

Thank you for following this guide. With these steps, you can confidently deploy and serve your ML models using BentoML. Happy modeling and API serving!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/2bd484e3-8ec0-4fe4-8dd9-0f7f92e52970/lesson/4f2615a4-d3a3-4f25-af8c-5c4688996ffb" />
</CardGroup>


# Demo Upgrading Model Versions with BentoML Serving

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Model-Deployment-and-Serving/Demo-Upgrading-Model-Versions-with-BentoML-Serving/page

This tutorial explains how to upgrade machine learning model versions using BentoML while minimizing disruption to live user traffic.

Welcome to this tutorial on using BentoML to gradually upgrade your machine learning models without disrupting live user traffic. In this example, we have two versions of our ML model—v1 and v2. Switching all user traffic to a new version instantly is impractical in production environments. Instead, we use a blue-green deployment strategy to gradually route traffic between the two model versions.

In our previous setup, a single model was deployed. In a real-world scenario, you might host both model versions in the same BentoML service yet keep their traffic isolated on different endpoints. This design allows requests for v1 and v2 to be handled separately, ensuring a smooth transition for your users.

Below is a diagram that illustrates the model serving flow using BentoML. It shows how incoming requests are distributed between the different endpoints based on the model version:

<Frame>
  ![The image is a diagram illustrating model serving using BentoML, showing a flow from users to a dashboard, then to BentoML serving with endpoints for different model versions, and finally to a machine learning model.](https://kodekloud.com/kk-media/image/upload/v1752875134/notes-assets/images/Fundamentals-of-MLOps-Demo-Upgrading-Model-Versions-with-BentoML-Serving/bentoml-model-serving-diagram.jpg)
</Frame>

In this updated architecture, all incoming requests are processed by one of two endpoints, each corresponding to a different model version.

## Prediction Function for the House Price Model

In the VS Code editor, consider the following snippet that defines the prediction function for our house price model:

```python theme={null}
async def predict_house_price(data: HouseInput):
    input_data = [[
        data.distance_to_city_center, data.has_garage, data.has_garden,
        data.crime_rate, data.avg_school_rating
        + country_encoded
    ]]
    prediction = await model_runner.predict.async_run(input_data)
    return {"predicted_price": prediction[0]}
```

After stopping the BentoML service, clearing the screen, and closing the file, open the `model_service_v3.py` file to review its configuration. This file references both models (v1 and v2) by creating two separate model runners and exposing two distinct endpoints.

## Defining Separate Endpoints for Each Model Version

In `model_service_v3.py`, you will find code defining separate APIs for each model version:

```python theme={null}
