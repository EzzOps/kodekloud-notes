# Initialize the OpenAI client using an environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

## 2. Load Fitness Data

Load your CSV dataset containing sleep, health, and lifestyle metrics. Update the file path as needed:

```python theme={null}
# Load the fitness dataset
df = pd.read_csv("/path/to/Sleep_health_and_lifestyle_dataset.csv")
```

> **lightbulb** Ensure the CSV file has columns like `sleep_duration`, `diet_quality`, and `stress_level` for best results.

## 3. Collect User Health Goals

Prompt the user to enter one or more goals. Type `done` to finish:

```python theme={null}
def get_user_goals():
    goals = []
    while True:
        goal = input("Enter a health goal (type 'done' when finished): ").strip()
        if goal.lower() == "done":
            break
        goals.append(goal)
    return goals

goals = get_user_goals()
```

## 4. Define the Trainer Function

This function builds a chat prompt from user goals and context, then calls the OpenAI chat completion API:

```python theme={null}
def trainer(goals, df):
    messages = []

    # Add user goals
    for goal in goals:
        messages.append({"role": "user", "content": goal})

    # System instructions
    messages.extend([
        {"role": "system", "content": "Provide concise, bullet-point recommendations."},
        {
            "role": "assistant",
            "content": (
                "You are a health expert advising an accountant. "
                "Be technical, specific, and offer actionable steps."
            )
        }
    ])

    # Call the GPT-4 model
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.8
    )

    return response.choices[0].message.content
```

> **triangle-alert** API calls may incur costs. Monitor your usage on the [OpenAI dashboard][openai-dashboard].

## 5. Main Execution

Invoke the trainer function and display recommendations:

```python theme={null}
if __name__ == "__main__":
    recommendations = trainer(goals, df)
    print("\nPersonal Trainer Recommendations:\n")
    print(recommendations)
```

## 6. Example Run

```bash theme={null}
$ python3 personal_trainer.py
Enter a health goal (type 'done' when finished): weight loss
Enter a health goal (type 'done' when finished): healthier diet
Enter a health goal (type 'done' when finished): stress reduction
Enter a health goal (type 'done' when finished): done

Personal Trainer Recommendations:

• Sleep Duration: Aim for 7–8 hours/night (current average: 6.2h)  
• Dietary Adjustments:
  – Reduce simple carbs by 20%  
  – Increase protein at breakfast  
• Exercise Plan:
  – 3× weekly circuit training sessions (30 min)  
  – 2× yoga or meditation sessions for stress control  
• Stress Management:
  – Implement 5-minute mindfulness breaks every 2 hours  
  – Track HRV trends; maintain ≥50 ms daily  
```

## Links and References

* [OpenAI Python SDK][openai-sdk]
* [pandas Documentation][pandas-docs]
* [OpenAI Dashboard][openai-dashboard]

[openai-sdk]: https://pypi.org/project/openai/

[pandas-docs]: https://pandas.pydata.org/

[openai-dashboard]: https://platform.openai.com/account/usage

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/63b8c65f-2957-476f-bc52-f8e932bc166d)


# Prompt Engineering

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Prompt-Engineering/page

This guide teaches how to create effective prompts for generative AI models to enhance output quality and task-specific performance.

In this guide, you’ll learn how to craft effective prompts that steer generative models—like OpenAI’s GPT-4—to deliver clear, accurate, and relevant outputs. Well-designed prompts minimize ambiguity, speed up iteration, and improve task-specific performance.

## Why Prompt Engineering Matters

Generative AI can tackle diverse tasks, but the clarity and structure of your prompt determine the quality of the response:

* Control over tone and format
* Precision to reduce vague answers
* Faster convergence on desired results
* Enhanced performance in specialized domains (e.g., legal, technical)

