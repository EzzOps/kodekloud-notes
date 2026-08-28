# KServe Architecture

Source: https://notes.kodekloud.com/docs/KServe-Fundamentals-Serving-ML-Models-on-Kubernetes/Foundations/KServe-Architecture/page

Overview of KServe architecture explaining Kubernetes-native InferenceService, control and data planes, runtimes, storage initializer, deployment modes, and the lifecycle for serving ML models reliably

Welcome back!

A model server is the bridge between a trained model and a live system that uses it. KServe brings that bridge to Kubernetes by adding ML-aware abstractions on top of Kubernetes primitives. This article explains KServe’s architecture, how its control and data planes interact, and the essential resources you’ll use to serve models reliably.

KServe is Kubernetes-native: it extends Kubernetes with Custom Resource Definitions (CRDs) that represent model-serving concepts. The primary CRD you will work with is the InferenceService.

The InferenceService is the main declarative abstraction. You provide a name, the model format, and a model location — for example `s3://my-bucket/my-model`, `gs://my-bucket/my-model`, or a Hugging Face model ID. KServe handles provisioning, runtime selection, networking, and status reporting based on that manifest.

<Frame>
  <img alt="The image illustrates a flow diagram featuring KServe and InferenceService, showcasing their components and relationships, including Custom Resource Definitions and various storage-related attributes." />
</Frame>

When you apply an InferenceService YAML to the cluster, the KServe controller-manager observes it and begins reconciliation. The controller-manager is the control plane: it watches InferenceService resources, picks a serving runtime, creates the underlying compute resources, configures networking, and updates resource status (for example indicating readiness and the service URL).

<Frame>
  <img alt="The image is a diagram labeled &#x22;The Control Plane,&#x22; showing connections between InferenceService, Cluster, Kserve Controller Manager, and components like Serving Runtime and Networking." />
</Frame>

This follows Kubernetes’ reconciliation pattern: declare the desired state, and the control plane enforces it. Change the model URI and the controller will roll out a new version. Restart the cluster and the controller will restore the declared state.

KServe does not provide a single monolithic model server. Instead it uses ClusterServingRuntimes — templates that map model formats to container images and pod specifications. KServe ships with runtimes for common frameworks:

* scikit-learn
* XGBoost
* LightGBM
* PyTorch (via TorchServe)
* NVIDIA Triton
* Hugging Face servers for generative/predictive models

You can also add custom ClusterServingRuntimes for frameworks or deployment patterns that aren’t included out of the box. When you declare a model format in an InferenceService, the controller chooses the appropriate runtime and constructs the Pod spec.

<Frame>
  <img alt="The image displays a list of serving runtimes for machine learning, including Scikit-learn, XGBoost, LightGBM, and others, under the category &#x22;ClusterServingRuntimes.&#x22; It also notes that the runtime matches the pod specification." />
</Frame>

The control plane handles lifecycle and orchestration; the data plane handles live inference traffic. A prediction request follows this flow: it arrives at an ingress point, is routed to the predictor component, the serving runtime loads the model, runs inference, and returns the result.

KServe supports an optional transformer component for pre-processing and post-processing. Placeholders for protocol translation, input normalization, or response formatting are implemented in the transformer so you can keep the serving runtime focused on inference.

<Callout icon="lightbulb">
  Use transformers to separate preprocessing/postprocessing from the predictor. This keeps model containers simple and lets you update request/response logic independently of the model server.
</Callout>

<Frame>
  <img alt="The image illustrates a data flow chart titled &#x22;The Data Plane – Request Flow,&#x22; showing steps like &#x22;Ingress Point,&#x22; &#x22;Route to Predictor,&#x22; &#x22;Run Inference,&#x22; and &#x22;Return Result.&#x22;" />
</Frame>

A key implementation detail is the storage initializer. When the predictor Pod is created, KServe injects an init container that runs before the model server starts. This initializer downloads the model artifact from the configured storage backend — S3, GCS, Azure Blob, a PVC, or Hugging Face — and places it at a known local path inside the Pod. The model server then reads the artifact from that local path.

