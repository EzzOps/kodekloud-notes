# ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC... root@host
```

### 3.2 Add Your Public Key in Jenkins

1. Click your Jenkins user name (e.g., **siddharth**) → **Configure**.
2. Scroll to the **SSH Public Keys** section.
3. Paste the contents of `~/.ssh/id_rsa.pub` into the text box.
4. Click **Apply**.

<Frame>
  ![The image shows a Jenkins security configuration page with options for authentication and authorization, listing users and groups with roles.](https://kodekloud.com/kk-media/image/upload/v1752870391/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-CLI-SSH-Authentication/jenkins-security-configuration-authentication-authorization.jpg)
</Frame>

<Frame>
  ![The image shows a configuration page from a Jenkins user interface, featuring fields for default view, notification URL, SSH public keys, and session termination options.](https://kodekloud.com/kk-media/image/upload/v1752870392/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-CLI-SSH-Authentication/jenkins-configuration-page-settings.jpg)
</Frame>

## 4. Connecting to Jenkins via SSH

Now that your public key is registered, connect to Jenkins over SSH and run CLI commands. Replace `4397` with the port reported by `X-SSH-Endpoint`:

```bash theme={null}
ssh -l siddharth -p 4397 localhost help
```

Sample output:

```text theme={null}
add-job-to-view    Adds jobs to view.
build              Builds a job, and optionally waits until completion.
cancel-quiet-down  Cancel the effect of the "quiet-down" command.
clear-queue        Clears the build queue.
...
```

## 5. Using SSH Mode with the Jenkins CLI JAR

You can also invoke SSH mode directly via `jenkins-cli.jar`. For full details, see the [Jenkins CLI documentation][jenkins-cli-docs].

<Frame>
  ![The image shows a webpage from the Jenkins documentation, specifically about the Jenkins CLI (Command Line Interface). It includes navigation links on the left and a table of contents on the right.](https://kodekloud.com/kk-media/image/upload/v1752870394/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-CLI-SSH-Authentication/jenkins-cli-documentation-webpage.jpg)
</Frame>

Example—list jobs over SSH:

```bash theme={null}
java -jar jenkins-cli.jar \
  -s http://localhost:8080 \
  -ssh -user siddharth \
  list-jobs
```

Expected output:

```text theme={null}
ascii-build-job
ascii-deploy-job
ascii-test-job
d-v-s-pipeline
Dasher_testJob
...
```

This confirms that authentication is performed via your SSH key pair instead of HTTP basic auth.

## Authentication Methods Comparison

| Method          | Port/Protocol | Complexity |
| --------------- | ------------- | ---------- |
| HTTP Basic Auth | 8080 (HTTP)   | Minimal    |
| SSH Key Auth    | Custom (SSH)  | Moderate   |

## References

* [Jenkins CLI documentation][jenkins-cli-docs]
* [Generating SSH Keys][ssh-keygen-docs]
* [Jenkins Security Concepts][jenkins-security-docs]

[jenkins-cli-docs]: https://www.jenkins.io/doc/book/managing/cli/

[ssh-keygen-docs]: https://www.ssh.com/academy/ssh/keygen

[jenkins-security-docs]: https://www.jenkins.io/doc/book/system-administration/security/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/4d6d1f39-307c-4fdb-8d2b-834c1650e792/lesson/ca011583-8662-41a9-8123-b4ed93693d21" />
</CardGroup>


# Demo Jenkins CSRF CRUMB

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Automation-and-Security/Demo-Jenkins-CSRF-CRUMB/page

This guide explains generating and using Jenkins CSRF crumb tokens to secure HTTP requests against Cross-Site Request Forgery attacks.

In this guide, we’ll walk through generating and using Jenkins CSRF crumb tokens to secure HTTP requests against Cross-Site Request Forgery attacks. You’ll learn how to configure Jenkins for CSRF protection, retrieve crumb tokens via the REST API, and trigger jobs with the proper headers and cookies.

## Jenkins CSRF Protection Configuration

By default, Jenkins enforces CSRF protection. As an administrator:

1. Go to **Manage Jenkins** → **Configure Global Security**.
2. Locate the **CSRF Protection** section and confirm it is enabled.

<Frame>
  ![The image shows a webpage from the Jenkins documentation, specifically focusing on configuring CSRF protection. It includes navigation links on the left and details about the "Crumb Issuer" settings on the right.](https://kodekloud.com/kk-media/image/upload/v1752870395/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-CSRF-CRUMB/jenkins-csrf-protection-configuration.jpg)
</Frame>

<Callout icon="triangle-alert">
  Disabling CSRF protection is **not recommended** in production. If you must disable it (for testing only), set the system property

  ```text theme={null}
  hudson.security.csrf.GlobalCrumbIssuerConfiguration.DISABLE_CSRF_PROTECTION=true
  ```

  at server startup.
</Callout>

## Default Crumb Issuer

Jenkins’s **Default Crumb Issuer** generates a token hash from several session-specific values. All must match when validating an incoming request:

| Encoded Value   | Description                               |
| --------------- | ----------------------------------------- |
| Username        | The authenticated user’s login            |
| Session ID      | Unique identifier for the Jenkins session |
| User IP Address | Client’s source IP                        |
| Instance Salt   | A secret salt unique to this Jenkins node |

<Frame>
  ![The image shows a Jenkins security configuration page with options for CSRF protection, artifact compatibility mode, and Git plugin access tokens.](https://kodekloud.com/kk-media/image/upload/v1752870396/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-CSRF-CRUMB/jenkins-security-configuration-csrf-git-tokens.jpg)
</Frame>

## Working with the Crumb Issuer API

The crumb is exposed at the REST endpoint `/crumbIssuer/api/json`. Authenticate with username/password or API token to receive:

* A JSON payload containing the crumb and header field name
* A session cookie to include on subsequent requests

<Frame>
  ![The image shows a webpage from the Jenkins documentation, specifically focusing on CSRF protection. It includes a navigation menu on the left and detailed information about working with scripted clients and disabling CSRF protection on the right.](https://kodekloud.com/kk-media/image/upload/v1752870398/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-CSRF-CRUMB/jenkins-csrf-protection-documentation.jpg)
</Frame>

### 1. Generate and View the Crumb

```bash theme={null}
curl -s \
  -u admin:password \
  http://localhost:8080/crumbIssuer/api/json | jq
