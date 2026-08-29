# Variables from Image Registeries

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/External-Data-Sources/Variables-from-Image-Registeries/page

Explains using Kyverno's imageRegistry context to fetch OCI image config and manifest, enabling policies to detect root-running images and enforce image-level admission controls

You can pull configuration and metadata from ConfigMaps, external APIs, and—most powerfully—directly from an OCI image registry. This lesson shows how to use Kyverno's image registry context to inspect container image configuration (for example, the default user) and make admission decisions based on that data.

Alex has become experienced at writing Kyverno policies that validate Kubernetes resources: labels, annotations, security context, and more. He blocked Pods from running as root by checking the Pod spec. Then a developer applies a Pod manifest that looks fine—the Pod spec doesn't request root—but it uses the `ubuntu:latest` image. Alex knows many base images (including Ubuntu) don't set a `USER` in the Dockerfile, so by default they run as root.

<Frame>
  <img alt="The image outlines a challenge involving deploying a Pod with the &#x22;ubuntu:latest&#x22; image, pointing out that while the Pod manifest doesn't specify a user, the image runs as root by default. There is also a graphic of puzzle pieces with a question mark." />
</Frame>

Alex's policies had a blind spot: they validate only the Kubernetes manifest and can't inspect the image contents stored in the registry. He needs a way to query the registry, fetch the image config (including the default `User`), and use that information inside a policy.

<Frame>
  <img alt="The image titled &#x22;Alex's New Challenge&#x22; shows a person named Alex facing a dilemma about writing a policy to analyze a container image's actual configuration beyond Kubernetes YAML." />
</Frame>

This is exactly what Kyverno's image registry context solves.

The `imageRegistry` context lets Kyverno query an OCI registry for an image manifest and config, and then expose that data as a variable inside a policy. Provide a reference to the target image and Kyverno returns a structured JSON object with useful fields.

<Frame>
  <img alt="The image introduces the imageRegistry context, explaining that it allows Kyverno to fetch image metadata from an OCI registry and store it in a variable." />
</Frame>

Example `context` entry:

```yaml theme={null}
context:
  - name: imageData
    imageRegistry:
      reference: "ghcr.io/kyverno/kyverno:latest"
```

* `imageData` is the variable name you can reference in rules.
* `reference` is the fully-qualified image (name:tag or name\@digest) Kyverno will inspect.

When the policy runs, Kyverno queries the registry (internally similar to using the `crane` tool), fetches the manifest and the image config, and fills `imageData` with a structured JSON object.

What does `imageData` contain? Typical keys include the resolved image, registry, repository, and two important structures: `manifest` and `configData`. Example shape:

```json theme={null}
{
  "image": "ghcr.io/kyverno/kyverno",
  "resolvedImage": "ghcr.io/kyverno/kyverno@sha256:...",
  "registry": "ghcr.io",
  "repository": "kyverno/kyverno",
  "identifier": "latest",
  "manifest": { /* crane manifest <image> */ },
  "configData": { /* crane config <image> */ }
}
```

<Frame>
  <img alt="The image contains a title, &#x22;What's Inside the imageData Variable?&#x22; and a description stating it is a rich JSON object containing the image's manifest and config." />
</Frame>

The `configData` payload includes the image configuration returned by the registry, such as `Entrypoint`, `Env`, and `User`. On the CLI, you can inspect the same info using `crane config`:

```bash theme={null}
$ crane config ghcr.io/kyverno/kyverno:latest | jq
{
  "architecture": "amd64",
  "created": "2023-01-08T00:10:08Z",
  "history": [ ... ],
  "os": "linux",
  "rootfs": { ... },
  "config": {
    "Entrypoint": [
      "/ko-app/kyverno"
    ],
    "Env": [
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin:/ko-app",
      "SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt"
    ],
    ...
    "User": "65532"
  },
  "User": "65532"
}
```

The critical field for preventing root containers is the `User` value inside the image config (`config.User`). If an image author sets `USER` in the Dockerfile, `User` will contain that value. If `USER` is not set (common for many base images like Ubuntu), `User` will be empty or absent, meaning the container runs as root by default.

How to deny Pods that use images configured to run as root
Below is a Kyverno `validate` rule that checks each container in a Pod using `foreach`. For each container, it calls `imageRegistry` to fetch the image config and denies the Pod if the image `User` is empty.

