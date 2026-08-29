# Project 1 Image Generator

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Vision/Project-1-Image-Generator/page

Generate stunning visuals using OpenAI’s DALL·E 3 with this step-by-step guide for installation, setup, and examples in Python.

Harness the power of OpenAI’s DALL·E 3 to generate stunning visuals from simple text prompts. This step-by-step guide walks you through installation, setup, and examples to help you build your own image generator in Python.

## Table of Contents

1. [Install the OpenAI Python SDK](#install-the-openai-python-sdk)
2. [Initialize the OpenAI Client](#initialize-the-openai-client)
3. [Define a Helper Function](#define-a-helper-function)
4. [Generate Your First Image](#generate-your-first-image)
5. [Experiment with Custom Prompts](#experiment-with-custom-prompts)
6. [Supported Image Sizes](#supported-image-sizes)
7. [Links and References](#links-and-references)

***

## Install the OpenAI Python SDK

First, install the official OpenAI Python package:

```bash theme={null}
pip install openai
```

<Callout icon="lightbulb">
  You can also pin a specific version for reproducibility:

  ```bash theme={null}
  pip install openai==0.27.0
  ```
</Callout>

***

## Initialize the OpenAI Client

Import and initialize the client using your API key. We recommend storing your key in an environment variable for security.

```python theme={null}
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
```

<Callout icon="triangle-alert">
  Never hard-code your API key in source files. Use environment variables or a secrets manager.
</Callout>

***

## Define a Helper Function

Create a reusable function that sends a prompt to DALL·E 3 and returns the URL of the generated image:

```python theme={null}
def generate_image(prompt: str, size: str = "1024x1024") -> str:
    """
    Generate an image from a text prompt using DALL·E 3.

    Args:
        prompt: Descriptive text for the image.
        size: One of '256x256', '512x512', or '1024x1024'.

    Returns:
        URL of the generated image.
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size
    )
    return response.data[0].url
```

***

## Generate Your First Image

Use the helper function in a standalone script:

```python theme={null}
if __name__ == "__main__":
    prompt = "A person playing golf on Mars with friendly aliens"
    image_url = generate_image(prompt, size="1024x1024")
    print("Generated Image URL:", image_url)
```

Run it:

```bash theme={null}
python example.py
