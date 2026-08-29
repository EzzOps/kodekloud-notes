# Expected output:
# inferenceservice.serving.kserve.io/sentiment-classifier created
```

KServe will detect the new resource, select the Hugging Face runtime, and begin provisioning the pod (the initializer downloads the DistilBERT weights). Watch the InferenceService until it becomes ready:

```bash theme={null}
kubectl get inferenceservice sentiment-classifier -n kserve-inference -w
```

When the resource is initially created you will usually see `READY False` while the model downloads and the pod initializes. DistilBERT is relatively small (\~250 MB), so readiness often follows quickly, though actual timing depends on network and model registry availability. When `READY True` appears, the endpoint is live.

You may also see a route URL such as:

[http://sentiment-classifier-kserve-inference.example.com](http://sentiment-classifier-kserve-inference.example.com)

To access the service from your local machine, open a port-forward to the predictor service (run it in the background so you can keep using the same terminal for curl requests):

```bash theme={null}
kubectl port-forward svc/sentiment-classifier-predictor -n kserve-inference 8080:80 &
# Example output:
# Forwarding from 127.0.0.1:8080 -> 8080
```

> **lightbulb** Classifiers use an Open Inference Protocol (OIP) style endpoint rather than the OpenAI-compatible chat/completion endpoints used by conversational models (e.g., Qwen). Conversational models accept a `messages` array on endpoints like `/openai/v1/chat/completions`. Classifiers receive text inputs as OIP tensors via `/v2/models/<model-name>/infer`.

Endpoint (local port-forward):

/v2/models/sentiment-classifier/infer

Example curl request (OIP v2 format). This sends a single sentence to classify:

```bash theme={null}
curl -s http://localhost:8080/v2/models/sentiment-classifier/infer \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "name": "input-0",
        "shape": [1],
        "datatype": "BYTES",
        "data": ["I really enjoyed this course. The examples were clear and helpful."]
      }
    ]
  }' | jq .
