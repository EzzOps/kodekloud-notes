# What Is Model Serving

Source: https://notes.kodekloud.com/docs/KServe-Fundamentals-Serving-ML-Models-on-Kubernetes/Foundations/What-Is-Model-Serving/page

Introduction to KServe and practical model serving on Kubernetes, covering deploying Hugging Face models, inference services, operational challenges, and differences between predictive and generative workloads.

Welcome to KServe Fundamentals.

This course focuses on a practical — and often underappreciated — part of the machine learning lifecycle: taking a model out of a notebook and into a system that actually uses it.

<Frame>
  <img alt="The image depicts a circular graphic with &#x22;Machine Learning&#x22; written inside, and a small blue dot on the circle's edge, set against a dark background. The bottom left corner contains a copyright notice from KodeKloud." />
</Frame>

Hi, I'm Chris Short — a longtime DevOps practitioner, Kubernetes contributor, and author of the DevOps'ish newsletter. I'm your instructor for this course. My goal is to help you not only get started with KServe, but also build the confidence to operate it in your environments.

You don't need to be a Kubernetes expert to participate, but you should be familiar with core Kubernetes concepts and comfortable using [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) to manage a cluster.

<Frame>
  <img alt="The image shows two Kubernetes logos under the heading &#x22;Required Knowledge,&#x22; each with a different star rating and symbol—a cross on the left and a checkmark on the right." />
</Frame>

