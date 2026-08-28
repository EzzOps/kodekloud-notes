# AWS Migration and Transfer Demo

Source: https://notes.kodekloud.com/docs/AWS-Cloud-Practitioner-CLF-C02/Technology-Part-Two/AWS-Migration-and-Transfer-Demo/page

Learn to configure an AWS Transfer Family SFTP server using an Amazon S3 bucket for secure file transfers.

Welcome to this AWS Cloud Practitioners lesson. In this demonstration, you'll learn how to configure the AWS Transfer Family to set up an SFTP server using an Amazon S3 bucket as its backend. This tutorial focuses on SFTP (Secure File Transfer Protocol) rather than FTPS, FTP, or AS2, ensuring a secure file transfer process over SSH.

<Frame>
  ![The image is a webpage for AWS Transfer Family, highlighting secure, scalable file transfers and features like authentication, storage, user support, and security compliance.](https://kodekloud.com/kk-media/image/upload/v1752862268/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Migration-and-Transfer-Demo/frame_10.jpg)
</Frame>

## Step 1: Creating an SFTP Server

Begin by navigating to the AWS Transfer Family console. Even if there is an existing server, create a new server specifically for your SFTP configuration. When prompted, select **SFTP** and opt for the service-managed identity provider.

<Frame>
  ![The image shows an AWS interface for selecting an identity provider for SFTP, FTPS, or FTP, with options for service-managed, AWS Directory Service, or custom identity provider.](https://kodekloud.com/kk-media/image/upload/v1752862269/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Migration-and-Transfer-Demo/frame_50.jpg)
</Frame>

Ensure that the server is publicly accessible using default hostnames and choose Amazon S3 for backend storage instead of EFS. Create a new IAM role without any additional managed workflows, triggers, cryptographic modifications, or host key changes. A welcome message such as “Welcome to our SFTP server, KodeKloud” will be displayed on your server.

After reviewing your configuration, click **Next** followed by **Create**. The server status will initiate as "starting."

<Frame>
  ![The image shows an AWS Transfer Family dashboard with two servers listed, one starting and one online, with a notification about adding users.](https://kodekloud.com/kk-media/image/upload/v1752862270/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Migration-and-Transfer-Demo/frame_90.jpg)
</Frame>

## Step 2: Adding a User

While the server is starting, click into its details and then select **Add User**. Provide a username (for example, KodeKloud) and assign the appropriate IAM role (this can be an existing role such as an admin role). For the home directory, input a placeholder name like "KodeKloud", and then paste your public SSH key.

<Frame>
  ![The image shows an AWS interface for adding a user, with fields for username, role, policy, and home directory configuration.](https://kodekloud.com/kk-media/image/upload/v1752862271/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Migration-and-Transfer-Demo/frame_110.jpg)
</Frame>

### Retrieving Your Public SSH Key

Open Visual Studio Code (or your preferred terminal) to retrieve your public SSH key from the file ending in `.pub`:

```bash theme={null}
$ cat ~/.ssh/id_ed25519.pub
```

Your public key will look similar to this:

```bash theme={null}
ssh-ed25519 [SECRET_REDACTED] michaelirishforrester@gmail.com
```

<Callout icon="lightbulb">
  The public SSH key is safe to share with servers and is essential for establishing a secure connection.
</Callout>

After entering the user information and pasting the public key, click **Add** in the AWS console to complete the user creation. Once finished, you'll see the username (e.g., KodeKloud) along with the SFTP endpoint. Copy this endpoint for later use and keep checking the server status until it changes from "starting" to "online."

## Step 3: Connecting from the Client Side

When your SFTP server status is online, you can connect using the SFTP command. Ensure you are using the correct private key corresponding to the public key you added earlier. For example:

```bash theme={null}
$ sftp -i ~/.ssh/id_ed25519 kodekloud@5-48d1d2f1ce04455b.server.transfer.us-east-2.amazonaws.com
```

<Callout icon="triangle-alert">
  If you attempt connecting before the server status is online, the connection may fail. Please refresh the server details and wait for a status update.
</Callout>

Verify that the endpoint in your terminal matches the one provided by AWS in the console. Once confirmed, execute the final SFTP command:

```bash theme={null}
$ sftp -i ~/.ssh/id_ed25519 kodekloud@g-4d81d12f1ce04455b.server.transfer.us-east-2.amazonaws.com
```

After a successful connection, you will be presented with your home directory and a welcome message similar to the following:

```bash theme={null}
$ sftp -i ~/.ssh/id_ed25519 kodekloud@s-48d1d12f1ce004455b.server.transfer.us-east-2.amazonaws.com
Welcome to our SFTP Server, KodeKloud
Connected to s-48d1d12f1ce004455b.server.transfer.us-east-2.amazonaws.com.
sftp>
```

<Frame>
  ![The image shows an AWS Transfer Family server dashboard, displaying server details like protocols, endpoint status, identity provider, and user management options.](https://kodekloud.com/kk-media/image/upload/v1752862272/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-AWS-Migration-and-Transfer-Demo/frame_240.jpg)
</Frame>

## Conclusion

This demonstration confirms that your AWS Transfer Family SFTP server is configured correctly. You can now perform various file transfer operations such as uploading files, listing directories, and more.

Thank you for following this AWS Migration and Transfer demo. For further details on secure file transfers with AWS, refer to the [AWS Transfer Family Documentation](https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html). We look forward to sharing more lessons in our upcoming articles.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-practitioner-clf-c02/module/f47a1e6e-5593-4fac-bc8b-f24ef6e6f418/lesson/7e5861b1-4b71-4470-9484-a54fade26709" />
</CardGroup>
