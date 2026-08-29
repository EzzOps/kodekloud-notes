# Training Testing Publishing and Reviewing

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Conversational-Language-Understanding-App/Training-Testing-Publishing-and-Reviewing/page

Lifecycle guide for conversational language understanding models covering training, testing, publishing, monitoring, and retraining to improve intent detection and entity extraction.

Training, testing, publishing, and reviewing compose the complete lifecycle of a conversational language understanding model. This lesson walks through that lifecycle step by step so you can build, validate, and maintain an accurate conversational AI.

Training is the foundation. In this phase you teach the model using labeled utterances — realistic user statements tagged with intents and entities. Training data is typically provided as a JSON file and uploaded to the training service to create the model.

<Frame>
  <img alt="A presentation slide titled &#x22;Training, Testing, Publishing, and Reviewing&#x22; showing a circular workflow graphic with a green arrow highlighting &#x22;Model Training&#x22; and the text &#x22;Teach the model using labeled utterances.&#x22;" />
</Frame>

Example: the utterance "I want to order a large pepperoni pizza" is labeled with the intent OrderPizza and entity annotations for size and type. These labels teach the model how to map natural language to structured actions and data (intents and entities).

Once a model is trained, validate it by running test queries and reviewing the predictions. Lightweight tests can be executed inside the portal or via the API to confirm the predicted intent and the entities extracted.

If you use the portal's Testing Deployments option, enter a sample utterance such as "Where is my order?", select the deployment, and run the test. The UI displays the top intent and any detected entities.

<Frame>
  <img alt="A screenshot of the Azure AI Studio &#x22;Testing deployments&#x22; page for a PizzaOrderProject, showing a deployment named &#x22;pizza-model-deployment.&#x22; The sample utterance &#x22;Where is my order?&#x22; is entered and the model predicts the intent &#x22;CheckStatus&#x22; with about 75% confidence and no entities detected." />
</Frame>

You can also inspect the detailed JSON response returned by the prediction endpoint. For example, testing the utterance "Send me a pizza, large veggie, to 123 Main St" might produce:

```json theme={null}
{
  "query": "Send me a pizza, large veggie, to 123 Main St",
  "prediction": {
    "topIntent": "OrderPizza",
    "projectKind": "Conversation",
    "intents": [
      {
        "category": "OrderPizza",
        "confidenceScore": 0.8656
      },
      {
        "category": "CheckStatus",
        "confidenceScore": 0.6436
      },
      {
        "category": "CancelOrder",
        "confidenceScore": 0.1778
      },
      {
        "category": "None",
        "confidenceScore": 0.0
      }
    ],
    "entities": [
      {
        "category": "size",
        "text": "large",
        "offset": 16,
        "length": 5,
        "confidenceScore": 1.0
      },
      {
        "category": "address",
        "text": "123 Main St",
        "offset": 30,
        "length": 11,
        "confidenceScore": 0.98
      }
    ]
  }
}
```

In this response the model correctly determines that the top intent is OrderPizza and extracts the size and address entities, but it missed the pizza type ("veggie"). That signals a gap in the training data: add more labeled examples that include pizza types in varied contexts so the model can learn to extract the type reliably.

After validation, publish the model to create an API endpoint. Publishing (or deploying) exposes the model so client applications — chatbots, websites, voice assistants — can call it in real time.

<Frame>
  <img alt="A presentation slide titled &#x22;Training, Testing, Publishing, and Reviewing&#x22; featuring a circular arrow diagram with the &#x22;Deployment&#x22; segment highlighted in orange and an icon. The slide's caption reads: &#x22;Publish as an API endpoint for applications.&#x22;" />
</Frame>

Deployment considerations:

* Provide a stable endpoint and API key to client applications.
* Monitor latency and throughput to ensure acceptable user experience.
* Version your deployments so you can roll back or test improvements safely.

Continuous improvement is essential: model performance decays if it isn't updated to reflect real-world usage. Monitor production traffic, collect misclassified or unrecognized utterances, label them, and retrain the model on a regular cadence.

> **lightbulb** Monitor production requests and log misclassified utterances so you can add them to your training set and retrain the model. Small, frequent updates help the model adapt to real-world usage.

For example, when users ask "What's going on with my pizza?" and the model fails to return CheckStatus, add that utterance as a labeled CheckStatus example and retrain. The iterative loop — train, test, deploy, monitor, and retrain — keeps accuracy high as usage evolves.

<Frame>
  <img alt="A presentation slide titled &#x22;Training, Testing, Publishing, and Reviewing&#x22; showing a circular process diagram. One segment is highlighted as &#x22;Continuous Improvement&#x22; with the caption &#x22;Analyze, adjust, and retrain for accuracy.&#x22;" />
</Frame>

Quick lifecycle reference

| Stage   | Purpose                                            | Practical actions / examples                                   |
| ------- | -------------------------------------------------- | -------------------------------------------------------------- |
| Train   | Teach model intents and entities from labeled data | Upload JSON training file with diverse utterances              |
| Test    | Validate predictions and inspect JSON responses    | Use portal testing or prediction API; review confidence scores |
| Publish | Expose model as an API for client applications     | Create a deployment endpoint and manage versions               |
| Review  | Monitor production, collect failures, and retrain  | Log misclassifications, add labels, retrain on a cadence       |

Helpful links and references

* Azure Language Service and AI Studio: [https://learn.microsoft.com/azure/cognitive-services/language-service/](https://learn.microsoft.com/azure/cognitive-services/language-service/)
* Best practices for conversational AI datasets: [https://learn.microsoft.com/azure/ai-services](https://learn.microsoft.com/azure/ai-services)

Summary checklist to create a robust conversational model:

* Train on diverse, well-labeled utterances that cover different phrasing and edge cases.
* Validate with representative inputs and inspect intent scores and entities.
* Deploy the model as a versioned API endpoint for integration.
* Continuously monitor production traffic, label new examples, and retrain frequently.

Following this lifecycle ensures your conversational language understanding system improves over time and remains accurate in production. This completes the conversational language understanding lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/3b91e872-14ae-4fc5-bdad-5c0927439d61/lesson/29162622-2c9b-4425-9b7e-9113f43ad4ed)
