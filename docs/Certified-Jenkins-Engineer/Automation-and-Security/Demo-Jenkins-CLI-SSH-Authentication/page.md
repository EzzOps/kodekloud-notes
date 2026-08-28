# Demo Jenkins CLI SSH Authentication

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Automation-and-Security/Demo-Jenkins-CLI-SSH-Authentication/page

This guide explains how to configure Jenkins for SSH key-based authentication for its CLI, enhancing security and integration with existing SSH infrastructure.

In this guide, you’ll learn how to configure Jenkins to use SSH key–based authentication for its CLI, replacing the default HTTP basic auth. This approach is more secure and integrates seamlessly with your existing SSH infrastructure.

## Prerequisites

| Requirement       | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| Jenkins server    | Running on `http://localhost:8080`                         |
| SSH client        | Installed on your local machine                            |
| `jenkins-cli.jar` | Downloaded from your Jenkins server (Manage → Jenkins CLI) |

## 1. Discovering the Jenkins SSH Endpoint

Jenkins exposes its CLI over SSH on a configurable port. To find the SSH endpoint before enabling it, query the `/login` endpoint:

```bash theme={null}
curl -Lv http://localhost:8080/login 2>&1 | grep -i 'x-ssh-endpoint'
```

<Callout icon="lightbulb">
  By default, the SSH server is disabled in Jenkins, so you won’t see the `X-SSH-Endpoint` header until it’s enabled.
</Callout>

<Frame>
  ![The image shows a terminal window displaying HTTP response headers and HTML code, likely from a web server or application. The environment appears to be a code editor with a dark theme.](https://kodekloud.com/kk-media/image/upload/v1752870389/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-CLI-SSH-Authentication/http-response-headers-html-code.jpg)
</Frame>

## 2. Enabling the Jenkins SSH Server

1. In Jenkins, go to **Manage Jenkins** → **Configure Global Security**.
2. Locate the **SSH Server** section and enable the SSH port. You can select **Random** or enter a fixed port (e.g., `2222`).
3. Click **Apply** to save changes.

<Callout icon="triangle-alert">
  If you choose a fixed port, make sure it’s open in your firewall and not in use by another service.
</Callout>

<Frame>
  ![The image shows a Jenkins security configuration page with options for API token settings and SSH server configurations. The "Enable API Token usage statistics" option is checked, and the SSH port is set to "Random."](https://kodekloud.com/kk-media/image/upload/v1752870390/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-CLI-SSH-Authentication/jenkins-security-configuration-api-ssh.jpg)
</Frame>

After applying, rerun the `curl` command:

```bash theme={null}
curl -Lv http://localhost:8080/login 2>&1 | grep -i 'x-ssh-endpoint'
```

You should now see output similar to:

```text theme={null}
< X-SSH-Endpoint: localhost:4397
```

The SSH server is listening on port **4397**.

## 3. Generating and Registering Your SSH Key

### 3.1 Generate an SSH Key Pair

If you don’t already have an SSH key, generate one:

```bash theme={null}
ssh-keygen -t rsa -b 4096
```

Press **Enter** to accept the default file location (`~/.ssh/id_rsa`) and leave the passphrase empty if you prefer. Then display your public key:

```bash theme={null}
cat ~/.ssh/id_rsa.pub
