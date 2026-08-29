# Custom Images

Source: https://notes.kodekloud.com/docs/HashiCorp-Packer/HashiCorp-Packer-Basics/Custom-Images/page

Streamline deployments by bundling application code and server configuration into a single, ready-to-deploy image using tools like HashiCorp Packer.

Streamline your deployments by bundling application code and server configuration into a single, ready-to-deploy image. Tools like HashiCorp Packer automate the image-building process, producing fully configured artifacts for any environment.

<Callout icon="lightbulb">
  Immutable images guarantee consistency, repeatability, and reliability across development, testing, and production.
</Callout>

## Why Use Custom Images?

| Benefit     | Description                                                                 |
| ----------- | --------------------------------------------------------------------------- |
| Consistency | Every environment runs the exact same image.                                |
| Speed       | Pre-baked configurations reduce startup time.                               |
| Security    | Reduce drift by disallowing manual changes to running instances.            |
| Automation  | Integrate with CI/CD pipelines for hands-off image creation and deployment. |

## Image-Building Tools

| Tool               | Use Case                  | Example Command                            |
| ------------------ | ------------------------- | ------------------------------------------ |
| HashiCorp Packer   | VM and cloud image builds | `packer build template.json`               |
| Docker             | Container images          | `docker build -t myapp:latest .`           |
| Custom AMI Scripts | AWS EC2 image automation  | `aws ec2 create-image --instance-id i-123` |

## Sample Workflow

1. Define your machine configuration in Packer (or a Dockerfile).
2. Run the build command to generate an immutable image.
3. Push the image to your registry or cloud provider.
4. Deploy new instances using the updated image.

```javascript theme={null}
while (alive) {
    eat();
    sleep();
    code();
    repeat();
}
```

<Callout icon="triangle-alert">
  Never modify a running image in place. Always build and deploy a new image for updates.
</Callout>

## Additional Resources

* [HashiCorp Packer Documentation](https://www.packer.io/docs)
* [Immutable Infrastructure—Martin Fowler](https://martinfowler.com/bliki/ImmutableServer.html)
* [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-packer/module/88bc689f-1e45-49d8-887c-cb44923b3390/lesson/72e6baf3-a447-4244-a215-fa4edb0ea427" />
</CardGroup>