You should also be comfortable using [Helm](https://helm.sh/) to install [KServe](https://kserve.github.io/) itself.

At its simplest, a model is a function: give it input (an image, a row of data, a sentence) and it returns a prediction — a label, a number, a probability, or a generated response.

<Frame>
  <img alt="The image is a diagram explaining what a model is, with &#x22;Input&#x22; on the left (including image, data, sentence), a &#x22;Function&#x22; in the middle, and &#x22;Prediction&#x22; on the right (including label, number)." />
</Frame>

A model artifact — whether you trained it yourself or downloaded it — is typically a bundle of files on disk: weights, configuration, tokenizer files, and so on. Those files alone don't accept requests or return predictions; they need an execution environment that loads them and exposes an API.

Hugging Face has become a common home for model artifacts — often described as the "GitHub for AI" — with tens of thousands of models across many tasks and frameworks. Throughout this course we'll rely on real, open models instead of a bespoke model trained for months. Specifically, we'll use Qwen (an open-capable model from Alibaba on Hugging Face) and later a DistilBERT-based sentiment classifier.

<Frame>
  <img alt="The image compares &#x22;Then vs Now,&#x22; featuring a central icon with &#x22;6 Months of training&#x22; on the left and &#x22;Real, open model&#x22; on the right, leading to the name &#x22;Qwen.&#x22;" />
</Frame>

What does a model server do?

* Loads the model artifact into memory for fast inference.
* Exposes an API endpoint (typically HTTP and/or gRPC) for client requests.
* Manages the request lifecycle: receive input, preprocess, run inference, post-process, and return results.
* At scale, handles batching, concurrency, health checks, autoscaling, and graceful restarts.

<Frame>
  <img alt="The image outlines four key aspects of model serving: loading the model in memory, exposing an API endpoint, handling request lifecycle, and managing batch and concurrent requests with health checking and graceful restarts." />
</Frame>

Model serving is the process of deploying a trained ML model so it can receive requests, run inference, and return predictions in real time or near-real time. Conceptually, it's like any other web service: rather than returning HTML or fetching JSON from a database, the service runs a model on provided inputs and returns predictions.

<Frame>
  <img alt="The image depicts a flowchart for &#x22;Model Serving,&#x22; showing a sequence from &#x22;Qwen&#x22; to &#x22;KServe,&#x22; followed by Kubernetes and a globe icon, with options for HTML and JSON outputs." />
</Frame>

How do you make a model artifact available so other systems — a web app, mobile client, pipeline, or API consumer — can call it? In this course we'll:

* Install KServe on Kubernetes in standard mode using [Helm](https://helm.sh/) and [cert-manager](https://cert-manager.io/).
* Use open models from [Hugging Face](https://huggingface.co/) (Qwen and DistilBERT).
* Create InferenceService manifests in YAML to declare the models we want to serve.
* Use [curl](https://curl.se/) and [jq](https://stedolan.github.io/jq/) to interact with the served models during demos and testing.

> **lightbulb** Recommended prerequisites: familiarity with core Kubernetes concepts, basic `kubectl` usage, and Helm. You should also be comfortable using the command line for testing (curl, jq). These skills will help you follow the hands-on demos more effectively.

If you've wrapped a model in a simple [Flask](https://flask.palletsprojects.com/) app and called it a day, you probably discovered the gap between "it works on my laptop" and "it works reliably under real traffic." Common real-world serving challenges include:

* Resource intensity: large models often need GPUs or specialized inference hardware to meet latency targets.
* Unpredictable scale: traffic spikes require rapid scaling, and you need policies to reduce costs during low traffic.
* Many models: organizations often serve dozens or hundreds of models, which requires repeatable deployment, configuration, and monitoring.
* Concurrency and memory management: handling concurrent requests and multiple models requires careful orchestration.

Open model availability (for example, pulling models from Hugging Face) only solves artifact distribution — running models reliably at scale, managing concurrency, and controlling compute costs are still difficult. KServe is designed to address these operational challenges.

<Frame>
  <img alt="The image presents four challenges of serving models, such as resource intensity and unpredictability in scale, alongside a KServe logo, indicating its use for simplifying model serving." />
</Frame>

One important distinction to draw early is between two broad classes of models: predictive and generative.

Predictive models include classifiers (image labeling), regressors (price prediction), recommenders (scoring items), or sentiment analysis. These models typically accept a request and return a single prediction. They tend to be faster, less resource-intensive, and stateless.

Generative models include large language models (LLMs) and image-generation models. These are often much larger and compute-heavy, may stream outputs incrementally, and require advanced batching and memory strategies.

To help compare, here’s a concise breakdown:

| Characteristic  |                          Predictive Models | Generative Models            |
| --------------- | -----------------------------------------: | ---------------------------- |
| Typical output  |                         Single label/score | Streams or token sequences   |
| Resource needs  |                          Lower (often CPU) | Higher (GPU / large memory)  |
| Latency pattern |                          Short, consistent | Variable, possibly streaming |
| Common tasks    | Classification, regression, recommendation | LLMs, text/image generation  |

<Frame>
  <img alt="The image shows a comparison between predictive and generative models, highlighting tasks such as labeling images, price prediction, scoring inputs, sentiment analysis, and resource usage." />
</Frame>

This course covers both flavors. Early on we'll use a quantized, CPU-friendly Qwen model from Hugging Face for generative inference. Later we'll deploy a DistilBERT-based text classifier to demonstrate how the same KServe primitives apply to predictive workloads. You’ll see how operational considerations change when moving from a language model to a lightweight classifier.

<Frame>
  <img alt="The image shows a timeline with labeled modules, including &#x22;Module 02,&#x22; &#x22;Quantized Version,&#x22; and &#x22;Module 03,&#x22; along with logos for Qwen and a hugging face emoji." />
</Frame>

Summary: model serving is the bridge between a trained model artifact on disk and a live system that uses that model. Serving makes the model reliable, scalable, and accessible. The concept is straightforward, but implementing it correctly — especially at scale on Kubernetes — requires attention to many operational details. That's what the rest of this course is designed to teach.

<Frame>
  <img alt="The image is a slide titled &#x22;Wrapping Up,&#x22; summarizing key points about model serving as an artifact on disk, acting as a bridge to live systems, and involving many moving parts." />
</Frame>

Next up in the course we'll examine KServe's architecture and how its components fit together on top of Kubernetes.

Links and references

* [KServe Documentation](https://kserve.github.io/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Helm](https://helm.sh/)
* [cert-manager](https://cert-manager.io/)
* [Hugging Face](https://huggingface.co/)
* [curl](https://curl.se/)
* [jq](https://stedolan.github.io/jq/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/5231587b-53d5-4ea2-a084-44550d4ce9bb/lesson/5193d2e4-a243-442d-97b8-b1a236f1e6e3)
