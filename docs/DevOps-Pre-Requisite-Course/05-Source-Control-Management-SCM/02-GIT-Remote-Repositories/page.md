# Example output:
# ssh-rsa AAAAB3NzaC1yc...KhtUBfotzlBqRV1NThv0o4opzEwRq01lmWx user1
# ssh-rsa AAAXCVJSDFF...SLKJSDLKFw23423xckjSDFDLKJLSDFKJlX user2
```

## Securing HTTPS with a Combination of Asymmetric and Symmetric Encryption

Securing web server communications poses a challenge with symmetric encryption because the encryption key must be shared between the client and server, risking exposure to interception. Asymmetric encryption is used in combination with symmetric encryption to securely exchange keys.

The process operates as follows:

1. **Key Generation:**\
   The server creates an asymmetric key pair (private and public keys) using a tool like OpenSSL. For example:

   ```bash theme={null}
   openssl genrsa -out my-bank.key 1024
   openssl rsa -in my-bank.key -pubout > mybank.pem
   ```

2. **Certificate Exchange:**\
   When a user connects via HTTPS, the server sends its public key, usually embedded in a digital certificate, to the client. Even if intercepted, the public key cannot be used to decrypt the symmetric key encrypted by the client.

3. **Symmetric Key Exchange:**\
   The user's browser generates a symmetric key, encrypts it with the server's public key, and sends it back. The server then decrypts this message using its private key to retrieve the symmetric key. All subsequent communications are encrypted using this symmetric key.

This dual use of asymmetric and symmetric encryption ensures a secure key exchange and robust data protection.

## Preventing Impersonation with Digital Certificates

An attack vector to be aware of involves hackers creating fake websites to impersonate legitimate institutions like banks. An attacker can generate their own keys and a fake certificate to lure users into giving up sensitive credentials. To counteract this risk, servers send digital certificates during an HTTPS handshake. These certificates include the public key and vital identification information such as the domain name and issuer details.

Consider this example certificate snippet:

```text theme={null}
Certificate:
  Data:
    Serial Number: 420327018966204255
    Signature Algorithm: sha256WithRSAEncryption
    Issuer: CN=kubernetes
    Validity
      Not After : Feb  9 13:41:28 2020 GMT
    Subject: CN=my-bank.com
    X509v3 Subject Alternative Name:
      DNS:my-bank.com, DNS:i-bank.com, DNS:we-bank.com,
    Subject Public Key Info:
      00:b9:b0:55:24:fb:a4:ef:77:73:7c:9b
```

The "Subject" field is critical as it specifies the identity to which the certificate is issued. Additional fields like Subject Alternative Name allow flexibility if the website is accessible through multiple domain names.

> **triangle-alert** Browsers flag self-signed certificates, which are signed by their own creator, as untrustworthy. Always obtain a certificate from a trusted Certificate Authority (CA) to ensure browser compatibility and end-user security.

Browsers rely on built-in validation mechanisms that confirm a certificate is signed by a trusted CA. Certificates signed by recognized CAs such as Symantec, DigiCert, Comodo, or GlobalSign are automatically trusted because their public keys are pre-installed in browsers.

![The image illustrates online banking security, showing a certificate authority, a secure website, and a digital certificate for "my-bank.com."](https://kodekloud.com/kk-media/image/upload/v1752873515/notes-assets/images/DevOps-Pre-Requisite-Course-SSL-TLS-Basics/frame_840.jpg)

## Obtaining a Certificate from a Certificate Authority

To secure your web server with a trusted certificate, follow these steps:

1. **Generate a Certificate Signing Request (CSR):**\
   Use OpenSSL along with your private key and domain name:

   ```bash theme={null}
   openssl req -new -key my-bank.key -out my-bank.csr \
   -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=my-bank.com"
   ```

2. **Submit the CSR to a CA:**\
   After verification, the CA signs your certificate and returns it. The certificate is then trusted by web browsers as it can be validated using the CA's pre-installed public key.

## Summary of the SSL/TLS Process

| Step | Description                                      | Example/Command                                                                                       |
| ---- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| 1    | Secure SSH access using key pairs                | `ssh-keygen`                                                                                          |
| 2    | Configure servers with public keys               | Add key to `~/.ssh/authorized_keys`                                                                   |
| 3    | Generate CSR for HTTPS encryption                | `openssl req -new -key my-bank.key -out my-bank.csr -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=my-bank.com"` |
| 4    | Certificate issuance by trusted CA               | Certificate signed by CA                                                                              |
| 5    | Establish HTTPS session                          | Browser verifies certificate and encrypts symmetric key                                               |
| 6    | Ongoing communication secured with symmetric key | Secure symmetric encryption session                                                                   |

