# Demo Password management with Amazon RDS and AWS Secrets Manager Part 2

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Networking-and-Security/Demo-Password-management-with-Amazon-RDS-and-AWS-Secrets-Manager-Part-2/page

Guide to storing and rotating Amazon RDS master credentials using AWS Secrets Manager, including setup, verification, rotation effects, application retrieval, IAM and deletion considerations.

Welcome back. In the previous lesson we stored an RDS username and password manually in AWS Secrets Manager. In this lesson we'll enable the RDS option that stores and manages the DB master credentials directly in AWS Secrets Manager at database creation time.

Note: this integration is not available for all RDS engines and deployment types — check the AWS documentation for engine/version support and limitations:

* [https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY].SecretsManager.html](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY].SecretsManager.html)

## Quick overview

* Enable "Manage master credentials in AWS Secrets Manager" when creating the RDS instance.
* RDS will create a Secrets Manager secret with the generated master username and password.
* Secrets Manager can optionally enable automatic rotation for that secret and (when configured) will update the RDS master password.
* Your application must fetch the current credentials from Secrets Manager (or use a secure cache) so it continues to work after rotation.

## Create the database and enable Secrets Manager

1. Open the RDS console and click Create database.

<Frame>
  <img alt="A screenshot of the Amazon Web Services RDS console dashboard showing resource usage, quotas, and links. The main pane includes a prominent &#x22;Create database&#x22; button while the left sidebar lists RDS navigation items." />
</Frame>

2. Choose Standard create and select PostgreSQL as the engine. Keep defaults where appropriate and pick a Free tier instance class (or another instance class you prefer).

3. In the Credentials section enable Manage master credentials in AWS Secrets Manager. When enabled, RDS will generate and store the master username and password in Secrets Manager and can optionally enable rotation for that secret.

<Frame>
  <img alt="A screenshot of the AWS RDS console during DB instance setup. It shows credentials settings (master username &#x22;postgres&#x22; with the option to manage credentials in AWS Secrets Manager), encryption key selection, and the instance class set to db.t3.micro." />
</Frame>

4. Scroll through the remaining settings, adjust networking/security as required (VPC, subnets, security groups), and click Create database.

Database provisioning typically takes \~10–15 minutes. Wait until the DB status shows Available.

## Verify the secret created by RDS

Once the DB is available, choose View details. You will see the master username and an indication that the master credentials are managed by AWS Secrets Manager. RDS creates the corresponding secret in Secrets Manager during DB creation.

<Frame>
  <img alt="A screenshot of an AWS RDS console dialog titled &#x22;Connection details to your database database-1.&#x22; It shows the master username &#x22;postgres,&#x22; the database endpoint, and links to manage credentials and learn how to connect." />
</Frame>

Click Manage credentials to open the secret in AWS Secrets Manager. The secret contains metadata (tags, ARN, name) that your application will reference. Scroll down to view the secret value and click Retrieve secret value to reveal the stored username and password.

Because of IAM permissions, a regular user might not have permission to retrieve the secret value. In this demo the account has administrative privileges and can view the secret.

<Frame>
  <img alt="A screenshot of the AWS Secrets Manager console showing a secret with key/value entries (username: postgres and a password) and a rotation configuration set to 7 days. The page also shows sections for resource permissions and sample code." />
</Frame>

## Sample code — retrieve the secret and connect to PostgreSQL

Below are code examples provided by Secrets Manager that demonstrate retrieving the secret (username/password) and using it to connect to PostgreSQL.

Java (AWS SDK v2) — retrieve the secret value

```java theme={null}
// Java (AWS SDK v2) example: get a secret value from AWS Secrets Manager
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.secretsmanager.SecretsManagerClient;
import software.amazon.awssdk.services.secretsmanager.model.GetSecretValueRequest;
import software.amazon.awssdk.services.secretsmanager.model.GetSecretValueResponse;
import software.amazon.awssdk.services.secretsmanager.model.SecretsManagerException;

public class SecretsExample {
    public static void getSecret() {
        String secretName = "rds!db-8fcc3794-ab80-4353-86fb-641f99a65793";
        Region region = Region.of("eu-central-1");

        try (SecretsManagerClient client = SecretsManagerClient.builder()
                .region(region)
                .build()) {

            GetSecretValueRequest getSecretValueRequest = GetSecretValueRequest.builder()
                    .secretId(secretName)
                    .build();

            GetSecretValueResponse getSecretValueResponse = client.getSecretValue(getSecretValueRequest);
            String secretString = getSecretValueResponse.secretString();
            System.out.println("Secret: " + secretString);
            // secretString typically contains a JSON with username, password, host, port, dbname
        } catch (SecretsManagerException e) {
            System.err.println("Secrets Manager error: " + e.awsErrorDetails().errorMessage());
            throw e;
        }
    }
}
```

Python (boto3) — retrieve the secret, parse it, and connect to PostgreSQL

```python theme={null}
