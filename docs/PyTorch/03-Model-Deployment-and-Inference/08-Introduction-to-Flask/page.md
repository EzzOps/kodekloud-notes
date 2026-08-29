# Build docker image called flask-app
docker build -t flask-app .
```

The dot indicates that the current directory serves as the build context, including the Dockerfile and any other required files.

To run the container and map the container's port 5000 to the host's port 5000, execute:

```shell theme={null}
# Run container from image
docker run -p 5000:5000 flask-app

# List available images
docker image ls
```

The `docker run` command creates and starts a container, while `docker image ls` lists all available Docker images.

Images can then be pushed to a registry for production deployment or team collaboration. When using Docker Hub, the workflow typically follows this sequence:

```shell theme={null}
# Tag the image
docker tag flask-app your-username/flask-app:latest

# Push to the registry
docker push your-username/flask-app:latest

# Pull the image
docker pull your-username/flask-app:latest

# Run the pulled image
docker run -p 5000:5000 your-username/flask-app:latest
```

For more information, see the [Docker Documentation](https://docs.docker.com/).

***

## Model Deployment Approaches

When deploying models with Docker, there are two popular approaches:

1. **Embedding the Model Directly into the Container**\
   The model is incorporated during the build process, simplifying deployment because every component is bundled together. However, this method can lead to larger container sizes and reduced flexibility for updating the model.

2. **Using a Model Registry**\
   The model is stored externally (e.g., on AWS S3, Google Cloud Storage, or managed via MLflow) and is downloaded at runtime. This reduces the container size and allows for easier updates without rebuilding the image.

<Frame>
  ![The image compares containerizing a model with using a model registry, highlighting embedding a PyTorch model in a container for simplified deployment and a self-contained container image.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883255/notes-assets/images/PyTorch-Introduction-to-Docker/model-container-vs-registry-comparison.jpg)
</Frame>

Both approaches have their merits; your choice will depend on your specific deployment requirements.

***

## Best Practices for Docker Deployment

Adhering to best practices when deploying models or applications using Docker can significantly improve efficiency, security, and scalability:

* **Efficient Image Management:**\
  Use lightweight base images such as Python 3.9 Slim to reduce image size. Remove intermediate files during the build process to keep your images lean.

<Frame>
  ![The image outlines best practices for efficient image management, suggesting the use of lightweight base images and cleaning up intermediate files during the build.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883255/notes-assets/images/PyTorch-Introduction-to-Docker/efficient-image-management-best-practices.jpg)
</Frame>

* **Security:**\
  Avoid running containers as the root user and opt for official or trusted base images to minimize vulnerabilities.

<Frame>
  ![The image provides best practices for security, advising to avoid running containers as root and to use official or trusted base images to minimize vulnerabilities.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883256/notes-assets/images/PyTorch-Introduction-to-Docker/security-best-practices-containers.jpg)
</Frame>

* **Scalability:**\
  Utilize tools like Docker Compose to manage multiple containers during development, and consider orchestration solutions such as Kubernetes for scaling production deployments.

<Frame>
  ![The image provides best practices for scalability, suggesting the use of Docker Compose for multiple containers in development and Kubernetes for large-scale production deployments.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883258/notes-assets/images/PyTorch-Introduction-to-Docker/scalability-best-practices-docker-kubernetes.jpg)
</Frame>

Below is a summary table highlighting various Docker components along with usage examples:

| Component    | Purpose                                                     | Command/Example                     |
| ------------ | ----------------------------------------------------------- | ----------------------------------- |
| Dockerfile   | Defines steps to build a Docker image                       | `docker build -t flask-app .`       |
| Docker Image | A packaged snapshot of the application and its dependencies | `docker image ls`                   |
| Container    | A running instance of a Docker image                        | `docker run -p 5000:5000 flask-app` |

***

## Summary

In this article, we covered the essentials of Docker and its significance in model deployment. Key takeaways include:

* Docker facilitates packaging applications into portable containers, ensuring consistency and reliability across diverse environments.
* The Docker architecture comprises vital components such as the Docker Engine, images, containers, and Dockerfiles.
* Containerization involves writing a Dockerfile, building an image, and running a container, with the option to push the image to a registry.
* Two primary approaches to model deployment with Docker include embedding the model directly into the container or leveraging an external model registry.
* Best practices for Docker deployment focus on maintaining lean images, ensuring security, and scaling effectively using tools like Docker Compose and Kubernetes.

<Frame>
  ![The image is a summary of Docker's features and best practices, highlighting containerization, key components, and the process of building and managing container images.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883259/notes-assets/images/PyTorch-Introduction-to-Docker/docker-features-best-practices-summary.jpg)
</Frame>

By following these guidelines, you can enhance your model deployment process and fully harness the benefits of Docker for efficient, scalable, and secure application management. For more detailed information, refer to the [official Docker documentation](https://docs.docker.com/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-845c-4cdf-9261-7688050bd96c/lesson/c686a7f3-2e4b-4c36-a212-dc9b95354760" />
</CardGroup>


# Introduction to Flask

Source: https://notes.kodekloud.com/docs/PyTorch/Model-Deployment-and-Inference/Introduction-to-Flask/page

This guide explores deploying PyTorch models using Flask, covering setup, integration, and best practices for creating an inference API.

In this guide, we explore how to deploy PyTorch models using Flask—a lightweight Python web framework that seamlessly transforms research code into accessible, production-ready services. You’ll learn what Flask is, why it’s an excellent choice for deployment, and how to set up a basic Flask application that loads a trained PyTorch model and creates an inference API endpoint.

<Frame>
  ![The image shows an agenda with three points: an introduction to Flask for deploying PyTorch models, setting up a Flask application and API for predictions, and best practices for running Flask applications.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883260/notes-assets/images/PyTorch-Introduction-to-Flask/flask-pytorch-models-agenda.jpg)
</Frame>

Let's dive in.

Flask is a simple, lightweight, and flexible web framework that makes building Python web applications fast and modular. Its minimalistic approach means you only add the functionality you require, which keeps projects well-organized and scalable—ideal for both beginners and more complex applications.

<Frame>
  ![The image is an introduction slide for Flask, describing it as a simple, lightweight, and flexible tool for building Python web applications, ideal for beginners.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883261/notes-assets/images/PyTorch-Introduction-to-Flask/flask-introduction-lightweight-tool.jpg)
</Frame>

Flask comes equipped with a built-in development server and debugger, along with robust support for creating RESTful APIs. These features make it perfectly suited for deploying machine learning models where quick testing and clear error reporting are critical.

<Frame>
  ![The image lists key features of Flask, highlighting its minimalistic and modular design, built-in development server and debugger, and support for RESTful request dispatching.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883262/notes-assets/images/PyTorch-Introduction-to-Flask/flask-key-features-minimalistic-design.jpg)
</Frame>

With its clarity, comprehensive documentation, and seamless integration with PyTorch, Flask is a top choice for deploying machine learning services. Although it is not designed for high-performance computing out-of-the-box, its stability and ease of use make it a robust choice for a wide range of applications.

<Frame>
  ![The image lists the advantages of Flask, highlighting ease of use, flexibility, integration, and scalability. Each advantage is briefly described with an icon and text.](../../../../images/kodekloud.com/kk-media/image/upload/v1752883264/notes-assets/images/PyTorch-Introduction-to-Flask/flask-advantages-ease-flexibility-integration-scalability.jpg)
</Frame>

## Installing Flask

To start using Flask, install it via pip. Open your terminal and run the following command:

```bash theme={null}
