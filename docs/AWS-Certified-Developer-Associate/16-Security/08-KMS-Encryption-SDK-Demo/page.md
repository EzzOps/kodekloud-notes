# Encrypt the data
aws kms encrypt --key-id alias/demo --plaintext fileb://db-credentials --output text --query CiphertextBlob > encrypted-db-credentials

# Decode the encrypted file to obtain pure binary data
cat encrypted-db-credentials | base64 -di > encrypted-db-credentials-decoded

# Decrypt the binary data
aws kms decrypt --ciphertext-blob fileb://encrypted-db-credentials-decoded --output text --query Plaintext > decrypted-file

# Decode the decrypted data to retrieve the original text
cat decrypted-file | base64 -d > decrypted-and-decoded-file
```

## Conclusion

In this guide, we've explored how to view AWS managed keys, create a customer-managed key, and utilize the AWS CLI to encrypt and decrypt data. This process ensures that you can securely manage and use cryptographic keys with AWS KMS while maintaining granular control over key administration and usage permissions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/294fdab3-80dd-4183-aa7e-e5e3ffc9edd8/lesson/53e303d9-104d-4a11-9d3e-25f020eed95c" />
</CardGroup>


# KMS Encryption SDK Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Security/KMS-Encryption-SDK-Demo/page

This article explains how to use the AWS Encryption SDK for simplified envelope encryption and decryption of large files.

In this article, we will explore how to simplify envelope encryption using the AWS Encryption SDK. Previously, manually performing envelope encryption was a tedious process that involved generating and decoding data keys, encrypting files, and securely deleting plaintext keys to prevent accidental exposure. The AWS Encryption SDK streamlines these steps, making it much easier to encrypt and decrypt large files.

Before you begin, ensure that Python is installed on your system. Verify your Python installation with the following command:

```bash theme={null}
python -V
PS C:\> dir HKLM:\Software\Python\PythonCore/<version>/InstallPath
