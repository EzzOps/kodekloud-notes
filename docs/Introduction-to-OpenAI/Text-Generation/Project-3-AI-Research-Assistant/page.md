# Sample article text in Japanese
article = (
    "監視機器大手オリンパスの前社長CEC【高橋雄資】は、警視庁は、"
    "自然なカメラマンの金賞受賞者として、東京の都庁と同社の営業法違反の疑いで通報し、"
    "8日発表した。"
)

# Build the translation prompt
prompt = f"Translate the following article into English:\n\n{article}"
```

<Callout icon="lightbulb">
  You can replace the hard-coded `article` variable with any string input or file contents for batch translation.
</Callout>

***

## 4. Define the Translator Function

Create a reusable function that sends the system and user messages to the chat completion endpoint.\
A low `temperature` (e.g., 0.1) ensures a faithful translation.

```python theme={null}
def article_translator(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional translator specializing in news articles. "
                    "Provide a direct, accurate English translation without commentary."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content
```

### API Parameters Overview

| Parameter     | Description                             | Example       |
| ------------- | --------------------------------------- | ------------- |
| `model`       | The chat model to use                   | `"gpt-4"`     |
| `messages`    | Conversation history with roles         | List of dicts |
| `temperature` | Controls randomness (0 = deterministic) | `0.1`         |

***

## 5. Run the Translator

Execute the script and print the translated text.

```python theme={null}
if __name__ == "__main__":
    translation = article_translator(prompt)
    print(translation)
```

```plaintext theme={null}
$ python translate_article.py
The Tokyo Metropolitan Police Department announced on the 8th that they reported Yusuke Takahashi, 
former president of major surveillance-equipment manufacturer Olympus, on suspicion of violating commercial 
law by acting as an unauthorized cameraman prize judge in Tokyo’s Metropolitan Government Building. 
The department says their investigation will continue carefully.
```

***

## What's Next?

* Batch-translate multiple articles
* Scrape article URLs automatically before translation
* Summarize translated content or detect sentiment

## Links and References

* [OpenAI Python SDK](https://github.com/openai/openai-python)
* [Chat Completion API Docs](https://platform.openai.com/docs/api-reference/chat)
* [Environment Variables Best Practices](https://12factor.net/config)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/d8712d1a-af45-4f6a-b138-47f41d7b18df" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/0556be30-c3c7-41cc-95a8-e2e9040f33a3" />
</CardGroup>


# Project 3 AI Research Assistant

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Project-3-AI-Research-Assistant/page

Learn to analyze CSV datasets with pandas and the OpenAI API to extract structured insights.

Learn how to analyze CSV datasets with pandas and the OpenAI API to extract structured, point-form insights.

## Prerequisites

| Requirement    | Version / Link                                                                               |
| -------------- | -------------------------------------------------------------------------------------------- |
| Python         | 3.7+                                                                                         |
| OpenAI API Key | [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys) |
| pandas         | [https://pandas.pydata.org/](https://pandas.pydata.org/)                                     |
| OpenAI SDK     | [https://pypi.org/project/openai/](https://pypi.org/project/openai/)                         |

## Installation

Install both pandas and the OpenAI Python client:

```bash theme={null}
pip install pandas openai
```

<Callout icon="lightbulb">
  If you already have these packages installed, pip will confirm that the requirements are satisfied.
</Callout>

## Configuration

Import the necessary modules and initialize your OpenAI client.\
**Warning:** Never commit your API key to version control.

```python theme={null}
from openai import OpenAI
import pandas as pd

client = OpenAI(api_key="YOUR_API_KEY")
```

Replace `"YOUR_API_KEY"` with your actual key or load it from an environment variable.

## Loading Your CSV Dataset

Download a CSV (for example, from [Kaggle](https://www.kaggle.com)) and load it into a pandas DataFrame:

```python theme={null}
df = pd.read_csv("/path/to/your/user_behavior_dataset.csv")
```

Adjust the file path to match your local environment.

## Defining the Analysis Function

This function converts the DataFrame to CSV text, invokes the GPT-4 model, and returns the AI-generated insights:

```python theme={null}
def analyze_data(df):
    csv_content = df.to_csv(index=False)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a research assistant. "
                    "Provide key insights from the following dataset in bullet points:\n"
                    f"{csv_content}"
                )
            }
        ],
        max_tokens=500,
        temperature=0.2
    )
    return response.choices[0].message.content
```

### API Call Parameters

| Parameter   | Description                                      | Example   |
| ----------- | ------------------------------------------------ | --------- |
| model       | OpenAI model to use                              | `"gpt-4"` |
| max\_tokens | Maximum tokens in the response                   | `500`     |
| temperature | Controls randomness; lower is more deterministic | `0.2`     |

## Running the Assistant

Invoke the function and print the summary:

```python theme={null}
if __name__ == "__main__":
    summary = analyze_data(df)
    print(summary)
```

You’ll see a concise, bullet-pointed list of insights extracted from your dataset.

## Focusing on Demographics

To target only demographic columns (e.g., age, gender, country), filter before sending:

```python theme={null}
def analyze_demographics(df):
    demo_df = df[['age', 'gender', 'country']]
    csv_content = demo_df.to_csv(index=False)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a research assistant. "
                    "Provide key demographic insights from the following data in bullet points:\n"
                    f"{csv_content}"
                )
            }
        ],
        max_tokens=300,
        temperature=0.2
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    demographics_summary = analyze_demographics(df)
    print(demographics_summary)
```

This returns focused insights on age distribution, gender breakdown, and geographic diversity.

## Conclusion

You’ve now built an AI research assistant that:

1. Installs and imports pandas & OpenAI SDK.
2. Loads a CSV into a DataFrame.
3. Sends your data to GPT-4.
4. Returns structured, point-form insights.

Feel free to tweak prompts, adjust parameters, or analyze other subsets of your data.

## Links & References

* [OpenAI Python SDK](https://pypi.org/project/openai/)
* [pandas Documentation](https://pandas.pydata.org/)
* [Kaggle Datasets](https://www.kaggle.com/datasets)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/6d442303-fde3-4cc4-8bad-af6115785fe8" />
</CardGroup>
