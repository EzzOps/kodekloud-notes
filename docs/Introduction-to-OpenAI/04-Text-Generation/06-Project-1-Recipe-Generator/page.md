# Project 1 Recipe Generator

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Project-1-Recipe-Generator/page

Build a dynamic recipe creator using OpenAI’s GPT-4 model that generates chef-quality recipes based on user-provided ingredients.

Build a dynamic recipe creator using OpenAI’s GPT-4 model. Enter a list of ingredients, and the application returns a chef-quality recipe tailored to your inputs.

## Prerequisites

Before you begin, ensure you have:

* Python 3.7+ installed
* An OpenAI API key (keep this secret!)

> **triangle-alert** Never hardcode your API key in source files. Use environment variables or a secrets manager.

### Install the OpenAI Python SDK

```bash theme={null}
pip install openai
```

### Configure Your API Key

Export your key as an environment variable:

```bash theme={null}
export OPENAI_API_KEY="sk-your-api-key-here"
```

Or set it programmatically:

```python theme={null}
import os
os.environ["OPENAI_API_KEY"] = "sk-your-api-key-here"
```

## Collecting Ingredients

Prompt users to input ingredients one at a time. Type `done` to finish:

```python theme={null}
ingredients = []

while True:
    item = input("Enter an ingredient (or 'done' to finish): ").strip()
    if item.lower() == "done":
        break
    ingredients.append(item)
```

## Defining the Recipe Generator Function

Create `recipe_gen()` to format messages for GPT-4 and request a chat completion.

```python theme={null}
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def recipe_gen(ingredients: list[str]) -> str:
    messages = []

    # Add each ingredient as a user message
    for ing in ingredients:
        messages.append({"role": "user", "content": ing})

    # Instruct the model
    messages.extend([
        {"role": "system", "content": "Provide a concise, structured recipe."},
        {
            "role": "assistant",
            "content": "You are a professional chef. Generate a detailed recipe using the above ingredients."
        }
    ])

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=400,
        temperature=0.8
    )

    return response.choices[0].message.content
```

## Chat Completion Parameters

| Parameter   | Description                                | Example   |
| ----------- | ------------------------------------------ | --------- |
| model       | GPT model to use                           | `"gpt-4"` |
| messages    | Conversation history as role/content pairs | See above |
| max\_tokens | Maximum tokens in the response             | `400`     |
| temperature | Sampling randomness (0.0–1.0)              | `0.8`     |

## Running the Generator

Once ingredients are collected, invoke `recipe_gen()` and display the result:

```python theme={null}
if ingredients:
    recipe = recipe_gen(ingredients)
    print("\n=== Generated Recipe ===\n")
    print(recipe)
else:
    print("No ingredients provided. Please try again.")
```

## Example Session

```bash theme={null}
$ python recipe_generator.py
Enter an ingredient (or 'done' to finish): apples
Enter an ingredient (or 'done' to finish): grapes
Enter an ingredient (or 'done' to finish): chicken
Enter an ingredient (or 'done' to finish): chocolate
Enter an ingredient (or 'done' to finish): done

=== Generated Recipe ===

Chocolate-Glazed Chicken with Apple & Grape Compote

Ingredients:
- 4 boneless chicken breasts
- 2 apples, peeled & diced
- 1 cup grapes, halved
- 100g dark chocolate, melted
- 1 tbsp olive oil
- 1 tsp balsamic vinegar
- 1 tsp honey
- Salt & pepper to taste

Instructions:
1. Season chicken with salt and pepper.
2. Sear in olive oil over medium-high heat until cooked through.
3. Mix melted chocolate, vinegar, and honey; brush onto chicken.
4. Sauté apples in butter with brown sugar until soft. Add grapes and simmer 3–4 min.
5. Plate chicken and top with fruit compote. Serve warm.
```

## References

* [OpenAI Python SDK](https://pypi.org/project/openai/)
* [OpenAI Chat Completion API](https://platform.openai.com/docs/api-reference/chat)
* [Environment Variables Best Practices](https://12factor.net/config)

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/0a1d2217-48a0-4d70-9370-9a6ec4408e35)
