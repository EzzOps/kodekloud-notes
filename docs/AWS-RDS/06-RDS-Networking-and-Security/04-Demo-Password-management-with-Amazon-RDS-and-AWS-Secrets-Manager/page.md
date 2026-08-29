# Python example: get secret from AWS Secrets Manager and connect to PostgreSQL
import json
import boto3
from botocore.exceptions import ClientError
import psycopg2

def get_secret(secret_name: str, region_name: str) -> dict:
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions see:
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # SecretString contains the JSON with username/password/host/etc.
    secret_string = get_secret_value_response.get("SecretString")
    if secret_string:
        return json.loads(secret_string)
    else:
        # In some cases the secret may be stored as binary
        secret_binary = get_secret_value_response.get("SecretBinary")
        return json.loads(secret_binary.decode("utf-8"))

def connect_with_secret(secret_info: dict):
    conn = psycopg2.connect(
        host=secret_info.get("host"),
        port=secret_info.get("port", 5432),
        database=secret_info.get("dbname"),
        user=secret_info.get("username"),
        password=secret_info.get("password")
    )
    return conn

if __name__ == "__main__":
    secret_name = "rds!db-8fcc3794-ab80-4353-86fb-641f99a65793"
    region = "eu-central-1"
    secret = get_secret(secret_name, region)
    conn = connect_with_secret(secret)
    print("Connected to DB as", secret.get("username"))
    conn.close()