```

Request field reference

| Field      | Description                                    | Example            |
| ---------- | ---------------------------------------------- | ------------------ |
| `inputs`   | Array of input tensors (OIP-style).            | See request above. |
| `name`     | Arbitrary identifier for the input tensor.     | `"input-0"`        |
| `shape`    | Tensor shape; `[1]` for a single sentence.     | `[1]`              |
| `datatype` | Data type of the tensor. Use `BYTES` for text. | `BYTES`            |
| `data`     | Array of text strings to classify.             | `["I loved it!"]`  |

Sample response (formatted):

```json theme={null}
{
  "model_name": "sentiment-classifier",
  "model_version": null,
  "id": "31f71876-e616-4aeb-a9d4-4c1f27f8efe1",
  "parameters": null,
  "outputs": [
    {
      "name": "output-0",
      "shape": [1],
      "datatype": "BYTES",
      "parameters": null,
      "data": [
        "{0: 0.0001, 1: 0.9999}"
      ]
    }
  ]
}
```

How to interpret the response:

* `outputs[0].data[0]` contains a string encoding of class probabilities mapping class index → probability.
* In this example, key `0` = negative sentiment and key `1` = positive sentiment.
* The example indicates \~0.0001 probability for negative and \~0.9999 for positive — \~99.99% confidence that the sentence is positive.

Try different inputs to observe how confidence varies:

* Strongly negative: "This course is a waste of time. Nothing worked the way it was supposed to." → high probability for `0` (negative).
* Ambiguous: "It was fine, I guess." → probabilities closer together (e.g., \~60% vs \~40%), showing model uncertainty that would be hidden by a bare class label.

Quick lab steps (try this yourself)

| Step                      | Command                                                                                 |
| ------------------------- | --------------------------------------------------------------------------------------- |
| 1. Apply manifest         | `kubectl apply -f sentiment-classifier.yaml`                                            |
| 2. Wait for readiness     | `kubectl get inferenceservice sentiment-classifier -n kserve-inference -w`              |
| 3. Port-forward predictor | `kubectl port-forward svc/sentiment-classifier-predictor -n kserve-inference 8080:80 &` |
| 4. Send inference request | Use the curl example above to POST to `/v2/models/sentiment-classifier/infer`           |
| 5. Inspect result         | Check `outputs[0].data[0]` — `0` = negative, `1` = positive                             |

> **warning** If you run port-forward in the background, remember to kill the job when finished (e.g., `kill %1` or use `pkill -f "kubectl port-forward ..."`). Leaving processes running can keep ports occupied or leak credentials in some environments.

Observability tips

* Clear, unambiguous inputs tend to produce high-confidence scores (>99%).
* Ambiguous or neutral sentences produce probabilities that are closer together, which is exactly why returning scores (instead of just labels) gives better insight into model uncertainty.
* Use multiple example sentences to validate expected behavior across edge cases.

References

* [KServe Documentation](https://kserve.github.io/website/)
* [Hugging Face Models & Runtimes](https://huggingface.co/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

Good luck experimenting — vary the inputs and observe how the probability distribution reflects confidence and ambiguity.

- [Watch Video](https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/d3f12b82-312d-4aee-a0bc-f5b313a63fd2/lesson/fc3b7835-781f-4ae9-b113-b0087ecbc7c8)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/d3f12b82-312d-4aee-a0bc-f5b313a63fd2/lesson/365cd8a1-bd9f-48e4-9670-44e26cbb5af5)


# What Changes With Predictive Models

Source: https://notes.kodekloud.com/docs/KServe-Fundamentals-Serving-ML-Models-on-Kubernetes/Serving-a-Predictive-Model/What-Changes-With-Predictive-Models/page

Explains differences between generative and predictive models, deploying a DistilBERT sentiment classifier with KServe, and how request and response shapes and manifests differ

Welcome to this module on serving predictive models with KServe. In the previous lesson we deployed a generative language model (Qwen) and invoked it with chat-style prompts. In this lesson we'll contrast that workflow with predictive (classification) models: what changes in the request/response shape, what stays the same in your deployment manifest, and why distilled models like DistilBERT are a great fit for production classification tasks.

This guide covers:

* The conceptual difference between generative and predictive models
* Why request and response payloads differ
* How KServe keeps the InferenceService manifest stable across model types
* A brief introduction to model distillation and the DistilBERT sentiment classifier we'll deploy

<Frame>
  <img alt="The image shows a presentation agenda with three points: differentiating predictive models from generative models, explaining model type impacts on request/response formats, and describing KServe InferenceService manifest stability." />
</Frame>

## Generative vs Predictive — core concept

A generative model composes new content token-by-token. Example: you ask "Tell me about Kubernetes" and the model generates an explanatory paragraph. Its output space is effectively open-ended.

A predictive model, by contrast, maps inputs to a predefined set of labels. It answers questions like "Which bucket does this input belong to?" or "Which label best describes this input?" The output is a discrete set (e.g., ) or a probability distribution over those labels.

<Frame>
  <img alt="The image illustrates the core difference between generative and predictive models, showing input from a client going into a predictive model to determine which category it belongs to, resulting in output from a fixed set of answers." />
</Frame>

Common predictive examples:

* Spam filtering: label an email `spam` or `not_spam`.

<Frame>
  <img alt="The image illustrates a spam filtering process using a predictive model, showing email as input and classifying the output as either &#x22;Spam&#x22; or &#x22;Not spam.&#x22;" />
</Frame>

* Image classification: detect whether a photo contains a cat (`cat` / `no_cat`).
* Sentiment analysis: classify text as `positive` or `negative`.

The classifier we’ll deploy in this lesson performs sentiment analysis: it reads a sentence and predicts positive or negative sentiment. This is a canonical predictive task and useful to illustrate the differences from generative workflows.

<Frame>
  <img alt="The image displays a flowchart of a predictive model, where a client input (&#x22;This course has been great!&#x22;) is processed to produce either a positive or negative output. It illustrates how the model predicts outcomes based on given inputs." />
</Frame>

## Distillation — why DistilBERT?

Distillation trains a smaller "student" model to mimic a larger "teacher". The result is a compact model that approximates the teacher's behavior while using far less memory, CPU, and storage. Distilled models trade a small amount of accuracy for much lower inference cost — ideal for production classifiers.

<Frame>
  <img alt="The image explains distillation in machine learning, illustrating how a smaller model is trained to mimic a larger one, with visual representations of a large model, distillation process, and distilled model." />
</Frame>

The model we’ll use is:

* Name: `distilbert-base-uncased-finetuned-sst-2-english`
  * DistilBERT: lighter, faster variant of BERT
  * `uncased`: ignores case differences
  * `finetuned SST-2 English`: trained on the Stanford Sentiment Treebank (SST-2) for sentiment classification

When you send a sentence to this model it returns a label (positive/negative) and a confidence score. We pull the model directly from Hugging Face via an hf URI — no external object storage is required. The Hugging Face model URI is:
`hf://distilbert-base-uncased-finetuned-sst-2-english`

