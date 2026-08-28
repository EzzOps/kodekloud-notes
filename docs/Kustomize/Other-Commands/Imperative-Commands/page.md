# Download Go modules
go mod download

# Execute all tests
go test ./...
```

If all tests pass, the pipeline moves on to building the Docker image.

***

## 3. Building & Tagging the Container Image

Most CI systems provide an environment variable for the commit SHA. For instance:

```bash theme={null}
# Provided by CI environment
GIT_COMMIT_HASH=abcdef123

# Build and tag the image
docker build -t myrepo/api:$GIT_COMMIT_HASH .
docker push myrepo/api:$GIT_COMMIT_HASH
```

Here, `myrepo/api:abcdef123` uniquely identifies the image corresponding to this commit.

***

## 4. Updating Manifests with kustomize edit

In the CD stage, adjust your Kustomize overlay so the manifest points to the new image tag:

```bash theme={null}
kustomize edit set image api=myrepo/api:$GIT_COMMIT_HASH
```

This command modifies the `images` section of your `kustomization.yaml`:

```yaml theme={null}
images:
- name: api
  newName: myrepo/api
  newTag: abcdef123
```

<Callout icon="triangle-alert">
  Ensure your `kustomization.yaml` is under version control so you can track these automated updates. Avoid committing sensitive credentials or hardcoded tags.
</Callout>

***

## 5. Deploying to Kubernetes

With your overlay updated, deploy the change to production:

```bash theme={null}
kubectl apply -k overlays/production
```

Kubernetes will detect the new image tag, pull `myrepo/api:abcdef123`, and perform a rolling update.

***

## References

* [Kustomize Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [Kubernetes Overviews & Tutorials](https://kubernetes.io/docs/tutorials/)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kustomize/module/060e95ac-e56c-42ed-be87-8701328432c3/lesson/9d6dc297-8f5d-497d-8991-a80c05acaef1" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kustomize/module/8ee78739-877b-4e11-a7a6-82ef7210468b/lesson/3dabb285-4658-4e1f-913a-eed08b1ca049" />
</CardGroup>


# Imperative Commands

Source: https://notes.kodekloud.com/docs/Kustomize/Other-Commands/Imperative-Commands/page

This guide explains how to imperatively update `kustomization.yaml` using `kustomize edit` subcommands via the command line interface.

In this guide, you’ll learn how to **imperatively** update your `kustomization.yaml` using the `kustomize edit` subcommands. Anything you normally declare in YAML—adding or removing labels, prefixes, namespaces, modifying images or replica counts—can also be done directly via the CLI.

Before you start, check the help output for available subcommands:

```bash theme={null}
kustomize edit --help
```

You’ll see usage examples and commands such as:

```bash theme={null}