```

## Rotation behavior and application impact

When rotation is enabled, Secrets Manager updates the stored password and (if rotation is configured correctly) updates RDS with the new password. Your application must use the current credentials from Secrets Manager; otherwise, a rotated password will break connections.

<Callout icon="lightbulb">
  Make sure your application either fetches the secret on each connection, refreshes at a safe cadence, or uses an in-process Secrets Manager cache/library that automatically refreshes. Also ensure IAM policies grant only the minimum required permissions to retrieve the secret and that the application has network access to the RDS endpoint (VPC, subnets, and security groups configured correctly).
</Callout>

## What happens to the secret when you delete the RDS instance?

By default, RDS can delete the Secrets Manager secret it created as part of the DB deletion process. This behavior depends on the deletion options you choose and the IAM permissions in your account, so confirm the settings when deleting a DB.

<Callout icon="warning">
  If you need to retain the secret after deleting the DB, explicitly update the secret's configuration or back it up before deleting the RDS instance — otherwise you may permanently lose the credentials needed for recovery.
</Callout>

## Quick checklist

| Action                                              | Why it matters                                                                   | Notes                                                          |
| --------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Enable Manage master credentials in Secrets Manager | Stores and optionally rotates DB master credentials                              | Only available for supported engines/versions — check AWS docs |
| Verify IAM permissions                              | Limit who can read secrets and update rotation                                   | Use least-privilege roles for applications and admins          |
| Configure rotation and rotation role                | Automates password changes and updates RDS                                       | Test rotation in a staging environment first                   |
| Ensure network access                               | Application must reach both Secrets Manager (for API calls) and the RDS endpoint | VPC endpoints, security groups, and routing matter             |

## Summary

* Enabling "Manage master credentials in AWS Secrets Manager" at RDS creation stores the DB master credentials in Secrets Manager and can enable automatic rotation.
* Ensure your application retrieves the current credentials from Secrets Manager (or uses a secure caching mechanism) to handle rotated passwords.
* Validate IAM permissions and network configuration so your application can retrieve secrets and connect to the RDS instance.
* Confirm deletion/retention behavior for secrets before deleting databases.

## Links and references

* AWS RDS + Secrets Manager integration: [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SecretsManager.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SecretsManager.html)
* Secrets Manager GetSecretValue API: [https://docs.aws.amazon.com/secretsmanager/latest/apireference/API\_GetSecretValue.html](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html)
* boto3 Secrets Manager client: [https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html)
* AWS SDK for Java v2: [https://sdk.amazonaws.com/java/api/latest/index.html](https://sdk.amazonaws.com/java/api/latest/index.html)
* psycopg2 PostgreSQL adapter: [https://www.psycopg.org/](https://www.psycopg.org/)

I hope this lesson clarified how to integrate Amazon RDS with AWS Secrets Manager for automated credential management.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/12fd8771-ab60-4e87-8f8b-67fe9507bb76/lesson/b34cdfab-5fb2-49f7-981b-17b786f03c21" />
</CardGroup>


# Demo Password management with Amazon RDS and AWS Secrets Manager

Source: https://notes.kodekloud.com/docs/AWS-RDS/RDS-Networking-and-Security/Demo-Password-management-with-Amazon-RDS-and-AWS-Secrets-Manager/page

Provisioning an Amazon RDS MariaDB instance, capturing its auto-generated master password, and securely storing and retrieving credentials using AWS Secrets Manager for applications

In this lesson you'll provision an Amazon RDS (MariaDB) instance, capture the auto-generated master password shown during creation, and securely store that credential in AWS Secrets Manager so your applications can retrieve it at runtime. This pattern reduces secrets sprawl, enables automatic rotation, and follows least-privilege and auditable access to database credentials.

What you will do

* Create an RDS (MariaDB) instance and let RDS auto-generate a strong master password.
* Retrieve the generated password from the RDS creation banner (the password is displayed only once).
* Store the username/password pair in AWS Secrets Manager and link the secret to the RDS instance.
* Use example client code (Python and Java) that reads the secret before creating DB connections.

Create the RDS instance

1. Open the AWS Management Console and navigate to [Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html).
2. Choose "DB instances" → "Create DB instance".
3. For this demo select MariaDB and choose the Free tier (if eligible).
4. Provide a DB instance identifier (for example, my-application) and a master username (for example, admin).
5. Click "Auto-generate a password" to have RDS create a strong master password. Leave other defaults as appropriate for your environment.
6. Click "Create database".

<Frame>
  <img alt="A screenshot of the AWS RDS Create database page configuring a MariaDB instance, showing DB instance size options (Production, Dev/Test, Free tier), a DB identifier &#x22;my-application&#x22; and master username &#x22;admin.&#x22; The right panel displays MariaDB details and there's a &#x22;Create database&#x22; button at the bottom." />
</Frame>

Wait for the database to finish provisioning (typically 10–15 minutes). When creation completes, the RDS console displays a banner with connection details including the master username and the auto-generated master password. Click "View connection details" and copy the master password to a secure temporary location so you can store it in Secrets Manager.

<Callout icon="warning">
  The auto-generated master password is shown only once in the RDS creation banner. If you close the banner without saving it elsewhere, the password cannot be retrieved — you would need to reset the master password.
</Callout>

<Frame>
  <img alt="A screenshot of the AWS RDS web console showing a pop-up titled &#x22;Connection details to your database my-application.&#x22; It displays the master username (admin), a generated master password, and the database endpoint with copy/close options." />
</Frame>

Store the credential in AWS Secrets Manager

1. In the AWS Console search bar open [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html).
2. Click "Store a new secret".
3. Choose the secret type: "Credentials for RDS database".
4. Enter the DB username (admin) and paste the master password you copied from the RDS banner.
5. Keep the KMS encryption key as the default (aws/secretsmanager) unless you require a custom KMS key.
6. Secrets Manager will list RDS instances available in the account/region — select the RDS instance you created (for example, my-application).
7. Click "Next".
8. Provide a secret name (for example, application-01-secret) and an optional description.
9. Configure cross-region replication only if you need it; otherwise continue with "Next".
10. Click "Store" to persist the secret into Secrets Manager.

<Frame>
  <img alt="A screenshot of the AWS Secrets Manager &#x22;New secret&#x22; page configured for Amazon RDS credentials, showing the username &#x22;admin&#x22;, a masked password field, and the KMS encryption key set to &#x22;aws/secretsmanager.&#x22; The Database section lists an RDS instance named &#x22;my-application&#x22; (mariadb) with status &#x22;available.&#x22;" />
</Frame>

After storing the secret you will see it listed in the Secrets Manager console (for example, application-01-secret). The stored secret contains the master username and password associated with your RDS instance.

<Frame>
  <img alt="A screenshot of the AWS Secrets Manager console showing a single secret named &#x22;application-01-secret.&#x22; The secret's description says it contains the master username and password for the RDS instance &#x22;my-application.&#x22;" />
</Frame>

Using Secrets Manager from your application
Best practice: retrieve the secret at application startup (or immediately before creating database connections) so the application uses credentials returned by [Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html) instead of hard-coded values. The AWS console includes snippets for many languages; below are ready-to-use examples for Python (boto3) and Java (AWS SDK v2).

Python (boto3)

* Install boto3: pip install boto3
* Ensure the application's IAM role or IAM user has permission to call GetSecretValue: [https://docs.aws.amazon.com/secretsmanager/latest/apireference/API\_GetSecretValue.html](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html)

```python theme={null}
import json
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name: str, region_name: str) -> dict:
    """
    Retrieve a secret from AWS Secrets Manager and return it as a dict.
    If the secret's SecretString contains JSON, this returns the parsed JSON.
    Otherwise returns {"secret": <SecretString>} or {"secretBinary": <bytes>}.

    Example secret JSON for RDS:
      {"username": "admin", "password": "generated-password", "host": "...", "port": 3306}
    """
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # Propagate or handle specific errors as required by your app
        raise e

    # SecretString contains a string; SecretBinary contains bytes if used.
    if "SecretString" in response and response["SecretString"]:
        secret_string = response["SecretString"]
        try:
            return json.loads(secret_string)
        except json.JSONDecodeError:
            return {"secret": secret_string}
    else:
        # SecretBinary is base64-encoded bytes
        return {"secretBinary": response.get("SecretBinary")}
