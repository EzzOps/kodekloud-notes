# Export the name of the bucket
bucketName: ${my-bucket.id}
resources:
  # Create an AWS resource (S3 Bucket)
  my-bucket:
    type: aws:s3:Bucket
```

Or, with the HTML bucket object:

```yaml theme={null}
resources:
  # Create an AWS resource (S3 Bucket)
  my-bucket:
    type: aws:s3:Bucket

  # Create an S3 Bucket object for index.html
  index.html:
    type: aws:s3:BucketObject
    properties:
      bucket: ${my-bucket.id}
      source: fn:fileAsset("./index.html")

outputs:
  # Export the name of the bucket
  bucketName: ${my-bucket.id}
```

***

## Redeploy the Updated Project

After updating your configuration and HTML file, redeploy your project with the following commands:

```bash theme={null}
controlplane ~/quickstart $ cat index.html
<html>
<body>Hello, Pulumi!</body>
</html>

controlplane ~/quickstart $ vi Pulumi.yaml
controlplane ~/quickstart $ pulumi up
Please choose a stack, or create a new one: dev
Previewing update (dev)

View in Browser (Ctrl+L): https://app.pulumi.com/trungkodekloud/quickstart/dev/preview
Type                 Name                   Plan
pulumi:pulumi:Stack  quickstart-dev        create
aws:s3:Bucket      my-bucket             create
aws:s3:BucketObject index.html            create

Outputs:
    bucketName: output<string>

Resources:
    + 3 to create

Do you want to perform this update? yes
View in Browser (Ctrl+L): https://app.pulumi.com/trungkodekloud/quickstart/dev/updates/1
type                 name                   status
pulumi:pulumi:Stack  quickstart-dev        creating (0s)
```

Once the deployment is complete, verify the contents of the S3 bucket by running:

```bash theme={null}
$ aws s3 ls $(pulumi stack output bucketName)
```

A potential output might be:

```plaintext theme={null}
2023-04-20 17:01:86      118 index.html
```

Finally, list all S3 buckets to confirm the deployment:

```bash theme={null}
controlplane ~/quickstart * aws s3 ls
```

***

> **lightbulb** For more details on Pulumi and AWS integration, visit the [Pulumi Documentation](https://www.pulumi.com/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/pulumi-essentials/module/ea00d2be-be1c-4d36-8ac2-e76b0438de84/lesson/3dbe612a-a69c-4459-aeb1-43bc2219cb0d)


# Conclusion

Source: https://notes.kodekloud.com/docs/Pulumi-Essentials/Conclusion/Conclusion/page

This article discusses Pulumi's capabilities for managing infrastructure as code using familiar programming languages.

This article wraps up our discussion on Pulumi and its capabilities for managing infrastructure as code. Pulumi empowers you to leverage familiar programming languages like Python and JavaScript, providing you with access to extensive ecosystems, libraries, and tools. This approach not only simplifies the process of defining your infrastructure but also enhances your ability to manage it efficiently.

> **lightbulb** By using languages you already know, you can integrate full programming logic into your infrastructure management, enabling more robust and maintainable solutions.

We hope you found this exploration of Pulumi insightful and valuable. Stay tuned for our next lesson, where we'll dive deeper into advanced techniques and best practices for infrastructure management.\
See you in the next one!

- [Watch Video](https://learn.kodekloud.com/user/courses/pulumi-essentials/module/9d060695-e802-410a-9e74-9c7d18501300/lesson/21940ccd-338e-41a3-8cba-723c231a6ee1)
