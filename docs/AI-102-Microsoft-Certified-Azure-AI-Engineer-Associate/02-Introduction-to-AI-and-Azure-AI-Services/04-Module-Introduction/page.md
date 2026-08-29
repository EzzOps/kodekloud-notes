# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Introduction-to-AI-and-Azure-AI-Services/Module-Introduction/page

Overview of AI fundamentals, distinctions between AI, machine learning, and data science, and how Azure AI services and tools support building, deploying, and monitoring intelligent solutions.

Welcome to the first module: Introduction to AI and Azure AI Services.

In this lesson you will:

* Build a clear understanding of the fundamentals of artificial intelligence (AI).
* Learn how AI relates to — and differs from — related fields such as machine learning (ML) and data science.
* Explore the AI capabilities and services available in Microsoft Azure, and how they help you build, train, and deploy intelligent solutions without starting from scratch.

Why this matters

* Precise terminology and a clear mental model help you choose the right tools and design patterns for real-world systems.
* Understanding the boundaries between AI, ML, and data science reduces rework and speeds up solution delivery—from data ingestion and feature engineering to model training, inference, and monitoring.

At a high level:

* AI is the broad discipline of creating systems that perform tasks typically requiring human intelligence (perception, reasoning, language, and planning).
* Machine learning is a subset of AI focusing on algorithms that learn patterns and make predictions from data.
* Data science centers on collecting, preparing, analyzing, and visualizing data to extract insight and support ML model development.

<Frame>
  <img alt="A slide titled &#x22;Learning Objectives.&#x22; It lists two goals: understanding AI fundamentals and their relationship to machine learning and data science, and learning about Azure's AI capabilities and services." />
</Frame>

Azure provides a comprehensive set of managed services and tools that accelerate building intelligent solutions. Key capabilities include:

* Pre-built cognitive APIs for vision, speech, language, and decision-making (Azure Cognitive Services).
* End-to-end platforms for training, tracking, and managing models (Azure Machine Learning).
* Model hosting and scalable inference options (managed endpoints, containers, and serverless deployments).
* DevOps and MLOps features to operationalize models: continuous training, monitoring, and governance.

How these areas map to common tasks

| Concept                          | Primary role                                                                            | Azure services / tools                                         |
| -------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Data collection & preparation    | Ingest, clean, and transform raw data for analysis and training                         | Azure Data Factory, Azure Databricks, Azure Storage            |
| Feature engineering & analysis   | Explore data, create features, validate assumptions                                     | Azure Machine Learning, Jupyter notebooks, Databricks          |
| Model training & experimentation | Train models, tune hyperparameters, track experiments                                   | Azure Machine Learning, Automated ML                           |
| Pre-built AI capabilities        | Add vision, speech, language, or decision features without building models from scratch | Azure Cognitive Services (Computer Vision, Speech, Language)   |
| Model deployment & inference     | Host models for real-time or batch predictions                                          | Azure Machine Learning endpoints, AKS, Azure Functions         |
| Monitoring & governance          | Track performance, drift, and compliance in production                                  | Azure Monitor, Application Insights, Azure ML model monitoring |

What you’ll gain from this module

* A strong conceptual foundation: know when to use pre-built services vs. custom ML models.
* Practical guidance for mapping solution requirements to Azure services.
* An understanding of the typical lifecycle: data → model → deployment → monitoring.

<Callout icon="lightbulb">
  Tip: As you progress, focus on the role each area (AI, ML, data science) plays in a solution — from data collection and model training to deployment and monitoring — so you can choose the right Azure services for each stage.
</Callout>

Links and references

* Microsoft Azure AI documentation: [https://learn.microsoft.com/azure/ai-services](https://learn.microsoft.com/azure/ai-services)
* Azure Machine Learning overview: [https://learn.microsoft.com/azure/machine-learning/](https://learn.microsoft.com/azure/machine-learning/)
* Azure Cognitive Services overview: [https://learn.microsoft.com/azure/cognitive-services/](https://learn.microsoft.com/azure/cognitive-services/)
* Introduction to data science: [https://en.wikipedia.org/wiki/Data\_science](https://en.wikipedia.org/wiki/Data_science)

Recommended next steps

* Review the Azure Cognitive Services and Azure Machine Learning docs for quick-start guides.
* Practice by choosing a small dataset and prototyping a model with Azure Machine Learning or using a Cognitive Service API for inference.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/608629a7-1574-4eb2-95a4-f026fc8888b2/lesson/dff16f0f-873d-44f9-aa90-aac6b3ec4a73" />
</CardGroup>
