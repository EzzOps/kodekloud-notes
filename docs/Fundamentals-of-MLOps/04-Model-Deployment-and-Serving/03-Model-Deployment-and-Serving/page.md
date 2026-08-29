# API for V1 model prediction
@svc.api(input=JSON(pydantic_model=HouseInputV1), output=JSON(), route="/predict_house_price_v1")
async def predict_house_price_v1(data: HouseInputV1):
    input_data = [[data.square_footage, data.num_rooms]]
    prediction = await model_v1_runner.predict.async_run(input_data)
    return {"predicted_price_v1": prediction[0]}

# API for V2 model prediction
@svc.api(input=JSON(pydantic_model=HouseInputV2), output=JSON(), route="/predict_house_price_v2")
async def predict_house_price_v2(data: HouseInputV2):
    # One-hot encoding for the country
    country_encoded = [0, 0, 0]  # Default for ['Canada', 'Germany', 'UK']
    if data.country == "Canada":
        country_encoded[0] = 1
    elif data.country == "Germany":
        country_encoded[1] = 1
    elif data.country == "UK":
        country_encoded[2] = 1
    # Further processing and prediction logic for v2 can be added here...
```

By merging both prediction functions into a single BentoML service, we can efficiently manage traffic for legacy integrations (using v1) and for new clients (using v2).

The snippet below further defines the input schema for the v2 model along with an API endpoint for the v1 model again:

```python theme={null}
class HouseInputV2(BaseModel):
    num_bathrooms: int
    has_garage: int
    has_garden: int
    crime_rate: float
    avg_school_rating: float
    country: str

# API for v1 model prediction
@svc.api(input=JSON(pydantic_model=HouseInputV1), output=JSON(), route="/predict_house_price_v1")
async def predict_house_price_v1(data: HouseInputV1):
    input_data = [data.square_footage, data.num_rooms]
    prediction = await model_v1_runner.predict.async_run(input_data)
    return {"predicted_price_v1": prediction[0]}
```

After running the BentoML service command and refreshing the service endpoint, both the v1 and v2 endpoints become available. This separation ensures compatibility with legacy clients while allowing new features and improvements to be tested using the v2 endpoint.

Below, the following diagram shows the BentoML Prediction Service’s web interface. It displays the available API endpoints for house price prediction and provides additional information on infrastructure observability:

![The image shows a web interface for a BentoML Prediction Service, displaying API endpoints for house price prediction and infrastructure observability. It includes sections for service APIs, infrastructure endpoints, and schemas.](https://kodekloud.com/kk-media/image/upload/v1752875135/notes-assets/images/Fundamentals-of-MLOps-Demo-Upgrading-Model-Versions-with-BentoML-Serving/bentoml-prediction-service-api-endpoints.jpg)

## Testing the API Endpoints

You can use curl to send requests to these endpoints:

### Testing the v1 Endpoint

```bash theme={null}
curl -X POST "http://127.0.0.1:3000/predict_house_price_v1" \
-H "Content-Type: application/json" \
-d '{"square_footage": 2500, "num_rooms": 5}'
```

### Testing the v2 Endpoint

```bash theme={null}
curl -X POST "http://127.0.0.1:3000/predict_house_price_v2" \
-H "Content-Type: application/json" \
-d '{"square_footage": 2500, "num_rooms": 5, "num_bathrooms": 5, "house_age": 0, "distance_to_city_center": 0.5, "has_garden": 1, "has_garage": 1, "avg_school_rating": 4.5, "country": "Germany"}'
```

Below is a comprehensive example demonstrating the curl commands and their expected outputs:

```bash theme={null}
$ curl -X POST "http://127.0.0.1:3000/predict_house_price_v1" \
  -H "Content-Type: application/json" \
  -d '{"square_footage": 2500, "num_rooms": 5, "num_bathrooms": 5, "house_age": 10, "distance_to_city_center": 1.5, "has_garden": true, "has_garage": true, "crime_rate": 0.5, "avg_school_rating": 8.0, "country": "Germany"}'