![The image outlines the importance of prompt engineering, highlighting four key benefits: control over output, reduced ambiguity, faster results, and task-specific performance.](https://kodekloud.com/kk-media/image/upload/v1752879242/notes-assets/images/Introduction-to-OpenAI-Prompt-Engineering/prompt-engineering-benefits-outline.jpg)

## Core Principles

### Clarity & Specificity

Make requests explicit to avoid off-target or incomplete answers.

![The image compares vague and specific prompts about solar energy, highlighting the importance of clarity and specificity in instructions.](https://kodekloud.com/kk-media/image/upload/v1752879243/notes-assets/images/Introduction-to-OpenAI-Prompt-Engineering/solar-energy-prompt-comparison-clarity.jpg)

Example of a precise prompt:

```python theme={null}
prompt = (
    "Explain how photovoltaic cells in solar panels convert sunlight "
    "into electricity. Include details about photons and electron movement."
)
```

### Using Constraints

Define style, length, or format to shape output consistency.

![The image shows a comparison between vague and specific prompts for summarizing photosynthesis, highlighting the importance of clarity and specificity in instructions.](https://kodekloud.com/kk-media/image/upload/v1752879244/notes-assets/images/Introduction-to-OpenAI-Prompt-Engineering/prompts-comparison-photosynthesis-summary.jpg)

Example with formatting constraints:

```python theme={null}
prompt = (
    "Summarize how photosynthesis works in three sentences "
    "using simple language and bullet points."
)
```

> **lightbulb** Use bullet points, word limits, or tone specifications (e.g., formal vs. conversational) to guide the model’s style.

### System Messages

In chat-based setups, system instructions define the model’s role and behavior before user input.

![The image provides guidance on using system instructions for defining a model's role, contrasting a bad prompt with a good prompt for explaining gradient descent.](https://kodekloud.com/kk-media/image/upload/v1752879245/notes-assets/images/Introduction-to-OpenAI-Prompt-Engineering/gradient-descent-prompt-guidance-diagram.jpg)

Example of a system-level prompt:

```text theme={null}
System: You are a technical expert in machine learning.
User: Explain gradient descent in simple terms, using an analogy.
```

### Step-by-Step Prompts

Break down complex tasks into sequential steps for transparency and logical flow.

Example:

```python theme={null}
prompt = (
    "Explain the process of solving a linear equation step by step. "
    "Include a simple example."
)
```

## Advanced Techniques

### Few-Shot Learning

Provide annotated examples within the prompt to demonstrate desired format and style.

![The image explains "Few-Shot Prompts," showing how providing examples in prompts can guide a model's understanding, with examples related to AI in healthcare and renewable energy.](https://kodekloud.com/kk-media/image/upload/v1752879246/notes-assets/images/Introduction-to-OpenAI-Prompt-Engineering/few-shot-prompts-ai-healthcare-energy.jpg)

Example few-shot prompt:

```python theme={null}
prompt = """
Summarize the following articles.

Example 1:
Article: "AI in Healthcare..."
Summary: "Artificial intelligence is transforming patient diagnostics..."

Example 2:
Article: "Renewable Energy Trends..."
Summary: "Solar and wind power are growing at..."

Now summarize the article: "The impact of blockchain on finance."
"""
```

### Zero-Shot Prompts

Rely on explicit instructions without examples—best for straightforward tasks.

Example:

```python theme={null}
prompt = "Summarize the article 'The future of renewable energy.'"
```

### Chain-of-Thought Prompting

Encourage the model to “think aloud,” revealing intermediate reasoning steps for complex queries.

![The image is about "Chain-of-Thought Prompting," highlighting its benefits in encouraging models to think aloud and generate logical answers, with an example related to calculating the area of a triangle.](https://kodekloud.com/kk-media/image/upload/v1752879247/notes-assets/images/Introduction-to-OpenAI-Prompt-Engineering/chain-of-thought-prompting-benefits.jpg)

Example:

```python theme={null}
prompt = (
    "Describe how to calculate the area of a triangle step by step. "
    "Start by explaining the formula clearly."
)
```

## Common Pitfalls & Solutions

> **triangle-alert** Avoid these mistakes to get the most reliable and focused outputs.

| Mistake             | Why It Happens                                           | How to Fix                                                            |
| ------------------- | -------------------------------------------------------- | --------------------------------------------------------------------- |
| Vague prompts       | Too broad or unspecific                                  | Specify topic, audience, and depth requirements                       |
| Missing constraints | No length, tone, or format guidelines                    | Add word limits, bullet points, or style instructions                 |
| Untested parameters | Default settings (temperature, top\_p) may not suit task | Experiment with lower temperature for accuracy, higher for creativity |
| Ignoring context    | Critical details left out                                | Provide background: audience, purpose, format, and relevant data      |

## Further Reading & Resources

* [OpenAI Prompt Design Guide](https://platform.openai.com/docs/guides/prompt-design)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Terraform Registry](https://registry.terraform.io/)

By applying these strategies—clarity, constraints, structured examples, and iterative testing—you’ll consistently produce high-quality, relevant responses from generative AI models.

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/818013b8-5333-4ac1-abad-64f0e855f943)
