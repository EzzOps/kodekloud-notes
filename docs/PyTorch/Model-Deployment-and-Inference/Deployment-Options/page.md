# Taint a node
kubectl taint nodes node-name gpu-only=true:NoSchedule
```

Then, update the deployment manifest to include the necessary toleration:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpu-tolerant-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gpu-tolerant-app
  template:
    metadata:
      labels:
        app: gpu-tolerant-app
    spec:
      tolerations:
        - key: "gpu-only"
          operator: "Equal"
          value: "true"
          effect: "NoSchedule"
      containers:
        - name: gpu-container
          image: my-ml-model:latest
```

### Resource Requests and Limits

Defining resource requests and limits ensures that your ML models receive the necessary CPU, GPU, or memory while preventing competition between workloads.

<Frame>
  ![The image is a slide titled "Specialized Workloads" focusing on "Resource Requests and Limits," advising the allocation of CPU, GPU, and memory to avoid resource contention and ensure proper job execution.](https://kodekloud.com/kk-media/image/upload/v1752883218/notes-assets/images/PyTorch-Deploying-to-Kubernetes/specialized-workloads-resource-requests-limits.jpg)
</Frame>

For example, if your model requires one GPU and 4GB of memory, specifying these in your YAML manifest will help ensure efficient resource allocation.

## Deploying an ML Model to Kubernetes

Deploying an ML model with Kubernetes involves a series of well-defined steps:

1. **Containerization:** Package your trained model into a container using a model serving framework. Test the container locally to ensure it functions as expected.
2. **Preparing Kubernetes Resources:** Define your deployment, services, config maps, and secrets using YAML manifests. These configurations instruct Kubernetes on how to run and manage your model.
3. **Deployment:** Apply the YAML files using `kubectl` or integrate them into a GitOps pipeline. Verify the deployment using commands like `kubectl get pods` and `kubectl logs`.
4. **Testing and Scaling:** Use a REST client (such as Postman) to test the model endpoint. Configure an autoscaler (e.g., Horizontal Pod Autoscaler) to adjust pod counts dynamically based on traffic.

<Frame>
  ![The image shows a "Deployment Workflow" diagram with steps including "Containerize the Model," "Prepare Kubernetes Resources," "Deploy to Kubernetes," and "Test and Scale." The highlighted step, "Prepare Kubernetes Resources," involves creating YAML files and specifying resource requests and limits.](https://kodekloud.com/kk-media/image/upload/v1752883219/notes-assets/images/PyTorch-Deploying-to-Kubernetes/deployment-workflow-kubernetes-diagram.jpg)
</Frame>

<Frame>
  ![The image shows a "Deployment Workflow" for deploying to Kubernetes, highlighting steps like applying YAML files and verifying pod status. It includes a sidebar with steps: "Containerize the Model," "Prepare Kubernetes Resources," "Deploy to Kubernetes," and "Test and Scale."](https://kodekloud.com/kk-media/image/upload/v1752883220/notes-assets/images/PyTorch-Deploying-to-Kubernetes/deployment-workflow-kubernetes-diagram-2.jpg)
</Frame>

<Frame>
  ![The image shows a "Deployment Workflow" diagram with steps for containerizing a model, preparing Kubernetes resources, deploying to Kubernetes, and testing and scaling. The highlighted step, "Test and Scale," includes testing the model endpoint with a REST client and autoscaling using Horizontal Pod Autoscaler (HPA).](https://kodekloud.com/kk-media/image/upload/v1752883222/notes-assets/images/PyTorch-Deploying-to-Kubernetes/deployment-workflow-containerization-diagram.jpg)
</Frame>

## Horizontal Pod Autoscaler (HPA)

The Horizontal Pod Autoscaler (HPA) is critical for managing workload fluctuations. It automatically adjusts the number of pods based on real-time metrics such as CPU usage, memory consumption, or custom metrics, ensuring your deployment remains responsive and resource-efficient.

<Frame>
  ![The image illustrates a "Horizontal Pod Autoscaler" with a focus on low traffic during off-peak hours, showing a deployment of six pods.](https://kodekloud.com/kk-media/image/upload/v1752883223/notes-assets/images/PyTorch-Deploying-to-Kubernetes/horizontal-pod-autoscaler-low-traffic.jpg)
</Frame>

HPA dynamically scales pods based on utilization metrics. The following diagram outlines key components such as CPU utilization, memory usage, and custom application metrics that influence scaling decisions:

<Frame>
  ![The image is a diagram titled "Horizontal Pod Autoscaler" showing three components: CPU Utilization, Memory Usage, and Custom Application Metrics.](https://kodekloud.com/kk-media/image/upload/v1752883225/notes-assets/images/PyTorch-Deploying-to-Kubernetes/horizontal-pod-autoscaler-diagram.jpg)
</Frame>

<Frame>
  ![The image is a slide titled "Horizontal Pod Autoscaler," highlighting two benefits: handling high traffic to prevent downtime and optimizing resource usage during low traffic to reduce costs.](https://kodekloud.com/kk-media/image/upload/v1752883225/notes-assets/images/PyTorch-Deploying-to-Kubernetes/horizontal-pod-autoscaler-benefits.jpg)
</Frame>

Currently, GPU metrics are not natively supported, but you can integrate custom metric systems to monitor GPU usage.

Below is an example configuration that demonstrates HPA in action. The deployment manifest sets resource requests and limits, while the HPA definition scales the deployment based on CPU utilization:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-deployment
spec:
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      containers:
        - name: ml-model-container
          image: my-ml-model:latest
          resources:
            requests:
              cpu: "500m"
            limits:
              cpu: "1000m"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

When the average CPU utilization exceeds 70%, HPA automatically scales out up to 10 replicas. Conversely, if the utilization drops, the deployment scales back down to a minimum of 2 replicas, ensuring that your application adapts to traffic changes seamlessly.

## Best Practices for Deploying ML Models on Kubernetes

Adopting best practices is crucial for robust and efficient ML model deployments:

1. **Container Optimization:**\
   Use lightweight, optimized containers such as slim Docker images that include only the necessary files and dependencies. This practice speeds up deployments and reduces resource overhead.

<Frame>
  ![The image is a slide titled "Best Practices" with a focus on using lightweight containers, suggesting the optimization of containers like slim Docker images.](https://kodekloud.com/kk-media/image/upload/v1752883226/notes-assets/images/PyTorch-Deploying-to-Kubernetes/best-practices-lightweight-containers.jpg)
</Frame>

2. **Resource Monitoring:**\
   Leverage monitoring tools like Prometheus and Grafana to track CPU, memory, and GPU usage. Always define resource limits to avoid contention, especially in shared cluster environments.

<Frame>
  ![The image provides best practices for monitoring resource usage, suggesting the use of tools like Prometheus and Grafana, and setting resource limits for CPU, memory, and GPU.](https://kodekloud.com/kk-media/image/upload/v1752883228/notes-assets/images/PyTorch-Deploying-to-Kubernetes/monitoring-resource-usage-best-practices.jpg)
</Frame>

3. **Rolling Updates:**\
   Employ rolling updates for model deployments to minimize downtime. This approach allows gradual updates and ensures a smooth user experience.

<Frame>
  ![The image is a slide titled "Best Practices" with a focus on "Leverage Rolling Updates," highlighting the benefits of gradual deployment and minimal downtime.](https://kodekloud.com/kk-media/image/upload/v1752883229/notes-assets/images/PyTorch-Deploying-to-Kubernetes/best-practices-rolling-updates.jpg)
</Frame>

4. **Security Measures:**\
   Implement strict security best practices by using Role-Based Access Control (RBAC) and network policies to restrict permissions for pods. This minimizes unauthorized access risks.

<Frame>
  ![The image is a slide titled "Best Practices" with a focus on "Enforce Security," suggesting the use of RBAC (Role-Based Access Control) to restrict permissions.](https://kodekloud.com/kk-media/image/upload/v1752883230/notes-assets/images/PyTorch-Deploying-to-Kubernetes/best-practices-enforce-security-rbac.jpg)
</Frame>

## ML Serving Frameworks for Kubernetes

While Kubernetes' native resources (Deployments, Services, etc.) suffice for many model deployments, specialized ML serving frameworks can streamline and enhance the process:

* **KServe (formerly KFServing):**\
  Specifically designed for serving ML models on Kubernetes, KServe supports advanced features such as explainability and model monitoring, making it perfect for production-grade deployments.

* **Seldon Core:**\
  Offers interoperability for models built on different frameworks. Seldon Core facilitates complex workflows like ensemble models and A/B testing while integrating natively with Kubernetes.

* **Triton Inference Server:**\
  Developed by NVIDIA, Triton provides GPU-accelerated inference and supports dynamic batching across multiple ML frameworks (TensorFlow, PyTorch, ONNX).

<Frame>
  ![The image lists three ML serving frameworks: KServe, Seldon Core, and Triton Inference Server, each with a brief description of their features.](https://kodekloud.com/kk-media/image/upload/v1752883230/notes-assets/images/PyTorch-Deploying-to-Kubernetes/ml-serving-frameworks-kserve-seldon-triton.jpg)
</Frame>

These frameworks also offer crucial capabilities such as model versioning, autoscaling, and integrated logging and monitoring, enabling efficient troubleshooting and management of multiple model versions.

<Frame>
  ![The image lists three key features of frameworks: model versioning and rollout strategies, autoscaling based on traffic, and logging and monitoring tools for ML workloads.](https://kodekloud.com/kk-media/image/upload/v1752883232/notes-assets/images/PyTorch-Deploying-to-Kubernetes/frameworks-key-features-ml-tools.jpg)
</Frame>

## Conclusion

Kubernetes provides a powerful and flexible platform for deploying machine learning models. Its ability to handle scalability, efficiently allocate resources, and adapt to diverse deployment scenarios makes it an excellent choice for modern ML workloads. Key techniques such as utilizing node affinity, applying taints and tolerations, and setting appropriate resource requests and limits simplify the deployment process.

By following best practices—optimizing containers, monitoring resources, employing rolling updates, and enforcing security measures—you can ensure robust and efficient deployments. Additionally, leveraging ML serving frameworks like KServe, Seldon Core, and Triton Inference Server further enhances your deployment capabilities with advanced features like autoscaling, model versioning, and integrated monitoring.

Let's now load up a Kubernetes cluster and deploy our model application using these best practices and real-world strategies.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-845c-4cdf-9261-7688050bd96c/lesson/254f1dc1-743a-495f-b990-c6aa13a334d6" />
</CardGroup>


# Deployment Options

Source: https://notes.kodekloud.com/docs/PyTorch/Model-Deployment-and-Inference/Deployment-Options/page

Overview of model deployment options for PyTorch, including formats, serving frameworks, and infrastructure components.

Congratulations on reaching this stage of the course!

After building and evaluating three models, it's time to share your best creation with your client at Awesome AI. In this lesson, we’ll provide an overview of model deployment options for PyTorch. You’ll learn about various deployment formats, serving frameworks, and essential infrastructure components. While some topics will be explored in further detail in later lessons, this guide offers a comprehensive outline to help you get started.

<Frame>
  ![The image shows an agenda with five points related to deployment options, formats, service frameworks, infrastructure components, and tools for effective deployment.](https://kodekloud.com/kk-media/image/upload/v1752883234/notes-assets/images/PyTorch-Deployment-Options/deployment-options-agenda.jpg)
</Frame>

## Deployment Formats

When deploying models, you don't have to stick to the native PyTorch format. Alternative formats can optimize your model's performance and extend its compatibility.

### ONNX

ONNX (Open Neural Network Exchange) is a widely adopted format that enables cross-framework model usage. Converting a PyTorch model to ONNX facilitates integration into systems that do not natively support PyTorch. This conversion also standardizes model inference, making it suitable for diverse platforms—from centralized servers to edge devices.

### Quantization

Quantization reduces the size and computational requirements of your model, making it especially useful for devices with limited resources such as mobile phones or IoT devices. Techniques like Int8, Dynamic, and Mixed Precision Quantization can significantly boost inference speed with minimal impact on accuracy.

<Callout icon="lightbulb">
  Quantization is a complex topic and may warrant its own dedicated lesson.
</Callout>

### GGUF

GGUF is a lightweight format optimized for low-latency inference, ideal for edge and mobile deployments where computational resources are limited. It has recently gained popularity, especially with tools like [Running Local LLMs With Ollama](https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama), which allow large language models (LLMs) to run on devices with just a CPU.

<Frame>
  ![The image is a comparison of model formats for deployment, highlighting Open Neural Network Exchange (ONNX), Quantization, and GGUF, each with their respective benefits.](https://kodekloud.com/kk-media/image/upload/v1752883236/notes-assets/images/PyTorch-Deployment-Options/model-formats-comparison-onnx-quantization-gguf.jpg)
</Frame>

## Serving Frameworks

To make your PyTorch models accessible, you need serving frameworks that expose your model via web endpoints. When a request is sent over HTTP, these endpoints return a prediction from the model. Here are three popular options:

### Flask

Flask is a lightweight Python web framework known for its simplicity. It is ideal for small-scale deployments where extensive features are not necessary. More in-depth coverage of Flask will be provided in a later lesson.

### FastAPI

Designed for high-performance applications, FastAPI is perfect for creating APIs that require asynchronous execution. It efficiently handles multiple requests simultaneously and offers a robust feature set, making it a favorite for serving models.

<Frame>
  ![The image is about FastAPI, highlighting it as a high-performance, feature-rich framework that is becoming popular for machine learning.](https://kodekloud.com/kk-media/image/upload/v1752883236/notes-assets/images/PyTorch-Deployment-Options/fastapi-high-performance-framework.jpg)
</Frame>

### TorchServe

TorchServe is crafted specifically for serving PyTorch models. It includes useful features such as model versioning and inference batching, which facilitate managing model updates and optimizing performance. However, it may not offer the same level of flexibility as Flask or FastAPI.

<Frame>
  ![The image is a presentation slide about "Serving Frameworks," specifically focusing on TorchServe, a PyTorch-specific serving framework. It highlights features like model versioning and inference batching, noting it is less flexible compared to Flask or FastAPI.](https://kodekloud.com/kk-media/image/upload/v1752883237/notes-assets/images/PyTorch-Deployment-Options/serving-frameworks-torchserve-slide.jpg)
</Frame>

## Deployment Infrastructure

In addition to selecting the proper model format and serving framework, containerization and scalable deployment tools are essential for successful deployment.

### Docker

Docker packages your application along with its dependencies into containers, ensuring consistent performance across your local machine, servers, or cloud environments. Key benefits of Docker include:

* Easy sharing and deployment of your model
* Simplified scaling and dependency management

<Frame>
  ![The image explains containerization, highlighting that it packages apps with dependencies into containers and ensures consistent performance across deployments.](https://kodekloud.com/kk-media/image/upload/v1752883239/notes-assets/images/PyTorch-Deployment-Options/containerization-apps-dependencies-diagram.jpg)
</Frame>

<Frame>
  ![The image illustrates the benefits of containerization, highlighting easy sharing and deployment of models, and simplified scaling and management of dependencies.](https://kodekloud.com/kk-media/image/upload/v1752883239/notes-assets/images/PyTorch-Deployment-Options/containerization-benefits-sharing-scaling.jpg)
</Frame>

### Kubernetes

Kubernetes is an orchestration platform for managing containerized applications, making it indispensable for large-scale deployments. Its standout features include:

* Autoscaling containers based on traffic demands
* Rolling updates for seamless version transitions without downtime
* Resource monitoring and management to optimize performance

<Frame>
  ![The image is an infographic titled "Scaling With Kubernetes," highlighting four features: autoscaling, rolling updates, resource monitoring and management, and preferred deployment platform.](https://kodekloud.com/kk-media/image/upload/v1752883241/notes-assets/images/PyTorch-Deployment-Options/scaling-with-kubernetes-infographic.jpg)
</Frame>

### Cloud Platforms

Deploying models to the cloud simplifies scaling and reduces the complexity of managing infrastructure. Popular cloud platforms include:

* **AWS SageMaker:** A fully managed service that handles both training and deployment, eliminating the need for infrastructure management.
* **Google Vertex AI:** Offers versatile options including serverless hosting for efficient deployment.
* **Azure ML:** Known for robust MLOps support and suitability for hybrid and edge deployments.

<Frame>
  ![The image compares three cloud platforms for deploying machine learning models: AWS SageMaker, Google Cloud Vertex AI, and Azure ML, highlighting their features and capabilities.](https://kodekloud.com/kk-media/image/upload/v1752883242/notes-assets/images/PyTorch-Deployment-Options/cloud-platforms-ml-comparison.jpg)
</Frame>

## Best Practices for Model Deployment

Deploying your PyTorch model effectively requires a strategic approach. Consider the following best practices to ensure a robust deployment.

### Model Preparation

* Optimize your model by converting it to ONNX for improved cross-platform compatibility.
* Apply quantization techniques to minimize model size and reduce latency.

<Frame>
  ![The image is a slide titled "Model Deployment – Best Practices," focusing on "Model Preparation" with a note to use ONNX for compatibility and quantization for efficiency.](https://kodekloud.com/kk-media/image/upload/v1752883243/notes-assets/images/PyTorch-Deployment-Options/model-deployment-best-practices-onnx.jpg)
</Frame>

### Testing

* Test your model thoroughly in a staging environment that closely mirrors production settings to verify its accuracy and performance.

### Version Control

* Use semantic versioning to maintain and track different versions of your models. This practice enhances reproducibility and simplifies change management.

### Monitoring and Maintenance

* Keep track of vital metrics such as latency, throughput, and error rates.
* Regularly monitor both input data variations and model outputs to detect any performance degradation.

<Frame>
  ![The image is a slide titled "Model Deployment – Best Practices," focusing on "Monitoring and Maintenance" with a note to track metrics like latency, throughput, and error rates.](https://kodekloud.com/kk-media/image/upload/v1752883244/notes-assets/images/PyTorch-Deployment-Options/model-deployment-best-practices-monitoring.jpg)
</Frame>

### Infrastructure and Scalability

* Package your model with Docker along with all its dependencies.
* Leverage Kubernetes for efficient resource management, automated scaling, and hassle-free deployment.
* Select a cloud platform (AWS, Google, or Azure) that best matches your application's requirements.

### Security

* Secure your APIs using HTTPS, and implement robust authentication and authorization mechanisms.
* Adhere to data privacy standards such as GDPR, ensuring that sensitive information is encrypted during transit and at rest.

<Frame>
  ![The image is a slide titled "Model Deployment – Best Practices" focusing on security, highlighting the importance of securing APIs with HTTPS, authentication, and authorization, and following data privacy standards like GDPR.](https://kodekloud.com/kk-media/image/upload/v1752883246/notes-assets/images/PyTorch-Deployment-Options/model-deployment-best-practices-security.jpg)
</Frame>

## Summary

In summary, deploying PyTorch models involves multiple layers of decision-making:

* **Deployment Formats:** Use ONNX for cross-platform support, quantization for performance optimization, and GGUF for low-latency inference in resource-constrained environments.
* **Serving Frameworks:** Choose from Flask and FastAPI for flexible API-based serving or TorchServe for PyTorch-specific features like versioning and inference batching.
* **Infrastructure Tools:** Docker ensures consistent, containerized deployments, while Kubernetes provides scalability and seamless updates through automated resource management.
* **Cloud Platforms:** Platforms like AWS SageMaker, Google Cloud Vertex AI, and Azure ML simplify the deployment process with managed services that handle scaling and infrastructure.

<Frame>
  ![The image is a summary of best practices for deploying models, including using specific formats, frameworks, tools, cloud platforms, and following optimization and security practices.](https://kodekloud.com/kk-media/image/upload/v1752883248/notes-assets/images/PyTorch-Deployment-Options/model-deployment-best-practices-summary.jpg)
</Frame>

Deploying models effectively requires a well-rounded approach that considers model optimization, infrastructure management, performance monitoring, and security. With these tools and best practices, your PyTorch models will be well-equipped for real-world applications.

Let's move on to the demo where we will see some of these concepts in action.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-845c-4cdf-9261-7688050bd96c/lesson/20d94f6c-8b89-4682-9878-3a3fcbc2c768" />
</CardGroup>