```

```bash theme={null}
$ curl -X POST "http://127.0.0.1:3000/predict_house_price_v2" \
  -H "Content-Type: application/json" \
  -d '{"square_footage":2500, "num_rooms":5, "num_bathrooms":5, "house_age":10, "distance_to_city_center":1.5, "has_garden":true, "has_garage":true, "crime_rate":0.5, "avg_school_rating":8.0, "country":"Germany"}'
```

```bash theme={null}
predicted_price_v1: 366794.6602055242
predicted_price_v2: 367670.9746143092
```

> **lightbulb** Managing both endpoints within a single service simplifies the transition and allows controlled traffic routing. In the future, depending on your production needs and traffic patterns, you may consider separating these endpoints into different services.

## Additional Context: Extended Model Input Schema

Here is another version of the model input schema and its endpoint configuration. This variation provides additional parameters for more detailed predictions:

```python theme={null}
class HouseInputV2(BaseModel):
    num_bathrooms: int
    house_age: int
    distance_to_city_center: float
    has_garden: int
    crime_rate: float
    avg_school_rating: float
    country: str

# API for V2 model prediction
@svc.api(input=JSON(pydantic_model=HouseInputV2), output=JSON(), route="/predict_house_price_v2")
async def predict_house_price_v2(data: HouseInputV2):
    input_data = [[data.square_footage, data.num_rooms]]
    prediction = await model_v1_runner.predict.async_run(input_data)
    return {"predicted_price_v2": prediction[0]}
```

Test the improved service setup with the following curl requests:

### Testing the v1 Endpoint (Extended)

```bash theme={null}
curl -X POST "http://127.0.0.1:3000/predict_house_price_v1" \
  -H "Content-Type: application/json" \
  -d '{
  "square_footage": 2500,
  "num_rooms": 5,
  "num_bathrooms": 5,
  "house_age": 10,
  "distance_to_city_center": 10.5,
  "has_garden": 1,
  "has_garage": 1,
  "crime_rate": 0.5,
  "avg_school_rating": 8.5,
  "country": "Germany"
}'
```

### Testing the v2 Endpoint (Extended)

```bash theme={null}
curl -X POST "http://127.0.0.1:3000/predict_house_price_v2" \
  -H "Content-Type: application/json" \
  -d '{
  "square_footage": 2500,
  "num_rooms": 5,
  "num_bathrooms": 5,
  "house_age": 10,
  "distance_to_city_center": 10.5,
  "has_garden": 1,
  "has_garage": 1,
  "crime_rate": 0.5,
  "avg_school_rating": 8.5,
  "country": "Germany"
}'
```

This setup, which provides separate endpoints for different model versions using a single BentoML service, offers a controlled environment for traffic routing and facilitates a smoother transition from legacy models to new enhancements.

Thank you for following this lesson on upgrading model versions with BentoML Serving.

Below is a final example of using curl to test the v1 endpoint:

```bash theme={null}
curl -X POST "http://127.0.0.1:3000/predict_house_price_v1" \
    -H "Content-Type: application/json" \
    -d '{"square_footage": 2500, "num_rooms": 5}'