```

Java (AWS SDK v2)

* Ensure your build includes the AWS SDK v2 Secrets Manager module and that the app's IAM identity has GetSecretValue permission.
* The method below returns the secret string; if it contains JSON, parse it into an object using your JSON library of choice.

```java theme={null}
// import software.amazon.awssdk.regions.Region;
// import software.amazon.awssdk.services.secretsmanager.SecretsManagerClient;
// import software.amazon.awssdk.services.secretsmanager.model.GetSecretValueRequest;
// import software.amazon.awssdk.services.secretsmanager.model.GetSecretValueResponse;
// import software.amazon.awssdk.services.secretsmanager.model.SecretsManagerException;

public static String getSecret(String secretName, String region) {
    Region awsRegion = Region.of(region);
    try (SecretsManagerClient client = SecretsManagerClient.builder()
            .region(awsRegion)
            .build()) {

        GetSecretValueRequest getSecretValueRequest = GetSecretValueRequest.builder()
                .secretId(secretName)
                .build();

        GetSecretValueResponse getSecretValueResponse = client.getSecretValue(getSecretValueRequest);

        if (getSecretValueResponse.secretString() != null) {
            return getSecretValueResponse.secretString();
        } else {
            // If secret is in binary form, handle it accordingly
            return getSecretValueResponse.secretBinary().asUtf8String();
        }
    } catch (SecretsManagerException e) {
        throw e;
    }
}
```

Integration and operational notes

| Topic              | Recommendation                                                                                                        | Reference                                                                                                                                                                                                                                                                                                                        |
| ------------------ | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Retrieval timing   | Fetch secrets at startup or immediately before DB connections to avoid long-lived secrets in memory                   | [https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)                                                                                                                                                                                 |
| Permissions        | Grant minimal IAM permissions (GetSecretValue) to the application role; include kms:Decrypt if using a custom KMS key | [https://docs.aws.amazon.com/secretsmanager/latest/apireference/API\_GetSecretValue.html](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html) and [https://docs.aws.amazon.com/kms/latest/developerguide/overview.html](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) |
| Automatic rotation | Enable Secrets Manager rotation for supported engines to rotate and update DB credentials automatically               | [https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)                                                                                                                                                           |
| Secret format      | Store RDS secrets as JSON (username, password, host, port) to simplify parsing in apps                                | Console samples and SDK examples                                                                                                                                                                                                                                                                                                 |

<Callout icon="lightbulb">
  AWS provides sample snippets for many languages in the [Secrets Manager console](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html). Use those samples as a starting point and adapt them to your application's error handling, caching, and refresh strategy.
</Callout>

Additional resources

* [Amazon RDS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
* [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
* [Secrets Manager API - GetSecretValue](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html)
* [Secrets rotation with AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
* [AWS KMS overview](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)

Summary

* You provisioned a MariaDB instance in RDS and used the auto-generated master password.
* The auto-generated password is visible only once during creation; copy it immediately or store it in Secrets Manager.
* You stored the credential in AWS Secrets Manager and learned how to retrieve it from Python and Java applications, enabling secure, auditable access to DB credentials.
* Consider enabling automatic rotation and apply least-privilege IAM policies for production deployments.

That is it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/12fd8771-ab60-4e87-8f8b-67fe9507bb76/lesson/1ac41a31-a067-48b9-bae5-a9d9bbbd17df" />
</CardGroup>
