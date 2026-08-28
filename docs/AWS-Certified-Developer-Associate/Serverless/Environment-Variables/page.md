# Environment Variables

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Serverless/Environment-Variables/page

This lesson explores how AWS Lambda functions utilize environment variables for managing sensitive information and configuration options securely.

In this lesson, we explore how [AWS Lambda](https://learn.kodekloud.com/user/courses/aws-lambda) functions utilize environment variables. These variables are essential for managing sensitive information such as database connection details, API keys, and other configuration options that you generally want to keep separate from your application code.

<Callout icon="lightbulb">
  Leveraging environment variables in your Lambda functions allows you to store potential secrets or configuration settings securely without embedding them directly into your code.
</Callout>

AWS Lambda supports the encryption of environment variables using AWS Key Management Service (KMS). This feature provides an added layer of security to ensure that your sensitive data remains confidential.

For more information on AWS Lambda security practices, refer to the [AWS Lambda Documentation](https://aws.amazon.com/lambda/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/3c842ffc-5841-456d-9fad-7bb3af5fdbfc/lesson/896e42af-6c36-45fa-a50c-361e58d1fe53" />
</CardGroup>