The process involves:

* Using key pairs to secure SSH and HTTPS.
* Generating a CSR and obtaining a trusted certificate.
* The browser verifying the certificate using the CA's public key.
* Exchanging a symmetric key for further communication encryption.

Client certificates are also available for authenticating users. In this approach, clients generate their own key pairs and receive a signed certificate from a trusted CA to securely authenticate to a server.

## A Note on Key Usage and Naming Conventions

Remember the simple analogy: a private key is kept secret like a personal key, while a public key is shared openly like a lock. Although both keys can encrypt data, only the corresponding opposite key can decrypt it. For example, encryption with your private key allows anyone with your public key to decrypt the message, which is why private keys must remain confidential.

Common file extensions help differentiate keys and certificates:

* Public key certificates often use extensions such as .crt or .pem (e.g., server.crt, server.pem).
* Private keys typically have extensions like .key or include “key” in the filename (e.g., server.key or server-dash-key.pem).

![The image illustrates the difference between public and private keys, showing file extensions and key representations for encryption purposes.](https://kodekloud.com/kk-media/image/upload/v1752873516/notes-assets/images/DevOps-Pre-Requisite-Course-SSL-TLS-Basics/frame_1180.jpg)

That concludes this lesson on SSL/TLS basics. By understanding the role of digital certificates, key pairs, and the underlying encryption techniques, you can establish secure communication channels for both SSH and HTTPS. Stay tuned for our next article where we'll dive deeper into advanced topics in secure communications.

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/078af284-cd5c-4557-81ee-73e680b8f300/lesson/a9b52f6d-c4e5-4440-9ec4-123d110efabc)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/078af284-cd5c-4557-81ee-73e680b8f300/lesson/8d1bb779-6950-45f3-95cb-53dbec22885d)


# GIT Remote Repositories

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Source-Control-Management-SCM/GIT-Remote-Repositories/page

This article explores remote Git repositories, their setup, and how they facilitate collaboration among developers.

In this lesson, we continue our discussion on Git by exploring remote repositories. Previously, we covered initializing a local Git repository—one that exists on your individual system. While each developer works on their own local repository containing specific parts of an application, collaborative development requires a centralized location where everyone can merge their changes. This centralized location is the remote Git repository.

Imagine you are updating the main file on your laptop, while Mark modifies the main and DB files, Aditi works on the cache file, and Lee enhances the back-end module. A remote Git repository, hosted either on your private network or over the internet, serves as the central hub where all these changes are pushed and merged.