```

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/2bd484e3-8ec0-4fe4-8dd9-0f7f92e52970/lesson/1fe0d1ad-057b-4a58-8e5a-cf42989c11d3)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/2bd484e3-8ec0-4fe4-8dd9-0f7f92e52970/lesson/d76264e2-e5d0-4e0c-8d30-a70707537723)


# Model Deployment and Serving

Source: https://notes.kodekloud.com/docs/Fundamentals-of-MLOps/Model-Deployment-and-Serving/Model-Deployment-and-Serving/page

This article explores frameworks for deploying machine learning models in production, focusing on TensorFlow Serving, TorchServe, and BentoML for various application needs.

Hello and welcome back!

In this lesson, we explore three powerful frameworks for deploying machine learning models in production: TensorFlow Serving, TorchServe (for PyTorch models), and BentoML. These tools offer robust capabilities that cater to different needs—from high-throughput computer vision applications to flexible MLOps integration.

For example, if you are working on a TensorFlow-based computer vision model that must process thousands of images per second, TensorFlow Serving is an excellent choice. If deploying PyTorch NLP models with advanced A/B testing is your goal, TorchServe fits the bill. And for teams looking for a framework-agnostic solution with strong MLOps integration, BentoML is highly recommended.

BentoML has become a favorite among organizations because deploying models with BentoML Serving is very similar to deploying any microservice.

![The image lists three model serving tools: TensorFlow Serving for computer vision models, Torch Serve for PyTorch NLP models, and BentoML for framework-agnostic solutions.](https://kodekloud.com/kk-media/image/upload/v1752875136/notes-assets/images/Fundamentals-of-MLOps-Model-Deployment-and-Serving/model-serving-tools-tensorflow-torch-bentoml.jpg)

Let's dive into the key characteristics that make these frameworks essential for production-grade machine learning deployments.

## Purpose

These frameworks enable the scalable deployment of machine learning models in production environments. Consider a recommendation system serving millions of users; such a system leverages these tools to handle request queuing, batching, and automatic resource allocation seamlessly.

## Flexibility

The frameworks support diverse MLOps workflows. For instance, BentoML can serve both a Scikit-Learn model and a PyTorch model via the same API endpoint, offering extensive flexibility in managing different model types.

## Performance

Performance is critical in production settings. These tools are optimized for fast, low-latency predictions. TensorFlow Serving, for example, can achieve sub-10 millisecond latencies for inference, especially when paired with optimizations like TensorRT.

## Seamless Integration

Integration with DevOps and MLOps tools is smooth and efficient. You can integrate TorchServe with AWS SageMaker or Kubernetes to automate deployments, ensuring that machine learning models are updated and scaled to meet enterprise requirements.

![The image is an infographic titled "Model Serving Tools," highlighting four key features: Purpose, Flexibility, Performance, and Integration, each with a brief description.](https://kodekloud.com/kk-media/image/upload/v1752875138/notes-assets/images/Fundamentals-of-MLOps-Model-Deployment-and-Serving/model-serving-tools-infographic.jpg)

## Advanced Capabilities

Production environments often require more than just scalability and speed. Here are some advanced capabilities provided by these frameworks:

* **Customization:** Tailor your serving solutions using APIs. For example, implement custom preprocessing logic in TorchServe to resize images dynamically before inference.
* **Monitoring:** Maintain high performance by tracking key metrics such as inference time, throughput, and model accuracy drift. Integrate with monitoring tools like Prometheus to stay on top of performance changes.
* **Scalability:** Efficiently manage high-throughput requests. TensorFlow Serving can automatically scale to manage hundreds or even thousands of requests per second through load balancing and replica management.

> **lightbulb** Remember that each framework has its strengths. Your choice should align with your project’s specific requirements and deployment environment.

## Deployment Example: Inventory Prediction Dashboard

Consider an Inventory Prediction Dashboard used by warehouse operators. This dashboard is typically deployed on a Kubernetes cluster with the front-end operating in a dedicated namespace (the front-end namespace).

When a prediction is required, the front-end namespace makes an API call to the ML serving namespace, where the ML model—deployed, for example, with BentoML—is hosted. The processed result is then returned to the front-end namespace and rendered on the dashboard.

This architecture mirrors common microservice deployments and traditional DevOps processes, with the primary difference being the deployment of an ML model rather than a conventional application.

![The image illustrates a "Simple Model Serving Architecture" showing a flow from a warehouse operator to a dashboard, then through frontend and ML serving namespaces, connected to a CI/CD system and a machine learning model.](https://kodekloud.com/kk-media/image/upload/v1752875139/notes-assets/images/Fundamentals-of-MLOps-Model-Deployment-and-Serving/simple-model-serving-architecture.jpg)

> **lightbulb** In the next lesson, we will deploy an ML serving layer using BentoML. Stay tuned to continue your journey into production-grade ML deployments.

Thank you for reading, and see you in the next lesson!

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-mlops/module/2bd484e3-8ec0-4fe4-8dd9-0f7f92e52970/lesson/5d5f9d15-8382-4dec-ba25-e018c24df5ef)