## KServe InferenceService — what stays the same

One of KServe's strengths is that the InferenceService manifest and predictor spec look the same whether you deploy a large generative model or a compact classifier. Only a few fields change: most notably the InferenceService `metadata.name` and the `storageUri` (model identifier). Resource requests/limits typically shrink for distilled classifiers.

Example InferenceService manifest (Hugging Face model):

```yaml theme={null}
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: sentiment-classifier
  namespace: kserve-inference
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      storageUri: "hf://distilbert-base-uncased-finetuned-sst-2-english"
      resources:
        requests:
          cpu: "500m"
          memory: "1Gi"
        limits:
          cpu: "1"
          memory: "2Gi"
```

Only a few manifest details differ compared to a generative model deployment:

* `metadata.name` — a descriptive name for the InferenceService
* `storageUri` — model identifier (e.g., the Hugging Face URI)
* `resources` — classifiers typically require smaller requests/limits than large generative LLMs

This consistency means you can reuse the same deployment workflow and tooling across generative and predictive models.

## Request / Response shape — what changes

The primary runtime difference is the inference payload. Generative models accept chat-style prompts (a list of messages, system and user roles) and produce open-ended text. Classifiers accept a single input (text or data tensor) and return a label or a probability distribution over labels.

Common payload examples (these are typical shapes — exact format depends on your predictor and KServe runtime configuration):

* Simple instances-style request:

```json theme={null}
{
  "instances": [
    "This course has been great!"
  ]
}
```

* Typical classifier response (probabilities for labels in fixed order `[negative, positive]`):

```json theme={null}
{
  "predictions": [
    [0.02, 0.98]
  ]
}
```

* Alternatively, some Hugging Face-style APIs return labeled results:

```json theme={null}
[
  {
    "label": "POSITIVE",
    "score": 0.9873
  }
]
```

<Frame>
  <img alt="The image compares &#x22;Qwen&#x22; and &#x22;Classifier&#x22; request formats, highlighting that Qwen uses chat-style prompts, accepts system and user messages, and generates text responses, whereas the Classifier takes plain text input and returns labels or categories without needing a conversation format." />
</Frame>

Note: the exact JSON keys (`instances` vs `inputs` vs a Hugging Face-specific shape) can differ by predictor and the chosen protocol (V1/V2). KServe docs and your runtime configuration specify the exact expected format.

> **lightbulb** Key takeaway: predictive models select from a predefined set of labels (e.g., positive/negative). KServe uses the same InferenceService manifest and runtime for both generative and predictive models; only the inference payload shape changes.

## Quick comparison: generative vs predictive

| Aspect          |               Generative Model | Predictive (Classifier)              |
| --------------- | -----------------------------: | ------------------------------------ |
| Output          |                 Free-form text | Fixed set of labels or probabilities |
| Input           |   Chat-style messages, prompts | Single text or tensor input          |
| Typical use     | Content generation, completion | Classification, detection, ranking   |
| Resource cost   |   Often very high (large LLMs) | Typically lower (distilled models)   |
| KServe manifest |      Same API & predictor spec | Same API & predictor spec            |

## Summary

* Predictive models map inputs to predefined labels rather than generating free-form content.
* DistilBERT (fine-tuned on SST-2) is a compact, production-friendly sentiment classifier.
* KServe keeps the InferenceService manifest and runtime consistent across different model types; only the model URI and resource sizing change.
* The main difference is the runtime payload format: generative models accept prompts/messages, while classifiers expect a single input and return labels or probability distributions.

Next: we'll deploy the sentiment classifier and demonstrate the exact request/response payloads for your KServe setup.

References:

* KServe documentation: [https://kserve.github.io](https://kserve.github.io)
* Hugging Face models: [https://huggingface.co](https://huggingface.co)
* Stanford Sentiment Treebank (SST-2): [https://nlp.stanford.edu/sentiment/](https://nlp.stanford.edu/sentiment/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kserve-fundamentals-serving-ml-models-on-kubernetes/module/d3f12b82-312d-4aee-a0bc-f5b313a63fd2/lesson/fa8f5ef0-41de-4835-854a-0971e79c2dae)
