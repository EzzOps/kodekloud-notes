# Rolling deployment failure

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Rolling-deployment-and-Rollback-of-deployments/Rolling-deployment-failure/page

Shows a simulated Amazon ECS rolling deployment failure, explains why ECS does not auto rollback, and outlines mitigations like deployment circuit breaker, health checks, CodeDeploy, and CI/CD safeguards

Welcome back. This lesson demonstrates what happens when a rolling deployment in Amazon ECS fails and how that failure can leave your service unhealthy or stuck. We'll simulate a faulty build artifact, push it through the CI/CD pipeline, and observe ECS behavior so you can learn how to guard against and recover from such failures.

Environment: AWS Cloud9 (you may also use VS Code in similar labs).

What we'll do

* Introduce a deliberately broken application build.
* Push the change to the repository and trigger a CodeBuild run that produces a new container image.
* Update an ECS service to use the new task revision and observe the failed rolling deployment.
* Cover why ECS does not automatically rollback by default and outline mitigations.

Application (fixed, simplified Flask app)
The app shown below is the simplified Flask application used in the demo. In the lab, a developer intentionally removes or comments out critical code (for example, a route or import) to create a broken image that will fail at runtime or fail health checks.

```python theme={null}
