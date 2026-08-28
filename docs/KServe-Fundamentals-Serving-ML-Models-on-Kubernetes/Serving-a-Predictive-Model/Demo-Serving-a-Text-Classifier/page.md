# Demo Serving a Text Classifier

Source: https://notes.kodekloud.com/docs/KServe-Fundamentals-Serving-ML-Models-on-Kubernetes/Serving-a-Predictive-Model/Demo-Serving-a-Text-Classifier/page

Guide to deploying and testing a DistilBERT sentiment classifier on KServe with a manifest, port forwarding, OIP inference requests, and interpreting class probability responses.

Earlier we reviewed model distillation, inspected the manifest for our sentiment-classifier, and compared its structure to the Qwen deployment we examined previously. The overall layout and resources are nearly identical; the primary differences come from the runtime type and the inference protocol used by a classifier versus a conversational model.

<Frame>
  <img alt="The image is a promotional slide titled &#x22;Demo: Serving a Text Classifier&#x22; with a rocket icon launching from a laptop on a dark blue background." />
</Frame>

This demo uses a manifest named `sentiment-classifier.yaml`. It creates an `InferenceService` called `sentiment-classifier` in the `kserve-inference` namespace and selects the Hugging Face runtime to load a DistilBERT-based model. The manifest includes a startup arg (for example `--return_all_scores`) so the runtime returns probability scores for each class (both negative and positive) instead of only the single winning class — that extra detail is visible in the response.

Apply the manifest to the cluster:

```bash theme={null}
less sentiment-classifier.yaml
kubectl apply -f sentiment-classifier.yaml