![The image shows four local Git repositories on different laptops, each containing similar files for a project named "my-application."](https://kodekloud.com/kk-media/image/upload/v1752873518/notes-assets/images/DevOps-Pre-Requisite-Course-GIT-Remote-Repositories/frame_40.jpg)

The illustration above shows multiple developers working independently on their local repositories. When they're ready to integrate their updates, each developer pushes their changes to a shared remote repository.

![The image illustrates a Git workflow, showing multiple laptops pushing code to a remote Git repository containing various files like LICENSE, README.md, and Python scripts.](https://kodekloud.com/kk-media/image/upload/v1752873519/notes-assets/images/DevOps-Pre-Requisite-Course-GIT-Remote-Repositories/frame_80.jpg)

In this diagram, changes from different developers are pushed to a common remote repository. Git attempts to merge the changes automatically, but if two developers modify the same line in the same file, a merge conflict occurs.

> **triangle-alert** If you encounter a merge conflict, you'll need to resolve it manually before the changes can be successfully integrated.

After resolving conflicts and merging all changes, each developer can update their local repository by pulling the latest version, ensuring everyone works with the most current code.

![The image illustrates a Git workflow, showing multiple laptops pulling files from a remote Git repository containing project files like LICENSE, README.md, and Python scripts.](https://kodekloud.com/kk-media/image/upload/v1752873520/notes-assets/images/DevOps-Pre-Requisite-Course-GIT-Remote-Repositories/frame_120.jpg)

Remote repositories can be set up in various ways. One approach is to host your own Git server by installing Git on a designated system and running the built-in Git daemon. Alternatively, you can use publicly hosted services such as [GitHub](https://github.com) or [GitLab](https://gitlab.com), which offer both free public repositories and private repository options for internal use.

![The image illustrates a Git workflow, showing a remote repository with files being pulled to multiple laptops using GitHub and GitLab.](https://kodekloud.com/kk-media/image/upload/v1752873521/notes-assets/images/DevOps-Pre-Requisite-Course-GIT-Remote-Repositories/frame_160.jpg)

For example, when you create a repository on [GitHub](https://github.com), you can select whether to keep your repository public or private. Each repository on GitHub is assigned a unique URL that serves as the connection link for your local repository.

![The image shows a GitHub interface for creating a new repository named "my-application," with options for public or private visibility and initializing with a README.](https://kodekloud.com/kk-media/image/upload/v1752873522/notes-assets/images/DevOps-Pre-Requisite-Course-GIT-Remote-Repositories/frame_260.jpg)

## Setting Up and Pushing to a Remote Repository

If you're the primary developer with the application source code, follow these steps to turn your project into a Git repository:

```bash theme={null}
git init
git add .
git commit -m "Initial Commit"
```

Next, create a remote repository on [GitHub](https://github.com) using their web interface. Once created, copy its unique URL. Then, connect your local repository to the remote repository with the following command:

```bash theme={null}
git remote add github https://github.com/mmumshad/my-application.git
```

Finally, push your local changes to the remote repository. Since the remote branch doesn't yet exist, use the --set-upstream option to establish a connection between your local branch (by default, "master") and the remote branch:

```bash theme={null}
git push -u github master
```

> **lightbulb** Using descriptive names like "github" for your remote is especially useful when managing multiple remote repositories.

## Cloning and Pulling Updates

When another developer, such as Mark, joins the project, he can clone the remote repository to create a local copy:

```bash theme={null}
git clone https://github.com/mmumshad/my-application.git
```

Cloning downloads the entire repository and automatically configures a connection to the remote (named "origin" by default). As changes are made, developers can synchronize their local copy with the remote repository using the pull command:

```bash theme={null}
git pull
```

To view all the configured remotes, run:

```bash theme={null}
git remote -v
```

This command lists all the remote connections associated with your repository.

## Summary

In this lesson, we explored:

* The difference between local and remote Git repositories.
* How remote repositories enable effective collaboration among multiple developers.
* Setting up a remote repository on platforms like [GitHub](https://github.com) or [GitLab](https://gitlab.com).
* How to initialize a local repository and push changes to a remote server.
* Cloning repositories and pulling updates to ensure everyone works with the latest code.

Practice these steps to boost your version control skills. In upcoming lessons, you'll delve into end-to-end projects that demonstrate advanced Git workflows and effective multi-developer collaboration.

Thank you for joining this tutorial—happy coding!

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/c106a6e8-1fac-45a3-b1ae-48e996a5a9ff/lesson/da6d0d15-3d53-4db1-bd91-8d09317f5f13)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/c106a6e8-1fac-45a3-b1ae-48e996a5a9ff/lesson/553b3665-0f47-484f-b9e3-3edd2510338c)