```

```json theme={null}
{
  "_class": "hudson.security.csrf.DefaultCrumbIssuer",
  "crumb": "628e6eb7b759cb388daec3a44de4e1fcde5da95edcbd779d8b9967c1239de5cff",
  "crumbRequestField": "Jenkins-Crumb"
}
```

### 2. Inspect Response Headers

View the `Set-Cookie` header to capture the session ID:

```bash theme={null}
curl -s -v \
  -u admin:password \
  http://localhost:8080/crumbIssuer/api/json > /dev/null
```

Example header output:

```text theme={null}
Set-Cookie: JSESSIONID.<...>=node01ylzmgr6pjx...; Path=/; HttpOnly
```

### 3. Store Cookies with a Cookie Jar

Save the session cookie for later use:

```bash theme={null}
curl -s \
  -u admin:password \
  --cookie-jar /tmp/jenkins_cookies \
  http://localhost:8080/crumbIssuer/api/json | jq
```

```json theme={null}
{
  "_class": "hudson.security.csrf.DefaultCrumbIssuer",
  "crumb": "28791665a0a7f47ecf03510ae3b0b2695e01d3e3f2d0ba96d1d230898051059a",
  "crumbRequestField": "Jenkins-Crumb"
}
```

Verify the stored cookie:

```bash theme={null}
cat /tmp/jenkins_cookies
```

<Callout icon="lightbulb">
  Using `--cookie-jar` ensures your session cookie is persisted securely between requests.
</Callout>

## Triggering a Parameterized Job with the Crumb

With both the crumb token and session cookie saved, you can trigger a build:

```bash theme={null}
curl -s \
  -u admin:password \
  --cookie /tmp/jenkins_cookies \
  -H "Jenkins-Crumb: <crumb_value>" \
  -X POST "http://localhost:8080/job/parameterized-pipeline-job/buildWithParameters" \
  -d BRANCH_NAME=test \
  -d APP_PORT=6767
```

After execution, verify the new build appears in the Jenkins UI.

## Alternative: API Token Authentication

If managing cookies and crumbs is cumbersome, switch to API token authentication. Requests using an API token are automatically exempt from CSRF checks, streamlining your CI/CD scripts.

## Links and References

* [Jenkins CSRF Protection](https://www.jenkins.io/doc/book/system-administration/security/#csrf-protection)
* [Jenkins REST API](https://www.jenkins.io/doc/book/using/remote-access-api/)
* [Continuous Integration Best Practices](https://www.jenkins.io/solutions/ci-cd/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/4d6d1f39-307c-4fdb-8d2b-834c1650e792/lesson/662942cf-8b11-4b25-9ecb-9198f2b26799" />
</CardGroup>