```yaml theme={null}
rules:
  - name: no-root-images
    match:
      resources:
        kinds:
          - Pod
    validate:
      message: "Images configured to run as root are not allowed."
      foreach:
        - list: "request.object.spec.containers"
          context:
            - name: imageData
              imageRegistry:
                reference: "{{ element.image }}"
          deny:
            conditions:
              any:
                - key: "{{ imageData.configData.config.User }}"
                  operator: Equals
                  value: ""
```

Why this works:

* `match` selects Pods for validation.
* `foreach` walks each container in `request.object.spec.containers` (Pod may have multiple).
* For each container, `imageRegistry` resolves the container `image` (`{{ element.image }}`) and stores the result in `imageData`.
* The `deny` condition checks `imageData.configData.config.User`; if it is empty, the rule denies the Pod because the image will run as root by default.

Practical examples

* Pod using Ubuntu (expected to be denied)

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: badpod
spec:
  containers:
  - name: ubuntu
    image: ubuntu:latest
```

Applying it:

```bash theme={null}
$ kubectl apply -f bad.yaml
Error from server: admission webhook "kyverno" denied the request: Images configured to run as root are not allowed.
```

* Pod using a non-root image (Kyverno image; expected to be allowed)

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: goodpod
spec:
  containers:
  - name: kyverno
    image: ghcr.io/kyverno/kyverno:latest
```

Applying it:

```bash theme={null}
$ kubectl apply -f good.yaml
pod/goodpod created
```

This enforces image-level best practices (the image author set a non-root `USER`) in addition to validating the Kubernetes manifest.

<Callout icon="lightbulb">
  Kyverno must be able to reach the registry to fetch image metadata. For private registries, configure the appropriate image pull credentials in Kyverno so it can authenticate when requesting image data.
</Callout>

Advanced usage: transform registry JSON with JMESPath
You can supply a `jmesPath` expression in the `imageRegistry` context to extract or compute exactly the value you need from the registry JSON. For example, compute the total image size (sum of layer sizes) and store it as a string:

```yaml theme={null}
context:
  - name: imageSize
    imageRegistry:
      reference: "{{ element.image }}"
      jmesPath: "to_string(sum(manifest.layers[*].size))"
```

This `jmesPath` expression:

* selects `manifest.layers[*].size`,
* sums them via `sum(...)`,
* converts the number to a string with `to_string(...)`, and
* stores the result in `imageSize` for use elsewhere (for example, to deny images larger than a size threshold).

Quick reference: common `imageData` keys

| Key             | Description                                          | Example                              |
| --------------- | ---------------------------------------------------- | ------------------------------------ |
| `image`         | Image name without identifier                        | `ghcr.io/kyverno/kyverno`            |
| `resolvedImage` | Image resolved to a digest                           | `ghcr.io/kyverno/kyverno@sha256:...` |
| `registry`      | Registry host                                        | `ghcr.io`                            |
| `repository`    | Repository path                                      | `kyverno/kyverno`                    |
| `identifier`    | Tag or digest identifier                             | `latest`                             |
| `manifest`      | The image manifest JSON                              | see `manifest.layers[*].size`        |
| `configData`    | The image config JSON containing `config` and `User` | `config.User`                        |

Recap

* Kyverno's `imageRegistry` context gives you a window into the container image: manifest and config.
* Use it to inspect `config.User` (and other fields like `Env`, `Entrypoint`) and enforce policies that depend on image internals, not just the Pod manifest.
* Use `jmesPath` to extract or compute values from the fetched JSON for more advanced validations.

<Frame>
  <img alt="The image is a summary list of four key features related to image data and policies, including new context, rich data, powerful validations, and advanced transformation. Each feature is numbered and briefly explained." />
</Frame>

You are now equipped to write Kyverno policies that pull image metadata from registries, enabling more intelligent, context-aware admission controls.

Links and references

* Kyverno: [https://kyverno.io/](https://kyverno.io/)
* Google go-containerregistry (crane): [https://github.com/google/go-containerregistry/tree/main/cmd/crane](https://github.com/google/go-containerregistry/tree/main/cmd/crane)
* JMESPath: [https://jmespath.org/](https://jmespath.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/470bb961-febf-41b6-b75b-4c439def6eae/lesson/201e7da3-4ecd-4ae8-bfc1-0c1e4587c0be" />
</CardGroup>
