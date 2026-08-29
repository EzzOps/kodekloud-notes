# Fetch instances and parse JSON
DATA=$(aws ec2 describe-instances)
echo "Raw describe-instances response: $DATA"

# Extract public DNS for tag "dev-deploy"
URL=$(echo "$DATA" \
  | jq -r '.Reservations[].Instances[]
      | select(.Tags[].Value == "dev-deploy")
      | .PublicDnsName')

echo "Discovered URL: $URL"
[[ -z "$URL" ]] && { echo "Failed to fetch URL; check AWS credentials and tags."; exit 1; }

# Define endpoints
declare -A ENDPOINTS=(
  ["/live"]="GET"
  ["/planet"]="POST"
)

# Test /live
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://$URL:3000/live")
echo "HTTP status code at /live: $HTTP_CODE"

# Test /planet
PLANET_DATA=$(curl -s -X POST "http://$URL:3000/planet" \
  -H "Content-Type: application/json" \
  -d '{"id":"3"}')
echo "Response from /planet: $PLANET_DATA"

PLANET_NAME=$(echo "$PLANET_DATA" | jq -r '.name')
echo "Parsed planet name: $PLANET_NAME"

# Validate responses
if [[ "$HTTP_CODE" -eq 200 && "$PLANET_NAME" == "Earth" ]]; then
  echo "Integration tests passed."
else
  echo "One or more integration tests failed."
  exit 1
fi
```

Make it executable:

```bash theme={null}
chmod +x integration-testing-ec2.sh
```

## 3. AWS CLI: `describe-instances`

We use the AWS CLI’s `describe-instances` to list EC2 instances and filter by tag.

![The image shows a webpage from the AWS CLI Command Reference, specifically the documentation for the "describe-instances" command. It includes a table of contents, a note about AWS CLI versioning, and a description of the command's functionality.](https://kodekloud.com/kk-media/image/upload/v1752870513/notes-assets/images/Certified-Jenkins-Engineer-Demo-Integration-Testing-AWS-EC2-Instance/aws-cli-describe-instances-docs.jpg)

Example JSON snippet:

```json theme={null}
{
  "Reservations": [
    {
      "Instances": [
        {
          "InstanceId": "i-1234567890abcdef0",
          "PublicDnsName": "ec2-34-253-223-13.us-east-2.compute.amazonaws.com",
          "PublicIpAddress": "34.253.223.13",
          "Tags": [
            { "Key": "Name", "Value": "dev-deploy" }
          ]
        }
      ]
    }
  ]
}
```

We extract `.PublicDnsName` where `.Tags[].Value == "dev-deploy"` using `jq`.

## 4. Integrating with Jenkins Pipeline

We’ll add a new stage **Integration Testing – AWS EC2** in the `Jenkinsfile`:

1. Trigger on `feature/*` branches
2. Use `withAWS` (AWS Pipeline Steps plugin) for credentials and region
3. Execute our shell script

> **triangle-alert** Store your AWS credentials securely in Jenkins Credentials. Never hard-code keys in your `Jenkinsfile`.

### Credentials Setup

![The image shows a Jenkins dashboard displaying a list of stored credentials, including IDs and names for various services like MongoDB, Gitea, and AWS.](https://kodekloud.com/kk-media/image/upload/v1752870514/notes-assets/images/Certified-Jenkins-Engineer-Demo-Integration-Testing-AWS-EC2-Instance/jenkins-dashboard-credentials-list.jpg)

### Generate `withAWS` Snippet

Use Jenkins’ **Pipeline Syntax** to obtain:

![The image shows a Jenkins Pipeline Syntax configuration page, where AWS settings are being set for a nested block, including fields for region, endpoint URL, and credentials.](https://kodekloud.com/kk-media/image/upload/v1752870515/notes-assets/images/Certified-Jenkins-Engineer-Demo-Integration-Testing-AWS-EC2-Instance/jenkins-pipeline-aws-settings-config.jpg)

### Jenkinsfile Stage

```groovy theme={null}
stage('Integration Testing - AWS EC2') {
  when {
    branch 'feature/*'
  }
  steps {
    sh 'printenv | grep -i branch'

    withAWS(credentials: 'aws-s3-ec2-lambda-creds', region: 'us-east-2') {
      sh 'bash integration-testing-ec2.sh'
    }
  }
}
```

## 5. Pipeline Execution & Results

After pushing changes, the new stage runs automatically. Here’s a successful pipeline:

![The image shows a Jenkins pipeline interface for a project named "solar-system," displaying various stages of a build process, with most stages completed successfully. The integration testing section provides details on specific tasks and their statuses.](https://kodekloud.com/kk-media/image/upload/v1752870516/notes-assets/images/Certified-Jenkins-Engineer-Demo-Integration-Testing-AWS-EC2-Instance/jenkins-pipeline-solar-system-build.jpg)

Log excerpt:

```bash theme={null}
$ printenv | grep -i branch
BRANCH_NAME=feature/enabling-cicd

[Integration Testing - AWS EC2] $ bash integration-testing-ec2.sh
Integration test starting...
aws-cli/2.17.56 Python/3.10.6 Linux/...
Raw describe-instances response: { ... }
Discovered URL: ec2-3-140-244-188.us-east-2.compute.amazonaws.com
HTTP status code at /live: 200
Response from /planet: {"id":3,"name":"Earth"}
Parsed planet name: Earth
Integration tests passed.
```

## 6. Summary of Endpoints Tested

| Endpoint | Method | Expected Output           |
| -------- | ------ | ------------------------- |
| /live    | GET    | 200 OK                    |
| /planet  | POST   | `{"id":3,"name":"Earth"}` |

With this setup, each commit on a feature branch dynamically locates the EC2 instance, verifies service health, and enforces basic integration tests before completing the pipeline.

## References

* [AWS CLI describe-instances](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html)
* [Jenkins AWS Steps Plugin](https://plugins.jenkins.io/aws-steps/)
* [jq Documentation](https://stedolan.github.io/jq/)
* [curl Manual](https://curl.se/docs/manpage.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/e16e4b93-31c4-479b-96b8-f0d26cde31cd/lesson/1f45881d-47c1-4154-bf4f-e5c80d18449b)


# Demo Push to Registry

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Containerization-and-Deployment/Demo-Push-to-Registry/page

This tutorial extends a Jenkins CI pipeline to push a Docker image to Docker Hub after building and scanning it for vulnerabilities.

In this tutorial, you’ll extend your Jenkins CI pipeline to push a Docker image to Docker Hub. We assume you have already:

* Built the Docker image.
* Scanned it for vulnerabilities using [Trivy](https://github.com/aquasecurity/trivy).

Let’s configure Jenkins to authenticate with Docker Hub and push the image.

> **lightbulb** Make sure your Jenkins agent has Docker installed and the Docker daemon is accessible by the Jenkins user.

## Stage: Push Docker Image

Begin by adding a `Push Docker Image` stage to your `Jenkinsfile`. A minimal example:

```groovy theme={null}
stage('Push Docker Image') {
  steps {
    sh 'docker push siddharth67/solar-system:$GIT_COMMIT'
  }
}
```

If you run this now, Jenkins will error out because it’s not logged in to Docker Hub.

## Install the Docker Pipeline Plugin

To enable registry authentication and image operations in a Jenkins Pipeline, install the **Docker Pipeline** plugin.

![The image shows a webpage for the Docker Pipeline plugin on the Jenkins website, detailing its documentation, version, installation statistics, and related links.](https://kodekloud.com/kk-media/image/upload/v1752870517/notes-assets/images/Certified-Jenkins-Engineer-Demo-Push-to-Registry/docker-pipeline-plugin-jenkins-docs.jpg)

This plugin provides the following key methods and global variables:

| Method / Variable    | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| `docker`             | Namespace for Docker operations (build, run, push, etc.)    |
| `withDockerRegistry` | Wraps steps inside a login session for a container registry |
| `registry`           | Reference to a configured registry endpoint                 |
| `image`              | Creates or references a Docker image object in the pipeline |

![The image shows a webpage displaying documentation for Jenkins Pipeline Syntax, specifically focusing on global variables related to Docker functions. It includes descriptions of methods like withRegistry, withServer, and image.](https://kodekloud.com/kk-media/image/upload/v1752870518/notes-assets/images/Certified-Jenkins-Engineer-Demo-Push-to-Registry/jenkins-pipeline-syntax-docker-vars.jpg)

## Generate the withDockerRegistry Snippet

1. In Jenkins, navigate to **Pipeline Syntax** > **Snippet Generator**.
2. Under **Docker Pipeline**, select **withDockerRegistry**.

![The image shows a Jenkins interface with a "Snippet Generator" for creating pipeline scripts, highlighting the "withDockerContainer" option to run build steps inside a Docker container.](https://kodekloud.com/kk-media/image/upload/v1752870519/notes-assets/images/Certified-Jenkins-Engineer-Demo-Push-to-Registry/jenkins-snippet-generator-withdockercontainer.jpg)

3. Switch to the **Docker Registry** snippet. Configure the registry URL and credentials.

![The image shows a Jenkins Pipeline Syntax page with options for configuring a Docker registry endpoint, including fields for the Docker registry URL and registry credentials.](https://kodekloud.com/kk-media/image/upload/v1752870520/notes-assets/images/Certified-Jenkins-Engineer-Demo-Push-to-Registry/jenkins-pipeline-docker-registry.jpg)

## Add Docker Hub Credentials

Create Docker Hub credentials in Jenkins:

![The image shows a Jenkins Credentials Provider interface where a user is configuring credentials with options for kind, scope, username, and password. The interface includes fields for entering an ID and description.](https://kodekloud.com/kk-media/image/upload/v1752870521/notes-assets/images/Certified-Jenkins-Engineer-Demo-Push-to-Registry/jenkins-credentials-provider-interface.jpg)

| Field    | Description                         | Example                  |
| -------- | ----------------------------------- | ------------------------ |
| Kind     | Credentials type                    | Username with password   |
| ID       | Unique Jenkins ID for lookup        | `docker-hub-credentials` |
| Username | Docker Hub account username         | `siddharth67`            |
| Password | Docker Hub password or access token | `••••••••`               |

## Final Jenkinsfile Configuration

Update your `Push Docker Image` stage to wrap the push command in `withDockerRegistry`:

```groovy theme={null}
stage('Push Docker Image') {
  steps {
    withDockerRegistry(credentialsId: 'docker-hub-credentials', url: '') {
      sh 'docker push siddharth67/solar-system:$GIT_COMMIT'
    }
  }
}
```

> **lightbulb** Leaving `url: ''` uses the default Docker Hub endpoint (`https://index.docker.io/v1/`).

Commit and push these changes. Jenkins will now authenticate and push the image:

```bash theme={null}
$ docker push siddharth67/solar-system:cf1715a460f1bcb02618528326bd84f70f6a0
The push refers to repository [docker.io/siddharth67/solar-system]
4a0d352d35f4: Preparing
0a471d608574: Preparing
804d07a05ede: Layer already exists
f3b328347c79: Layer already exists
```

## Verifying on Docker Hub

After the pipeline finishes, log in to Docker Hub to confirm your repository and tag:

![The image shows a Docker Hub interface displaying a list of repositories under the user "siddharth67," with options to search, create repositories, and manage organizations.](https://kodekloud.com/kk-media/image/upload/v1752870523/notes-assets/images/Certified-Jenkins-Engineer-Demo-Push-to-Registry/docker-hub-repositories-siddharth67.jpg)

You should see the new image tag matching your git commit hash.

## Confirm in GitHub

You can also verify the commit ID in your source repository:

![The image shows a code repository interface with a list of commits, branches, and files. It highlights a recent commit on the "feature/enabling-cicd" branch.](https://kodekloud.com/kk-media/image/upload/v1752870524/notes-assets/images/Certified-Jenkins-Engineer-Demo-Push-to-Registry/code-repository-commits-branches.jpg)

## Summary

With this configuration, your CI pipeline now:

* Builds a Docker image.
* Scans it with Trivy for vulnerabilities.
* Authenticates and pushes the image to Docker Hub.

Next, we’ll cover automated deployment in a future guide.

## References

* [Trivy – Aqua Security](https://github.com/aquasecurity/trivy)
* [Jenkins Docker Pipeline Plugin](https://www.jenkins.io/doc/book/pipeline/docker/)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/e16e4b93-31c4-479b-96b8-f0d26cde31cd/lesson/8aaf01ac-7a64-439d-b3d9-627781e6a7e1)
