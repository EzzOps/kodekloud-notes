# When prompted, paste your PAT
```

On success, you’ll see:

```text theme={null}
Login succeeded
```

## 3. Push the OCI Artifact

Flux’s `push artifact` command packages a directory (or file) as an OCI artifact and uploads it to a registry.

<Frame>
  ![The image shows a webpage from the Flux documentation, specifically detailing the "flux push artifact" command. It includes a synopsis of the command's functionality, which involves creating a tarball and uploading it to an OCI repository, along with examples and additional options.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877633/notes-assets/images/GitOps-with-FluxCD-DEMO-Push-Kubernetes-Manifest-to-OCI-Registry/flux-push-artifact-command-documentation.jpg)
</Frame>

First, set reusable variables and then run:

```bash theme={null}
# Generate tags and metadata
REF=$(git rev-parse --short HEAD)
SRC=$(git config --get remote.origin.url)
TAG="7.7.0-${REF}"
REPO="oci://ghcr.io/<username>/bb-app:${TAG}"

# Push manifests as an OCI artifact
flux push artifact "${REPO}" \
  --path="./manifests" \
  --source="${SRC}" \
  --revision="${TAG}"
```

What happens:

* Flux reads your GHCR credentials from `~/.docker/config.json`
* It tars up `./manifests`
* Uploads to `ghcr.io/<username>/bb-app:7.7.0-<short-git-sha>`
* Attaches the Git remote URL and revision metadata

A successful push shows:

```bash theme={null}
pushing artifact to ghcr.io/<username>/bb-app@sha256:<digest>
artifact successfully pushed to ghcr
```

## 4. Verify the Package

1. Go to your GitHub repo’s **Packages** tab and refresh.
2. You should see `bb-app` listed under private packages.

You can also confirm locally:

```bash theme={null}
docker pull ghcr.io/<username>/bb-app:7.7.0-<short-git-sha>
```

<Callout icon="lightbulb">
  Flux requires a Kubernetes [imagePullSecret](/docs/guides/oci-acr/) to authenticate when pulling OCI artifacts. We’ll cover secret creation in a later module.
</Callout>

***

## Next Steps

In the following lesson, we will package and push Helm charts to an OCI registry.

## References

* [Flux CLI: push artifact](https://fluxcd.io/docs/cli/flux_push_artifact/)
* [GitHub Container Registry](https://docs.github.com/packages)
* [OCI Artifacts Spec](https://github.com/opencontainers/artifacts)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/205ec7c7-4cb6-4ecb-9bb5-fa50419f1e68/lesson/13765f33-6b31-4a36-bb10-d07ab3bfa621" />
</CardGroup>


# DEMO Setting up the MySQL Database

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Helm-Controller-and-OCI-Registry/DEMO-Setting-up-the-MySQL-Database/page

This guide covers deploying a MySQL database on Kubernetes using Flux and Kustomize manifests.

In this guide, we’ll walk through deploying a MySQL database on Kubernetes using Flux’s GitRepository and Kustomization controllers along with Kustomize manifests. By following these steps, you will:

1. Update the PHP application to connect to MySQL
2. Define Kubernetes manifests for MySQL
3. Use Flux GitRepository and Kustomization resources for GitOps deployment

***

## 1. Update the PHP Application

On the `7-demo` branch, the PHP app has been extended to store high scores in a MySQL database. The connection logic in `highscore.php` now looks like:

```php theme={null}
<?php
$servername = "mysql.database.svc.cluster.local";
$username   = "root";
$password   = "mysql-password-0123456789";
$dbname     = "bricks";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Escape and use the posted high score
$highscore = mysqli_real_escape_string($conn, $_POST['highscore']);
// ... (insert logic)
```

Ensure you’re on the correct branch in your terminal:

```bash theme={null}
git checkout 7-demo
