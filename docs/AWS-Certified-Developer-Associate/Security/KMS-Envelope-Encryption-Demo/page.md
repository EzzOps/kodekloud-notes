# -or-
PS C:\> dir HKCU:\Software\Python\PythonCore/<version>/InstallPath
```

Once Python is set up, install the AWS Encryption SDK CLI using pip:

```bash theme={null}
pip install aws-encryption-sdk-cli
pip install --upgrade aws-encryption-sdk-cli
aws-encryption-cli --version
```

This sequence installs the required tools and then displays the installed version of the AWS Encryption SDK CLI.

## Encryption Example

To encrypt a file, first export the ARN of your KMS key as an environment variable (e.g., `keyArn`). This step saves you from having to repeatedly enter the long ARN value in each command. In the following example, we assume that your demo key's ARN is stored in the `$keyArn` variable and you are encrypting a file named `db-creds`.

Copy and modify the command below:

```bash theme={null}
aws-encryption-cli --encrypt \
  --input db-creds \
  --wrapping-keys key=$keyArn \
  --metadata-output metadata \
  --encryption-context purpose=test \
  --commitment-policy require-encrypt-require-decrypt \
  --output output
```

Here's a breakdown of the command parameters:

* **--input db-creds**: Specifies the file to encrypt.
* \*\*--wrapping-keys key=$keyArn**: Uses your KMS key, identified by the ARN stored in `$keyArn\`, for key wrapping.
* **--metadata-output metadata**: Designates the location to store the encryption metadata.
* **--encryption-context purpose=test**: Applies an encryption context for validation during decryption.
* **--commitment-policy require-encrypt-require-decrypt**: Enforces strict commitment policies for both encryption and decryption.
* **--output output**: Specifies the folder for the encrypted data.

After executing this command, you should see two primary outputs: a metadata file in JSON format and an encrypted file containing binary data. For example, you can view the metadata file using the following command:

```bash theme={null}
cat metadata | jq
```

Below is an example of what the metadata JSON might look like:

```json theme={null}
{
  "header": {
    "algorithm": "AES_256_GCM_HKDF_SHA512_COMMIT_KEY_ECDSA_P384",
    "commitment_key": "JeK8VKo7y50+6z4y2Rpi2J3Px+ER7KMeb2B+4jCMDRk=",
    "content_type": 2,
    "encrypted_data_keys": [
      {
        "encrypted_data_key": "AQIBAhhIPn5jWlokyhTrOUNemva4jMiIw9RNFBBjMDPJwNggh3TTk7ntCDURimak35c55DA3bddPIqrk10Nbk6VeFp2m7P0R/xhRGrvE5MrjQ1BRZi0rI71Fn46TQpnYkunSduA==",
        "key_provider": {
          "key_info": "YXJuUmFzczprbk6XMtZWZcdxOjg0MTg2MDkyNzMzNzprZXkwNWU2Njk2YzUtZGU0Ni00ZDU2LWI=",
          "provider_id": "YxdzLWttcw=="
        }
      }
    ]
  },
  "encryption_context": {
    "aws-crypto-public": "A664LzkW6MAlgfbJ3BtD7Ic+fEyTscr4K9it0rHSZ0V22D3rI9d0Rs511PrB+E7w==",
    "purpose": "test"
  },
  "frame_length": 4096
}
```

<Callout icon="lightbulb">
  The metadata provides crucial details like the encryption algorithm, the encrypted data key, and the encryption context which are useful for auditing and troubleshooting.
</Callout>

## Decryption Example

Decrypting your data is a straightforward process. Ensure that you specify the same encryption context and KMS key ARN that were used during encryption. Use the following command to decrypt the file:

```bash theme={null}
aws-encryption-cli --decrypt \
  --input output \
  --wrapping-keys key=$keyArn \
  --commitment-policy require-encrypt-require-decrypt \
  --encryption-context purpose=test \
  --metadata-output metadata-decrypted \
  --max-encrypted-data-keys 1 \
  --buffer \
  --output decrypted-file
