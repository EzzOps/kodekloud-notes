# 
# Keep your API key secure. Do not commit it to source control.
# 1. Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 2. Suffix to enforce confident answers or “I don't know”
suffix = " answer only if you know it. Otherwise say 'I don't know'\n\n###\n\n"

# 3. Replace with your fine-tuned model ID
model_id = "davinci:ft-janakiram-associates:sotu-qna-2023-08-05-17-12-17"

# 4. Define prompts
questions = [
    "Who presented the State of the Union?",
    "When was the State of the Union presented?",
    "What is the key takeaway from the domestic policy?",
    "What positive trends in the US economy did President Biden highlight?",
    "What message did President Biden send to Republicans in his 2023 SOTU?"
]

# 5. Invoke the model for each question
for prompt in questions:
    response = openai.Completion.create(
        model=model_id,
        prompt=prompt + suffix,
        max_tokens=500,
        temperature=0,
        frequency_penalty=2.0,
        stop=["END", "***"]
    )
    answer = response.choices[0].text.strip()
    print(f"Q: {prompt}\nA: {answer}\n")
```

### Key Parameters

| Parameter           | Purpose                                 | Example Value   |
| ------------------- | --------------------------------------- | --------------- |
| `max_tokens`        | Max length of the generated answer      | `500`           |
| `temperature`       | Controls randomness (0 = deterministic) | `0`             |
| `frequency_penalty` | Reduces repeated phrases                | `2.0`           |
| `stop`              | Tokens where generation halts           | `["END","***"]` |

***

## 4. Why This Approach Works

* **Self-contained inference**: The model depends solely on its fine-tuned parameters—no external context injection.
* **Controlled output**: A suffix forces the model to admit uncertainty, preventing hallucinations.
* **Batchable prompts**: Easily loop through multiple questions without managing conversational state.

With these examples, you can seamlessly integrate your fine-tuned OpenAI model into command-line tools, Jupyter notebooks, or production services. Apply the same pattern to tasks like summarization or classification by adjusting the training dataset and prompts.

***

## Links and References

* [OpenAI API Reference](https://platform.openai.com/docs/api-reference/completions)
* [Fine-Tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
* [Authentication](https://platform.openai.com/docs/api-reference/authentication)

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/bdd763d1-210d-41de-a60c-607b722e7afe/lesson/edf343a6-eda3-49ae-918b-7cae35254b21)


# Section Intro

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Fine-tuning-GPT-3-with-a-Custom-Dataset/Section-Intro/page

This article explains fine-tuning large language models on custom datasets for improved accuracy and context-aware responses in specialized domains.

## Introduction to Fine-Tuning Custom Datasets

Fine-tuning enables you to adapt large language models (LLMs) to specialized domains by training them on your own data. While dynamic context injection customizes outputs at inference time, fine-tuning updates the model’s parameters so it “remembers” your unique content permanently. This approach ensures more accurate, context-aware responses for queries outside the model’s original training set.

### What You’ll Learn in This Section

1. Definition of fine-tuning
2. Importance and use cases
3. Step-by-step fine-tuning workflow
4. Cost estimation strategies
5. Executing the fine-tuning process
6. Deploying and calling your fine-tuned model

We’ll start by exploring **why** fine-tuning is critical, then move quickly into a hands-on demo. Let’s dive in!

> **lightbulb** Make sure you have:

  * An OpenAI API key
  * A structured dataset in JSONL or CSV format
  * The `openai` Python package installed (`pip install openai`)

| Topic                   | Description                                      | Example Command                                 |
| ----------------------- | ------------------------------------------------ | ----------------------------------------------- |
| Data Preparation        | Formatting training data in JSONL/CSV            | N/A                                             |
| Fine-Tuning Job Launch  | Starting the fine-tuning process via API or CLI  | `openai api fine_tunes.create …`                |
| Monitoring & Evaluation | Tracking job status and assessing model accuracy | `openai api fine_tunes.get -i <JOB_ID>`         |
| Deployment              | Loading your custom model for inference          | `openai.ChatCompletion.create(model="ft-…", …)` |

## Why Fine-Tuning Matters

Fine-tuning yields models that:

* Understand niche terminology (e.g., legal, medical)
* Maintain consistent tone and formatting
* Improve accuracy on domain-specific tasks

Unlike prompt engineering alone, a fine-tuned model will not “forget” your custom logic or examples.

***

Proceed to the next sections for a detailed walkthrough of each step, from data formatting to deploying your specialized model.

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/bdd763d1-210d-41de-a60c-607b722e7afe/lesson/bc6c0cbb-ab9b-47d7-9cbf-e830fc01956c)