This abstraction hides the artifact’s origin from the model server; the runtime only needs to read a local path, so your InferenceService can point to different storage backends interchangeably.

<Frame>
  <img alt="The image is a flowchart titled &#x22;The Storage Initializer,&#x22; describing the process where Kserve creates a pod, injects an init container, which downloads a model artifact and places it in a known local path. Various icons are displayed at the bottom." />
</Frame>

Deployment modes

KServe supports two main deployment modes. Choose based on resource cost, operational complexity, and latency requirements:

| Mode                                                     | Behavior                                                                                     | When to use                                                                                              |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Serverless (`KServe + Knative + Istio`)                  | Scale-to-zero for idle models; scales up on traffic. Adds Knative and networking complexity. | Environments where reducing steady-state cost is important and occasional cold starts are acceptable.    |
| RawDeployment (standard Kubernetes Deployment + ingress) | Uses regular Deployments; no scale-to-zero and no Knative. Simpler and avoids cold starts.   | Local development, simpler clusters, or low-latency production workloads needing consistent performance. |

<Callout icon="warning">
  Serverless mode saves resources by scaling idle models to zero, but expect cold-start latency on the first request and additional components to operate.
</Callout>

<Frame>
  <img alt="The image illustrates deployment modes, focusing on a &#x22;Serverless&#x22; option with features like scaling to zero pods, freeing GPU/CPU resources, scale backup, and operational complexity challenges. A &#x22;RawDeployment&#x22; option is also mentioned." />
</Frame>

These examples use RawDeployment because it’s easier to run locally with tools like Minikube or kind, and it keeps the focus on KServe itself rather than serverless components.

<Frame>
  <img alt="The image compares &#x22;Deployment Modes&#x22; with selections for &#x22;Serverless&#x22; and &#x22;RawDeployment,&#x22; highlighting features such as &#x22;Simple,&#x22; &#x22;No Cold Start,&#x22; and &#x22;No Scale to Zero.&#x22; It includes icons for Kubernetes and related tools." />
</Frame>

Putting it all together: the typical lifecycle

1. Write an InferenceService manifest (name, model format, model URI).
2. Apply it to the cluster.
3. KServe controller-manager detects the resource, selects a ClusterServingRuntime, and creates Pods.
4. Each Pod gets a storage initializer that downloads the model to a local path.
5. The model server loads the artifact and begins serving.
6. Ingress routes requests to the predictor (and optional transformer), and predictions are returned to clients.

KServe gives you a declarative, Kubernetes-native way to automate the hard parts of model-serving infrastructure: runtime selection, artifact provisioning, scaling, and networking.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Putting It All Together,&#x22; outlining steps in a process involving writing an InferenceService, a controller picking it up, selecting a ClusterServingRuntime, downloading a model, and serving it." />
</Frame>

Next steps

This architecture can feel abstract until you use actual resources. To get hands-on, set up a local cluster and install KServe:

* Minikube: [https://minikube.sigs.k8s.io/docs/](https://minikube.sigs.k8s.io/docs/)
* kind: [https://kind.sigs.k8s.io/](https://kind.sigs.k8s.io/)

References and further reading

* KServe documentation: [https://kserve.github.io/](https://kserve.github.io/)
* Kubernetes concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)
* Knative Serving: [https://knative.dev/docs/serving/](https://knative.dev/docs/serving/)
* Hugging Face model hub: [https://huggingface.co/](https://huggingface.co/)

In the following lessons we’ll walk through installing KServe on a local cluster and deploying a sample InferenceService so you can experience the entire control/data plane lifecycle end-to-end.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/5231587b-53d5-4ea2-a084-44550d4ce9bb/lesson/b185ca30-5e3b-4e44-8f75-1bed7e006f3a" />
</CardGroup>