```

Here's an explanation of the extra decryption parameters:

* **--input output**: Points to the folder containing the encrypted data.
* **--metadata-output metadata-decrypted**: Specifies the location for the decryption metadata.
* **--max-encrypted-data-keys 1**: Ensures the message contains only one encrypted data key, reducing the risk of processing malformed messages.
* **--buffer**: Ensures decryption is complete before outputting the decrypted data, which is important for validating digital signatures.
* **--output decrypted-file**: Defines the name of the file where the decrypted data will be stored.

Upon running this command, you'll receive metadata output similar to the encryption process, along with a decrypted file containing your original data (e.g., credentials from the `db-creds` file).

## Summary

The AWS Encryption SDK CLI significantly streamlines the process of securing sensitive data through envelope encryption:

* It automates data key management so you don't have to manually generate, decode, or securely dispose of keys.
* A single command handles both encryption and decryption, simplifying your workflow.
* Detailed metadata files allow you to verify encryption parameters and support auditing processes.

By following the commands and best practices outlined in this guide, you can efficiently secure and access sensitive data using envelope encryption with the AWS Encryption SDK.

For more information and additional resources, consider visiting:

* [AWS Encryption SDK Documentation](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/)
* [AWS KMS Documentation](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/294fdab3-80dd-4183-aa7e-e5e3ffc9edd8/lesson/a670f11c-fac0-463d-84a7-d117b7651f15" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/294fdab3-80dd-4183-aa7e-e5e3ffc9edd8/lesson/ef35703c-fe57-400a-944b-f5db7310faab" />
</CardGroup>


# KMS Envelope Encryption Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Security/KMS-Envelope-Encryption-Demo/page

Learn to encrypt large files using AWS KMS envelope encryption, generating data keys for secure file handling and decryption.

In this lesson, you'll learn how to encrypt large files using AWS KMS envelope encryption. By leveraging envelope encryption, AWS KMS generates a data key from a primary KMS key that encrypts files of any size. Although we will use a sample file named "db-creds," the same steps apply to larger files.

## Generating a Data Key

A KMS key (for example, one named "demo") can directly encrypt or decrypt data up to 4 KB. To handle larger files, we generate a data key through our KMS key. This data key is provided in two forms:

* The plaintext key, used by OpenSSL for file encryption.
* The encrypted key, stored securely for later decryption.

To generate a data key, run the following command:

```bash theme={null}
aws kms generate-data-key --key-id alias/demo --key-spec AES_256
```

The command returns output similar to this:

```json theme={null}
{
  "CiphertextBlob": "AQIDAHhPIn5jWlOkyhcTrOUNemva4jMiIW9RNFBBMjDPJwngHbFmSd7rWYRpzC32pUfq/AAAAfjfERTNoj8WtmQvDnN+ahOOU/1CB9U8odPg+UoEfgjdRiwahNNYgki76w==",
  "Plaintext": "2gy7bq/apUh36hT39xYkEy+gHVA2yM2Y9RHM=",
  "KeyId": "arn:aws:us-east-1:841869029733:key/5e6696c5-de46-4d56-bb50-a9b71e187cad"
}
```

The returned plaintext key is base64 encoded. Save it to a file after decoding. Similarly, decode and store the encrypted key. For instance:

```bash theme={null}
echo '2gy7bp/qPhuH36NTR9xYKY+VHG+0VaM2Y9n/RHM=' | base64 -d > plaintext.key
```

```bash theme={null}
echo 'AQIdAHIpIn5jWLoKhyTrOUNemva4jMiIwi9NRFBMjMDPJwNgBHF5dr7wRhp3zC32pFuHlxZxUz80Qo/fERTNoj8wtmQvDnN+a+oOUb/1C9bU8odPG+uOefgXlDrwsGiahNNYgki76w==' | base64 -d > encrypted-key
```

This diagram from the AWS KMS console displays your customer-managed keys, including the "demo" key:

<Frame>
  ![The image shows the AWS Key Management Service (KMS) console, displaying a list of customer-managed keys with details such as aliases, key IDs, status, key type, and usage.](https://kodekloud.com/kk-media/image/upload/v1752859371/notes-assets/images/AWS-Certified-Developer-Associate-KMS-Envelope-Encryption-Demo/aws-kms-console-customer-keys.jpg)
</Frame>

## Encrypting Data

With your plaintext data key ready, use it to encrypt the "db-creds" file with OpenSSL. Execute the following command:

```bash theme={null}
openssl enc -e -aes256 -pass file:plaintext.key -in db-creds -pbkdf2 > encrypted-data
```

In this command:

* OpenSSL employs the AES-256 cipher.
* The encryption key is read from the provided plaintext key file.
* The `-pbkdf2` flag ensures a secure key derivation and prevents warnings.

For enhanced security, remove the plaintext key file after encryption:

```bash theme={null}
rm plaintext.key
```

<Callout icon="lightbulb">
  Removing the plaintext key from disk prevents it from being compromised, ensuring the security of your encrypted data.
</Callout>

## Decrypting Data

To decrypt the encrypted data file later, follow these steps:

1. **Decrypt the Encrypted Key Using AWS KMS**

   Run the command below to decrypt the stored encrypted key:

   ```bash theme={null}
   aws kms decrypt --ciphertext-blob fileb://encrypted-key
   ```

   The output will resemble:

   ```json theme={null}
   {
     "KeyId": "arn:aws:kms:us-east-1:841860927337:key/5e6696c5-de46-4d56-bb50-a9b71e187cad",
     "Plaintext": "2gyy7bp/qPhuH36N3T9xKY+VHG+0BVaM2Y9n/RHM=",
     "EncryptionAlgorithm": "SYMMETRIC_DEFAULT"
   }
   ```

2. **Store the Decrypted Plaintext Key**

   Decode the returned plaintext key and save it:

   ```bash theme={null}
   echo '2gyy7bp/qPhuH36N3T9xKY+VHG+0BVaM2Y9n/RHM=' | base64 -d > plaintext.key
   ```

3. **Decrypt the Data Using OpenSSL**

   Now decrypt the file with this command:

   ```bash theme={null}
   openssl enc -d -aes256 -pass file:plaintext.key -in encrypted-data -out decrypted-data -pbkdf2
   ```

   The `-d` flag indicates decryption. After executing this command, the file "decrypted-data" will match the original "db-creds" file.

## Final Notes

Envelope encryption requires you to store both the encrypted data and the corresponding encrypted data key. When decryption is necessary, AWS KMS can be used to extract the plaintext key from the encrypted key. Then, OpenSSL uses this plaintext key to restore your original data. This method ensures the data key is never stored in plaintext for an extended period, enhancing your overall security.

<Callout icon="lightbulb">
  By following this workflow, you effectively safeguard your sensitive data while leveraging the robust encryption capabilities offered by AWS KMS and OpenSSL.
</Callout>

That concludes our walkthrough on AWS KMS envelope encryption. Happy encrypting!

## Additional Resources

* [AWS Key Management Service Documentation](https://aws.amazon.com/kms/)
* [OpenSSL Documentation](https://www.openssl.org/docs/)
* [AWS Security Best Practices](https://aws.amazon.com/architecture/security-best-practices/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/294fdab3-80dd-4183-aa7e-e5e3ffc9edd8/lesson/5bcf280b-f1fc-4dd2-87b1-edb086c0a762" />
</CardGroup>
