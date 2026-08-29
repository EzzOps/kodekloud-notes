# Establish a connection to the Redis database using environment variables for host and port.
redis_db = Redis(host=os.getenv('HOST'), port=os.getenv('PORT'))
redis_db.set('visitorCount', 0)
```

The code above demonstrates how to connect to the Redis database and reset the `visitorCount` to 0. Running tasks like this as isolated, one-off processes ensures that they are automated, scalable, and reproducible, in alignment with the [12-Factor App](https://learn.kodekloud.com/user/courses/12-factor-app) principle of keeping admin tasks separate from long-running application processes.

> **lightbulb** The admin processes principle advocates for executing any administrative task—whether it is a one-time operation or a periodic task—in isolation. This guarantees that these operations remain automated, scalable, and reproducible, while mirroring the configuration of the primary application environment.

- [Watch Video](https://learn.kodekloud.com/user/courses/12-factor-app/module/086a3d2d-be7f-4b05-92ae-1b2e4ab90f6a/lesson/1f1dcebc-971d-4af7-a084-f4fb2712bb06)


# Backing Services

Source: https://notes.kodekloud.com/docs/12-Factor-App/Twelve-Factor-App-methodology/Backing-Services/page

Backing services are external resources your application relies on, enabling consistent integration and flexibility across different deployment environments.

Backing services are external resources that your application depends on. These services can range from caching solutions like Redis to email providers, object storage services, and more. For instance, we integrated Redis as a caching service in our application to store the visitor count. Other typical backing services include:

* SMTP services for sending emails
* S3 integrations for storing images
* Managed databases and search engines

Your application should be designed to interact with these backing services as attached resources. This means that regardless of whether the service is hosted locally, on a managed cloud platform, or as a cloud-native service, the integration remains consistent. The application code should remain unchanged when switching between different deployment environments.

> **lightbulb** The concept of treating backing services as attached resources enables seamless scaling and flexibility. Simply update configuration details to point your application to a new instance without modifying any code logic.

## Redis as a Backing Service Example

Consider Redis, which we use as a caching layer:

* **Local Instance:** You might run Redis on your local machine during development.
* **Cloud Deployment:** In a production environment, Redis might be hosted on a cloud provider like AWS or Azure.
* **Managed Service:** Alternatively, you could use a managed Redis service offered by various vendors.

Despite these variations, your application logic remains the same. You only need to update the connection settings to point to the chosen Redis instance.

> **lightbulb** Ensure that all your backing services are configurable via environment variables or external configurations. This decouples service specifics from your application code, enhancing portability and maintainability.

## Why This Architecture Matters

By decoupling applications from the specific implementations of backing services, you gain flexibility and resilience in your deployment. Whether scaling up in cloud environments or switching service providers, your application's core functionality remains intact.

For more detailed insights and integration guidelines, explore comprehensive examples and further documentation on working with backing services.

## Additional Resources

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

This approach not only simplifies deployments but also enhances the maintainability of your system by following best practices for service-oriented design.

- [Watch Video](https://learn.kodekloud.com/user/courses/12-factor-app/module/086a3d2d-be7f-4b05-92ae-1b2e4ab90f6a/lesson/3d8c71d7-3c86-42d3-9856-dbdf894280e2)
